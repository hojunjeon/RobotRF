from __future__ import annotations

import argparse
from pathlib import Path

import imageio.v2 as imageio

from robot_sorting_rl.training import make_env


def parse_args():
    parser = argparse.ArgumentParser(description="Record rollout video for a checkpoint.")
    parser.add_argument("--env-id", default="FetchPickAndPlace-v4")
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("videos/rollout.mp4"))
    parser.add_argument("--max-steps", type=int, default=50)
    return parser.parse_args()


def main() -> None:
    from stable_baselines3 import SAC

    args = parse_args()
    env = make_env(env_id=args.env_id, render_mode="rgb_array")
    model = SAC.load(args.checkpoint, env=env)
    obs, _ = env.reset(seed=42)
    frames = [env.render()]
    for _ in range(args.max_steps):
        action, _ = model.predict(obs, deterministic=True)
        obs, _, terminated, truncated, _ = env.step(action)
        frames.append(env.render())
        if terminated or truncated:
            break
    args.output.parent.mkdir(parents=True, exist_ok=True)
    imageio.mimsave(args.output, frames, fps=25)
    env.close()
    print(f"saved video: {args.output}")


if __name__ == "__main__":
    main()
