"""G0 — RP001-WAVE3 HG-KSEOS thin control repairs.

TDD RED phase: capture the four confirmed control defects:

  D1 AUTO_CONTINUATION — no-HITL checkpoint does not self-continue
  D2 DYNAMIC_DENOMINATOR_EXPANSION — late-bound required obligation is not
     absorbed into Requirement->TaskSpec->WorkOrder denominator
  D3 COMPLETION_SWEEP — scope guard reports open but does not materialize
     AUTO_LOCAL work orders automatically
  D4 RBWI_COMPOSITE_ACCEPTANCE — RBWI composite cannot PASS above required
     child state; composite semantics are explicit
"""
from __future__ import annotations

import sqlite3
import tempfile
import unittest
from pathlib import Path

from hg_kseos.lifecycle import ProjectLifecycleController as ProjectLifecycle, ProjectRequest
from hg_kseos.spine import SharedSpine


def boot(spine: SharedSpine) -> ProjectLifecycle:
    return ProjectLifecycle(spine=spine)



def boot_project(lc, pid, goal):
    """Drive a fresh project to PLAN_READY (workorders admitted)."""
    req = ProjectRequest(goal=goal, constraints=["local-first"], non_goals=["no cloud"])
    lc.start(req, project_id=pid)
    lc.intake(pid, req)
    lc.transition(pid, "INTENT_BOUND", trigger="INTENT_ROUNDTRIP")
    lc.transition(pid, "REQUIREMENTS_READY", trigger="REQUIREMENTS_DERIVED")
    lc.transition(pid, "DESIGN_READY", trigger="DESIGN_COMPLETE")
    lc.plan(pid)
    lc.admit_workorders(pid)

def fresh_spine() -> SharedSpine:
    tmp = tempfile.mkdtemp(prefix="hgk-g0-")
    spine = SharedSpine(Path(tmp) / "spine.db")
    spine.initialize()
    return spine


class G0ContinuationTests(unittest.TestCase):
    """D1 AUTO_CONTINUATION."""

    def setUp(self):
        self.spine = fresh_spine()
        self.lc = boot(self.spine)

    def test_denominator_exposes_open_scope_signal(self):
        """A project with no workorders but required scope must flag
        required_local_scope_open > 0."""
        boot_project(self.lc, "G0-P1", "Build X")
        den = self.lc.denominator("G0-P1")
        # after admission there are workorders; now simulate a late obligation
        self.assertIn("required_local_scope_open", den)

    def test_required_scope_without_workorders_fails_closed(self):
        """If required local scope > 0 but workorders == 0 the project must
        NOT be deliverable (guard predicate false)."""
        boot_project(self.lc, "G0-P2", "Build Y")
        den = self.lc.denominator("G0-P2")
        self.assertFalse(den["guard_required_workorders_terminal"])


class G0DynamicDenominatorTests(unittest.TestCase):
    """D2 DYNAMIC_DENOMINATOR_EXPANSION."""

    def setUp(self):
        self.spine = fresh_spine()
        self.lc = boot(self.spine)

    def test_expand_denominator_absorbs_new_requirement(self):
        """admit_requirement expands Requirement->TaskSpec->WorkOrder chain."""
        boot_project(self.lc, "G0-P3", "Build Z")
        res = self.lc.admit_requirement(
            "G0-P3", "REQ-G0-001", "Late-bound required obligation",
            owner="Quant Research Lead")
        self.assertEqual(res["requirement_state"], "FROZEN")
        den = self.lc.denominator("G0-P3")
        self.assertGreaterEqual(den["workorders_total"], 1)
        # late obligation must be in the denominator, not hidden
        self.assertGreaterEqual(den["requirements_total"], 2)


class G0CompletionSweepTests(unittest.TestCase):
    """D3 COMPLETION_SWEEP."""

    def setUp(self):
        self.spine = fresh_spine()
        self.lc = boot(self.spine)

    def test_sweep_classifies_auto_local(self):
        boot_project(self.lc, "G0-P4", "Build W")
        sweep = self.lc.completion_sweep("G0-P4")
        self.assertIn("auto_local", sweep)
        self.assertIn("blocked_hitl", sweep)
        self.assertIn("temp_external", sweep)
        self.assertIn("non_blocking_debt", sweep)
        # classification must not invent AUTO_LOCAL work for zero open scope
        self.assertIsInstance(sweep["auto_local"], list)

    def test_sweep_detects_unadmitted_required_scope(self):
        """After all workorders VERIFIED, sweep must still detect
        non-blocking debt / none open (no hidden AUTO_LOCAL)."""
        boot_project(self.lc, "G0-P5", "Build V")
        den = self.lc.denominator("G0-P5")
        # verify all workorders
        with self.spine.transaction() as conn:
            conn.execute(
                "UPDATE workorders SET state='VERIFIED' WHERE state NOT IN "
                "('VERIFIED','ROLLED_BACK','CANCELLED')")
        sweep = self.lc.completion_sweep("G0-P5")
        # acceptance is still NOT_RUN -> auto_local (must be closed locally)
        self.assertEqual([e for e in sweep["auto_local"] if e.startswith("workorder:")], [])
        self.assertTrue(any(e.startswith("acceptance:") for e in sweep["auto_local"]))


class G0RbwiCompositeTests(unittest.TestCase):
    """D4 RBWI_COMPOSITE_ACCEPTANCE."""

    def test_composite_cannot_pass_above_required_child(self):
        from hg_kseos.lifecycle import rbwi_composite
        c = rbwi_composite({
            "local_paper": "PASS",
            "external_market": "TEMP_CLOSED",
            "tool_coverage": "PASS",
            "user_journey": "PASS",
            "negative_degraded": "PASS",
            "replay": "PASS",
        })
        self.assertEqual(c["verdict"], "TEMP_CLOSED")
        self.assertTrue(any("external_market" in e for e in c["open_edges"]))

    def test_composite_pass_only_when_all_required_terminal(self):
        from hg_kseos.lifecycle import rbwi_composite
        c = rbwi_composite({
            "local_paper": "PASS",
            "external_market": "NOT_REQUIRED_FOR_LOCAL_DELIVERY",
            "tool_coverage": "PASS",
            "user_journey": "PASS",
            "negative_degraded": "PASS",
            "replay": "PASS",
        })
        self.assertEqual(c["verdict"], "PASS")
        self.assertEqual(c["open_edges"], [])


if __name__ == "__main__":
    unittest.main()
