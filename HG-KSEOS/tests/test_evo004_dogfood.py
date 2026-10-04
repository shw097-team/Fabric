"""EVO004 FINAL-IDENTITY — NEG-13 / NEG-14 dogfood tests (RED phase).

NEG-13: capsules exist externally (JSON) but are NOT physically embedded in
        the Final MD -> gate must FAIL.
NEG-14: mechanism (FTS/retrieval) passes on a tiny fixture while a required
        corpus family is absent -> gate must FAIL.
Also: atomic-candidate downstream enforcement (capsule bound to a different
candidate than current -> STALE).
"""
from __future__ import annotations

import unittest


class NEG13EmbeddingTests(unittest.TestCase):
    def test_external_only_capsules_fail(self):
        from hg_kseos.meta_gates import single_md_embedding_gate
        res = single_md_embedding_gate(
            required_claim_ids=["C1", "C2"],
            embedded_capsule_ids=["C1"],       # C2 missing from MD
            md_has_capsules=True)
        self.assertEqual(res["verdict"], "FAIL")
        self.assertIn("C2", res["missing_embedded"])
        self.assertIn("NEG-13", res["reasons"])

    def test_all_embedded_pass(self):
        from hg_kseos.meta_gates import single_md_embedding_gate
        res = single_md_embedding_gate(
            required_claim_ids=["C1", "C2"],
            embedded_capsule_ids=["C1", "C2"],
            md_has_capsules=True)
        self.assertEqual(res["verdict"], "PASS")

    def test_no_capsules_in_md_fails(self):
        from hg_kseos.meta_gates import single_md_embedding_gate
        res = single_md_embedding_gate(
            required_claim_ids=["C1"], embedded_capsule_ids=[],
            md_has_capsules=False)
        self.assertEqual(res["verdict"], "FAIL")
        self.assertIn("NEG-13", res["reasons"])


class NEG14CorpusTests(unittest.TestCase):
    def test_missing_required_family_fails(self):
        from hg_kseos.meta_gates import corpus_completeness_gate
        required = {"FAM-ICT-SMC", "FAM-ICT-V6", "FAM-TWICT-V3",
                    "FAM-DAYTRADE", "FAM-MARKET"}
        present = {"FAM-ICT-SMC", "FAM-ICT-V6"}   # 3 families absent
        res = corpus_completeness_gate(required, present)
        self.assertEqual(res["verdict"], "FAIL")
        self.assertEqual(len(res["missing_families"]), 3)
        self.assertIn("NEG-14", res["reasons"])

    def test_all_families_present_pass(self):
        from hg_kseos.meta_gates import corpus_completeness_gate
        required = {"FAM-ICT-SMC", "FAM-ICT-V6", "FAM-TWICT-V3",
                    "FAM-DAYTRADE", "FAM-MARKET"}
        res = corpus_completeness_gate(required, set(required))
        self.assertEqual(res["verdict"], "PASS")

    def test_tiny_fixture_not_corpus(self):
        from hg_kseos.meta_gates import corpus_completeness_gate
        required = {"FAM-ICT-SMC", "FAM-ICT-V6", "FAM-TWICT-V3",
                    "FAM-DAYTRADE", "FAM-MARKET"}
        res = corpus_completeness_gate(required, {"FAM-ICT-SMC"}, fixture_only=True)
        self.assertEqual(res["verdict"], "FAIL")
        self.assertIn("fixture_neq_corpus", res["reasons"])


class AtomicCandidateTests(unittest.TestCase):
    def test_stale_capsule_rejected(self):
        from hg_kseos.meta_gates import atomic_candidate_binding
        res = atomic_candidate_binding(
            capsule_candidate="OLD-CAND-001",
            current_candidate="NEW-CAND-002")
        self.assertEqual(res["verdict"], "STALE")
        res2 = atomic_candidate_binding(
            capsule_candidate="NEW-CAND-002",
            current_candidate="NEW-CAND-002")
        self.assertEqual(res2["verdict"], "BOUND")


if __name__ == "__main__":
    unittest.main()
