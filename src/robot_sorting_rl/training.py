from __future__ import annotations

from pathlib import Path
from typing import Any

from robot_sorting_rl.algorithms import create_model_config


def make_env(env_id: str = "FetchPickAndPlace-v4", render_mode: str | None = None):
    import gymnasium as gym
    import gymnasium_robotics

    gym.register_envs(gymnasium_robotics)
    return gym.make(env_id, render_mode=render_mode)


def _make_env_fn(env_id: str, seed: int, rank: int):
    def _init():
        env = make_env(env_id=env_id)
        env.reset(seed=seed + rank)
        return env

    return _init


def make_training_env(env_id: str, seed: int, n_envs: int = 1):
    if n_envs < 1:
        raise ValueError("n_envs must be at least 1")
    if n_envs == 1:
        return make_env(env_id=env_id)

    import os

    from stable_baselines3.common.vec_env import SubprocVecEnv

    start_method = "spawn" if os.name == "nt" else "forkserver"
    env_fns = [_make_env_fn(env_id=env_id, seed=seed, rank=rank) for rank in range(n_envs)]
    return SubprocVecEnv(env_fns, start_method=start_method)


def resolve_learning_starts(learning_starts: int | None, n_envs: int) -> int | None:
    if learning_starts is not None or n_envs == 1:
        return learning_starts
    return 10_000


class TimestepProgressCallback:
    def __init__(self, total_timesteps: int, log_interval_steps: int):
        from stable_baselines3.common.callbacks import BaseCallback

        class _Callback(BaseCallback):
            def __init__(self, total_timesteps: int, log_interval_steps: int):
                super().__init__()
                self.total_timesteps = total_timesteps
                self.log_interval_steps = log_interval_steps
                self.target_timesteps = total_timesteps
                self.last_logged_step = 0

            def _on_training_start(self) -> None:
                self.target_timesteps = self.num_timesteps + self.total_timesteps
                self.last_logged_step = self.num_timesteps

            def _on_step(self) -> bool:
                reached_interval = (
                    self.num_timesteps - self.last_logged_step >= self.log_interval_steps
                )
                reached_end = self.num_timesteps >= self.target_timesteps
                if reached_interval or reached_end:
                    print(
                        f"timesteps: {self.num_timesteps}/{self.target_timesteps}",
                        flush=True,
                    )
                    self.last_logged_step = self.num_timesteps
                return True

        self.callback = _Callback(total_timesteps, log_interval_steps)


def train_sac(
    env_id: str,
    total_timesteps: int,
    output_dir: Path,
    tensorboard_log: Path | None = None,
    seed: int = 42,
    progress_bar: bool = False,
    n_envs: int = 1,
    batch_size: int | None = None,
    buffer_size: int | None = None,
    gradient_steps: int | None = None,
    learning_starts: int | None = None,
    n_sampled_goal: int | None = None,
    log_interval_steps: int | None = None,
    checkpoint_interval: int | None = None,
    resume_from: Path | None = None,
):
    from stable_baselines3 import SAC
    from stable_baselines3.common.callbacks import CallbackList
    from stable_baselines3.her.her_replay_buffer import HerReplayBuffer

    env = make_training_env(env_id=env_id, seed=seed, n_envs=n_envs)
    overrides = {}
    if batch_size is not None:
        overrides["batch_size"] = batch_size
    if buffer_size is not None:
        overrides["buffer_size"] = buffer_size
    if gradient_steps is not None:
        overrides["gradient_steps"] = gradient_steps
    learning_starts = resolve_learning_starts(learning_starts=learning_starts, n_envs=n_envs)
    if learning_starts is not None:
        overrides["learning_starts"] = learning_starts

    config = create_model_config(
        "sac",
        replay_buffer_class=HerReplayBuffer,
        tensorboard_log=str(tensorboard_log) if tensorboard_log else None,
        **overrides,
    )
    if n_sampled_goal is not None:
        config.kwargs["replay_buffer_kwargs"]["n_sampled_goal"] = n_sampled_goal

    if resume_from is None:
        model = SAC("MultiInputPolicy", env, seed=seed, **config.kwargs)
    else:
        model = SAC.load(resume_from, env=env, seed=seed, **config.kwargs)
    callbacks: list[Any] = []
    if log_interval_steps is None and n_envs > 1:
        log_interval_steps = 10_000
    if log_interval_steps is not None:
        callbacks.append(
            TimestepProgressCallback(
                total_timesteps=total_timesteps,
                log_interval_steps=log_interval_steps,
            ).callback
        )
    output_dir.mkdir(parents=True, exist_ok=True)
    if checkpoint_interval is not None:
        from stable_baselines3.common.callbacks import CheckpointCallback

        checkpoint_prefix = f"{env_id.replace('-', '_')}_sac"
        callbacks.append(
            CheckpointCallback(
                save_freq=checkpoint_interval,
                save_path=str(output_dir),
                name_prefix=checkpoint_prefix,
            )
        )
    callback = CallbackList(callbacks) if callbacks else None
    model.learn(
        total_timesteps=total_timesteps,
        progress_bar=progress_bar,
        callback=callback,
        reset_num_timesteps=resume_from is None,
    )
    checkpoint_name = f"{env_id.replace('-', '_')}_sac.zip"
    checkpoint = output_dir / checkpoint_name
    model.save(checkpoint)
    env.close()
    return checkpoint


def evaluate_model(
    checkpoint: Path,
    env_id: str,
    episodes: int = 100,
):
    from stable_baselines3 import SAC

    env = make_env(env_id=env_id)
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
