"""Bounded, local screenshot comparisons; no model or browser needed."""
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image, ImageDraw

from saygo.devices import actions, observations
from saygo.platforms import device_session as ds
from tests.control_demo.test_agent_service import Device


def frame(box=None, color='black'):
    image = Image.new('RGB', (1000, 800), 'white')
    if box:
        ImageDraw.Draw(image).rectangle(box, fill=color)
    stream = io.BytesIO()
    image.save(stream, format='PNG')
    return stream.getvalue()


class LocalMotionTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        patcher = patch.object(ds, 'STATE_DIR', self.root / 'sessions')
        patcher.start()
        self.addCleanup(patcher.stop)
        ds.save_state('web', {'kind': 'browser', 'browser_backend': 'extension'})
        self.device = Device()
        self.device.screen_size = (1000, 800)
        self.device.frame = frame()
        self.a = frame()
        self.b = frame((600, 550, 636, 610))

    def wait_observation(self, frames):
        clock = [0.0]
        def sleep(seconds):
            clock[0] += seconds
        with patch.object(self.device, 'screenshot_raw', side_effect=frames) as capture, \
                patch.object(observations.time, 'monotonic', side_effect=lambda: clock[0]), \
                patch.object(observations.time, 'sleep', side_effect=sleep):
            result = observations.wait(self.device, timeout=.4, interval=.2, session='web')
            shot = observations.capture_after_wait(self.device, result, 'web')
        self.assertEqual(capture.call_count, 3)
        # Internal phases never appear in tool JSON or as extra returned images.
        self.assertNotIn('frames', json.dumps(result))
        self.assertEqual(Path(shot['source_path']).read_bytes(), frames[-1])
        return shot

    def test_known_local_phase_can_return_away_from_target(self):
        shot = self.wait_observation([self.b, self.a, self.a])
        self.device.frame = self.b
        prepared = actions.prepare(self.device, {'type': 'tap', 'x': 150, 'y': 650}, shot)
        self.assertEqual(prepared['x'], 150)

    def test_unseen_content_inside_same_small_area_is_rejected(self):
        shot = self.wait_observation([self.b, self.a, self.a])
        self.device.frame = frame((600, 550, 636, 610), 'red')
        with self.assertRaisesRegex(ValueError, 'Screen changed'):
            actions.prepare(self.device, {'type': 'tap', 'x': 150, 'y': 650}, shot)

    def test_motion_in_target_context_remains_blocked(self):
        shot = self.wait_observation([self.b, self.a, self.a])
        self.device.frame = self.b
        # Outside the old 49x49 target box, inside its surrounding context.
        with self.assertRaisesRegex(ValueError, 'Screen changed'):
            actions.prepare(self.device, {'type': 'tap', 'x': 520, 'y': 650}, shot)

    def test_input_and_swipe_do_not_use_local_motion_exception(self):
        shot = self.wait_observation([self.b, self.a, self.a])
        self.device.frame = self.b
        for action in ({'type': 'input', 'text': 'example'},
                       {'type': 'swipe', 'x1': 100, 'y1': 100, 'x2': 900, 'y2': 700}):
            with self.subTest(action=action['type']), self.assertRaisesRegex(ValueError, 'Screen changed'):
                actions.prepare(self.device, action, shot)

    def test_large_or_distributed_changes_are_not_local_motion(self):
        for box in ((500, 400, 900, 700), (10, 10, 980, 12)):
            with self.subTest(box=box):
                changed = frame(box)
                shot = self.wait_observation([changed, self.a, self.a])
                self.device.frame = changed
                with self.assertRaisesRegex(ValueError, 'Screen changed'):
                    actions.prepare(self.device, {'type': 'tap', 'x': 150, 'y': 650}, shot)

    def test_normal_observation_does_not_inherit_motion_evidence(self):
        self.wait_observation([self.b, self.a, self.a])
        self.device.frame = self.a
        shot = observations.capture(self.device, 'web')
        self.device.frame = self.b
        with self.assertRaisesRegex(ValueError, 'Screen changed'):
            actions.prepare(self.device, {'type': 'tap', 'x': 150, 'y': 650}, shot)

    def test_changed_identity_still_blocks_known_phase(self):
        self.device.page_id = 'first-page'
        shot = self.wait_observation([self.b, self.a, self.a])
        self.device.frame = self.b
        self.device.page_id = 'second-page'
        with self.assertRaisesRegex(ValueError, 'Target changed'):
            actions.prepare(self.device, {'type': 'tap', 'x': 150, 'y': 650}, shot)

    def test_changed_identity_during_wait_does_not_relabel_old_pixels(self):
        self.device.page_id = 'first-page'
        identity = observations.metadata(self.device, self.a, 'web')
        result = observations.WaitResult({'condition_met': True}, [self.b, self.a], identity)
        self.device.page_id = 'second-page'
        with self.assertRaisesRegex(ValueError, 'Target changed during wait'):
            observations.capture_after_wait(self.device, result, 'web')
        self.assertFalse((self.root / 'observations').exists())

    def test_missing_phase_file_fails_closed(self):
        shot = self.wait_observation([self.b, self.a, self.a])
        (self.root / 'observations' / f"{shot['id']}-phase-0.png").unlink()
        self.device.frame = self.b
        with self.assertRaisesRegex(ValueError, 'Screen changed'):
            actions.prepare(self.device, {'type': 'tap', 'x': 150, 'y': 650}, shot)

    def test_changed_screen_still_requires_observation_when_evidence_save_fails(self):
        shot = observations.capture(self.device, 'web')
        self.device.frame = self.b
        with patch.object(observations, 'save', side_effect=OSError('disk full')):
            with self.assertRaises(observations.ObservationChangedError) as caught:
                actions.prepare(self.device, {'type': 'tap', 'x': 150, 'y': 650}, shot)
        self.assertTrue(caught.exception.requires_observation)

    def test_delayed_wait_result_keeps_capture_time_and_expires(self):
        identity = observations.metadata(self.device, self.a, 'web')
        result = observations.WaitResult({'condition_met': True}, [self.b, self.a], identity, captured_at=1000)
        with patch.object(observations.time, 'time', return_value=1061):
            shot = observations.capture_after_wait(self.device, result, 'web')
            self.assertEqual(shot['at'], 1000)
            with self.assertRaisesRegex(ValueError, 'Observation expired'):
                actions.prepare(self.device, {'type': 'tap', 'x': 150, 'y': 650}, shot)

    def test_optional_phase_write_failure_preserves_observation(self):
        original = Path.write_bytes
        def write(path, data):
            if '-phase-' in path.name:
                raise OSError('disk full')
            return original(path, data)
        with patch.object(Path, 'write_bytes', write):
            shot = self.wait_observation([self.b, self.a, self.a])
        self.assertTrue(Path(shot['source_path']).exists())
        self.device.frame = self.b
        with self.assertRaisesRegex(ValueError, 'Screen changed'):
            actions.prepare(self.device, {'type': 'tap', 'x': 150, 'y': 650}, shot)


if __name__ == '__main__':
    unittest.main()
