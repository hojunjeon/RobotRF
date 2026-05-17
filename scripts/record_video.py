from __future__ import annotations

import argparse
from pathlib import Path

import imageio.v2 as imageio

from robot_sorting_rl.envs import SIDE_BIN_ENV_ID
from robot_sorting_rl.training import make_env


def parse_args():
    parser = argparse.ArgumentParser(description="Record rollout video for a checkpoint.")
    parser.add_argument("--env-id", default=SIDE_BIN_ENV_ID)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("videos/rollout.mp4"))
    parser.add_argument("--max-steps", type=int, default=50)
    parser.add_argument("--fps", type=int, default=25)
    parser.add_argument("--start-delay-seconds", type=float, default=1.0)
    parser.add_argument("--end-delay-seconds", type=float, default=1.0)
    return parser.parse_args()


def collect_rollout_frames(
    env,
    model,
    max_steps: int,
    seed: int = 42,
    start_delay_frames: int = 0,
    end_delay_frames: int = 0,
):
    obs, _ = env.reset(seed=seed)
    frames = [env.render() for _ in range(max(0, start_delay_frames))]
    for _ in range(max_steps):
        action, _ = model.predict(obs, deterministic=True)
        obs, _, terminated, truncated, _ = env.step(action)
        frames.append(env.render())
        if terminated or truncated:
            break
    frames.extend(env.render() for _ in range(max(0, end_delay_frames)))
    return frames


def main() -> None:
    from stable_baselines3 import SAC

    args = parse_args()
    env = make_env(env_id=args.env_id, render_mode="rgb_array")
    model = SAC.load(args.checkpoint, env=env)
    start_delay_frames = round(max(0.0, args.start_delay_seconds) * args.fps)
    end_delay_frames = round(max(0.0, args.end_delay_seconds) * args.fps)
    frames = collect_rollout_frames(
        env=env,
        model=model,
        max_steps=args.max_steps,
        start_delay_frames=start_delay_frames,
        end_delay_frames=end_delay_frames,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    imageio.mimsave(args.output, frames, fps=args.fps)
    env.close()
    print(f"saved video: {args.output}")


if __name__ == "__main__":
    main()
