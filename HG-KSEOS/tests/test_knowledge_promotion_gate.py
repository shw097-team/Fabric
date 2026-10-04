from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from hg_kseos.errors import InvariantViolation
from hg_kseos.knowledge import KnowledgeFactory
from hg_kseos.spine import SharedSpine


class PromotionEvidenceGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.spine = SharedSpine(Path(self.temp.name) / "spine.db")
        self.spine.initialize()
        self.spine.create_project()
        self.knowledge = KnowledgeFactory(self.spine)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_promote_with_evidence_succeeds(self) -> None:
        result = self.knowledge.ingest_text("source.md", "Shared Spine is canonical", "A1")
        doc_id = self.knowledge.promote(result["candidate_id"], "R-VERIFY", "E-1", "Architecture")
        self.assertTrue(doc_id.startswith("DOC-"))
        with self.spine.connect() as connection:
            state = connection.execute(
                "SELECT state FROM candidates WHERE candidate_id=?", (result["candidate_id"],)
            ).fetchone()[0]
            count = connection.execute("SELECT COUNT(*) FROM knowledge_docs").fetchone()[0]
        self.assertEqual(state, "PROMOTED")
        self.assertEqual(count, 1)

    def test_promote_with_empty_evidence_raises(self) -> None:
        result = self.knowledge.ingest_text("source.md", "bounded candidate", "A1")
        with self.assertRaises(InvariantViolation) as caught:
            self.knowledge.promote(result["candidate_id"], "R-VERIFY", "", "Bad")
        self.assertEqual(str(caught.exception), "ERR_PROMOTION_EVIDENCE_REQUIRED")
        self._assert_not_published(result["candidate_id"])

    def test_promote_with_whitespace_evidence_raises(self) -> None:
        result = self.knowledge.ingest_text("source.md", "bounded candidate", "A1")
        with self.assertRaises(InvariantViolation) as caught:
            self.knowledge.promote(result["candidate_id"], "R-VERIFY", "   ", "Bad")
        self.assertEqual(str(caught.exception), "ERR_PROMOTION_EVIDENCE_REQUIRED")
        self._assert_not_published(result["candidate_id"])

    def test_self_approval_still_blocked(self) -> None:
        result = self.knowledge.ingest_text("source.md", "bounded candidate", "A1")
        with self.assertRaises(InvariantViolation) as caught:
            self.knowledge.promote(result["candidate_id"], "maker", "E-1", "Bad")
        self.assertEqual(str(caught.exception), "ERR_SELF_APPROVAL")
        self._assert_not_published(result["candidate_id"])

    def _assert_not_published(self, candidate_id: str) -> None:
        with self.spine.connect() as connection:
            state = connection.execute(
                "SELECT state FROM candidates WHERE candidate_id=?", (candidate_id,)
            ).fetchone()[0]
            count = connection.execute("SELECT COUNT(*) FROM knowledge_docs").fetchone()[0]
        self.assertEqual(state, "CANDIDATE")
        self.assertEqual(count, 0)


if __name__ == "__main__":
    unittest.main()
