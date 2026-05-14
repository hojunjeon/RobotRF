import json
from pathlib import Path

from scripts.evaluate import append_evaluation_result


def test_append_evaluation_result_creates_json_array_and_appends_entries(tmp_path: Path) -> None:
    output = tmp_path / "evals" / "results.json"

    append_evaluation_result(
        output,
        {
            "env_id": "FetchPickAndPlace-v4",
            "checkpoint": "checkpoints/a.zip",
            "episodes": 100,
            "success_rate": 0.1,
        },
    )
    append_evaluation_result(
        output,
        {
            "env_id": "FetchPickAndPlace-v4",
            "checkpoint": "checkpoints/b.zip",
            "episodes": 100,
            "success_rate": 0.2,
        },
    )

    saved = json.loads(output.read_text(encoding="utf-8"))

    assert len(saved) == 2
    assert saved[0]["checkpoint"] == "checkpoints/a.zip"
    assert saved[1]["success_rate"] == 0.2


def test_evaluate_script_exposes_output_flag() -> None:
    script = Path("scripts/evaluate.py").read_text(encoding="utf-8")

    assert "--output" in script
