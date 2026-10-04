"""Task-014 named-method closure regression tests.

Validates: named-method evidence schema/verdicts, activation invariants,
canonical Hermes v0.20 resolution, execution delta, single-current Final
Evidence claims (after normalization), and no authority/release escapes.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
REVIEW = ROOT / "evidence" / "review"


def read_json(name: str) -> dict:
    return json.loads((REVIEW / name).read_text(encoding="utf-8"))


class NamedMethodEvidenceTests(unittest.TestCase):
    def test_openspec_identity_exact(self) -> None:
        d = read_json("HG-KSEOS_OPENSPEC_IDENTITY_READBACK.json")
        self.assertTrue(d["identity_exact"])
        self.assertEqual(d["readback_version"], "1.8.0")
        self.assertIn("MIT", d["readback_license"])

    def test_gstack_identity_exact(self) -> None:
        d = read_json("HG-KSEOS_GSTACK_IDENTITY_READBACK.json")
        self.assertTrue(d["identity_exact"])
        self.assertEqual(d["readback_commit"], "94993f74012782fd94416dd44b8314f6363a13a4")

    def test_independent_acceptances_pass(self) -> None:
        for name in ("HG-KSEOS_OPENSPEC_RUNTIME_INDEPENDENT_ACCEPTANCE.json",
                     "HG-KSEOS_GSTACK_RUNTIME_INDEPENDENT_ACCEPTANCE.json",
                     "HG-KSEOS_NAMED_METHOD_ROUTING_INDEPENDENT_ACCEPTANCE.json"):
            d = read_json(name)
            self.assertEqual(d["verdict"], "PASS", name)
            self.assertEqual(d["checker"], "INDEPENDENT_CHECKER (fresh read-only recompute)")

    def test_self_bootstrap_no_authority_mutation(self) -> None:
        d = read_json("HG-KSEOS_NAMED_METHOD_SELF_BOOTSTRAP_ACCEPTANCE.json")
        self.assertEqual(d["verdict"], "PASS")
        self.assertEqual(d["authority_mutation"], 0)
        self.assertEqual(d["evaluator_mutation"], 0)
        self.assertEqual(d["second_control_plane"], 0)

    def test_activation_contract_zero_invariants(self) -> None:
        d = read_json("HG-KSEOS_NAMED_METHOD_ACTIVATION_CONTRACT_ACCEPTANCE.json")
        self.assertEqual(d["verdict"], "PASS")
        for key, value in d["invariants"].items():
            self.assertEqual(value, 0, key)

    def test_openspec_xor_and_boundaries(self) -> None:
        e2e = read_json("HG-KSEOS_OPENSPEC_BROWNFIELD_E2E.json")
        self.assertEqual(e2e["verdict"], "PASS")
        self.assertTrue(e2e["openspec_not_root_ssot"])
        self.assertTrue(e2e["openspec_not_release_owner"])
        self.assertTrue(e2e["codex_remains_writer"])

    def test_gstack_ship_advisory_only(self) -> None:
        e2e = read_json("HG-KSEOS_GSTACK_SELECTED_E2E.json")
        self.assertEqual(e2e["verdict"], "PASS")


class CanonicalRuntimeTests(unittest.TestCase):
    def test_config_resolves_scheme_b_appdata_runtime(self) -> None:
        cfg = json.loads((ROOT / "config" / "hermes.json").read_text(encoding="utf-8"))
        self.assertEqual(cfg["release"]["version"], "0.20.0")
        self.assertEqual(cfg["release"]["tag"], "v2026.8.3")
        self.assertEqual(cfg["release"]["commit"], "3c27eb6234bf91b8ceee9e9071591b31e9b148cb")
        self.assertEqual(cfg["status"], "ACTIVE_SELECTED_REINSTALL_BASELINE")
        self.assertEqual(
            cfg["executable"],
            r"C:\Users\user\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe",
        )
        self.assertEqual(
            cfg["python_executable"],
            r"C:\Users\user\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe",
        )
        self.assertEqual(cfg["canonical_hermes_home"], r"C:\Users\user\AppData\Local\hermes")

    def test_canonical_live_readback(self) -> None:
        d = read_json("HG-KSEOS_HERMES_V020_CANONICAL_LIVE_READBACK.json")
        self.assertTrue(d["resolved"]["hermes_core_ps1_pass"])
        self.assertEqual(d["resolved"]["version"], "0.20.0")
        self.assertEqual(d["resolved"]["commit"], "3c27eb6234bf91b8ceee9e9071591b31e9b148cb")
        self.assertTrue(d["canonical_identity_aligned"])
        self.assertTrue(all(s["verdict"] == "PASS" for s in d["smokes"].values()))
        self.assertEqual(d["verdict"], "PASS")

    def test_final_md_raw_byte_fields(self) -> None:
        d = read_json("HG-KSEOS_FINAL_MD_RAW_BYTE_INDEPENDENT_READBACK.json")
        self.assertEqual(d["verdict"], "PASS")
        self.assertTrue(d["raw_sha256"])
        self.assertEqual(d["bytes"], (REVIEW / "HG-KSEOS_FINAL_EVIDENCE_FOR_REVIEW.md").stat().st_size)


class SingleCurrentTests(unittest.TestCase):
    """Gate-0A regression: stale identities must NOT appear in current context."""

    def test_single_current_identity(self) -> None:
        d = read_json("HG-KSEOS_FINAL_MD_RAW_BYTE_INDEPENDENT_READBACK.json")
        for key in ("single_current_head", "single_current_package",
                    "single_current_changeset", "single_current_test_denominator",
                    "single_current_hermes", "single_current_openspec", "single_current_gstack"):
            self.assertTrue(d["checks"].get(key), key)

    def test_no_stale_task013_as_current(self) -> None:
        d = read_json("HG-KSEOS_FINAL_MD_RAW_BYTE_INDEPENDENT_READBACK.json")
        self.assertTrue(d["checks"].get("task013_as_current"))
        self.assertTrue(d["checks"].get("task012_as_current"))
        self.assertTrue(d["checks"].get("task011_as_current"))

    def test_external_acceptance_current_identity(self) -> None:
        d = read_json("HG-KSEOS_EXTERNAL_FINAL_ACCEPTANCE.json")
        self.assertEqual(d["acceptance_context"]["current_changeset_task_id"],
                         "HGK-CS-A-APL-FULL-PROJECT-GATE-REPAIR-001")
        self.assertIn("HGK-SELF-BOOTSTRAP-NAMED-METHOD-RUNTIME-READINESS-TASK013-FINAL-CLOSURE-014",
                      d["acceptance_context"]["historical_task_ids"])
        self.assertIn("HGK-HERMES-V020-NATIVE-RUNTIME-REUSE-CONVERGENCE-QUALIFICATION-013",
                      d["acceptance_context"]["historical_task_ids"])


if __name__ == "__main__":
    unittest.main()
