from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from robot_sorting_rl.envs import SIDE_BIN_ENV_ID
from robot_sorting_rl.training import make_env


def parse_args():
    parser = argparse.ArgumentParser(description="Inspect side-bin wall contacts in a rollout.")
    parser.add_argument("--env-id", default=SIDE_BIN_ENV_ID)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--max-steps", type=int, default=50)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def contact_pairs(env) -> list[tuple[str, str]]:
    unwrapped = env.unwrapped
    pairs = []
    for index in range(unwrapped.data.ncon):
        contact = unwrapped.data.contact[index]
        geom1 = unwrapped._geom_name(contact.geom1)
        geom2 = unwrapped._geom_name(contact.geom2)
        if unwrapped._is_wall_contact_pair(geom1, geom2):
            pairs.append((geom1, geom2))
    return pairs


def main() -> None:
    from stable_baselines3 import SAC

    args = parse_args()
    env = make_env(env_id=args.env_id, render_mode="rgb_array")
    model = SAC.load(args.checkpoint, env=env)
    obs, _ = env.reset(seed=args.seed)

    print("step,object_xyz,wall_contact,contact_pairs")
    for step in range(1, args.max_steps + 1):
        action, _ = model.predict(obs, deterministic=True)
        obs, _, terminated, truncated, info = env.step(action)
        pairs = contact_pairs(env)
        object_xyz = np.asarray(obs["achieved_goal"]).round(4).tolist()
        print(f"{step},{object_xyz},{info.get('is_wall_contact', False)},{pairs}")
        if terminated or truncated:
            break

    env.close()


if __name__ == "__main__":
    main()
