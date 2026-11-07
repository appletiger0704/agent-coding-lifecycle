#!/usr/bin/env python3
"""Evidence-oriented, issue-scoped lifecycle status (stdlib only).

Live mode queries GitHub via gh and Git via git. Snapshot mode is solely for
offline tests and is NEVER an authorization source.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


class EvidenceError(Exception):
    pass


def run(args, cwd):
    try:
        process = subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False, timeout=20)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise EvidenceError(f"tool_unavailable:{args[0]}:{type(exc).__name__}") from exc
    if process.returncode != 0:
        raise EvidenceError(f"command_failed:{args[0]}:{process.stderr.strip()[:160]}")
    return process.stdout.strip()


def json_command(args, cwd):
    try:
        return json.loads(run(args, cwd))
    except json.JSONDecodeError as exc:
        raise EvidenceError(f"invalid_json:{args[0]}") from exc


def adr_status(path):
    """Only read declared status, not loose mentions of Accepted in prose."""
    if not path.is_file():
        return "MISSING"
    try:
        lines = path.read_text(encoding="utf-8").splitlines()[:100]
    except (OSError, UnicodeError):
        return "UNKNOWN"
    for index, line in enumerate(lines):
        match = re.match(r"^\s*(?:-\s*)?(?:\*\*)?status(?:\*\*)?:?(?:\*\*)?\s*(accepted|proposed|superseded|rejected)\b", line, re.I)
        if match:
            return match.group(1).upper()
        if re.match(r"^\s*##\s*status\s*$", line, re.I):
            for subsequent in lines[index + 1:]:
                if not subsequent.strip():
                    continue
                result = re.match(r"^\s*(accepted|proposed|superseded|rejected)\b", subsequent, re.I)
                return result.group(1).upper() if result else "UNKNOWN"
    return "UNKNOWN"


def collect(repo, issue_number):
    repo = Path(repo).resolve()
    if not (repo / ".git").exists() and not (repo / ".git").is_file():
        raise EvidenceError("not_a_git_checkout")
    full_name = run(["gh", "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"], repo)
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", full_name):
        raise EvidenceError("invalid_repository_identity")
    issue = json_command(["gh", "issue", "view", str(issue_number), "-R", full_name,
                          "--json", "number,state,title,url"], repo)
    if issue.get("number") != issue_number:
        raise EvidenceError("issue_identity_mismatch")

    contract_path = repo / ".agent-lifecycle" / "issues" / f"{issue_number}.json"
    contract = None
    if contract_path.is_file():
        try:
            contract = json.loads(contract_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise EvidenceError("invalid_issue_contract") from exc
        if contract.get("issue_number") != issue_number or contract.get("type") not in ("routine", "feature", "architecture"):
            raise EvidenceError("invalid_contract_identity_or_type")

    branch = run(["git", "branch", "--show-current"], repo)
    head = run(["git", "rev-parse", "HEAD"], repo)
    dirty = bool(run(["git", "status", "--porcelain=v1"], repo))
    ahead = 0 if branch == "main" else None
    if branch and branch != "main":
        try:
            ahead = int(run(["git", "rev-list", "--count", "main..HEAD"], repo))
        except (EvidenceError, ValueError):
            ahead = None

    prs = json_command(["gh", "pr", "list", "-R", full_name, "--state", "all", "--limit", "100",
                        "--json", "number,state,mergedAt,headRefName,headRefOid,closingIssuesReferences,url"], repo)
    linked = []
    for pr in prs:
        refs = pr.get("closingIssuesReferences") or []
        if any(item.get("number") == issue_number and
               ((item.get("repository") or {}).get("nameWithOwner") in (None, full_name)) for item in refs):
            linked.append(pr)
    if branch and any(p.get("headRefName") == branch and p.get("number") not in
                      {linked_pr.get("number") for linked_pr in linked} for p in prs):
        raise EvidenceError("branch_pr_not_linked_to_issue")
    expected_pr = contract.get("pr_number") if contract else None
    if expected_pr is not None:
        if not isinstance(expected_pr, int) or expected_pr < 1:
            raise EvidenceError("invalid_contract_pr_number")
        if not any(pr.get("number") == expected_pr for pr in linked):
            raise EvidenceError("pr_not_linked_to_issue")
        linked = [pr for pr in linked if pr["number"] == expected_pr]
    elif len(linked) > 1:
        raise EvidenceError("ambiguous_linked_pull_requests")
    pr = linked[0] if linked else None

    kind = contract["type"] if contract else None
    spec_change = contract.get("spec_change") if contract else None
    if spec_change is not None and (not isinstance(spec_change, str) or not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,80}", spec_change)):
        raise EvidenceError("invalid_spec_change")
    spec_dir = repo / "openspec" / "changes" / spec_change if spec_change else None
    spec_exists = bool(spec_dir and (spec_dir / "proposal.md").is_file() and (spec_dir / "tasks.md").is_file())
    adr_paths = contract.get("adr_paths", []) if contract else []
    if not isinstance(adr_paths, list):
        raise EvidenceError("invalid_adr_paths")
    adr_records = []
    for rel in adr_paths:
        if not isinstance(rel, str) or not rel.startswith(("docs/adr/", "adr/", "decisions/")) or ".." in Path(rel).parts or not rel.endswith(".md"):
            raise EvidenceError("unsafe_adr_path")
        adr_records.append({"path": rel, "status": adr_status(repo / rel)})
    required_checks = contract.get("required_checks", []) if contract else []
    if not isinstance(required_checks, list) or not all(isinstance(x, str) and x.strip() for x in required_checks):
        raise EvidenceError("invalid_required_checks")
    checks = []
    checks_verified = False
    if pr:
        check_sha = pr.get("headRefOid")
        if check_sha:
            try:
                response = json_command(["gh", "api", f"repos/{full_name}/commits/{check_sha}/check-runs?per_page=100"], repo)
                checks = response.get("check_runs", [])
                checks_verified = True
            except EvidenceError:
                pass
    return {
        "source": "github_git_live", "repository": full_name,
        "issue": {"number": issue_number, "state": issue.get("state"), "verified": True, "url": issue.get("url")},
        "contract": {"exists": contract is not None, "type": kind},
        "spec": {"id": spec_change, "ready": spec_exists},
        "adr": {"items": adr_records},
        "implementation": {"branch": branch, "head_sha": head, "ahead": ahead, "dirty": dirty},
        "pull_request": {"number": pr.get("number"), "state": pr.get("state"), "merged_at": pr.get("mergedAt"),
                         "head_sha": pr.get("headRefOid"), "head_ref": pr.get("headRefName"), "url": pr.get("url")} if pr else None,
        "validation": {"required_checks": required_checks, "verified": checks_verified,
                       "checks": [{"name": x.get("name"), "conclusion": x.get("conclusion"), "status": x.get("status")} for x in checks]},
    }


def derive(facts):
    """Pure, conservative stage policy. All decisions are scoped to the Issue."""
    blockers = []
    issue = facts.get("issue") or {}
    if not issue.get("verified") or not isinstance(issue.get("number"), int):
        blockers.append("issue_not_verified")
    if issue.get("state") not in ("OPEN", "CLOSED"):
        blockers.append("issue_state_unknown")
    if facts.get("source") != "github_git_live":
        blockers.append("snapshot_not_authoritative")

    def result(stage, action, blocked=False, reason=None):
        reasons = blockers.copy()
        if reason:
            reasons.extend(reason if isinstance(reason, list) else [reason])
        return {"schema_version": "0.3", "issue_number": issue.get("number"),
                "stage": stage, "next_action": action, "blocked": blocked or bool(reasons),
                "blockers": reasons, "source": facts.get("source"),
                "evidence": {"repository": facts.get("repository"), "issue_url": issue.get("url"),
                             "branch": (facts.get("implementation") or {}).get("branch"),
                             "commit_sha": (facts.get("implementation") or {}).get("head_sha"),
                             "pr_url": (facts.get("pull_request") or {}).get("url"),
                             "ci_queried": (facts.get("validation") or {}).get("verified", False)}}

    if blockers:
        return result("unknown", "verify_evidence", True)
    contract = facts.get("contract") or {}
    if not contract.get("exists"):
        return result("issue", "define_issue_contract", True, "missing_issue_contract")
    kind = contract.get("type")
    if kind not in ("routine", "feature", "architecture"):
        return result("issue", "define_issue_contract", True, "invalid_classification")
    if issue.get("state") == "CLOSED" and not (facts.get("pull_request") or {}).get("merged_at"):
        return result("unknown", "resolve_closed_issue", True, "issue_closed_without_verified_merge")
    spec = facts.get("spec") or {}
    if kind in ("feature", "architecture"):
        if not spec.get("id"):
            return result("openspec", "link_spec", True, "missing_spec_link")
        if not spec.get("ready"):
            return result("openspec", "prepare_spec")
    adr = facts.get("adr") or {}
    adrs = adr.get("items") or []
    if kind == "architecture" and not adrs:
        return result("adr", "propose_adr")
    for item in adrs:
        if item.get("status") != "ACCEPTED":
            return result("adr", "await_human_adr_approval", True,
                          f"adr_not_accepted:{item.get('path', '?')}:{item.get('status', 'UNKNOWN')}")
    implementation = facts.get("implementation") or {}
    pr = facts.get("pull_request") or {}
    if pr.get("merged_at"):
        return result("close", "verify_and_close")
    if pr.get("number"):
        if pr.get("state") != "OPEN":
            return result("unknown", "inspect_pr", True, "pr_not_open_or_merged")
        if implementation.get("branch") == pr.get("head_ref") and implementation.get("head_sha") != pr.get("head_sha"):
            return result("unknown", "sync_branch", True, "local_branch_out_of_date")
        validation = facts.get("validation") or {}
        required = validation.get("required_checks") or []
        if not required:
            return result("validation", "configure_required_checks", True, "missing_required_checks")
        if not validation.get("verified"):
            return result("validation", "verify_ci_checks", True, "ci_checks_unavailable")
        runs = validation.get("checks") or []
        missing = [check for check in required if not any(r.get("name") == check and r.get("conclusion") == "success" and r.get("status") == "completed" for r in runs)]
        if missing:
            return result("validation", "fix_or_run_tests", True, ["check_not_passed:" + c for c in missing])
        return result("review", "await_human_review", True, "human_review_required")
    if implementation.get("dirty"):
        return result("implementation", "review_uncommitted_changes", True, "dirty_worktree")
    if implementation.get("ahead") is None:
        return result("implementation", "verify_branch_history", True, "branch_history_unknown")
    if implementation["ahead"] == 0:
        return result("implement", "implement_change")
    return result("pr", "prepare_pull_request")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".")
    parser.add_argument("--issue", type=int)
    parser.add_argument("--snapshot", help="Offline test fixture; NOT an authorization source")
    parser.add_argument("--format", choices=["json"], default="json")
    args = parser.parse_args()
    if args.snapshot and args.issue:
        parser.error("--snapshot and --issue are mutually exclusive")
    if not args.snapshot and (not args.issue or args.issue <= 0):
        parser.error("live mode requires --issue N")
    try:
        facts = json.loads(Path(args.snapshot).read_text(encoding="utf-8")) if args.snapshot else collect(args.repo, args.issue)
        if args.snapshot:
            facts["source"] = "fixture"
        decision = derive(facts)
    except (EvidenceError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        decision = {"schema_version": "0.3", "stage": "unknown", "next_action": "verify_evidence",
                    "blocked": True, "blockers": [str(exc)], "source": "live_error"}
    print(json.dumps(decision, indent=2, ensure_ascii=False))
    return 0 if not decision["blocked"] else 2


if __name__ == "__main__":
    sys.exit(main())
