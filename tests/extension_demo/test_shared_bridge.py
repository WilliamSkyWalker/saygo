"""Desktop and WSL must agree on one Windows native-messaging directory."""
import os
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

from saygo.integrations import browser_setup, browser_location as location
from saygo.integrations.browser_bridge import atomic_json, read_frame, write_frame


class SharedBridgeTests(unittest.TestCase):
    def test_native_windows_fresh_install_uses_the_wsl_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            local = root / 'AppData/Local'
            expected = local / 'Saygo/browser-bridge'
            with patch('pathlib.Path.home', return_value=root), \
                 patch.dict(os.environ, {'LOCALAPPDATA':str(local)}), \
                 patch('saygo.devices.mobile_host.is_wsl', return_value=False), \
                 patch.object(location, '_layout', wraps=ORIGINAL_LAYOUT), \
                 patch.object(location, '_windows_info', return_value={'home':str(root), 'local':str(local), 'manifest':None}), \
                 patch.object(browser_setup.sys, 'platform', 'win32'), \
                 patch('saygo.integrations.browser_bridge.install', return_value={'directory':str(expected)}) as install:
                browser_setup.setup('a' * 32)
            self.assertEqual(Path(install.call_args.args[0]), expected)

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='saygo shared 中文 ')
        self.addCleanup(temporary.cleanup)
        # Windows runners may spell TEMP with an 8.3 user alias (RUNNER~1).
        # Production OS discovery returns canonical paths; injected layouts must too.
        self.root = Path(temporary.name).resolve()
        self.standard = self.root / 'AppData/Local/Saygo/browser-bridge'
        self.legacy = self.root / '.saygo/browser-bridge'
        self.registration = self.root / 'registry/com.saygo.browser.json'
        self.registration.parent.mkdir(parents=True)
        layout = patch.object(location, '_layout', return_value=(self.standard, self.legacy, self.registration))
        layout.start(); self.addCleanup(layout.stop)
        wsl = patch('saygo.devices.mobile_host.is_wsl', return_value=False)
        wsl.start(); self.addCleanup(wsl.stop)

    def register(self, directory, identity='a' * 32):
        directory.mkdir(parents=True, exist_ok=True)
        atomic_json(self.registration, {'name':'com.saygo.browser', 'type':'stdio',
            'path':str(directory / 'host.cmd'), 'allowed_origins':[f'chrome-extension://{identity}/']})

    def host(self, directory):
        """Real native-host subprocess and IPC; the framed extension peer is synthetic."""
        host_script = Path(__file__).resolve().parents[2] / 'saygo/integrations/browser_bridge.py'
        proc = subprocess.Popen([sys.executable, str(host_script),
            'host', '--directory', str(directory)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        read_frame(proc.stdout)
        write_frame(proc.stdin, {'type':'hello','protocol':1,'version':'test'})
        seen, failures = [], []
        def peer():
            try:
                while True:
                    request = read_frame(proc.stdout)
                    seen.append(request['operation'])
                    if request['operation'] != 'pages':
                        raise AssertionError('Discovery must never send input')
                    write_frame(proc.stdin, {'id':request['id'], 'last':True,
                        'chunk':json.dumps({'result':[{'page_id':'browser:7','url':'https://fixture.test'}]})})
            except EOFError:
                pass
            except Exception as exc:
                failures.append(exc)
        worker = threading.Thread(target=peer, daemon=True); worker.start()
        def stop():
            proc.stdin.close()
            proc.wait(timeout=5); worker.join(2)
            proc.stdout.close(); proc.stderr.close()
            self.assertFalse(failures, failures)
        self.addCleanup(stop)
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            if proc.poll() is not None:
                self.fail('Native host exited: ' + proc.stderr.read().decode('utf-8', errors='replace'))
            status = directory / 'status.json'
            if status.exists() and json.loads(status.read_text()).get('connected'):
                return proc, seen
            time.sleep(.01)
        self.fail('Native host did not become connected')

    def test_fresh_desktop_and_wsl_choose_same_directory(self):
        self.assertEqual(location.resolve_directory(), self.standard)
        self.assertEqual(location.resolve_directory(self.standard), self.standard)

    def test_wsl_maps_the_browser_user_profile_and_registration(self):
        info = {'home':r'C:\Users\browser-user', 'local':r'C:\Users\browser-user\AppData\Local',
                'manifest':r'C:\Users\browser-user\.saygo\browser-bridge\com.saygo.browser.json'}
        paths = {info['home']:str(self.root), info['local']:str(self.root/'AppData/Local'),
                 info['manifest']:str(self.legacy/'com.saygo.browser.json')}
        with patch('saygo.devices.mobile_host.is_wsl', return_value=True), \
             patch.object(location, '_windows_info', return_value=info), \
             patch('saygo.devices.mobile_host.wsl_path', side_effect=lambda path:paths[path]):
            default, legacy, registration = ORIGINAL_LAYOUT('chrome')
        self.assertEqual(default, self.standard)
        self.assertEqual(legacy, self.legacy)
        self.assertEqual(registration, self.legacy/'com.saygo.browser.json')

    def test_upgrade_setup_preserves_the_running_directory_and_host_epoch(self):
        self.register(self.standard)
        host, _ = self.host(self.legacy)
        before = json.loads((self.legacy/'status.json').read_text())['epoch']
        def install(directory, extension_id, browser):
            self.register(directory, extension_id)
            return {'installed':True, 'directory':str(directory)}
        with patch('saygo.integrations.browser_bridge.install', side_effect=install) as installer:
            result = browser_setup.setup('a' * 32, directory=self.standard)
        self.assertEqual(result['directory'], str(self.legacy))
        self.assertEqual(installer.call_args.args[0], self.legacy)
        self.assertEqual(location.registration_directory(), self.legacy)
        self.assertEqual(json.loads((self.legacy/'status.json').read_text())['epoch'], before)
        self.assertIsNone(host.poll())

    def test_live_desktop_wins_over_stale_wsl_registration_and_default(self):
        self.register(self.standard)
        host, seen = self.host(self.legacy)
        atomic_json(self.standard / 'status.json', {'protocol':1, 'connected':False})
        for hint in (None, self.standard, self.legacy):
            with self.subTest(hint=hint):
                self.assertEqual(location.resolve_directory(hint, extension_id='a' * 32), self.legacy)
        self.assertIsNone(host.poll())
        self.assertEqual(seen, ['pages'] * 3)

    def test_live_wsl_wins_over_stale_desktop_registration(self):
        self.register(self.legacy)
        host, _ = self.host(self.standard)
        self.assertEqual(location.resolve_directory(self.legacy), self.standard)
        self.assertIsNone(host.poll())

    def test_existing_registered_directory_survives_disconnection(self):
        self.register(self.legacy)
        self.assertEqual(location.resolve_directory(self.standard), self.legacy)

    def test_two_live_hosts_are_reported_without_choosing_another_profile(self):
        first, _ = self.host(self.standard)
        second, _ = self.host(self.legacy)
        with self.assertRaisesRegex(RuntimeError, 'Multiple browser bridges'):
            location.resolve_directory()
        self.assertIsNone(first.poll()); self.assertIsNone(second.poll())

    def test_unresponsive_connected_flag_cannot_trigger_new_installation(self):
        self.legacy.mkdir(parents=True, exist_ok=True)
        atomic_json(self.legacy / 'status.json', {'protocol':1,'connected':True,'epoch':'stale'})
        with patch.object(location.Client, 'call', side_effect=RuntimeError('timed out')):
            with self.assertRaisesRegex(RuntimeError, 'timed out'):
                location.resolve_directory()

    def test_protocol_and_extension_identity_conflicts_fail_before_input(self):
        self.register(self.standard, 'b' * 32)
        atomic_json(self.standard / 'status.json', {'protocol':1,'connected':True})
        with self.assertRaisesRegex(RuntimeError, 'another extension identity'):
            location.resolve_directory(extension_id='a' * 32)
        atomic_json(self.standard / 'status.json', {'protocol':1,'connected':False})
        self.legacy.mkdir(parents=True, exist_ok=True)
        atomic_json(self.legacy / 'status.json', {'protocol':99,'connected':True})
        with self.assertRaisesRegex(RuntimeError, 'protocol mismatch'):
            location.resolve_directory()

    def test_manual_identity_migration_retains_the_disconnected_registered_directory(self):
        self.register(self.legacy, 'b' * 32)
        atomic_json(self.legacy / 'status.json', {'protocol':1,'connected':False})
        self.assertEqual(location.resolve_directory(extension_id='a' * 32), self.legacy)

    def test_custom_directory_remains_explicit_and_does_not_discover_other_hosts(self):
        custom = self.root / 'custom bridge'
        with patch.object(location, '_layout', side_effect=AssertionError('must stay explicit')):
            self.assertEqual(location.resolve_directory(custom), custom)

    def test_new_cli_and_desktop_connections_use_shared_discovery(self):
        from saygo.platforms import device_session as ds
        from saygo.devices import control
        from saygo.desktop import connections
        self.register(self.standard)
        self.host(self.legacy)
        state_root = self.root / 'client'
        state_root.mkdir()
        atomic_json(state_root / 'browser-bridge.json', {'directory':str(self.standard)})
        with patch.object(ds, 'STATE_DIR', state_root / 'device-sessions'):
            result = control.connect(connections.arguments('browser', 'fixture', page_id=None))
            self.assertTrue(result['connected'])
            self.assertEqual(ds.load_state('fixture')['bridge_directory'], str(self.legacy))
            desktop = connections.browser_status()
            self.assertTrue(desktop['connected'])
            self.assertEqual(desktop['directory'], str(self.legacy))

    def test_saved_page_binding_is_not_implicitly_migrated(self):
        from saygo.platforms import device_session as ds
        from saygo.devices import control
        from saygo.desktop import connections
        self.host(self.legacy)
        self.standard.mkdir(parents=True, exist_ok=True)
        atomic_json(self.standard / 'status.json', {'protocol':1,'connected':False})
        with patch.object(ds, 'STATE_DIR', self.root / 'client/device-sessions'):
            state = {'kind':'browser','browser_backend':'extension','bridge_directory':str(self.standard), 'page_id':'old:42'}
            ds.save_state('fixture', state)
            with self.assertRaisesRegex(RuntimeError, 'No browser connection at'):
                control.connect(connections.arguments('browser', 'fixture'))
            self.assertEqual(ds.load_state('fixture'), state)


ORIGINAL_LAYOUT = location._layout

if __name__ == '__main__':
    unittest.main()
