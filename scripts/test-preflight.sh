#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
preflight="$root/skills/agent-coding-lifecycle/scripts/preflight.sh"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

mkdir -p "$tmp/repo"
git -C "$tmp/repo" init -q
out="$(bash "$preflight" "$tmp/repo")"
grep -q '^openspec_directory=absent$' <<<"$out"
grep -q '^adr_directories=none$' <<<"$out"
grep -q '^remote_issue_pr_status=not_checked' <<<"$out"

mkdir -p "$tmp/repo/openspec/changes/example" "$tmp/repo/docs/adr"
cat > "$tmp/repo/docs/adr/0001-accepted.md" <<'ADR'
# ADR-0001
- **Status:** Accepted
ADR
cat > "$tmp/repo/docs/adr/0002-superseded.md" <<'ADR'
# ADR-0002
## Status
Superseded by ADR-0003
ADR
out="$(bash "$preflight" "$tmp/repo")"
grep -q '^openspec_directory=present$' <<<"$out"
grep -q '^accepted_adr_count=1$' <<<"$out"
grep -q '0001-accepted.md' <<<"$out"
if grep -q '0002-superseded.md' <<<"$out"; then
  echo 'FAIL: superseded ADR classified as accepted' >&2
  exit 1
fi

cat > "$tmp/repo/docs/adr/0003-block.md" <<'ADR'
# ADR-0003
## Status

Accepted
ADR
out="$(bash "$preflight" "$tmp/repo")"
grep -q '^accepted_adr_count=2$' <<<"$out"
if bash "$preflight" "$tmp/missing" >/dev/null 2>&1; then
  echo 'FAIL: missing repository was accepted' >&2
  exit 1
fi
echo 'preflight smoke tests passed'
