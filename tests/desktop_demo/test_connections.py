"""Whole-computer bindings, browser onboarding and local application inventory."""
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from saygo.desktop import connections
from saygo.devices import control
from saygo.platforms import device_session as ds


class ConnectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.state = patch.object(ds, 'STATE_DIR', Path(self.temp.name)/'sessions')
        self.state.start(); self.addCleanup(self.state.stop)

    def test_computer_connection_requires_no_app_and_keeps_shared_lock(self):
        fake = Mock(screen_size=(1920,1080))
        with patch.object(control, 'desktop_platform', return_value='windows'), patch.object(ds, 'attach_desktop', return_value=fake), patch.object(ds, 'release_controller'), \
                patch('saygo.runtime.locking.resource_guard') as guard:
            result = connections.connect_computer()
        self.assertTrue(result['connected'])
        self.assertEqual(ds.load_state(connections.COMPUTER)['desktop_scope'], 'computer')
        self.assertIn('desktop:local', guard.call_args.args[0])

    def test_computer_does_not_overwrite_window_binding(self):
        ds.save_state(connections.COMPUTER, {'kind':'desktop','os':'windows','app':'Example'})
        with patch.object(control, 'desktop_platform', return_value='windows'), \
                patch.object(ds, 'attach_desktop') as attach:
            with self.assertRaisesRegex(ValueError, 'window'):
                connections.connect_computer()
            attach.assert_not_called()
        self.assertEqual(ds.load_state(connections.COMPUTER)['app'], 'Example')

    def test_saved_bridge_is_not_assumed_live(self):
        (Path(self.temp.name)/'browser-bridge.json').write_text(json.dumps({'directory':self.temp.name}))
        with patch('saygo.integrations.browser_bridge.Client.call', side_effect=RuntimeError('offline')):
            result = connections.browser_status()
        self.assertFalse(result['connected'])

    def test_install_registers_before_opening_chrome(self):
        events = []
        with patch('saygo.integrations.browser_setup.setup', side_effect=lambda *a:events.append('setup') or {'directory':self.temp.name}), \
                patch.object(connections, 'open_chrome', side_effect=lambda url:events.append(url)):
            connections.install_browser()
        self.assertEqual(events[0], 'setup')
        self.assertTrue(events[1].startswith('https://chromewebstore.google.com/detail/'))
        self.assertTrue((Path(self.temp.name)/'browser-bridge.json').exists())

    def test_application_inventory_returns_launchable_targets(self):
        from saygo.devices.applications import installed_applications
        root = Path(self.temp.name)/'Microsoft/Windows/Start Menu/Programs/Example'
        root.mkdir(parents=True); (root/'Editor.lnk').touch(); (root/'readme.txt').touch()
        with patch.dict(os.environ, {'APPDATA':self.temp.name,'PROGRAMDATA':self.temp.name}), \
                patch('saygo.devices.applications.subprocess.run', return_value=Mock(stdout='[{"Name":"Store App","AppID":"example!App"}]')):
            apps = installed_applications('Windows')
        self.assertEqual([a['name'] for a in apps], ['Editor','Store App'])
        self.assertEqual(apps[0]['target'], str(root/'Editor.lnk'))
        self.assertEqual(apps[1]['target'], 'shell:AppsFolder\\example!App')

    def test_display_coordinates_and_focus_validation(self):
        from saygo.platforms.desktop_local import LocalDesktopPlatform
        driver = LocalDesktopPlatform()
        driver._win_x=-1920; driver._win_y=0
        self.assertEqual(driver._to_global(2000,100), (80,100))
        driver._pg=Mock()
        driver.observation_metadata=Mock(return_value={'window_id':'2','window_bounds':[-1920,0,3840,1080]})
        driver.expect_window({'window_id':'1','window_bounds':[-1920,0,3840,1080]})
        with self.assertRaisesRegex(RuntimeError, '重新观察'):
            driver.tap(2000,100)
        driver._pg.click.assert_not_called()

    def test_browser_initial_binding_does_not_activate_tab(self):
        from saygo.platforms.browser_extension import ExtensionBrowserPlatform
        browser=ExtensionBrowserPlatform(); browser.client=Mock()
        browser.client.call.return_value=[{'page_id':'page-1'}]
        browser.bind_page('page-1')
        self.assertEqual(browser.page_id,'page-1')
        self.assertEqual([c.args[0] for c in browser.client.call.call_args_list],['pages'])
