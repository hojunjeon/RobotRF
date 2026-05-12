from robot_sorting_rl.algorithms import create_model_config, supported_algorithms


def test_sac_uses_her_replay_buffer_by_default():
    config = create_model_config(algo="sac", learning_rate=0.0003)

    assert config.algorithm_name == "SAC"
    assert config.uses_her is True
    assert config.kwargs["learning_rate"] == 0.0003
    assert config.kwargs["replay_buffer_kwargs"]["n_sampled_goal"] == 4


def test_algorithm_registry_documents_extension_candidates():
    algorithms = supported_algorithms()

    assert algorithms["sac"].mvp_supported is True
    assert algorithms["td3"].mvp_supported is False
    assert algorithms["dqn"].continuous_action_compatible is False
