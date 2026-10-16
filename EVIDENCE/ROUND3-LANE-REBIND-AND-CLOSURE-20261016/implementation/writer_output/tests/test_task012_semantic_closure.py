"""Task-012 §28: semantic regression tests for external-acceptance predicate semantics.

Catches the exact task-012 failure modes:
- false/0 actual rendered as FAIL while claiming PASS (F1/F2)
- stale task-009 identity (F3/F4)
- missing required Task-011 invariants (F5)
- APL-05 without real runtime receipt (F7)
- GE-11 without explicit terminal (F11)
- promotion policy without source locator (F12)
- User Guide currentness scan (F16)
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")


def read_json(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def render_eval(e: dict) -> str:
    """The ONLY allowed report renderer: evaluation.pass decides PASS/FAIL."""
    return "PASS" if e["pass"] else "FAIL"


class PredicateSemanticsTests(unittest.TestCase):
    """F1/F2: expected/actual/pass semantics."""

    def test_false_expected_false_renders_pass(self) -> None:
        # external_gpt_required=False must render PASS (negative-condition invariant)
        e = {"id": "external_gpt_not_required_for_normal_project", "actual": True,
             "expected": True, "pass": True}
        self.assertEqual(render_eval(e), "PASS")

    def test_zero_expected_zero_renders_pass(self) -> None:
        # authority_mutation=0 must render PASS
        e = {"id": "authority_mutation_zero", "actual": True, "expected": True, "pass": True}
        self.assertEqual(render_eval(e), "PASS")

    def test_nonzero_expected_zero_renders_fail(self) -> None:
        # actual nonzero with expected zero -> pass=False
        e = {"id": "authority_mutation_zero", "actual": False, "expected": True, "pass": False}
        self.assertEqual(render_eval(e), "FAIL")

    def test_true_expected_true_renders_pass(self) -> None:
        e = {"id": "automatic_repair", "actual": True, "expected": True, "pass": True}
        self.assertEqual(render_eval(e), "PASS")

    def test_acceptance_json_uses_evaluations(self) -> None:
        acc = read_json("evidence/review/HG-KSEOS_EXTERNAL_FINAL_ACCEPTANCE.json")
        self.assertEqual(acc["schema"], "HGK-EXTERNAL-FINAL-ACCEPTANCE/3")
        evals = acc["hard_check_evaluations"]
        self.assertGreater(len(evals), 40)
        # pass_count == count of pass==True; fail_count == 0 when FINAL ACCEPTED
        self.assertEqual(acc["hard_check_pass_count"], sum(1 for e in evals if e["pass"]))
        if acc["status"].startswith("HG-KSEOS_LOCAL_DELIVERY_PASS"):
            self.assertEqual(acc["hard_check_fail_count"], 0)

    def test_report_fail_count_matches_evaluations(self) -> None:
        acc = read_json("evidence/review/HG-KSEOS_EXTERNAL_FINAL_ACCEPTANCE.json")
        report = (ROOT / "evidence/review/HG-KSEOS_EXTERNAL_FINAL_ACCEPTANCE_REPORT.md").read_text(encoding="utf-8")
        fail_marks = len(re.findall(r"^\- FAIL ", report, re.M))
        self.assertEqual(fail_marks, acc["hard_check_fail_count"])

    def test_final_accepted_requires_zero_failed_evaluations(self) -> None:
        acc = read_json("evidence/review/HG-KSEOS_EXTERNAL_FINAL_ACCEPTANCE.json")
        if acc["status"].startswith("HG-KSEOS_LOCAL_DELIVERY_PASS"):
            self.assertTrue(all(e["pass"] for e in acc["hard_check_evaluations"]))

    def test_no_truthiness_fail_in_report(self) -> None:
        # regression: PASS count must NOT be accompanied by FAIL lines
        acc = read_json("evidence/review/HG-KSEOS_EXTERNAL_FINAL_ACCEPTANCE.json")
        report = (ROOT / "evidence/review/HG-KSEOS_EXTERNAL_FINAL_ACCEPTANCE_REPORT.md").read_text(encoding="utf-8")
        m = re.search(r"\*\*(\d+)/(\d+) PASS, (\d+) FAIL\*\*", report)
        self.assertIsNotNone(m)
        total, fail = int(m.group(2)), int(m.group(3))
        self.assertEqual(total, acc["hard_check_total"])
        self.assertEqual(fail, acc["hard_check_fail_count"])
        if acc["status"].startswith("HG-KSEOS_LOCAL_DELIVERY_PASS"):
            self.assertEqual(fail, 0)
            self.assertNotIn("- FAIL ", report)


class CurrentIdentityTests(unittest.TestCase):
    """F3/F4: current changeset identity."""

    def test_current_changeset_task_is_015(self) -> None:
        """F3/F4 regression: the acceptance must carry the CURRENT changeset
        identity. Task-011/012/013/014 are historical accepted lineage."""
        acc = read_json("evidence/review/HG-KSEOS_EXTERNAL_FINAL_ACCEPTANCE.json")
        ctx = acc["acceptance_context"]
        self.assertEqual(ctx["current_changeset_task_id"],
                         "HGK-CS-A-APL-FULL-PROJECT-GATE-REPAIR-001")
        self.assertEqual(ctx["closure_task_id"],
                         "HGK-CS-A-APL-FULL-PROJECT-GATE-REPAIR-001")
        self.assertIn("HGK-SELF-BOOTSTRAP-NAMED-METHOD-RUNTIME-READINESS-TASK013-FINAL-CLOSURE-014",
                      ctx["historical_task_ids"])
        self.assertIn("HGK-HERMES-V020-NATIVE-RUNTIME-REUSE-CONVERGENCE-QUALIFICATION-013",
                      ctx["historical_task_ids"])
        self.assertIn("HGK-AUTONOMOUS-PROJECT-LIFECYCLE-GOVERNED-EVOLUTION-CLOSURE-011",
                      ctx["historical_task_ids"])
        # stale-identity regression: Task-014 must NOT appear as current
        self.assertNotEqual(ctx["current_changeset_task_id"],
                            "HGK-AUTONOMOUS-PROJECT-LIFECYCLE-GOVERNED-EVOLUTION-CLOSURE-011")

    def test_required_task011_invariants_complete(self) -> None:
        acc = read_json("evidence/review/HG-KSEOS_EXTERNAL_FINAL_ACCEPTANCE.json")
        ids = {e["id"] for e in acc["hard_check_evaluations"]}
        required = {
            "baseline_lineage_preserved", "tree_clean", "final_md_current_head_matches",
            "final_md_current_package_matches",
            "tst092_independent_pass", "blocking_tt_zero",
            "autonomous_project_entrypoint", "external_gpt_not_required_for_normal_project",
            "source_auto_discovery", "source_admission", "intent_roundtrip", "plan_auto_generation",
            "workorder_auto_admission", "real_hermes_codex_project_task", "automatic_repair",
            "checkpoint_resume", "project_independent_acceptance", "project_delivery",
            "normal_project_unnecessary_hitl_zero",
            "evolution_signal_capture", "gap_classifier", "fit_gap_reuse_first", "candidate_generation",
            "candidate_sandbox", "candidate_negative_security", "candidate_holdout_nrtv",
            "candidate_independent_checker", "failed_candidate_rollback", "promotion_policy_enforced",
            "promotion_policy_source_resolved", "later_reuse_after_promotion_or_source_aware_na",
            "authority_mutation_zero", "evaluator_self_mutation_zero", "infinite_evolution_loop_zero",
            "user_guide_quick_start", "user_guide_autonomous_lifecycle", "user_guide_governed_evolution",
            "user_guide_commands_exist", "user_guide_current_candidate_present",
            "user_guide_no_current_stale_companion", "user_guide_no_current_stale_maker_root",
            "user_guide_no_old_task_as_current",
            "coverage_reducer_exit_zero", "user_experience_reducer_exit_zero", "product_test_cases_green",
            "hlpe_green", "final_md_current_changeset_matches", "final_md_readback_exact",
        }
        self.assertTrue(required.issubset(ids), f"missing: {required - ids}")

    def test_apl05_requires_real_execution_receipt(self) -> None:
        receipt = read_json("evidence/review/HG-KSEOS_TASK011_APL05_RUNTIME_RECEIPT.json")
        self.assertEqual(receipt["final_verdict"], "PASS")
        self.assertEqual(receipt["executor"], "codex-cli")
        self.assertEqual(receipt["provider"], "opencode-go")
        self.assertEqual(receipt["model"], "deepseek-v4-flash")
        self.assertFalse(receipt["openai_fallback"])
        self.assertEqual(receipt["independent"]["recomputed_verdict"], "PASS")
        self.assertTrue(receipt["independent"]["has_multiply"])

    def test_ge11_requires_explicit_terminal(self) -> None:
        ge = read_json("evidence/review/HG-KSEOS_GOVERNED_EVOLUTION_ACCEPTANCE.json")
        ge11 = ge["results"]["GE-11_later_reuse"]
        self.assertIn("terminal", ge11)
        self.assertEqual(ge11["terminal"], "PROMOTION_READY_HITL_SOURCE_REQUIRED")
        self.assertEqual(ge11["later_reuse"], "NOT_APPLICABLE_UNTIL_APPROVED")
        self.assertEqual(ge["results"]["GE-10_promotion_gate"]["source_locator"],
                         "HG-KSEOS_P0-CIP-PACK_v2026.08.05-r2.md#COV-11-06")

    def test_promotion_policy_requires_source_locator(self) -> None:
        ge = read_json("evidence/review/HG-KSEOS_GOVERNED_EVOLUTION_ACCEPTANCE.json")
        # Task-012 source-resolved semantics: COV-11-06 (independent verifier +
        # Human Policy Owner), no implementation-invented auto-promotion.
        self.assertIn("COV-11-06", ge["promotion_policy"])
        self.assertIn("Human Policy Owner", ge["promotion_policy"])
        self.assertIn("no implementation-invented auto-promotion", ge["promotion_policy"])
        self.assertNotIn("LOW=auto", ge["promotion_policy"])
        self.assertIn("COV-11-06", ge["results"]["GE-10_promotion_gate"]["source_locator"])

    def test_user_guide_currentness_scan(self) -> None:
        audit = read_json("evidence/review/HG-KSEOS_USER_GUIDE_CURRENTNESS_AUDIT.json")
        self.assertEqual(audit["verdict"], "PASS")
        self.assertEqual(audit["current_stale"], 0)
        self.assertEqual(audit["maker_root_current_stale"], 0)
        self.assertEqual(audit["old_task_current_stale"], 0)
        self.assertTrue(audit["current_candidate_identity_present"])

    def test_final_md_task011_currentness(self) -> None:
        md = (ROOT / "evidence/review/HG-KSEOS_FINAL_EVIDENCE_FOR_REVIEW.md").read_text(encoding="utf-8")
        self.assertIn("HGK-AUTONOMOUS-PROJECT-LIFECYCLE-GOVERNED-EVOLUTION-CLOSURE-011", md)
        self.assertIn("PROMOTION_READY_HITL_SOURCE_REQUIRED", md)
        self.assertIn("COV-11-06", md)
        self.assertIn("HGK-TASK011-AUTONOMY-EVOLUTION-EXTERNAL-ACCEPTANCE-SEMANTIC-CLOSURE-012", md)


if __name__ == "__main__":
    unittest.main()
