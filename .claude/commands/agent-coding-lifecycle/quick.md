---
description: Run a small, explicitly requested local task without mandatory Issue or PR.
disable-model-invocation: true
---

Execute only the `quick` subcommand of agent-coding-lifecycle.
User request: $ARGUMENTS

Load the first available instructions from:
1. `.claude/skills/agent-coding-lifecycle/SKILL.md`
2. `.agents/skills/agent-coding-lifecycle/SKILL.md`
3. `~/.claude/skills/agent-coding-lifecycle/SKILL.md`
4. `~/.agents/skills/agent-coding-lifecycle/SKILL.md`
5. `skills/agent-coding-lifecycle/SKILL.md`

Read only the adjacent `## quick` command in `references/commands.md`.
No automatic issue creation, PR creation, ADR acceptance, merge, or deploy. Escalate architecture-sensitive changes to Tracked mode.
