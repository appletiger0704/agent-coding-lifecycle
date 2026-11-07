# Command behaviors — read only the requested section

This file supplements `SKILL.md`. Use the routing gate first. Replace example identifiers with validated ones. **Never paste chat slash commands into a shell.**

## quick

- Only run for an **explicit** request for a small, reversible, local change. No Issue ID required; do not silently create Issue/PR, initialize OpenSpec, or add ADR.
- Before edits, check requested scope and existing file changes. Existing architecture/security/contract policy still applies. If new externally observable contract, cross-component architecture, security or durable multi-session handoff is involved, **stop** and recommend Tracked mode with a specific reason.
- Use the target Repo's documented verification commands or optional reviewed `.agent-lifecycle/verification.json` with `verification-runner.py`. First `--list` to inspect, then `--run` when appropriate. Do not treat missing tools or skipped checks as passing.
- Keep changes scoped. Report files modified, tests actually run, failing/not-run checks, blockers and next action. No automatic remote writes, approval, merge, deploy or side effects outside explicit authorization.

## status

- For a **specified Issue #N**, run `python3 "<skill-dir>/scripts/status-validator.py" --repo . --issue N` before selecting any stage. This is read-only.
- Without an Issue number, run `bash "<skill-dir>/scripts/preflight.sh" .` for environment information only, and report `stage=unknown`; do not guess which Issue to resume.
- If the validator exits 2 or cannot run, report its blockers and do not synthesize a stage.
- If a specific Issue is known and `gh` is available/authenticated: `gh issue view 123 --json number,title,state,url,body`.
- If a PR is known and `gh` is available/authenticated: `gh pr view 123 --json number,state,mergedAt,url`.
- If `gh` is missing, use an authorized GitHub connector; otherwise state remote status was **not checked**.
- Report current stage, existing work, approval blockers, and one next step. No writes.

## issue

- Read existing Issue first: `gh issue view 123 --json number,title,state,url,body` or an authorized GitHub connector.
- If no issue identifier is given, `gh issue list --limit 20` may help (if available); do not substitute an invented issue number.
- Capture objective, acceptance criteria, and relevant OpenSpec / ADR links.
- For a newly classified task, prepare the reviewed `.agent-lifecycle/issues/<N>.json` contract based on central `templates/issue-contract.json` (`routine`, `feature`, or `architecture`). Never invent an Issue ID or silently overwrite the contract.
- Create/update remotely **only when authorized**. Without GitHub access, provide a draft and say it was not saved.

## openspec

- **Gate:** Check `openspec/` and `command -v openspec` or installed Agent skills/commands. A CLI may exist while this Repo is not initialized. For feature/architecture contracts, a missing required Spec blocks progress; it is not a routine skip.
- For a known change with the CLI installed, inspect state using `openspec status --change <change-name> --json`; obtain the ID from `openspec/changes/`, never invent it.
- Prefer the project's installed OpenSpec flow. Official core chat examples: Claude Code `/opsx:propose`, `/opsx:update`, `/opsx:apply`, `/opsx:archive`; Codex typically uses `$openspec-propose` and other installed OpenSpec skills. **These are chat/skill invocations, not shell commands.** Verify exact names/version locally.
- Reuse existing proposal/specs/design/tasks and never overwrite silently. If a newly accepted ADR alters design, revise design/tasks before implementation.
- If OpenSpec is absent: skip an **implicit** step. If explicitly requested, report installation/init as a prerequisite; do not auto-install.

## adr

- **Gate:** If no ADR directory exists, there are no existing ADR files to scan. This does not waive a major **new** architecture decision.
- Preflight lists likely Accepted documents in common ADR directories or `.adr-dir`. Open only those relevant to the current change; verify status and supersession by reading each file.
- For manual triage when `rg` is available: `rg -n -i 'status.*accepted|^## status$' docs/adr`; inspect candidate documents before treating them as Accepted. This is a **candidate search**, not a final status verifier.
- Create a Proposed ADR only if changing long-lived structure, security boundaries, data contracts, major dependencies/infrastructure, cross-component patterns, or costly-to-reverse choices.
- Follow the target Repo's ADR template/skill. Link Issue and OpenSpec, document alternatives, consequences and verification. **Human acceptance required** before architecture-sensitive implementation. Supersede rather than silently edit an Accepted decision.
- Routine fixes or an already-approved pattern: no new ADR.
- v0.3 document status parsing is **not proof of human approval**. Verify approval by project governance; P1 will add machine-checkable provenance.

## implement

- Read Issue acceptance criteria, relevant OpenSpec tasks (if present), and applicable Accepted ADRs; do not load all records.
- On a known Issue, run the live validator first. Missing required Spec, Proposed ADR, wrong linkage or unverifiable state must be addressed, not ignored.
- No implementation of an architecture-sensitive Proposed ADR before human approval.
- Review the worktree before edits: `git status --short` and `git diff --check`. Respect existing uncommitted changes.
- Implement only the requested scope. Run the target Repo's documented tests. If a reviewed `.agent-lifecycle/verification.json` exists, call `verification-runner.py --list` before `--run` and report passed/failed/not-run. Never invent tests or assume dependencies are installed.
- If a significant new technical choice arises, route back to `adr`; after approval, revise OpenSpec if needed.

## pr

- Check changes first: `git status --short`, `git diff --check`, `git diff --stat`.
- Verify Issue/PR linkage with the validator. A draft PR may precede CI; CI must be verified on that PR head SHA afterward. Never report unrun tests as passed.
- If `gh` exists and an existing PR may exist, inspect via `gh pr status` or `gh pr view --json number,state,url`.
- Prepare the PR with Issue, OpenSpec change (if any), Accepted / Proposed ADR state, change summary, tests run/not run, risks, and remaining work.
- GitHub checks must correspond to the PR's current SHA; passing checks do not replace explicit human approval or GitHub Rulesets. Include actual verification results, not self-approval.
- Only create a remote PR if the user authorized it and tooling is available. Never self-approve, merge or deploy.

## close

- **Gate:** Verify merge, not just review completion: `gh pr view 123 --json number,state,mergedAt,url` (or authoritative GitHub connector). A non-null `mergedAt` indicates merge.
- After confirmed merge and authorization, follow installed OpenSpec archive/sync convention and update Issue/Project status.
- If the PR is open, checks have not passed, or remote status cannot be verified, do **not** close or claim successful completion.

## run

- Require a concrete Issue number and run `python3 "<skill-dir>/scripts/status-validator.py" --repo . --issue N`. Do not infer the next stage from preflight alone.
- If `blocked=true`, source is not live, or exit is nonzero, **stop**. Report exactly why and the targeted remediation instead of bypassing the gate.
- For allowed actions, execute **only one** of: `prepare_spec`, `propose_adr`, `implement_change`, `prepare_pull_request` (as authorized). `define_issue_contract` belongs to the `issue` command.
- Review, validation, ADR human approval, merge and closure require their own actual evidence/authorization. Never auto-approve, merge or deploy.
