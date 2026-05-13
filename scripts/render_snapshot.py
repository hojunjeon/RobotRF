from __future__ import annotations

import argparse
from pathlib import Path

import imageio.v2 as imageio

from robot_sorting_rl.training import make_env


def parse_args():
    parser = argparse.ArgumentParser(description="Render one environment snapshot.")
    parser.add_argument("--stage", type=int, choices=[1, 2], required=True)
    parser.add_argument("--output", type=Path, default=Path("docs/stage_snapshot.png"))
    parser.add_argument("--seed", type=int, default=7)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    env = make_env(stage=args.stage, render_mode="rgb_array")
    _, info = env.reset(seed=args.seed)
    frame = env.render()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    imageio.imwrite(args.output, frame)
    env.close()
    print(f"saved snapshot: {args.output}")
    print(f"stage: {info['stage']}")
    print(f"object_type: {info['object_type']}")


if __name__ == "__main__":
    main()
