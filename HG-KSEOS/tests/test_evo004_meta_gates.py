"""EVO-004 G1/G2/G3 — monotonic requirement gate + meta-learning + evidence capsule.

TDD RED phase for three new HGK controls:
  G1 MONOTONIC_REQUIREMENT_GATE — inherited required set must never shrink
     without explicit supersession receipt.
  G2 GOVERNED_META_LEARNING — defect-class promotion to permanent invariant
     with positive+negative fixtures + regression binding.
  G3 SELF_CONTAINED_EVIDENCE — proof-capsule join; missing capsule => FAIL.
"""
from __future__ import annotations

import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from hg_kseos.spine import SharedSpine


def fresh_spine() -> SharedSpine:
    tmp = tempfile.mkdtemp(prefix="hgk-e4-")
    spine = SharedSpine(Path(tmp) / "spine.db")
    spine.initialize()
    return spine


class G1MonotonicTests(unittest.TestCase):
    """Monotonic Requirement Gate."""

    def setUp(self):
        self.spine = fresh_spine()

    def test_inherited_set_retained(self):
        from hg_kseos.meta_gates import monotonic_gate
        prev = {"REQ-A", "REQ-B", "REQ-C"}
        cur = {"REQ-A", "REQ-B", "REQ-C", "REQ-D"}
        res = monotonic_gate(prev, cur)
        self.assertEqual(res["verdict"], "PASS")
        self.assertEqual(res["dropped"], [])

    def test_dropped_requires_supersession(self):
        from hg_kseos.meta_gates import monotonic_gate
        prev = {"REQ-A", "REQ-B", "REQ-C"}
        cur = {"REQ-A", "REQ-B"}
        res = monotonic_gate(prev, cur)
        self.assertEqual(res["verdict"], "FAIL")
        self.assertEqual(res["dropped"], ["REQ-C"])
        # supersession receipt closes it
        res2 = monotonic_gate(prev, cur, superseded={"REQ-C": {"source": "SRC-X", "reason": "merged into REQ-B"}})
        self.assertEqual(res2["verdict"], "PASS")

    def test_negative_fixtures_covered(self):
        from hg_kseos.meta_gates import MONOTONIC_NEGATIVE_FIXTURES
        self.assertIn("single evidence MD", MONOTONIC_NEGATIVE_FIXTURES)
        self.assertIn("knowledge preload", MONOTONIC_NEGATIVE_FIXTURES)
        self.assertIn("user guide", MONOTONIC_NEGATIVE_FIXTURES)
        self.assertIn("full-project independent acceptance", MONOTONIC_NEGATIVE_FIXTURES)


class G2MetaLearningTests(unittest.TestCase):
    """Governed meta-learning: defect class -> permanent invariant."""

    def setUp(self):
        self.spine = fresh_spine()

    def test_defect_class_promotion(self):
        from hg_kseos.meta_gates import promote_defect_class
        res = promote_defect_class(
            defect_class="DENOMINATOR",
            invariant="required_local_scope_open must equal sum of open workorders+acceptances+capabilities",
            positive_fixture="scope>0 -> workorders>0",
            negative_fixture="scope>0 with workorders==0 -> FAIL",
            owner="lifecycle",
        )
        # DENOMINATOR is pre-seeded -> ALREADY_PROMOTED; use a fresh class
        self.assertEqual(res["verdict"], "ALREADY_PROMOTED")
        res_new = promote_defect_class(
            defect_class="TEST_FRESH_CLASS",
            invariant="fresh invariant", positive_fixture="p", negative_fixture="n",
            owner="test")
        self.assertEqual(res_new["verdict"], "PROMOTED")
        self.assertEqual(res_new["invariant_id"], "INV-TEST_FRESH_CLASS")
        # duplicate promotion rejected (idempotent)
        res2 = promote_defect_class(
            defect_class="DENOMINATOR",
            invariant="x", positive_fixture="y", negative_fixture="z", owner="lifecycle")
        self.assertEqual(res2["verdict"], "ALREADY_PROMOTED")

    def test_invariant_registry(self):
        from hg_kseos.meta_gates import INVARIANT_REGISTRY
        for req in ("DENOMINATOR", "WAVE_NEQ_PROJECT", "AUTO_LOCAL",
                    "CONDITIONAL_APPLICABILITY", "SELF_CONTAINED_EVIDENCE",
                    "PROXY_NEQ_RUNTIME", "STALE_SEAL", "PER_WO_NEQ_FULL_PROJECT",
                    "SUBAGENT_STYLE_NEQ_SUBAGENT", "EVALUATOR_MUTATION_NEQ_GCF",
                    "KNOWLEDGE_PERSISTENCE", "NAMESPACE_LEAK_DENY"):
            self.assertIn(f"INV-{req}", INVARIANT_REGISTRY, req)


class G3EvidenceCapsuleTests(unittest.TestCase):
    """Self-contained evidence: proof capsule join."""

    def test_capsule_required_fields(self):
        from hg_kseos.meta_gates import validate_proof_capsule
        ok = validate_proof_capsule({
            "requirement_id": "R1", "edge": "e", "source_locator": "s",
            "verdict": "PASS", "candidate": "c", "raw": {"path": "p", "bytes": 1,
            "sha256": "0" * 64, "key_result": "r"}, "checker": {"name": "x",
            "result": "PASS"}, "trace_id": "t"})
        self.assertTrue(ok["valid"])
        bad = validate_proof_capsule({"verdict": "PASS"})
        self.assertFalse(bad["valid"])
        self.assertIn("missing", bad["detail"])

    def test_reducer_predicates(self):
        from hg_kseos.meta_gates import evidence_reducer
        res = evidence_reducer(capsules=[], raw_path_only=0)
        self.assertEqual(res["missing_capsules"], 0)
        self.assertEqual(res["verdict"], "PASS")
        res2 = evidence_reducer(capsules=[{"verdict": "PASS"}], raw_path_only=0)
        self.assertEqual(res2["missing_capsules"], 1)
        self.assertEqual(res2["verdict"], "FAIL")


if __name__ == "__main__":
    unittest.main()
