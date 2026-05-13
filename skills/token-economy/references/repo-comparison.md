# Token-Saving Repository Comparison

Sources checked on 2026-05-13:

- RTK: https://github.com/rtk-ai/rtk
- Caveman: https://github.com/juliusbrussee/caveman
- Context Mode: https://github.com/mksglu/context-mode
- Code Review Graph: https://github.com/tirth8205/code-review-graph

## Distinct Ideas

| Repo | Core move | Best use | Main tradeoff |
| --- | --- | --- | --- |
| RTK | Proxy common CLI commands and return compact output | `git`, test, lint, search, logs, cloud/container commands | Requires tool/hook support; raw output may still be needed for rare edge cases |
| Caveman | Make agent replies and memory files terse | Daily agent conversation and persistent instruction files | Output-token saving only; too-terse style can hurt mentoring or stakeholder updates |
| Context Mode | Sandbox/reroute large tool output before it enters context | Long sessions, multi-agent tools, compaction, web/file reads | Needs platform-specific MCP/hooks; setup complexity |
| Code Review Graph | Build persistent AST/dependency graph and read only blast radius | Code review, monorepos, large codebases | Graph overhead is not worth it for tiny single-file changes |

## One Skill Each vs One Combined Skill

Create four separate skills when the team will install real tooling per category:

- `cli-output-compression`: RTK-style command wrappers.
- `terse-agent-output`: Caveman-style response policy.
- `context-routing`: Context Mode-style MCP/hook routing.
- `graph-guided-review`: Code Review Graph-style blast-radius reading.

This gives sharper triggers and less accidental overreach, but each agent has to decide among four policies and may load more metadata.

Create one combined skill when portability matters more than tool-specific automation. This is better here because the user wants the policy to apply across Codex, Claude Code, Hermes, Antigravity, and similar agents. A combined skill can use manual equivalents when hooks, MCP servers, or graph tools are unavailable:

- RTK becomes "compress shell output by default."
- Caveman becomes "answer tersely without losing technical exactness."
- Context Mode becomes "sandbox noisy output into summaries and checkpoints."
- Code Review Graph becomes "trace blast radius before reading files."

Recommendation: use one combined `token-economy` skill as the default. Split later only if a specific platform adopts RTK, Context Mode, or Code Review Graph as installed automation and needs dedicated setup/runbooks.

## Borrowed Principles

- Filter before reading: never load raw output that can be grouped, counted, or sliced.
- Keep failure evidence, not passing noise.
- Treat context as a budget shared by code, logs, memory, and final answer.
- Prefer persistent maps/checkpoints over rediscovering the same repository shape.
- Terse output is a correctness tool when it forces direct claims and removes hedging.
