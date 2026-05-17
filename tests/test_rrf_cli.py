from pathlib import Path


RRF_SCRIPT = Path("rrf")


def test_rrf_script_exposes_common_training_commands() -> None:
    script = RRF_SCRIPT.read_text(encoding="utf-8")

    assert "train-2m" in script
    assert "resume-3m" in script
    assert "eval" in script
    assert "video" in script
    assert "tensorboard" in script
    assert "status" in script


def test_rrf_resume_command_uses_safe_resume_defaults() -> None:
    script = RRF_SCRIPT.read_text(encoding="utf-8")

    assert "FetchSideBinPlace-v0" in script
    assert "--total-timesteps 3000000" in script
    assert "--checkpoint-interval 250000" in script
    assert "--learning-starts 510000" in script
    assert "BASE_OUT=\"checkpoints/side_bin_contact_safe_vec6_2m\"" in script
    assert "FetchSideBinPlace_v0_sac_500000_steps.zip" in script
    assert "checkpoints/side_bin_contact_safe_vec6_3p5m" in script
    assert "runs/side_bin_contact_safe_vec6_3p5m" in script


def test_readme_documents_short_rrf_commands() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "./rrf resume-3m" in readme
    assert "./rrf eval" in readme
    assert "./rrf video" in readme
    assert "./rrf tensorboard" in readme
