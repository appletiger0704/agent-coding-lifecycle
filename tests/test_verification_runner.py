"""Verification profile: no network or third-party test dependency."""
import importlib.util
import json
import pathlib
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "skills/agent-coding-lifecycle/scripts/verification-runner.py"
SPEC = importlib.util.spec_from_file_location("acl_verify", SCRIPT)
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


class VerificationTests(unittest.TestCase):
    def test_profile_list_not_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = pathlib.Path(tmp)
            marker = repo / "marker"
            profile = repo / "verify.json"
            profile.write_text(json.dumps({"schema_version": 1, "checks": [
                {"name": "safe-check", "argv": [sys.executable, "-c", f"open({str(marker)!r},'w').write('x')"]}]}))
            result = M.verify(profile, repo, execute=False)
            self.assertFalse(marker.exists())
            self.assertEqual(result["checks"][0]["status"], "not_run")
            self.assertFalse(result["all_enabled_passed"])

    def test_success_failure_and_disabled(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = pathlib.Path(tmp); profile = repo / "verify.json"
            profile.write_text(json.dumps({"schema_version": 1, "checks": [
                {"name": "pass", "argv": [sys.executable, "-c", "import sys;sys.exit(0)"]},
                {"name": "fail", "argv": [sys.executable, "-c", "import sys;sys.exit(3)"]},
                {"name": "disabled", "enabled": False, "argv": [sys.executable, "-c", "import sys;sys.exit(5)"]}]}))
            result = M.verify(profile, repo, execute=True)
            self.assertEqual([x["status"] for x in result["checks"]], ["passed", "failed", "not_run"])
            self.assertFalse(result["all_enabled_passed"])

    def test_all_enabled_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = pathlib.Path(tmp); profile = repo / "verify.json"
            profile.write_text(json.dumps({"schema_version": 1, "checks": [
                {"name": "pass", "argv": [sys.executable, "-c", "import sys;sys.exit(0)"]}]}))
            self.assertTrue(M.verify(profile, repo, execute=True)["all_enabled_passed"])

    def test_invalid_schema_and_shell_string(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = pathlib.Path(tmp); profile = repo / "verify.json"
            for body in ({"schema_version": 7, "checks": []},
                         {"schema_version": 1, "checks": [{"name": "x", "argv": "echo hi"}]},
                         {"schema_version": 1, "checks": [{"name": "x", "argv": ["python"]},
                                                           {"name": "x", "argv": ["python"]}]}):
                profile.write_text(json.dumps(body))
                with self.assertRaises(ValueError):
                    M.verify(profile, repo, execute=False)


if __name__ == "__main__":
    unittest.main()
