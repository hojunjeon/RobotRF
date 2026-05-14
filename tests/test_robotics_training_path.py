from robot_sorting_rl.training import make_env


def test_make_env_can_create_gymnasium_robotics_fetch_env():
    env = make_env(env_id="FetchPickAndPlace-v4", render_mode="rgb_array")
    try:
        observation, info = env.reset(seed=7)
        frame = env.render()
    finally:
        env.close()

    assert set(observation) == {"observation", "achieved_goal", "desired_goal"}
    assert frame.shape == (480, 480, 3)
    assert isinstance(info, dict)
