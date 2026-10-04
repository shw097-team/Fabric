"""Deterministic unit tests for far_watchdog (stdlib unittest only)."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import far_watchdog  # noqa: E402


class FarWatchdogTests(unittest.TestCase):

    def test_identical_action_repeat_aborts(self):
        watchdog = far_watchdog.ActionWatchdog()
        for _ in range(4):
            watchdog.record_action("new_candidate_artifact_digest")
        status = watchdog.check()
        self.assertTrue(status["identical_action_exceeded"])
        self.assertEqual(watchdog.verdict(), "FAR_ABORT_NO_PROGRESS")

    def test_no_progress_cycles_aborts(self):
        watchdog = far_watchdog.ActionWatchdog()
        watchdog.record_action("noop_signal_1")
        watchdog.record_action("noop_signal_2")
        watchdog.record_action("noop_signal_3")
        status = watchdog.check()
        self.assertTrue(status["no_progress_exceeded"])
        self.assertEqual(watchdog.verdict(), "FAR_ABORT_NO_PROGRESS")

    def test_same_failure_twice_stops(self):
        watchdog = far_watchdog.ActionWatchdog()
        watchdog.record_failure("prime:acp_timeout")
        watchdog.record_failure("prime:acp_timeout")
        status = watchdog.check()
        self.assertTrue(status["same_failure_exceeded"])
        self.assertEqual(watchdog.verdict(), "FAR_ABORT_NO_PROGRESS")

    def test_budget_exhaustion_terminal(self):
        guard = far_watchdog.BudgetGuard(wall_clock_seconds=0.0)
        status = guard.check()
        self.assertTrue(status["wall_clock_exceeded"])
        self.assertEqual(guard.terminal(), "FAR_ABORT_BUDGET")

    def test_progress_class_whitelist(self):
        progress = far_watchdog.VerifiedProgress()
        for signature in far_watchdog.VerifiedProgress.PROGRESS_CLASSES:
            self.assertTrue(progress.is_progress(signature))
        self.assertFalse(progress.is_progress("file_touched_no_evidence"))
        self.assertFalse(progress.is_progress("anything_else"))


if __name__ == "__main__":
    unittest.main()
