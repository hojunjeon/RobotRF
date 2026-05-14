import inspect
from pathlib import Path

from robot_sorting_rl.training import resolve_learning_starts, train_sac


def test_train_sac_disables_progress_bar_by_default() -> None:
    signature = inspect.signature(train_sac)

    assert signature.parameters["progress_bar"].default is False


def test_train_sac_keeps_single_env_as_default_and_exposes_parallel_controls() -> None:
    signature = inspect.signature(train_sac)

    assert signature.parameters["n_envs"].default == 1
    assert signature.parameters["batch_size"].default is None
    assert signature.parameters["buffer_size"].default is None
    assert signature.parameters["gradient_steps"].default is None
    assert signature.parameters["learning_starts"].default is None
    assert signature.parameters["n_sampled_goal"].default is None
    assert signature.parameters["log_interval_steps"].default is None
    assert signature.parameters["checkpoint_interval"].default is None
    assert signature.parameters["resume_from"].default is None


def test_train_script_exposes_parallel_training_cli_flags() -> None:
    script = Path("scripts/train.py").read_text(encoding="utf-8")

    assert "--n-envs" in script
    assert "--batch-size" in script
    assert "--buffer-size" in script
    assert "--gradient-steps" in script
    assert "--learning-starts" in script
    assert "--n-sampled-goal" in script
    assert "--log-interval-steps" in script
    assert "--checkpoint-interval" in script
    assert "--resume-from" in script


def test_parallel_training_uses_safe_learning_starts_when_not_overridden() -> None:
    assert resolve_learning_starts(learning_starts=None, n_envs=1) is None
    assert resolve_learning_starts(learning_starts=None, n_envs=4) == 10_000
    assert resolve_learning_starts(learning_starts=512, n_envs=4) == 512
