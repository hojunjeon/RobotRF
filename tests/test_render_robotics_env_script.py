import subprocess
import sys


def test_render_robotics_env_script_writes_png(tmp_path):
    output = tmp_path / "fetch.png"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/render_robotics_env.py",
            "--env-id",
            "FetchPickAndPlace-v4",
            "--output",
            str(output),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert output.exists()
    assert output.read_bytes().startswith(b"\x89PNG")
    assert "saved snapshot:" in result.stdout
    assert "env_id: FetchPickAndPlace-v4" in result.stdout
