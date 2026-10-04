"""Deterministic unit tests for far_router (stdlib unittest only)."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import far_router  # noqa: E402


def minimal_req(**overrides):
    """Return a request profile with safe defaults for routing tests."""
    req = {
        "required_capabilities": [],
        "resume_required": False,
        "sandbox_required": False,
        "network_requirement": "DENY",
        "cost_budget": 100,
        "blocking_finding": False,
    }
    req.update(overrides)
    return req


class FarRouterTests(unittest.TestCase):

    def test_general_research_routes_native(self):
        result = far_router.route("RESEARCH_GENERAL", minimal_req())
        self.assertEqual(result["decision"], "NATIVE")
        self.assertEqual(result["primary"], "fabric-autoresearch-native")
        self.assertEqual(result["reason_code"], "FAR_ROUTE_NATIVE_DEFAULT")

    def test_literature_routes_native_aris(self):
        result = far_router.route("RESEARCH_LITERATURE_REPO", minimal_req())
        self.assertEqual(result["decision"], "NATIVE_WITH_SELECTED_ARIS")
        self.assertEqual(result["reason_code"], "FAR_ROUTE_NATIVE_ARIS")
        self.assertIn("research-lit", result["methods"])

    def test_rlm_prime_unqualified_blocks(self):
        req = minimal_req(
            blocking_finding=True, native_capability_minimum=False)
        result = far_router.route("RLM_CONTEXT_HEAVY", req)
        self.assertEqual(result["decision"], "BLOCK")
        self.assertEqual(
            result["block_reason"], "FAR_BLOCK_PROVIDER_UNQUALIFIED")
        self.assertEqual(
            result["reason_code"], "FAR_BLOCK_PROVIDER_UNQUALIFIED")

    def test_rlm_prime_unqualified_degrades_native(self):
        req = minimal_req(
            blocking_finding=True, native_capability_minimum=True)
        result = far_router.route("RLM_CONTEXT_HEAVY", req)
        self.assertEqual(result["decision"], "NATIVE")
        self.assertEqual(result["reason_code"], "FAR_DEGRADE_NATIVE")
        self.assertEqual(result["primary"], "fabric-autoresearch-native")
        self.assertEqual(result["degrade_note"], "FAR_DEGRADE_NATIVE")

    def test_mandatory_challenge_unavailable_blocks(self):
        req = minimal_req(challenge_required=True)
        result = far_router.route("RESEARCH_ADVERSARIAL_CHALLENGE", req)
        self.assertEqual(result["decision"], "BLOCK")
        self.assertEqual(
            result["block_reason"], "FAR_BLOCK_REQUIRED_CHALLENGE_UNAVAILABLE")

    def test_science_without_arc_research_only(self):
        req = minimal_req(sandbox_required=True)
        result = far_router.route("RESEARCH_SCIENTIFIC_EXPERIMENT", req)
        self.assertEqual(result["decision"], "RESEARCH_ONLY")
        self.assertFalse(result["experiment_claim"])

    def test_financial_method_no_mutation(self):
        result = far_router.route("RESEARCH_FINANCIAL_METHOD", minimal_req())
        self.assertEqual(result["mutation_authority"], "NONE")
        self.assertEqual(
            result["decision"], "NATIVE_WITH_SQS_OWNER_BOUNDARY")

    def test_eligible_negative_cases(self):
        base_provider = {
            "qualification_state": "ACTIVE",
            "capabilities": {"research", "web"},
            "resume_supported": True,
            "sandbox_ready": True,
            "network_policy": "ALLOW",
            "cost_floor": 10,
        }
        base_req = minimal_req()
        self.assertTrue(far_router.eligible(base_provider, base_req))

        provider = dict(base_provider, qualification_state="CANDIDATE")
        self.assertFalse(far_router.eligible(provider, base_req))

        req = minimal_req(required_capabilities=["missing_cap"])
        self.assertFalse(far_router.eligible(base_provider, req))

        provider = dict(base_provider, resume_supported=False)
        req = minimal_req(resume_required=True)
        self.assertFalse(far_router.eligible(provider, req))

        provider = dict(base_provider, sandbox_ready=False)
        req = minimal_req(sandbox_required=True)
        self.assertFalse(far_router.eligible(provider, req))

        provider = dict(base_provider, network_policy="DENY")
        req = minimal_req(network_requirement="ALLOW")
        self.assertFalse(far_router.eligible(provider, req))

        provider = dict(base_provider, cost_floor=200)
        req = minimal_req(cost_budget=100)
        self.assertFalse(far_router.eligible(provider, req))

        req = minimal_req(blocking_finding=True)
        self.assertFalse(far_router.eligible(base_provider, req))


if __name__ == "__main__":
    unittest.main()
