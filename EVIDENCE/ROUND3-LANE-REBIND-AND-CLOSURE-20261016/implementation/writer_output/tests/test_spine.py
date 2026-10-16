from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from hg_kseos.errors import InvariantViolation, LeaseConflict, StaleState
from hg_kseos.spine import SharedSpine


class SharedSpineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.spine = SharedSpine(self.root / "spine.db")
        self.spine.initialize()
        self.spine.create_project()
        self.spine.register_requirement(
            "REQ-T1", "source#1", "Preserve one Product Root", "ACC-T1", "root count is one", "1", "second root"
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def lease(self, holder: str = "maker", token: str = "token") -> None:
        self.spine.acquire_lease("REQ-T1", holder, token)

    def test_illegal_transition_is_rejected(self) -> None:
        self.lease()
        with self.assertRaises(InvariantViolation):
            self.spine.transition_requirement("REQ-T1", "IMPLEMENTED", "maker", "token", 0, "E1", "K1")

    def test_transition_and_idempotent_replay(self) -> None:
        self.lease()
        first = self.spine.transition_requirement("REQ-T1", "FROZEN", "maker", "token", 0, "E1", "K1")
        replay = self.spine.transition_requirement("REQ-T1", "FROZEN", "maker", "token", 0, "E1", "K1")
        self.assertEqual(first["event_id"], replay["event_id"])
        self.assertTrue(replay["idempotent_replay"])

    def test_stale_version_is_rejected(self) -> None:
        self.lease()
        self.spine.transition_requirement("REQ-T1", "FROZEN", "maker", "token", 0, "E1", "K1")
        with self.assertRaises(StaleState):
            self.spine.transition_requirement("REQ-T1", "IMPLEMENTED", "maker", "token", 0, "E2", "K2")

    def test_dual_writer_is_rejected(self) -> None:
        self.lease("maker-a", "a")
        with self.assertRaises(LeaseConflict):
            self.spine.acquire_lease("REQ-T1", "maker-b", "b")

    def test_wrong_lease_token_is_rejected(self) -> None:
        self.lease()
        with self.assertRaises(LeaseConflict):
            self.spine.transition_requirement("REQ-T1", "FROZEN", "maker", "wrong", 0, "E1", "K1")

    def test_taskspec_requires_frozen_requirement(self) -> None:
        with self.assertRaises(InvariantViolation):
            self.spine.create_taskspec(
                "TS-1", "REQ-T1", "Implement", "maker", self.root, {"network": "OFF"}, ["unit"], "evidence"
            )

    def test_taskspec_materializes_after_freeze(self) -> None:
        self.lease()
        self.spine.transition_requirement("REQ-T1", "FROZEN", "maker", "token", 0, "E1", "K1")
        self.spine.create_taskspec(
            "TS-1", "REQ-T1", "Implement", "maker", self.root, {"network": "OFF"}, ["unit"], "evidence"
        )
        self.assertEqual(self.spine.snapshot()["counts"]["taskspecs"], 1)

    def test_critical_requirement_field_is_mandatory(self) -> None:
        with self.assertRaises(InvariantViolation):
            self.spine.register_requirement("REQ-X", "", "body", "ACC-X", "oracle", "1", "negative")

    def test_tt_open_and_close(self) -> None:
        self.spine.open_tt("TT-1", "blocked", "owner", True, "supply evidence")
        self.assertEqual(self.spine.snapshot()["open_blocking_tt"], 1)
        self.spine.close_tt("TT-1", "E-TT")
        self.assertEqual(self.spine.snapshot()["open_blocking_tt"], 0)


if __name__ == "__main__":
    unittest.main()

