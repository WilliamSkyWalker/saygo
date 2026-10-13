"""移动输入、滚动和帧流故障回归；不连接实际设备。"""
import io
import unittest
from unittest.mock import Mock, patch

from PIL import Image
from saygo.platforms.appium import AppiumPlatform
from saygo.platforms.mjpeg import MjpegFrameReader


class MobileSafetyTests(unittest.TestCase):
    def platform(self, os_name='android'):
        platform = AppiumPlatform()
        platform._os = os_name
        platform._driver = Mock()
        platform._screen_width, platform._screen_height = 400, 800
        return platform

    def test_android_lost_input_response_never_sends_again(self):
        platform = self.platform()
        platform._driver.execute_script.side_effect = TimeoutError('response lost after dispatch')
        with self.assertRaisesRegex(RuntimeError, 'unknown|uncertain'):
            platform.input_text('示例文本')
        platform._driver.execute_script.assert_called_once()
        platform._driver.switch_to.active_element.send_keys.assert_not_called()

    def test_ios_lost_input_response_never_uses_fallback(self):
        platform = self.platform('ios')
        platform._driver.switch_to.active_element.send_keys.side_effect = TimeoutError('response lost')
        with self.assertRaisesRegex(RuntimeError, 'unknown|uncertain'):
            platform.input_text('示例文本')
        platform._driver.switch_to.active_element.send_keys.assert_called_once()
        platform._driver.execute_script.assert_not_called()

    def test_scroll_direction_means_viewport_toward_top_or_bottom(self):
        platform = self.platform()
        with patch.object(platform, '_w3c_swipe') as swipe:
            platform.scroll_up()
            swipe.assert_called_once_with(200, 200, 200, 600)
            swipe.reset_mock()
            platform.scroll_down()
            swipe.assert_called_once_with(200, 600, 200, 200)

    def test_stale_frame_falls_back_to_driver_and_failure_propagates(self):
        reader = MjpegFrameReader('http://127.0.0.1:9100')
        reader._latest = b'stale'
        reader._latest_at = 10.0
        platform = self.platform()
        platform._mjpeg = reader
        image = io.BytesIO()
        Image.new('RGB', (400, 800)).save(image, format='PNG')
        platform._driver.get_screenshot_as_png.return_value = image.getvalue()
        with patch('saygo.platforms.mjpeg.time.monotonic', return_value=100.0):
            self.assertIsNone(reader.latest())
            self.assertEqual(platform.screenshot_raw(), image.getvalue())
            platform._driver.get_screenshot_as_png.side_effect = OSError('device offline')
            with self.assertRaises(OSError):
                platform.screenshot_raw()
        self.assertEqual(platform._driver.get_screenshot_as_png.call_count, 2)

    def test_fresh_frame_then_stop_returns_no_frame(self):
        reader = MjpegFrameReader('http://127.0.0.1:9100')
        reader._latest, reader._latest_at = b'fresh', 10.0
        with patch('saygo.platforms.mjpeg.time.monotonic', return_value=10.1):
            self.assertEqual(reader.latest(), b'fresh')
            reader.stop()
            self.assertIsNone(reader.latest())

    def test_disconnect_invalidates_frame_before_reconnect_wait(self):
        reader = MjpegFrameReader('http://127.0.0.1:9100')
        reader._latest, reader._latest_at = b'old', 10.0

        def wait(_delay):
            self.assertIsNone(reader.latest())
            reader._stop.set()

        with patch.object(reader, '_read_stream', side_effect=OSError('EOF')), \
             patch.object(reader._stop, 'wait', side_effect=wait):
            reader._run()


if __name__ == '__main__':
    unittest.main()
