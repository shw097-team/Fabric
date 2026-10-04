"""EVO-005 G2 — Canonical Evidence Graph tests (RED phase).

Nodes: Subject / Requirement / Execution / Artifact / Verification
Edges: requirement-evaluated_by-execution, execution-produced-artifact,
       artifact-about-subject, verification-checks-*, requirement-supported_by-verification

Artifact record holds full digest ONCE (artifact_id -> path/bytes/full_sha256).
Proof capsules reference requirement_id/verification_id/artifact_id only —
no digest/candidate/count duplication.
"""
from __future__ import annotations

import hashlib
import sqlite3
import tempfile
import unittest
from pathlib import Path


def fresh_db() -> Path:
    tmp = tempfile.mkdtemp(prefix="hgk-e5-")
    return Path(tmp) / "graph.db"


class EvidenceGraphTests(unittest.TestCase):
    def test_register_artifact_digest_once(self):
        from hg_kseos.evidence_graph import EvidenceGraph
        g = EvidenceGraph(fresh_db())
        p = Path(tempfile.mkdtemp()) / "raw.json"
        p.write_text('{"v": 1}', encoding="utf-8")
        art = g.register_artifact(path=str(p), producer="RUNNER")
        self.assertEqual(art["sha256"], hashlib.sha256(p.read_bytes()).hexdigest())
        # capsule references artifact_id only
        capsule = g.proof_capsule(requirement_id="R1", verification_id="V1", artifact_id=art["artifact_id"])
        self.assertNotIn("sha256", capsule)
        self.assertNotIn("bytes", capsule)

    def test_duplicate_truth_fields_rejected(self):
        from hg_kseos.evidence_graph import EvidenceGraph
        g = EvidenceGraph(fresh_db())
        # capsule with copied digest must fail validation
        ok = g.validate_capsule({"requirement_id": "R", "verification_id": "V",
                                 "artifact_id": "ART-1", "sha256": "copied"})
        self.assertFalse(ok["valid"])
        self.assertIn("duplicate", ok["reason"])

    def test_join_queries(self):
        from hg_kseos.evidence_graph import EvidenceGraph
        g = EvidenceGraph(fresh_db())
        g.register_subject("SUBJ-1", "digest-a")
        g.register_requirement("R1", scope="PRODUCT")
        g.register_execution("EX-1", requirement_id="R1", runner="RUNNER")
        p = Path(tempfile.mkdtemp()) / "a.json"
        p.write_text("{}", encoding="utf-8")
        art = g.register_artifact(path=str(p), producer="RUNNER")
        g.link_execution_produced(execution_id="EX-1", artifact_id=art["artifact_id"])
        g.link_artifact_about(artifact_id=art["artifact_id"], subject_id="SUBJ-1")
        g.register_verification("V1", requirement_id="R1", checker="INDEP", verdict="PASS")
        g.link_verification_checks(verification_id="V1", artifact_id=art["artifact_id"])
        joins = g.requirement_supported_by("R1")
        self.assertGreaterEqual(len(joins), 1)
        self.assertEqual(joins[0]["verdict"], "PASS")

    def test_no_runner_verdict_authority(self):
        from hg_kseos.evidence_graph import EvidenceGraph
        g = EvidenceGraph(fresh_db())
        # runner summaries cannot be the authority; only verification records count
        g.register_runner_summary("RUNNER", "note: pass=3 stored as execution note, not authority")
        rows = g.verification_records()
        self.assertEqual(len(rows), 0)

    def test_graph_root_digest_deterministic(self):
        from hg_kseos.evidence_graph import EvidenceGraph
        import tempfile as _tf
        p = Path(_tf.mkdtemp()) / "raw.json"
        p.write_text('{"v": 1}', encoding="utf-8")
        d1 = EvidenceGraph(fresh_db())
        d2 = EvidenceGraph(fresh_db())
        for g in (d1, d2):
            g.register_subject("S1", "digest-x")
            g.register_requirement("R1", scope="PRODUCT")
            a = g.register_artifact(path=str(p), producer="RUNNER", subject_digest="digest-x")
            g.register_verification("V1", "R1", checker="INDEP", verdict="PASS")
            g.link_verification_checks("V1", a["artifact_id"])
        self.assertEqual(d1.graph_root_digest(), d2.graph_root_digest())


if __name__ == "__main__":
    unittest.main()
