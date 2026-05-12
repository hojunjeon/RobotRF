from __future__ import annotations


def main() -> None:
    import gymnasium as gym
    import gymnasium_robotics
    import mujoco
    import torch

    gym.register_envs(gymnasium_robotics)
    env = gym.make("FetchPickAndPlace-v3", render_mode="rgb_array")
    obs, info = env.reset(seed=42)
    frame = env.render()
    env.close()

    print(f"torch: {torch.__version__}")
    print(f"cuda_available: {torch.cuda.is_available()}")
    print(f"mujoco: {mujoco.__version__}")
    print(f"fetch_observation_keys: {sorted(obs.keys())}")
    print(f"fetch_info_keys: {sorted(info.keys())}")
    print(f"render_shape: {frame.shape}")


if __name__ == "__main__":
    main()
