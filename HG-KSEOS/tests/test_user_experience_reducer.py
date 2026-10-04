"""Focused tests for UserExperienceReducer v1 (task-006 §16)."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from hg_kseos.release import UserExperienceEnvelope, UserExperienceReducer
from hg_kseos.spine import SharedSpine


def make_envelope(**overrides: object) -> UserExperienceEnvelope:
    base: dict[str, object] = {
        "uecx_source_expectations": 16,
        "uecx_rows": 15,
        "uecx_orphans": 0,
        "uecx_unknown": 0,
        "p0_required_user_journeys_open": 0,
        "p0_required_user_journeys_static_only": 0,
        "p0_required_user_journeys_maker_only": 0,
        "required_vertical_slices_total": 15,
        "required_vertical_slices_applicable": 13,
        "required_vertical_slices_pass": 13,
        "required_vertical_slices_deferred_source_backed": 2,
        "required_negative_tests_total": 12,
        "required_negative_tests_pass": 12,
        "natural_task_auto_route": "PASS",
        "skill_auto_select": "PASS",
        "memory_route_positive": "PASS",
        "memory_route_negative": "PASS",
        "rag_auto_route": "PASS",
        "kg_route_positive": "PASS",
        "kg_route_negative": "PASS",
        "unnecessary_hitl": 0,
        "unnecessary_multi_agent": 0,
        "unnecessary_tool_activation": 0,
        "self_promotion": 0,
        "authority_mutation": 0,
        "controlled_learning_scope_resolved": True,
        "obsidian_scope_resolved": True,
        "all_deferred_items_source_backed": True,
        "blocking_user_experience_tt": 0,
        "coverage_reducer_v2_exit": 0,
        "source_families_required": 23,
        "source_families_reviewed": 23,
        "source_expectations_unmapped": 0,
        "requirement_id_not_in_canonical_ledger": 0,
        "requirement_domain_mismatch": 0,
        "requirement_disposition_mismatch": 0,
        "u0_u1_disposition_conflict": 0,
        "p0_runtime_pass_raw_evidence_missing": 0,
        "p0_runtime_pass_independent_evidence_missing": 0,
        "p0_runtime_pass_fixture_missing": 0,
        "p0_runtime_pass_command_missing": 0,
        "p0_runtime_pass_trace_missing": 0,
        "p0_runtime_pass_hash_missing": 0,
        "classification_terminal_contradiction": 0,
        "named_tool_claim_without_lifecycle_evidence": 0,
        "knowledge_workbench_scope_resolved": True,
        "obsidian_identity_resolved": True,
        "obsidian_installed": True,
        "obsidian_runtime_qualified": True,
        "obsidian_feature_inventory_complete": True,
        "obsidian_unknown_features": 0,
        "llm_wiki_identity_resolved": True,
        "llm_wiki_single_selected_identity": True,
        "llm_wiki_installed": True,
        "llm_wiki_runtime_qualified": True,
        "llm_wiki_feature_inventory_complete": True,
        "llm_wiki_unknown_features": 0,
        "workbench_canonical_authority_violation": 0,
        "tool_claim_without_identity": 0,
        "tool_claim_without_version": 0,
        "tool_claim_without_raw_evidence": 0,
        "tool_claim_without_independent_evidence": 0,
        "obsidian_llmwiki_integration_pass": True,
        "withdrawal_consistency_pass": True,
        "conflict_fail_closed_pass": True,
        "fallback_to_git_markdown_pass": True,
        "external_gated_features_all_accounted_for": True,
        "blocking_workbench_tt": 0,
        "autonomous_project_entrypoint": True,
        "external_gpt_not_required": True,
        "project_source_auto_admission": True,
        "intent_roundtrip": True,
        "workorder_auto_admission": True,
        "real_hermes_codex_execution": True,
        "automatic_repair": True,
        "checkpoint_resume": True,
        "independent_project_acceptance": True,
        "minimal_hitl": True,
        "evolution_signal_capture": True,
        "gap_classification": True,
        "fit_gap_reuse_first": True,
        "candidate_sandbox": True,
        "holdout_nrtv": True,
        "independent_candidate_check": True,
        "failed_candidate_rollback": True,
        "promotion_policy_enforced": True,
        "authority_mutation": 0,
        "evaluator_self_mutation": 0,
        "infinite_evolution_loop": 0,
        "user_guide_current_runtime": True,
        "user_guide_no_stale_companion_claim": True,
        "user_guide_no_task007_current_wording": True,
        "checker": "INDEPENDENT_CHECKER",
        "artifacts": ("UECX", "U7", "U8", "U9", "OBS", "WIKI"),
    }
    base.update(overrides)
    return UserExperienceEnvelope.from_dict(base)


class UserExperienceReducerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.spine = SharedSpine(Path(self.tmp.name) / "spine.db")
        self.spine.initialize()
        self.spine.create_project()
        self.reducer = UserExperienceReducer(self.spine)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_full_pass(self) -> None:
        decision = self.reducer.reduce(make_envelope())
        self.assertEqual(decision["verdict"], "HG-KSEOS_USER_EXPECTED_CAPABILITY_EXPERIENCE_PASS")
        self.assertEqual(decision["reasons"], [])
        self.assertEqual(decision["exit_code"], 0)
        self.assertEqual(decision["schema"], "HGK-USER-EXPERIENCE-REDUCER/1")

    def test_open_p0_journey_fails(self) -> None:
        decision = self.reducer.reduce(make_envelope(p0_required_user_journeys_open=1))
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")
        self.assertIn("P0_USER_JOURNEYS_OPEN", decision["reasons"])

    def test_vertical_slice_incomplete_fails(self) -> None:
        decision = self.reducer.reduce(make_envelope(required_vertical_slices_pass=12))
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")
        self.assertIn("VERTICAL_SLICES_INCOMPLETE", decision["reasons"])

    def test_negative_tests_incomplete_fails(self) -> None:
        decision = self.reducer.reduce(make_envelope(required_negative_tests_pass=11))
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")
        self.assertIn("NEGATIVE_OPERATIONAL_TESTS_INCOMPLETE", decision["reasons"])

    def test_auto_route_fail(self) -> None:
        decision = self.reducer.reduce(make_envelope(natural_task_auto_route="FAIL"))
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")
        self.assertIn("NATURAL_TASK_AUTO_ROUTE_FAIL", decision["reasons"])

    def test_unnecessary_hitl_fails(self) -> None:
        decision = self.reducer.reduce(make_envelope(unnecessary_hitl=1))
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")
        self.assertIn("UNNECESSARY_HITL_NONZERO", decision["reasons"])

    def test_self_promotion_fails(self) -> None:
        decision = self.reducer.reduce(make_envelope(self_promotion=1))
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")
        self.assertIn("SELF_PROMOTION_NONZERO", decision["reasons"])

    def test_coverage_reducer_not_pass_fails(self) -> None:
        decision = self.reducer.reduce(make_envelope(coverage_reducer_v2_exit=1))
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")
        self.assertIn("COVERAGE_REDUCER_V2_NOT_PASS", decision["reasons"])

    def test_source_family_scan_incomplete_fails(self) -> None:
        decision = self.reducer.reduce(make_envelope(source_families_reviewed=22))
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")
        self.assertIn("SOURCE_FAMILY_SCAN_INCOMPLETE", decision["reasons"])

    def test_raw_evidence_missing_fails(self) -> None:
        decision = self.reducer.reduce(make_envelope(p0_runtime_pass_raw_evidence_missing=1))
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")
        self.assertIn("P0_RUNTIME_PASS_RAW_EVIDENCE_MISSING", decision["reasons"])

    def test_independent_evidence_missing_fails(self) -> None:
        decision = self.reducer.reduce(make_envelope(p0_runtime_pass_independent_evidence_missing=2))
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")
        self.assertIn("P0_RUNTIME_PASS_INDEPENDENT_EVIDENCE_MISSING", decision["reasons"])

    def test_crosswalk_mismatch_fails(self) -> None:
        decision = self.reducer.reduce(make_envelope(requirement_domain_mismatch=1))
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")
        self.assertIn("REQUIREMENT_DOMAIN_MISMATCH", decision["reasons"])

    def test_disposition_conflict_fails(self) -> None:
        decision = self.reducer.reduce(make_envelope(u0_u1_disposition_conflict=1))
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")
        self.assertIn("U0_U1_DISPOSITION_CONFLICT", decision["reasons"])

    def test_classification_contradiction_fails(self) -> None:
        decision = self.reducer.reduce(make_envelope(classification_terminal_contradiction=1))
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")
        self.assertIn("CLASSIFICATION_TERMINAL_CONTRADICTION", decision["reasons"])

    def test_obsidian_not_installed_fails(self) -> None:
        decision = self.reducer.reduce(make_envelope(obsidian_installed=False))
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")
        self.assertIn("OBSIDIAN_NOT_INSTALLED", decision["reasons"])

    def test_llmwiki_unknown_features_fails(self) -> None:
        decision = self.reducer.reduce(make_envelope(llm_wiki_unknown_features=1))
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")
        self.assertIn("LLM_WIKI_UNKNOWN_FEATURES_NONZERO", decision["reasons"])

    def test_integration_fail_fails(self) -> None:
        decision = self.reducer.reduce(make_envelope(obsidian_llmwiki_integration_pass=False))
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")
        self.assertIn("OBSIDIAN_LLMWIKI_INTEGRATION_FAIL", decision["reasons"])

    def test_autonomy_entrypoint_missing_fails(self) -> None:
        decision = self.reducer.reduce(make_envelope(autonomous_project_entrypoint=False))
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")
        self.assertIn("AUTONOMOUS_PROJECT_ENTRYPOINT_MISSING", decision["reasons"])

    def test_external_gpt_required_fails(self) -> None:
        decision = self.reducer.reduce(make_envelope(external_gpt_not_required=False))
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")
        self.assertIn("EXTERNAL_GPT_REQUIRED_FOR_NORMAL_LIFECYCLE", decision["reasons"])

    def test_authority_mutation_fails(self) -> None:
        decision = self.reducer.reduce(make_envelope(authority_mutation=1))
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")
        self.assertIn("AUTHORITY_MUTATION_ATTEMPT_SUCCEEDED", decision["reasons"])

    def test_evolution_loop_fails(self) -> None:
        decision = self.reducer.reduce(make_envelope(infinite_evolution_loop=1))
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")
        self.assertIn("INFINITE_EVOLUTION_LOOP", decision["reasons"])

    def test_user_guide_stale_fails(self) -> None:
        decision = self.reducer.reduce(make_envelope(user_guide_current_runtime=False))
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")
        self.assertIn("USER_GUIDE_STALE", decision["reasons"])

    def test_missing_field_rejected(self) -> None:
        data = make_envelope().__dict__
        del data["checker"]
        with self.assertRaises(ValueError):
            UserExperienceEnvelope.from_dict(data)


if __name__ == "__main__":
    unittest.main()
