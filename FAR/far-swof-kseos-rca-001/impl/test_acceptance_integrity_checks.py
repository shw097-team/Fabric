#!/usr/bin/env python
"""test_acceptance_integrity_checks.py — 7 test classes for the FAR PE-HGK-SWOF-ACCEPTANCE-INTEGRITY-001
controls. Each class carries a POSITIVE (the control fires on the defect it names) and a NEGATIVE
fixture (the control does NOT fire on a legitimate artifact) — the negative half is what the challenge
lane demanded, because an over-broad predicate is worse than no predicate.

Run: python -m unittest test_acceptance_integrity_checks -v
"""
import importlib.util, json, sqlite3, tempfile, unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("aic", HERE / "acceptance_integrity_checks.py")
aic = importlib.util.module_from_spec(spec); spec.loader.exec_module(aic)
EMPTY = aic.EMPTY_SHA


class T1_CrossRoundIdentity(unittest.TestCase):
    def test_fires_on_pinned_order_id(self):
        d = tempfile.mkdtemp()
        p = Path(d, "R4_LOCAL_CLOSURE_RECEIPT.json")
        p.write_text(json.dumps({"repair_id": "SWOF-W2-CLOSURE-R4",
                                 "order_id": "SWOF-CONSTRUCTION-002-W2-REPAIR-001"}), encoding="utf-8")
        f, n = aic.c3_cross_round_identity(Path(d), round_of={"R4_LOCAL_CLOSURE_RECEIPT.json": "R4"})
        self.assertTrue(any("order_id_frozen" in x[0] for x in f), f)
        self.assertEqual(n, 1)

    def test_does_not_fire_on_exempt_or_correct(self):
        d = tempfile.mkdtemp()
        Path(d, "historical").mkdir()
        Path(d, "historical", "R4_OLD.json").write_text(json.dumps({"order_id": "X-REPAIR-001"}), encoding="utf-8")
        Path(d, "R4_GOOD.json").write_text(json.dumps({"repair_id": "SWOF-W2-CLOSURE-R4",
                                                       "order_id": "SWOF-CONSTRUCTION-002-W2-REPAIR-R4"}), encoding="utf-8")
        f, _ = aic.c3_cross_round_identity(Path(d), round_of={"R4_GOOD.json": "R4"})
        self.assertEqual(f, [], f)


class T2_HandoffSubjectEquality(unittest.TestCase):
    def test_fires_on_stale_nested_subject(self):
        rs = {"subject": {"w2_source_candidate_sha": "aaa", "w2_evidence_commit_sha": "bbb"},
              "publication_state": {"pushed": {"source": "OLD"}}}
        f = aic.c4_handoff_subject_equality(rs, {"source_candidate_sha": "aaa", "evidence_commit_sha": "bbb"})
        self.assertTrue(any("nested_subject_stale" in x[0] for x in f), f)

    def test_does_not_fire_on_sanctioned_self_referential(self):
        rs = {"subject": {"w2_source_candidate_sha": "aaa", "w2_evidence_commit_sha": "bbb"},
              "publication_state": {"status": "SELF_REFERENTIAL_SEE_OUT_OF_TREE_POST_PUBLICATION_READSET",
                                    "pushed": {"source": "aaa"}}}
        f = aic.c4_handoff_subject_equality(rs, {"source_candidate_sha": "aaa", "evidence_commit_sha": "bbb"})
        self.assertEqual(f, [], f)


class T3_DescriptorResolvability(unittest.TestCase):
    def test_fires_on_empty_sha_for_nonempty(self):
        f = aic.c5_descriptor_resolvability(
            [{"path": "a.json", "sha256": EMPTY, "bytes": 0}], lambda p: b'{"x":1}')
        self.assertTrue(any(x[0].startswith("C5.") for x in f), f)

    def test_fires_on_unresolvable_and_clean_passes(self):
        f = aic.c5_descriptor_resolvability([{"path": "gone.json", "sha256": "ab" * 32, "bytes": 3}], lambda p: None)
        self.assertTrue(any("unresolvable" in x[0] for x in f), f)
        blob = b"abc"
        import hashlib
        f2 = aic.c5_descriptor_resolvability(
            [{"path": "ok", "sha256": hashlib.sha256(blob).hexdigest(), "bytes": 3}], lambda p: blob)
        self.assertEqual(f2, [], f2)


class T4_PublicationPreflight(unittest.TestCase):
    def test_fires_on_postpub_claim_with_null_sha(self):
        f = aic.c6_publication_preflight([("pack", {"claim_ceiling": "X / NEW_EVIDENCE_COMMIT_PUBLISHED",
                                                     "w2_evidence_commit_sha": None})])
        self.assertTrue(f, f)

    def test_fires_on_published_without_checker_pass(self):
        f = aic.c6_publication_preflight([("p", {"publication_state": "PUBLISHED", "independent_receipt": {}})])
        self.assertTrue(any("published_without" in x[0] for x in f), f)

    def test_clean_artifact_passes(self):
        f = aic.c6_publication_preflight([("p", {"claim_ceiling": "LOCALLY_CLOSED",
                                                 "w2_evidence_commit_sha": None})])
        self.assertEqual(f, [], f)


class T5_MinimumMatrixCoverage(unittest.TestCase):
    def test_fires_on_missing_case(self):
        miss, total = aic.c2_minimum_matrix_coverage(["AAC1", "AAC9"], {"covered_cases": ["AAC1"]})
        self.assertEqual(total, 2)
        self.assertEqual([m[1] for m in miss], ["AAC9"])

    def test_full_coverage_passes(self):
        miss, _ = aic.c2_minimum_matrix_coverage(["AAC1"], {"covered_cases": ["AAC1"]})
        self.assertEqual(miss, [], miss)


class T6_AdmissionEventOrder(unittest.TestCase):
    def _conn(self, states):
        c = sqlite3.connect(":memory:")
        c.execute("CREATE TABLE canonical_events(event_id TEXT PRIMARY KEY, entity_type TEXT, entity_id TEXT, to_state TEXT, actor TEXT)")
        for i, s in enumerate(states):
            c.execute("INSERT INTO canonical_events VALUES(?,?,?,?,?)", (f"e{i}", "workorder", "WO-1", s, "a"))
        return c

    def test_fires_when_mutation_precedes_admission(self):
        f = aic.c7_admission_precedes_mutation(self._conn(["MUTATING", "ADMITTED"]), "WO-1")
        self.assertTrue(any("mutation_precedes_admission" in x[0] for x in f), f)

    def test_passes_when_admission_first(self):
        f = aic.c7_admission_precedes_mutation(self._conn(["ADMITTED", "MUTATING"]), "WO-1")
        self.assertFalse(any("mutation_precedes_admission" in x[0] for x in f), f)
        self.assertTrue(any("ordering_oracle" in x[0] for x in f))

    def test_reports_na_on_empty(self):
        f = aic.c7_admission_precedes_mutation(self._conn([]), "WO-1")
        self.assertTrue(any("NOT_APPLICABLE" in x[0] for x in f), f)


class T7_ContractFieldGates(unittest.TestCase):
    def test_c1_fires_when_oracle_basis_absent(self):
        f = aic.c1_oracle_basis_attribution({"verdict": "PASS"})
        self.assertTrue(any("lacks_oracle_basis" in x[0] for x in f), f)
        f2 = aic.c1_oracle_basis_attribution({"assertions": [{"id": "a1", "oracle_basis": "PI06:L9610"}]})
        self.assertEqual(f2, [], f2)

    def test_c8_fires_on_path_only_and_mismatch(self):
        f = aic.c8_compiler_identity({"compiler_root": "C:/x"}, "deadbeef")
        self.assertTrue(any("absent" in x[0] for x in f), f)
        f2 = aic.c8_compiler_identity({"compiler_identity_digest": "aaaa"}, "bbbb")
        self.assertTrue(any("mismatch" in x[0] for x in f2), f2)
        f3 = aic.c8_compiler_identity({"compiler_identity_digest": "same"}, "same")
        self.assertEqual(f3, [], f3)


class T8_HardeningAgainstIndependentChecker(unittest.TestCase):
    """Regression tests encoding the four over-breadth counterexamples and the vacuity gap that an
    independent VERIFY_ONLY checker demonstrated against an earlier revision. Each MUST stay fixed."""

    # --- vacuity: a check that cannot run must say so, never silently pass ---
    def test_no_silent_clean_on_unrunnable_inputs(self):
        self.assertTrue(aic.c1_oracle_basis_attribution({"assertions": []}), "C1 empty must NOT_APPLICABLE")
        self.assertIn("NOT_APPLICABLE", aic.c2_minimum_matrix_coverage([], {})[0][0][0], "C2 no-matrix")
        self.assertIn("NOT_APPLICABLE", aic.c3_cross_round_identity(Path(tempfile.mkdtemp()))[0][0][0])
        self.assertIn("NOT_APPLICABLE", aic.c4_handoff_subject_equality({}, {})[0][0])
        self.assertIn("NOT_APPLICABLE", aic.c5_descriptor_resolvability([], lambda p: None)[0][0])
        self.assertIn("NOT_APPLICABLE", aic.c6_publication_preflight([])[0][0])

    # --- over-breadth 1: a ceiling that NEGATES the token must not be read as asserting it ---
    def test_c6_negated_ceiling_does_not_fire(self):
        f = aic.c6_publication_preflight([("p", {"claim_ceiling": "LOCAL_ONLY; MUST_NOT_CLAIM_NEW_EVIDENCE_COMMIT_PUBLISHED",
                                                 "w2_evidence_commit_sha": None})])
        self.assertEqual(f, [], f)

    # --- over-breadth 2: a declared carried/immutable predecessor is exempt ---
    def test_c3_declared_carried_is_exempt(self):
        d = tempfile.mkdtemp()
        Path(d, "R4_APPLY_RECEIPT.json").write_text(json.dumps(
            {"repair_id": "SWOF-W2-CLOSURE-R4", "order_id": "SWOF-CONSTRUCTION-002-W2-REPAIR-001",
             "carried": True}), encoding="utf-8")
        f, _ = aic.c3_cross_round_identity(Path(d), round_of={"R4_APPLY_RECEIPT.json": "R4"})
        self.assertEqual(f, [], f)

    # --- over-breadth 3: a lawful out-of-tree pushed.source must not false-positive ---
    def test_c4_lawful_out_of_tree_source_ok(self):
        rs = {"subject": {"w2_source_candidate_sha": "aaa", "w2_evidence_commit_sha": "bbb"},
              "publication_state": {"status": "PUBLISHED", "pushed": {"source": "bbb"}}}
        f = aic.c4_handoff_subject_equality(rs, {"source_candidate_sha": "aaa", "evidence_commit_sha": "bbb"})
        self.assertEqual(f, [], f)

    # --- over-breadth 4: the PASS receipt may be carried under a canonical alias key ---
    def test_c6_receipt_alias_key_accepted(self):
        f = aic.c6_publication_preflight([("p", {"publication_state": "PUBLISHED",
                                                 "checker_receipt": {"verdict": "PASS"}})])
        self.assertEqual(f, [], f)

    # --- false NEGATIVE: prose mention must NOT count as coverage ---
    def test_c2_prose_mention_is_not_coverage(self):
        missing, _ = aic.c2_minimum_matrix_coverage(["AAC9"], {"note": "no such case; see AAC9 discussion"})
        self.assertTrue(missing and "NOT_APPLICABLE" in missing[0][0], missing)


if __name__ == "__main__":
    unittest.main(verbosity=2)
