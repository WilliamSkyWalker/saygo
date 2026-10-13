"""QA 与统一控制入口的资源、观察及不重放契约。"""
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from PIL import Image
from saygo.platforms import device_session as ds
from saygo.platforms.base import ActionOutcomeUnknown
from saygo.runtime.locking import resource_guard, reserve, release
from saygo.runtime.store import BusyError


class QAControlSafetyTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        patcher = patch.object(ds, 'STATE_DIR', Path(tmp.name) / 'sessions')
        patcher.start(); self.addCleanup(patcher.stop)
        out = io.BytesIO()
        Image.new('RGB', (80, 60), 'white').save(out, format='PNG')
        self.png = out.getvalue()

    def controller(self):
        from saygo.qa.control import QAPlatform
        from saygo.platforms.appium import AppiumPlatform
        raw = AppiumPlatform()
        raw._driver = Mock()
        raw._screen_width, raw._screen_height = 80, 60
        raw._driver.get_screenshot_as_png.return_value = self.png
        raw._w3c_tap = Mock()
        return QAPlatform(raw, ['mobile:example-device']), raw

    def test_task_ownership_blocks_qa_before_input(self):
        platform, raw = self.controller()
        platform.screenshot_raw()
        reserve('other-task', ['mobile:example-device'])
        self.addCleanup(release, 'other-task')
        with self.assertRaises(BusyError):
            platform.execute_action({'type': 'tap', 'x': 10, 'y': 20})
        raw._w3c_tap.assert_not_called()

    def test_unknown_input_stops_all_following_qa_input_and_retains_ownership(self):
        platform, raw = self.controller()
        platform.screenshot_raw()
        raw._w3c_tap.side_effect = TimeoutError('response lost')
        with self.assertRaises(ActionOutcomeUnknown):
            platform.execute_action({'type': 'tap', 'x': 10, 'y': 20})
        platform.screenshot_raw()
        with self.assertRaises(ActionOutcomeUnknown):
            platform.execute_action({'type': 'tap', 'x': 10, 'y': 20})
        raw._w3c_tap.assert_called_once()
        with self.assertRaises(BusyError), resource_guard(['mobile:example-device']):
            pass

    def test_changed_image_rejects_qa_action_without_dispatch(self):
        platform, raw = self.controller()
        platform.screenshot_raw()
        out = io.BytesIO()
        Image.new('RGB', (80, 60), 'black').save(out, format='PNG')
        raw._driver.get_screenshot_as_png.return_value = out.getvalue()
        with self.assertRaises(ValueError):
            platform.execute_action({'type': 'tap', 'x': 10, 'y': 20})
        raw._w3c_tap.assert_not_called()

    def test_split_actions_propagate_uncertainty_instead_of_fallback(self):
        from saygo.qa.agent import Agent
        agent = Agent.__new__(Agent)
        agent.platform = Mock()
        agent.platform.tap.side_effect = ActionOutcomeUnknown('unknown result')
        agent.locator = Mock(enabled=True)
        agent.locator.locate.return_value = (10, 20)
        with self.assertRaises(ActionOutcomeUnknown):
            agent._run_action_step({'type': 'tap', 'target': 'Example button'}, self.png, (80, 60))

    def test_agent_loop_preserves_current_action_and_screenshot_on_lost_response(self):
        from saygo.qa.agent import Agent
        agent = Agent.__new__(Agent)
        agent.platform, raw = self.controller()
        raw._w3c_tap.side_effect = TimeoutError('response lost')
        agent.brain = Mock(history=[], max_tokens=100, model='example')
        agent.brain.decide.return_value = {
            'action': {'type': 'tap', 'x': 10, 'y': 20},
            'step_progress': {'current_step_index': 1, 'current_step_status': 'in_progress'}}
        agent.probe_context = {}
        agent._load_reference_images = Mock(return_value=[])
        agent.planner_model = 'example'
        agent.max_steps = 2
        agent.step_delay = 0
        agent.settle_enabled = agent.split_act_check = agent.merge_asserts = False
        agent.assert_burst_frames = 1
        agent.skills_pipeline = []
        agent.locator = Mock(enabled=False)
        with patch('saygo.qa.agent.plan_scenario', return_value=Mock(steps=[])):
            result = agent.run('Tap the example button')
        self.assertTrue(result['needs_review'])
        self.assertEqual(result['result'], 'error')
        self.assertEqual(result['steps_detail'][-1]['action']['type'], 'tap')
        self.assertEqual(result['steps_detail'][-1]['screenshot_png'], self.png)
        self.assertTrue(Path(result['operation']['record']).is_file())
        agent.brain.decide.assert_called_once()
        raw._w3c_tap.assert_called_once()

    def test_case_guard_allows_same_thread_nested_operation_but_not_another_thread(self):
        from concurrent.futures import ThreadPoolExecutor
        def attempt():
            with resource_guard(['mobile:example-device']):
                pass
        with resource_guard(['mobile:example-device'], allow_nested=True):
            with resource_guard(['mobile:example-device']):
                pass
            with ThreadPoolExecutor(max_workers=1) as pool:
                with self.assertRaises(BusyError):
                    pool.submit(attempt).result()
