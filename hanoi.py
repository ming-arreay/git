"""Tower of Hanoi solvers."""

from __future__ import annotations

import argparse


def solve_hanoi(n: int, source: str = "A", auxiliary: str = "B", target: str = "C") -> list[tuple[str, str]]:
    """Return the move sequence needed to solve a Tower of Hanoi puzzle."""
    validate_disk_count(n)

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


def solve_hanoi_iterative(
    n: int,
    source: str = "A",
    auxiliary: str = "B",
    target: str = "C",
) -> list[tuple[str, str]]:
    """Return the Hanoi move sequence using an explicit stack instead of recursion."""
    validate_disk_count(n)

    moves: list[tuple[str, str]] = []
    stack: list[tuple[int, str, str, str]] = [(n, source, auxiliary, target)]

    while stack:
        disks, start, spare, finish = stack.pop()
        if disks == 1:
            moves.append((start, finish))
            continue

        stack.append((disks - 1, spare, start, finish))
        stack.append((1, start, spare, finish))
        stack.append((disks - 1, start, finish, spare))

    return moves


def validate_disk_count(n: int) -> None:
    """Validate the number of disks accepted by solver functions."""
    if isinstance(n, bool) or not isinstance(n, int) or n <= 0:
        raise ValueError("n must be a positive integer")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Solve the Tower of Hanoi puzzle.")
    parser.add_argument("n", nargs="?", type=int, help="number of disks")
    parser.add_argument("--disks", type=int, help="number of disks")
    parser.add_argument(
        "--mode",
        choices=("recursive", "iterative"),
        default="recursive",
        help="solver mode",
    )
    args = parser.parse_args()

    if args.disks is None and args.n is None:
        parser.error("the number of disks must be provided")

    args.disks = args.disks if args.disks is not None else args.n
    return args


def main() -> None:
    args = parse_args()
    solver = solve_hanoi if args.mode == "recursive" else solve_hanoi_iterative

    for index, (source, target) in enumerate(solver(args.disks), start=1):
        print(f"{index}: {source} -> {target}")


if __name__ == "__main__":
    main()
