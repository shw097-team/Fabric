"""Task-015 final external evidence coherence closure regression tests.

Covers G1–G6: Final MD acceptance status machine-projection, denominator
schema/current-task binding, unique hard-check IDs, TST-092 receipt lineage
(historical immutability), acceptance input manifest hashes, and cross-artifact
semantic coherence.
"""
from __future__ import annotations

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
REVIEW = ROOT / "evidence" / "review"
WAVE = ROOT / "evidence" / "wave-18"
TASK = "HGK-CS-A-APL-FULL-PROJECT-GATE-REPAIR-001"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class G1FinalMdProjectionTests(unittest.TestCase):
    def test_ab_status_and_counts_match_acceptance(self) -> None:
        raw = read_json(REVIEW / "HG-KSEOS_FINAL_MD_RAW_BYTE_INDEPENDENT_READBACK.json")
        self.assertEqual(raw["verdict"], "PASS")
        self.assertTrue(raw["checks"]["final_md_external_acceptance_status_matches"])
        self.assertTrue(raw["checks"]["final_md_external_acceptance_counts_match"])
        self.assertTrue(raw["checks"]["final_md_unique_counts_match"])

    def test_no_stale_acceptance_counts_in_final_md(self) -> None:
        md = (REVIEW / "HG-KSEOS_FINAL_EVIDENCE_FOR_REVIEW.md").read_text(encoding="utf-8")
        self.assertNotIn("157/158", md)
        self.assertNotIn("FAIL_CLOSED - 1 HARD CHECK FAILURES", md.split("## AB.")[0])


class G2DenominatorTests(unittest.TestCase):
    def test_denominator_schema_and_task_binding(self) -> None:
        td = read_json(REVIEW / "HG-KSEOS_CURRENT_TEST_DENOMINATOR.json")
        self.assertEqual(td["schema"], "HGK-CURRENT-TEST-DENOMINATOR/2")
        self.assertEqual(td["current_changeset_task_id"], TASK)
        self.assertIn("HGK-SELF-BOOTSTRAP-NAMED-METHOD-RUNTIME-READINESS-TASK013-FINAL-CLOSURE-014",
                      td["historical_source_task_ids"])
        self.assertIn("discovery_command", td)
        self.assertIn("test_manifest_sha256", td)

    def test_denominator_head_matches_git(self) -> None:
        import subprocess
        head = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"],
                              capture_output=True, text=True, encoding="utf-8").stdout.strip()
        td = read_json(REVIEW / "HG-KSEOS_CURRENT_TEST_DENOMINATOR.json")
        self.assertEqual(td["head"], head)


class G3UniqueHardCheckTests(unittest.TestCase):
    def test_unique_ids(self) -> None:
        acc = read_json(REVIEW / "HG-KSEOS_EXTERNAL_FINAL_ACCEPTANCE.json")
        ids = [e["id"] for e in acc["hard_check_evaluations"]]
        self.assertEqual(len(ids), acc["hard_check_row_total"])
        self.assertEqual(len(set(ids)), acc["hard_check_unique_id_total"])
        self.assertEqual(acc["hard_check_row_total"], acc["hard_check_unique_id_total"])
        self.assertEqual(acc["duplicate_hard_check_id_count"], 0)
        self.assertEqual(acc["duplicate_hard_check_ids"], [])
        self.assertEqual([i for i, c in Counter(ids).items() if c > 1], [])

    def test_no_known_duplicates(self) -> None:
        acc = read_json(REVIEW / "HG-KSEOS_EXTERNAL_FINAL_ACCEPTANCE.json")
        ids = [e["id"] for e in acc["hard_check_evaluations"]]
        for dup in ("blocking_tt_zero", "promotion_policy_source_resolved",
                    "coverage_reducer_exit_zero", "user_experience_reducer_exit_zero",
                    "production_not_claimed"):
            self.assertEqual(ids.count(dup), 1, dup)


class G4Tst092LineageTests(unittest.TestCase):
    def test_current_receipt_lineage(self) -> None:
        cur = read_json(WAVE / "TST-092_TASK014_FINAL_COHERENCE_INDEPENDENT_READBACK.json")
        self.assertEqual(cur["current_changeset_task_id"], TASK)
        self.assertEqual(cur["verdict"], "INDEPENDENT_CASE_PASS")
        self.assertTrue(cur["exact_set"])
        self.assertEqual(cur["hash_mismatches"], [])

    def test_historical_receipt_restored_immutable(self) -> None:
        hist = read_json(WAVE / "TST-092_TASK013_INDEPENDENT_READBACK.json")
        self.assertEqual(hist["receipt_identity"], "TASK013_HISTORICAL_RESTORED")
        self.assertTrue(hist["historical"])
        self.assertEqual(hist["head"], "deab9ea507ec1042df533b1aa7be0123ae13c823")
        self.assertEqual(hist["package_sha256"], "17cbe722f1fe85b595a7ce820394f7d1e0392e69c4f06b9a8d3c2ac94c71b5aa")


class G5InputManifestTests(unittest.TestCase):
    def test_manifest_complete_and_hashes_match(self) -> None:
        manifest = read_json(REVIEW / "HG-KSEOS_EXTERNAL_ACCEPTANCE_INPUT_MANIFEST.json")
        roles = {e["role"] for e in manifest["inputs"]}
        self.assertIn("test_denominator", roles)
        self.assertIn("coverage_reducer", roles)
        self.assertIn("user_experience_reducer", roles)
        self.assertIn("tst092", roles)
        self.assertIn("package_readback", roles)
        for e in manifest["inputs"]:
            p = ROOT / e["path"]
            self.assertTrue(p.is_file(), e["path"])
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), e["sha256"], e["role"])

    def test_acceptance_binds_manifest(self) -> None:
        acc = read_json(REVIEW / "HG-KSEOS_EXTERNAL_FINAL_ACCEPTANCE.json")
        self.assertEqual(acc["input_manifest"]["path"],
                         "evidence/review/HG-KSEOS_EXTERNAL_ACCEPTANCE_INPUT_MANIFEST.json")
        m = read_json(REVIEW / "HG-KSEOS_EXTERNAL_ACCEPTANCE_INPUT_MANIFEST.json")
        self.assertEqual(acc["input_manifest"]["sha256"],
                         hashlib.sha256((REVIEW / "HG-KSEOS_EXTERNAL_ACCEPTANCE_INPUT_MANIFEST.json").read_bytes()).hexdigest())
        self.assertEqual(m["current_changeset_task_id"], TASK)


class G6CrossArtifactTests(unittest.TestCase):
    def test_cross_artifact_checker_pass(self) -> None:
        ck = read_json(REVIEW / "HG-KSEOS_TASK014_FINAL_CROSS_ARTIFACT_INDEPENDENT_CHECK.json")
        self.assertEqual(ck["verdict"], "PASS")
        for k, v in ck["checks"].items():
            if isinstance(v, bool):
                self.assertTrue(v, k)

    def test_acceptance_coherence_predicates(self) -> None:
        acc = read_json(REVIEW / "HG-KSEOS_EXTERNAL_FINAL_ACCEPTANCE.json")
        preds = {e["id"]: e["pass"] for e in acc["hard_check_evaluations"]}
        for cid in ("hard_check_ids_unique",
                    "current_test_denominator_task_matches_current_changeset",
                    "current_test_denominator_head_matches_candidate",
                    "tst092_receipt_task_matches_current_changeset",
                    "tst092_receipt_head_matches_candidate",
                    "tst092_receipt_package_matches_candidate",
                    "acceptance_input_manifest_complete",
                    "acceptance_input_hashes_match",
                    "historical_receipts_immutable",
                    # F3: the six Final-MD cross-artifact predicates
                    "final_md_external_acceptance_status_matches",
                    "final_md_external_acceptance_counts_match",
                    "final_md_test_denominator_matches",
                    "final_md_current_changeset_matches",
                    "final_md_current_head_matches",
                    "final_md_current_package_matches"):
            self.assertTrue(preds.get(cid), cid)


class GuideAndDeterminismTests(unittest.TestCase):
    def test_guide_validator_pass(self) -> None:
        gv = read_json(REVIEW / "HG-KSEOS_USER_GUIDE_CURRENT_RUNTIME_READBACK.json")
        self.assertEqual(gv["verdict"], "PASS")
        for k, v in gv["checks"].items():
            self.assertEqual(v["verdict"], "PASS", k)

    def test_guide_maker_root_zero_and_stale_zero(self) -> None:
        gv = read_json(REVIEW / "HG-KSEOS_USER_GUIDE_CURRENT_RUNTIME_READBACK.json")
        self.assertEqual(gv["checks"]["current_operational_maker_root_occurrences"]["actual"], 0)
        self.assertEqual(gv["checks"]["user_guide_stale_current_claim_count"]["actual"], 0)
        self.assertTrue(gv["checks"]["maker_root_current_zero"]["verdict"] == "PASS")
        self.assertTrue(gv["checks"]["user_guide_no_stale_current_claims"]["verdict"] == "PASS")

    def test_final_md_guide_projection_matches_actual_guide(self) -> None:
        md = (REVIEW / "HG-KSEOS_FINAL_EVIDENCE_FOR_REVIEW.md").read_text(encoding="utf-8")
        ab = md.split("## AB. Task-014 Final External Evidence Coherence Closure")[-1]
        import hashlib
        guide = (ROOT / "docs" / "HG-KSEOS使用說明文檔.md").read_bytes()
        self.assertIn(hashlib.sha256(guide).hexdigest(), ab)
        self.assertIn("stale_current_claim_count=0", ab)

    def test_guide_current_claim_is_task015(self) -> None:
        guide = (ROOT / "docs" / "HG-KSEOS使用說明文檔.md").read_text(encoding="utf-8")
        self.assertIn("Current changeset = **Task-015**", guide)
        self.assertNotIn("Current changeset = **Task-014**", guide)
        self.assertNotIn("Current changeset = **Task-013**", guide)

    def test_determinism_acceptance(self) -> None:
        d = read_json(REVIEW / "HG-KSEOS_FINAL_CLOSURE_GENERATOR_DETERMINISM_ACCEPTANCE.json")
        self.assertEqual(d["verdict"], "PASS")
        for name, r in d["results"].items():
            self.assertTrue(r["deterministic"], name)

    def test_coherence_baseline_records_gaps(self) -> None:
        b = read_json(REVIEW / "HG-KSEOS_TASK014_FINAL_COHERENCE_BASELINE.json")
        self.assertGreaterEqual(len(b["known_coherence_gaps"]), 6)
        self.assertTrue(b["final_md_sha256"])


if __name__ == "__main__":
    unittest.main()
