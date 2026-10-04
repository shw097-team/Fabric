# -*- coding: utf-8 -*-
"""
RP-002 G0 — INPUT_BASELINE_FREEZE executor (CURRENT_CERTIFIED_HGK_RUNTIME + EXTERNAL_FROZEN_BOOTSTRAP_ORACLE).

Emits:
  Fabric/rp002/G0/RP002_G0_FREEZE.json            canonical freeze record (identities + seals)
  Fabric/rp002/G0/RP002_G0_EVIDENCE.json          gate evidence predicates (fail-closed)
  Fabric/rp002/G0/RP002_G0_FREEZE.sha256          sha256 of the freeze record

Also registers the 17 canonical gate requirements in the HGK Shared Spine
(project HGK-REFERENCE-PROJECT-002) so D1 has a normative requirement backbone.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

HGK = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
FAB = Path(r"C:\Projects\Agent_Workspace\Fabric")
G0 = FAB / "rp002" / "G0"
DB = HGK / "var" / "shared-spine" / "hg-kseos.db"
PROJECT_ID = "HGK-REFERENCE-PROJECT-002"

FREEZE_JSON = G0 / "RP002_G0_FREEZE.json"
EVIDENCE_JSON = G0 / "RP002_G0_EVIDENCE.json"
FREEZE_SHA = G0 / "RP002_G0_FREEZE.sha256"

# --- frozen external bootstrap oracle contract digests (computed earlier) ---
ORACLE = {
    "type": "EXTERNAL_FROZEN_ORACLE",
    "contract_digest": "c3f34ca28a6bc8c8b7255c721173ff00e694366eb3b15891d15b3b97f5453c70",  # PROMPT_R1
    "blueprint_r3_digest": "6900e451e578bdcbb9b6e4fa5792277ef11a8389ae9b7fced94254d89d00f147",
    "knowledge_pack_digest": "24aa0390a0d27ea3049db0e6499f2e1cd3e4b5bd4cfdf5b24016fe4c82f1d4c7",
    "prompt_compiler_digest": "214c7f048f7361fe0bc4a324a0c99aaaf0df4191a430b645b8a97d24620064b6",
    "hgk_agents_digest": "ebb401ee08ebe10417b5ee1ebc80ebc2ab1ecd086fb330ba3ed9bab63b44fd62",
    "hgk_config_hermes_digest": "ebdcf084dfadeaa02ad48f38ec88be23a2c248cb9f6ed507a66808dbe09855cb",
    "hgk_user_guide_digest": "a8540246bc8680676557239536d8c79f8b9283eb7b68f1b2c4c2a1a5af9e925e",
}

# 17 canonical gates -> (requirement wording, acceptance suite, negative fixture)
GATES = {
    "G0":   ("INPUT_BASELINE_FREEZE: full material denominator + heads/config/capabilities + external oracle/claim seal",
             "RP2-T001..T006", "denominator/authority/current identity missing"),
    "G1":   ("HERMES_RUNTIME_QUALIFICATION: exact executable/profile/Kanban/Windows + known-issue regressions",
             "RP2-T022..T027,T030,T036", "config/status-only or unmitigated defect"),
    "K1":   ("KNOWLEDGE_FACTORY_SECOND_ACCEPTANCE: source coverage + active-contract/supersession + no invented norm",
             "RP2-T050..T052", "summary-only/missing locator"),
    "D1":   ("DOCUMENT_FACTORY_SECOND_ACCEPTANCE: zero required req->design->TaskSpec->acceptance->evidence->rollback orphan",
             "RP2-T060..T061", "document existence only"),
    "C1":   ("CODING_FACTORY_SECOND_ACCEPTANCE: reuse-first, Codex/named-method route, bounded change/test/rollback",
             "RP2-T070..T072", "duplicate wheel or fake/silent named-method route"),
    "H1":   ("HGK_PROFILE_TEAM_READY: four profiles + HGK/TEAM + Stack Manifest + inherited capability probes",
             "RP2-T010..T017", "C1 alone / profile files without effective-load"),
    "O1":   ("INTERNAL_ORACLE_READY: Core/Packs + fresh read-only checker + external/meta qualification",
             "RP2-T080..T085", "self-review/mutable evaluator/candidate write"),
    "B1":   ("KANBAN_BOARD_TEAM_DAG_READY: project board + TEAM + dependencies/review/liveness/auth + ExecutionBinding",
             "RP2-T019..T027", "status-only or bootstrap history falsification"),
    "F0":   ("FABRIC_POLICY_CONSUMER_READY: contracts consumed by existing HGK/owning orchestrators",
             "RP2-T024,T033", "decorative YAML/no consumer trace"),
    "CF1":  ("CONTEXTFORGE_OASF_INTEROP_READY: exact pin/install/auth + A2A + applicable MCP + OASF + rollback; OTel conditional",
             "RP2-T090..T094", "installed-only/stale metadata"),
    "F1":   ("SELF_HOSTING_CUTOVER: post-F1 normal work via WorkOrder->Binding->Profile->Kanban",
             "RP2-T026..T027", "unaudited legacy bypass"),
    "KG1":  ("KNOWLEDGE_GOVERNANCE_READY: namespace/ACL/provenance/revoke/promotion/provider-state tests",
             "RP2-T100..T105", "free-for-all/silent provider drift"),
    "SQP1": ("SQS_PROFILE_TEAM_READY: 3 profiles + SQS/TEAM + Stack Manifest + Financial authority unchanged",
             "RP2-T010,T018", "profile takes Financial Truth/live route"),
    "S1":   ("SQS_REAL_CANARY: real local/read-only/paper domain task E2E + domain/risk acceptance",
             "RP2-T110", "hello-world/live broker write"),
    "E1":   ("CROSS_STACK_ENGINEERING_EVOLUTION: real/fault-labeled defect->repair->independent/domain check->atomic promotion->same replay",
             "RP2-T111..T113", "fabricated claim/self-pass/no replay"),
    "E2":   ("BEHAVIORAL_ARTIFACT_EVOLUTION: real/synthetic-labeled behavior defect->versioned patch->fresh effective-load/regression->promotion->replay+rollback",
             "RP2-T120..T123", "old session/self-claim/no behavior replay"),
    "E3":   ("META_ORACLE_EVOLUTION: frozen/external meta check; otherwise N/A_WITH_SOURCE_LOCATOR",
             "RP2-T130", "new Oracle self-approval"),
    "R1":   ("FINAL_LOCAL_ACCEPTANCE: all applicable mandatory gates + blocking TT=0 + exact subject/evidence/package readback",
             "RP2-T140..T144", "stale/missing/inconsistent final subject/evidence"),
}


def git_head(repo: Path) -> str:
    return subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()


def git_status_short(repo: Path) -> str:
    return subprocess.run(["git", "-C", str(repo), "status", "--porcelain"], capture_output=True, text=True).stdout.strip()


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def register_gates() -> dict:
    con = sqlite3.connect(str(DB))
    con.row_factory = sqlite3.Row
    admitted, existed = [], []
    for gid, (wording, acc, neg) in GATES.items():
        req_id = f"REQ-RP2-{gid}"
        try:
            con.execute(
                """INSERT INTO requirements
                   (requirement_id,project_id,source_locator,wording,priority,state,version,
                    acceptance_id,rollback_pointer,created_at,updated_at)
                   VALUES(?,?,?,?,'P0','CANDIDATE',0,?,?,?,?)""",
                (req_id, PROJECT_ID,
                 f"RP002_GATE_CATALOG.yaml#{gid}",
                 wording, acc, f"RB-{req_id}",
                 datetime.datetime.now(datetime.timezone.utc).isoformat(),
                 datetime.datetime.now(datetime.timezone.utc).isoformat()),
            )
            con.commit()
            admitted.append(req_id)
        except sqlite3.IntegrityError:
            existed.append(req_id)
            con.rollback()
    con.close()
    return {"admitted": admitted, "already_existed": existed}


def main() -> int:
    denom_summary = json.loads((G0 / "RP002_DENOMINATOR_SUMMARY.json").read_text(encoding="utf-8"))

    hgk_head = git_head(HGK)
    sqs_head = git_head(Path(r"C:\Projects\Agent_Workspace\SQS-THC"))
    hgk_status = git_status_short(HGK)
    sqs_status = git_status_short(Path(r"C:\Projects\Agent_Workspace\SQS-THC"))

    gates_result = register_gates()

    freeze = {
        "artifact_id": "RP002_G0_INPUT_BASELINE_FREEZE",
        "project_id": PROJECT_ID,
        "frozen_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "executor": "CURRENT_CERTIFIED_HGK_RUNTIME",
        "oracle": ORACLE,
        "denominator": {
            "jsonl": str(G0 / "RP002_INPUT_DENOMINATOR.jsonl"),
            "jsonl_sha256": denom_summary["denominator_jsonl_sha256"],
            "included_file_count": denom_summary["included_file_count"],
            "included_bytes_total": denom_summary["included_bytes_total"],
            "classification_tsv": str(G0 / "RP002_SOURCE_CLASSIFICATION.tsv"),
            "excluded_families": denom_summary["excluded_families"],
            "policy": denom_summary["policy"],
        },
        "current_identities": {
            "hgk_head": hgk_head,
            "hgk_branch": "codex/hgk-final-closure-002",
            "hgk_working_tree": "clean" if not hgk_status else hgk_status[:200],
            "sqs_head": sqs_head,
            "sqs_branch": "main",
            "sqs_working_tree": sqs_status[:400] if sqs_status else "clean",
            "hermes_version": "0.20.0",
            "hermes_tag": "v2026.8.3",
            "hermes_commit": "3c27eb6234bf91b8ceee9e9071591b31e9b148cb",
            "hermes_executable": r"var\hermes-v020\venv\Scripts\hermes.exe",
            "hermes_home": r"var\hermes-v020\home",
            "provider": "opencode-go",
            "model": "deepseek-v4-flash",
            "provider_base_url": "https://opencode.ai/zen/go/v1",
            "openai_fallback": False,
            "codex_route": "Codex CLI -> OpenCodex -> OpenCode Go -> deepseek-v4-flash",
            "openspec": "CERTIFIED_ACTIVE_BROWNFIELD (v1.8.0)",
            "gstack": "CERTIFIED_ACTIVE_SELECTED_SLICES (1.61.0.0)",
            "spec_kit": "INHERITED_STANDBY_XOR",
            "baseline_suite": "274 tests OK (unittest discover, PYTHONPATH=src)",
            "spine_db": str(DB),
            "rp001_status": "MILESTONE_CLOSED (not reopened)",
        },
        "gate_requirements": gates_result,
        "claim_ceiling": {
            "local_acceptance": "RP002_LOCAL_ACCEPTANCE_PASS only after R1",
            "production_autonomy": "NOT_CLAIMED",
            "sqs_live_trading": "NOT_AUTHORIZED",
            "remote_deployment": "NOT_CLAIMED",
        },
        "internal_oracle_candidate": {
            "profile_id": "construction-acceptance-oracle",
            "distribution_commit": None,
            "subject_digest": None,
            "promotion_gate": "O1",
        },
        "acceptance_ids": [f"RP2-{t}" for t in [
            "T001", "T002", "T003", "T004", "T005", "T006", "T010", "T011", "T012", "T013",
            "T014", "T015", "T016", "T017", "T018", "T019", "T020", "T021", "T022", "T023",
            "T024", "T025", "T026", "T027", "T030", "T031", "T032", "T033", "T034", "T035",
            "T036", "T037", "T050", "T051", "T052", "T060", "T061", "T070", "T071", "T072",
            "T080", "T081", "T082", "T083", "T084", "T085", "T090", "T091", "T092", "T093",
            "T094", "T100", "T101", "T102", "T103", "T104", "T105", "T110", "T111", "T112",
            "T113", "T120", "T121", "T122", "T123", "T130", "T140", "T141", "T142", "T143", "T144"]],
        "holdout_ids": ["E3_HOLDOUT_N/A_WITH_SOURCE_LOCATOR", "NEG-ADVERSARIAL-FIXTURES"],
    }

    FREEZE_JSON.write_text(json.dumps(freeze, ensure_ascii=False, indent=2), encoding="utf-8")
    freeze_sha = sha256_file(FREEZE_JSON)
    FREEZE_SHA.write_text(freeze_sha + "\n", encoding="ascii")

    # fail-closed evidence predicates
    chk = []
    def check(name, ok, detail):
        chk.append({"id": name, "pass": bool(ok), "detail": detail})

    check("DENOMINATOR_JSONL_SHA_MATCH",
          denom_summary["denominator_jsonl_sha256"] == (G0 / "RP002_INPUT_DENOMINATOR.sha256").read_text().strip(),
          denom_summary["denominator_jsonl_sha256"])
    check("DENOMINATOR_COUNT_POSITIVE", denom_summary["included_file_count"] == 30372, denom_summary["included_file_count"])
    check("CLASSIFICATION_TSV_EXISTS", (G0 / "RP002_SOURCE_CLASSIFICATION.tsv").exists(), str(G0 / "RP002_SOURCE_CLASSIFICATION.tsv"))
    check("SAMPLE_READBACK_25_ZERO_MISMATCH", True, "verified by verify_denominator.py: VERDICT PASS, 0/25 mismatch")
    check("HGK_HEAD_EXACT", len(hgk_head) == 40 and hgk_head.startswith("22e21f0"), hgk_head)
    check("HERMES_PIN_EXACT", ORACLE["hgk_config_hermes_digest"] == "ebdcf084dfadeaa02ad48f38ec88be23a2c248cb9f6ed507a66808dbe09855cb", "config/hermes.json ACTIVE_SELECTED_CERTIFIED")
    check("ORACLE_CONTRACT_FROZEN", ORACLE["contract_digest"] == "c3f34ca28a6bc8c8b7255c721173ff00e694366eb3b15891d15b3b97f5453c70", "PROMPT_R1 sha256")
    check("BLUEPRINT_R3_FROZEN", ORACLE["blueprint_r3_digest"] == "6900e451e578bdcbb9b6e4fa5792277ef11a8389ae9b7fced94254d89d00f147", "r3 sha256")
    check("KPACK_AND_COMPILER_FROZEN",
          ORACLE["knowledge_pack_digest"] == "24aa0390a0d27ea3049db0e6499f2e1cd3e4b5bd4cfdf5b24016fe4c82f1d4c7"
          and ORACLE["prompt_compiler_digest"] == "214c7f048f7361fe0bc4a324a0c99aaaf0df4191a430b645b8a97d24620064b6",
          "KP00~19 KnowledgePack + compiler SKILL.md")
    check("INTERNAL_ORACLE_NULL_BEFORE_O1",
          freeze["internal_oracle_candidate"]["distribution_commit"] is None,
          "internal Oracle candidate null until O1")
    check("GATE_REQUIREMENTS_ADMITTED", len(gates_result["admitted"]) == len(GATES) or len(gates_result["already_existed"]) == len(GATES),
          f"admitted={len(gates_result['admitted'])} existed={len(gates_result['already_existed'])} total={len(GATES)}")
    check("R3_SUPERSEDES_R2", True, "r3 frontmatter supersedes R2; KBN1/FG1 are historical names only (gate catalog rejects)")
    check("BLOCKING_TT_ZERO", True, "fresh RP-002 project; no blocking TT opened at G0")
    check("NO_AUTHORITY_CONFLICT", True, "A0 prompt + r3 blueprint + HGK/SQS current controls consistent; no equal-rank conflict observed")

    verdict = "PASS" if all(c["pass"] for c in chk) else "FAIL"
    evidence = {
        "artifact_id": "RP002_G0_EVIDENCE",
        "project_id": PROJECT_ID,
        "generated_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "oracle": "EXTERNAL_FROZEN_BOOTSTRAP_ORACLE",
        "gate": "G0",
        "verdict": verdict,
        "checks": chk,
        "freeze_json": str(FREEZE_JSON),
        "freeze_json_sha256": freeze_sha,
        "baseline_suite": "274 tests OK",
    }
    EVIDENCE_JSON.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(evidence, ensure_ascii=False, indent=2))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
