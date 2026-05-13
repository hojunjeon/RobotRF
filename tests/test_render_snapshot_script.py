import subprocess
import sys


def test_render_snapshot_script_writes_png(tmp_path):
    output = tmp_path / "stage1.png"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/render_snapshot.py",
            "--stage",
            "1",
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
    assert "stage: 1" in result.stdout
