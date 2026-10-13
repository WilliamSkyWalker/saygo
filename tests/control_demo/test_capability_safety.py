"""能力声明和语义校验必须在派发之前拒绝不支持的动作。"""
import unittest
from unittest.mock import Mock

from saygo.devices.actions import capabilities, prepare
from saygo.platforms.appium import AppiumPlatform
from saygo.platforms.browser_playwright import PlaywrightBrowserPlatform
from saygo.platforms.desktop_mac import DesktopMacPlatform


class CapabilitySafetyTests(unittest.TestCase):
    def test_open_operations_match_backend(self):
        for platform, allowed, rejected in (
            (AppiumPlatform(), 'open_app', 'open_url'),
            (PlaywrightBrowserPlatform(), 'open_url', 'open_app'),
            (DesktopMacPlatform(), 'open_app', 'open_url'),
        ):
            with self.subTest(platform=type(platform).__name__):
                supported = capabilities(platform)['actions']
                self.assertIn(allowed, supported)
                self.assertNotIn(rejected, supported)
                with self.assertRaisesRegex(ValueError, 'Unsupported action'):
                    prepare(platform, {'type': rejected, 'url': 'https://example.test', 'target': 'com.example.app'})

    def test_scroll_capabilities_explain_viewport_direction(self):
        result = capabilities(AppiumPlatform())
        self.assertEqual(result['scroll_direction'], 'viewport')
        self.assertEqual(result['scroll_up'], 'toward_top')
        self.assertEqual(result['scroll_down'], 'toward_bottom')


if __name__ == '__main__':
    unittest.main()
