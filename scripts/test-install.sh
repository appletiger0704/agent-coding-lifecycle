#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/product"
bash "$root/scripts/install.sh" "$tmp/product" > /dev/null
bash "$root/scripts/install.sh" "$tmp/product" --check | grep -q 'outdated_files=0'
test -f "$tmp/product/.agents/skills/agent-coding-lifecycle/scripts/verification-runner.py"
test -f "$tmp/product/.claude/commands/agent-coding-lifecycle/quick.md"
echo 'old version' > "$tmp/product/.claude/skills/agent-coding-lifecycle/VERSION"
if bash "$root/scripts/install.sh" "$tmp/product" --check > /dev/null; then
  echo 'FAIL: version drift should be detected' >&2
  exit 1
fi
bash "$root/scripts/install.sh" "$tmp/product" --force > /dev/null
bash "$root/scripts/install.sh" "$tmp/product" --check | grep -q 'outdated_files=0'
echo 'installer version checks passed'
