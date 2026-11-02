import re
import unittest
from pathlib import Path
BASE = Path(__file__).resolve().parents[3]
class CIBaselineTests(unittest.TestCase):
    def test_expected_readonly_workflow(self):
        p = BASE / '.github/workflows/fhs-entry-check.yml'
        x = p.read_text('utf-8')
        self.assertIn('contents: read', x)
        self.assertNotIn('pull_request_target', x)
        self.assertIn('merge_group:', x)
        self.assertIn('persist-credentials: false', x)
        self.assertRegex(x, r'actions/checkout@[0-9a-f]{40}')
        self.assertNotIn('id-token: write', x)
        self.assertNotIn('issues: write', x)
        self.assertNotIn('pull-requests: write', x)
    def test_reader_link_no_guess(self):
        x=(BASE/'INTEGRATION/FHS/README.md').read_text('utf-8')
        for task in ('sbl_product','fabric_policy','hgk_admission','pipd_canonical','cross_repo','hermes_runtime'):
            self.assertIn('`'+task+'`',x)
        self.assertIn('MISSING: original host source link',x)
if __name__=='__main__':unittest.main()
