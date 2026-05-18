from __future__ import annotations

import argparse
from pathlib import Path

from robot_sorting_rl.envs import SIDE_BIN_ENV_ID
from robot_sorting_rl.training import train_sac


def parse_args():
    parser = argparse.ArgumentParser(description="Train robot sorting RL policy.")
    parser.add_argument("--env-id", default=SIDE_BIN_ENV_ID, help="default: FetchSideBinPlace-v0")
    parser.add_argument("--algo", choices=["sac"], default="sac")
    parser.add_argument("--total-timesteps", type=int, default=50_000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output-dir", type=Path, default=Path("checkpoints"))
    parser.add_argument("--tensorboard-log", type=Path, default=Path("runs/tensorboard"))
    parser.add_argument("--n-envs", type=int, default=1)
    parser.add_argument("--reward-type", choices=["sparse", "dense", "shaped"], default="shaped")
    parser.add_argument("--batch-size", type=int, default=None)
    parser.add_argument("--buffer-size", type=int, default=None)
    parser.add_argument("--gradient-steps", type=int, default=None)
    parser.add_argument("--learning-starts", type=int, default=None)
    parser.add_argument("--n-sampled-goal", type=int, default=None)
    parser.add_argument("--log-interval-steps", type=int, default=None)
    parser.add_argument("--checkpoint-interval", type=int, default=None)
    parser.add_argument("--resume-from", type=Path, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    checkpoint = train_sac(
        env_id=args.env_id,
        total_timesteps=args.total_timesteps,
        output_dir=args.output_dir,
        tensorboard_log=args.tensorboard_log,
        seed=args.seed,
        n_envs=args.n_envs,
        reward_type=args.reward_type,
        batch_size=args.batch_size,
        buffer_size=args.buffer_size,
        gradient_steps=args.gradient_steps,
        learning_starts=args.learning_starts,
        n_sampled_goal=args.n_sampled_goal,
        log_interval_steps=args.log_interval_steps,
        checkpoint_interval=args.checkpoint_interval,
        resume_from=args.resume_from,
    )
    print(f"saved checkpoint: {checkpoint}")


if __name__ == "__main__":
    main()
