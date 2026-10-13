"""Offline screenshot comparison and sampling contracts using synthetic PNGs."""

import io
import unittest
from unittest.mock import Mock, patch

from PIL import Image, ImageDraw

from saygo.vision import settle


def png(color=0, size=(100, 100), changed_columns=0):
    rgb = (color, color, color) if isinstance(color, int) else color
    image = Image.new("RGB", size, rgb)
    if changed_columns:
        ImageDraw.Draw(image).rectangle((0, 0, changed_columns - 1, size[1]), fill="white")
    output = io.BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


class SettleTests(unittest.TestCase):
    def test_ratio_keeps_strict_threshold_mask_and_size_alignment(self):
        black = png()
        self.assertEqual(settle._change_ratio(black, png(30)), 0.0)
        self.assertEqual(settle._change_ratio(black, png(31)), 1.0)
        self.assertEqual(settle._change_ratio(black, png((31, 0, 0))), 0.0)
        self.assertEqual(settle._change_ratio(black, png(size=(80, 160))), 0.0)
        status_bar = Image.new("RGB", (100, 100), "black")
        ImageDraw.Draw(status_bar).rectangle((0, 0, 99, 3), fill="white")
        output = io.BytesIO()
        status_bar.save(output, format="PNG")
        self.assertEqual(settle._change_ratio(black, output.getvalue()), 0.0)

    def test_invalid_frame_is_treated_as_changed(self):
        for previous, current in ((b"invalid", png()), (png(), b"invalid")):
            with self.subTest(previous_is_invalid=previous == b"invalid"):
                self.assertEqual(settle._change_ratio(previous, current), 1.0)

    def test_sampling_preserves_route_boundary_and_original_frames(self):
        black = png()
        below = [black, png(changed_columns=1), black]
        boundary = [black, png(changed_columns=2), black]
        self.assertEqual(settle.sample_then_frames(below), ([black], False))
        chosen, dynamic = settle.sample_then_frames(boundary)
        self.assertTrue(dynamic)
        self.assertEqual(chosen, boundary)
        for original, selected in zip(boundary, chosen):
            self.assertIs(original, selected)
        self.assertEqual(settle.sample_then_frames([]), ([], False))
        self.assertEqual(settle.sample_then_frames(boundary[:2]), ([boundary[1]], False))
        malformed = [black, b"invalid", black]
        self.assertEqual(settle.sample_then_frames(malformed), (malformed, True))

    def test_sampling_prepares_each_selected_frame_once(self):
        frames = [png(), png(), png()]
        with patch.object(settle, "_prep", wraps=settle._prep) as prepare:
            self.assertEqual(settle.sample_then_frames(frames), ([frames[-1]], False))
        self.assertEqual(prepare.call_count, 3)

    def test_wait_resets_stability_and_prepares_each_frame_once(self):
        frames = [png(), png(), png(255), png(255), png(255)]
        platform = Mock()
        platform.screenshot_raw.side_effect = frames
        with patch.object(settle.time, "sleep"), \
                patch.object(settle.time, "monotonic", return_value=0), \
                patch.object(settle, "_prep", wraps=settle._prep) as prepare:
            self.assertEqual(settle.wait_settled(platform), (True, frames))
        self.assertEqual(prepare.call_count, len(frames))

    def test_wait_retains_frames_on_failure_and_timeout(self):
        frame = png()
        platform = Mock()
        platform.screenshot_raw.side_effect = [frame, RuntimeError("capture failed")]
        with patch.object(settle.time, "sleep"), \
                patch.object(settle, "_prep", wraps=settle._prep) as prepare:
            self.assertEqual(settle.wait_settled(platform), (False, [frame]))
        prepare.assert_not_called()
        platform.screenshot_raw.side_effect = RuntimeError("capture failed")
        self.assertEqual(settle.wait_settled(platform), (False, []))
        platform.screenshot_raw.side_effect = [frame]
        with patch.object(settle, "_prep", wraps=settle._prep) as prepare:
            self.assertEqual(settle.wait_settled(platform, timeout_s=0), (False, [frame]))
        prepare.assert_not_called()


if __name__ == "__main__":
    unittest.main()
