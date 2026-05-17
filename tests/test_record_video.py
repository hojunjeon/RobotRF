from scripts.record_video import collect_rollout_frames


class FakeEnv:
    def __init__(self):
        self.step_count = 0
        self.rendered_steps = []

    def reset(self, seed=None):
        return "obs0", {}

    def step(self, action):
        self.step_count += 1
        done = self.step_count >= 2
        return f"obs{self.step_count}", 0.0, False, done, {}

    def render(self):
        self.rendered_steps.append(self.step_count)
        return f"frame{self.step_count}"


class FakeModel:
    def predict(self, obs, deterministic=True):
        return f"action_for_{obs}", None


def test_collect_rollout_frames_starts_after_first_environment_step():
    env = FakeEnv()

    frames = collect_rollout_frames(env=env, model=FakeModel(), max_steps=2, seed=42)

    assert frames == ["frame1", "frame2"]
    assert env.rendered_steps == [1, 2]


def test_collect_rollout_frames_can_delay_robot_motion_after_recording_starts():
    env = FakeEnv()

    frames = collect_rollout_frames(
        env=env,
        model=FakeModel(),
        max_steps=2,
        seed=42,
        start_delay_frames=2,
    )

    assert frames == ["frame0", "frame0", "frame1", "frame2"]
    assert env.rendered_steps == [0, 0, 1, 2]


def test_collect_rollout_frames_can_delay_recording_end_after_robot_motion_stops():
    env = FakeEnv()

    frames = collect_rollout_frames(
        env=env,
        model=FakeModel(),
        max_steps=2,
        seed=42,
        end_delay_frames=2,
    )

    assert frames == ["frame1", "frame2", "frame2", "frame2"]
    assert env.rendered_steps == [1, 2, 2, 2]
