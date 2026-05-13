from __future__ import annotations

from pathlib import Path

from robot_sorting_rl.algorithms import create_model_config
from robot_sorting_rl.envs import TabletopSortingEnv


def make_env(stage: int, render_mode: str | None = None) -> TabletopSortingEnv:
    return TabletopSortingEnv(stage=stage, render_mode=render_mode)


def train_sac(
    stage: int,
    total_timesteps: int,
    output_dir: Path,
    tensorboard_log: Path | None = None,
    seed: int = 42,
    progress_bar: bool = False,
):
    from stable_baselines3 import SAC
    from stable_baselines3.her.her_replay_buffer import HerReplayBuffer

    env = make_env(stage=stage)
    config = create_model_config(
        "sac",
        replay_buffer_class=HerReplayBuffer,
        tensorboard_log=str(tensorboard_log) if tensorboard_log else None,
    )
    model = SAC("MultiInputPolicy", env, seed=seed, **config.kwargs)
    model.learn(total_timesteps=total_timesteps, progress_bar=progress_bar)
    output_dir.mkdir(parents=True, exist_ok=True)
    checkpoint = output_dir / f"stage{stage}_sac.zip"
    model.save(checkpoint)
    env.close()
    return checkpoint


def evaluate_model(checkpoint: Path, stage: int, episodes: int = 100):
    from stable_baselines3 import SAC

    env = make_env(stage=stage)
    model = SAC.load(checkpoint, env=env)
    successes = 0
    total_reward = 0.0
    total_length = 0
    for episode in range(episodes):
        obs, _ = env.reset(seed=episode)
        done = False
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = env.step(action)
            total_reward += float(reward)
            total_length += 1
            done = terminated or truncated
        successes += int(info["is_success"])
    env.close()
    return {
        "episodes": episodes,
        "success_rate": successes / episodes,
        "mean_reward": total_reward / episodes,
        "mean_episode_length": total_length / episodes,
    }
