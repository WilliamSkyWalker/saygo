import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import Mock, patch

from saygo.desktop.runner import TaskLoop
from saygo.devices import actions
from saygo.platforms.desktop_local import LocalDesktopPlatform


class LaunchTests(unittest.TestCase):
    def test_local_task_never_captures_unused_browser(self):
        with tempfile.TemporaryDirectory() as tmp:
            image=Path(tmp)/'desktop.png'; image.write_bytes(b'png')
            state={'id':'task','status':'idle','desktop_goal':'Open Example App',
                   'workflow':{'resources':{'web':{'kind':'browser'},'computer':{'kind':'windows'}}},
                   'observations':{'computer':{'id':'obs','path':str(image)}}}
            rt=Mock(); rt.store.get.return_value=state
            def observe(task, resource):
                if resource=='web':raise RuntimeError('discarded browser capture timed out')
                return state
            rt.observe.side_effect=observe; rt.timeline.return_value={'timeline':[]}
            rt.submit.return_value=state
            model=Mock(); model.complete.side_effect=[json.dumps({'kind':'act','resource':'computer',
                'note':'Launch application from catalog','action':{'type':'open_app','target':'example.lnk'}}),
                json.dumps({'kind':'done','note':'Application is visible on the desktop'})]
            with patch('saygo.devices.applications.installed_applications',return_value=[{'name':'Example App','target':'example.lnk'}]):
                TaskLoop(model,rt).run('task',threading.Event(),threading.Event(),lambda state:None)
            self.assertEqual([c.args[1] for c in rt.observe.call_args_list],['computer','computer'])
            self.assertIn('web',json.loads(model.complete.call_args.args[1])['available_resources'])
            rt.submit.assert_called_once(); rt.finish.assert_called_once(); rt.handoff_task.assert_not_called()

    def driver(self):
        driver=LocalDesktopPlatform(); driver.kind='windows'; driver._win_w=1920; driver._win_h=1080
        driver.screenshot_raw=Mock(side_effect=AssertionError('unexpected screenshot'))
        return driver

    def test_catalog_launch_does_not_depend_on_stale_pixels_or_focus(self):
        driver=self.driver()
        observation={'session':'example','target':{'desktop_scope':'computer'},'at':0,'window_id':'old'}
        with patch('saygo.platforms.device_session.load_state',return_value={'os':'windows','desktop_scope':'computer'}), \
                patch('saygo.devices.applications.installed_applications',return_value=[{'target':'example.lnk'}]):
            result=actions.prepare(driver,{'type':'open_app','target':'example.lnk'},observation)
        self.assertEqual(result['target'],'example.lnk'); driver.screenshot_raw.assert_not_called()
        self.assertIsNone(driver._expected_window)

    def test_unknown_launch_and_changed_computer_binding_are_rejected(self):
        driver=self.driver(); observation={'session':'example','target':{'desktop_scope':'computer'}}
        with patch('saygo.platforms.device_session.load_state',return_value={'os':'windows','desktop_scope':'computer'}), \
                patch('saygo.devices.applications.installed_applications',return_value=[]):
            with self.assertRaisesRegex(ValueError,'catalog'):
                actions.prepare(driver,{'type':'open_app','target':'unknown.lnk'},observation)
        with patch('saygo.platforms.device_session.load_state',return_value={'os':'windows','app':'Example'}):
            with self.assertRaisesRegex(ValueError,'binding'):
                actions.prepare(driver,{'type':'open_app','target':'example.lnk'},observation)

    def test_coordinate_actions_still_reject_expired_observations(self):
        driver=self.driver()
        with self.assertRaisesRegex(ValueError,'expired'):
            actions.prepare(driver,{'type':'tap','x':10,'y':10},{'at':0})
