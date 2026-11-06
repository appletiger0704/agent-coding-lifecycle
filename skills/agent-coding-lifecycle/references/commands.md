# Command behaviors — read only the requested section

This file supplements `SKILL.md`. Use the routing gate first. Replace example identifiers with validated ones. **Never paste chat slash commands into a shell.**

## status

- Run the read-only discovery: `bash "<skill-dir>/scripts/preflight.sh" .`
- If a specific Issue is known and `gh` is available/authenticated: `gh issue view 123 --json number,title,state,url,body`.
- If a PR is known and `gh` is available/authenticated: `gh pr view 123 --json number,state,mergedAt,url`.
- If `gh` is missing, use an authorized GitHub connector; otherwise state remote status was **not checked**.
- Report current stage, existing work, approval blockers, and one next step. No writes.

## issue

- Read existing Issue first: `gh issue view 123 --json number,title,state,url,body` or an authorized GitHub connector.
- If no issue identifier is given, `gh issue list --limit 20` may help (if available); do not substitute an invented issue number.
- Capture objective, acceptance criteria, and relevant OpenSpec / ADR links.
- Create/update remotely **only when authorized**. Without GitHub access, provide a draft and say it was not saved.

## openspec

- **Gate:** Check `openspec/` and `command -v openspec` or installed Agent skills/commands. A CLI may exist while this Repo is not initialized.
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

## implement

- Read Issue acceptance criteria, relevant OpenSpec tasks (if present), and applicable Accepted ADRs; do not load all records.
- No implementation of an architecture-sensitive Proposed ADR before human approval.
- Review the worktree before edits: `git status --short` and `git diff --check`. Respect existing uncommitted changes.
- Implement only the requested scope. Run the target Repo's real documented tests; record commands, passes, failures, and **not-run** checks. Never invent a test command.
- If a significant new technical choice arises, route back to `adr`; after approval, revise OpenSpec if needed.

## pr

- Check changes first: `git status --short`, `git diff --check`, `git diff --stat`.
- If `gh` exists and an existing PR may exist, inspect via `gh pr status` or `gh pr view --json number,state,url`.
- Prepare the PR with Issue, OpenSpec change (if any), Accepted / Proposed ADR state, change summary, tests run/not run, risks, and remaining work.
- Only create a remote PR if the user authorized it and tooling is available. Never self-approve, merge or deploy.

## close

- **Gate:** Verify merge, not just review completion: `gh pr view 123 --json number,state,mergedAt,url` (or authoritative GitHub connector). A non-null `mergedAt` indicates merge.
- After confirmed merge and authorization, follow installed OpenSpec archive/sync convention and update Issue/Project status.
- If the PR is open, checks have not passed, or remote status cannot be verified, do **not** close or claim successful completion.

## run

- Perform `status` discovery and select the **next unfinished** step; never reset to Issue if work already exists.
- Routine fix with established patterns → `implement` (respect Issue as context), then `pr`.
- OpenSpec missing and not specifically requested → skip that stage; significant architecture choice still requires `adr`.
- Significant architecture decision pending → stop affected implementation at Proposed ADR until a human accepts it.
- Work ready for review → `pr`; confirmed merged → `close` only with authorization.
- Execute **one** selected stage per invocation, summarize results and the next step. Do not silently chain to merge/deployment.
