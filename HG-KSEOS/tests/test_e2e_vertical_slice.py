from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from hg_kseos.errors import AdmissionDenied
from hg_kseos.harness import Harness, HarnessAction
from hg_kseos.knowledge import KnowledgeFactory
from hg_kseos.recovery import backup_database, restore_database
from hg_kseos.release import EvidenceEnvelope, ReleaseReducer
from hg_kseos.spine import SharedSpine


class VerticalSliceTests(unittest.TestCase):
    def test_requirement_to_evidence_to_rollback_slice(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            spine = SharedSpine(root / "spine.db")
            spine.initialize()
            spine.create_project()
            spine.register_requirement(
                "REQ-VS",
                "A1#slice",
                "Candidate knowledge must not self-approve",
                "ACC-VS",
                "self approval rejected and independent approval accepted",
                "2/2",
                "candidate approves itself",
            )
            spine.acquire_lease("REQ-VS", "maker", "secret-token")
            spine.transition_requirement("REQ-VS", "FROZEN", "maker", "secret-token", 0, "E-FREEZE", "VS-1")
            spine.create_taskspec(
                "TS-VS",
                "REQ-VS",
                "Implement candidate-first promotion",
                "maker",
                root,
                {"network": "OFF", "secrets": "NONE"},
                ["positive", "negative", "rollback"],
                "EvidenceEnvelope",
            )
            worktree = root / "isolated-worktree"
            worktree.mkdir()
            spine.create_workorder("WO-VS", "TS-VS", "maker", worktree, "a" * 40)
            harness = Harness(root, root / "harness.jsonl")
            action = HarnessAction(
                action_id="HRA-VS",
                workorder_id="WO-VS",
                actor="maker",
                tool="internal",
                tool_identity="hg-kseos",
                tool_version="1",
                input_digest="a" * 64,
                side_effect_class="ISOLATED_WORKTREE_WRITE",
                filesystem_scope=(str(worktree),),
                expected_postcondition="candidate artifact exists",
                rollback="remove only candidate artifact",
                evidence_required=("candidate digest",),
                dry_run=False,
            )
            run = harness.run(action, lambda: (worktree / "candidate.txt").write_text("candidate", encoding="utf-8"))
            self.assertEqual(run["verdict"], "PASS")
            with self.assertRaises(AdmissionDenied):
                harness.preflight(HarnessAction(**(action.__dict__ | {"action_id": "HRA-NEG", "filesystem_scope": (str(root.parent / "escape"),)})))
            factory = KnowledgeFactory(spine)
            candidate = factory.ingest_text("source.md", "candidate first bounded promotion", "A1")
            factory.promote(candidate["candidate_id"], "independent-checker", "E-PROMOTE", "Candidate first")
            self.assertTrue(factory.search("bounded"))
            spine.record_workorder_result("WO-VS", "maker", "independent-checker", "PASS", ["E-TEST", "E-SECURITY"])
            spine.transition_requirement("REQ-VS", "IMPLEMENTED", "maker", "secret-token", 1, "E-IMPL", "VS-2")
            spine.transition_requirement("REQ-VS", "VERIFIED", "maker", "secret-token", 2, "E-VERIFY", "VS-3")
            backup = backup_database(spine.database, root / "backup")
            restored = restore_database(Path(backup["backup"]), backup["sha256"], root / "restore" / "spine.db")
            self.assertEqual(restored["status"], "RESTORE_READBACK_PASS")
            decision = ReleaseReducer(spine).reduce(
                EvidenceEnvelope(
                    requirements_total=1,
                    requirements_passed=1,
                    blocking_tests_passed=True,
                    security_critical=0,
                    rollback_passed=True,
                    restore_passed=True,
                    independent_passed=True,
                    provider_lifecycle_closed=True,
                    user_guide_complete=True,
                    raw_evidence_complete=True,
                    open_blocking_tt=0,
                    checker="independent-checker",
                    artifacts=("E-FREEZE", "E-IMPL", "E-VERIFY", backup["sha256"]),
                )
            )
            self.assertEqual(decision["verdict"], "HG-KSEOS_LOCAL_DELIVERY_PASS")
            spine.rollback_workorder("WO-VS", "E-ROLLBACK")
            with spine.connect() as connection:
                self.assertEqual(connection.execute("SELECT state FROM workorders WHERE workorder_id='WO-VS'").fetchone()[0], "ROLLED_BACK")


if __name__ == "__main__":
    unittest.main()
