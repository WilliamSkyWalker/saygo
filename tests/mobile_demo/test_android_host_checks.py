import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from saygo.devices import android_host_checks as checks


class AndroidHostChecksTests(unittest.TestCase):
    def test_server_and_diagnostics_use_the_same_sdk_selection(self):
        from saygo.devices import mobile
        from saygo.platforms import appium_server
        with tempfile.TemporaryDirectory() as tmp:
            sdk = Path(tmp) / 'private-sdk'
            other = Path(tmp) / 'studio-sdk'
            sdk.mkdir(); other.mkdir()
            with patch.dict(appium_server.os.environ, {}, clear=True), \
                    patch.object(appium_server.os.path, 'expanduser', return_value=str(other)), \
                    patch.object(mobile, 'sdk_root', return_value=sdk):
                self.assertEqual(appium_server._default_android_home(), str(sdk))

    def fixture(self, root):
        sdk = root / 'sdk'
        for name in ('platform-tools/adb', 'platforms/android-35/android.jar',
                     'build-tools/35.0.0/aapt', 'cmdline-tools/latest/bin/sdkmanager'):
            path = sdk / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch()
        java, node, appium = [root / name for name in ('java', 'node', 'appium.js')]
        for path in (java, node, appium): path.touch()
        return dict(sdk_root=str(sdk), runtime=str(root / 'runtime'),
                    java=str(java), node=str(node), appium=str(appium),
                    appium_home=str(root / 'appium-home'))

    def output(self, argv, **kwargs):
        text = ('openjdk version "21.0.1"' if '-version' in argv else
                'v22.12.0' if '--version' in argv else
                json.dumps({'uiautomator2': {'version': '1'}}))
        return subprocess.CompletedProcess(argv, 0, text, '')

    def test_complete_host_checks_without_starting_server_or_adb(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = self.fixture(Path(tmp))
            with patch.object(checks, '_run', side_effect=self.output) as run:
                result = checks.inspect_host(config)
        self.assertTrue(all(item['status'] == 'ready' for item in result), result)
        self.assertTrue(any(item['id'] == 'uiautomator2' for item in result))
        self.assertTrue(all('devices' not in call.args[0] for call in run.call_args_list))
        self.assertTrue(all('install' not in call.args[0] for call in run.call_args_list))

    def test_platform_tools_alone_is_not_complete_sdk(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = self.fixture(Path(tmp))
            (Path(config['sdk_root']) / 'platforms/android-35/android.jar').unlink()
            with patch.object(checks, '_run', side_effect=self.output):
                result = {item['id']: item for item in checks.inspect_host(config)}
        self.assertEqual(result['adb']['status'], 'ready')
        self.assertEqual(result['android_platform']['status'], 'missing')

    def test_driver_query_failure_is_unknown_not_missing_or_ready(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = self.fixture(Path(tmp))
            def output(argv, **kwargs):
                if 'driver' in argv: raise subprocess.TimeoutExpired(argv, 10)
                return self.output(argv, **kwargs)
            with patch.object(checks, '_run', side_effect=output):
                result = {item['id']: item for item in checks.inspect_host(config)}
        self.assertEqual(result['uiautomator2']['status'], 'unknown')

    def test_python_uiautomator_is_not_an_appium_driver(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = self.fixture(Path(tmp))
            def output(argv, **kwargs):
                if 'driver' in argv: return subprocess.CompletedProcess(argv, 0, '{}', '')
                return self.output(argv, **kwargs)
            with patch.object(checks, '_run', side_effect=output):
                result = {item['id']: item for item in checks.inspect_host(config)}
        self.assertEqual(result['uiautomator2']['status'], 'missing')

    def test_external_appium_uses_its_adjacent_node_before_private_or_path_node(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = self.fixture(Path(tmp))
            appium = Path(tmp) / 'external/bin/appium'
            appium.parent.mkdir(parents=True)
            appium.touch()
            adjacent_node = appium.with_name('node')
            adjacent_node.touch()
            private_node = Path(config['runtime']) / 'node/bin/node'
            private_node.parent.mkdir(parents=True)
            private_node.touch()
            config.update(appium=str(appium), node=None, appium_home=None, managed_appium=False)
            with patch.object(checks, '_run', side_effect=self.output) as run, \
                    patch.object(checks.shutil, 'which', return_value='/example/other/node'):
                checks.inspect_host(config)
            node_call = next(call for call in run.call_args_list if '--version' in call.args[0])
            self.assertEqual(node_call.args[0][0], str(adjacent_node))
            driver_call = next(call for call in run.call_args_list if 'driver' in call.args[0])
            self.assertTrue(driver_call.kwargs['env']['PATH'].startswith(str(appium.parent)))

    def test_private_windows_host_does_not_accept_global_node_or_appium(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = self.fixture(Path(tmp))
            config.update(appium=None, node=None, appium_home=None, managed_only=True)
            with patch.object(checks, '_run', side_effect=self.output) as run, \
                    patch.object(checks.shutil, 'which', side_effect=lambda name, **kwargs: '/example/global/' + name):
                result = {item['id']: item for item in checks.inspect_host(config)}
            self.assertEqual(result['node']['status'], 'missing')
            self.assertEqual(result['appium']['status'], 'missing')
            self.assertFalse(any('driver' in call.args[0] for call in run.call_args_list))

    def test_private_host_rejects_stale_node_marker_without_path_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = self.fixture(Path(tmp))
            runtime = Path(config['runtime'])
            appium = runtime / 'node_modules/appium/build/lib/main.js'
            appium.parent.mkdir(parents=True)
            appium.touch()
            (runtime / 'node_path.txt').write_text(str(Path(tmp) / 'removed-node'))
            config.update(appium=None, node=None, appium_home=None, managed_only=True)
            with patch.object(checks, '_run', side_effect=self.output) as run, \
                    patch.object(checks.shutil, 'which', return_value='/example/global/node'):
                result = {item['id']: item for item in checks.inspect_host(config)}
            self.assertEqual(result['node']['status'], 'missing')
            self.assertEqual(result['appium']['status'], 'ready')
            self.assertEqual(result['uiautomator2']['status'], 'unknown')
            self.assertFalse(any('driver' in call.args[0] for call in run.call_args_list))

    def test_private_host_reuses_existing_marker_and_prefers_private_node(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = self.fixture(Path(tmp))
            runtime = Path(config['runtime'])
            appium = runtime / 'node_modules/appium/build/lib/main.js'
            appium.parent.mkdir(parents=True)
            appium.touch()
            marker_node = config['node']
            (runtime / 'node_path.txt').write_text(marker_node)
            config.update(appium=None, node=None, appium_home=None, managed_only=True)
            private_node = runtime / 'node/bin/node'
            for private in (False, True):
                if private:
                    private_node.parent.mkdir(parents=True)
                    private_node.touch()
                with self.subTest(private=private), patch.object(checks, '_run', side_effect=self.output) as run:
                    result = {item['id']: item for item in checks.inspect_host(config)}
                    expected = str(private_node) if private else marker_node
                    driver_call = next(call for call in run.call_args_list if 'driver' in call.args[0])
                    self.assertEqual(driver_call.args[0][:2], [expected, str(appium)])
                    self.assertEqual(driver_call.kwargs['env']['APPIUM_HOME'], str(runtime / 'appium_home'))
                    self.assertEqual(result['uiautomator2']['status'], 'ready')

    def test_windows_probe_requests_private_runtime_without_copying_worker(self):
        from saygo.devices import android_setup, mobile_host
        with tempfile.TemporaryDirectory() as tmp:
            python = Path(tmp) / 'python/python.exe'
            python.parent.mkdir()
            python.touch()
            info = {'home': 'C:\\Example Host', 'sdk_root': 'C:\\Example SDK'}
            with patch.object(mobile_host, 'windows_info', return_value=info), \
                    patch.object(mobile_host, 'wsl_path', return_value=tmp), \
                    patch.object(mobile_host, 'prepare_windows', side_effect=AssertionError('No worker writes')), \
                    patch.object(android_setup.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '[]', '')) as run:
                android_setup.windows_checks()
            config = json.loads(run.call_args.kwargs['input'])
            self.assertTrue(config.get('managed_only'))
            self.assertEqual(config['runtime'], 'C:\\Example Host\\runtime')


if __name__ == '__main__':
    unittest.main()
