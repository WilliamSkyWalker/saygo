"""普通设备命令的观察绑定、持久去重与人工核对。"""
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image
from saygo.devices import service
from saygo.platforms import device_session as ds
from saygo.platforms.base import Platform


class Device(Platform):
    platform_name = 'browser'
    screen_size = (80, 60)
    def __init__(self):
        self.calls = []
        self.fail = False
        out = io.BytesIO()
        Image.new('RGB', self.screen_size, 'white').save(out, format='PNG')
        self.frame = out.getvalue()
    def setup(self, config): pass
    def teardown(self): pass
    def screenshot_png(self): return self.frame
    def get_system_prompt_segment(self): return ''
    def tap(self, x, y):
        self.calls.append(('tap', x, y))
        if self.fail: raise TimeoutError('response lost')
    def input_text(self, text): self.calls.append(('input', text))
    def press_key(self, key): self.calls.append(('key', key))
    def swipe(self, *points): self.calls.append(('swipe', *points))
    def scroll_up(self): self.calls.append(('scroll_up',))
    def scroll_down(self): self.calls.append(('scroll_down',))
    def open_target(self, target): self.calls.append(('open', target))


class DeviceSafetyTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        patcher = patch.object(ds, 'STATE_DIR', self.root / 'sessions')
        patcher.start(); self.addCleanup(patcher.stop)
        self.device = Device()
        state = {'kind': 'browser', 'browser_backend': 'extension', 'bridge_directory': str(self.root / 'bridge')}
        ds.save_state('web', state)
        ds.save_state('alias', state)
        patcher = patch.object(ds, 'attach_browser', return_value=self.device)
        self.attach = patcher.start(); self.addCleanup(patcher.stop)

    def observe(self):
        return service.execute('screenshot', 'web')['observation_id']

    def test_cli_and_mcp_defaults_share_request_identity(self):
        options = dict(text='example', observation_id=self.observe(), request_id='cross-entry')
        original = service.execute('input', 'web', **options)
        repeated = service.execute('input', 'web', out=None, **options)
        self.assertEqual(repeated, original)
        self.assertEqual(self.device.calls, [('input', 'example')])

    def test_post_input_journal_failure_releases_controller_but_blocks_replay(self):
        oid = self.observe()
        original_record = service._record
        def record(path, kind, data):
            if kind in {'after', 'observation_failed'}:
                raise OSError('example disk full')
            return original_record(path, kind, data)
        with patch.object(service, '_record', side_effect=record), \
             patch.object(ds, 'release_controller') as release:
            result = service.execute('input', 'web', text='example', observation_id=oid, request_id='journal-full')
        self.assertEqual(result['outcome'], 'uncertain')
        release.assert_called_once_with(self.device)
        repeat = service.execute('input', 'web', text='example', observation_id=oid, request_id='journal-full')
        self.assertEqual(result, repeat)
        self.assertEqual(self.device.calls, [('input', 'example')])

    def test_legacy_input_commands_require_original_observation(self):
        for command, options in [('input', {'text': 'example'}), ('key', {'key': 'enter'}),
                                 ('tap', {'x': 1, 'y': 2}), ('act', {'action': {'type': 'tap', 'x': 1, 'y': 2}})]:
            with self.subTest(command=command):
                result = service.execute(command, 'web', **options)
                self.assertFalse(result['ok'])
                self.assertEqual(result['outcome'], 'not_dispatched')
                self.assertIn('observation', result['error'].lower())
        self.assertEqual(self.device.calls, [])

    def test_request_id_reuse_returns_original_result_without_input(self):
        oid = self.observe()
        options = dict(action={'type': 'tap', 'x': 1, 'y': 2}, observation_id=oid, request_id='request-one')
        first = service.execute('act', 'web', **options)
        self.assertTrue(first['ok'], first)
        second = service.execute('act', 'web', **options)
        self.assertEqual(first['operation_id'], second['operation_id'])
        self.assertEqual(self.device.calls, [('tap', 1, 2)])
        conflict = service.execute('act', 'web', **{**options, 'action': {'type': 'tap', 'x': 3, 'y': 4}})
        self.assertFalse(conflict['ok'])
        self.assertEqual(self.device.calls, [('tap', 1, 2)])

    def test_uncertain_request_blocks_alias_until_explicit_review(self):
        oid = self.observe()
        self.device.fail = True
        result = service.execute('act', 'web', action={'type': 'tap', 'x': 1, 'y': 2},
                                 observation_id=oid, request_id='lost-response')
        self.assertEqual(result['outcome'], 'uncertain')
        blocked = service.execute('input', 'alias', text='must not type', observation_id=oid)
        self.assertFalse(blocked['ok'])
        self.assertEqual(self.device.calls, [('tap', 1, 2)])
        self.assertTrue(service.execute('screenshot', 'web')['ok'])
        resolved = service.execute('resolve', 'web', request_id='lost-response',
                                   resolution='applied', note='Checked the isolated test page')
        self.assertTrue(resolved['ok'], resolved)
        self.device.fail = False
        stale = service.execute('input', 'web', text='must observe again', observation_id=oid)
        self.assertFalse(stale['ok'])
        fresh = service.execute('input', 'web', text='example', observation_id=self.observe())
        self.assertTrue(fresh['ok'], fresh)
        self.assertEqual(self.device.calls, [('tap', 1, 2), ('input', 'example')])

    def test_stale_observation_rejects_legacy_key_before_dispatch(self):
        oid = self.observe()
        out = io.BytesIO()
        Image.new('RGB', self.device.screen_size, 'black').save(out, format='PNG')
        self.device.frame = out.getvalue()
        result = service.execute('key', 'web', key='enter', observation_id=oid)
        self.assertFalse(result['ok'])
        self.assertEqual(self.device.calls, [])

    def test_ime_preparation_failure_is_not_dispatched_for_input_and_act(self):
        from saygo.platforms.android_ime import InputMethodError
        for command, options in [('input', {'text': 'example'}),
                                 ('act', {'action': {'type': 'input', 'text': 'example'}})]:
            with self.subTest(command=command):
                observation_id = self.observe()
                request_id = 'ime-unavailable-' + command
                with patch.object(self.device, 'input_text', side_effect=InputMethodError('Choose a manual keyboard')):
                    result = service.execute(command, 'web', observation_id=observation_id,
                                             request_id=request_id, **options)
                self.assertFalse(result['ok'])
                self.assertEqual(result['outcome'], 'not_dispatched')
                self.assertFalse(result['requires_observation'])
                # Known no-input failures release operation ownership. A new
                # observed request can run without resolving an uncertain input.
                next_result = service.execute('input', 'web', text='after recovery',
                                              observation_id=self.observe())
                self.assertTrue(next_result['ok'], next_result)
        self.assertEqual(self.device.calls, [('input', 'after recovery')] * 2)

    def test_ime_preparation_failure_in_observed_service_releases_ownership(self):
        from saygo.platforms.android_ime import InputMethodError
        from saygo.runtime.locking import session_keys
        observation = service.execute('screenshot', 'web')
        with patch.object(self.device, 'input_text', side_effect=InputMethodError('Choose a manual keyboard')):
            result = service.execute_observed(self.device, 'web', {'type': 'input', 'text': 'example'},
                                              observation, session_keys('web'))
        self.assertEqual(result['outcome'], 'not_dispatched')
        self.assertFalse(result['requires_observation'])
        self.assertEqual(self.device.calls, [])
        next_result = service.execute('input', 'web', text='after recovery', observation_id=self.observe())
        self.assertTrue(next_result['ok'], next_result)

    def test_ime_failure_after_type_send_focus_still_reports_prior_dispatch(self):
        from saygo.platforms.android_ime import InputMethodError
        observation_id = self.observe()
        with patch.object(self.device, 'input_text', side_effect=InputMethodError('Choose a manual keyboard')), \
                patch.object(service.time, 'sleep'):
            result = service.execute('type-send', 'web', text='example', input_x=1, input_y=2,
                                     prepare_only=True, observation_id=observation_id)
        self.assertEqual(result['outcome'], 'uncertain')
        self.assertTrue(result['requires_observation'])
        self.assertFalse(result['submission_attempted'])
        self.assertEqual(self.device.calls, [('tap', 1, 2)])


if __name__ == '__main__':
    unittest.main()
