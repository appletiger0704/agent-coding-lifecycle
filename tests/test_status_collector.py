"""Mock GitHub CLI integration tests; no network credentials required."""
import importlib.util
import json
import pathlib
import tempfile
import unittest
from unittest.mock import patch

PATH = pathlib.Path(__file__).resolve().parents[1] / 'skills' / 'agent-coding-lifecycle' / 'scripts' / 'status-validator.py'
SPEC = importlib.util.spec_from_file_location('acl_collect', PATH)
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


class CollectorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = pathlib.Path(self.tmp.name)
        (self.repo / '.git').mkdir()
        contract = self.repo / '.agent-lifecycle' / 'issues'
        contract.mkdir(parents=True)
        (contract / '123.json').write_text(json.dumps({'issue_number': 123, 'type': 'routine',
                                                         'required_checks': ['unit-tests'], 'branch': 'feat/issue-123'}))
        self.pr = {'number': 45, 'state': 'OPEN', 'mergedAt': None,
                   'headRefName': 'feat/issue-123', 'headRefOid': 'commit-b',
                   'closingIssuesReferences': [{'number': 123, 'repository': {'nameWithOwner': 'example/repo'}}],
                   'url': 'https://github.com/example/repo/pull/45'}

    def tearDown(self):
        self.tmp.cleanup()

    def command(self, args, cwd):
        if args[:3] == ['gh', 'repo', 'view'] and '--json' in args and 'nameWithOwner' in args:
            return 'example/repo'
        if args[:3] == ['gh', 'repo', 'view'] and 'defaultBranchRef' in args:
            assert args[3] == 'example/repo', args
            return 'main'
        if args[:3] == ['git', 'rev-parse', 'main']:
            return 'a' * 40
        if args[:3] == ['git', 'branch', '--show-current']:
            return 'feat/issue-123'
        if args[:3] == ['git', 'rev-parse', 'HEAD']:
            return 'commit-b'
        if args[:3] == ['git', 'status', '--porcelain=v1']:
            return ''
        if args[:3] == ['git', 'rev-list', '--count']:
            return '0' if args[3].startswith('HEAD..') else '2'
        raise AssertionError(args)

    def json_result(self, args, cwd):
        if args[:3] == ['gh', 'issue', 'view']:
            return {'number': 123, 'state': 'OPEN', 'url': 'https://github.com/example/repo/issues/123'}
        if args[:3] == ['gh', 'pr', 'list']:
            return [self.pr]
        if args[:2] == ['gh', 'api'] and '/git/ref/heads/' in args[2]:
            return {'object': {'sha': 'a' * 40}}
        if args[:2] == ['gh', 'api'] and '/check-runs' in args[2]:
            return {'total_count': 1, 'check_runs': [{'name': 'unit-tests', 'status': 'completed', 'conclusion': 'success'}]}
        raise AssertionError(args)

    def test_live_collect_and_review_gate(self):
        with patch.object(M, 'run', side_effect=self.command), patch.object(M, 'json_command', side_effect=self.json_result):
            facts = M.collect(self.repo, 123)
        self.assertEqual(facts['pull_request']['number'], 45)
        self.assertTrue(facts['validation']['verified'])
        output = M.derive(facts)
        self.assertEqual(output['stage'], 'review')
        self.assertTrue(output['blocked'])
        self.assertEqual(output['evidence']['commit_sha'], 'commit-b')

    def test_unlinked_pr_cannot_be_ignored(self):
        self.pr['closingIssuesReferences'] = []
        with patch.object(M, 'run', side_effect=self.command), patch.object(M, 'json_command', side_effect=self.json_result):
            with self.assertRaisesRegex(M.EvidenceError, 'branch_pr_not_linked_to_issue'):
                M.collect(self.repo, 123)

    def test_conflicting_issue_identity_is_rejected(self):
        def mismatch(args, cwd):
            x = self.json_result(args, cwd)
            return dict(x, number=999) if args[:3] == ['gh', 'issue', 'view'] else x
        with patch.object(M, 'run', side_effect=self.command), patch.object(M, 'json_command', side_effect=mismatch):
            with self.assertRaisesRegex(M.EvidenceError, 'issue_identity_mismatch'):
                M.collect(self.repo, 123)

    def test_ambiguous_linked_prs_fail_closed(self):
        def duplicates(args, cwd):
            x = self.json_result(args, cwd)
            return [self.pr, dict(self.pr, number=46)] if args[:3] == ['gh', 'pr', 'list'] else x
        with patch.object(M, 'run', side_effect=self.command), patch.object(M, 'json_command', side_effect=duplicates):
            with self.assertRaisesRegex(M.EvidenceError, 'ambiguous_linked_pull_requests'):
                M.collect(self.repo, 123)


    def test_wrong_branch_fails_closed(self):
        contract_file = self.repo / '.agent-lifecycle' / 'issues' / '123.json'
        contract = json.loads(contract_file.read_text())
        contract['branch'] = 'feat/issue-999'
        contract_file.write_text(json.dumps(contract))
        with patch.object(M, 'run', side_effect=self.command), patch.object(M, 'json_command', side_effect=self.json_result):
            result = M.derive(M.collect(self.repo, 123))
        self.assertEqual(result['blockers'], ['branch_issue_mismatch'])

    def test_default_branch_not_main(self):
        def other_branch(args, cwd):
            if args[:3] == ['gh', 'repo', 'view'] and 'defaultBranchRef' in args:
                return 'trunk'
            if args[:3] == ['git', 'rev-parse', 'trunk']:
                return 'a' * 40
            return self.command(args, cwd)
        with patch.object(M, 'run', side_effect=other_branch), patch.object(M, 'json_command', side_effect=self.json_result):
            result = M.collect(self.repo, 123)
        self.assertEqual(result['implementation']['default_branch'], 'trunk')

    def test_stale_default_branch_fails_closed(self):
        def stale(args, cwd):
            if args[:2] == ['gh', 'api'] and '/git/ref/heads/' in args[2]:
                return {'object': {'sha': 'b' * 40}}
            return self.json_result(args, cwd)
        with patch.object(M, 'run', side_effect=self.command), patch.object(M, 'json_command', side_effect=stale):
            result = M.derive(M.collect(self.repo, 123))
        self.assertIn('local_default_branch_not_current', result['blockers'])

    def test_incomplete_check_page_not_verified(self):
        def truncated(args, cwd):
            if args[:2] == ['gh', 'api'] and '/check-runs' in args[2]:
                return {'total_count': 101, 'check_runs': [{'name': 'unit-tests', 'status': 'completed', 'conclusion': 'success'}]}
            return self.json_result(args, cwd)
        with patch.object(M, 'run', side_effect=self.command), patch.object(M, 'json_command', side_effect=truncated):
            result = M.derive(M.collect(self.repo, 123))
        self.assertIn('ci_checks_unavailable', result['blockers'])

if __name__ == '__main__':
    unittest.main()
