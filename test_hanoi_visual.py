"""Tests for Tower of Hanoi visualization state generation."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from hanoi_visual import build_frames, save_gif, save_png


class TestHanoiVisual(unittest.TestCase):
    def test_three_disks_builds_initial_plus_seven_move_frames(self) -> None:
        frames = build_frames(3)

        self.assertEqual(len(frames), 8)
        self.assertEqual(frames[0].rods["A"], (3, 2, 1))
        self.assertEqual(frames[-1].rods["A"], ())
        self.assertEqual(frames[-1].rods["B"], ())
        self.assertEqual(frames[-1].rods["C"], (3, 2, 1))

    def test_frame_moves_match_expected_sequence(self) -> None:
        frames = build_frames(2)
        moves = [frame.move for frame in frames[1:]]

        self.assertEqual(moves, [("A", "B"), ("A", "C"), ("B", "C")])

    def test_visual_files_are_created(self) -> None:
        frames = build_frames(2)

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            png_path = save_png(frames, temp_path / "hanoi.png", 2)
            gif_path = save_gif(frames, temp_path / "hanoi.gif", 2, duration_ms=100)

            self.assertTrue(png_path.exists())
            self.assertGreater(png_path.stat().st_size, 0)
            self.assertTrue(gif_path.exists())
            self.assertGreater(gif_path.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
