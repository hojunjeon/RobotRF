from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AlgorithmSpec:
    key: str
    display_name: str
    mvp_supported: bool
    continuous_action_compatible: bool
    her_compatible: bool
    note: str


@dataclass(frozen=True)
class ModelConfig:
    algorithm_name: str
    uses_her: bool
    kwargs: dict[str, Any]


def supported_algorithms() -> dict[str, AlgorithmSpec]:
    return {
        "sac": AlgorithmSpec(
            key="sac",
            display_name="SAC + HER",
            mvp_supported=True,
            continuous_action_compatible=True,
            her_compatible=True,
            note="MVP default for Fetch-style continuous control.",
        ),
        "td3": AlgorithmSpec(
            key="td3",
            display_name="TD3 + HER",
            mvp_supported=False,
            continuous_action_compatible=True,
            her_compatible=True,
            note="Good off-policy comparison candidate after SAC is stable.",
        ),
        "tqc": AlgorithmSpec(
            key="tqc",
            display_name="TQC + HER",
            mvp_supported=False,
            continuous_action_compatible=True,
            her_compatible=True,
            note="SB3-Contrib candidate with stronger performance and extra dependency.",
        ),
        "ddpg": AlgorithmSpec(
            key="ddpg",
            display_name="DDPG + HER",
            mvp_supported=False,
            continuous_action_compatible=True,
            her_compatible=True,
            note="Classic baseline; more tuning-sensitive than SAC or TD3.",
        ),
        "ppo": AlgorithmSpec(
            key="ppo",
            display_name="PPO baseline",
            mvp_supported=False,
            continuous_action_compatible=True,
            her_compatible=False,
            note="On-policy baseline; useful to explain HER/off-policy tradeoffs.",
        ),
        "dqn": AlgorithmSpec(
            key="dqn",
            display_name="DQN / QR-DQN",
            mvp_supported=False,
            continuous_action_compatible=False,
            her_compatible=False,
            note="Discrete-action experiment only; not a direct fit for Fetch action space.",
        ),
    }


def create_model_config(algo: str, **overrides: Any) -> ModelConfig:
    specs = supported_algorithms()
    key = algo.lower()
    if key not in specs:
        raise ValueError(f"unsupported algorithm '{algo}'. Choose one of: {', '.join(specs)}")
    if key != "sac":
        raise ValueError("MVP implementation supports training only with 'sac'")

    kwargs: dict[str, Any] = {
        "learning_rate": 3e-4,
        "buffer_size": 100_000,
        "batch_size": 256,
        "gamma": 0.95,
        "tau": 0.05,
        "replay_buffer_kwargs": {
            "n_sampled_goal": 4,
            "goal_selection_strategy": "future",
        },
        "verbose": 1,
    }
    kwargs.update(overrides)
    return ModelConfig(algorithm_name="SAC", uses_her=True, kwargs=kwargs)
