from __future__ import annotations

import argparse
from pathlib import Path

from robot_sorting_rl.training import train_sac


def parse_args():
    parser = argparse.ArgumentParser(description="Train robot sorting RL policy.")
    parser.add_argument("--stage", type=int, choices=[1, 2], required=True)
    parser.add_argument("--algo", choices=["sac"], default="sac")
    parser.add_argument("--total-timesteps", type=int, default=50_000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output-dir", type=Path, default=Path("checkpoints"))
    parser.add_argument("--tensorboard-log", type=Path, default=Path("runs/tensorboard"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    checkpoint = train_sac(
        stage=args.stage,
        total_timesteps=args.total_timesteps,
        output_dir=args.output_dir,
        tensorboard_log=args.tensorboard_log,
        seed=args.seed,
    )
    print(f"saved checkpoint: {checkpoint}")


if __name__ == "__main__":
    main()
