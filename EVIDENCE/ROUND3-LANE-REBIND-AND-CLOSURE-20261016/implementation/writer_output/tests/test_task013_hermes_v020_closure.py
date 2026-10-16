"""Task-013 regression tests: Hermes v0.20 qualification evidence closure.

Deterministic product-side checks for the Task-013 ChangeSet:
- Gate-0: Final Evidence Section W promotion policy must be source-resolved
  (COV-11-06) and consistent with Section Y — the stale
  "LOW = auto + independent checker + rollback" tiering is forbidden.
- The 13 Hermes-v0.20 evidence artifacts exist, parse, and carry the
  mandatory invariants (exact identity, zero duplicate runtime owners,
  provider/model preservation, explicit fail-closed approvals, rollback).
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")

EXPECTED_V020_COMMIT = "3c27eb6234bf91b8ceee9e9071591b31e9b148cb"
EXPECTED_V020_TAG = "v2026.8.3"
EXPECTED_V020_VERSION = "0.20.0"

EVIDENCE_FILES = [
    "HG-KSEOS_HERMES_V020_IDENTITY_READBACK.json",
    "HG-KSEOS_HERMES_V0182_TO_V020_CAPABILITY_DELTA.json",
    "HG-KSEOS_HERMES_V020_REUSE_BINDING_MATRIX.json",
    "HG-KSEOS_HERMES_V020_WINDOWS_QUALIFICATION.json",
    "HG-KSEOS_HERMES_V020_PROVIDER_ROUTE_ACCEPTANCE.json",
    "HG-KSEOS_HERMES_V020_KANBAN_ACCEPTANCE.json",
    "HG-KSEOS_HERMES_V020_GOAL_CONTRACT_ACCEPTANCE.json",
    "HG-KSEOS_HERMES_V020_TOOL_RECOVERY_ACCEPTANCE.json",
    "HG-KSEOS_HERMES_V020_APPROVALS_ACCEPTANCE.json",
    "HG-KSEOS_HERMES_V020_COMPRESSION_ACCEPTANCE.json",
    "HG-KSEOS_HERMES_V020_SKILL_GOVERNANCE_ACCEPTANCE.json",
    "HG-KSEOS_HERMES_V020_ROLLBACK_ACCEPTANCE.json",
    "HG-KSEOS_HERMES_V020_INDEPENDENT_ACCEPTANCE.json",
]


def read_json(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


class Gate0PolicySemanticsTests(unittest.TestCase):
    """Section W must be source-resolved, not the stale implementation tiering."""

    def test_section_w_no_stale_auto_tiering(self) -> None:
        final_md = (ROOT / "evidence/review/HG-KSEOS_FINAL_EVIDENCE_FOR_REVIEW.md").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("LOW = auto + independent checker + rollback", final_md)
        self.assertNotIn("MEDIUM = checker + human-if-authority-requires", final_md)

    def test_section_w_cites_cov_11_06_and_human_policy_owner(self) -> None:
        final_md = (ROOT / "evidence/review/HG-KSEOS_FINAL_EVIDENCE_FOR_REVIEW.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("COV-11-06", final_md)
        self.assertIn("Human Policy Owner", final_md)
        self.assertIn("PROMOTION_READY_HITL_SOURCE_REQUIRED", final_md)

    def test_section_w_consistent_with_section_y(self) -> None:
        final_md = (ROOT / "evidence/review/HG-KSEOS_FINAL_EVIDENCE_FOR_REVIEW.md").read_text(
            encoding="utf-8"
        )
        # W and Y (and Z) must agree: promotion requires independent verifier +
        # Human Policy Owner; no implementation-invented auto-promotion.
        self.assertGreaterEqual(final_md.count("no implementation-invented auto-promotion"), 2)

    def test_cov_11_06_source_text_unchanged(self) -> None:
        corpus = ROOT / "HG-KSEOS_實作RBWI_WP_控制工件_PACK_FINAL_r2"
        group01 = next(corpus.glob("*Group-01_Authority_Source_Requirements.md"))
        text = group01.read_text(encoding="utf-8")
        row = [line for line in text.splitlines() if "COV-11-06" in line and "Promotion" in line]
        self.assertEqual(len(row), 1, "exactly one COV-11-06 source row expected")
        self.assertIn("independent verifier", row[0])
        self.assertIn("Human Policy Owner", row[0])


class V020EvidencePresenceTests(unittest.TestCase):
    def test_all_thirteen_evidence_artifacts_exist(self) -> None:
        for name in EVIDENCE_FILES:
            path = ROOT / "evidence" / "review" / name
            self.assertTrue(path.is_file(), f"missing {name}")
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertIn("task_id", payload)
            self.assertEqual(
                payload["task_id"],
                "HGK-HERMES-V020-NATIVE-RUNTIME-REUSE-CONVERGENCE-QUALIFICATION-013",
            )

    def test_identity_exact(self) -> None:
        ident = read_json("evidence/review/HG-KSEOS_HERMES_V020_IDENTITY_READBACK.json")
        v = ident["verifications"]
        self.assertEqual(ident["candidate"]["commit"], EXPECTED_V020_COMMIT)
        self.assertEqual(ident["candidate"]["tag"], EXPECTED_V020_TAG)
        self.assertEqual(ident["candidate"]["version"], EXPECTED_V020_VERSION)
        self.assertEqual(v["git_rev_parse_head"], EXPECTED_V020_COMMIT)
        self.assertEqual(v["git_tag_points_at_head"], EXPECTED_V020_TAG)
        self.assertTrue(v["tag_commit_version_aligned"])
        self.assertFalse(v["floating_main_used"])
        self.assertFalse(v["hermes_update_used_for_promotion"])

    def test_reuse_matrix_zero_duplicates(self) -> None:
        matrix = read_json("evidence/review/HG-KSEOS_HERMES_V020_REUSE_BINDING_MATRIX.json")
        for key in (
            "duplicate_scheduler_remaining",
            "duplicate_worker_dispatcher_remaining",
            "duplicate_runtime_checkpoint_store_remaining",
            "duplicate_provider_proxy_remaining",
            "duplicate_skill_store_remaining",
        ):
            self.assertEqual(matrix[key], 0, key)
        for entry in matrix["entries"]:
            self.assertIn(entry["decision"],
                          {"HGK_NORMATIVE", "REUSE_HERMES", "ADAPTER", "DUPLICATE_TO_REMOVE", "DEFERRED_NOT_REQUIRED"})
            self.assertFalse(entry["duplicate_runtime_found"], entry["capability"])

    def test_provider_route_preserved(self) -> None:
        prov = read_json("evidence/review/HG-KSEOS_HERMES_V020_PROVIDER_ROUTE_ACCEPTANCE.json")
        self.assertEqual(prov["provider"], "opencode-go")
        self.assertEqual(prov["model"], "deepseek-v4-flash")
        self.assertTrue(prov["preserved_from_v0182"])
        self.assertFalse(prov["openai_fallback"])
        self.assertEqual(prov["unadmitted_provider"], 0)
        self.assertFalse(prov["model_silently_switched"])

    def test_approvals_explicit_fail_closed(self) -> None:
        appr = read_json("evidence/review/HG-KSEOS_HERMES_V020_APPROVALS_ACCEPTANCE.json")
        self.assertEqual(appr["mode"], "manual")
        self.assertTrue(appr["mode_explicit"])
        self.assertTrue(appr["fail_closed"])
        self.assertTrue(appr["runtime_fail_closed"]["agent_refused_bypass"])

    def test_independent_acceptance_pass(self) -> None:
        indep = read_json("evidence/review/HG-KSEOS_HERMES_V020_INDEPENDENT_ACCEPTANCE.json")
        self.assertEqual(indep["verdict"], "PASS")
        self.assertTrue(indep["hermes_v020_identity_exact"])
        self.assertTrue(indep["provider_model_unchanged"])
        self.assertTrue(indep["rollback_v0182_verified"])
        self.assertTrue(indep["promotion_authority_still_hgk"])

    def test_windows_qualification_all_gates_pass(self) -> None:
        qual = read_json("evidence/review/HG-KSEOS_HERMES_V020_WINDOWS_QUALIFICATION.json")
        self.assertEqual(qual["verdict"], "PASS")
        for q in ("q01_identity", "q02_doctor", "q04_provider", "q05_workorder_route",
                  "q06_kanban_basic", "q07_kanban_dependency", "q08_kanban_block",
                  "q09_kanban_retry", "q10_kanban_heartbeat_reclaim", "q11_kanban_worktree",
                  "q12_goal", "q13_goal_contract", "q14_goal_resume", "q15_tool_recovery",
                  "q16_compression", "q17_approvals", "q18_deepseek_cache",
                  "q19_skill_mechanism", "q20_rollback"):
            self.assertEqual(qual[q]["result"], "PASS", q)


if __name__ == "__main__":
    unittest.main()
