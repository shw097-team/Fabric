# -*- coding: utf-8 -*-
"""FDA one-active-writer lease + idempotency tests (blueprint 5.6/5.6A/5.8).
Contract: second writer DENY; hot-swap requires readback+checkpoint+known state;
stable idempotency key prevents duplicate side effect; prior-effect readback
before replay; unknown state blocks replay.
"""
import hashlib
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from fda_lease import DesktopLeaseManager, LeaseDenied, UnknownState, idempotency_key


class TestLease(unittest.TestCase):
    def test_single_writer_ok(self):
        lm = DesktopLeaseManager()
        lm.acquire("session-1", "fabric-desktop-cua")
        self.assertEqual(lm.current_writer("session-1"), "fabric-desktop-cua")

    def test_second_writer_denied(self):
        lm = DesktopLeaseManager()
        lm.acquire("session-1", "fabric-desktop-cua")
        with self.assertRaises(LeaseDenied):
            lm.acquire("session-1", "fabric-desktop-ufo2")

    def test_lease_transfer_requires_checkpoint(self):
        lm = DesktopLeaseManager()
        lm.acquire("session-1", "fabric-desktop-cua")
        # transfer without readback/checkpoint must fail
        with self.assertRaises(ValueError):
            lm.transfer("session-1", "fabric-desktop-cua", "fabric-desktop-ufo2")

    def test_hot_swap_with_readback_checkpoint(self):
        lm = DesktopLeaseManager()
        lm.acquire("session-1", "fabric-desktop-cua")
        lm.checkpoint("session-1", "chk-001", desktop_state_digest="abc123")
        lm.release("session-1", "fabric-desktop-cua")
        lm.acquire("session-1", "fabric-desktop-ufo2", after_checkpoint="chk-001")
        self.assertEqual(lm.current_writer("session-1"), "fabric-desktop-ufo2")

    def test_release_then_reacquire(self):
        lm = DesktopLeaseManager()
        lm.acquire("session-1", "fabric-desktop-cua")
        lm.release("session-1", "fabric-desktop-cua")
        lm.acquire("session-1", "fabric-desktop-ufo2")
        self.assertEqual(lm.current_writer("session-1"), "fabric-desktop-ufo2")


class TestIdempotency(unittest.TestCase):
    def test_stable_key_semantics(self):
        k1 = idempotency_key(workorder_id="WO-FDA-001", task_id="t_314a5148",
                             application_id="XQ", application_version="v1",
                             action_class="XS_COMPILE_PASS", target_identity="script-a")
        k2 = idempotency_key(workorder_id="WO-FDA-001", task_id="t_314a5148",
                             application_id="XQ", application_version="v1",
                             action_class="XS_COMPILE_PASS", target_identity="script-a")
        k3 = idempotency_key(workorder_id="WO-FDA-001", task_id="t_314a5148",
                             application_id="XQ", application_version="v1",
                             action_class="XS_COMPILE_PASS", target_identity="script-b")
        self.assertEqual(k1, k2)
        self.assertNotEqual(k1, k3)
        self.assertEqual(len(k1), 64)  # sha256 hex

    def test_prior_effect_readback_blocks_duplicate(self):
        # a prior effect receipt exists and current state confirms applied -> replay forbidden
        lm = DesktopLeaseManager()
        self.assertFalse(lm.replay_allowed(
            side_effect_class="LOCAL_REVERSIBLE",
            prior_effect_receipt_ref="receipt-1",
            current_state_confirms_applied=True))
        # no prior receipt -> replay allowed only with readback
        self.assertTrue(lm.replay_allowed(
            side_effect_class="NONE",
            prior_effect_receipt_ref=None,
            current_state_confirms_applied=False))

    def test_unknown_state_blocks_replay(self):
        lm = DesktopLeaseManager()
        with self.assertRaises(UnknownState):
            lm.replay_allowed(
                side_effect_class="LOCAL_REVERSIBLE",
                prior_effect_receipt_ref=None,
                current_state_confirms_applied=None)  # None = UNKNOWN


if __name__ == "__main__":
    unittest.main()
