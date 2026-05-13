import inspect

from robot_sorting_rl.training import train_sac


def test_train_sac_disables_progress_bar_by_default() -> None:
    signature = inspect.signature(train_sac)

    assert signature.parameters["progress_bar"].default is False
