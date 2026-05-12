from __future__ import annotations

from dataclasses import dataclass

import gymnasium as gym
import numpy as np
from gymnasium import spaces


@dataclass(frozen=True)
class TabletopLayout:
    table_height: float = 0.42
    workspace_low_x: float = 1.15
    workspace_high_x: float = 1.55
    workspace_low_y: float = 0.45
    workspace_high_y: float = 1.05
    gripper_start_x: float = 1.34
    gripper_start_y: float = 0.75
    gripper_start_z: float = 0.58


class TabletopSortingEnv(gym.Env):
    """Fetch-style GoalEnv-compatible tabletop sorting environment.

    This is the project-local environment contract used for training scripts and tests.
    It follows the Gymnasium-Robotics multi-goal API shape and mirrors Fetch action
    semantics: dx, dy, dz, gripper open/close. The MVP keeps the table and target
    boxes deterministic while randomizing the object start position.
    """

    metadata = {"render_modes": ["rgb_array"], "render_fps": 25}

    def __init__(
        self,
        stage: int = 1,
        max_episode_steps: int = 50,
        success_threshold: float = 0.05,
        render_mode: str | None = None,
    ) -> None:
        if stage not in (1, 2):
            raise ValueError("stage must be 1 or 2")
        if render_mode not in (None, "rgb_array"):
            raise ValueError("only render_mode=None or 'rgb_array' is supported")

        self.stage = stage
        self.max_episode_steps = max_episode_steps
        self.success_threshold = success_threshold
        self.render_mode = render_mode
        self.layout = TabletopLayout()

        z = self.layout.table_height
        self.box_centers = np.array(
            [
                [1.25, 1.12, z],
                [1.35, 1.12, z],
                [1.45, 1.12, z],
            ],
            dtype=np.float32,
        )

        self.action_space = spaces.Box(-1.0, 1.0, shape=(4,), dtype=np.float32)
        self.observation_space = spaces.Dict(
            {
                "observation": spaces.Box(-np.inf, np.inf, shape=(13,), dtype=np.float32),
                "achieved_goal": spaces.Box(-np.inf, np.inf, shape=(3,), dtype=np.float32),
                "desired_goal": spaces.Box(-np.inf, np.inf, shape=(3,), dtype=np.float32),
            }
        )

        self.gripper_position = np.zeros(3, dtype=np.float32)
        self.object_position = np.zeros(3, dtype=np.float32)
        self.object_type = 0
        self.desired_goal = np.zeros(3, dtype=np.float32)
        self._held = False
        self._step_count = 0

    def reset(self, *, seed: int | None = None, options: dict | None = None):
        super().reset(seed=seed)
        options = options or {}
        self._step_count = 0
        self._held = False
        self.gripper_position = np.array(
            [
                self.layout.gripper_start_x,
                self.layout.gripper_start_y,
                self.layout.gripper_start_z,
            ],
            dtype=np.float32,
        )

        if "object_type" in options:
            self.object_type = int(options["object_type"])
        elif self.stage == 1:
            self.object_type = 0
        else:
            self.object_type = int(self.np_random.integers(0, 3))
        if not 0 <= self.object_type <= 2:
            raise ValueError("object_type must be 0, 1, or 2")

        object_xy = self.np_random.uniform(
            low=[self.layout.workspace_low_x, self.layout.workspace_low_y],
            high=[self.layout.workspace_high_x, self.layout.workspace_high_y],
        )
        self.object_position = np.array(
            [object_xy[0], object_xy[1], self.layout.table_height],
            dtype=np.float32,
        )
        target_index = 0 if self.stage == 1 else self.object_type
        self.desired_goal = self.box_centers[target_index].copy()
        return self._get_obs(), self._get_info()

    def step(self, action):
        action = np.asarray(action, dtype=np.float32)
        if action.shape != (4,):
            raise ValueError("action must have shape (4,)")

        self._step_count += 1
        delta = np.clip(action[:3], -1.0, 1.0) * 0.04
        self.gripper_position = self._clip_to_workspace(self.gripper_position + delta)

        distance_to_object = np.linalg.norm(self.gripper_position - self.object_position)
        gripper_closed = action[3] < 0.0
        if gripper_closed and distance_to_object <= 0.06:
            self._held = True
        if self._held:
            self.object_position = self.gripper_position.copy()
        if not gripper_closed:
            self._held = False
            self.object_position[2] = max(self.object_position[2], self.layout.table_height)

        obs = self._get_obs()
        info = self._get_info()
        reward = float(self.compute_reward(obs["achieved_goal"], obs["desired_goal"], info))
        terminated = bool(info["is_success"])
        truncated = self._step_count >= self.max_episode_steps and not terminated
        return obs, reward, terminated, truncated, info

    def compute_reward(self, achieved_goal, desired_goal, info):
        achieved = np.asarray(achieved_goal, dtype=np.float32)
        desired = np.asarray(desired_goal, dtype=np.float32)
        distances = np.linalg.norm(achieved - desired, axis=-1)
        return np.where(distances <= self.success_threshold, 0.0, -1.0).astype(np.float32)

    def render(self):
        image = np.full((480, 640, 3), 245, dtype=np.uint8)
        table_min = np.array([self.layout.workspace_low_x, self.layout.workspace_low_y])
        table_max = np.array([self.layout.workspace_high_x, 1.16])

        def project(point: np.ndarray) -> tuple[int, int]:
            xy = (point[:2] - table_min) / (table_max - table_min)
            x = int(np.clip(xy[0], 0.0, 1.0) * 560 + 40)
            y = int((1.0 - np.clip(xy[1], 0.0, 1.0)) * 400 + 40)
            return x, y

        image[40:440, 40:600] = np.array([210, 218, 214], dtype=np.uint8)
        colors = [(40, 120, 220), (40, 170, 90), (220, 120, 40)]
        for index, center in enumerate(self.box_centers):
            x, y = project(center)
            image[y - 18 : y + 18, x - 22 : x + 22] = np.array(colors[index], dtype=np.uint8)
        ox, oy = project(self.object_position)
        gx, gy = project(self.gripper_position)
        image[oy - 8 : oy + 8, ox - 8 : ox + 8] = np.array([30, 30, 30], dtype=np.uint8)
        image[gy - 6 : gy + 6, gx - 6 : gx + 6] = np.array([180, 30, 30], dtype=np.uint8)
        return image

    def _get_obs(self) -> dict[str, np.ndarray]:
        type_one_hot = np.zeros(3, dtype=np.float32)
        type_one_hot[self.object_type] = 1.0
        observation = np.concatenate(
            [
                self.gripper_position,
                self.object_position,
                self.desired_goal,
                type_one_hot,
                np.array([float(self._held)], dtype=np.float32),
            ]
        ).astype(np.float32)
        return {
            "observation": observation,
            "achieved_goal": self.object_position.astype(np.float32),
            "desired_goal": self.desired_goal.astype(np.float32),
        }

    def _get_info(self) -> dict:
        distance = float(np.linalg.norm(self.object_position - self.desired_goal))
        return {
            "is_success": distance <= self.success_threshold,
            "distance_to_goal": distance,
            "object_type": self.object_type,
            "stage": self.stage,
            "held": self._held,
        }

    def _clip_to_workspace(self, position: np.ndarray) -> np.ndarray:
        low = np.array(
            [self.layout.workspace_low_x, self.layout.workspace_low_y, self.layout.table_height],
            dtype=np.float32,
        )
        high = np.array(
            [self.layout.workspace_high_x, self.layout.workspace_high_y, 0.9],
            dtype=np.float32,
        )
        return np.clip(position, low, high).astype(np.float32)
