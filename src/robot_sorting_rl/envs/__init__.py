from __future__ import annotations

SIDE_BIN_ENV_ID = "FetchSideBinPlace-v0"


def register_custom_envs() -> None:
    import gymnasium as gym
    from gymnasium.envs.registration import registry

    if SIDE_BIN_ENV_ID in registry:
        return
    gym.register(
        id=SIDE_BIN_ENV_ID,
        entry_point="robot_sorting_rl.envs.side_bin_place:FetchSideBinPlaceEnv",
        max_episode_steps=100,
    )
