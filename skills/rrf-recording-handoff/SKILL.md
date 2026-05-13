---
name: rrf-recording-handoff
description: Use when meaningful Robot Sorting RL project work creates evidence for Notion, portfolio, README, interview notes, training logs, debugging notes, environment setup, GitHub pushes, diagrams, screenshots, videos, or milestone summaries.
---

# RRF Recording Handoff

Use this project-local skill to pass development evidence to the separate recording/portfolio agent. Write handoff entries in Korean by default. Do not draft the final Notion post unless the user explicitly asks.

## When To Append

Append to `docs/recording_handoff_log.md` after:

- project scope, architecture, environment, dependency, or runtime decisions
- simulation, GoalEnv, reward, curriculum, algorithm, training, or evaluation changes
- debugging with a clear cause and fix
- generated evidence such as checkpoints, TensorBoard/W&B logs, screenshots, videos, diagrams, README updates, GitHub pushes

Number each top-level entry sequentially so records are easy to reference. Use `001`, `002`, `003`, and continue from the highest existing number.

## Packet Format

Use this Korean structure:

```markdown
## NNN - YYYY-MM-DD KST - {작업 제목}

### 오늘 한 일
- 

### 막힌 문제
- 없음

### 해결 방법 / 결정
- 

### 남은 문제
- 

### 증거
- 코드 경로:
- 실행 명령:
- 결과 로그/지표:
- 스크린샷/영상:
- 체크포인트/학습 로그:
- 커밋:

### 기록 담당 에이전트에게 강조할 관점
- 채용 담당자:
- 기술 면접관:
- 개발자/학습자:

### 검증 상태
- 검증 완료:
- 검증 불가:
- 가정:
```

## Evidence Rules

- Write factual notes, not marketing copy.
- Include exact commands only if they were actually run.
- Include failed commands when the failure shaped the final decision.
- Put unverified claims under `가정` or `검증 불가`.
- For training/evaluation, include stage, algorithm, seed if known, timesteps, episodes, success rate, reward, checkpoint path, and log path.

## Portfolio Frame

Emphasize that the owner operated as PM / Agent Operator / RL experiment designer:

- environment design
- reward design
- curriculum design
- experiment verification
- AI tools as productivity and orchestration tools, not replacements

For final prose, use `docs/notion_blog_strategy.md` and `docs/notion_blog_template.md` only when drafting blog material is explicitly requested.
