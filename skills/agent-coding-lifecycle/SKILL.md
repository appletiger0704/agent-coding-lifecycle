---
name: agent-coding-lifecycle
description: Route GitHub Issue, OpenSpec, ADR, coding, and PR tasks for Codex or Claude Code. Invoke with help, status, issue, openspec, adr, implement, pr, close, or run. Use for starting or resuming a repository development task; skip for trivial edits and general questions.
---

# Agent Coding Lifecycle — Command Router (MVP)

One shared skill, multiple **on-demand commands**. Do not execute the full lifecycle when only one command was requested.

## Invoke

- Codex: `$agent-coding-lifecycle <command> [details]`
- Claude Code: `/agent-coding-lifecycle <command> [details]`
- Optional Claude namespaced wrappers: `/agent-coding-lifecycle:<command> [details]` (require separate command installation).
- User arguments in Claude Code: $ARGUMENTS
- If no command is given, use `run`. If the command is unknown, display `help` instead of taking action.

## Commands

| Command | Outcome |
|---|---|
| `help` | List purpose, commands, and the recommended Issue → OpenSpec → ADR → Code → PR flow. No repository scan. |
| `status` | Read-only stage and blockers, without changing files or GitHub. |
| `issue` | Inspect, draft, or (when authorized) create/update an Issue. |
| `openspec` | Use the project's existing OpenSpec workflow, if installed. |
| `adr` | Check relevant accepted decisions; propose an ADR only for significant architecture changes. |
| `implement` | Implement an approved scope and run relevant tests. |
| `pr` | Summarize/review changes and prepare or (when authorized) create a PR. |
| `close` | After confirmed merge, archive and update status when authorized. |
| `run` | Inspect existing progress and continue **only the next unfinished step**. |

For `help`, show: (1) the six-stage standard sequence `issue → openspec → adr gate → implement → pr → close`, (2) `status` as read-only inspection, (3) `run` as one-step resume, and (4) an ADR check does not always produce a new ADR. If ADR approval changes design, revisit OpenSpec before implementation. For other commands, read **only the matching section** of [references/commands.md](references/commands.md), plus pertinent repository evidence. Do not read all related ADRs or specifications indiscriminately.

## Always enforce

1. Reuse current Issues, changes, ADRs, branches, and PRs; do not recreate existing work.
2. OpenSpec, ADR skills, and GitHub tooling remain the owners of their respective operations. Never claim an uninstalled tool was invoked.
3. Read relevant **Accepted** ADRs before architectural implementation. Significant changes require a **Proposed** ADR and explicit human acceptance first. Never self-accept or silently override an Accepted ADR.
4. Never self-approve, merge, release, deploy, or change remote data without appropriate authorization. Report unavailable permissions/tools and unrun tests.
5. Keep simple changes lightweight; do not mandate a full OpenSpec change or ADR for routine bug fixes.

## Handoff

For commands other than `help`, keep the result brief: **stage**, relevant **Issue / OpenSpec / ADR / PR**, **tests** (actual result or not run), **blocker**, and **next action**. Omit irrelevant fields instead of filling the response with `N/A`.
