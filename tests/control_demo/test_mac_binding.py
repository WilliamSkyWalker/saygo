"""macOS 前台窗口跨控制器重连时不允许换窗。"""
import sys
import unittest
from unittest.mock import Mock, patch

from saygo.platforms.desktop_mac import DesktopMacPlatform
from saygo.platforms import device_session as ds


def window(number, pid=10, width=400):
    return {'kCGWindowOwnerName': 'Example App', 'kCGWindowOwnerPID': pid,
            'kCGWindowNumber': number, 'kCGWindowLayer': 0,
            'kCGWindowBounds': {'X': 0, 'Y': 0, 'Width': width, 'Height': 300}}


class MacBindingTests(unittest.TestCase):
    def test_observe_keeps_selected_window_when_other_window_is_larger(self):
        platform = DesktopMacPlatform()
        platform._app_name = 'Example App'
        platform._apply_window(window(11))
        platform._Q = Mock()
        platform._Q.CGWindowListCopyWindowInfo.return_value = [window(12, width=1200), window(11)]
        self.assertEqual(platform._find_window()['kCGWindowNumber'], 11)
        platform._Q.CGWindowListCopyWindowInfo.return_value = [window(12)]
        self.assertIsNone(platform._find_window())
        platform._Q.CGWindowListCopyWindowInfo.return_value = [window(11, pid=99)]
        self.assertIsNone(platform._find_window())

    def test_bound_setup_never_launches_and_restores_identity(self):
        quartz = Mock()
        quartz.CGWindowListCopyWindowInfo.return_value = [window(12, width=1200), window(11)]
        platform = DesktopMacPlatform()
        with patch.dict(sys.modules, {'pyautogui': Mock(), 'Quartz': quartz, 'AppKit': Mock()}), \
             patch.object(platform, '_open_app') as launch:
            platform.setup({'mac': {'app': 'Example App', 'process_id': 10, 'window_id': '11'}})
        launch.assert_not_called()
        self.assertEqual(platform.connection['window_id'], '11')
        self.assertEqual(platform.connection['process_id'], 10)

    def test_bound_window_missing_rejects_before_launch(self):
        quartz = Mock()
        quartz.CGWindowListCopyWindowInfo.return_value = [window(12)]
        platform = DesktopMacPlatform()
        with patch.dict(sys.modules, {'pyautogui': Mock(), 'Quartz': quartz, 'AppKit': Mock()}), \
             patch.object(platform, '_open_app') as launch:
            with self.assertRaisesRegex(RuntimeError, 'window|窗口'):
                platform.setup({'mac': {'app': 'Example App', 'process_id': 10, 'window_id': '11'}})
        launch.assert_not_called()

    def test_attach_passes_foreground_window_identity(self):
        platform = Mock()
        with patch('saygo.platforms.create_platform', return_value=platform):
            ds.attach_desktop({'os': 'mac', 'app': 'Example App', 'process_id': 10, 'window_id': '11'})
        self.assertEqual(platform.setup.call_args.args[0]['mac']['window_id'], '11')


if __name__ == '__main__':
    unittest.main()
