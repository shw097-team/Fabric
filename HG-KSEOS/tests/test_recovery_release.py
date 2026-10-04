from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from hg_kseos.errors import InvariantViolation
from hg_kseos.recovery import backup_database, restore_database
from hg_kseos.release import EvidenceEnvelope, ReleaseReducer
from hg_kseos.spine import SharedSpine


def passing_envelope(**updates: object) -> EvidenceEnvelope:
    values = {
        "requirements_total": 499,
        "requirements_passed": 499,
        "blocking_tests_passed": True,
        "security_critical": 0,
        "rollback_passed": True,
        "restore_passed": True,
        "independent_passed": True,
        "provider_lifecycle_closed": True,
        "user_guide_complete": True,
        "raw_evidence_complete": True,
        "open_blocking_tt": 0,
        "checker": "R-VERIFY-CLEAN",
        "artifacts": ("manifest", "tests", "security"),
    }
    values.update(updates)
    return EvidenceEnvelope(**values)


class RecoveryReleaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.spine = SharedSpine(self.root / "spine.db")
        self.spine.initialize()
        self.spine.create_project()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_backup_restore_readback(self) -> None:
        receipt = backup_database(self.spine.database, self.root / "backups")
        restored = restore_database(Path(receipt["backup"]), receipt["sha256"], self.root / "restore" / "spine.db")
        self.assertEqual(restored["status"], "RESTORE_READBACK_PASS")

    def test_tampered_backup_rejected(self) -> None:
        receipt = backup_database(self.spine.database, self.root / "backups")
        Path(receipt["backup"]).write_bytes(b"tampered")
        with self.assertRaises(InvariantViolation):
            restore_database(Path(receipt["backup"]), receipt["sha256"], self.root / "restore.db")

    def test_restore_does_not_overwrite(self) -> None:
        receipt = backup_database(self.spine.database, self.root / "backups")
        target = self.root / "existing.db"
        target.write_text("owner data")
        with self.assertRaises(InvariantViolation):
            restore_database(Path(receipt["backup"]), receipt["sha256"], target)

    def test_release_reducer_pass(self) -> None:
        decision = ReleaseReducer(self.spine).reduce(passing_envelope())
        self.assertEqual(decision["verdict"], "HG-KSEOS_LOCAL_DELIVERY_PASS")

    def test_release_reducer_fails_closed(self) -> None:
        decision = ReleaseReducer(self.spine).reduce(
            passing_envelope(security_critical=1, independent_passed=False, open_blocking_tt=2)
        )
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")
        self.assertIn("SECURITY_CRITICAL_NONZERO", decision["reasons"])
        self.assertIn("INDEPENDENT_ACCEPTANCE_MISSING", decision["reasons"])
        self.assertIn("RELEASE_BLOCKING_TT_OPEN", decision["reasons"])


if __name__ == "__main__":
    unittest.main()

