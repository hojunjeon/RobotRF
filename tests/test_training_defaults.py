import inspect
from pathlib import Path

from robot_sorting_rl.training import (
    resolve_learning_starts,
    resolve_next_checkpoint_timestep,
    train_sac,
)


def test_train_sac_disables_progress_bar_by_default() -> None:
    signature = inspect.signature(train_sac)

    assert signature.parameters["progress_bar"].default is False


def test_train_sac_keeps_single_env_as_default_and_exposes_parallel_controls() -> None:
    signature = inspect.signature(train_sac)

    assert signature.parameters["n_envs"].default == 1
    assert signature.parameters["reward_type"].default == "shaped"
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

    assert "FetchSideBinPlace-v0" in script
    assert "--reward-type" in script
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


def test_checkpoint_schedule_uses_real_timesteps() -> None:
    assert (
        resolve_next_checkpoint_timestep(current_timesteps=0, checkpoint_interval=250_000)
        == 250_000
    )
    assert (
        resolve_next_checkpoint_timestep(
            current_timesteps=250_002,
            checkpoint_interval=250_000,
        )
        == 500_000
    )
    assert (
        resolve_next_checkpoint_timestep(
            current_timesteps=2_000_000,
            checkpoint_interval=250_000,
        )
        == 2_250_000
    )
