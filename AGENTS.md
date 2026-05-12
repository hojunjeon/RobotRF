# Project Operating Instructions

## Notion Blog Policy

All meaningful project work should be recordable for a Notion blog. Treat the blog as a portfolio artifact for three audiences:

- company recruiters who need fast context, impact, and proof of completion
- robotics/AI interviewers who need technical decisions, tradeoffs, and evidence
- developer job seekers who need reusable setup steps, debugging notes, and learning path

Do not write a blog post after every small edit. Capture notes during work, then draft or update blog material at milestone boundaries:

- project scope or architecture changes
- environment setup and runtime decisions
- simulation environment changes
- RL algorithm or reward design changes
- debugging sessions with clear cause and fix
- training/evaluation runs with metrics
- portfolio deliverables such as videos, diagrams, README updates, and GitHub pushes

When writing blog material, use the structure and tone from `docs/notion_blog_strategy.md` and `docs/notion_blog_template.md`.

## Evidence Rules

- Prefer concrete commands, file paths, screenshots/videos, metrics, and commit hashes.
- Separate verified facts from assumptions.
- Record failures if they shaped the final design.
- For test or training claims, include the command and result.
- If verification could not run, state the environment blocker explicitly.

## Style

- Write in Korean by default.
- Keep recruiter-facing sections short and outcome-oriented.
- Keep interviewer-facing sections technically defensible.
- Keep job-seeker-facing sections procedural and reproducible.
- Avoid exaggerating results that were not measured.
