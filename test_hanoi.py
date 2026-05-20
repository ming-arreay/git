"""Tests for the recursive Tower of Hanoi solver."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

from hanoi import solve_hanoi, solve_hanoi_iterative


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

    def test_recursive_and_iterative_match_for_three_disks(self) -> None:
        self.assertEqual(solve_hanoi(3), solve_hanoi_iterative(3))

    def test_cli_options_run_successfully(self) -> None:
        script_path = Path(__file__).with_name("hanoi.py")
        expected_output = "\n".join(
            [
                "1: A -> C",
                "2: A -> B",
                "3: C -> B",
                "4: A -> C",
                "5: B -> A",
                "6: B -> C",
                "7: A -> C",
            ]
        )

        for mode in ("recursive", "iterative"):
            with self.subTest(mode=mode):
                result = subprocess.run(
                    [sys.executable, str(script_path), "--disks", "3", "--mode", mode],
                    capture_output=True,
                    check=True,
                    text=True,
                )
                self.assertEqual(result.stdout.strip(), expected_output)


if __name__ == "__main__":
    unittest.main()
