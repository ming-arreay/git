"""Visualize Tower of Hanoi solutions as PNG images or animated GIFs."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont

from hanoi import solve_hanoi


ROD_NAMES = ("A", "B", "C")


@dataclass(frozen=True)
class HanoiFrame:
    """A single puzzle state after applying one move."""

    move_index: int
    move: tuple[str, str] | None
    rods: dict[str, tuple[int, ...]]


def build_frames(n: int) -> list[HanoiFrame]:
    """Return every puzzle state from the initial layout to the solved layout."""
    moves = solve_hanoi(n)
    rods: dict[str, list[int]] = {
        "A": list(range(n, 0, -1)),
        "B": [],
        "C": [],
    }
    frames = [snapshot(0, None, rods)]

    for index, (source, target) in enumerate(moves, start=1):
        if not rods[source]:
            raise ValueError(f"cannot move from empty rod {source}")

        disk = rods[source].pop()
        if rods[target] and rods[target][-1] < disk:
            raise ValueError(f"cannot place disk {disk} on smaller disk {rods[target][-1]}")

        rods[target].append(disk)
        frames.append(snapshot(index, (source, target), rods))

    return frames


def snapshot(move_index: int, move: tuple[str, str] | None, rods: dict[str, list[int]]) -> HanoiFrame:
    """Create an immutable frame from mutable rod lists."""
    return HanoiFrame(
        move_index=move_index,
        move=move,
        rods={rod: tuple(disks) for rod, disks in rods.items()},
    )


def render_frame(
    frame: HanoiFrame,
    total_moves: int,
    disk_count: int,
    *,
    width: int = 960,
    height: int = 540,
) -> Image.Image:
    """Render one HanoiFrame as a Pillow image."""
    if width < 640 or height < 360:
        raise ValueError("width must be at least 640 and height must be at least 360")

    image = Image.new("RGB", (width, height), "#f5f7fb")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    colors = (
        "#4e79a7",
        "#f28e2b",
        "#e15759",
        "#76b7b2",
        "#59a14f",
        "#edc948",
        "#b07aa1",
        "#ff9da7",
    )

    base_y = int(height * 0.82)
    rod_top = int(height * 0.25)
    rod_height = base_y - rod_top
    rod_width = max(8, width // 120)
    base_height = max(12, height // 36)
    disk_height = max(18, min(34, int(rod_height / (disk_count + 2))))
    max_disk_width = int(width * 0.22)
    min_disk_width = int(width * 0.08)
    rod_xs = [int(width * ratio) for ratio in (0.22, 0.5, 0.78)]

    draw.text((28, 24), f"Tower of Hanoi - {disk_count} disks", fill="#172033", font=font)
    if frame.move is None:
        status = f"Start / {total_moves} moves"
    else:
        source, target = frame.move
        status = f"Move {frame.move_index}/{total_moves}: {source} -> {target}"
    draw.text((28, 48), status, fill="#42526e", font=font)

    draw.rounded_rectangle(
        (int(width * 0.08), base_y, int(width * 0.92), base_y + base_height),
        radius=base_height // 2,
        fill="#26364f",
    )

    for rod_name, rod_x in zip(ROD_NAMES, rod_xs):
        draw.rounded_rectangle(
            (rod_x - rod_width // 2, rod_top, rod_x + rod_width // 2, base_y),
            radius=rod_width // 2,
            fill="#526175",
        )
        draw.text((rod_x - 4, base_y + base_height + 10), rod_name, fill="#172033", font=font)

        for level, disk in enumerate(frame.rods[rod_name]):
            disk_scale = 0 if disk_count == 1 else (disk - 1) / (disk_count - 1)
            disk_width = int(min_disk_width + disk_scale * (max_disk_width - min_disk_width))
            left = rod_x - disk_width // 2
            top = base_y - (level + 1) * disk_height
            right = rod_x + disk_width // 2
            bottom = top + disk_height - 3
            color = colors[(disk - 1) % len(colors)]

            draw.rounded_rectangle((left, top, right, bottom), radius=8, fill=color, outline="#ffffff", width=2)
            label = str(disk)
            label_box = draw.textbbox((0, 0), label, font=font)
            label_width = label_box[2] - label_box[0]
            label_height = label_box[3] - label_box[1]
            draw.text(
                (rod_x - label_width / 2, top + (bottom - top - label_height) / 2),
                label,
                fill="#ffffff",
                font=font,
            )

    return image


def save_png(frames: list[HanoiFrame], output_path: Path, disk_count: int, step: int = -1) -> Path:
    """Save a single frame as a PNG image."""
    if not frames:
        raise ValueError("frames cannot be empty")

    frame = frames[step]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    render_frame(frame, len(frames) - 1, disk_count).save(output_path)
    return output_path


def save_gif(frames: list[HanoiFrame], output_path: Path, disk_count: int, duration_ms: int = 650) -> Path:
    """Save all frames as an animated GIF."""
    if not frames:
        raise ValueError("frames cannot be empty")

    rendered_frames = [
        render_frame(frame, len(frames) - 1, disk_count).convert("P", palette=Image.Palette.ADAPTIVE)
        for frame in frames
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rendered_frames[0].save(
        output_path,
        save_all=True,
        append_images=rendered_frames[1:],
        duration=duration_ms,
        loop=0,
        optimize=False,
    )
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create Tower of Hanoi visualizations.")
    parser.add_argument("n", type=int, help="number of disks")
    parser.add_argument("--gif", type=Path, help="animated GIF output path")
    parser.add_argument("--png", type=Path, help="single PNG output path")
    parser.add_argument("--duration", type=int, default=650, help="GIF frame duration in milliseconds")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    frames = build_frames(args.n)
    default_dir = Path("outputs")
    gif_path = args.gif or default_dir / f"hanoi_{args.n}.gif"
    png_path = args.png or default_dir / f"hanoi_{args.n}_final.png"

    saved_paths: Iterable[Path] = (
        save_gif(frames, gif_path, args.n, args.duration),
        save_png(frames, png_path, args.n),
    )

    print(f"Generated {len(frames) - 1} moves and {len(frames)} frames.")
    for path in saved_paths:
        print(path)


if __name__ == "__main__":
    main()
