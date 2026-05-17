from pathlib import Path


def test_check_runtime_uses_side_bin_place_default_env() -> None:
    script = Path("scripts/check_runtime.py").read_text(encoding="utf-8")

    assert "FetchSideBinPlace-v0" in script
    assert "FetchPickAndPlace-v3" not in script
