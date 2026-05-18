import numpy as np
import gymnasium as gym

from robot_sorting_rl.envs import register_custom_envs
from robot_sorting_rl.training import make_env


def _set_object_position(env, position: np.ndarray) -> None:
    unwrapped = env.unwrapped
    object_qpos = unwrapped._utils.get_joint_qpos(
        unwrapped.model,
        unwrapped.data,
        "object0:joint",
    )
    object_qpos[:3] = position
    unwrapped._utils.set_joint_qpos(
        unwrapped.model,
        unwrapped.data,
        "object0:joint",
        object_qpos,
    )
    unwrapped._mujoco.mj_forward(unwrapped.model, unwrapped.data)


def test_make_env_can_create_side_bin_place_env():
    env = make_env(env_id="FetchSideBinPlace-v0", render_mode="rgb_array")
    try:
        observation, info = env.reset(seed=7)
        frame = env.render()
    finally:
        env.close()

    assert set(observation) == {"observation", "achieved_goal", "desired_goal"}
    assert frame.shape == (480, 480, 3)
    assert isinstance(info, dict)


def test_side_bin_place_env_registers_with_gymnasium():
    register_custom_envs()
    env = gym.make("FetchSideBinPlace-v0", render_mode="rgb_array")
    try:
        observation, _ = env.reset(seed=7)
    finally:
        env.close()

    assert set(observation) == {"observation", "achieved_goal", "desired_goal"}


def test_side_bin_success_requires_object_to_stay_inside_bin():
    env = make_env(env_id="FetchSideBinPlace-v0")
    try:
        env.reset(seed=7)
        bin_center = env.unwrapped.bin_center.copy()
        object_position = bin_center.copy()
        object_position[2] = env.unwrapped.bin_floor_z + 0.04

        info = {}
        for _ in range(env.unwrapped.success_hold_steps):
            _set_object_position(env, object_position)
            _, _, _, _, info = env.step(np.zeros(env.action_space.shape))
    finally:
        env.close()

    assert info["is_success"] == 1.0


def test_side_bin_success_fails_outside_bin():
    env = make_env(env_id="FetchSideBinPlace-v0")
    try:
        env.reset(seed=7)
        object_position = env.unwrapped.bin_center.copy()
        object_position[1] = env.unwrapped.bin_inner_max[1] + 0.10
        object_position[2] = env.unwrapped.bin_floor_z + 0.04

        info = {}
        for _ in range(env.unwrapped.success_hold_steps):
            _set_object_position(env, object_position)
            _, _, _, _, info = env.step(np.zeros(env.action_space.shape))
    finally:
        env.close()

    assert info["is_success"] == 0.0


def test_side_bin_success_requires_object_clearance_from_walls_and_floor():
    env = make_env(env_id="FetchSideBinPlace-v0")
    try:
        env.reset(seed=7)
        unwrapped = env.unwrapped

        wall_overlap_position = unwrapped.bin_center.copy()
        wall_overlap_position[1] = unwrapped.bin_wall_inner_min[1]
        wall_overlap_position[2] = unwrapped.bin_floor_z + unwrapped.object_half_size

        floor_overlap_position = unwrapped.bin_center.copy()
        floor_overlap_position[2] = unwrapped.bin_floor_z

        clear_position = unwrapped.bin_center.copy()
        clear_position[2] = unwrapped.bin_floor_z + unwrapped.object_half_size
    finally:
        env.close()

    assert not unwrapped._is_inside_physical_bin(wall_overlap_position)
    assert not unwrapped._is_inside_physical_bin(floor_overlap_position)
    assert unwrapped._is_inside_physical_bin(clear_position)


def test_side_bin_uses_smaller_action_scale_near_bin():
    env = make_env(env_id="FetchSideBinPlace-v0")
    try:
        assert env.unwrapped.action_position_scale == 0.02
    finally:
        env.close()


def test_side_bin_can_identify_wall_contact_from_geom_names():
    env = make_env(env_id="FetchSideBinPlace-v0")
    try:
        unwrapped = env.unwrapped
        assert unwrapped._is_wall_contact_pair("object0", "side_bin_front_wall")
        assert unwrapped._is_wall_contact_pair(
            "robot0:l_gripper_finger_link",
            "side_bin_back_wall",
        )
        assert not unwrapped._is_wall_contact_pair("object0", "table0")
    finally:
        env.close()


def test_side_bin_wall_contact_keeps_sparse_reward_negative():
    env = make_env(env_id="FetchSideBinPlace-v0")
    try:
        assert env.unwrapped._apply_wall_contact_reward(np.float32(0.0), True) == -1.0
        assert env.unwrapped._apply_wall_contact_reward(np.float32(0.0), False) == 0.0
    finally:
        env.close()


def test_side_bin_shaped_reward_rewards_object_progress_toward_bin():
    env = make_env(env_id="FetchSideBinPlace-v0", reward_type="shaped")
    try:
        unwrapped = env.unwrapped
        start = np.array([1.30, 0.70, unwrapped.object_table_z])
        near_bin = np.array([1.30, 0.90, unwrapped.object_table_z + 0.04])
        in_bin = unwrapped.bin_center.copy()
        in_bin[2] = unwrapped.bin_floor_z + 0.04

        start_reward = unwrapped.compute_reward(start, unwrapped.bin_center, {})
        near_reward = unwrapped.compute_reward(near_bin, unwrapped.bin_center, {})
        success_reward = unwrapped.compute_reward(in_bin, unwrapped.bin_center, {})
    finally:
        env.close()

    assert near_reward > start_reward
    assert success_reward > near_reward


def test_side_bin_step_shaped_reward_guides_gripper_to_object():
    env = make_env(env_id="FetchSideBinPlace-v0", reward_type="shaped")
    try:
        unwrapped = env.unwrapped
        object_position = np.array([1.30, 0.70, unwrapped.object_table_z])
        far_gripper = np.array([1.30, 1.00, unwrapped.object_table_z + 0.20])
        near_gripper = object_position + np.array([0.0, 0.0, 0.03])

        far_reward = unwrapped._compute_shaped_reward(
            achieved_goal=object_position,
            desired_goal=unwrapped.bin_center,
            gripper_position=far_gripper,
            wall_contact=False,
        )
        near_reward = unwrapped._compute_shaped_reward(
            achieved_goal=object_position,
            desired_goal=unwrapped.bin_center,
            gripper_position=near_gripper,
            wall_contact=False,
        )
    finally:
        env.close()

    assert near_reward > far_reward
