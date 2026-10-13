"""Cross-process handoff contracts using real platform hooks and a fake wire."""
import io
from argparse import Namespace
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from PIL import Image
from saygo.devices import control
from saygo.platforms import device_session as ds
from saygo.runtime.locking import resource_guard, session_keys
from saygo.runtime.store import BusyError

MANUAL = 'com.example.keyboard/.Keyboard'
OTHER = 'com.example.other/.Keyboard'
UNICODE = 'io.appium.settings/.UnicodeIME'


class Wire:
    session_id = 'example-session'
    def __init__(self):
        self.current = UNICODE
        self.commands = {}
        self.command_executor = self
        self.calls = []
        self.fail_switch = self.fail_image = False
    def add_command(self, name, method, path): self.commands[name] = path
    def execute(self, name, params):
        action = self.commands[name].rsplit('/', 1)[-1]
        self.calls.append(action)
        if action == 'active_engine': return {'value': self.current}
        if action == 'available_engines': return {'value': [MANUAL, OTHER, UNICODE]}
        if self.fail_switch: raise RuntimeError('switch denied')
        self.current = params['engine']
        return {'value': None}
    def get_window_size(self): return {'width': 200, 'height': 100}
    def get_screenshot_as_png(self):
        if self.fail_image: raise RuntimeError('image unavailable')
        out = io.BytesIO()
        Image.new('RGB', (200, 100), 'white').save(out, format='PNG')
        return out.getvalue()


class MobileHandoffTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        p = patch.object(ds, 'STATE_DIR', Path(tmp.name) / 'sessions')
        p.start(); self.addCleanup(p.stop)
        self.wire = Wire()
        p = patch.object(ds, '_attach_driver', return_value=self.wire)
        p.start(); self.addCleanup(p.stop)
        self.state = dict(os='android', device_id='example-device', session_id=self.wire.session_id,
                          server_url='http://127.0.0.1:4723', screen_width=200, screen_height=100,
                          android_input_method={'manual_ime': MANUAL})
        ds.save_state('phone', self.state)
        self.args = Namespace(session='phone', reason='manual', instructions='Type in the test page')
        self.resume = Namespace(session='phone', note='Manual typing confirmed')
        self.connect = Namespace(session='phone', platform='android', device='example-device',
                                 server_url=None, team_id=None)

    def test_handoff_restores_and_repeated_handoff_keeps_choice_and_lock(self):
        control.handoff(self.args)
        self.assertEqual(self.wire.current, MANUAL)
        control.handoff(self.args)
        self.assertEqual(self.wire.calls.count('activate'), 1)
        self.assertEqual(ds.load_state('phone')['android_input_method']['manual_ime'], MANUAL)
        with self.assertRaises(BusyError), resource_guard(session_keys('phone')): pass

    def test_failed_switch_keeps_pause_and_ownership_until_recovery(self):
        self.wire.fail_switch = True
        with self.assertRaisesRegex(RuntimeError, 'switch denied'): control.handoff(self.args)
        self.assertIn('error', ds.load_state('phone')['handoff'])
        with self.assertRaises(BusyError), resource_guard(session_keys('phone')): pass
        self.wire.fail_switch = False
        control.handoff(self.args)
        self.assertEqual(self.wire.current, MANUAL)

    def test_missing_record_does_not_guess_and_human_selection_is_saved(self):
        self.state.pop('android_input_method')
        ds.save_state('phone', self.state)
        with self.assertRaisesRegex(RuntimeError, 'unknown'): control.handoff(self.args)
        self.assertEqual(self.wire.current, UNICODE)
        self.wire.current = OTHER  # A human chooses a keyboard in system settings.
        control.handoff(self.args)
        self.assertEqual(ds.load_state('phone')['android_input_method']['manual_ime'], OTHER)

    def test_resume_requires_fresh_image_and_remembers_human_choice(self):
        control.handoff(self.args)
        self.wire.current = OTHER
        self.wire.fail_image = True
        with self.assertRaisesRegex(RuntimeError, 'image unavailable'): control.resume(self.resume)
        self.assertIn('handoff', ds.load_state('phone'))
        self.wire.fail_image = False
        result = control.resume(self.resume)
        self.assertEqual(result['status'], 'needs_observation')
        self.assertTrue(Path(result['observation']['path']).is_file())
        self.assertNotIn('handoff', ds.load_state('phone'))
        self.assertEqual(ds.load_state('phone')['android_input_method']['manual_ime'], OTHER)
        with resource_guard(session_keys('phone')): pass

    def test_attach_preserves_pause_on_disk_and_persists_choice(self):
        self.state['handoff'] = {'status': 'waiting_for_human'}
        ds.save_state('phone', self.state)
        candidate = {k: v for k, v in self.state.items() if k != 'handoff'}
        plat = ds.attach('phone', state=candidate)
        plat.prepare_handoff()
        self.assertIn('handoff', ds.load_state('phone'))
        self.wire.current = OTHER
        plat.prepare_resume()
        self.assertEqual(ds.load_state('phone')['android_input_method']['manual_ime'], OTHER)

    def test_ios_handoff_and_resume_do_not_send_android_ime_commands(self):
        self.state['os'] = 'ios'
        ds.save_state('phone', self.state)
        control.handoff(self.args)
        result = control.resume(self.resume)
        self.assertEqual(result['status'], 'needs_observation')
        self.assertEqual(self.wire.calls, [])

    def test_connect_reuses_live_handoff_without_resuming_or_quitting(self):
        control.handoff(self.args)
        with patch('appium.webdriver.Remote') as remote:
            result = control.connect(self.connect)
        self.assertTrue(result['connected'], result)
        self.assertEqual(result['status'], 'waiting_for_human')
        self.assertEqual(ds.load_state('phone')['session_id'], self.wire.session_id)
        remote.assert_not_called()
        with self.assertRaises(BusyError), resource_guard(session_keys('phone')): pass

    def test_expired_handoff_explicit_connect_rebuilds_preserving_choice_and_lock(self):
        from selenium.common.exceptions import InvalidSessionIdException
        control.handoff(self.args)
        state = ds.load_state('phone')
        state['appium_connection'] = {'adb_port': 15037}
        ds.save_state('phone', state)
        replacement = Wire()
        replacement.session_id = 'replacement-session'
        with patch.object(ds, '_attach_driver', side_effect=InvalidSessionIdException('expired')), \
                patch('saygo.platforms.appium_server.AppiumServerManager') as manager, \
                patch('appium.webdriver.Remote', return_value=replacement) as remote:
            manager.return_value.ensure_running.return_value = self.state['server_url']
            result = control.connect(self.connect)
        self.assertTrue(result['connected'], result)
        self.assertEqual(result['status'], 'waiting_for_human')
        state = ds.load_state('phone')
        self.assertEqual(state['session_id'], replacement.session_id)
        self.assertEqual(state['android_input_method'], {'manual_ime': MANUAL})
        self.assertIn('handoff', state)
        self.assertEqual(replacement.current, MANUAL)
        caps = remote.call_args.kwargs['options'].to_capabilities()
        self.assertEqual(caps['appium:adbPort'], 15037)
        self.assertTrue(caps['appium:noReset'])
        self.assertFalse(caps['appium:autoLaunch'])
        self.assertNotIn('appium:appPackage', caps)
        with self.assertRaises(BusyError), resource_guard(session_keys('phone')): pass

    def test_connect_cannot_replace_possibly_live_session_after_transport_failure(self):
        control.handoff(self.args)
        with patch.object(ds, '_attach_driver', side_effect=TimeoutError('server unreachable')), \
                patch('appium.webdriver.Remote') as remote:
            with self.assertRaisesRegex(RuntimeError, 'server unreachable'):
                control.connect(self.connect)
        self.assertEqual(ds.load_state('phone')['session_id'], self.wire.session_id)
        remote.assert_not_called()
        with self.assertRaises(BusyError), resource_guard(session_keys('phone')): pass

    def test_handoff_reconnect_rejects_changed_device_or_server(self):
        control.handoff(self.args)
        for field, value in [('device', 'other-device'), ('server_url', 'http://example.invalid:4723'), ('platform', 'ios')]:
            with self.subTest(field=field), patch.object(ds, '_attach_driver') as attach:
                args = Namespace(**vars(self.connect))
                setattr(args, field, value)
                with self.assertRaisesRegex(ValueError, 'different|another'):
                    control.connect(args)
                attach.assert_not_called()

    def test_task_owned_handoff_reconnect_keeps_task_owner(self):
        from saygo.runtime.locking import reserve
        task_id = 'example-task'
        reserve(task_id, session_keys('phone'))
        args = Namespace(**vars(self.args), task=task_id)
        with resource_guard(session_keys('phone'), owner=task_id):
            control._handoff(args)
        result = control.connect(self.connect)
        self.assertTrue(result['connected'], result)
        self.assertEqual(ds.load_state('phone')['handoff']['task'], task_id)
        with resource_guard(session_keys('phone'), owner=task_id): pass
        with self.assertRaises(BusyError), resource_guard(session_keys('phone')): pass

    def test_connect_cannot_bypass_task_ownership_without_handoff(self):
        from saygo.runtime.locking import reserve
        reserve('example-task', session_keys('phone'))
        with patch('appium.webdriver.Remote') as remote:
            with self.assertRaises(BusyError):
                control.connect(self.connect)
        remote.assert_not_called()

    def test_legacy_handoff_reconnect_restores_missing_persistent_lock_on_failure(self):
        self.state['handoff'] = {'status': 'waiting_for_human', 'instructions': 'Manual input'}
        ds.save_state('phone', self.state)
        self.wire.fail_switch = True
        with self.assertRaisesRegex(RuntimeError, 'switch denied'):
            control.connect(self.connect)
        with self.assertRaises(BusyError), resource_guard(session_keys('phone')): pass

    def test_handoff_reconnect_cannot_steal_conflicting_task_ownership(self):
        from saygo.runtime.locking import reserve
        self.state['handoff'] = {'status': 'waiting_for_human', 'instructions': 'Manual input'}
        ds.save_state('phone', self.state)
        reserve('other-task', session_keys('phone'))
        with patch.object(ds, '_attach_driver') as attach:
            with self.assertRaises(BusyError):
                control.connect(self.connect)
        attach.assert_not_called()

    def test_ios_expired_handoff_preserves_signing_and_never_uses_android_ime(self):
        from selenium.common.exceptions import InvalidSessionIdException
        self.state['os'] = 'ios'
        self.state['appium_connection'] = {'team_id': 'TEAM_PLACEHOLDER', 'wda_bundle_id': 'com.example.wda'}
        ds.save_state('phone', self.state)
        self.connect.platform = 'ios'
        control.handoff(self.args)
        replacement = Wire()
        replacement.session_id = 'replacement-session'
        with patch.object(ds, '_attach_driver', side_effect=InvalidSessionIdException('expired')), \
                patch('saygo.platforms.appium_server.AppiumServerManager') as manager, \
                patch('appium.webdriver.Remote', return_value=replacement) as remote:
            manager.return_value.ensure_running.return_value = self.state['server_url']
            result = control.connect(self.connect)
        self.assertTrue(result['connected'], result)
        self.assertEqual(result['status'], 'waiting_for_human')
        caps = remote.call_args.kwargs['options'].to_capabilities()
        self.assertEqual(caps['appium:xcodeOrgId'], 'TEAM_PLACEHOLDER')
        self.assertEqual(caps['appium:updatedWDABundleId'], 'com.example.wda')
        self.assertNotIn('appium:bundleId', caps)
        self.assertFalse(caps['appium:shouldTerminateApp'])
        self.assertEqual(replacement.calls, [])

    def test_unknown_choice_after_expired_session_stays_paused_with_new_binding(self):
        from selenium.common.exceptions import InvalidSessionIdException
        self.state.pop('android_input_method')
        ds.save_state('phone', self.state)
        with self.assertRaises(RuntimeError): control.handoff(self.args)
        replacement = Wire()
        replacement.session_id = 'replacement-session'
        with patch.object(ds, '_attach_driver', side_effect=InvalidSessionIdException('expired')), \
                patch('saygo.platforms.appium_server.AppiumServerManager') as manager, \
                patch('appium.webdriver.Remote', return_value=replacement):
            manager.return_value.ensure_running.return_value = self.state['server_url']
            with self.assertRaisesRegex(RuntimeError, 'unknown'):
                control.connect(self.connect)
        self.assertEqual(ds.load_state('phone')['session_id'], replacement.session_id)
        self.assertIn('handoff', ds.load_state('phone'))
        self.assertEqual(replacement.current, UNICODE)
        with self.assertRaises(BusyError), resource_guard(session_keys('phone')): pass

    def test_android_reconnect_configuration_is_saved_on_initial_connection(self):
        ds.clear_state('phone')
        self.wire.current = MANUAL
        with patch('saygo.platforms.appium_server.AppiumServerManager') as manager, \
                patch('appium.webdriver.Remote', return_value=self.wire):
            manager.return_value.ensure_running.return_value = self.state['server_url']
            ds.start('phone', 'android', appium_config={'device': 'example-device', 'adb_port': 15037})
        self.assertEqual(ds.load_state('phone')['appium_connection'], {'adb_port': 15037})

    def test_failed_ime_read_after_creating_session_keeps_recoverable_paused_binding(self):
        from selenium.common.exceptions import InvalidSessionIdException
        control.handoff(self.args)
        replacement = Wire()
        replacement.session_id = 'replacement-session'
        replacement.execute = Mock(side_effect=TimeoutError('IME read unavailable'))
        with patch.object(ds, '_attach_driver', side_effect=InvalidSessionIdException('expired')), \
                patch('saygo.platforms.appium_server.AppiumServerManager') as manager, \
                patch('appium.webdriver.Remote', return_value=replacement):
            manager.return_value.ensure_running.return_value = self.state['server_url']
            with self.assertRaisesRegex(RuntimeError, 'IME read unavailable'):
                control.connect(self.connect)
        self.assertEqual(ds.load_state('phone')['session_id'], replacement.session_id)
        self.assertIn('handoff', ds.load_state('phone'))
        with self.assertRaises(BusyError), resource_guard(session_keys('phone')): pass

    def test_initial_connection_ime_read_failure_does_not_lose_created_session(self):
        ds.clear_state('phone')
        self.wire.execute = Mock(side_effect=TimeoutError('IME read unavailable'))
        with patch('saygo.platforms.appium_server.AppiumServerManager') as manager, \
                patch('appium.webdriver.Remote', return_value=self.wire):
            manager.return_value.ensure_running.return_value = self.state['server_url']
            with self.assertRaisesRegex(RuntimeError, 'IME read unavailable'):
                ds.start('phone', 'android', appium_config={'device': 'example-device', 'adb_port': 15037})
        state = ds.load_state('phone')
        self.assertIsNotNone(state)
        self.assertEqual(state['session_id'], self.wire.session_id)
        self.assertEqual(state['appium_connection'], {'adb_port': 15037})


if __name__ == '__main__': unittest.main()
