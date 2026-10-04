# -*- coding: utf-8 -*-
"""FDA deterministic provider router tests (blueprint 5.7).
Contract of behavior: hard denials outrank capability; deterministic policy;
no silent fallback; unknown/ambiguous state never auto-failed-over.
"""
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from fda_router import route, failover, Request


def matrix(cua_pass=True, ufo2_pass=False):
    return {
        ("XQ", "XQLite-1.10.0.0-INSTALLED", "XS_COMPILE_PASS"): {
            "cua": "PASS" if cua_pass else "DEFERRED",
            "ufo2": "PASS" if ufo2_pass else "DEFERRED",
        },
        ("XQ", "XQLite-1.10.0.0-INSTALLED", "XQ_PAPER_CONFIG"): {
            "cua": "PASS" if cua_pass else "DEFERRED",
            "ufo2": "PASS" if ufo2_pass else "DEFERRED",
        },
    }


class TestRouter(unittest.TestCase):
    def test_hard_denial_secret(self):
        req = Request(app="XQ", app_version="v1", action_class="XS_COMPILE_PASS",
                      risk_class="LOW", requires_secret=True,
                      financial_side_effect=False, active_position_policy_mutation=False)
        self.assertEqual(route(req, matrix()), "HITL")

    def test_hard_denial_financial_side_effect(self):
        req = Request(app="XQ", app_version="v1", action_class="XS_COMPILE_PASS",
                      risk_class="HIGH", requires_secret=False,
                      financial_side_effect=True, active_position_policy_mutation=False)
        self.assertEqual(route(req, matrix()), "HITL")

    def test_hard_denial_active_position_mutation(self):
        req = Request(app="XQ", app_version="v1", action_class="MODIFY_POSITION",
                      risk_class="HIGH", requires_secret=False,
                      financial_side_effect=False, active_position_policy_mutation=True)
        self.assertEqual(route(req, matrix()), "BLOCKED")

    def test_cua_preferred_when_pass(self):
        req = Request(app="XQ", app_version="XQLite-1.10.0.0-INSTALLED",
                      action_class="XS_COMPILE_PASS", risk_class="LOW",
                      requires_secret=False, financial_side_effect=False,
                      active_position_policy_mutation=False)
        self.assertEqual(route(req, matrix(cua_pass=True, ufo2_pass=True)), "CUA")

    def test_ufo2_when_only_ufo2_pass(self):
        req = Request(app="XQ", app_version="XQLite-1.10.0.0-INSTALLED",
                      action_class="XS_COMPILE_PASS", risk_class="LOW",
                      requires_secret=False, financial_side_effect=False,
                      active_position_policy_mutation=False)
        self.assertEqual(route(req, matrix(cua_pass=False, ufo2_pass=True)), "UFO2")

    def test_blocked_when_no_provider_certified(self):
        req = Request(app="XQ", app_version="XQLite-1.10.0.0-INSTALLED",
                      action_class="XS_COMPILE_PASS", risk_class="LOW",
                      requires_secret=False, financial_side_effect=False,
                      active_position_policy_mutation=False)
        self.assertEqual(route(req, matrix(cua_pass=False, ufo2_pass=False)), "BLOCKED")


class TestFailover(unittest.TestCase):
    def test_pass_stays_primary(self):
        self.assertEqual(failover("CUA", "PASS", True), "CUA")

    def test_detected_fail_to_alternate(self):
        self.assertEqual(failover("CUA", "DETECTED_FAIL", True), "UFO2")
        self.assertEqual(failover("UFO2", "DETECTED_FAIL", True), "CUA")

    def test_safe_halt_to_alternate(self):
        self.assertEqual(failover("CUA", "SAFE_HALT", True), "UFO2")

    def test_unknown_outcome_never_failover(self):
        self.assertEqual(failover("CUA", "UNKNOWN", True), "BLOCKED")

    def test_ambiguous_effect_never_failover(self):
        self.assertEqual(failover("CUA", "POSSIBLY_APPLIED_BUT_UNVERIFIED", True), "BLOCKED")

    def test_no_alternate_certified_blocks(self):
        self.assertEqual(failover("CUA", "DETECTED_FAIL", False), "BLOCKED")


if __name__ == "__main__":
    unittest.main()
