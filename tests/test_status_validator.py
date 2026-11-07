"""Offline positive/negative fixtures for deterministic state policy."""
import importlib.util
import pathlib
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / 'scripts' / 'status-validator.py'
SPEC = importlib.util.spec_from_file_location('lifecycle_status', SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def facts(kind='routine'):
    return {
        'source': 'github_git_live',
        'issue': {'number': 123, 'state': 'OPEN', 'verified': True},
        'contract': {'exists': True, 'type': kind},
        'spec': {'id': 'issue-123', 'ready': True},
        'adr': {'items': [{'path': 'docs/adr/001.md', 'status': 'ACCEPTED'}]} if kind == 'architecture' else {'items': []},
        'implementation': {'branch': 'feat/issue-123', 'head_sha': 'sha-b', 'ahead': 0, 'dirty': False},
        'pull_request': None,
        'validation': {'required_checks': ['unit-tests'], 'verified': True,
                       'checks': [{'name': 'unit-tests', 'conclusion': 'success', 'status': 'completed'}]},
    }


class PolicyTests(unittest.TestCase):
    def assert_decision(self, data, stage, action, blocked=False):
        result = MODULE.derive(data)
        self.assertEqual((result['stage'], result['next_action'], result['blocked']), (stage, action, blocked), result)

    def test_no_authority(self):
        for source in (None, 'fixture', 'agent_claim'):
            with self.subTest(source=source):
                f = facts(); f['source'] = source
                self.assert_decision(f, 'unknown', 'verify_evidence', True)

    def test_missing_issue(self):
        f = facts(); f['issue']['verified'] = False
        self.assert_decision(f, 'unknown', 'verify_evidence', True)

    def test_missing_contract(self):
        f = facts(); f['contract']['exists'] = False
        self.assert_decision(f, 'issue', 'define_issue_contract', True)

    def test_invalid_contract(self):
        f = facts(); f['contract']['type'] = 'unexpected'
        self.assert_decision(f, 'issue', 'define_issue_contract', True)

    def test_closed_issue_without_merge(self):
        f = facts(); f['issue']['state'] = 'CLOSED'
        self.assert_decision(f, 'unknown', 'resolve_closed_issue', True)

    def test_feature_missing_spec_link(self):
        f = facts('feature'); f['spec']['id'] = None
        self.assert_decision(f, 'openspec', 'link_spec', True)

    def test_feature_missing_spec_files(self):
        f = facts('feature'); f['spec']['ready'] = False
        self.assert_decision(f, 'openspec', 'prepare_spec')

    def test_architecture_missing_adr(self):
        f = facts('architecture'); f['adr']['items'] = []
        self.assert_decision(f, 'adr', 'propose_adr')

    def test_adr_never_implicitly_approved(self):
        for s in ('PROPOSED', 'REJECTED', 'SUPERSEDED', 'UNKNOWN', 'MISSING'):
            with self.subTest(status=s):
                f = facts('architecture'); f['adr']['items'][0]['status'] = s
                self.assert_decision(f, 'adr', 'await_human_adr_approval', True)

    def test_implementation_empty(self):
        self.assert_decision(facts(), 'implement', 'implement_change')

    def test_dirty_worktree(self):
        f = facts(); f['implementation']['dirty'] = True
        self.assert_decision(f, 'implementation', 'review_uncommitted_changes', True)

    def test_branch_history_missing(self):
        f = facts(); f['implementation']['ahead'] = None
        self.assert_decision(f, 'implementation', 'verify_branch_history', True)

    def test_ready_pr(self):
        f = facts(); f['implementation']['ahead'] = 3
        self.assert_decision(f, 'pr', 'prepare_pull_request')

    def test_pr_closed_without_merge(self):
        f = facts(); f['pull_request'] = {'number': 4, 'state': 'CLOSED', 'merged_at': None}
        self.assert_decision(f, 'unknown', 'inspect_pr', True)

    def test_pr_needs_required_checks(self):
        f = facts(); f['pull_request'] = {'number': 4, 'state': 'OPEN', 'merged_at': None}
        f['validation']['required_checks'] = []
        self.assert_decision(f, 'validation', 'configure_required_checks', True)

    def test_pr_ci_unavailable(self):
        f = facts(); f['pull_request'] = {'number': 4, 'state': 'OPEN', 'merged_at': None}
        f['validation']['verified'] = False
        self.assert_decision(f, 'validation', 'verify_ci_checks', True)

    def test_pr_check_missing_or_failing(self):
        for case in ([], [{'name': 'unit-tests', 'conclusion': 'failure', 'status': 'completed'}],
                     [{'name': 'unit-tests', 'conclusion': 'success', 'status': 'in_progress'}]):
            with self.subTest(checks=case):
                f = facts(); f['pull_request'] = {'number': 4, 'state': 'OPEN', 'merged_at': None}
                f['validation']['checks'] = case
                self.assert_decision(f, 'validation', 'fix_or_run_tests', True)

    def test_pr_green_requires_human_review(self):
        f = facts(); f['pull_request'] = {'number': 4, 'state': 'OPEN', 'merged_at': None}
        self.assert_decision(f, 'review', 'await_human_review', True)

    def test_stale_branch(self):
        f = facts(); f['pull_request'] = {'number': 4, 'state': 'OPEN', 'merged_at': None, 'head_ref': 'feat/issue-123', 'head_sha': 'sha-a'}
        self.assert_decision(f, 'unknown', 'sync_branch', True)

    def test_merged_pr(self):
        f = facts(); f['pull_request'] = {'number': 4, 'state': 'MERGED', 'merged_at': '2026-11-07T10:00:00Z'}
        self.assert_decision(f, 'close', 'verify_and_close')

    def test_adr_parser(self):
        examples = [('## Status\n\nAccepted\n', 'ACCEPTED'),
                    ('- **Status:** Proposed\n', 'PROPOSED'),
                    ('## Status\nSuperseded by #2\n', 'SUPERSEDED'),
                    ('This contains Accepted in body only', 'UNKNOWN')]
        with tempfile.TemporaryDirectory() as tmp:
            for i, (contents, expected) in enumerate(examples):
                path = pathlib.Path(tmp) / f'{i}.md'
                path.write_text(contents)
                self.assertEqual(MODULE.adr_status(path), expected)


if __name__ == '__main__':
    unittest.main()
