from pathlib import Path


def test_check_runtime_uses_current_fetch_pick_and_place_version() -> None:
    script = Path("scripts/check_runtime.py").read_text(encoding="utf-8")

    assert "FetchPickAndPlace-v4" in script
    assert "FetchPickAndPlace-v3" not in script
