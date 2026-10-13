"""Visual diff semantics and unchanged-frame fast path; no device access."""

import unittest
from unittest.mock import patch

from PIL import Image, ImageDraw

from saygo.skills.visual_diff import _compute_diff, _find_change_regions


class VisualDiffTests(unittest.TestCase):
    def test_unchanged_frame_skips_region_filter_and_returns_independent_rgb(self):
        source = Image.new("RGBA", (80, 80), (90, 120, 200, 100))
        with patch.object(Image.Image, "filter", side_effect=AssertionError("no changes to dilate")):
            output, ratio, regions = _compute_diff(source, source)
        self.assertEqual((ratio, regions), (0.0, []))
        self.assertEqual(output.mode, "RGB")
        self.assertEqual(output.tobytes(), source.convert("RGB").tobytes())
        output.putpixel((0, 0), (0, 0, 0))
        self.assertEqual(source.getpixel((0, 0)), (90, 120, 200, 100))

    def test_threshold_ratio_regions_and_overlay(self):
        previous = Image.new("RGB", (120, 120), "black")
        current = previous.copy()
        ImageDraw.Draw(current).rectangle((40, 40, 79, 79), fill=(31, 31, 31))
        output, ratio, regions = _compute_diff(previous, current)
        self.assertEqual(ratio, 1600 / 14400)
        self.assertEqual(regions, [(0, 0, 120, 120)])
        self.assertNotEqual(output.tobytes(), current.tobytes())
        self.assertEqual(current.getpixel((50, 50)), (31, 31, 31))
        self.assertEqual(_compute_diff(previous, current, threshold=31)[1:], (0.0, []))

    def test_previous_frame_resize_preserves_unchanged_result(self):
        previous = Image.new("L", (60, 60), 255)
        current = Image.new("RGB", (120, 120), "white")
        output, ratio, regions = _compute_diff(previous, current)
        self.assertEqual((ratio, regions), (0.0, []))
        self.assertEqual(output.tobytes(), current.tobytes())

    def test_regions_keep_diagonal_components_separate_and_clip_edges(self):
        mask = Image.new("L", (105, 105))
        for point in ((0, 0), (40, 40), (80, 80)):
            mask.putpixel(point, 255)
        self.assertCountEqual(_find_change_regions(mask),
                              [(0, 0, 40, 40), (40, 40, 80, 80), (80, 80, 105, 105)])
        self.assertEqual(_find_change_regions(mask, min_size=41), [])


if __name__ == "__main__":
    unittest.main()
