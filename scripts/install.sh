#!/usr/bin/env bash
set -euo pipefail

# Version-aware local installer. No global installation, no auto-overwrites.
# Usage: bash scripts/install.sh /path/to/product-repo [--force|--check|--dry-run]
if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo 'Usage: bash scripts/install.sh /path/to/product-repo [--force|--check|--dry-run]' >&2
  exit 2
fi
mode="${2:-install}"
case "$mode" in install|--force|--check|--dry-run) ;; *) echo "unknown option: $mode" >&2; exit 2 ;; esac
source_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ ! -d "$1" ]]; then
  echo "target directory does not exist: $1" >&2
  exit 2
fi
target_root="$(cd "$1" && pwd)"
source_dir="$source_root/skills/agent-coding-lifecycle"
outdated=0

copy_one() {
  local source="$1" dest="$2"
  if [[ ! -f "$source" ]]; then echo "MISSING SOURCE: $source" >&2; exit 2; fi
  if [[ -f "$dest" ]] && cmp -s "$source" "$dest"; then
    echo "CURRENT: $dest"
    return
  fi
  if [[ "$mode" == "--check" ]]; then
    echo "OUTDATED OR MISSING: $dest"
    outdated=$((outdated+1))
    return
  fi
  if [[ "$mode" == "--dry-run" ]]; then echo "WOULD INSTALL: $dest"; return; fi
  if [[ -e "$dest" && "$mode" != "--force" ]]; then
    echo "SKIP different existing file: $dest (review then --force)"
    return
  fi
  mkdir -p "$(dirname "$dest")"
  cp "$source" "$dest"
  echo "INSTALLED: $dest"
}

for agent_root in ".agents/skills" ".claude/skills"; do
  dest_dir="$target_root/$agent_root/agent-coding-lifecycle"
  for file in SKILL.md VERSION references/commands.md scripts/preflight.sh scripts/status-validator.py scripts/verification-runner.py; do
    copy_one "$source_dir/$file" "$dest_dir/$file"
  done
done

for cmd in help status issue openspec adr implement pr close run quick; do
  copy_one "$source_root/.claude/commands/agent-coding-lifecycle/$cmd.md" \
           "$target_root/.claude/commands/agent-coding-lifecycle/$cmd.md"
done

if [[ "$mode" == "--check" ]]; then
  echo "outdated_files=$outdated"
  [[ "$outdated" -eq 0 ]] || exit 1
else
  echo 'Review before upgrading existing files. Restart Claude Code if commands do not appear.'
fi
