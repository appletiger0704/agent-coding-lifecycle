---
name: agent-coding-lifecycle
disable-model-invocation: true
description: "Use when explicitly invoked to coordinate a GitHub Issue → OpenSpec → ADR → PR workflow or a cross-agent handoff. 中文：接續 Issue、開發生命週期、OpenSpec 規格、ADR 架構決策、交接開發。 Do not auto-trigger for ordinary coding, trivial fixes, or general questions."
---

# Agent Coding Lifecycle — v0.4 Release Candidate (Quick + Tracked)

Coordinate existing tools; do not replace GitHub, OpenSpec, ADR skills, tests, or human reviewers.

## Invocation

- Codex: `$agent-coding-lifecycle <command> [details]`
- Claude Code: `/agent-coding-lifecycle <command> [details]`
- Claude wrappers (separate install): `/agent-coding-lifecycle:<command> [details]`
- Commands: `help`, `status`, `quick`, `issue`, `openspec`, `adr`, `implement`, `pr`, `close`, `run`.
- Unknown command → `help`; omitted command → `help` (never infer Issue or auto-enter Tracked mode).

## Modes

- **Quick (explicit `quick`)**: small, local, reversible change; no mandatory Issue/OpenSpec/ADR/PR. Inspect changes, preserve user files, run relevant verification, and report not-run checks. No remote writes unless separately authorized. Upgrade to Tracked if new public behavior, long-lived decisions, security/data contracts or cross-agent persistence are required.
- **Tracked (`status` / `run` / named stages)**: versioned Issue → conditional OpenSpec/ADR → implement → PR → close, with Issue-scoped live state validation. Keep the existing approval and CI gates.
- Neither mode may self-accept ADR, merge, deploy or claim success without observed evidence.

## Routing gate — BEFORE any workflow

1. `help`: display Quick and Tracked commands and `issue → openspec → adr → implement → pr → close`. **No repository scan, no tools.**
2. `status`: discovery only. **No file or remote writes.**
3. `quick`: execute only the requested local change after scope/safety classification; do not manufacture an Issue, Spec, ADR or PR.
4. Explicit Tracked stage command: execute **only that stage** and its necessary safety checks; do not run all stages.
5. `run`: require a specific Issue number, obtain the **live validator result**, and handle only its allowed next stage. When blocked or unverified, stop; never auto-merge or deploy.
6. No Git repository: do not claim successful discovery; for `issue`, drafting from supplied text is allowed, but report missing repo access.
7. Routine fix using established patterns: skip creating OpenSpec changes and ADRs unless user/project policy requires them.
8. No `openspec/` or OpenSpec tooling: routine fixes can skip it. For feature/architecture contracts requiring a spec, report the missing prerequisite and stop; never pretend it ran.
9. No existing ADR directory: skip searching absent ADRs. **Still propose** an ADR when a genuinely significant new architecture decision arises.

**Spec trigger:** new/changed externally observable behavior, API/data contract, or multi-step feature needing acceptance criteria.  
**ADR trigger:** long-lived architecture, security boundary, data contract, major dependency/infrastructure, multi-component pattern, or hard-to-reverse choice.

## Issue-scoped state validation (v0.3 P0)

For Tracked `status` or `run` on Issue #N, get read-only live evidence before stage selection. Quick does not use this validator:

```bash
python3 "<skill-dir>/scripts/status-validator.py" --repo . --issue N
```

Requires Git checkout, Python 3, authenticated `gh` with access to Issues/PRs/Checks, and a reviewed `.agent-lifecycle/issues/N.json` contract from the central Repo template. Do not invent an Issue ID or classification.

- Trust `stage` / `next_action` / `blocked` only when `source=github_git_live`; `--snapshot` is **not live evidence**.
- If `blocked=true`, the command fails, or remote status is unknown: report the blocker, **do not advance**. A separately authorized explicit command may address a specific blocker.
- `run` executes only one validated action; actions requiring a human stop rather than being performed by the Agent.
- The validator only parses ADR document status, **not independent approval provenance**; OpenSpec file presence is not semantic approval either. **Never let an Accepted string alone authorize new architecture-sensitive implementation.** See [v0.3 contract and limitations](https://github.com/appletiger0704/agent-coding-lifecycle/blob/main/docs/v0.3-deterministic-state.md) in the central repository.
- Passing CI is not authorization to merge.

## Deterministic discovery (when needed)

From the target Git repository, resolve this Skill's installed directory and run:

```bash
bash "<skill-dir>/scripts/preflight.sh" .
```

The script is **read-only** and reports branch, worktree, recent commits, availability of `gh`/`openspec`, OpenSpec directories, and likely Accepted ADR files. Review only relevant matching ADRs; status labels must be verified within the documents. If shell is unavailable, inspect the same facts via available repository tools. Remote Issue/PR state requires a separate authorized GitHub lookup.

## Optional project verification profile

Each target repo may define `.agent-lifecycle/verification.json` by adapting `templates/verification.python.json`. **Review profile commands before use**; do not invent missing commands or silently install tools. This repo ships a stdlib runner:

```bash
python3 "<skill-dir>/scripts/verification-runner.py" --repo . --profile .agent-lifecycle/verification.json --list
python3 "<skill-dir>/scripts/verification-runner.py" --repo . --profile .agent-lifecycle/verification.json --run
```

The runner uses argv arrays without a shell, records passed/failed/not-run, and does not persist test output. No profile → use documented repo checks, and explicitly say what was not run.

## Command implementation

For any non-`help` command, read **only its own heading** in [references/commands.md](references/commands.md). Use documented commands only after confirming the CLI/integration exists. Do not indiscriminately load all specifications or ADRs.

## Non-negotiable rules

- Reuse existing Issue, change, ADR, branch, and PR; never invent identifiers or success reports.
- Before architecture-sensitive implementation, read relevant **Accepted ADRs**. New significant decisions remain **Proposed** until explicit human acceptance. Do not self-accept or silently override.
- If approval changes design, update the OpenSpec design/tasks **before** implementation.
- Log tests that passed, failed, and **were not run**. Never claim actions succeeded without evidence.
- Do not self-approve, merge, release, deploy, or modify remote state without appropriate authorization.

## Handoff

Report: mode, Issue (if Tracked), stage, relevant Spec/ADR/PR, evidence source and commit SHA when available, tests passed/failed/not-run, blockers, and one next action. A handoff summary is **not** proof of work completion; always re-check live GitHub state in a new session.
