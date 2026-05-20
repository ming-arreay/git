"""Generate Tower of Hanoi images without command-line arguments.

Run this file directly from an IDE or by double-clicking it. The output files
will be written into the outputs folder.
"""

from __future__ import annotations

from pathlib import Path

from hanoi_visual import build_frames, save_gif, save_png


DISK_COUNT = 10
GIF_DURATION_MS = 450
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"


def main() -> None:
    frames = build_frames(DISK_COUNT)
    gif_path = OUTPUT_DIR / f"hanoi_{DISK_COUNT}.gif"
    png_path = OUTPUT_DIR / f"hanoi_{DISK_COUNT}_final.png"

    save_gif(frames, gif_path, DISK_COUNT, duration_ms=GIF_DURATION_MS)
    save_png(frames, png_path, DISK_COUNT)

    print(f"Generated {len(frames) - 1} moves and {len(frames)} frames.")
    print(f"GIF: {gif_path}")
    print(f"PNG: {png_path}")
    input("Press Enter to close...")


if __name__ == "__main__":
    main()
