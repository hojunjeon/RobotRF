# Agent Portability Notes

Use this skill as a portable policy document. If a platform supports native skills, install `SKILL.md` as a skill. If not, copy the core rules into that platform's persistent instruction file.

## Codex

- Project scope: keep this folder under `skills/token-economy/` and reference it from `AGENTS.md` if automatic discovery is unavailable.
- Global scope: copy to `$CODEX_HOME/skills/token-economy/` when filesystem permissions allow.
- Prefer `rg`, targeted shell commands, and concise final answers.

## Claude Code

- Install as a skill folder or copy the operating loop into `CLAUDE.md`.
- If RTK or Context Mode is installed, prefer their compact wrappers for shell/tool output.
- Built-in file tools may bypass shell hooks, so still read files selectively.

## Gemini, Copilot, Cursor, Hermes, Antigravity, OpenCode

- Use the same policy in the platform's persistent instruction file: `GEMINI.md`, repository agent rules, plugin instructions, or equivalent.
- When hooks/MCP are available, route large file reads, shell output, web fetches, and test logs through compression tools.
- When hooks/MCP are unavailable, manually summarize command output before continuing.

## Universal Guardrails

- Do not hide uncertainty to save tokens.
- Do not omit commands, file paths, metrics, or sources that are needed as evidence.
- Do not use terse style for user-facing docs, blog drafts, or teaching material when the requested artifact needs prose.
- Do not compress secrets into summaries; redact them.
