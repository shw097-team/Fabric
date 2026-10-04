# -*- coding: utf-8 -*-
"""FDA-C5 router INTEGRATION test — drives route() from the REAL canonical
FDA_DESKTOP_CAPABILITY_MATRIX.yaml file (not an inline dict).
This is the blueprint 5.7/5.3B requirement: routing truth lives in the
canonical matrix artifact, never an ephemeral dict.
"""
import json
import sys
import unittest
from pathlib import Path

import yaml

FDA_DIR = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation")
sys.path.insert(0, str(FDA_DIR))

from fda_router import route, failover, Request

MATRIX_PATH = FDA_DIR / "FDA_DESKTOP_CAPABILITY_MATRIX.yaml"


def load_matrix_from_canonical():
    """Build the route-consumable matrix from the canonical YAML.
    Key: (application_id, application_version, action_class) ->
    {"cua": state, "ufo2": state}. Only QUALIFIED providers count as PASS.
    """
    doc = yaml.safe_load(MATRIX_PATH.read_text(encoding="utf-8"))
    out = {}
    for cls, spec in doc["action_classes"].items():
        app = spec["application"]["id"]
        ver = spec["application"]["version"]
        prov = spec["providers"]
        out[(app, ver, cls)] = {
            "cua": "PASS" if prov["CUA"]["state"] == "QUALIFIED" else prov["CUA"]["state"],
            "ufo2": "PASS" if prov["UFO2"]["state"] == "QUALIFIED" else prov["UFO2"]["state"],
        }
    return out, doc


class TestRouterFromCanonicalMatrix(unittest.TestCase):
    def setUp(self):
        self.matrix, self.doc = load_matrix_from_canonical()

    def test_matrix_file_is_canonical(self):
        self.assertEqual(self.doc["artifact_id"], "FDA_DESKTOP_CAPABILITY_MATRIX")
        self.assertEqual(self.doc["canonical_owner"], "FABRIC_CAPABILITY_QUALIFICATION_POLICY")
        self.assertEqual(self.doc["mutation_authority"], "ADMITTED_HGK_WORKORDER_ONLY")

    def test_all_five_mandatory_action_classes_present(self):
        classes = set(self.doc["action_classes"].keys())
        self.assertTrue({"XQ_LAUNCH_LOCATE", "XS_COMPILE_PASS", "XS_COMPILE_FAIL_READBACK",
                         "XQ_PAPER_CONFIG", "XQ_LOG_EXPORT_READBACK"} <= classes)

    def test_every_action_class_has_both_providers(self):
        for cls, spec in self.doc["action_classes"].items():
            self.assertIn("CUA", spec["providers"], cls)
            self.assertIn("UFO2", spec["providers"], cls)

    def test_route_uses_matrix_not_guesswork(self):
        # XQ_LAUNCH_LOCATE on the CURRENT matrix must route from the matrix state.
        req = Request(app="XQ", app_version="XQLite-3.20.02-260811",
                      action_class="XQ_LAUNCH_LOCATE", risk_class="LOW",
                      requires_secret=False, financial_side_effect=False,
                      active_position_policy_mutation=False)
        r = route(req, self.matrix)
        # matrix now has CUA=QUALIFIED (10/10 live fixture) -> route CUA deterministically
        self.assertEqual(r, "CUA")

    def test_qualified_compile_class_routes_cua(self):
        # XS_COMPILE_PASS is now QUALIFIED (F06 10/10 file-readback) -> CUA
        req = Request(app="XQ", app_version="XQLite-3.20.02-260811",
                      action_class="XS_COMPILE_PASS", risk_class="LOW",
                      requires_secret=False, financial_side_effect=False,
                      active_position_policy_mutation=False)
        self.assertEqual(route(req, self.matrix), "CUA")

    def test_failover_rules_still_apply(self):
        self.assertEqual(failover("CUA", "DETECTED_FAIL", True), "UFO2")
        self.assertEqual(failover("CUA", "UNKNOWN", True), "BLOCKED")

    def test_no_unknown_provider_state_in_matrix(self):
        allowed = {"QUALIFIED", "BLOCKED", "DEFERRED", "QUARANTINED", "QUALIFIED_SURFACE"}
        for cls, spec in self.doc["action_classes"].items():
            for p in ("CUA", "UFO2"):
                self.assertIn(spec["providers"][p]["state"], allowed,
                              f"{cls}.{p} state {spec['providers'][p]['state']}")


if __name__ == "__main__":
    unittest.main()
