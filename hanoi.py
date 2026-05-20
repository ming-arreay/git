"""Recursive Tower of Hanoi solver."""

from __future__ import annotations

import argparse


def solve_hanoi(n: int, source: str = "A", auxiliary: str = "B", target: str = "C") -> list[tuple[str, str]]:
    """Return the move sequence needed to solve a Tower of Hanoi puzzle."""
    if isinstance(n, bool) or not isinstance(n, int) or n <= 0:
        raise ValueError("n must be a positive integer")

    moves: list[tuple[str, str]] = []

    def move(disks: int, start: str, spare: str, finish: str) -> None:
        if disks == 1:
            moves.append((start, finish))
            return

        move(disks - 1, start, finish, spare)
        moves.append((start, finish))
        move(disks - 1, spare, start, finish)

    move(n, source, auxiliary, target)
    return moves


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve the Tower of Hanoi puzzle.")
    parser.add_argument("n", type=int, help="number of disks")
    args = parser.parse_args()

    for index, (source, target) in enumerate(solve_hanoi(args.n), start=1):
        print(f"{index}: {source} -> {target}")


if __name__ == "__main__":
    main()
