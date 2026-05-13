---
name: token-economy
description: Use when doing repository exploration, code review, debugging, long-running implementation, log/test analysis, context compaction handoff, or any task where coding agents should inspect less, compress tool output, answer briefly, and keep evidence.
---

# Token Economy

Default to ON. Use the smallest context that can still prove the answer, then turn this policy down only when the requested artifact needs fuller prose, raw evidence, or broad ideation.

## Default Mode

Keep token economy ON for normal agent work:

- repository exploration, code review, debugging, tests, logs, diffs, and build output
- long-running implementation, context handoff, compaction, and multi-agent work
- repeated shell commands, dependency output, generated output, and training/evaluation logs
- any task where speed, cost, or context-window pressure matters

Turn it OFF or relax it when the user asks for:

- detailed teaching, tutorials, mentoring, or step-by-step explanation
- blog posts, README prose, portfolio copy, specs, or stakeholder-facing documents
- brainstorming where breadth matters more than brevity
- full raw logs, complete files, exact transcripts, or uncompressed evidence
- high-risk legal, medical, financial, contract, or safety-sensitive analysis where omitted context could change the answer

If unsure, keep token economy ON for exploration and OFF for the final artifact only when the artifact needs richer prose.

## Operating Loop

1. Start with the user's goal, known files, and changed paths. Do not scan the whole repository unless the task requires architecture discovery.
2. Build a candidate context set before reading: entrypoints, directly changed files, imports/callers, tests, configs, and recent logs.
3. Read in slices. Prefer `rg`, `rg --files`, targeted `git diff`, `git status --short`, `git log --oneline -n`, and line-bounded file views over full dumps.
4. Compress every noisy command. Keep failures, changed paths, counts, metrics, and artifact paths. Drop progress bars, repeated warnings, dependency trees, generated code, and passing test chatter.
5. Maintain a short working note: goal, facts, assumptions, open questions, touched files, commands run, current risk.
6. Before context grows, checkpoint the working note and discard raw output that is no longer needed.
7. Final response: state outcome, changed paths, verification, and remaining risk. Avoid filler.

## Tool Output Rules

- Directory listing: show top-level shape and relevant matches only.
- Search: group by file; include line numbers and one-line matches.
- File read: read function/class boundaries or the nearest relevant block first; expand only on uncertainty.
- Diff: focus on semantic changes, not formatting noise.
- Test/build/log output: report failing cases first, then command, result count, and shortest useful traceback.
- Git commands: prefer concise status/log summaries; never paste full history unless requested.
- Web/docs: cite source links and summarize only the relevant claims.

## Code Review and Debugging

For reviews, approximate a local code graph even without graph tooling:

1. Identify changed symbols and files.
2. Trace imports, call sites, config wiring, and tests with targeted search.
3. Read only the blast radius plus contracts that could break.
4. Report uncertainty when graph coverage is incomplete.

For debugging:

1. Capture the exact failing command and minimal error.
2. Form one hypothesis at a time.
3. Inspect only files needed to confirm or reject it.
4. Keep raw logs out of context after extracting the cause.

## Response Style

- Be concise by default: no prefaces, no praise, no restating obvious context.
- Use fragments only when clarity survives.
- Keep code and command snippets exact.
- Expand explanations only for tradeoffs, non-obvious decisions, or user-requested teaching.
- Match the user's language.

## RRF Project Addendum

For this repository, preserve portfolio evidence while staying token-light:

- Record meaningful milestones in `docs/recording_handoff_log.md` using the project protocol.
- For RL/training work, keep metrics, command lines, seeds, checkpoints, screenshots/videos, and log paths. Do not paste full training logs.
- For environment work, record runtime decisions and blockers exactly.
- Treat unverified claims as assumptions.

## Optional References

- For the repository comparison and the "one skill vs four skills" decision, read `references/repo-comparison.md`.
- For cross-agent installation/adaptation notes, read `references/agent-portability.md`.
