#!/usr/bin/env bash
set -euo pipefail

# Read-only, bounded repository discovery for agent-coding-lifecycle.
# Usage: bash scripts/preflight.sh [path-to-git-repo]
repo="${1:-.}"
if [[ ! -d "$repo" ]] || ! git -C "$repo" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo 'error=not_a_git_repository' >&2
  exit 2
fi
cd "$(git -C "$repo" rev-parse --show-toplevel)"

printf 'repository=%s\n' "$PWD"
printf 'branch=%s\n' "$(git branch --show-current | sed 's/^$/DETACHED_HEAD/')"
printf 'dirty_files=%s\n' "$(git status --porcelain=v1 | wc -l | tr -d '[:space:]')"
printf 'recent_commits:\n'
commits="$(git log --oneline -5 2>/dev/null || true)"
if [[ -n "$commits" ]]; then printf '%s\n' "$commits"; else echo '(none)'; fi

for cli in gh openspec; do
  if command -v "$cli" >/dev/null 2>&1; then
    printf '%s_cli=available\n' "$cli"
  else
    printf '%s_cli=missing\n' "$cli"
  fi
done

if [[ -d openspec ]]; then
  echo 'openspec_directory=present'
  if [[ -d openspec/changes ]]; then
    printf 'openspec_active_changes:\n'
    change_count=0
    for change in openspec/changes/*; do
      if [[ -d "$change" && "${change##*/}" != archive ]]; then
        change_count=$((change_count+1))
        if [[ "$change_count" -le 20 ]]; then printf '%s\n' "$change"; fi
      fi
    done
    printf 'openspec_active_change_count=%d\n' "$change_count"
  fi
else
  echo 'openspec_directory=absent'
fi

is_accepted() {
  awk '
    NR > 80 { exit }
    {
      line=tolower($0)
      if (line ~ /^[[:space:]]*(-[[:space:]]*)?(status:[[:space:]]*accepted([[:space:]]|$)|\*\*status:\*\*[[:space:]]*accepted([[:space:]]|$)|\*\*status\*\*:[[:space:]]*accepted([[:space:]]|$))/) accepted=1
      if (line ~ /^[[:space:]]*##[[:space:]]*status[[:space:]]*$/) in_status=1
      else if (in_status && line ~ /^[[:space:]]*accepted[[:space:]]*$/) accepted=1
      else if (in_status && line ~ /^[[:space:]]*##/) in_status=0
    }
    END { exit accepted ? 0 : 1 }
  ' "$1"
}

adr_dirs=()
add_adr_dir() {
  for existing in ${adr_dirs[@]+"${adr_dirs[@]}"}; do
    [[ "$existing" == "$1" ]] && return
  done
  adr_dirs+=("$1")
}
if [[ -f .adr-dir ]]; then
  configured="$(head -n 1 .adr-dir)"
  if [[ "$configured" != /* && "$configured" != *".."* && -d "$configured" ]]; then add_adr_dir "$configured"; fi
fi
for candidate in docs/adr doc/adr docs/decisions adr decisions; do
  if [[ -d "$candidate" ]]; then add_adr_dir "$candidate"; fi
done
if [[ -z "${adr_dirs[*]-}" ]]; then
  echo 'adr_directories=none'
else
  printf 'adr_directories=%s\n' "${adr_dirs[*]}"
  echo 'accepted_adrs:'
  count=0
  while IFS= read -r -d '' file; do
    if is_accepted "$file"; then
      count=$((count+1))
      if [[ "$count" -le 20 ]]; then printf '%s\n' "$file"; fi
    fi
  done < <(find "${adr_dirs[@]}" -type f -name '*.md' -print0)
  printf 'accepted_adr_count=%d\n' "$count"
fi

echo 'remote_issue_pr_status=not_checked (requires explicit GitHub lookup)'
