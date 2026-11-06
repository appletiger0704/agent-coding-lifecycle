---
description: Show goals, available lifecycle commands and recommended steps (read-only).
---

# Agent Coding Lifecycle — Help

Goal: Make Codex and Claude Code development repeatable and traceable, with GitHub Issue, OpenSpec, architecture decisions (ADR), implementation/tests, and PR review.

| Command | Purpose |
|---|---|
| `/agent-coding-lifecycle:help` | Show commands and recommended flow |
| `/agent-coding-lifecycle:status` | Show the current stage (read-only) |
| `/agent-coding-lifecycle:issue` | Manage a GitHub Issue |
| `/agent-coding-lifecycle:openspec` | Use the project's OpenSpec |
| `/agent-coding-lifecycle:adr` | Check or propose an ADR |
| `/agent-coding-lifecycle:implement` | Implement and test |
| `/agent-coding-lifecycle:pr` | Review/prepare PR |
| `/agent-coding-lifecycle:close` | Archive after merge |
| `/agent-coding-lifecycle:run` | Continue the next unfinished step |

Suggested flow: **Issue → OpenSpec → ADR decision gate (only when needed) → Code + Tests → PR → Merge → Archive**.

Only significant architecture choices need a new ADR, and human approval is required before treating one as Accepted. This help command must not read or modify the repository, invoke external tools, or start coding.
