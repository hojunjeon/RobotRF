# Project Operating Instructions

This file is only a router. Keep it short so cloned agents load detailed rules from project-local skills.

## Always Consider

- `skills/rrf-project-ops/SKILL.md`: development, debugging, tests, environment setup, training/evaluation, README/status work.
- `skills/token-economy/SKILL.md`: default context economy for exploration, diffs, logs, reviews, handoffs, and final reporting.
- `skills/rrf-recording-handoff/SKILL.md`: append evidence for the separate Notion/portfolio recording agent after meaningful work.

## Defaults

- Korean by default.
- Evidence before claims.
- Do not inflate unmeasured training or portfolio results.

## Coding Behavior — Always Apply

Derived from [Karpathy's LLM coding guidelines](https://x.com/karpathy/status/2015883857489522876). Apply to all code writing, review, and refactoring — no exceptions.

**1. Think Before Coding**
- State assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If something is unclear, stop. Name what's confusing. Ask.

**2. Simplicity First**
- Minimum code that solves the problem. Nothing speculative.
- No features beyond what was asked. No abstractions for single-use code.
- If you write 200 lines and it could be 50, rewrite it.

**3. Surgical Changes**
- Touch only what you must. Don't "improve" adjacent code or formatting.
- Match existing style, even if you'd do it differently.
- Every changed line must trace directly to the user's request.
- If YOUR changes create unused imports/variables/functions, remove them. Don't touch pre-existing dead code unless asked.

**4. Goal-Driven Execution**
- Transform tasks into verifiable goals before starting.
  - "Fix the bug" → "Write a test that reproduces it, then make it pass"
  - "Refactor X" → "Ensure tests pass before and after"
- For multi-step tasks, state a brief plan with verification steps.
