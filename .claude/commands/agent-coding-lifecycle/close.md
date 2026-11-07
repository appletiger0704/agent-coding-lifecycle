---
description: Archive/change issue state after a verified PR merge.
---

Execute ONLY the `close` subcommand of **agent-coding-lifecycle** for this user request.

User-supplied details: $ARGUMENTS

Read the first available skill instructions in this order:
1. `.claude/skills/agent-coding-lifecycle/SKILL.md`
2. `.agents/skills/agent-coding-lifecycle/SKILL.md`
3. `~/.claude/skills/agent-coding-lifecycle/SKILL.md` (personal Claude install)
4. `~/.agents/skills/agent-coding-lifecycle/SKILL.md` (personal Codex install)
5. `skills/agent-coding-lifecycle/SKILL.md` (central repository checkout)

Then consult ONLY the `## close` section of its adjacent `references/commands.md`. Follow the skill's safety rules; do not execute the other stages unless the selected `run` command directs you to the next unfinished stage. If the skill is unavailable, explain the missing installation rather than pretending it ran.
