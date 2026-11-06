#!/usr/bin/env bash
set -euo pipefail

# Install the shared skill plus Claude Code namespaced command wrappers.
# Usage: bash scripts/install.sh /path/to/product-repo [--force]
if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: bash scripts/install.sh /path/to/product-repo [--force]" >&2
  exit 2
fi

force="${2:-}"
if [[ -n "$force" && "$force" != "--force" ]]; then
  echo "Unknown option: $force" >&2
  exit 2
fi

source_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ ! -d "$1" ]]; then
  echo "Target directory does not exist: $1" >&2
  exit 2
fi
target_root="$(cd "$1" && pwd)"

copy_one() {
  local source="$1"
  local dest="$2"
  if [[ ! -f "$source" ]]; then
    echo "Missing source: $source" >&2
    exit 1
  fi
  if [[ -e "$dest" && "$force" != "--force" ]]; then
    echo "SKIP existing: $dest"
    return
  fi
  mkdir -p "$(dirname "$dest")"
  cp "$source" "$dest"
  echo "INSTALLED: $dest"
}

for agent_root in ".agents/skills" ".claude/skills"; do
  source_dir="$source_root/skills/agent-coding-lifecycle"
  dest_dir="$target_root/$agent_root/agent-coding-lifecycle"
  copy_one "$source_dir/SKILL.md" "$dest_dir/SKILL.md"
  copy_one "$source_dir/references/commands.md" "$dest_dir/references/commands.md"
  copy_one "$source_dir/scripts/preflight.sh" "$dest_dir/scripts/preflight.sh"
done

for cmd in help status issue openspec adr implement pr close run; do
  copy_one \
    "$source_root/.claude/commands/agent-coding-lifecycle/$cmd.md" \
    "$target_root/.claude/commands/agent-coding-lifecycle/$cmd.md"
done

echo "Done. Restart Claude Code if new slash commands do not appear."
echo "Codex: \$agent-coding-lifecycle help"
echo "Claude Code: /agent-coding-lifecycle:help"
