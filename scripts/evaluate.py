from __future__ import annotations

import argparse
import json
from pathlib import Path

from robot_sorting_rl.training import evaluate_model


def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate robot sorting RL checkpoint.")
    parser.add_argument("--stage", type=int, choices=[1, 2], required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--episodes", type=int, default=100)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    metrics = evaluate_model(args.checkpoint, stage=args.stage, episodes=args.episodes)
    print(json.dumps(metrics, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
