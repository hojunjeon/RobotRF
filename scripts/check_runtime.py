from __future__ import annotations


def main() -> None:
    import gymnasium as gym
    import gymnasium_robotics
    import mujoco
    import torch

    from robot_sorting_rl.envs import SIDE_BIN_ENV_ID, register_custom_envs

    expected_env_id = "FetchSideBinPlace-v0"
    assert SIDE_BIN_ENV_ID == expected_env_id

    gym.register_envs(gymnasium_robotics)
    register_custom_envs()
    env = gym.make(SIDE_BIN_ENV_ID, render_mode="rgb_array")
    obs, info = env.reset(seed=42)
    frame = env.render()
    env.close()

    print(f"torch: {torch.__version__}")
    print(f"cuda_available: {torch.cuda.is_available()}")
    print(f"mujoco: {mujoco.__version__}")
    print(f"env_id: {SIDE_BIN_ENV_ID}")
    print(f"observation_keys: {sorted(obs.keys())}")
    print(f"info_keys: {sorted(info.keys())}")
    print(f"render_shape: {frame.shape}")


if __name__ == "__main__":
    main()
