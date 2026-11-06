---
name: agent-coding-lifecycle
description: "Use when explicitly invoked to coordinate a GitHub Issue → OpenSpec → ADR → PR workflow or a cross-agent handoff. 中文：接續 Issue、開發生命週期、OpenSpec 規格、ADR 架構決策、交接開發。 Do not auto-trigger for ordinary coding, trivial fixes, or general questions."
---

# Agent Coding Lifecycle — MVP Command Router

Coordinate existing tools; do not replace GitHub, OpenSpec, ADR skills, tests, or human reviewers.

## Invocation

- Codex: `$agent-coding-lifecycle <command> [details]`
- Claude Code: `/agent-coding-lifecycle <command> [details]`
- Claude wrappers (separate install): `/agent-coding-lifecycle:<command> [details]`
- Commands: `help`, `status`, `issue`, `openspec`, `adr`, `implement`, `pr`, `close`, `run`.
- Unknown command → `help`; omitted command → `run`.

## Routing gate — BEFORE any workflow

1. `help`: display purpose, commands, and `issue → openspec → adr → implement → pr → close`. **No repository scan, no tools.**
2. `status`: discovery only. **No file or remote writes.**
3. Explicit stage command: execute **only that stage** and its necessary safety checks; do not run all stages.
4. `run`: inspect progress, then handle **only the next unfinished stage**. Never auto-merge or deploy.
5. No Git repository: do not claim successful discovery; for `issue`, drafting from supplied text is allowed, but report missing repo access.
6. Routine fix using established patterns: skip creating OpenSpec changes and ADRs unless user/project policy requires them.
7. No `openspec/` or OpenSpec tooling: skip the **implicit** OpenSpec step. If `openspec` was explicitly requested, explain setup needed; never pretend it ran.
8. No existing ADR directory: skip searching absent ADRs. **Still propose** an ADR when a genuinely significant new architecture decision arises.

**Spec trigger:** new/changed externally observable behavior, API/data contract, or multi-step feature needing acceptance criteria.  
**ADR trigger:** long-lived architecture, security boundary, data contract, major dependency/infrastructure, multi-component pattern, or hard-to-reverse choice.

## Deterministic discovery (when needed)

From the target Git repository, resolve this Skill's installed directory and run:

```bash
bash "<skill-dir>/scripts/preflight.sh" .
```

The script is **read-only** and reports branch, worktree, recent commits, availability of `gh`/`openspec`, OpenSpec directories, and likely Accepted ADR files. Review only relevant matching ADRs; status labels must be verified within the documents. If shell is unavailable, inspect the same facts via available repository tools. Remote Issue/PR state requires a separate authorized GitHub lookup.

## Command implementation

For any non-`help` command, read **only its own heading** in [references/commands.md](references/commands.md). Use documented commands only after confirming the CLI/integration exists. Do not indiscriminately load all specifications or ADRs.

## Non-negotiable rules

- Reuse existing Issue, change, ADR, branch, and PR; never invent identifiers or success reports.
- Before architecture-sensitive implementation, read relevant **Accepted ADRs**. New significant decisions remain **Proposed** until explicit human acceptance. Do not self-accept or silently override.
- If approval changes design, update the OpenSpec design/tasks **before** implementation.
- Log tests that passed, failed, and **were not run**. Never claim actions succeeded without evidence.
- Do not self-approve, merge, release, deploy, or modify remote state without appropriate authorization.

## Handoff

Report concisely: stage, relevant Issue/Spec/ADR/PR, actual test evidence (or not run), blockers, and **one next action**. Omit fields not applicable to the selected command.
