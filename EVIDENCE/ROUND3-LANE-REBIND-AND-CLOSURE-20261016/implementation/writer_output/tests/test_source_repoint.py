from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from hg_kseos.errors import InvariantViolation
from hg_kseos.knowledge import KnowledgeFactory
from hg_kseos.spine import SharedSpine
from hg_kseos.util import sha256_text

# HGK-EBC-SOURCE-REPOINT-001
# A canonical source may move on disk without its CONTENT changing. Re-pointing the
# `sources.canonical_path` pointer must be a typed, evidence-bound, transactional
# transition -- never a direct SQL UPDATE (consumers are forbidden to bypass the API).

ORIGINAL = "Shared Spine is canonical\n"
RANK = "A1"


class SourceRepointTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.spine = SharedSpine(root / "spine.db")
        self.spine.initialize()
        self.spine.create_project()
        self.knowledge = KnowledgeFactory(self.spine)
        # original ingested source
        rel_old = root / "old" / "source.md"
        rel_old.parent.mkdir(parents=True, exist_ok=True)
        rel_old.write_bytes(ORIGINAL.encode("utf-8"))
        res = self.knowledge.ingest_text(str(rel_old), ORIGINAL, RANK)
        self.source_id = res["source_id"]
        self.old_path = str(rel_old)
        # recorded evidence ref (repoint must never produce an orphan verdict)
        self.spine.register_evidence(
            "EV-REPOINT-1", "repoint", str(rel_old), sha256_text(ORIGINAL), "R-MAKER"
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _moved_copy(self, name="source.md", body=ORIGINAL) -> str:
        p = Path(self.temp.name) / "new" / name
        p.parent.mkdir(parents=True, exist_ok=True)
        # write BYTES: Path.write_text() would translate \n -> \r\n on Windows and change the digest
        p.write_bytes(body.encode("utf-8"))
        return str(p)

    # --- positive ---------------------------------------------------------
    def test_repoint_updates_pointer_and_emits_event(self) -> None:
        new_path = self._moved_copy()
        out = self.knowledge.repoint_source(
            self.source_id, new_path, actor="R-MAKER", evidence_ref="EV-REPOINT-1"
        )
        self.assertFalse(out["idempotent_replay"])
        self.assertEqual(out["from_path"], self.old_path)
        self.assertEqual(out["to_path"], new_path)
        self.assertTrue(out["event_id"].startswith("EVT-"))
        with self.spine.connect() as c:
            row = c.execute(
                "SELECT canonical_path,status FROM sources WHERE source_id=?", (self.source_id,)
            ).fetchone()
            self.assertEqual(row["canonical_path"], new_path)
            self.assertEqual(row["status"], "ACTIVE")  # repoint is a pointer move, not a lifecycle change
            n = c.execute(
                "SELECT COUNT(*) FROM canonical_events WHERE entity_id=? AND entity_type='source'",
                (self.source_id,),
            ).fetchone()[0]
            self.assertEqual(n, 1)

    def test_repoint_is_idempotent_on_identical_replay(self) -> None:
        new_path = self._moved_copy()
        self.knowledge.repoint_source(
            self.source_id, new_path, actor="R-MAKER", evidence_ref="EV-REPOINT-1"
        )
        again = self.knowledge.repoint_source(
            self.source_id, new_path, actor="R-MAKER", evidence_ref="EV-REPOINT-1"
        )
        self.assertTrue(again["idempotent_replay"])
        with self.spine.connect() as c:
            n = c.execute(
                "SELECT COUNT(*) FROM canonical_events WHERE entity_id=? AND entity_type='source'",
                (self.source_id,),
            ).fetchone()[0]
            self.assertEqual(n, 1)  # replay must not append a second event

    # --- negatives (fail-closed) -----------------------------------------
    def test_missing_target_file_fails_closed(self) -> None:
        with self.assertRaises(InvariantViolation) as ctx:
            self.knowledge.repoint_source(
                self.source_id,
                str(Path(self.temp.name) / "does-not-exist.md"),
                actor="R-MAKER",
                evidence_ref="EV-REPOINT-1",
            )
        self.assertIn("ERR_REPOINT_PATH_MISSING", str(ctx.exception))

    def test_content_drift_fails_closed(self) -> None:
        drifted = self._moved_copy(body="Shared Spine is canonical\nTAMPERED\n")
        with self.assertRaises(InvariantViolation) as ctx:
            self.knowledge.repoint_source(
                self.source_id, drifted, actor="R-MAKER", evidence_ref="EV-REPOINT-1"
            )
        self.assertIn("ERR_REPOINT_SHA_DRIFT", str(ctx.exception))

    def test_unknown_source_fails_closed(self) -> None:
        with self.assertRaises(InvariantViolation) as ctx:
            self.knowledge.repoint_source(
                "SRC-nope", self._moved_copy(), actor="R-MAKER", evidence_ref="EV-REPOINT-1"
            )
        self.assertIn("ERR_REPOINT_UNKNOWN_SOURCE", str(ctx.exception))

    def test_withdrawn_source_fails_closed(self) -> None:
        self.knowledge.withdraw_source(self.source_id)
        with self.assertRaises(InvariantViolation) as ctx:
            self.knowledge.repoint_source(
                self.source_id, self._moved_copy(), actor="R-MAKER", evidence_ref="EV-REPOINT-1"
            )
        self.assertIn("ERR_REPOINT_SOURCE_STATE", str(ctx.exception))

    def test_unregistered_evidence_fails_closed(self) -> None:
        with self.assertRaises(InvariantViolation) as ctx:
            self.knowledge.repoint_source(
                self.source_id, self._moved_copy(), actor="R-MAKER", evidence_ref="EV-NOT-REGISTERED"
            )
        self.assertIn("ERR_REPOINT_EVIDENCE_UNREGISTERED", str(ctx.exception))

    def test_blank_actor_fails_closed(self) -> None:
        with self.assertRaises(InvariantViolation) as ctx:
            self.knowledge.repoint_source(
                self.source_id, self._moved_copy(), actor="  ", evidence_ref="EV-REPOINT-1"
            )
        self.assertIn("ERR_REPOINT_ACTOR_MISSING", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
