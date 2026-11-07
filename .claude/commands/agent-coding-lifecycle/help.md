---
description: Show goals, available lifecycle commands and recommended steps (read-only).
disable-model-invocation: true
---

# Agent Coding Lifecycle — Help

Goal: Make Codex and Claude Code development repeatable and traceable, with GitHub Issue, OpenSpec, architecture decisions (ADR), implementation/tests, and PR review.

| Command | Purpose |
|---|---|
| `/agent-coding-lifecycle:help` | Show commands and recommended flow |
| `/agent-coding-lifecycle:status` | Show Tracked task status (read-only) |
| `/agent-coding-lifecycle:quick` | Small local task; no mandatory Issue or PR |
| `/agent-coding-lifecycle:issue` | Manage a GitHub Issue |
| `/agent-coding-lifecycle:openspec` | Use the project's OpenSpec |
| `/agent-coding-lifecycle:adr` | Check or propose an ADR |
| `/agent-coding-lifecycle:implement` | Implement and test |
| `/agent-coding-lifecycle:pr` | Review/prepare PR |
| `/agent-coding-lifecycle:close` | Archive after merge |
| `/agent-coding-lifecycle:run` | Continue the next unfinished step |

**Tracked workflow (six steps):** `issue → openspec → adr → implement → pr → close` (merge must be verified before `close`).

**Quick:** invoke `quick` explicitly for small reversible changes, with real tests and no automatic remote changes.

**First-time use:** `help` for instructions, then `status` to inspect progress.

**Resume:** `status → run` requires a concrete Issue number and selects only the verified next step. `run` does not automatically authorize changes, merging, or deployment.

At `adr`, check existing Accepted ADRs every time architecture is affected; create a new Proposed ADR only for significant decisions. After approval, return to `openspec` if Design / Tasks need updates.

Only significant architecture choices need a new ADR, and human approval is required before treating one as Accepted. This help command must not read or modify the repository, invoke external tools, or start coding.
