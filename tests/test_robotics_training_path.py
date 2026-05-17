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


def test_make_env_defaults_to_side_bin_place_env():
    env = make_env(render_mode="rgb_array")
    try:
        observation, _ = env.reset(seed=7)
        spec_id = env.spec.id
    finally:
        env.close()

    assert spec_id == "FetchSideBinPlace-v0"
    assert set(observation) == {"observation", "achieved_goal", "desired_goal"}
