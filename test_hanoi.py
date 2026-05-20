"""Tests for the recursive Tower of Hanoi solver."""

from __future__ import annotations

import unittest

from hanoi import solve_hanoi


class TestHanoi(unittest.TestCase):
    def test_one_disk_has_one_move(self) -> None:
        self.assertEqual(solve_hanoi(1), [("A", "C")])

    def test_three_disks_has_seven_moves(self) -> None:
        self.assertEqual(len(solve_hanoi(3)), 7)

    def test_three_disk_solution_is_legal(self) -> None:
        moves = solve_hanoi(3)
        rods = {
            "A": [3, 2, 1],
            "B": [],
            "C": [],
        }

        for source, target in moves:
            self.assertTrue(rods[source], f"cannot move from empty rod {source}")
            disk = rods[source].pop()
            if rods[target]:
                self.assertLess(disk, rods[target][-1])
            rods[target].append(disk)

        self.assertEqual(rods["A"], [])
        self.assertEqual(rods["B"], [])
        self.assertEqual(rods["C"], [3, 2, 1])

    def test_invalid_input_raises_value_error(self) -> None:
        for value in (0, -1, 1.5, "3", True):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    solve_hanoi(value)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
