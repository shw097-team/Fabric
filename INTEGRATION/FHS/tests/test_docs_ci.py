import json
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
    def test_historical_pointer_documented(self):
        x=(BASE/'INTEGRATION/FHS/README.md').read_text('utf-8')
        self.assertIn('HISTORICAL_CANONICAL_MOVED_TO_SBL',x)
        self.assertIn('FHS-NAV/v2',x)
        m=json.loads((BASE/'INTEGRATION/FHS/repository-map.json').read_text('utf-8'))
        self.assertEqual(m['schema_version'],'FHS-NAV/v2')
        self.assertNotIn('pipd',m['repositories'])
        self.assertEqual(m['historical_repositories']['pipd']['write_authority'],'NONE')
        self.assertIs(m['historical_repositories']['pipd']['archived'],False)
        self.assertFalse(any(r['primary_repo']=='pipd' or 'pipd' in r['affected_repos'] for r in m['routes']))
        self.assertEqual(m['effect_permission'],'NONE')
        self.assertEqual(m['source_state'],'PROPOSED_NOT_OWNER_RATIFIED')
        self.assertEqual(m['unknown_route'],'HOLD_AFFECTED_WRITE_ONLY')
if __name__=='__main__':unittest.main()
