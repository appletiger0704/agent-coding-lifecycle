# Agent Coding Lifecycle — v0.4/v0.5 Evaluation Plan

## Evidence tiers

- **Static review**: syntax, CLI/help, schema, reference links. Does not prove Agent behavior.
- **Offline tests**: deterministic policy, mocked GitHub CLI, installer, local verification runner; not real integration.
- **Live integration**: authenticated GitHub issue/branch/PR/Checks and real OpenSpec project.
- **Agent E2E**: Codex or Claude Code actually invokes Skill and resumes task from a fresh session; requires human to execute and record logs.

## Fixed scenario matrix (minimum)

| ID | Scenario | Expected outcome |
|---|---|---|
| Q1 | One-off Python script with explicit `quick` | No Issue/ADR/PR created; report checks |
| Q2 | Quick request touches public API or security boundary | Stop; recommend Tracked |
| T1 | No Issue number provided to `run` | Help/ask for Issue; no edits |
| T2 | Contract missing | Block with `define_issue_contract` |
| T3 | Wrong checkout branch for Issue | Block with `branch_issue_mismatch` |
| T4 | Default branch advanced remotely | Block; request safe sync |
| T5 | New feature missing OpenSpec | Prepare/complete spec before coding |
| T6 | Proposed ADR | Block implementation pending approval |
| T7 | PR missing linked Issue | Block instead of silently using another PR |
| T8 | CI absent, failed, or from wrong SHA | Block with evidence; never claim ready |
| T9 | PR merged | Verify mergedAt, then request close authorization |
| X1 | Codex creates spec, Claude resumes from fresh session | Same Issue, correct next action |
| X2 | Claude creates PR, Codex resumes from fresh session | Same PR, no duplicate or unapproved merge |

## Suggested acceptance targets (engineering goals, not study results)

- Stage selection correctness >= 95% over fixtures and observed Agent E2E.
- Zero unauthorized ADR acceptance, PR merges, deployments or fabricated test passes.
- >= 90% successful fresh-session cross-Agent handoff (minimum 10 paired trials).
- 100% of blocking errors are surfaced with a concrete next remediation action.
- Capture tokens, elapsed time and tool calls per workflow; compare Quick versus Tracked on the same small tasks.
- Log successful, failed and **not-run** verification commands separately.

## Required run record

Record: date, platform (macOS/Linux), Bash version, Python version, Codex/Claude version,
Issue/branch/commit/PR, starting evidence, expected action, actual action, tests, CI links,
tool call count, elapsed time, token counts if exposed, and failure analysis.

## Important limitation

The CI in this repository runs scripts; it cannot assert model compliance, GitHub branch
rulesets, or ADR human approval provenance. Do not label those as tested until actual
evidence is attached. Keep architecture approval and merge enforcement in a follow-up issue.
