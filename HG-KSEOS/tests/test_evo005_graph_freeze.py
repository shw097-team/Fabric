"""EVO005 FINAL-GRAPH-FREEZE — graph lifecycle/freeze tests (RED phase).

G1: OPEN -> FINALIZING -> FROZEN state machine; registration allowed only in
    OPEN/authorized FINALIZING; append-after-freeze rejected; root immutable
    after freeze; one final root per generation.
G2: artifact identity uniqueness — same path+digest -> same ID; same path +
    changed digest -> new version (supersedes), never silent replace.
"""
from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path


def fresh_db() -> Path:
    return Path(tempfile.mkdtemp(prefix="hgk-e5f-")) / "graph.db"


class GraphLifecycleTests(unittest.TestCase):
    def test_lifecycle_open_finalizing_frozen(self):
        from hg_kseos.evidence_graph import EvidenceGraph
        g = EvidenceGraph(fresh_db())
        self.assertEqual(g.lifecycle_state(), "OPEN")
        g.begin_finalizing()
        self.assertEqual(g.lifecycle_state(), "FINALIZING")
        g.freeze()
        self.assertEqual(g.lifecycle_state(), "FROZEN")

    def test_append_after_freeze_rejected(self):
        from hg_kseos.evidence_graph import EvidenceGraph
        g = EvidenceGraph(fresh_db())
        g.freeze()
        p = Path(tempfile.mkdtemp()) / "late.json"
        p.write_text("{}", encoding="utf-8")
        with self.assertRaises(Exception) as ctx:
            g.register_artifact(path=str(p), producer="LATE")
        self.assertIn("FROZEN", str(ctx.exception))

    def test_one_final_root_per_generation(self):
        from hg_kseos.evidence_graph import EvidenceGraph
        g = EvidenceGraph(fresh_db())
        p = Path(tempfile.mkdtemp()) / "a.json"
        p.write_text('{"a":1}', encoding="utf-8")
        g.register_artifact(path=str(p), producer="R")
        root1 = g.freeze()
        root2 = g.graph_root_digest()
        self.assertEqual(root1, root2)
        self.assertEqual(len(g.final_roots()), 1)

    def test_generation_id(self):
        from hg_kseos.evidence_graph import EvidenceGraph
        g = EvidenceGraph(fresh_db())
        self.assertTrue(g.generation_id().startswith("GEN-"))
        g.freeze()
        self.assertEqual(g.generation_id(), g.generation_id())


class ArtifactIdentityTests(unittest.TestCase):
    def test_same_path_digest_same_id(self):
        from hg_kseos.evidence_graph import EvidenceGraph
        g = EvidenceGraph(fresh_db())
        p = Path(tempfile.mkdtemp()) / "x.json"
        p.write_text("{}", encoding="utf-8")
        a1 = g.register_artifact(path=str(p), producer="R")
        a2 = g.register_artifact(path=str(p), producer="R")
        self.assertEqual(a1["artifact_id"], a2["artifact_id"])

    def test_changed_digest_new_version(self):
        from hg_kseos.evidence_graph import EvidenceGraph
        g = EvidenceGraph(fresh_db())
        p = Path(tempfile.mkdtemp()) / "x.json"
        p.write_text("{}", encoding="utf-8")
        a1 = g.register_artifact(path=str(p), producer="R")
        p.write_text('{"v":2}', encoding="utf-8")
        a2 = g.register_artifact(path=str(p), producer="R")
        self.assertNotEqual(a1["artifact_id"], a2["artifact_id"])
        # supersedes relation recorded
        rel = g.artifact_version_relation(a1["artifact_id"], a2["artifact_id"])
        self.assertEqual(rel, "SUPERSEDED")

    def test_duplicate_path_digest_conflict_rejected(self):
        from hg_kseos.evidence_graph import EvidenceGraph
        g = EvidenceGraph(fresh_db())
        p = Path(tempfile.mkdtemp()) / "x.json"
        p.write_text("{}", encoding="utf-8")
        a1 = g.register_artifact(path=str(p), producer="R")
        # second registration with same path+digest returns same id (no conflict)
        a2 = g.register_artifact(path=str(p), producer="R")
        self.assertEqual(a1["artifact_id"], a2["artifact_id"])
        self.assertEqual(g.identity_conflicts(), 0)


if __name__ == "__main__":
    unittest.main()
