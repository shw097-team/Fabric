"""Task-014 named-method registry / router / activation-invariant tests.

Covers: registry completeness, deterministic routing (no LLM guessing),
XOR enforcement, fail-closed activation invariants, and CoverageReducer
named-method gates.
"""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from hg_kseos.named_methods import (
    ACTIVE_SELECTED,
    NAMED_METHODS,
    evaluate_activation_invariants,
    route,
)
from hg_kseos.release import CoverageEnvelope, CoverageReducer
from hg_kseos.spine import SharedSpine

NEEDED_EVIDENCE = {
    "openspec": ["HG-KSEOS_OPENSPEC_IDENTITY_READBACK.json",
                 "HG-KSEOS_OPENSPEC_HERMES_BINDING_ACCEPTANCE.json",
                 "HG-KSEOS_OPENSPEC_BROWNFIELD_E2E.json",
                 "HG-KSEOS_OPENSPEC_RUNTIME_INDEPENDENT_ACCEPTANCE.json"],
    "gstack": ["HG-KSEOS_GSTACK_IDENTITY_READBACK.json",
               "HG-KSEOS_GSTACK_HERMES_BINDING_ACCEPTANCE.json",
               "HG-KSEOS_GSTACK_SELECTED_E2E.json",
               "HG-KSEOS_GSTACK_RUNTIME_INDEPENDENT_ACCEPTANCE.json"],
}


class RegistryTests(unittest.TestCase):
    def test_openspec_and_gstack_registered(self) -> None:
        self.assertIn("openspec", NAMED_METHODS)
        for slice_id in ("gstack.plan-eng-review", "gstack.review", "gstack.qa",
                         "gstack.cso", "gstack.ship", "gstack.office-hours", "gstack.retro"):
            self.assertIn(slice_id, NAMED_METHODS)
        self.assertIn("spec_kit", NAMED_METHODS)

    def test_openspec_xor_spec_kit(self) -> None:
        self.assertEqual(NAMED_METHODS["openspec"].xor_with, "spec_kit")
        self.assertEqual(NAMED_METHODS["spec_kit"].xor_with, "openspec")

    def test_ship_is_advisory_only(self) -> None:
        self.assertFalse(NAMED_METHODS["gstack.ship"].final_authority)

    def test_active_selected_requires_runtime(self) -> None:
        for tid in ACTIVE_SELECTED:
            self.assertTrue(NAMED_METHODS[tid].runtime_required_now)
            self.assertNotEqual(NAMED_METHODS[tid].provider_state, "STANDBY")


class RouterTests(unittest.TestCase):
    def test_brownfield_routes_to_openspec(self) -> None:
        d = route("brownfield login refactor")
        self.assertEqual(d["provider"], "openspec")
        self.assertEqual(d["state"], "CERTIFIED_ACTIVE_BROWNFIELD")
        self.assertEqual(d["fallback"], "hgk_native_prw")

    def test_greenfield_is_xor_not_openspec(self) -> None:
        d = route("greenfield new service")
        self.assertEqual(d["state"], "XOR_GREENFIELD")
        self.assertIsNone(d["provider"])

    def test_plan_routes_to_plan_eng_review(self) -> None:
        d = route("plan ready for engineering review")
        self.assertEqual(d["provider"], "gstack.plan-eng-review")
        self.assertEqual(d["fallback"], "hgk_native_plan_review")

    def test_code_review_routes_to_review(self) -> None:
        d = route("review implementation complete")
        self.assertEqual(d["provider"], "gstack.review")

    def test_qa_routes_to_qa(self) -> None:
        d = route("qa required for the release")
        self.assertEqual(d["provider"], "gstack.qa")

    def test_security_routes_to_cso(self) -> None:
        d = route("security sensitive change review")
        self.assertEqual(d["provider"], "gstack.cso")

    def test_release_is_advisory_not_authority(self) -> None:
        d = route("release readiness check")
        self.assertEqual(d["provider"], "gstack.ship")
        self.assertFalse(d["final_authority"])

    def test_ambiguity_routes_to_office_hours(self) -> None:
        d = route("high-impact ambiguity on scope")
        self.assertEqual(d["provider"], "gstack.office-hours")

    def test_retro_routes_to_retro(self) -> None:
        d = route("retro after the iteration")
        self.assertEqual(d["provider"], "gstack.retro")

    def test_unknown_flow_is_native(self) -> None:
        d = route("plain task")
        self.assertEqual(d["route"], "NATIVE")
        self.assertIsNone(d["provider"])

    def test_deselected_brownfield_degrades(self) -> None:
        d = route("brownfield work", selected_slices=set())
        self.assertEqual(d["state"], "DEGRADED")

    def test_no_llm_guessing(self) -> None:
        # every flow maps deterministically; never a free-form string decision
        for flow in ("brownfield", "plan", "review", "qa", "security", "release",
                     "ambiguity", "retro", "greenfield", "whatever"):
            d = route(flow)
            self.assertIn(d["route"], {"OPENSPEC", "GSTACK", "NATIVE", "XOR_GREENFIELD"})


class ActivationInvariantTests(unittest.TestCase):
    def test_missing_evidence_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            inv = evaluate_activation_invariants(Path(tmp))
            self.assertGreater(inv["active_named_method_missing_identity"], 0)
            self.assertGreater(inv["active_named_method_missing_pilot"], 0)
            self.assertGreater(
                inv["canonical_flow_named_method_without_runtime_or_certified_substitute"], 0)

    def test_complete_evidence_is_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for tool, refs in NEEDED_EVIDENCE.items():
                for ref in refs:
                    (root / ref).write_text("{}", encoding="utf-8")
            inv = evaluate_activation_invariants(root)
            for key, value in inv.items():
                self.assertEqual(value, 0, key)


class ReducerGateTests(unittest.TestCase):
    def _envelope(self, **overrides: object) -> CoverageEnvelope:
        base: dict[str, object] = {
            "coverage_domains_total": 30, "coverage_domains_terminal": 30,
            "subcapabilities_total": 2, "subcapabilities_terminal": 2,
            "canonical_requirements_total": 499, "requirements_reconciled": True,
            "requirements_domain_mapped": 499, "requirements_source_bound": 499,
            "requirement_owner_matches_domain_owner": 499,
            "requirement_owner_source_validated": 499, "unsupported_disposition_count": 0,
            "orphan_requirements": 0, "unowned_mandatory_assets": 0,
            "runtime_pass_missing_evidence": 0, "active_deferred_contradiction": 0,
            "missing_evidence_refs": 0, "tst_total": 92, "tst_independent_pass": 92,
            "semantic_depth_calibrated": True, "runtime_required_static_only_count": 0,
            "current_executor_missing": 0, "raw_receipt_missing": 0,
            "domains": {"memory": "RUNTIME_PASS", "knowledge_factory": "RUNTIME_PASS",
                        "retrieval_rag_kb": "RUNTIME_PASS", "knowledge_graph": "RUNTIME_PASS",
                        "graphrag": "DEFERRED_SOURCE_BACKED", "storage": "RUNTIME_PASS"},
            "knowledge_security_negative": "PASS", "domain_blocking_gaps": 0,
            "hermes_provider": "opencode-go", "hermes_model": "deepseek-v4-flash",
            "codex_cli_primary_executor": True, "opencodex_transport": True,
            "openai_model_fallback": False,
            "protected_identities_78_disposition_complete": True,
            "mandatory_default_active_providers_certified": True,
            "tst_054": "INDEPENDENT_CASE_PASS", "tst_092": "INDEPENDENT_CASE_PASS",
            "product_tests_all_pass": True, "hlpe_tests_all_pass": True,
            "security_blockers": 0, "blocking_tt": 0, "backup_restore_pass": True,
            "rollback_pass": True, "sbom_current": True, "user_guide_exists": True,
            "user_guide_runtime_consistent": True, "user_guide_sha256_verified": True,
            "package_exact_readback": True, "final_head_independently_checked": True,
            "final_evidence_md_exists": True, "final_evidence_md_readback_verified": True,
            "checker": "INDEPENDENT_CHECKER",
            "artifacts": ("evidence/review/x.json",),
        }
        base.update(overrides)
        return CoverageEnvelope.from_dict(base)

    def _reduce(self, envelope: CoverageEnvelope) -> dict:
        with tempfile.TemporaryDirectory() as tmp:
            spine = SharedSpine(Path(tmp) / "spine.db")
            spine.initialize()
            return CoverageReducer(spine).reduce(envelope)

    def test_zero_invariants_pass(self) -> None:
        decision = self._reduce(self._envelope())
        self.assertEqual(decision["verdict"], "HG-KSEOS_LOCAL_DELIVERY_PASS")

    def test_nonzero_silent_fallback_fails_closed(self) -> None:
        decision = self._reduce(self._envelope(named_method_silent_fallback=1))
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")
        self.assertIn("NAMED_METHOD_SILENT_FALLBACK_NONZERO", decision["reasons"])

    def test_nonzero_missing_pilot_fails_closed(self) -> None:
        decision = self._reduce(self._envelope(active_named_method_missing_pilot=1))
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")
        self.assertIn("ACTIVE_NAMED_METHOD_MISSING_PILOT_NONZERO", decision["reasons"])

    def test_nonzero_dual_spec_owner_fails_closed(self) -> None:
        decision = self._reduce(self._envelope(dual_spec_owner=1))
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")

    def test_nonzero_release_authority_escape_fails_closed(self) -> None:
        decision = self._reduce(self._envelope(release_authority_escape=1))
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")


if __name__ == "__main__":
    unittest.main()
