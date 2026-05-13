---
name: rrf-project-ops
description: Use when working in the Robot Sorting RL repository on development, debugging, environment setup, dependency changes, tests, training scripts, evaluation, README updates, or final status reports.
---

# RRF Project Ops

Use this project-local skill after cloning the repository. It contains the operating rules that used to live directly in `AGENTS.md`.

## Defaults

- Write in Korean by default.
- Keep routine updates concise.
- Preserve commands, paths, metrics, logs, checkpoints, screenshots, videos, and commit hashes as evidence.
- Separate verified facts from assumptions.
- Do not exaggerate training, evaluation, or portfolio results that were not measured.
- Do not revert user or unrelated changes.

## Development Loop

1. Read the smallest relevant context first. Prefer `rg`, targeted file reads, `git status --short`, and narrow diffs.
2. If behavior changes, add or update a focused test before implementation when practical.
3. Run the command that proves the claim before reporting completion.
4. For environment work, record exact Python/WSL/package versions and the failing command when blocked.
5. For RL work, record stage, algorithm, seed, timesteps, checkpoint path, TensorBoard/W&B path, evaluation episodes, success rate, reward, and videos if generated.

## Current Local Execution Path

Prefer the Windows `.venv` smoke-test path unless the user explicitly asks for WSL-native training:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_windows_bootstrap.ps1
.\.venv\Scripts\python.exe scripts\check_runtime.py
.\.venv\Scripts\python.exe -m pytest
```

For smoke training:

```powershell
.\.venv\Scripts\python.exe scripts\train.py --stage 1 --algo sac --total-timesteps 1000 --output-dir checkpoints\smoke --tensorboard-log runs\smoke
.\.venv\Scripts\python.exe scripts\evaluate.py --stage 1 --checkpoint checkpoints\smoke\stage1_sac.zip --episodes 5
```

Treat smoke success as execution-path proof only, not model-quality proof.

## Style By Audience

- Recruiter-facing: short, outcome-oriented, evidence-backed.
- Robotics/AI interviewer-facing: technical decisions, tradeoffs, failure causes, validation method.
- Developer/job-seeker-facing: reproducible setup, commands, debugging notes, learning path.

## Related Skills

- Use `skills/token-economy/SKILL.md` for context control and concise reporting.
- Use `skills/rrf-recording-handoff/SKILL.md` after meaningful project work.
