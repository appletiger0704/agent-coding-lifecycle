# Command behavior — load only the selected section

This file supplements `SKILL.md`. Never treat a subcommand as authorization to run every other phase.

## status

- Read-only: inspect repository instructions, current branch, relevant Issue/PR, OpenSpec change, and **relevant** ADRs as available.
- Infer the current stage and next unfinished action. Distinguish verified facts from missing access.
- **Do not create or modify** files, issues, ADRs, or PRs.

## issue

- Reuse an existing Issue; extract objectives, constraints, acceptance criteria, and relationships.
- When no Issue exists, draft one from the supplied context. Only create/update it remotely when user intent authorizes the write and the GitHub tool is available.
- Link any known OpenSpec change and ADR; do not invent issue numbers.

## openspec

- Check whether OpenSpec is installed/configured in the target project. Inspect its instructions and the existing `openspec/` directory first.
- With a supplied target change or intent, use **the OpenSpec tools/skills available in that environment** to explore, propose, apply, or archive, matching the user's requested operation.
- Never invent a shell command or claim invocation of a missing OpenSpec tool.
- If missing or unconfigured, provide concrete setup prerequisites and stop short of installation unless explicitly authorized.
- Don't regenerate an existing change or treat OpenSpec `design` as a replacement for accepted architecture decisions.
- After a major ADR is accepted, revisit the OpenSpec design/tasks if the approved decision changes the plan; do this before implementation.

## adr

- Read only the applicable **Accepted** ADRs; check for conflicts and supersession.
- If the work introduces significant long-term architectural tradeoffs, draft a **Proposed** ADR using the product repository's established template; link Issue and OpenSpec if known.
- Explicit human decision is required to change an ADR to `Accepted` or approve a superseding decision. Stop architecture-sensitive implementation until approval.
- Do not write a new ADR for ordinary bugfixes, formatting, or choices already governed by accepted decisions.
- If the project has an installed ADR Skill, prefer its documented creation and validation process rather than replicating it here.

## implement

- Inspect Issue acceptance criteria, relevant OpenSpec tasks, and applicable accepted ADR constraints.
- Do not implement an architecture-sensitive choice while its ADR is Proposed.
- Write small, reviewable changes; run relevant tests and checks. State what passed, failed, or wasn't run.
- If a significant new design choice emerges, return to the ADR gate rather than silently committing to it.
- Do not self-deploy, self-approve, or claim a PR was merged.

## pr

- Inspect diff, branch, test evidence, and current PR before creating anything.
- Present an Issue reference, OpenSpec change (if applicable), Accepted/Proposed ADR status, change summary, test commands/results, remaining risk, and review request.
- Use an existing PR when present. Create a new remote PR only when explicitly requested or authorized, and tooling is available.
- No self-approval, merge, release, or deployment.

## close

- Verify that the PR actually merged and that corresponding work is complete.
- When the user authorizes closure, use the project's installed OpenSpec archiving approach and update linked Issue/Project status. If tools unavailable, provide accurate manual steps instead.
- An open PR or completed coding task is **not** proof of merge; never close early.

## run

- Inspect what exists: repository instructions, Issue, branch/PR, existing OpenSpec change, applicable accepted ADR, and completed tasks.
- Pick the **next unfinished step**; do not create redundant docs or force a full process for trivial changes.
- If blocked by a Proposed ADR or unavailable tool/approval, explain and stop the affected operations.
- Delegate the selected stage to the matching command section above, not every command at once.
