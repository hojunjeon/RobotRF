import numpy as np

from robot_sorting_rl.envs import TabletopSortingEnv


def test_stage1_reset_returns_goal_env_observation():
    env = TabletopSortingEnv(stage=1)

    observation, info = env.reset(seed=7)

    assert set(observation) == {"observation", "achieved_goal", "desired_goal"}
    assert observation["observation"].shape == (13,)
    assert observation["achieved_goal"].shape == (3,)
    assert observation["desired_goal"].shape == (3,)
    assert info["stage"] == 1
    assert info["object_type"] == 0


def test_stage2_uses_object_type_to_select_target_box():
    env = TabletopSortingEnv(stage=2)

    observation, info = env.reset(seed=3, options={"object_type": 2})

    assert info["object_type"] == 2
    np.testing.assert_allclose(
        observation["desired_goal"],
        env.box_centers[2],
        atol=1e-6,
    )


def test_sparse_reward_is_vectorized_and_success_threshold_based():
    env = TabletopSortingEnv(stage=2, success_threshold=0.05)
    desired = np.array([[1.0, 0.0, 0.45], [1.0, 0.0, 0.45]], dtype=np.float32)
    achieved = np.array([[1.01, 0.0, 0.45], [1.2, 0.0, 0.45]], dtype=np.float32)

    rewards = env.compute_reward(achieved, desired, {})

    np.testing.assert_array_equal(rewards, np.array([0.0, -1.0], dtype=np.float32))


def test_step_reports_success_when_object_reaches_desired_goal():
    env = TabletopSortingEnv(stage=1, success_threshold=0.05)
    observation, _ = env.reset(seed=11)
    env.object_position = observation["desired_goal"].copy()

    observation, reward, terminated, truncated, info = env.step(np.zeros(4, dtype=np.float32))

    assert reward == 0.0
    assert terminated is True
    assert truncated is False
    assert info["is_success"] is True
    np.testing.assert_allclose(observation["achieved_goal"], observation["desired_goal"])
