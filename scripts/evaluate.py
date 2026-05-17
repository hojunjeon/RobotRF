from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from robot_sorting_rl.envs import SIDE_BIN_ENV_ID
from robot_sorting_rl.training import evaluate_model


def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate robot sorting RL checkpoint.")
    parser.add_argument("--env-id", default=SIDE_BIN_ENV_ID)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--episodes", type=int, default=100)
    parser.add_argument("--output", type=Path, default=None)
    return parser.parse_args()


def append_evaluation_result(output: Path, result: dict[str, Any]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        results = json.loads(output.read_text(encoding="utf-8"))
        if not isinstance(results, list):
            raise ValueError(f"evaluation output must contain a JSON array: {output}")
    else:
        results = []
    results.append(result)
    output.write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    args = parse_args()
    metrics = evaluate_model(
        args.checkpoint,
        env_id=args.env_id,
        episodes=args.episodes,
    )
    result = {
        "env_id": args.env_id,
        "checkpoint": str(args.checkpoint),
        **metrics,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.output:
        append_evaluation_result(args.output, result)
        print(f"appended evaluation result: {args.output}")


if __name__ == "__main__":
    main()
