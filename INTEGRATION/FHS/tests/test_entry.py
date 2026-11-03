import copy
import datetime as dt
import json
import sys
import unittest
from pathlib import Path
HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import validate_entry as nav

class RouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = nav.read_json(HERE / 'repository-map.json')

    def test_original_valid(self):
        self.assertEqual(nav.validate(self.base), [])
    def test_schema_is_v2(self):
        self.assertEqual(self.base['schema_version'],'FHS-NAV/v2')
        d=copy.deepcopy(self.base);d['schema_version']='FHS-NAV/v1'
        self.assertIn('FIELD_schema_version',nav.validate(d))
    def test_six_route_coverage(self):
        self.assertEqual(set(r['task_class'] for r in self.base['routes']), set(nav.EXPECTED_ROUTE_DETAILS))
    def test_all_six_source_readers(self):
        self.assertEqual(set(nav.NAV_READERS), set(nav.EXPECTED_ROUTE_DETAILS))
        self.assertTrue(all(v['next'] and v['reader'] for v in nav.NAV_READERS.values()))
    def test_all_reader_permissions_none(self):
        for k in nav.EXPECTED_ROUTE_DETAILS:
            r, code = nav.route_result(self.base, k)
            self.assertEqual(code, 0)
            self.assertEqual(r['effect_permission'], 'NONE')
            self.assertFalse(r['owner_ratification_verified'])
    def test_unknown_route_hold(self):
        r, code = nav.route_result(self.base, 'destroy_world')
        self.assertEqual(code, 3)
        self.assertEqual(r['status'], 'HOLD_AFFECTED_WRITE')
    def test_wrong_repo(self):
        d = copy.deepcopy(self.base);d['repositories']['hgk']['full_name']='shw097-team/Fabric'
        self.assertTrue(nav.validate(d))
        # TT-E04 and TT-E05: source writer must never move by editing route text.
        # v2: pipd_canonical's writer is SBL; moving it back to pipd or to fabric must fail.
        for task, bad_primary in (('hgk_admission','fabric'),('pipd_canonical','fabric'),('pipd_canonical','pipd')):
            mutated=copy.deepcopy(self.base)
            self.find(mutated,task)['primary_repo']=bad_primary
            self.assertTrue(nav.validate(mutated))
    def test_wrong_domain(self):
        d=copy.deepcopy(self.base);d['repositories']['hgk']['domain']='POLICY_FAR'
        self.assertTrue(nav.validate(d))
    def test_duplicate_task(self):
        d=copy.deepcopy(self.base);d['routes'].append(copy.deepcopy(d['routes'][0]));self.assertTrue(nav.validate(d))
    def test_source_ratified_smuggle(self):
        d=copy.deepcopy(self.base);d['source_state']='OWNER_RATIFIED';self.assertTrue(nav.validate(d))
    def test_unknown_repo_field(self):
        d=copy.deepcopy(self.base);d['historical_repositories']['pipd']['admitted']=True;self.assertTrue(nav.validate(d))
    def test_illegal_grant_field(self):
        d=copy.deepcopy(self.base);d['routes'][0]['grant']='repo_write';self.assertTrue(nav.validate(d))
    def test_unknown_top_field(self):
        d=copy.deepcopy(self.base);d['write_all']=True;self.assertTrue(nav.validate(d))
    def test_non_string_task(self):
        d=copy.deepcopy(self.base);d['routes'][0]['task_class']=[];self.assertTrue(nav.validate(d))
    def test_unsafe_external_repo_fetch(self):
        with self.assertRaises(ValueError):nav.fetch_main('attacker/host')
    def test_snapshot_pass_and_drift(self):
        now=dt.datetime.now(dt.timezone.utc)
        d={'schema_version':'FHS-HEAD-EXPECTATION/v1','observed_at_utc':now.isoformat(),'source_scope':'GITHUB_MAIN_ONLY','expected_heads':{k:'a'*40 for k in nav.EXPECTED_REPOS}}
        self.assertEqual(nav.validate_expected_snapshot(d,now),d['expected_heads'])
        self.assertEqual(nav.compare_heads(d['expected_heads'],{k:'a'*40 for k in nav.EXPECTED_REPOS}),[])
        mismatched={k:'a'*40 for k in nav.EXPECTED_REPOS};mismatched['fabric']='b'*40
        self.assertEqual(nav.compare_heads(d['expected_heads'],mismatched),['SOURCE_DRIFT_fabric'])
    def test_snapshot_stale(self):
        now=dt.datetime.now(dt.timezone.utc)
        d={'schema_version':'FHS-HEAD-EXPECTATION/v1','observed_at_utc':(now-dt.timedelta(hours=1)).isoformat(),'source_scope':'GITHUB_MAIN_ONLY','expected_heads':{k:'a'*40 for k in nav.EXPECTED_REPOS}}
        with self.assertRaisesRegex(ValueError,'STALE'):nav.validate_expected_snapshot(d,now)
    def test_all_twenty_one_mutations(self):
        mutations=[
          ('wrong_repo_fullname',lambda d:d['repositories']['hgk'].__setitem__('full_name','other/wrong'),False),
          ('wrong_issuer_domain',lambda d:d['repositories']['hgk'].__setitem__('domain','POLICY_FAR'),False),
          ('unknown_topkey',lambda d:d.__setitem__('spare',1),False),
          ('unknown_nested_field',lambda d:d['repositories']['hgk'].__setitem__('spare',1),False),
          ('bad_claim_cross_repo',lambda d:self.find(d,'cross_repo').__setitem__('claim','NAVIGATION_ONLY'),False),
          ('bad_claim_hermes',lambda d:self.find(d,'hermes_runtime').__setitem__('claim','NAVIGATION_ONLY'),False),
          ('bad_claim_hgk',lambda d:self.find(d,'hgk_admission').__setitem__('claim','HOST_SOURCE_READER_REQUIRED'),False),
          ('remove_fabric_consumer_from_product',lambda d:self.find(d,'sbl_product').__setitem__('affected_repos',[]),False),
          ('add_hgk_to_canonical',lambda d:self.find(d,'pipd_canonical').__setitem__('affected_repos',['fabric','hgk']),False),
          ('remove_all_cross_repo_affected',lambda d:self.find(d,'cross_repo').__setitem__('affected_repos',[]),False),
          ('remove_hgk_fabric_consumer',lambda d:self.find(d,'hgk_admission').__setitem__('affected_repos',['sbl']),False),
          ('non_string_task',lambda d:d['routes'][0].__setitem__('task_class',42),False),
          ('list_type_affected',lambda d:d['routes'][0].__setitem__('affected_repos','fabric'),False),
          ('duplicate_affected',lambda d:d['routes'][0].__setitem__('affected_repos',['fabric','fabric']),False),
          ('unarchived_historical',lambda d:d['historical_repositories']['pipd'].__setitem__('archived',False),False),
          ('authority_smuggling_field',lambda d:d['routes'][0].__setitem__('permit','GRANTED'),False),
          ('duplicate_task',lambda d:d['routes'].append(copy.deepcopy(d['routes'][0])),False),
          ('unknown_route',lambda d:d['routes'][0].__setitem__('task_class','new_task'),False),
          ('repo_identity_reorder',lambda d:d.__setitem__('repositories',dict(reversed(list(d['repositories'].items())))),True),
          ('no_first_route',lambda d:d['routes'].pop(0),False),
          ('route_extra_field',lambda d:d['routes'][0].__setitem__('writer','HGK'),False),
        ]
        self.assertEqual(len(mutations),21)
        for name,change,accept in mutations:
            with self.subTest(mutation=name):
                d=copy.deepcopy(self.base);change(d)
                self.assertEqual(nav.validate(d)==[],accept,name)
    @staticmethod
    def find(d,key):
        return next(r for r in d['routes'] if r['task_class']==key)
    # ------------------------------------------------ v2: PIPD is historical, not active
    def test_pipd_not_in_active_set(self):
        self.assertNotIn('pipd',self.base['repositories'])
        self.assertIn('pipd',self.base['historical_repositories'])
        d=copy.deepcopy(self.base);d['repositories']['pipd']={'full_name':'shw097-team/PIPD-LS-SP','default_branch':'main','domain':'CANONICAL_COMPILER_PRE_CUTOVER'}
        errors=nav.validate(d)
        self.assertIn('REPO_SET',errors);self.assertIn('REPO_REACTIVATES_HISTORICAL',errors)
    def test_pipd_historical_pointer_shape(self):
        e=self.base['historical_repositories']['pipd']
        self.assertEqual(e['role'],'HISTORICAL_CANONICAL_MOVED_TO_SBL')
        self.assertEqual(e['write_authority'],'NONE')
        self.assertIs(e['archived'],True)
    def test_no_route_targets_historical(self):
        for r in self.base['routes']:
            self.assertNotEqual(r['primary_repo'],'pipd')
            self.assertNotIn('pipd',r['affected_repos'])
        d=copy.deepcopy(self.base);self.find(d,'pipd_canonical')['primary_repo']='pipd'
        self.assertIn('ROUTE_TARGET_NOT_ACTIVE_pipd_canonical',nav.validate(d))
    def test_pipd_reactivation_rejected(self):
        d=copy.deepcopy(self.base);d['repositories']['pipd']={'full_name':'x','default_branch':'main','domain':'PRODUCT_TPM'}
        self.assertTrue(nav.validate(d))
        d=copy.deepcopy(self.base);d['repositories']['sbl']['full_name']='shw097-team/PIPD-LS-SP'
        self.assertIn('ACTIVE_SHADOWS_HISTORICAL',nav.validate(d))
    def test_historical_pointer_tampering_rejected(self):
        for field,value,error in (('full_name','other/repo','HISTORICAL_SEMANTICS_pipd'),
                                  ('role','ACTIVE','HISTORICAL_SEMANTICS_pipd'),
                                  ('archived',False,'HISTORICAL_ACTIVE_pipd'),
                                  ('write_authority','PUSH','HISTORICAL_WRITE_pipd')):
            with self.subTest(field=field):
                d=copy.deepcopy(self.base);d['historical_repositories']['pipd'][field]=value
                self.assertIn(error,nav.validate(d))
        d=copy.deepcopy(self.base);d['historical_repositories']['pipd']={'full_name':'shw097-team/PIPD-LS-SP','default_branch':'main','role':'HISTORICAL_CANONICAL_MOVED_TO_SBL','archived':True}
        self.assertIn('HISTORICAL_FIELDS_pipd',nav.validate(d))
        d=copy.deepcopy(self.base);d['historical_repositories']={}
        self.assertIn('HISTORICAL_SET',nav.validate(d))
    def test_historical_repo_never_fetched(self):
        with self.assertRaises(ValueError):nav.fetch_main('shw097-team/PIPD-LS-SP')
        now=dt.datetime.now(dt.timezone.utc)
        snap={'schema_version':'FHS-HEAD-EXPECTATION/v1','observed_at_utc':now.isoformat(),'source_scope':'GITHUB_MAIN_ONLY','expected_heads':{k:'a'*40 for k in nav.EXPECTED_REPOS}}
        snap['expected_heads']['pipd']='a'*40
        with self.assertRaisesRegex(ValueError,'EXPECTED_SNAPSHOT_REPOS'):nav.validate_expected_snapshot(snap,now)
    def test_duplicate_json_key_rejected(self):
        with self.assertRaisesRegex(ValueError,'DUPLICATE_JSON_KEY'):json.loads('{"a":1,"a":2}',object_pairs_hook=nav.no_duplicate_keys)
    def test_change_in_affected_order_rejected(self):
        d=copy.deepcopy(self.base);self.find(d,'cross_repo')['affected_repos'].reverse();self.assertTrue(nav.validate(d))
    def test_unauthorized_claim_false_bool(self):
        d=copy.deepcopy(self.base);self.find(d,'hgk_admission')['claim']=False;self.assertTrue(nav.validate(d))

if __name__=='__main__':unittest.main()
