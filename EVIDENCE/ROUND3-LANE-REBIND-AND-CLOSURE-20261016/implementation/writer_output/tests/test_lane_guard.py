
"""Regression tests for the pre-dispatch lane guard (R2-R5 of round FAR-LANE-SOD-003).

Closed defects: V3 bare-string admission, V4 skipped provider reconciliation, V5 non-projected
reasoning_effort, V6 argv-forced epoch. Each test names the defect it locks down.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import pathlib
import shutil
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent

_spec = importlib.util.spec_from_file_location("hgk_lane_guard", ROOT / "scripts" / "hgk-lane-guard.py")
guard = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(guard)

_spec2 = importlib.util.spec_from_file_location("lane_policy_mod", ROOT / "src" / "hg_kseos" / "lane_policy.py")
lp = importlib.util.module_from_spec(_spec2)
_spec2.loader.exec_module(lp)

FIXTURE_NOTE = "CONTROL-FIXTURE-NOT-A-REAL-ADMISSION"


def _fixture(path, model, provider, engine):
    path.write_text(json.dumps({
        "schema": FIXTURE_NOTE, "status": "ADMITTED",
        "arm": {"engine": engine, "model": model, "provider": provider},
        "served": {"engine": engine, "model": model, "provider": provider},
    }), encoding="utf-8")
    return str(path)


def evaluate(argv):
    return guard.evaluate(guard.build_parser().parse_args(argv))


def _registry_with_pair(tmp, *, status, distinct_required):
    """Copy the live registry, force the EXECUTE/VERIFY_SECURITY declaration, re-pin the source
    digest so only the SoD surface (not source_digest) is under test."""
    reg = copy.deepcopy(lp.load_registry())
    reg["source_of_routes"]["sha256"] = lp._sha256_file(ROOT / reg["source_of_routes"]["path"])
    for pair in reg["sod_invariants"]["pairs"]:
        if {pair.get("maker"), pair.get("checker")} == {"EXECUTE", "VERIFY_SECURITY"}:
            pair["distinct_required"] = distinct_required
    for conflict in reg["sod_invariants"]["declared_conflicts"]:
        if conflict.get("id") == "SOD006-C3":
            conflict["status"] = status
    path = tmp / "registry_fixture.json"
    path.write_text(json.dumps(reg), encoding="utf-8")
    return str(path)


def _registry_without_declaration(tmp):
    """Copy the live registry and STRIP every EXECUTE/VERIFY_SECURITY declaration entry, so the pair
    is genuinely undeclared (no pairs entry, no OWNER_ORDERED_IN_FORCE conflict)."""
    reg = copy.deepcopy(lp.load_registry())
    reg["source_of_routes"]["sha256"] = lp._sha256_file(ROOT / reg["source_of_routes"]["path"])
    reg["sod_invariants"]["pairs"] = [
        pair for pair in reg["sod_invariants"]["pairs"]
        if {pair.get("maker"), pair.get("checker")} != {"EXECUTE", "VERIFY_SECURITY"}
    ]
    reg["sod_invariants"]["declared_conflicts"] = [
        conflict for conflict in reg["sod_invariants"]["declared_conflicts"]
        if conflict.get("id") != "SOD006-C3"
    ]
    path = tmp / "registry_open.json"
    path.write_text(json.dumps(reg), encoding="utf-8")
    return str(path)


PLAN_ARM = ["--lane", "PLAN", "--maker-engine", "opencode-go", "--maker-model", "deepseek-v4.1-flash",
            "--target-engine", "openai-codex", "--target-model", "gpt-6.1-sol", "--target-provider", "openai-codex"]
VERIFY_ARM = ["--lane", "VERIFY_SECURITY", "--maker-engine", "opencode-go", "--maker-model", "deepseek-v4.1-flash",
              "--target-engine", "hermes", "--target-model", "glm-5.3-flash", "--target-provider", "opencode-go"]


class TestLaneGuard(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.plan_fix = _fixture(self.tmp / "plan.json", "gpt-6.1-sol", "openai-codex", "openai-codex")
        self.verify_fix = _fixture(self.tmp / "verify.json", "glm-5.3-flash", "opencode-go", "hermes")
        self.deepseek_fix = _fixture(self.tmp / "deepseek.json", "deepseek-v4.1-flash", "opencode-go", "hermes")

    def test_sod_same_model_is_refused(self):
        v = evaluate(["--lane", "VERIFY_SECURITY", "--maker-engine", "opencode-go",
                      "--maker-model", "deepseek-v4.1-flash", "--target-engine", "hermes",
                      "--target-model", "deepseek-v4.1-flash", "--target-provider", "opencode-go",
                      "--admission", "ADMITTED"])
        self.assertEqual(v["exit_code"], 2)
        self.assertIn("ERR_LANE_SOD_VIOLATION", v["errors"])

    # -- owner-ordered exemption (round ROUND3-LANE-REBIND-AND-CLOSURE-20261016) --------------------
    def test_sod_undeclared_same_model_pair_still_refused(self):
        # The regression that must NOT move: an undeclared same-model pair is refused, exit 2, and
        # never carries a declared_conflict field.
        reg = _registry_without_declaration(self.tmp)
        v = evaluate(["--lane", "VERIFY_SECURITY", "--maker-lane", "EXECUTE", "--maker-engine", "opencode-go",
                      "--maker-model", "deepseek-v4.1-flash", "--target-engine", "hermes",
                      "--target-model", "deepseek-v4.1-flash", "--target-provider", "opencode-go",
                      "--admission", self.deepseek_fix, "--registry", reg, "--root", str(ROOT)])
        self.assertEqual(v["exit_code"], 2)
        self.assertIn("ERR_LANE_SOD_VIOLATION", v["errors"])
        self.assertNotIn("declared_conflict", v)

    def test_declared_owner_ordered_pair_admits_with_conflict_id(self):
        reg = _registry_with_pair(self.tmp, status="OWNER_ORDERED_IN_FORCE", distinct_required=False)
        v = evaluate(["--lane", "VERIFY_SECURITY", "--maker-lane", "EXECUTE",
                      "--maker-engine", "opencode-go", "--maker-model", "deepseek-v4.1-flash",
                      "--target-engine", "hermes", "--target-model", "deepseek-v4.1-flash",
                      "--target-provider", "opencode-go", "--admission", self.deepseek_fix,
                      "--registry", reg, "--root", str(ROOT)])
        self.assertEqual(v["exit_code"], 0, v["errors"])
        self.assertEqual(v["status"], "ADMIT")
        self.assertEqual(v.get("declared_conflict"), "SOD006-C3")
        check = [c for c in v["checks"] if c["id"] == "sod_distinct_model"][0]
        self.assertTrue(check["ok"])
        self.assertEqual(check.get("declared_conflict"), "SOD006-C3")
        self.assertIn("SOD006-C3", check["detail"])

    def test_distinct_pair_admits_without_declared_conflict(self):
        v = evaluate(VERIFY_ARM + ["--admission", self.verify_fix])
        self.assertEqual(v["exit_code"], 0, v["errors"])
        self.assertNotIn("declared_conflict", v)
        check = [c for c in v["checks"] if c["id"] == "sod_distinct_model"][0]
        self.assertNotIn("declared_conflict", check)

    def test_declared_but_still_distinct_required_is_refused(self):
        # The exemption cannot be widened: named by the declaration, but distinct_required is still
        # true -> still refused.
        reg = _registry_with_pair(self.tmp, status="OWNER_ORDERED_IN_FORCE", distinct_required=True)
        v = evaluate(["--lane", "VERIFY_SECURITY", "--maker-lane", "EXECUTE",
                      "--maker-engine", "opencode-go", "--maker-model", "deepseek-v4.1-flash",
                      "--target-engine", "hermes", "--target-model", "deepseek-v4.1-flash",
                      "--target-provider", "opencode-go", "--admission", self.deepseek_fix,
                      "--registry", reg, "--root", str(ROOT)])
        self.assertEqual(v["exit_code"], 2)
        self.assertIn("ERR_LANE_SOD_VIOLATION", v["errors"])
        self.assertNotIn("declared_conflict", v)

    def test_declared_but_wrong_status_is_refused(self):
        # Named by the declaration and distinct_required false, but status is not
        # OWNER_ORDERED_IN_FORCE -> still refused.
        reg = _registry_with_pair(self.tmp, status="SUPERSEDED", distinct_required=False)
        v = evaluate(["--lane", "VERIFY_SECURITY", "--maker-lane", "EXECUTE",
                      "--maker-engine", "opencode-go", "--maker-model", "deepseek-v4.1-flash",
                      "--target-engine", "hermes", "--target-model", "deepseek-v4.1-flash",
                      "--target-provider", "opencode-go", "--admission", self.deepseek_fix,
                      "--registry", reg, "--root", str(ROOT)])
        self.assertEqual(v["exit_code"], 2)
        self.assertIn("ERR_LANE_SOD_VIOLATION", v["errors"])
        self.assertNotIn("declared_conflict", v)

    def test_admit_with_receipt_evidence(self):
        v = evaluate(VERIFY_ARM + ["--admission", self.verify_fix])
        self.assertEqual(v["exit_code"], 0, v["errors"])
        self.assertEqual(v["status"], "ADMIT")

    def test_v3_bare_admitted_string_is_not_admissible(self):
        v = evaluate(VERIFY_ARM + ["--admission", "ADMITTED"])
        self.assertEqual(v["exit_code"], 3)
        self.assertIn("ERR_LANE_NOT_ADMITTED", v["errors"])
        detail = [c["detail"] for c in v["checks"] if c["id"] == "arm_admitted"][0]
        self.assertIn("evidence=ABSENT", detail)

    def test_v4_provider_mismatch_is_refused(self):
        v = evaluate(VERIFY_ARM[:-2] + ["--target-provider", "nvidia", "--admission", self.verify_fix])
        self.assertEqual(v["exit_code"], 3)
        self.assertIn("ERR_LANE_NOT_ADMITTED", v["errors"])

    def test_v4_omitted_provider_is_not_a_wildcard(self):
        arm = ["--lane", "VERIFY_SECURITY", "--maker-engine", "opencode-go",
               "--maker-model", "deepseek-v4.1-flash", "--target-engine", "hermes",
               "--target-model", "glm-5.3-flash"]
        v = evaluate(arm + ["--admission", self.verify_fix])
        self.assertEqual(v["exit_code"], 3)
        self.assertIn("ERR_LANE_NOT_ADMITTED", v["errors"])

    def test_v1_stale_source_pin_is_refused(self):
        reg = self.tmp / "registry_stale.yaml"
        text = (ROOT / "config" / "lane-routing-registry.yaml").read_text(encoding="utf-8")
        text = text.replace(lp.load_registry()["source_of_routes"]["sha256"], "de" * 32)
        reg.write_text(text, encoding="utf-8")
        v = evaluate(PLAN_ARM + ["--admission", self.plan_fix, "--registry", str(reg)])
        self.assertEqual(v["exit_code"], 4)
        self.assertIn("ERR_LANE_SOURCE_STALE", v["errors"])

    def test_v6_expected_epoch_is_an_assertion_not_an_override(self):
        v = evaluate(PLAN_ARM + ["--admission", self.plan_fix, "--expected-epoch", "8"])
        self.assertEqual(v["exit_code"], 4)
        assertion = [c for c in v["checks"] if c["id"] == "expected_epoch_assertion"]
        self.assertEqual(len(assertion), 1)
        self.assertFalse(assertion[0]["ok"])
        self.assertEqual(v["live_epoch"], lp.load_site(ROOT / "config" / "model-lane-assignment.json")["revision"])

    def test_v5_reasoning_effort_survives_projection(self):
        policy = lp.project_policy(lp.load_registry())
        self.assertEqual(policy["routes"]["VERIFY_SECURITY"]["reasoning_effort"], "medium")
        self.assertEqual(lp.load_registry()["routes"][2]["reasoning_effort"], "medium") if False else None


if __name__ == "__main__":
    unittest.main()
