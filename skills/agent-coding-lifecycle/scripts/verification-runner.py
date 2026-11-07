#!/usr/bin/env python3
"""Optional, local-only checks from a reviewed project profile (no shell)."""
import argparse
import json
import subprocess
import sys
from pathlib import Path


def verify(profile_path, repo, execute=False):
    path = Path(profile_path).resolve()
    repo = Path(repo).resolve()
    if not path.is_file() or not repo.is_dir():
        raise ValueError("profile_or_repo_missing")
    profile = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(profile, dict) or profile.get("schema_version") != 1:
        raise ValueError("unsupported_profile_version")
    checks = profile.get("checks")
    if not isinstance(checks, list) or not checks:
        raise ValueError("checks_must_be_nonempty_list")
    names = set()
    results = []
    for check in checks:
        if not isinstance(check, dict):
            raise ValueError("invalid_check")
        name, argv = check.get("name"), check.get("argv")
        if not isinstance(name, str) or not name.strip() or name in names:
            raise ValueError("duplicate_or_invalid_check_name")
        names.add(name)
        if not isinstance(argv, list) or not argv or not all(isinstance(a, str) and a for a in argv):
            raise ValueError("invalid_command_argv")
        if any("\x00" in a for a in argv):
            raise ValueError("invalid_command_argv")
        enabled = check.get("enabled", True)
        if not isinstance(enabled, bool):
            raise ValueError("invalid_enabled_flag")
        timeout = check.get("timeout_seconds", 300)
        if not isinstance(timeout, int) or isinstance(timeout, bool) or not 1 <= timeout <= 3600:
            raise ValueError("invalid_timeout")
        item = {"name": name, "argv": argv, "status": "not_run", "exit_code": None}
        if execute and enabled:
            try:
                process = subprocess.run(argv, cwd=repo, capture_output=True, text=True, timeout=timeout,
                                         check=False)
                item["exit_code"] = process.returncode
                item["status"] = "passed" if process.returncode == 0 else "failed"
            except (OSError, subprocess.TimeoutExpired):
                item["status"] = "error"
        results.append(item)
    return {"schema_version": 1, "source": "local_profile", "profile": str(path), "checks": results,
            "all_enabled_passed": execute and all(x["status"] in ("passed", "not_run") for x in results)
            and all(x["status"] == "passed" for x, chk in zip(results, checks) if chk.get("enabled", True))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".")
    parser.add_argument("--profile", required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--list", action="store_true", help="show commands without running")
    mode.add_argument("--run", action="store_true", help="execute reviewed commands locally")
    args = parser.parse_args()
    try:
        result = verify(args.profile, args.repo, execute=args.run)
    except (ValueError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc), "all_enabled_passed": False, "checks": []}))
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if args.list or result["all_enabled_passed"] else 2


if __name__ == "__main__":
    sys.exit(main())
