from __future__ import annotations

import argparse
from pathlib import Path

import gymnasium as gym
import gymnasium_robotics
import imageio.v2 as imageio


def parse_args():
    parser = argparse.ArgumentParser(description="Render one Gymnasium-Robotics snapshot.")
    parser.add_argument("--env-id", default="FetchPickAndPlace-v4")
    parser.add_argument("--output", type=Path, default=Path("docs/fetch_pick_and_place_snapshot.png"))
    parser.add_argument("--seed", type=int, default=7)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    gym.register_envs(gymnasium_robotics)
    env = gym.make(args.env_id, render_mode="rgb_array")
    _, info = env.reset(seed=args.seed)
    frame = env.render()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    imageio.imwrite(args.output, frame)
    env.close()
    print(f"saved snapshot: {args.output}")
    print(f"env_id: {args.env_id}")
    print(f"info_keys: {sorted(info.keys())}")


if __name__ == "__main__":
    main()
