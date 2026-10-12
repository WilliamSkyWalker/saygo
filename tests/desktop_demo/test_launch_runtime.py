"""Regression scenarios through TaskLoop, real SQLite and shared action validation.

Only OS I/O and model responses are replaced. These are not live application or
provider acceptance tests. The browser remains connected but may fail to capture.
"""
import io
import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import Mock, patch

from PIL import Image
from saygo.desktop.runner import TaskLoop
from saygo.platforms import device_session as ds
from saygo.platforms.desktop_local import LocalDesktopPlatform
from saygo.runtime.interactive import InteractiveRuntime
from saygo.runtime.resources import VisualResource
from saygo.runtime.store import Store


def png(color):
    out = io.BytesIO()
    Image.new('RGB', (160, 100), color).save(out, format='PNG')
    return out.getvalue()


class Computer(LocalDesktopPlatform):
    def __init__(self):
        self.kind = 'mac'
        self._win_w, self._win_h = 160, 100
        self._win_x = self._win_y = 0
        self._pg = Mock()
        self.frame = png('white')
        self.focus = '1'

    def screenshot_raw(self):
        return self.frame

    def observation_metadata(self):
        return {'window_id': self.focus, 'process_id': 1,
                'window_bounds': [0, 0, 160, 100], 'desktop_scope': 'computer'}

    def teardown(self):
        pass


class Browser:
    platform_name = 'browser'
    screen_size = (160, 100)
    page_id = 'page-1'

    def __init__(self):
        self.captures = 0
        self.sleeping = True

    def screenshot_raw(self):
        self.captures += 1
        if self.sleeping:
            raise RuntimeError('Browser request timed out at Page.getLayoutMetrics; tab_discarded=true')
        return png('blue')

    def observation_metadata(self):
        return {'page_id': self.page_id}

    def teardown(self):
        pass


class LaunchRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.computer, self.browser = Computer(), Browser()
        self.launch = '/Applications/Example.app'
        self.catalog = [{'name': 'Example', 'target': self.launch}]
        for replacement in (
            patch.object(ds, 'STATE_DIR', self.root / 'sessions'),
            patch.object(ds, 'attach_desktop', return_value=self.computer),
            patch.object(ds, 'attach_browser', return_value=self.browser),
            patch('saygo.devices.applications.installed_applications', return_value=self.catalog),
            patch.object(VisualResource, 'wait', return_value={'condition_met': True}),
        ):
            replacement.start()
            self.addCleanup(replacement.stop)
        ds.save_state('computer', {'kind': 'desktop', 'os': 'mac', 'desktop_scope': 'computer'})
        ds.save_state('browser', {'kind': 'browser', 'browser_backend': 'extension',
                                 'bridge_directory': str(self.root / 'bridge'), 'page_id': 'page-1'})
        self.runtime = InteractiveRuntime(Store(self.root / 'runtime'))
        self.provider = Mock()
        self.loop = TaskLoop(self.provider, self.runtime)
        # Browser first reproduces the user's target ordering.
        self.task = self.loop.create('Open Example', {'web': 'browser', 'computer': 'computer'})
        self.pause, self.stop = threading.Event(), threading.Event()

    def run_loop(self):
        return self.loop.run(self.task['id'], self.pause, self.stop, lambda state: None)

    def step(self, kind, **values):
        return json.dumps({'kind': kind, 'note': 'Fixture decision', **values})

    def observe_computer(self):
        state = self.runtime.observe(self.task['id'], 'computer')
        return state['observations']['computer']['id']

    def submit(self, action, oid, request='request-1'):
        return self.runtime.submit(self.task['id'], 'computer', action, oid, request)

    def test_launch_with_changed_desktop_and_sleeping_browser_records_exactly_one_dispatch(self):
        contexts = []
        def complete(system, context, images):
            contexts.append(json.loads(context))
            if len(contexts) == 1:
                self.computer.frame = png('black')
                self.computer.focus = '2'
                return self.step('act', resource='computer', action={'type': 'open_app', 'target': self.launch})
            self.assertEqual(images, [('computer', png('green'))])
            return self.step('done')
        self.provider.complete.side_effect = complete
        def launch(command, **kwargs):
            pending = self.runtime.store.get(self.task['id'])['pending']
            self.assertEqual(pending['action']['target'], self.launch)
            self.assertEqual(command, ['open', self.launch])
            self.computer.frame = png('green')
        with patch('saygo.platforms.desktop_local.subprocess.run', side_effect=launch) as native:
            result = self.run_loop()
        self.assertEqual(result['status'], 'succeeded')
        native.assert_called_once()
        self.assertEqual(self.browser.captures, 0)
        self.assertEqual(contexts[0]['installed_applications'], self.catalog)
        self.assertIn('web', contexts[0]['available_resources'])
        events = self.runtime.timeline(self.task['id'])['timeline']
        self.assertEqual(sum(e['kind'] == 'action_dispatching' for e in events), 1)
        self.assertEqual(sum(e['kind'] == 'step_completed' for e in events), 1)
        self.assertIsNone(result['pending'])

    def test_changed_pixels_still_reject_click_before_dispatch(self):
        oid = self.observe_computer()
        self.computer.frame = png('black')
        state = self.submit({'type': 'tap', 'x': 40, 'y': 30}, oid)
        self.assertIn('Screen changed', state['error'])
        self.assertIsNone(state['pending'])
        self.computer._pg.click.assert_not_called()

    def test_changed_focus_still_rejects_input_before_dispatch(self):
        oid = self.observe_computer()
        self.computer.focus = '2'
        state = self.submit({'type': 'input', 'text': 'example'}, oid)
        self.assertIn('Target changed', state['error'])
        self.assertIsNone(state['pending'])
        self.computer._pg.hotkey.assert_not_called()

    def test_application_removed_after_discovery_is_not_launched(self):
        oid = self.observe_computer()
        self.catalog.clear()
        with patch('saygo.platforms.desktop_local.subprocess.run') as native:
            state = self.submit({'type': 'open_app', 'target': self.launch}, oid)
        self.assertIn('catalog', state['error'])
        self.assertIsNone(state['pending'])
        native.assert_not_called()

    def test_launch_response_loss_is_never_replayed_after_restart(self):
        oid = self.observe_computer()
        action = {'type': 'open_app', 'target': self.launch}
        with patch('saygo.platforms.desktop_local.subprocess.run', side_effect=OSError('response lost')) as native:
            state = self.submit(action, oid)
            self.assertEqual(state['status'], 'needs_review')
            restarted = InteractiveRuntime(Store(self.root / 'runtime'))
            duplicate = restarted.submit(self.task['id'], 'computer', action, oid, 'request-1')
            self.assertEqual(duplicate['status'], 'needs_review')
            with self.assertRaisesRegex(ValueError, 'needs_review'):
                restarted.submit(self.task['id'], 'computer', action, oid, 'request-2')
            native.assert_called_once()

    def test_pause_or_stop_during_model_call_prevents_launch(self):
        for signal in (self.pause, self.stop):
            with self.subTest(signal='pause' if signal is self.pause else 'stop'):
                def complete(*args):
                    signal.set()
                    return self.step('act', resource='computer', action={'type': 'open_app', 'target': self.launch})
                self.provider.complete.side_effect = complete
                with patch('saygo.platforms.desktop_local.subprocess.run') as native:
                    state = self.run_loop()
                self.assertEqual(state['status'], 'waiting_for_human' if signal is self.pause else 'cancelled')
                native.assert_not_called()
                self.assertEqual(state['requests'], {})
                if signal is self.pause:
                    self.runtime.cancel_task(self.task['id'], 'Reset fixture')
                    self.pause.clear()
                    self.task = self.loop.create('Open Example', {'web': 'browser', 'computer': 'computer'})

    def test_requested_browser_is_observed_and_selection_survives_restart(self):
        self.browser.sleeping = False
        self.provider.complete.side_effect = [self.step('observe', resource='web'), self.step('handoff')]
        state = self.run_loop()
        self.assertEqual(self.browser.captures, 1)
        saved = Store(self.root / 'runtime').get(state['id'])
        self.assertEqual(saved['desktop_active_resources'], ['computer', 'web'])
        self.runtime.resume_task(state['id'], 'Continue fixture')
        self.browser.captures = 0
        provider = Mock()
        provider.complete.return_value = self.step('done')
        loop = TaskLoop(provider, InteractiveRuntime(Store(self.root / 'runtime')))
        state = loop.run(state['id'], self.pause, self.stop, lambda state: None)
        self.assertEqual(state['status'], 'succeeded')
        self.assertEqual(self.browser.captures, 1)

    def test_requested_sleeping_browser_cannot_be_declared_successful(self):
        self.provider.complete.side_effect = [self.step('observe', resource='web')] + [self.step('done')] * 3
        state = self.run_loop()
        self.assertEqual(state['status'], 'waiting_for_human')
        self.assertEqual(state['requests'], {})
        self.assertGreater(self.browser.captures, 0)

    def test_unicode_session_round_trip_with_non_utf8_system_default(self):
        from saygo.devices import control
        binding = {'kind': 'desktop', 'os': 'mac', 'app': '示例应用',
                   'handoff': {'instructions': '用户暂停，请核对后继续'}}
        ds.save_state('unicode-example', binding)
        original_read = Path.read_text
        def legacy_default(path, encoding=None, errors=None, **kwargs):
            return original_read(path, encoding=encoding or 'cp1252', errors=errors, **kwargs)
        with patch.object(Path, 'read_text', legacy_default):
            self.assertEqual(ds.load_state('unicode-example'), binding)
            rows = control.sessions()
        entry = next(row for row in rows if row['session'] == 'unicode-example')
        self.assertEqual(entry['app'], '示例应用')
        self.assertNotIn('error', entry)
