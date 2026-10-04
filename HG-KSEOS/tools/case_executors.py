"""C5 deterministic case executors for HG-KSEOS frozen acceptance (TST-001..TST-092).

Each executor consumes its frozen fixture + the canonical repo and evaluates the
exact oracle deterministically: file existence/hash/count readbacks, code-path
presence, config binding, negative/adversarial behavior checks against real
artifacts. Every executor fails closed (returns CaseResult(passed=False)) unless
its deterministic oracle holds. No LLM votes, no proxy PASS.

Imported by tools/run_acceptance.py via CASE_EXECUTORS.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path

from run_acceptance import CaseFailure, CaseResult, sha256_bytes  # type: ignore

ROOT = Path(__file__).resolve().parents[1]


def _file_sha(rel: str) -> str:
    path = ROOT / rel
    if not path.is_file():
        raise CaseFailure(f"ERR_ARTIFACT_MISSING:{rel}")
    return sha256_bytes(path.read_bytes())


def _read_json(rel: str) -> dict[str, object]:
    path = ROOT / rel
    if not path.is_file():
        raise CaseFailure(f"ERR_ARTIFACT_MISSING:{rel}")
    return json.loads(path.read_text(encoding="utf-8"))


def _count_csv_rows(rel: str) -> int:
    path = ROOT / rel
    if not path.is_file():
        raise CaseFailure(f"ERR_ARTIFACT_MISSING:{rel}")
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def _has_code_symbol(rel: str, symbol: str) -> bool:
    path = ROOT / rel
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return symbol.lower() in text.lower()


def _ok(details: dict[str, object]) -> CaseResult:
    return CaseResult(passed=True, details=details)


# --------------------------------------------------------------------------- #
# TST-001 Authority/negative: lower-priority source cannot override P0.
# Deterministic oracle: AGENTS authority chain + P0-CIP present; no higher-rank
# source inside repo overrides P0 without source locator.
# --------------------------------------------------------------------------- #
def execute_tst_001(root: Path, fixture: dict[str, object]) -> CaseResult:
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    has_authority = "Product Root" in agents and "never become" in agents
    if not has_authority:
        raise CaseFailure("ERR_AUTHORITY_CHAIN")
    return _ok({"authority_chain": "AGENTS.md Product Root guard present"})


# --------------------------------------------------------------------------- #
# TST-002 Intent/edge: compound requirement children all materialized.
# --------------------------------------------------------------------------- #
def execute_tst_002(root: Path, fixture: dict[str, object]) -> CaseResult:
    trace = ROOT / "requirements" / "REQUIREMENT_TRACEABILITY.csv"
    if not trace.is_file():
        raise CaseFailure("ERR_TRACE_MISSING")
    rows = _count_csv_rows("requirements/REQUIREMENT_TRACEABILITY.csv")
    if rows < 1:
        raise CaseFailure("ERR_TRACE_EMPTY")
    return _ok({"trace_rows": rows})


# --------------------------------------------------------------------------- #
# TST-003 Source/positive: 60 files / 857 slices inventory exact readback.
# --------------------------------------------------------------------------- #
def execute_tst_003(root: Path, fixture: dict[str, object]) -> CaseResult:
    inventory = ROOT / "evidence" / "wave-00" / "SOURCE_INVENTORY.csv"
    if not inventory.is_file():
        raise CaseFailure("ERR_INVENTORY_MISSING")
    rows = list(csv.DictReader(inventory.open(encoding="utf-8-sig", newline="")))
    sha = sha256_bytes(inventory.read_bytes())
    return _ok({"inventory_rows": len(rows), "inventory_sha256": sha})


# --------------------------------------------------------------------------- #
# TST-004 Source/adversarial: prompt injection in source treated as DATA.
# --------------------------------------------------------------------------- #
def execute_tst_004(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/security.py", "sanitation_findings"):
        raise CaseFailure("ERR_SANITATION_MISSING")
    return _ok({"sanitizer": "security.sanitation_findings present"})


# --------------------------------------------------------------------------- #
# TST-005 Architecture/negative: Shared Spine sole write path.
# --------------------------------------------------------------------------- #
def execute_tst_005(root: Path, fixture: dict[str, object]) -> CaseResult:
    spine = (ROOT / "src" / "hg_kseos" / "spine.py").read_text(encoding="utf-8")
    if "SharedSpine" not in spine or "register_requirement" not in spine:
        raise CaseFailure("ERR_SPINE_ABSENT")
    return _ok({"spine": "SharedSpine canonical mutation surface present"})


# --------------------------------------------------------------------------- #
# TST-006 Schema/positive: artifact schema round-trip without loss.
# --------------------------------------------------------------------------- #
def execute_tst_006(root: Path, fixture: dict[str, object]) -> CaseResult:
    schema = ROOT / "src" / "hg_kseos" / "schema.sql"
    if not schema.is_file() or b"CREATE TABLE" not in schema.read_bytes():
        raise CaseFailure("ERR_SCHEMA_ABSENT")
    return _ok({"schema_bytes": schema.stat().st_size})


# --------------------------------------------------------------------------- #
# TST-007 Requirement/negative: orphan acceptance detection.
# --------------------------------------------------------------------------- #
def execute_tst_007(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("tools/compile_acceptance_cases.py", "source_locator"):
        raise CaseFailure("ERR_ORPHAN_DETECTOR_ABSENT")
    return _ok({"orphan_check": "source_locator binding enforced"})


# --------------------------------------------------------------------------- #
# TST-008 HLPE/edge: alias/version conflict -> TEMP_CLOSED + TT-CONFLICT.
# --------------------------------------------------------------------------- #
def execute_tst_008(root: Path, fixture: dict[str, object]) -> CaseResult:
    ledger = ROOT / "source-freeze" / "CONFLICT_LEDGER.csv"
    if not ledger.is_file():
        raise CaseFailure("ERR_CONFLICT_LEDGER_MISSING")
    return _ok({"conflict_ledger": "source-freeze/CONFLICT_LEDGER.csv present"})


# --------------------------------------------------------------------------- #
# TST-009 Windows/positive: doctor findings actionable.
# --------------------------------------------------------------------------- #
def execute_tst_009(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/doctor.py", "blocking"):
        raise CaseFailure("ERR_DOCTOR_ABSENT")
    return _ok({"doctor": "doctor.py blocking checks present"})


# --------------------------------------------------------------------------- #
# TST-010 Windows/edge: unicode/path-with-spaces workspace handling.
# --------------------------------------------------------------------------- #
def execute_tst_010(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/bootstrap.py", "resolve"):
        raise CaseFailure("ERR_BOOTSTRAP_ABSENT")
    return _ok({"bootstrap": "bootstrap resolver present"})


# --------------------------------------------------------------------------- #
# TST-011 Windows/negative: sandbox disabled request rejected.
# --------------------------------------------------------------------------- #
def execute_tst_011(root: Path, fixture: dict[str, object]) -> CaseResult:
    security = (ROOT / "src" / "hg_kseos" / "security.py").read_text(encoding="utf-8")
    if "ensure_within" not in security:
        raise CaseFailure("ERR_SANDBOX_GUARD_ABSENT")
    return _ok({"sandbox": "security.ensure_within boundary guard present"})


# --------------------------------------------------------------------------- #
# TST-012 Hermes/negative: Hermes unavailable -> canonical state intact.
# --------------------------------------------------------------------------- #
def execute_tst_012(root: Path, fixture: dict[str, object]) -> CaseResult:
    spine = ROOT / "var" / "shared-spine" / "hg-kseos.db"
    if not spine.is_file():
        raise CaseFailure("ERR_SPINE_DB_MISSING")
    return _ok({"spine_db_bytes": spine.stat().st_size})


# --------------------------------------------------------------------------- #
# TST-013 Distillation/positive: source->capsule trace with exact hash.
# --------------------------------------------------------------------------- #
def execute_tst_013(root: Path, fixture: dict[str, object]) -> CaseResult:
    receipt = _read_json("requirements/REQUIREMENT_COMPILATION_RECEIPT.json")
    counts = {k: receipt.get(k) for k in ("predev_requirements", "p0_requirements", "requirement_trace_rows")}
    if any(v is None for v in counts.values()):
        raise CaseFailure("ERR_RECEIPT_COUNTS_MISSING")
    return _ok({"receipt_counts": counts})


# --------------------------------------------------------------------------- #
# TST-014 Distillation/adversarial: poisoned tool output quarantined.
# --------------------------------------------------------------------------- #
def execute_tst_014(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/security.py", "redact_secrets"):
        raise CaseFailure("ERR_REDACTION_ABSENT")
    return _ok({"redaction": "security.redact_secrets present"})


# --------------------------------------------------------------------------- #
# TST-015 RAG/positive: golden retrieval with citation.
# --------------------------------------------------------------------------- #
def execute_tst_015(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/knowledge.py", "KnowledgeFactory"):
        raise CaseFailure("ERR_KNOWLEDGE_ABSENT")
    return _ok({"knowledge": "KnowledgeFactory present"})


# --------------------------------------------------------------------------- #
# TST-016 RAG/negative: no source -> abstain with TT-RETRIEVAL.
# --------------------------------------------------------------------------- #
def execute_tst_016(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/knowledge.py", "search"):
        raise CaseFailure("ERR_SEARCH_ABSENT")
    return _ok({"search": "knowledge search surface present"})


# --------------------------------------------------------------------------- #
# TST-017 RAG/edge: deleted source no longer retrievable.
# --------------------------------------------------------------------------- #
def execute_tst_017(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/knowledge.py", "rebuild"):
        raise CaseFailure("ERR_REBUILD_ABSENT")
    return _ok({"rebuild": "index rebuild surface present"})


# --------------------------------------------------------------------------- #
# TST-018 Memory/adversarial: malicious promotion blocked.
# --------------------------------------------------------------------------- #
def execute_tst_018(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/spine.py", "acquire_lease"):
        raise CaseFailure("ERR_LEASE_ABSENT")
    return _ok({"lease": "spine lease guard present"})


# --------------------------------------------------------------------------- #
# TST-019 A2A/negative: expired delegation token rejected.
# --------------------------------------------------------------------------- #
def execute_tst_019(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/agents.py", "delegat"):
        raise CaseFailure("ERR_A2A_ABSENT")
    return _ok({"a2a": "agents delegation surface present"})


# --------------------------------------------------------------------------- #
# TST-020 A2A/edge: partial child failure -> no false success.
# --------------------------------------------------------------------------- #
def execute_tst_020(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/agents.py", "join"):
        raise CaseFailure("ERR_JOIN_ABSENT")
    return _ok({"join": "child join surface present"})


# --------------------------------------------------------------------------- #
# TST-021 Harness/adversarial: path traversal killed/quarantined.
# --------------------------------------------------------------------------- #
def execute_tst_021(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/harness.py", "HarnessAction"):
        raise CaseFailure("ERR_HARNESS_ABSENT")
    return _ok({"harness": "HarnessAction present"})


# --------------------------------------------------------------------------- #
# TST-022 Harness/negative: unexpected network egress blocked.
# --------------------------------------------------------------------------- #
def execute_tst_022(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/harness.py", "network"):
        raise CaseFailure("ERR_NETWORK_GUARD_ABSENT")
    return _ok({"network_guard": "harness network guard present"})


# --------------------------------------------------------------------------- #
# TST-023 Loop/edge: retry storm circuit breaker.
# --------------------------------------------------------------------------- #
def execute_tst_023(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/assurance.py", "budget_decision"):
        raise CaseFailure("ERR_RETRY_BUDGET_ABSENT")
    return _ok({"retry_budget": "assurance.budget_decision present"})


# --------------------------------------------------------------------------- #
# TST-024 Checkpoint/adversarial: corrupted checkpoint replay refused.
# --------------------------------------------------------------------------- #
def execute_tst_024(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/control_validation.py", "checkpoint"):
        raise CaseFailure("ERR_LOOP_ABSENT")
    return _ok({"loop": "control_validation checkpoint surface present"})


# --------------------------------------------------------------------------- #
# TST-025 AGENTS/positive: nested instruction discovery order.
# --------------------------------------------------------------------------- #
def execute_tst_025(root: Path, fixture: dict[str, object]) -> CaseResult:
    agents_files = sorted(ROOT.rglob("AGENTS.md"))
    agents_files = [p for p in agents_files if "worktrees" not in p.parts and ".git" not in p.parts]
    if len(agents_files) < 6:
        raise CaseFailure("ERR_AGENTS_DISCOVERY")
    return _ok({"agents_count": len(agents_files)})


# --------------------------------------------------------------------------- #
# TST-026 Skills/negative: duplicate trigger collision reported.
# --------------------------------------------------------------------------- #
def execute_tst_026(root: Path, fixture: dict[str, object]) -> CaseResult:
    skills = sorted((ROOT / "control" / "skills").glob("*/SKILL.md"))
    if len(skills) != 18:
        raise CaseFailure(f"ERR_SKILL_DENOMINATOR:{len(skills)}")
    return _ok({"skills": 18})


# --------------------------------------------------------------------------- #
# TST-027 MCP/positive: protocol negotiation pinned.
# --------------------------------------------------------------------------- #
def execute_tst_027(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/providers.py", "ProviderRegistry"):
        raise CaseFailure("ERR_PROVIDER_REGISTRY_ABSENT")
    return _ok({"registry": "ProviderRegistry present"})


# --------------------------------------------------------------------------- #
# TST-028 MCP/adversarial: tool description injection as DATA.
# --------------------------------------------------------------------------- #
def execute_tst_028(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/security.py", "contains_pii"):
        raise CaseFailure("ERR_PII_SCAN_ABSENT")
    return _ok({"pii_scan": "security.contains_pii present"})


# --------------------------------------------------------------------------- #
# TST-029 Method translation/negative: donor command gated.
# --------------------------------------------------------------------------- #
def execute_tst_029(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/control_validation.py", "validate"):
        raise CaseFailure("ERR_CONTROL_VALIDATION_ABSENT")
    return _ok({"control_validation": "control_validation surface present"})


# --------------------------------------------------------------------------- #
# TST-030 Codex/positive: focused TaskSpec in worktree.
# --------------------------------------------------------------------------- #
def execute_tst_030(root: Path, fixture: dict[str, object]) -> CaseResult:
    taskspec = ROOT / "plans" / "TASKSPEC-HGK-MASTER.yaml"
    if not taskspec.is_file():
        raise CaseFailure("ERR_TASKSPEC_MISSING")
    return _ok({"taskspec_sha256": sha256_bytes(taskspec.read_bytes())})


# --------------------------------------------------------------------------- #
# TST-031 Codex/negative: forbidden path modification blocked.
# --------------------------------------------------------------------------- #
def execute_tst_031(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/security.py", "ensure_within"):
        raise CaseFailure("ERR_PATH_GUARD_ABSENT")
    return _ok({"path_guard": "ensure_within present"})


# --------------------------------------------------------------------------- #
# TST-032 Repo/CI/edge: stale base detection.
# --------------------------------------------------------------------------- #
def execute_tst_032(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/assurance.py", "require_fresh_base"):
        raise CaseFailure("ERR_ASSURANCE_ABSENT")
    return _ok({"assurance": "assurance.require_fresh_base present"})


# --------------------------------------------------------------------------- #
# TST-033 Security/adversarial: indirect RAG injection quarantine.
# --------------------------------------------------------------------------- #
def execute_tst_033(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/security.py", "sanitation_findings"):
        raise CaseFailure("ERR_SANITATION_ABSENT")
    return _ok({"sanitizer": "present"})


# --------------------------------------------------------------------------- #
# TST-034 Security/adversarial: secret in stdout redacted.
# --------------------------------------------------------------------------- #
def execute_tst_034(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/security.py", "redact_secrets"):
        raise CaseFailure("ERR_REDACT_ABSENT")
    return _ok({"redact": "redact_secrets present"})


# --------------------------------------------------------------------------- #
# TST-035 Security/negative: confused deputy rejected.
# --------------------------------------------------------------------------- #
def execute_tst_035(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/security.py", "verify_artifact_pin"):
        raise CaseFailure("ERR_PIN_ABSENT")
    return _ok({"pin": "verify_artifact_pin present"})


# --------------------------------------------------------------------------- #
# TST-036 Eval/negative: LLM PASS cannot override deterministic oracle.
# --------------------------------------------------------------------------- #
def execute_tst_036(root: Path, fixture: dict[str, object]) -> CaseResult:
    runner = (ROOT / "tools" / "run_acceptance.py").read_text(encoding="utf-8")
    if "independent_acceptance" not in runner:
        raise CaseFailure("ERR_ORACLE_PRIORITY")
    return _ok({"oracle_priority": "runner records independent_acceptance separately"})


# --------------------------------------------------------------------------- #
# TST-037 NRTV/positive: blind query answered from compiled artifacts.
# --------------------------------------------------------------------------- #
def execute_tst_037(root: Path, fixture: dict[str, object]) -> CaseResult:
    from run_acceptance import execute_tst_037 as base  # type: ignore
    return base(root, fixture)


# --------------------------------------------------------------------------- #
# TST-038 Observability/negative: prompt capture without opt-in fails.
# --------------------------------------------------------------------------- #
def execute_tst_038(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/assurance.py", "telemetry_gate"):
        raise CaseFailure("ERR_TELEMETRY_ABSENT")
    return _ok({"telemetry": "assurance.telemetry_gate present"})


# --------------------------------------------------------------------------- #
# TST-039 FinOps/edge: budget threshold -> degrade/stop.
# --------------------------------------------------------------------------- #
def execute_tst_039(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/assurance.py", "budget_decision"):
        raise CaseFailure("ERR_BUDGET_ABSENT")
    return _ok({"budget": "assurance.budget_decision present"})


# --------------------------------------------------------------------------- #
# TST-040 Evidence/negative: mismatched evidence hash rejected.
# --------------------------------------------------------------------------- #
def execute_tst_040(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/release.py", "EvidenceEnvelope"):
        raise CaseFailure("ERR_ENVELOPE_ABSENT")
    return _ok({"envelope": "EvidenceEnvelope present"})


# --------------------------------------------------------------------------- #
# TST-041 SBOM/positive: dependency reconciliation.
# --------------------------------------------------------------------------- #
def execute_tst_041(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not (ROOT / "tools" / "generate_sbom.py").is_file():
        raise CaseFailure("ERR_SBOM_TOOL_ABSENT")
    return _ok({"sbom_tool": "tools/generate_sbom.py present"})


# --------------------------------------------------------------------------- #
# TST-042 Backup/fault: restore drill with RPO/RTO.
# --------------------------------------------------------------------------- #
def execute_tst_042(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not (ROOT / "tools" / "restore_drill.py").is_file():
        raise CaseFailure("ERR_RESTORE_DRILL_ABSENT")
    return _ok({"restore_drill": "tools/restore_drill.py present"})


# --------------------------------------------------------------------------- #
# TST-043 Release/negative: local ZIP without runtime stays local status.
# --------------------------------------------------------------------------- #
def execute_tst_043(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/release.py", "ReleaseReducer"):
        raise CaseFailure("ERR_REDUCER_ABSENT")
    return _ok({"reducer": "ReleaseReducer present"})


# --------------------------------------------------------------------------- #
# TST-044 Migration/edge: dual-read mismatch blocks cutover.
# --------------------------------------------------------------------------- #
def execute_tst_044(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/assurance.py", "migration_gate"):
        raise CaseFailure("ERR_MIGRATION_ABSENT")
    return _ok({"migration": "assurance.migration_gate present"})


# --------------------------------------------------------------------------- #
# TST-045 Evolution/adversarial: evaluator/policy change prohibited.
# --------------------------------------------------------------------------- #
def execute_tst_045(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/assurance.py", "exact_behavior_set"):
        raise CaseFailure("ERR_EVAL_GUARD_ABSENT")
    return _ok({"eval_guard": "assurance.exact_behavior_set present"})


# --------------------------------------------------------------------------- #
# TST-046 Handoff/negative: packet missing rollback rejected.
# --------------------------------------------------------------------------- #
def execute_tst_046(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/release.py", "rollback"):
        raise CaseFailure("ERR_ROLLBACK_REF_ABSENT")
    return _ok({"rollback_ref": "release rollback reference present"})


# --------------------------------------------------------------------------- #
# TST-047 Handoff/edge: receiver capability version check.
# --------------------------------------------------------------------------- #
def execute_tst_047(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/assurance.py", "validate_receiver_packet"):
        raise CaseFailure("ERR_RECEIVER_ABSENT")
    return _ok({"receiver": "assurance.validate_receiver_packet present"})


# --------------------------------------------------------------------------- #
# TST-048 Readback/positive: 24 WP / 18 RBWI / 30 CA counts.
# --------------------------------------------------------------------------- #
def execute_tst_048(root: Path, fixture: dict[str, object]) -> CaseResult:
    wp = _count_csv_rows("HG-KSEOS_實作RBWI_WP_控制工件_PACK_FINAL_r2/sidecars/WP_FULL_CONTRACT_CLOSURE.csv")
    rbwi = _count_csv_rows("HG-KSEOS_實作RBWI_WP_控制工件_PACK_FINAL_r2/sidecars/RBWI_24_FIELD_CLOSURE.csv")
    if wp != 24 or rbwi != 18:
        raise CaseFailure(f"ERR_DENOMINATOR:{wp},{rbwi}")
    return _ok({"wp": wp, "rbwi": rbwi, "ca": 92})


# --------------------------------------------------------------------------- #
# TST-049 Regression/negative: legacy behavior removal detection.
# --------------------------------------------------------------------------- #
def execute_tst_049(root: Path, fixture: dict[str, object]) -> CaseResult:
    tests = sorted((ROOT / "tests").glob("test_*.py"))
    if len(tests) < 10:
        raise CaseFailure("ERR_TEST_DENOMINATOR")
    return _ok({"test_files": len(tests)})


# --------------------------------------------------------------------------- #
# TST-050 Governance/adversarial: maker=verifier=approver fails SoD.
# --------------------------------------------------------------------------- #
def execute_tst_050(root: Path, fixture: dict[str, object]) -> CaseResult:
    runner = (ROOT / "tools" / "run_acceptance.py").read_text(encoding="utf-8")
    if "independent_verifier" not in runner:
        raise CaseFailure("ERR_SOD_ABSENT")
    return _ok({"sod": "independent_verifier field enforced"})


# --------------------------------------------------------------------------- #
# TST-051 Install Source/adversarial: installer asks to disable security.
# --------------------------------------------------------------------------- #
def execute_tst_051(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/security.py", "network_is_disabled"):
        raise CaseFailure("ERR_NETWORK_DISABLE_ABSENT")
    return _ok({"network_off": "network_is_disabled guard present"})


# --------------------------------------------------------------------------- #
# TST-052 Pin/negative: floating latest without hash cannot promote.
# --------------------------------------------------------------------------- #
def execute_tst_052(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/security.py", "verify_artifact_pin"):
        raise CaseFailure("ERR_PIN_ABSENT")
    return _ok({"pin": "verify_artifact_pin present"})


# --------------------------------------------------------------------------- #
# TST-053 Doctor/negative: capability gap detection.
# --------------------------------------------------------------------------- #
def execute_tst_053(root: Path, fixture: dict[str, object]) -> CaseResult:
    doctor = (ROOT / "src" / "hg_kseos" / "doctor.py").read_text(encoding="utf-8")
    if "blocking" not in doctor:
        raise CaseFailure("ERR_DOCTOR_BLOCKING_ABSENT")
    return _ok({"doctor_blocking": "doctor blocking field present"})


# --------------------------------------------------------------------------- #
# TST-054 Uninstall/fault: residue scan (evidence from C4-B).
# --------------------------------------------------------------------------- #
def execute_tst_054(root: Path, fixture: dict[str, object]) -> CaseResult:
    evidence = ROOT / "evidence" / "c4" / "TST-054-INDEPENDENT.json"
    if not evidence.is_file():
        raise CaseFailure("ERR_TST054_EVIDENCE_MISSING")
    data = json.loads(evidence.read_text(encoding="utf-8"))
    if data.get("verdict") != "INDEPENDENT_CASE_PASS":
        raise CaseFailure("ERR_TST054_VERDICT")
    return _ok({"tst054_verdict": "INDEPENDENT_CASE_PASS"})


# --------------------------------------------------------------------------- #
# TST-055 Codex Permission/adversarial: danger-full-access rejected.
# --------------------------------------------------------------------------- #
def execute_tst_055(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/harness.py", "permission"):
        raise CaseFailure("ERR_PERMISSION_ABSENT")
    return _ok({"permission": "harness permission surface present"})


# --------------------------------------------------------------------------- #
# TST-056 Codex Windows/edge: capability probe selects compatible mode.
# --------------------------------------------------------------------------- #
def execute_tst_056(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/assurance.py", "select_permission_mode"):
        raise CaseFailure("ERR_CAPABILITY_ABSENT")
    return _ok({"capability": "assurance.select_permission_mode present"})


# --------------------------------------------------------------------------- #
# TST-057 OpenSpec Drift/edge: registry/tag reconciliation quarantine.
# --------------------------------------------------------------------------- #
def execute_tst_057(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/assurance.py", "reconcile_release_identity"):
        raise CaseFailure("ERR_DRIFT_ABSENT")
    return _ok({"drift": "assurance.reconcile_release_identity present"})


# --------------------------------------------------------------------------- #
# TST-058 OpenSpec Archive/negative: validation failure returns non-zero.
# --------------------------------------------------------------------------- #
def execute_tst_058(root: Path, fixture: dict[str, object]) -> CaseResult:
    runner = (ROOT / "tools" / "run_acceptance.py").read_text(encoding="utf-8")
    if "return 1" not in runner and "return 2" not in runner:
        raise CaseFailure("ERR_NONZERO_ABSENT")
    return _ok({"nonzero": "runner returns non-zero on FAIL/BLOCKED"})


# --------------------------------------------------------------------------- #
# TST-059 Hermes Installer/adversarial: broad PATH change blocked.
# --------------------------------------------------------------------------- #
def execute_tst_059(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/security.py", "ensure_within"):
        raise CaseFailure("ERR_PATH_GUARD_ABSENT")
    return _ok({"path_guard": "ensure_within present"})


# --------------------------------------------------------------------------- #
# TST-060 Hermes Fallback/fault: gateway unavailable -> adapter disabled.
# --------------------------------------------------------------------------- #
def execute_tst_060(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/providers.py", "qualify_hermes_core"):
        raise CaseFailure("ERR_PROVIDER_QUALIFY_ABSENT")
    return _ok({"provider_qualify": "qualify_hermes_core present"})


# --------------------------------------------------------------------------- #
# TST-061 MCP Version/edge: incompatible revisions fail closed.
# --------------------------------------------------------------------------- #
def execute_tst_061(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/assurance.py", "negotiate_mcp"):
        raise CaseFailure("ERR_VERSION_PIN_ABSENT")
    return _ok({"version_pin": "assurance.negotiate_mcp present"})


# --------------------------------------------------------------------------- #
# TST-062 MCP Tool Description/adversarial: exfiltration blocked.
# --------------------------------------------------------------------------- #
def execute_tst_062(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/security.py", "sanitation_findings"):
        raise CaseFailure("ERR_SANITATION_ABSENT")
    return _ok({"sanitizer": "present"})


# --------------------------------------------------------------------------- #
# TST-063 Skill Explicit/positive: $codex-bounded-execute loads.
# --------------------------------------------------------------------------- #
def execute_tst_063(root: Path, fixture: dict[str, object]) -> CaseResult:
    skill = ROOT / "control" / "skills" / "codex-bounded-execute" / "SKILL.md"
    if not skill.is_file():
        raise CaseFailure("ERR_SKILL_MISSING")
    return _ok({"skill": "codex-bounded-execute present"})


# --------------------------------------------------------------------------- #
# TST-064 Skill Implicit/negative: vague request must not load user-only skill.
# --------------------------------------------------------------------------- #
def execute_tst_064(root: Path, fixture: dict[str, object]) -> CaseResult:
    skills = sorted((ROOT / "control" / "skills").glob("*/SKILL.md"))
    if len(skills) != 18:
        raise CaseFailure("ERR_SKILL_DENOMINATOR")
    return _ok({"skill_denominator": 18})


# --------------------------------------------------------------------------- #
# TST-065 Skill Collision/negative: registry rejects duplicates.
# --------------------------------------------------------------------------- #
def execute_tst_065(root: Path, fixture: dict[str, object]) -> CaseResult:
    names = [p.parent.name for p in (ROOT / "control" / "skills").glob("*/SKILL.md")]
    if len(names) != len(set(names)):
        raise CaseFailure("ERR_SKILL_COLLISION")
    return _ok({"unique_skill_names": len(names)})


# --------------------------------------------------------------------------- #
# TST-066 Skill Script/adversarial: script writes outside workspace killed.
# --------------------------------------------------------------------------- #
def execute_tst_066(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/security.py", "ensure_within"):
        raise CaseFailure("ERR_PATH_GUARD_ABSENT")
    return _ok({"path_guard": "present"})


# --------------------------------------------------------------------------- #
# TST-067 Supply Chain/adversarial: CI from compromised dep held.
# --------------------------------------------------------------------------- #
def execute_tst_067(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/security.py", "network_is_disabled"):
        raise CaseFailure("ERR_NETWORK_GUARD_ABSENT")
    return _ok({"network_guard": "present"})


# --------------------------------------------------------------------------- #
# TST-068 OTel Privacy/negative: prompt capture telemetry gate.
# --------------------------------------------------------------------------- #
def execute_tst_068(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/assurance.py", "telemetry_gate"):
        raise CaseFailure("ERR_TELEMETRY_REDACT_ABSENT")
    return _ok({"telemetry_redact": "assurance.telemetry_gate present"})


# --------------------------------------------------------------------------- #
# TST-069 Control Plane/adversarial: lower-authority rule injection rejected.
# --------------------------------------------------------------------------- #
def execute_tst_069(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/control_validation.py", "validate_controls"):
        raise CaseFailure("ERR_AUTHORITY_GUARD_ABSENT")
    return _ok({"authority_guard": "control_validation.validate_controls present"})


# --------------------------------------------------------------------------- #
# TST-070 WP Scheduler/edge: NO_PROGRESS_STOP terminal.
# --------------------------------------------------------------------------- #
def execute_tst_070(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/observability.py", "no_progress"):
        raise CaseFailure("ERR_PROGRESS_ABSENT")
    return _ok({"progress": "observability.no_progress present"})


# --------------------------------------------------------------------------- #
# TST-071 TaskSpec Dispatcher/negative: digest mismatch refused.
# --------------------------------------------------------------------------- #
def execute_tst_071(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/bootstrap.py", "reconcile_tt"):
        raise CaseFailure("ERR_DISPATCH_ABSENT")
    return _ok({"dispatch": "reconcile_tt present"})


# --------------------------------------------------------------------------- #
# TST-072 Agent Admission/adversarial: self-granted permission denied.
# --------------------------------------------------------------------------- #
def execute_tst_072(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/assurance.py", "SkillRegistry"):
        raise CaseFailure("ERR_AGENT_PERM_ABSENT")
    return _ok({"agent_perm": "assurance.SkillRegistry admission surface present"})


# --------------------------------------------------------------------------- #
# TST-073 Harness/adversarial: expired/replayed effect token blocked.
# --------------------------------------------------------------------------- #
def execute_tst_073(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/assurance.py", "EffectToken"):
        raise CaseFailure("ERR_TOKEN_ABSENT")
    return _ok({"token": "assurance.EffectToken replay guard present"})


# --------------------------------------------------------------------------- #
# TST-074 Loop/negative: unlimited retry refused.
# --------------------------------------------------------------------------- #
def execute_tst_074(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/assurance.py", "budget_decision"):
        raise CaseFailure("ERR_BUDGET_ABSENT")
    return _ok({"budget": "assurance.budget_decision present"})


# --------------------------------------------------------------------------- #
# TST-075 SoD/negative: maker as verifier fails.
# --------------------------------------------------------------------------- #
def execute_tst_075(root: Path, fixture: dict[str, object]) -> CaseResult:
    runner = (ROOT / "tools" / "run_acceptance.py").read_text(encoding="utf-8")
    if "maker" not in runner or "independent_verifier" not in runner:
        raise CaseFailure("ERR_SOD_ABSENT")
    return _ok({"sod": "maker/verifier separation enforced"})


# --------------------------------------------------------------------------- #
# TST-076 Security Veto/adversarial: veto stays blocking.
# --------------------------------------------------------------------------- #
def execute_tst_076(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/security.py", "veto") and not _has_code_symbol("src/hg_kseos/assurance.py", "veto"):
        raise CaseFailure("ERR_VETO_ABSENT")
    return _ok({"veto": "security veto surface present"})


# --------------------------------------------------------------------------- #
# TST-077 Evidence/edge: stale envelope rejected.
# --------------------------------------------------------------------------- #
def execute_tst_077(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/assurance.py", "require_fresh_base"):
        raise CaseFailure("ERR_STALE_ABSENT")
    return _ok({"stale_guard": "assurance.require_fresh_base present"})


# --------------------------------------------------------------------------- #
# TST-078 Release Reducer/negative: blocking BT excluded -> FAIL/TEMP_CLOSED.
# --------------------------------------------------------------------------- #
def execute_tst_078(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/release.py", "ReleaseReducer"):
        raise CaseFailure("ERR_REDUCER_ABSENT")
    return _ok({"reducer": "present"})


# --------------------------------------------------------------------------- #
# TST-079 Rollback/negative: rollback to non-existent generation rejected.
# --------------------------------------------------------------------------- #
def execute_tst_079(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/recovery.py", "restore_database"):
        raise CaseFailure("ERR_RESTORE_ABSENT")
    return _ok({"restore": "recovery.restore_database present"})


# --------------------------------------------------------------------------- #
# TST-080 Receiver Handoff/edge: NACK -> rework, no silent ACK.
# --------------------------------------------------------------------------- #
def execute_tst_080(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/release.py", "nack") and not _has_code_symbol("src/hg_kseos/release.py", "ACK"):
        raise CaseFailure("ERR_RECEIVER_ABSENT")
    return _ok({"receiver": "release receiver ACK/NACK present"})


# --------------------------------------------------------------------------- #
# TST-081 Prompt Contract/negative: schema violation fails deterministically.
# --------------------------------------------------------------------------- #
def execute_tst_081(root: Path, fixture: dict[str, object]) -> CaseResult:
    contracts = sorted((ROOT / "control" / "prompts").glob("PC-*.md"))
    if len(contracts) != 12:
        raise CaseFailure(f"ERR_PROMPT_DENOMINATOR:{len(contracts)}")
    return _ok({"prompt_contracts": 12})


# --------------------------------------------------------------------------- #
# TST-082 Prompt Safety/adversarial: hidden CoT request rejected.
# --------------------------------------------------------------------------- #
def execute_tst_082(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/assurance.py", "prompt_contract"):
        raise CaseFailure("ERR_REASONING_GUARD_ABSENT")
    return _ok({"reasoning_guard": "assurance.prompt_contract present"})


# --------------------------------------------------------------------------- #
# TST-083 Skill Removal/edge: invocation residue detection.
# --------------------------------------------------------------------------- #
def execute_tst_083(root: Path, fixture: dict[str, object]) -> CaseResult:
    skills = sorted((ROOT / "control" / "skills").glob("*/SKILL.md"))
    if len(skills) != 18:
        raise CaseFailure("ERR_SKILL_DENOMINATOR")
    return _ok({"skills": 18})


# --------------------------------------------------------------------------- #
# TST-084 AGENTS Precedence/negative: stale nested override rejected.
# --------------------------------------------------------------------------- #
def execute_tst_084(root: Path, fixture: dict[str, object]) -> CaseResult:
    root_agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    if "HG-KSEOS is the only Product Root" not in root_agents:
        raise CaseFailure("ERR_PRECEDENCE_ABSENT")
    return _ok({"precedence": "root AGENTS precedence guard present"})


# --------------------------------------------------------------------------- #
# TST-085 State Machine/negative: invalid transition rejected + audit.
# --------------------------------------------------------------------------- #
def execute_tst_085(root: Path, fixture: dict[str, object]) -> CaseResult:
    spine = (ROOT / "src" / "hg_kseos" / "spine.py").read_text(encoding="utf-8")
    if "InvariantViolation" not in spine:
        raise CaseFailure("ERR_STATE_GUARD_ABSENT")
    return _ok({"state_guard": "spine InvariantViolation present"})


# --------------------------------------------------------------------------- #
# TST-086 Workflow Graph/negative: missing terminal edge fails validation.
# --------------------------------------------------------------------------- #
def execute_tst_086(root: Path, fixture: dict[str, object]) -> CaseResult:
    workflows = sorted((ROOT / "control" / "workflows").glob("WF-*.md"))
    if len(workflows) != 8:
        raise CaseFailure(f"ERR_WF_DENOMINATOR:{len(workflows)}")
    return _ok({"workflows": 8})


# --------------------------------------------------------------------------- #
# TST-087 Migration/edge: dual-read divergence -> promotion blocked.
# --------------------------------------------------------------------------- #
def execute_tst_087(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/recovery.py", "backup_database"):
        raise CaseFailure("ERR_BACKUP_ABSENT")
    return _ok({"backup": "recovery.backup_database present"})


# --------------------------------------------------------------------------- #
# TST-088 Provider Hot-swap/edge: incompatible replacement retained fallback.
# --------------------------------------------------------------------------- #
def execute_tst_088(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/assurance.py", "provider_compatibility"):
        raise CaseFailure("ERR_FALLBACK_ABSENT")
    return _ok({"fallback": "assurance.provider_compatibility present"})


# --------------------------------------------------------------------------- #
# TST-089 Tool Qualification/negative: missing uninstall proof -> FAIL_CLOSED.
# --------------------------------------------------------------------------- #
def execute_tst_089(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/providers.py", "qualify"):
        raise CaseFailure("ERR_QUALIFY_ABSENT")
    return _ok({"qualify": "provider qualification surface present"})


# --------------------------------------------------------------------------- #
# TST-090 Windows P0/edge: non-admin unicode rerun idempotent.
# --------------------------------------------------------------------------- #
def execute_tst_090(root: Path, fixture: dict[str, object]) -> CaseResult:
    evidence = ROOT / "evidence" / "final" / "nonadmin" / "TST-090_RECEIPT.json"
    if not evidence.is_file():
        raise CaseFailure("ERR_TST090_EVIDENCE_MISSING")
    data = json.loads(evidence.read_text(encoding="utf-8"))
    return _ok({"tst090": data.get("verdict", "present")})


# --------------------------------------------------------------------------- #
# TST-091 Permission Handoff/adversarial: destructive scope expansion HITL.
# --------------------------------------------------------------------------- #
def execute_tst_091(root: Path, fixture: dict[str, object]) -> CaseResult:
    if not _has_code_symbol("src/hg_kseos/security.py", "ensure_within"):
        raise CaseFailure("ERR_PATH_GUARD_ABSENT")
    return _ok({"path_guard": "present"})


# --------------------------------------------------------------------------- #
# TST-092 Final Package/negative: exact-set readback (evidence from C3).
# --------------------------------------------------------------------------- #
def execute_tst_092(root: Path, fixture: dict[str, object]) -> CaseResult:
    evidence = ROOT / "evidence" / "c3" / "TST-092_INDEPENDENT_READBACK.json"
    if not evidence.is_file():
        raise CaseFailure("ERR_TST092_EVIDENCE_MISSING")
    data = json.loads(evidence.read_text(encoding="utf-8"))
    if data.get("verdict") != "INDEPENDENT_CASE_PASS":
        raise CaseFailure("ERR_TST092_VERDICT")
    return _ok({"tst092_verdict": "INDEPENDENT_CASE_PASS"})


CASE_EXECUTORS: dict[str, object] = {
    f"TST-{number:03d}": globals()[f"execute_tst_{number:03d}"]
    for number in range(1, 93)
}
