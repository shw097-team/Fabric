"""Task-011 tests: Autonomous Project Lifecycle + Governed Evolution (L1-L4 + negatives)."""
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from hg_kseos.evolution import (EvolutionSignal, GovernedEvolutionController,
                                PROMOTION_POLICY)
from hg_kseos.lifecycle import (LIFECYCLE_STATES, ProjectLifecycleController,
                                ProjectRequest, VALID_TRANSITIONS)
from hg_kseos.observability import EventLog
from hg_kseos.spine import SharedSpine

ROOT = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")


def fresh_spine(project_id: str = "HGK-PRJ-TEST") -> tuple[Path, SharedSpine]:
    tmp = Path(tempfile.mkdtemp(prefix="hgk-t11-"))
    spine = SharedSpine(tmp / "spine.db")
    spine.initialize()
    spine.create_project(project_id)
    return tmp, spine


def boot_lifecycle(spine: SharedSpine, project_id: str = "HGK-PRJ-TEST",
                   goal: str = "Build a knowledge system with tests and acceptance") -> tuple[ProjectLifecycleController, str]:
    lc = ProjectLifecycleController(spine)
    req = ProjectRequest(goal=goal, source_paths=[], constraints=["local-first"],
                         non_goals=["no cloud"], target_root="worktrees")
    start = lc.start(req, project_id=project_id)
    lc.intake(project_id, req)
    lc.transition(project_id, "INTENT_BOUND", trigger="INTENT_ROUNDTRIP")
    lc.transition(project_id, "REQUIREMENTS_READY", trigger="REQUIREMENTS_DERIVED")
    lc.transition(project_id, "DESIGN_READY", trigger="DESIGN_COMPLETE")
    lc.plan(project_id)
    return lc, project_id


class LifecycleStateMachineTests(unittest.TestCase):
    """L1: state transitions + schema."""

    def test_states_defined(self) -> None:
        self.assertIn("PROJECT_CREATED", LIFECYCLE_STATES)
        self.assertIn("DELIVERED", LIFECYCLE_STATES)
        self.assertIn("REPAIRING", VALID_TRANSITIONS)
        self.assertIn("BLOCKED_HITL", VALID_TRANSITIONS["EXECUTING"])

    def test_illegal_transition_rejected(self) -> None:
        tmp, spine = fresh_spine()
        try:
            lc = ProjectLifecycleController(spine)
            start = lc.start(ProjectRequest(goal="g"), project_id="HGK-PRJ-TEST")
            with self.assertRaises(Exception):
                lc.transition("HGK-PRJ-TEST", "DELIVERED", trigger="JUMP")
            self.assertEqual(lc.status("HGK-PRJ-TEST")["state"], "PROJECT_CREATED")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_full_forward_path(self) -> None:
        tmp, spine = fresh_spine()
        try:
            lc, pid = boot_lifecycle(spine)
            wo = lc.admit_workorders(pid)
            self.assertEqual(wo["count"], 5)
            lc.transition(pid, "EXECUTING", trigger="WO_EXECUTE")
            lc.transition(pid, "VERIFYING", trigger="VERIFY")
            lc.transition(pid, "EVOLUTION_REVIEW", trigger="EVO_REVIEW")
            lc.transition(pid, "RELEASE_REDUCING", trigger="REDUCE")
            lc.transition(pid, "DELIVERY_READY", trigger="READY")
            # CS-A D4: pending required workorders block DELIVERED
            with self.assertRaises(Exception):
                lc.transition(pid, "DELIVERED", trigger="DELIVER")
            self.assertEqual(lc.status(pid)["state"], "DELIVERY_READY")
            # complete all workorders -> DELIVERED legal
            with spine.transaction() as c:
                c.execute("UPDATE workorders SET state='VERIFIED'")
            lc.transition(pid, "DELIVERED", trigger="DELIVER")
            self.assertEqual(lc.status(pid)["state"], "DELIVERED")
            snap = spine.snapshot()["counts"]
            self.assertEqual(snap["project_lifecycles"], 1)
            self.assertGreaterEqual(snap["project_transitions"], 8)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_repair_loop(self) -> None:
        tmp, spine = fresh_spine()
        try:
            lc, pid = boot_lifecycle(spine)
            lc.admit_workorders(pid)
            lc.transition(pid, "EXECUTING", trigger="WO_EXECUTE")
            lc.transition(pid, "VERIFYING", trigger="VERIFY")
            r = lc.begin_repair(pid)
            self.assertEqual(r["state"], "REPAIRING")
            self.assertEqual(lc.status(pid)["repair_count"], 1)
            lc.transition(pid, "EXECUTING", trigger="REPAIR_RETRY")
            st = lc.status(pid)
            self.assertEqual(st["attempts_used"], 1)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class LifecycleIntegrationTests(unittest.TestCase):
    """L2: intake/plan/workorder/checkpoint integration."""

    def test_intake_hashes_sources(self) -> None:
        tmp, spine = fresh_spine()
        try:
            src = tmp / "sources"
            src.mkdir()
            (src / "req.md").write_text("# Requirement A\n", encoding="utf-8")
            lc = ProjectLifecycleController(spine)
            req = ProjectRequest(goal="build system", source_paths=[str(src)],
                                 target_root=str(tmp / "target"))
            start = lc.start(req, project_id="HGK-PRJ-TEST")
            env = lc.intake("HGK-PRJ-TEST", req)
            self.assertEqual(env["status"], "READY")
            self.assertEqual(env["source_count"], 1)
            self.assertEqual(len(env["inventory"][0]["sha256"]), 64)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_workorders_admitted_via_spine(self) -> None:
        tmp, spine = fresh_spine()
        try:
            lc, pid = boot_lifecycle(spine)
            wo = lc.admit_workorders(pid)
            self.assertGreaterEqual(wo["count"], 4)
            with spine.connect() as c:
                n = c.execute("SELECT COUNT(*) FROM workorders").fetchone()[0]
            self.assertGreaterEqual(n, 4)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_checkpoint_resume_idempotent(self) -> None:
        tmp, spine = fresh_spine()
        try:
            lc, pid = boot_lifecycle(spine)
            lc.admit_workorders(pid)
            ck = lc.checkpoint(pid)
            res = lc.resume(pid)
            self.assertEqual(res["checkpoint_id"], ck["checkpoint_id"])
            self.assertEqual(res["payload"]["project_id"], pid)
            # stale checkpoint refused
            with spine.transaction() as c:
                c.execute("UPDATE project_lifecycles SET intent_json=? WHERE project_id=?",
                          (json.dumps({"_checkpoint": {"project_id": "OTHER"}}), pid))
            with self.assertRaises(Exception):
                lc.resume(pid, verify_hashes=True)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class EvolutionTests(unittest.TestCase):
    """L2: evolution signal/candidate pipeline."""

    def _ec(self) -> tuple[Path, SharedSpine, GovernedEvolutionController]:
        tmp, spine = fresh_spine("HGK-PRJ-EVO")
        log = EventLog(tmp / "events.jsonl")
        return tmp, spine, GovernedEvolutionController(spine, log, recurrence_threshold=2)

    def test_single_failure_not_learned(self) -> None:
        tmp, _, ec = self._ec()
        try:
            s = ec.capture_signal(EvolutionSignal("HGK-PRJ-EVO", "R1", "SKILL_GAP", "LOW", ["e1"]))
            self.assertFalse(s["candidate_worthy"])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_recurrence_triggers_candidate(self) -> None:
        tmp, _, ec = self._ec()
        try:
            ec.capture_signal(EvolutionSignal("HGK-PRJ-EVO", "R1", "SKILL_GAP", "LOW", ["e1"]))
            s2 = ec.capture_signal(EvolutionSignal("HGK-PRJ-EVO", "R2", "SKILL_GAP", "LOW", ["e2"]))
            self.assertTrue(s2["candidate_worthy"])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_fit_gap_reuse_first(self) -> None:
        tmp, _, ec = self._ec()
        try:
            fg = ec.fit_gap("SKILL_GAP")
            self.assertFalse(fg["create_new_candidate"])
            fg2 = ec.fit_gap("ARCHITECTURE_GAP")
            self.assertTrue(fg2["create_new_candidate"])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_candidate_full_pipeline(self) -> None:
        tmp, _, ec = self._ec()
        try:
            c = ec.create_candidate("HGK-PRJ-EVO", "GAP-1", "SkillCandidate", "p", "c", "g", "LOW",
                                    allowed_write_set=["skills/"])
            self.assertEqual(c["state"], "CANDIDATE")
            q = ec.qualify(c["candidate_id"], tests_pass=True, negative_pass=True, security_pass=True,
                           holdout_pass=True, nrtv_pass=True, baseline_verified=True, rollback_verified=True,
                           sandbox_path=str(tmp / "sb"))
            self.assertEqual(q["state"], "QUALIFIED")
            ic = ec.independent_check(c["candidate_id"], raw_evidence_refs=["EV-1"])
            self.assertEqual(ic["verdict"], "PASS")
            pg = ec.promotion_gate(c["candidate_id"])
            # source COV-11-06: promotion requires Human Policy Owner -> no auto-promote
            self.assertEqual(pg["state"], "PROMOTION_READY_HITL_SOURCE_REQUIRED")
            self.assertEqual(pg["source_locator"], "HG-KSEOS_P0-CIP-PACK_v2026.08.05-r2.md#COV-11-06")
            # with human approval -> promoted
            pg2 = ec.promotion_gate(c["candidate_id"], human_approval=True)
            self.assertEqual(pg2["state"], "PROMOTED")
            self.assertEqual(pg2["gate"], "HUMAN_APPROVED")
            cn = ec.canary(c["candidate_id"])
            self.assertEqual(cn["state"], "CANARY_OK")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_maker_cannot_be_checker(self) -> None:
        tmp, _, ec = self._ec()
        try:
            c = ec.create_candidate("HGK-PRJ-EVO", "GAP-1", "TestCandidate", "p", "c", "g", "LOW")
            ec.qualify(c["candidate_id"], tests_pass=True, negative_pass=True, security_pass=True,
                       holdout_pass=True, nrtv_pass=True, baseline_verified=True, rollback_verified=True)
            with self.assertRaises(Exception):
                ec.independent_check(c["candidate_id"], checker="maker")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_failed_candidate_rollback_no_contamination(self) -> None:
        tmp, _, ec = self._ec()
        try:
            c = ec.create_candidate("HGK-PRJ-EVO", "GAP-1", "SkillCandidate", "p", "c", "g", "LOW")
            q = ec.qualify(c["candidate_id"], tests_pass=False, negative_pass=True, security_pass=True,
                           holdout_pass=True, nrtv_pass=True, baseline_verified=True, rollback_verified=True)
            self.assertEqual(q["state"], "REJECTED")
            st = ec.status("HGK-PRJ-EVO")
            self.assertEqual(st["candidates_by_state"].get("REJECTED"), 1)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_authority_mutation_blocked(self) -> None:
        tmp, _, ec = self._ec()
        try:
            c = ec.create_candidate("HGK-PRJ-EVO", "GAP-1", "CodePatchCandidate", "p", "c", "g", "LOW")
            q = ec.qualify(c["candidate_id"], tests_pass=True, negative_pass=True, security_pass=True,
                           holdout_pass=True, nrtv_pass=True, baseline_verified=True, rollback_verified=True,
                           authority_mutation=True)
            self.assertEqual(q["state"], "REJECTED")
            self.assertEqual(q["reason"], "authority/evaluator mutation detected — fail closed")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_evaluator_tamper_blocked(self) -> None:
        tmp, _, ec = self._ec()
        try:
            c = ec.create_candidate("HGK-PRJ-EVO", "GAP-1", "EvaluatorCandidate", "p", "c", "g", "MEDIUM")
            q = ec.qualify(c["candidate_id"], tests_pass=True, negative_pass=True, security_pass=True,
                           holdout_pass=True, nrtv_pass=True, baseline_verified=True, rollback_verified=True,
                           evaluator_self_mutation=True)
            self.assertEqual(q["state"], "REJECTED")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_high_risk_requires_human_gate(self) -> None:
        tmp, _, ec = self._ec()
        try:
            c = ec.create_candidate("HGK-PRJ-EVO", "GAP-1", "ProviderCandidate", "p", "c", "g", "HIGH")
            ec.qualify(c["candidate_id"], tests_pass=True, negative_pass=True, security_pass=True,
                       holdout_pass=True, nrtv_pass=True, baseline_verified=True, rollback_verified=True)
            ec.independent_check(c["candidate_id"], raw_evidence_refs=["EV-1"])
            pg = ec.promotion_gate(c["candidate_id"])
            self.assertEqual(pg["state"], "PROMOTION_READY_HITL_SOURCE_REQUIRED")
            self.assertEqual(pg["human_role"], "AUTHORITY_GATE_ONLY")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_constitutional_never_auto_promotes(self) -> None:
        self.assertFalse(PROMOTION_POLICY["constitutional"]["auto_promotion"])
        self.assertEqual(PROMOTION_POLICY["constitutional"]["human_gate"], "mandatory")


class CliEntrypointTests(unittest.TestCase):
    """L3: real CLI product entrypoint."""

    def _run(self, *argv: str) -> subprocess.CompletedProcess:
        return subprocess.run([str(ROOT / ".venv/Scripts/python.exe"), "-m", "hg_kseos.cli", *argv],
                              cwd=ROOT, capture_output=True, text=True, encoding="utf-8")

    def test_project_start_cli(self) -> None:
        r = self._run("project", "start", "--goal", "build a tool with tests",
                      "--project-id", "HGK-PRJ-CLI")
        self.assertEqual(r.returncode, 0, r.stderr[-300:])
        d = json.loads(r.stdout)
        self.assertEqual(d["state"], "PROJECT_CREATED")

    def test_evolution_status_cli(self) -> None:
        r = self._run("evolution", "status")
        self.assertEqual(r.returncode, 0, r.stderr[-300:])
        d = json.loads(r.stdout)
        self.assertIn("signal_count", d)


if __name__ == "__main__":
    unittest.main()
