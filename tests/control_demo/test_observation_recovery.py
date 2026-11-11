"""Rejected input returns the comparison frame without dispatching or recapturing."""
import base64
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image

from saygo.devices import observations, service
from saygo.platforms import device_session as ds
from saygo.platforms.base import Platform
from saygo.runtime.locking import session_keys


def png(color):
    stream = io.BytesIO()
    Image.new('RGB', (160, 120), color).save(stream, format='PNG')
    return stream.getvalue()


class Device(Platform):
    platform_name = 'browser'
    screen_size = (160, 120)

    def __init__(self):
        self.frame = png('white')
        self.calls = []

    def setup(self, config): pass
    def teardown(self): pass
    def screenshot_png(self): return self.frame
    def get_system_prompt_segment(self): return ''
    def tap(self, x, y): self.calls.append(('tap', x, y))
    def input_text(self, text): self.calls.append(('input', text))
    def press_key(self, key): self.calls.append(('key', key))
    def swipe(self, *points): self.calls.append(('swipe', *points))
    def scroll_up(self): self.calls.append(('scroll_up',))
    def scroll_down(self): self.calls.append(('scroll_down',))
    def open_target(self, target): self.calls.append(('open', target))


class ObservationRecoveryTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        state_patch = patch.object(ds, 'STATE_DIR', self.root / 'sessions')
        state_patch.start()
        self.addCleanup(state_patch.stop)
        self.device = Device()
        ds.save_state('web', {'kind': 'browser', 'browser_backend': 'extension',
                              'bridge_directory': str(self.root / 'bridge')})
        attach_patch = patch.object(ds, 'attach_browser', return_value=self.device)
        attach_patch.start()
        self.addCleanup(attach_patch.stop)

    def observe(self):
        return service.execute('screenshot', 'web')

    def assert_rejected_with_frame(self, result, frame):
        self.assertFalse(result['ok'], result)
        self.assertEqual(result['outcome'], 'not_dispatched')
        self.assertTrue(result['requires_observation'])
        self.assertEqual(self.device.calls, [])
        observation = result['observation']
        self.assertEqual(Path(observation['source_path']).read_bytes(), frame)
        self.assertEqual(observations.load(observation['id'], 'web'), observation)
        self.assertIn('visual_change', result)
        events = [json.loads(line) for line in Path(result['record']).read_text().splitlines()]
        recorded = next(event['data'] for event in events if event['kind'] == 'result')
        self.assertEqual(recorded['observation'], observation)
        self.assertEqual(recorded['visual_change'], result['visual_change'])
        self.assertNotIn('dispatching', [event['kind'] for event in events])

    def test_rejection_preserves_comparison_frame_and_does_not_replay(self):
        original = self.observe()
        changed = png('black')
        self.device.frame = changed
        options = dict(action={'type': 'tap', 'x': 20, 'y': 30},
                       observation_id=original['id'], request_id='changed-screen')
        with patch.object(self.device, 'screenshot_raw', wraps=self.device.screenshot_raw) as capture:
            result = service.execute('act', 'web', **options)
            self.assert_rejected_with_frame(result, changed)
            repeated = service.execute('act', 'web', **options)
            self.assertEqual(repeated, result)
            self.assertEqual(capture.call_count, 1)
        fresh = service.execute('act', 'web', action=options['action'],
                                observation_id=result['observation']['id'], request_id='reviewed-screen')
        self.assertTrue(fresh['ok'], fresh)
        self.assertEqual(self.device.calls, [('tap', 20, 30)])

    def test_observed_service_returns_the_same_recovery_contract(self):
        original = self.observe()
        changed = png('black')
        self.device.frame = changed
        with patch.object(self.device, 'screenshot_raw', wraps=self.device.screenshot_raw) as capture:
            result = service.execute_observed(self.device, 'web', {'type': 'tap', 'x': 20, 'y': 30},
                                               original, session_keys('web'))
            self.assert_rejected_with_frame(result, changed)
            self.assertEqual(capture.call_count, 1)

    def test_type_send_early_rejection_keeps_observation_requirement(self):
        original = self.observe()
        self.device.frame = png('black')
        result = service.execute('type-send', 'web', text='example', input_x=20, input_y=30,
                                 prepare_only=True, observation_id=original['id'])
        self.assert_rejected_with_frame(result, self.device.frame)
        self.assertFalse(result['submission_attempted'])

    def test_expired_observation_requests_fresh_evidence_without_capture(self):
        with patch('time.time', return_value=1000):
            original = self.observe()
        with patch('time.time', return_value=1061), \
                patch.object(self.device, 'screenshot_raw', wraps=self.device.screenshot_raw) as capture:
            result = service.execute('act', 'web', action={'type': 'tap', 'x': 20, 'y': 30},
                                     observation_id=original['id'])
        self.assertEqual(result['outcome'], 'not_dispatched')
        self.assertTrue(result['requires_observation'])
        self.assertNotIn('observation', result)
        self.assertEqual(self.device.calls, [])
        capture.assert_not_called()

    def test_unrelated_input_validation_does_not_request_new_observation(self):
        original = self.observe()
        result = service.execute('act', 'web', action={'type': 'tap', 'x': -1, 'y': 30},
                                 observation_id=original['id'])
        self.assertEqual(result['outcome'], 'not_dispatched')
        self.assertFalse(result['requires_observation'])
        self.assertNotIn('observation', result)
        self.assertEqual(self.device.calls, [])

    def test_waiting_commands_return_and_journal_the_last_sample_without_recapture(self):
        for command in ('wait', 'act', 'tap'):
            with self.subTest(command=command):
                self.device.frame = png('white')
                original = self.observe()
                self.device.calls.clear()
                options = {}
                if command != 'wait':
                    options.update(observation_id=original['id'], observe_after=True)
                    if command == 'act':
                        options['action'] = {'type': 'tap', 'x': 20, 'y': 30}
                    else:
                        options.update(x=20, y=30)
                def tap(x, y):
                    self.device.calls.append(('tap', x, y))
                    self.device.frame = png('black')
                with patch.object(self.device, 'tap', side_effect=tap), \
                        patch.object(self.device, 'screenshot_raw', wraps=self.device.screenshot_raw) as capture, \
                        patch.object(observations.time, 'monotonic', side_effect=[0, 0, 0, 1]), \
                        patch.object(observations.time, 'sleep'):
                    result = service.execute(command, 'web', **options)
                self.assertTrue(result['ok'], result)
                observation = result if command == 'tap' else result['observation']
                self.assertEqual(Path(observation['source_path']).read_bytes(), self.device.frame)
                self.assertEqual(capture.call_count, 2 if command == 'wait' else 4)
                if command != 'wait':
                    events = [json.loads(line) for line in Path(result['record']).read_text().splitlines()]
                    after = next(event['data'] for event in events if event['kind'] == 'after')
                    self.assertEqual(after['id'], observation['id'])

    def test_mcp_rejection_returns_only_the_comparison_image(self):
        from saygo.mcp import server
        original = self.observe()
        self.device.frame = png('black')
        # The ordinary service produces the same payload consumed by MCP.
        result = service.execute('act', 'web', action={'type': 'tap', 'x': 20, 'y': 30},
                                 observation_id=original['id'], observe_after=False)
        with patch.object(server, '_device', return_value=result):
            content = server.device_act('web', {'type': 'tap', 'x': 20, 'y': 30},
                                        observation_id=original['id'], observe_after=False)
        self.assertEqual([part.type for part in content], ['text', 'image'])
        self.assertEqual(base64.b64decode(content[1].data), self.device.frame)
        payload = json.loads(content[0].text)
        self.assertFalse(payload['ok'])
        self.assertTrue(payload['requires_observation'])


if __name__ == '__main__':
    unittest.main()
