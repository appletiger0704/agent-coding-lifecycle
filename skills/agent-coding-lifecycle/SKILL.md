---
name: agent-coding-lifecycle
description: Coordinate software changes across GitHub Issues, OpenSpec, existing architecture decision records (ADRs), implementation, tests, and pull requests. Use when starting, resuming, or reviewing a feature or significant code change with Codex or Claude Code. Do not invoke for general questions, trivial one-line edits, or work without a repository.
---

# Agent Coding Lifecycle — MVP v0.1

Act as a **workflow coordinator**, not a replacement for GitHub, OpenSpec, an ADR skill, test tools, or a human reviewer. Follow this process only to the extent needed for the current task.

## 0. Resume and assess

1. Read project-level instructions (`AGENTS.md`, `CLAUDE.md`, or equivalent), then inspect the relevant repository.
2. Identify the Issue/request, current branch and PR (if any), existing OpenSpec change, relevant ADRs, and completed tasks.
3. Determine the **next unfinished step**. Do not recreate issues, specs, ADRs, branches, or PRs that already exist.
4. Check what CLI, integrations, and permissions are actually available; do not imply an operation succeeded without checking.
5. For small fixes that follow established patterns, prefer a lightweight Issue → implementation → tests → PR flow; do not force a large specification or ADR.

## 1. Intake — GitHub Issue

- Reuse the existing Issue if one exists. Capture the objective, scope, acceptance criteria, and relevant constraints.
- If GitHub access is unavailable, work from a supplied issue description; report missing links explicitly instead of inventing them.
- Create or update remote Issues only when the request authorizes that change.

## 2. Plan — OpenSpec

- Reuse the repository's **existing** OpenSpec change and conventions first.
- When OpenSpec is installed and the change warrants specifications, use its maintained workflow, not a new homemade specification format. The current core workflow provides explore (optional), propose, apply, sync/update, and archive. Check the installed version for exact commands and behavior.
- Prefer proposal/specs/design/tasks for meaningful feature changes; avoid duplicate prose between Issue, OpenSpec, and ADR.
- If OpenSpec is absent, **do not silently install or initialize it**. Follow project instructions or present the needed setup as a separate task.

## 3. Decision gate — ADR

- Search the product repository's ADR directory (e.g. `docs/adr/`) and read relevant **Accepted** records *before implementation*.
- Propose an ADR if the choice is significant: changes long-lived architecture, security boundaries, data contracts, major dependencies or infrastructure, affects several components, or is costly to reverse.
- If needed, write a **Proposed** ADR using the repository's template and link it to Issue and OpenSpec.
- **Never approve an ADR or change its status to Accepted autonomously.** Wait for explicit human approval before implementing the architecture-sensitive choice.
- If the request conflicts with an Accepted ADR, report the conflict and propose a superseding ADR; do not silently disregard the decision.
- Do not create an ADR for routine fixes, formatting, small refactors, or decisions already covered by existing records.

## 4. Implement and verify

- Follow the relevant OpenSpec tasks or the Issue acceptance criteria and Accepted ADR constraints.
- Implement in reviewable increments. Run applicable tests and checks when executable in the environment; record actual results, including failures and any checks not run.
- If a substantial design change emerges, return to the decision gate before continuing the affected work.
- Do not claim test success, deployed state, or tool execution without evidence.

## 5. Review — PR

- Prepare a PR or PR description that includes:
  - GitHub Issue link or identifier;
  - OpenSpec change path (or `N/A`);
  - relevant Accepted ADR / Proposed ADR status (or `N/A`);
  - implementation summary, test commands/results, known risks and remaining work.
- Create a remote PR only when authorized and supported by available tooling.
- **Do not self-approve, merge, release, or deploy** without explicit authorization and the repository's required checks/review.

## 6. Close — only after actual merge

- After confirmed merge, follow the installed OpenSpec procedure for syncing/archiving a completed change, where appropriate.
- Update Issue/Project status only with authorization and after verifying the relevant outcome.
- Do not treat a submitted PR as completed implementation.

## Response contract

At each handoff, report succinctly:

- **Stage:** Intake / Plan / ADR Gate / Implement / Review / Close
- **Issue:** link or missing
- **OpenSpec:** path / N/A / pending
- **ADR:** Accepted reference / Proposed pending review / N/A
- **Tests:** passed, failed, not run, or pending (with evidence)
- **PR:** link / not created
- **Next:** one concrete next step and any human approval blocker

## Non-goals for v0.1

No automated GitHub Projects board, CI enforcement, ADR CLI, model-specific sub-agent delegation, deployment automation, or new MCP server. These are later enhancements, not prerequisites.

## Reference

See the central project policy and MVP trial plan:
- https://github.com/appletiger0704/agent-coding-lifecycle/blob/main/docs/architecture/lifecycle.md
- https://github.com/appletiger0704/agent-coding-lifecycle/blob/main/docs/mvp.md
