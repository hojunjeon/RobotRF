from __future__ import annotations

import tempfile
from importlib import resources
from pathlib import Path

import numpy as np
from gymnasium.utils.ezpickle import EzPickle
from gymnasium_robotics.envs.fetch import MujocoFetchEnv


class FetchSideBinPlaceEnv(MujocoFetchEnv, EzPickle):
    """Fetch task where the block must be placed into a physical side bin."""

    side_bin_wall_geoms = frozenset(
        {
            "side_bin_left_wall",
            "side_bin_right_wall",
            "side_bin_front_wall",
            "side_bin_back_wall",
        }
    )
    wall_contact_geoms = frozenset(
        {
            "object0",
            "robot0:l_gripper_finger_link",
            "robot0:r_gripper_finger_link",
        }
    )

    def __init__(
        self,
        reward_type: str = "sparse",
        success_hold_steps: int = 5,
        **kwargs,
    ):
        self.object_half_size = 0.025
        self.bin_floor_z = 0.410
        self.bin_wall_top_z = 0.570
        self.bin_wall_inner_min = np.array([1.215, 0.915], dtype=np.float64)
        self.bin_wall_inner_max = np.array([1.385, 1.085], dtype=np.float64)
        self.bin_inner_min = np.array(
            [
                self.bin_wall_inner_min[0] + self.object_half_size,
                self.bin_wall_inner_min[1] + self.object_half_size,
                self.bin_floor_z + self.object_half_size,
            ],
            dtype=np.float64,
        )
        self.bin_inner_max = np.array(
            [
                self.bin_wall_inner_max[0] - self.object_half_size,
                self.bin_wall_inner_max[1] - self.object_half_size,
                self.bin_wall_top_z - self.object_half_size,
            ],
            dtype=np.float64,
        )
        self.bin_center = np.array([1.30, 1.00, self.bin_inner_min[2]], dtype=np.float64)
        self.goal_tolerance = np.array([0.06, 0.06, 0.03], dtype=np.float64)
        self.object_start_xy = np.array([1.30, 0.70], dtype=np.float64)
        self.object_start_noise = 0.015
        self.action_position_scale = 0.02
        self.success_hold_steps = success_hold_steps
        self._success_streak = 0

        initial_qpos = {
            "robot0:slide0": 0.405,
            "robot0:slide1": 0.48,
            "robot0:slide2": 0.0,
            "object0:joint": [1.30, 0.70, 0.4, 1.0, 0.0, 0.0, 0.0],
        }
        MujocoFetchEnv.__init__(
            self,
            model_path=_resolved_model_path(),
            has_object=True,
            block_gripper=False,
            n_substeps=20,
            gripper_extra_height=0.2,
            target_in_the_air=False,
            target_offset=0.0,
            obj_range=self.object_start_noise,
            target_range=0.0,
            distance_threshold=0.05,
            initial_qpos=initial_qpos,
            reward_type=reward_type,
            **kwargs,
        )
        EzPickle.__init__(
            self,
            reward_type=reward_type,
            success_hold_steps=success_hold_steps,
            **kwargs,
        )

    def _sample_goal(self):
        return self.bin_center.copy()

    def _reset_sim(self):
        self._success_streak = 0
        self._mujoco.mj_resetData(self.model, self.data)
        self.data.time = self.initial_time
        self.data.qpos[:] = np.copy(self.initial_qpos)
        self.data.qvel[:] = np.copy(self.initial_qvel)
        if self.model.na != 0:
            self.data.act[:] = None

        object_xy = self.object_start_xy + self.np_random.uniform(
            -self.object_start_noise,
            self.object_start_noise,
            size=2,
        )
        object_qpos = self._utils.get_joint_qpos(
            self.model,
            self.data,
            "object0:joint",
        )
        object_qpos[:2] = object_xy
        self._utils.set_joint_qpos(
            self.model,
            self.data,
            "object0:joint",
            object_qpos,
        )

        self._mujoco.mj_forward(self.model, self.data)
        return True

    def compute_reward(self, achieved_goal, goal, info):
        if self.reward_type == "dense":
            return -np.linalg.norm(achieved_goal - goal, axis=-1)
        success = self._within_bin_clearance(achieved_goal)
        return -(~success).astype(np.float32)

    def step(self, action):
        obs, reward, terminated, truncated, info = super().step(action)
        wall_contact = self._has_wall_contact()
        info["is_wall_contact"] = wall_contact
        if wall_contact:
            info["is_success"] = np.float32(0.0)
            reward = self._apply_wall_contact_reward(reward, wall_contact)
            self._success_streak = 0
        return obs, reward, terminated, truncated, info

    def _is_success(self, achieved_goal, desired_goal):
        in_bin = self._is_inside_physical_bin(achieved_goal) and not self._has_wall_contact()
        if in_bin:
            self._success_streak += 1
        else:
            self._success_streak = 0
        return np.float32(self._success_streak >= self.success_hold_steps)

    def _set_action(self, action):
        assert action.shape == (4,)
        action = action.copy()
        pos_ctrl, gripper_ctrl = action[:3], action[3]
        pos_ctrl *= self.action_position_scale
        rot_ctrl = [1.0, 0.0, 1.0, 0.0]
        gripper_ctrl = np.array([gripper_ctrl, gripper_ctrl])
        if self.block_gripper:
            gripper_ctrl = np.zeros_like(gripper_ctrl)
        action = np.concatenate([pos_ctrl, rot_ctrl, gripper_ctrl])

        self._utils.ctrl_set_action(self.model, self.data, action)
        self._utils.mocap_set_action(self.model, self.data, action)

    def _is_inside_physical_bin(self, achieved_goal) -> bool:
        return bool(self._within_bin_clearance(achieved_goal))

    def _within_bin_clearance(self, achieved_goal):
        achieved_goal = np.asarray(achieved_goal)
        return np.all(
            (achieved_goal >= self.bin_inner_min) & (achieved_goal <= self.bin_inner_max),
            axis=-1,
        )

    def _has_wall_contact(self) -> bool:
        for index in range(self.data.ncon):
            contact = self.data.contact[index]
            geom1 = self._geom_name(contact.geom1)
            geom2 = self._geom_name(contact.geom2)
            if self._is_wall_contact_pair(geom1, geom2):
                return True
        return False

    def _geom_name(self, geom_id: int) -> str:
        name = self._mujoco.mj_id2name(
            self.model,
            self._mujoco.mjtObj.mjOBJ_GEOM,
            geom_id,
        )
        return "" if name is None else name

    def _is_wall_contact_pair(self, geom1: str, geom2: str) -> bool:
        pair = {geom1, geom2}
        return bool(pair & self.side_bin_wall_geoms and pair & self.wall_contact_geoms)

    def _apply_wall_contact_reward(self, reward, wall_contact: bool):
        if not wall_contact:
            return reward
        if self.reward_type == "dense":
            return reward - 1.0
        return np.float32(-1.0)

    def _within_goal_box(self, achieved_goal, goal):
        achieved_goal = np.asarray(achieved_goal)
        goal = np.asarray(goal)
        return np.all(np.abs(achieved_goal - goal) <= self.goal_tolerance, axis=-1)


def _resolved_model_path() -> str:
    template = resources.files("robot_sorting_rl").joinpath(
        "assets",
        "fetch",
        "side_bin_place.xml",
    )
    import gymnasium_robotics.envs as robotics_envs

    robotics_assets = Path(robotics_envs.__file__).parent / "assets"
    fetch_assets = robotics_assets / "fetch"
    xml = template.read_text(encoding="utf-8")
    replacements = {
        "__FETCH_STL_DIR__": (robotics_assets / "stls" / "fetch").as_posix(),
        "__FETCH_TEXTURE_DIR__": (robotics_assets / "textures").as_posix(),
        "__FETCH_SHARED_XML__": (fetch_assets / "shared.xml").as_posix(),
        "__FETCH_ROBOT_XML__": (fetch_assets / "robot.xml").as_posix(),
    }
    for old, new in replacements.items():
        xml = xml.replace(old, new)

    output = Path(tempfile.gettempdir()) / "robot_sorting_rl_side_bin_place.xml"
    output.write_text(xml, encoding="utf-8")
    if output.is_relative_to(robotics_assets):
        return str(output.relative_to(robotics_assets))
    return str(_relpath(output, robotics_assets))


def _relpath(path: Path, start: Path) -> Path:
    import os

    return Path(os.path.relpath(path, start=start))
