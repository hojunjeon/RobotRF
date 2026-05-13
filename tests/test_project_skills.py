from pathlib import Path


SKILLS = [
    Path("skills/rrf-project-ops/SKILL.md"),
    Path("skills/rrf-recording-handoff/SKILL.md"),
    Path("skills/token-economy/SKILL.md"),
]


def test_project_skills_are_clone_local_and_complete() -> None:
    for skill_path in SKILLS:
        text = skill_path.read_text(encoding="utf-8")

        assert text.startswith("---\nname: ")
        assert "description: Use when" in text
        assert "TODO" not in text


def test_agents_md_routes_to_skills_and_keeps_operating_rules() -> None:
    text = Path("AGENTS.md").read_text(encoding="utf-8")

    assert "skills/rrf-project-ops/SKILL.md" in text
    assert "skills/rrf-recording-handoff/SKILL.md" in text
    assert "skills/token-economy/SKILL.md" in text
    assert "## Coding Behavior" in text
    assert "Think Before Coding" in text
    assert "Simplicity First" in text
    assert "Surgical Changes" in text
    assert "Goal-Driven Execution" in text


def test_recording_handoff_entries_are_numbered() -> None:
    text = Path("docs/recording_handoff_log.md").read_text(encoding="utf-8", errors="replace")
    headings = [line for line in text.splitlines() if line.startswith("## ")]

    assert headings
    for index, heading in enumerate(headings, start=1):
        assert heading.startswith(f"## {index:03d} - ")


def test_recording_handoff_headings_have_readable_names() -> None:
    text = Path("docs/recording_handoff_log.md").read_text(encoding="utf-8", errors="replace")
    headings = [line for line in text.splitlines() if line.startswith("## ")]

    assert headings
    assert all("\ufffd" not in heading for heading in headings)
    assert all("\u5360" not in heading for heading in headings)


def test_recording_handoff_log_has_no_mojibake_markers() -> None:
    text = Path("docs/recording_handoff_log.md").read_text(encoding="utf-8", errors="replace")

    assert "\ufffd" not in text
    assert "\u5360" not in text


def test_recording_handoff_sections_use_korean_names() -> None:
    text = Path("docs/recording_handoff_log.md").read_text(encoding="utf-8", errors="replace")
    section_headings = [line for line in text.splitlines() if line.startswith("### ")]
    allowed = {
        "### 오늘 한 일",
        "### 막힌 문제",
        "### 해결 방법 / 결정",
        "### 남은 문제",
        "### 증거",
        "### 기록 담당 에이전트에게 강조할 관점",
        "### 검증 상태",
    }

    assert section_headings
    assert set(section_headings) <= allowed


def test_recording_handoff_skill_uses_korean_packet_headings() -> None:
    text = Path("skills/rrf-recording-handoff/SKILL.md").read_text(
        encoding="utf-8",
        errors="replace",
    )

    assert "\ufffd" not in text
    assert "\u5360" not in text
    assert "### 오늘 한 일" in text
    assert "### 막힌 문제" in text
    assert "### 검증 상태" in text
