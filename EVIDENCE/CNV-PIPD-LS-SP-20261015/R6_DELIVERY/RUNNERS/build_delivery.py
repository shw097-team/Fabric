#!/usr/bin/env python3
"""R6 bounded-writer delivery builder.

Reads only admitted sources already on disk, plus the RAW/ captures produced by
the executed probes, and materializes the R6_DELIVERY candidate artifact set.
Every artifact carries producer / produced_utc / source_hashes_used /
raw_evidence_refs / verdict=PENDING_CHECKER / claim_level=LOCAL.

This script performs no network egress and writes only under R6_DELIVERY/.
"""
import hashlib
import json
import os
import shutil
from datetime import datetime, timezone

ROOT = r"C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015"
DEL = os.path.join(ROOT, "R6_DELIVERY")
RAW = os.path.join(DEL, "RAW")
RUNNERS = os.path.join(DEL, "RUNNERS")

PRODUCER = "Codex CLI bounded writer EXECUTE lane (opencode-go/deepseek-v4.1-flash)"
CHECKER = "opencode-go/glm-5.3-flash (independent; not this writer)"
ROUND = "CNV-PIPD-LS-SP-20261015-R6"
MISSION = "CNV-PIPD-LS-SP-20261015"

PKG = (r"C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0"
       r"\LocalCache\Local\hermes\attachments\Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md")
COMMANDER = (r"C:\Projects\Agent_Workspace\知識庫\實作相關DOC\HG-KSEOS"
             r"\Fabric_HG-KSEOS_Convergence\PROMPT\Fabric_HG-KSEOS_Convergence_指揮薄PROMPT.md")

SOURCE_HASHES = {
    "OWNER_TRUST_LOCK.json": "8b78edebd79c8149a2b74e2a7f873e3116f772c881a501bd4600ea0e7a891f6b",
    "HG-KSEOS/AGENTS.md": "7f7246d34be112bb465b48dadaef6163e466e16e5e705fc58acee04b3809a613",
    "Fabric/AGENTS.md": "115912cdccbf5b3788fe1d6e1c8c10fe575252d72accf31cb6f1955dd8750974",
    "Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md": "96d9d564286743e17550ccef15b9952347901eb77168f930376938893cff9c3f",
    "Fabric_HG-KSEOS_Convergence_指揮薄PROMPT.md": "6894a6ba08781f2ed5758af132f758c14c1a9e9b69d42056837f5ce45bba6c64",
    "C0_C9_CONTRACT_R5.json": "6629af1d4cf09ec11b99e79488ea515692ebd9c802fef6353b1ac3ed31b7bd6e",
    "compiler_native_output_R5/thin-prompt.md": "2f246796c3b927170a90ed7dd3f4307e913579db2efb56b307cbc2377a1cb77f",
}
SOURCE_HASHES_LIST = [SOURCE_HASHES[k] for k in sorted(SOURCE_HASHES)]


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def read(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def write_json(name, obj):
    path = os.path.join(DEL, name)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return path


def write_text(name, text):
    path = os.path.join(DEL, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


def base(extra_refs=None, produced=None):
    d = {
        "producer": PRODUCER,
        "produced_utc": produced or utc_now(),
        "source_hashes_used": SOURCE_HASHES_LIST,
        "raw_evidence_refs": extra_refs or [],
        "verdict": "PENDING_CHECKER",
        "claim_level": "LOCAL",
    }
    return d


# ---------------------------------------------------------------- load inputs
contract = load(os.path.join(ROOT, "C0_C9_CONTRACT_R5.json"))
acc_rows = contract["acceptance"]
gate_rows = contract["evidence"]
audit = load(os.path.join(ROOT, "AUDIT_24_CLOSURE_PREFLIGHT.json"))
mutations = load(os.path.join(ROOT, "MUTATIONS_18_PREFLIGHT.json"))
kledger = load(os.path.join(ROOT, "K_LEDGER_CROSSWALK_PREFLIGHT.json"))
matrix = load(os.path.join(ROOT, "RUNNER_AND_TEST_MATRIX_PREFLIGHT.json"))
caps = load(os.path.join(DEL, "RUNNERS", "capability_probes.json"))
supp = load(os.path.join(DEL, "RUNNERS", "supplement_probes.json"))
muts = load(os.path.join(DEL, "RUNNERS", "mutation_records.json"))
spine = load(os.path.join(DEL, "RUNNERS", "cap03_records.json"))

all_probes = {p["probe_id"]: p for p in (caps + supp + spine)}


def probe_ref(pid):
    p = all_probes.get(pid)
    if not p:
        return None
    return {
        "probe_id": pid,
        "command": p["command"],
        "cwd": p["cwd"],
        "started_utc": p["started_utc"],
        "exit_code": p["exit_code"],
        "stdout_file": p["stdout_file"],
        "stderr_file": p["stderr_file"],
        "stdout_sha256": p["stdout_sha256"],
        "stderr_sha256": p["stderr_sha256"],
    }


# capability -> probe ids (positive / negative)
CAP_PROBES = {
    "native-prompt-compiler": {"pos": ["cap01_compiler_lint", "cap01_compiler_activation",
                                       "cap01_compiler_acceptance", "cap01_compiler_hash",
                                       "cap01_compiler_duplication"]},
    "approved-document-verifier": {"pos": ["cap02_pkg_check_help"],
                                   "blocked": ["cap02_pkg_check_run", "cap02_pkg_check_selftest_corrected"]},
    "HGK-typed-spine-and-lifecycle": {"pos": ["cap03_spine_positive", "cap03_spine_acceptance"],
                                      "neg": ["cap03_spine_negative", "cap03_spine_fk_negative"]},
    "Hermes-canonical-runtime": {"pos": ["cap04_hermes_version"]},
    "Codex-EXECUTE-DeepSeek": {"pos": ["cap05_codex_version"], "neg": ["cap05_lane_toolchain_resolve"],
                               "other": ["cap05_role_binding_assert"]},
    "Codex-VERIFY-GLM": {"other": ["checker_independent_run"]},
    "Hermes-Kanban": {"pos": ["cap07_kanban_boards"]},
    "Hermes-Swarm": {"pos": ["cap08_swarm_help"]},
    "gstack-advisory": {"pos": ["cap11_gstack_positive"], "neg": ["cap11_gstack_negative"]},
    "OpenSpec-brownfield": {"pos": ["cap12_openspec_version"]},
    "AVR-HGK-Skill-loader": {"pos": ["cap_avr_skill_pack"]},
    "FAR-SQLite-FTS5": {"pos": ["cap13_fts5_positive"], "neg": ["cap13_fts5_negative"]},
    "bounded-FS-API-Desktop": {"pos": ["cap_pipd_project_unsafe"]},
    "approval-gated-GitHub": {"blocked": ["cap15_github_publish"]},
    "pipd-route-intake": {"pos": ["cap_pipd_intake"], "neg": ["cap_pipd_intake_missing", "cap_pipd_intake_ambiguous"]},
    "pipd-authority-source": {"pos": ["cap_pipd_intake_pkg"]},
    "pipd-profile-tailor": {"pos": ["cap_pipd_profile_ok"], "neg": ["cap_pipd_profile"]},
    "pipd-pi-compile": {"pos": ["cap_pipd_compile_pi"], "neg": ["cap_pipd_compile_pi_tamper"]},
    "pipd-pd-bind": {"pos": ["cap_pipd_bind_pd"], "neg": ["cap_pipd_bind_pd_nocxt"]},
    "pipd-execution-contract": {"pos": ["cap_pipd_ecp"]},
    "pipd-assurance-tqaep": {"pos": ["cap_pipd_tqaep"], "neg": ["cap_pipd_tqaep_self", "cap_pipd_tqaep_noreceipt"]},
    "pipd-package-project": {"pos": ["cap_pipd_project_unsafe", "cap_pipd_claim_ladder_ok"],
                             "neg": ["cap_pipd_claim_ceiling"]},
}

# Disposition per capability (from executed evidence).
CAP_DISPOSITION = {
    "native-prompt-compiler": ("QUALIFIED_LOCAL", "Entrypoint scripts/prompt_contract_compiler.py; lint/activation/acceptance/hash/duplication exit 0"),
    "approved-document-verifier": ("BLOCKED_EXTERNAL", "pipd_pkg_v2_check.py --check / --materialize exit 30 FAIL_CLOSED MISSING_EXTERNAL_OWNER_APPROVED_LOCK; --check locked exit 30 SOURCE_PHYSICAL_MISSING"),
    "HGK-typed-spine-and-lifecycle": ("QUALIFIED_LOCAL", "Positive/negative/acceptance probes exit 0; illegal transition refused; FK refused"),
    "Hermes-canonical-runtime": ("BLOCKED_HITL", "hermes --version exit 0 but reports v0.21.5 (2026.9.24) while config declares 0.20.0/v2026.8.3; runtime binding mismatch requires Owner certification (K-06)"),
    "Codex-EXECUTE-DeepSeek": ("BLOCKED_EXTERNAL", "codex.exe present reports 0.162.0-alpha.17.2, but declared lane binary .../Codex/bin/2e5e00daee91c61d/codex.exe is absent; lane toolchain resolve exit 3 ERR_LANE_TOOLCHAIN_BINARY_MISSING"),
    "Codex-VERIFY-GLM": ("BLOCKED_EXTERNAL", "Independent checker ran (exit 1, verdict FAIL, denominator 92) but produced 2 FAILs; mandated checker arm availability is an Owner/external condition (K-10)"),
    "Hermes-Kanban": ("QUALIFIED_LOCAL", "hermes kanban boards list exit 0 with real board output"),
    "Hermes-Swarm": ("QUALIFIED_LOCAL", "hermes kanban swarm --help exit 0"),
    "gstack-advisory": ("QUALIFIED_LOCAL", "positive + negative exit 0; ADOPT_FULL_ROLE_ARCHITECTURE true, 4 hard-deny, 0 breaches"),
    "OpenSpec-brownfield": ("QUALIFIED_LOCAL", "openspec --version exit 0 = 1.8.0"),
    "AVR-HGK-Skill-loader": ("QUALIFIED_LOCAL", "skill pack self-run exit 0 PASS 8/8 skills, 56/56 cases"),
    "FAR-SQLite-FTS5": ("QUALIFIED_LOCAL", "FTS5 positive/negative/teardown exit 0; MATCH hit, malformed MATCH refused"),
    "bounded-FS-API-Desktop": ("QUALIFIED_LOCAL", "unsafe destination refused exit 2; bounded write path enforced"),
    "approval-gated-GitHub": ("BLOCKED_EXTERNAL", "github_publish.py exit 2 {\"PAT_PRESENT\": false, \"verdict\": \"GITHUB_AUTH_BLOCKED\"}"),
    "pipd-route-intake": ("QUALIFIED_LOCAL", "intake exit 0; missing/ambiguous refused (AuthorityUnknown / IntakeInvalid)"),
    "pipd-authority-source": ("QUALIFIED_LOCAL", "intake-pkg exit 0 over real PKG.md; compound ambiguity refused"),
    "pipd-profile-tailor": ("QUALIFIED_LOCAL", "profile-ok exit 0 LITE/deterministic_validator; unknown axis refused"),
    "pipd-pi-compile": ("QUALIFIED_LOCAL", "compile-pi exit 0; tamper refused PiSemanticFail"),
    "pipd-pd-bind": ("QUALIFIED_LOCAL", "bind-pd exit 0; no-RepoContext refused"),
    "pipd-execution-contract": ("QUALIFIED_LOCAL", "ecp exit 0"),
    "pipd-assurance-tqaep": ("QUALIFIED_LOCAL", "tqaep exit 0 independent_acceptance=NOT_GRANTED; self/noreceipt refused"),
    "pipd-package-project": ("QUALIFIED_LOCAL", "project-unsafe exit 2 refused; claim ladder LOCAL_QUALIFIED with forbidden upper claims"),
}


def cap_acc_id(name):
    for r in acc_rows:
        if r["subject_type"] == "CAPABILITY" and r["subject_id"] == name:
            return r["acceptance_id"]
    return None


# --------------------------------------------------------------- 1 SUBJECT
def build_subject_and_source():
    d = base(produced=None)
    d.update({
        "artifact": "SUBJECT_AND_SOURCE.json",
        "round": ROUND,
        "mission_id": MISSION,
        "lane": "EXECUTE (bounded writer)",
        "subject": {
            "task_id": contract["task_id"],
            "changeset": contract["changeset"]["class"],
            "compiled_prompt": "compiler_native_output_R5/thin-prompt.md",
            "compiler_state": "PROMPT_COMPILE_PASS",
            "compiler_sha256": SOURCE_HASHES["compiler_native_output_R5/thin-prompt.md"],
            "candidate_subject_sha": None,
            "candidate_head": "NOT_CREATED",
        },
        "authority_anchor": {
            "path": PKG,
            "sha256": SOURCE_HASHES["Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md"],
            "bytes": 2689181,
            "role": "sole authority anchor per Owner decision 2026-10-15",
        },
        "sources": [
            {"path": os.path.join(ROOT, "OWNER_TRUST_LOCK.json"), "role": "A0 NORMATIVE",
             "sha256": SOURCE_HASHES["OWNER_TRUST_LOCK.json"]},
            {"path": os.path.join(ROOT, "C0_C9_CONTRACT_R5.json"), "role": "compiled contract",
             "sha256": SOURCE_HASHES["C0_C9_CONTRACT_R5.json"]},
            {"path": os.path.join(ROOT, "compiler_native_output_R5", "thin-prompt.md"),
             "role": "compiled thin prompt (authoritative job order)",
             "sha256": SOURCE_HASHES["compiler_native_output_R5/thin-prompt.md"]},
            {"path": COMMANDER, "role": "A4 NORMATIVE",
             "sha256": SOURCE_HASHES["Fabric_HG-KSEOS_Convergence_指揮薄PROMPT.md"]},
            {"path": PKG, "role": "A3 NORMATIVE",
             "sha256": SOURCE_HASHES["Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md"]},
            {"path": r"C:\Projects\Agent_Workspace\HG-KSEOS\AGENTS.md", "role": "A1 NORMATIVE",
             "sha256": SOURCE_HASHES["HG-KSEOS/AGENTS.md"]},
            {"path": r"C:\Projects\Agent_Workspace\Fabric\AGENTS.md", "role": "A6 SUPPORT",
             "sha256": SOURCE_HASHES["Fabric/AGENTS.md"]},
        ],
        "notes": [
            "All seven authority files were read and hashed before use.",
            "No source corpus file was modified; all writes are confined to R6_DELIVERY/.",
        ],
    })
    return d


# ---------------------------------------------------------- 2 AUTHORITY LOCK
def build_authority_lock():
    lock = load(os.path.join(ROOT, "OWNER_TRUST_LOCK.json"))
    d = base([{"source": os.path.join(ROOT, "OWNER_TRUST_LOCK.json"),
               "sha256": SOURCE_HASHES["OWNER_TRUST_LOCK.json"]}])
    d.update({
        "artifact": "AUTHORITY_LOCK_STATUS.json",
        "owner_trust_lock": {
            "path": os.path.join(ROOT, "OWNER_TRUST_LOCK.json"),
            "sha256": SOURCE_HASHES["OWNER_TRUST_LOCK.json"],
            "record_type": lock["record_type"],
            "observed_at": lock["observed_at"],
            "authority": lock["authority"],
            "signature_type": lock["signature_type"],
            "canonical_mutation": lock["canonical_mutation"],
        },
        "package_pin": lock["package"],
        "verifier_pin": lock["verifier"],
        "authorized_scope": lock["authorized_scope"],
        "not_granted_by_this_record": lock["not_granted_by_this_record"],
        "status": "OWNER_PINS_VERIFIED_OTHER_AUTHORITY_GATES_OPEN",
        "open_authority_conditions": [
            "canonical admission (C0-C9 typed admission) not performed",
            "world effects not authorized",
            "publication gate not passed",
            "independent acceptance not granted",
        ],
        "notes": [
            "This lock is a noncanonical interactive user attestation, not a cryptographic signature.",
            "No canonical Shared Spine mutation was performed by this lane.",
        ],
    })
    return d


# --------------------------------------------------------- 3 COMPILER RECEIPTS
R5_RECEIPTS = [
    "COMPILER_R5_lint.receipt.json",
    "COMPILER_R5_lint.stdout.txt",
    "COMPILER_R5_lint.stderr.txt",
    "COMPILER_R5_activation.receipt.json",
    "COMPILER_R5_activation.stdout.txt",
    "COMPILER_R5_activation.stderr.txt",
    "COMPILER_R5_acceptance.receipt.json",
    "COMPILER_R5_acceptance.stdout.txt",
    "COMPILER_R5_acceptance.stderr.txt",
    "COMPILER_R5_compile.receipt.json",
    "COMPILER_R5_compile.stdout.txt",
    "COMPILER_R5_compile.stderr.txt",
]
NATIVE_RECEIPTS = [
    "compiler_native_output_R5/compiler-receipt.json",
    "compiler_native_output_R5/compiler-report.json",
    "compiler_native_output_R5/thin-prompt.md",
]


def copy_receipts():
    dest_dir = os.path.join(DEL, "COMPILER_RECEIPTS")
    os.makedirs(dest_dir, exist_ok=True)
    index = []
    for name in R5_RECEIPTS:
        src = os.path.join(ROOT, name)
        if not os.path.exists(src):
            continue
        dest = os.path.join(dest_dir, "R5_" + name)
        shutil.copy2(src, dest)
        index.append({"copied_name": "R5_" + name, "source_path": src,
                      "bytes": os.path.getsize(dest), "sha256": sha256_file(dest)})
    for rel in NATIVE_RECEIPTS:
        src = os.path.join(ROOT, rel.replace("/", os.sep))
        if not os.path.exists(src):
            continue
        flat = "R5_native_" + os.path.basename(rel)
        dest = os.path.join(dest_dir, flat)
        shutil.copy2(src, dest)
        index.append({"copied_name": flat, "source_path": src,
                      "bytes": os.path.getsize(dest), "sha256": sha256_file(dest)})
    return index


def build_compiler_index(index_rows):
    d = base([{"raw": r["copied_name"], "sha256": r["sha256"]} for r in index_rows])
    d.update({
        "artifact": "COMPILER_RECEIPTS/index.json",
        "compiler_state": "PROMPT_COMPILE_PASS",
        "compiled_prompt_sha256": SOURCE_HASHES["compiler_native_output_R5/thin-prompt.md"],
        "compiled_prompt_sha256_prefix_declared": "2f247960d5f1",
        "compiled_prompt_sha256_prefix_observed": SOURCE_HASHES["compiler_native_output_R5/thin-prompt.md"][:12],
        "receipts": index_rows,
        "note": ("index.json lists copies of the R5 compiler receipts actually read; "
                 "copies live beside this index under COMPILER_RECEIPTS/."),
    })
    return d


# ------------------------------------------------------------- 4 REQ_TRACE_221
def build_req_trace():
    executed = {
        "ACC-001": {"real_runner": "prompt_contract_compiler.py", "outcome": "LOCAL_CASE_PASS",
                    "probes": ["cap01_compiler_lint", "cap01_compiler_activation",
                               "cap01_compiler_acceptance", "cap01_compiler_hash",
                               "cap01_compiler_duplication"]},
        "ACC-002": {"real_runner": "pipd_pkg_v2_check.py", "outcome": "BLOCKED_EXTERNAL",
                    "missing": "MISSING_EXTERNAL_OWNER_APPROVED_LOCK / SOURCE_PHYSICAL_MISSING",
                    "probes": ["cap02_pkg_check_run", "cap02_pkg_check_selftest_corrected"]},
        "ACC-003": {"real_runner": "hg_kseos typed spine", "outcome": "LOCAL_CASE_PASS",
                    "probes": ["cap03_spine_positive", "cap03_spine_negative", "cap03_spine_acceptance"]},
        "ACC-004": {"real_runner": "hermes --version", "outcome": "BLOCKED_HITL",
                    "missing": "declared runtime binding 0.20.0 vs served 0.21.5 certification",
                    "probes": ["cap04_hermes_version"]},
        "ACC-005": {"real_runner": "codex lane resolve + role binding", "outcome": "BLOCKED_EXTERNAL",
                    "missing": "declared lane binary .../bin/2e5e00daee91c61d/codex.exe absent",
                    "probes": ["cap05_codex_version", "cap05_lane_toolchain_resolve", "cap05_role_binding_assert"]},
        "ACC-006": {"real_runner": "check_acceptance_independent.py", "outcome": "BLOCKED_EXTERNAL",
                    "missing": "checker arm availability / 2 residual FAILs (TST-025, TST-048)",
                    "probes": ["checker_independent_run"]},
        "ACC-007": {"real_runner": "hermes kanban boards list", "outcome": "LOCAL_CASE_PASS",
                    "probes": ["cap07_kanban_boards"]},
        "ACC-008": {"real_runner": "hermes kanban swarm", "outcome": "LOCAL_CASE_PASS",
                    "probes": ["cap08_swarm_help"]},
        "ACC-009": {"real_runner": "probe_gstack_rolemap.py", "outcome": "LOCAL_CASE_PASS",
                    "probes": ["cap11_gstack_positive", "cap11_gstack_negative"]},
        "ACC-010": {"real_runner": "openspec --version", "outcome": "LOCAL_CASE_PASS",
                    "probes": ["cap12_openspec_version"]},
        "ACC-011": {"real_runner": "AVR skill pack self-run", "outcome": "LOCAL_CASE_PASS",
                    "probes": ["cap_avr_skill_pack"]},
        "ACC-012": {"real_runner": "probe_fts5.py", "outcome": "LOCAL_CASE_PASS",
                    "probes": ["cap13_fts5_positive", "cap13_fts5_negative"]},
        "ACC-013": {"real_runner": "PIPD bounded-FS destination guard", "outcome": "LOCAL_CASE_PASS",
                    "probes": ["cap_pipd_project_unsafe"]},
        "ACC-014": {"real_runner": "github_publish.py", "outcome": "BLOCKED_EXTERNAL",
                    "missing": "no GitHub PAT (PAT_PRESENT=false)",
                    "probes": ["cap15_github_publish"]},
        "ACC-015": {"real_runner": "PIPD intake", "outcome": "LOCAL_CASE_PASS",
                    "probes": ["cap_pipd_intake", "cap_pipd_intake_missing", "cap_pipd_intake_ambiguous"]},
        "ACC-016": {"real_runner": "PIPD authority source", "outcome": "LOCAL_CASE_PASS",
                    "probes": ["cap_pipd_intake_pkg"]},
        "ACC-017": {"real_runner": "PIPD profile", "outcome": "LOCAL_CASE_PASS",
                    "probes": ["cap_pipd_profile_ok", "cap_pipd_profile"]},
        "ACC-018": {"real_runner": "PIPD compile PI", "outcome": "LOCAL_CASE_PASS",
                    "probes": ["cap_pipd_compile_pi", "cap_pipd_compile_pi_tamper"]},
        "ACC-019": {"real_runner": "PIPD bind PD", "outcome": "LOCAL_CASE_PASS",
                    "probes": ["cap_pipd_bind_pd", "cap_pipd_bind_pd_nocxt"]},
        "ACC-020": {"real_runner": "PIPD ECP", "outcome": "LOCAL_CASE_PASS",
                    "probes": ["cap_pipd_ecp"]},
        "ACC-021": {"real_runner": "PIPD TQAEP", "outcome": "LOCAL_CASE_PASS",
                    "probes": ["cap_pipd_tqaep", "cap_pipd_tqaep_self", "cap_pipd_tqaep_noreceipt"]},
        "ACC-022": {"real_runner": "PIPD package project", "outcome": "LOCAL_CASE_PASS",
                    "probes": ["cap_pipd_project_unsafe", "cap_pipd_claim_ladder_ok", "cap_pipd_claim_ceiling"]},
    }
    deliverable_runner = {
        "SUBJECT_AND_SOURCE.json": "SUBJECT_AND_SOURCE.json",
        "AUTHORITY_LOCK_STATUS.json": "AUTHORITY_LOCK_STATUS.json",
        "COMPILER_RECEIPTS/": "COMPILER_RECEIPTS/index.json",
        "REQ_TRACE_221.json": "REQ_TRACE_221.json",
        "AUDIT_24_CLOSURE.json": "AUDIT_24_CLOSURE.json",
        "K_LEDGER_CROSSWALK.json": "K_LEDGER_CROSSWALK.json",
        "RUNNER_AND_TEST_MATRIX.json": "RUNNER_AND_TEST_MATRIX.json",
        "MUTATIONS_18.json": "MUTATIONS_18.json",
        "EFFECTS_5.json": "EFFECTS_5.json",
        "GATES_A_TO_H.json": "GATES_A_TO_H.json",
        "MAKER_CHECKER_SEPARATION.json": "MAKER_CHECKER_SEPARATION.json",
        "TT_CR_REGISTER.json": "TT_CR_REGISTER.json",
        "CHECKPOINT_AND_ROLLBACK.json": "CHECKPOINT_AND_ROLLBACK.json",
        "PUBLICATION_RECEIPT.json": "PUBLICATION_RECEIPT.json",
        "EXTERNAL_ACCEPTANCE_HANDOFF.md": "EXTERNAL_ACCEPTANCE_HANDOFF.md",
        "NON_CLAIMS.md": "NON_CLAIMS.md",
    }
    rows = []
    for r in acc_rows:
        aid = r["acceptance_id"]
        st = r["subject_type"]
        loc = (r.get("source_locators") or [None])[0]
        row = {
            "subject_id": aid,
            "acc_id": aid,
            "subject_name": r["subject_id"],
            "subject_type": st,
            "source_locator": loc,
            "required_depth": r.get("required_depth"),
            "real_runner": "REAL_RUNNER_NOT_BOUND",
            "runner_reason": None,
            "outcome": None,
            "raw_evidence_refs": [],
        }
        if st == "CAPABILITY" and aid in executed:
            e = executed[aid]
            row["real_runner"] = e["real_runner"]
            row["outcome"] = e["outcome"]
            row["raw_evidence_refs"] = ["RAW/%s.%s.txt" % (p, "stdout") for p in e["probes"]]
            if e.get("missing"):
                row["runner_reason"] = e["missing"]
        elif st == "DELIVERABLE":
            row["real_runner"] = deliverable_runner.get(r["subject_id"], "DELIVERY_ARTIFACT")
            row["outcome"] = "CANDIDATE_PRODUCED"
            row["raw_evidence_refs"] = ["R6_DELIVERY/" + r["subject_id"]]
        elif st == "JOURNEY":
            row["real_runner"] = "REAL_RUNNER_NOT_BOUND"
            row["runner_reason"] = "END_TO_END_JOURNEY_NOT_RUN; depends on all capability and requirement gates"
            row["outcome"] = "NOT_RUN"
        else:
            row["runner_reason"] = "SOURCE_PHYSICAL_MISSING / PROMPT_COMPILE_BLOCKED / EXECUTION_ADMISSION_NOT_RUN"
            row["outcome"] = "BLOCKED_NOT_RUN"
        rows.append(row)

    planning = [x for x in rows if x["subject_type"] == "REQUIREMENT"
                and not x["subject_name"].startswith("CNV-")]
    cnv_rows = [x for x in rows if x["subject_type"] == "REQUIREMENT"
                and x["subject_name"].startswith("CNV-")]
    d = base()
    d.update({
        "artifact": "REQ_TRACE_221.json",
        "denominator": 221,
        "denominator_breakdown": {"rq_parents": 64, "children": 129, "legacy_t": 28},
        "planning_rows": planning,
        "cnv_delivery_requirement_rows": cnv_rows,
        "capability_rows": [x for x in rows if x["subject_type"] == "CAPABILITY"],
        "deliverable_rows": [x for x in rows if x["subject_type"] == "DELIVERABLE"],
        "journey_rows": [x for x in rows if x["subject_type"] == "JOURNEY"],
        "rows": rows,
        "executed_summary": {
            "planning_cases_executed": 0,
            "planning_cases_planned": 221,
            "capabilities_executed": 22,
            "capabilities_locally_passed": sum(1 for x in rows if x["outcome"] == "LOCAL_CASE_PASS"),
            "capabilities_blocked": sum(1 for x in rows if x["outcome"] in ("BLOCKED_EXTERNAL", "BLOCKED_HITL")),
        },
        "disagreement_note": (
            "R6 writer brief describes 'ACC-001..ACC-262 plus the planning rows'; the authoritative "
            "file 7 section 6 enumerates ACC-001..ACC-279 (adds CNV-01..CNV-19 and 16 delivery "
            "artifacts and CNV-USER-JOURNEY). File 7 wins; this trace covers ACC-001..ACC-279."),
    })
    assert len(planning) == 221, len(planning)
    return d


# --------------------------------------------------------- 5 AUDIT_24_CLOSURE
def build_audit():
    rows = []
    for r in audit["rows"]:
        disp = "BLOCKED_EXTERNAL"
        reason = "LOCAL_DESIGN_REPAIR_ONLY_EXTERNAL_PROOF_PENDING; requires independent checker receipt and/or external authority not reachable in this lane"
        rows.append({
            "id": r["id"],
            "severity": r["severity"],
            "priority": r["priority"],
            "root_cause": r["root_cause"],
            "required_patch": r["required_patch"],
            "acceptance_close_predicate": r["acceptance_close_predicate"],
            "owner": r["owner"],
            "audit_locator": r["audit_locator"],
            "source_locator": r["source_locator"],
            "evidence_paths": [],
            "convergence_status": r.get("convergence_status"),
            "disposition": disp,
            "disposition_reason": reason,
        })
    d = base()
    d.update({
        "artifact": "AUDIT_24_CLOSURE.json",
        "closed": 0,
        "open": 24,
        "blocked_external": 24,
        "rows": rows,
        "notes": [
            "No AUD finding can be CLOSED_WITH_EVIDENCE in this lane: each close predicate needs an "
            "independent checker receipt or an external authority condition.",
            "Every row is BLOCKED_EXTERNAL with the exact close predicate it must satisfy.",
        ],
    })
    return d


# ------------------------------------------------------ 6 K_LEDGER_CROSSWALK
def build_k_ledger():
    rows = []
    for r in kledger["rows"]:
        rows.append({
            "id": r["id"],
            "finding": r["finding"],
            "remote_status": r["remote_status"],
            "evidence_or_gap": r["evidence_or_gap"],
            "local_convergence_reverification": "NOT_RUN",
            "closure_claim": "NOT_MADE",
            "mapped": False,
            "unmapped_reason": "no local re-verification receipt bound to this K entry in this lane",
        })
    d = base()
    d.update({
        "artifact": "K_LEDGER_CROSSWALK.json",
        "remote_main": kledger["remote_main"],
        "remote_main_source": "public read-only observed main sha (readback only; no publication)",
        "claim": kledger["claim"],
        "rows": rows,
        "mapped_count": 0,
        "unmapped_count": len(rows),
        "notes": [
            "Every K-ledger entry is recorded explicitly as UNMAPPED rather than guessed.",
            "K-06 runtime binding mismatch is corroborated by cap04_hermes_version (served 0.21.5 vs declared 0.20.0).",
        ],
    })
    return d


# -------------------------------------------------- 7 RUNNER_AND_TEST_MATRIX
def build_runner_matrix():
    exec_rows = []
    for pid in sorted(all_probes):
        p = all_probes[pid]
        exec_rows.append({
            "probe_id": pid,
            "command": p["command"],
            "cwd": p["cwd"],
            "started_utc": p["started_utc"],
            "ended_utc": p["ended_utc"],
            "exit_code": p["exit_code"],
            "timed_out": p.get("timed_out"),
            "raw_log_paths": {"stdout": p["stdout_file"], "stderr": p["stderr_file"]},
            "stdout_sha256": p["stdout_sha256"],
            "stderr_sha256": p["stderr_sha256"],
        })
    mut_rows = []
    for p in sorted(muts, key=lambda x: x["probe_id"]):
        mut_rows.append({
            "probe_id": p["probe_id"],
            "command": p["command"],
            "cwd": p["cwd"],
            "started_utc": p["started_utc"],
            "exit_code": p["exit_code"],
            "raw_log_paths": {"stdout": p["stdout_file"], "stderr": p["stderr_file"]},
            "stdout_sha256": p["stdout_sha256"],
        })
    planned = matrix["rows"]
    d = base()
    d.update({
        "artifact": "RUNNER_AND_TEST_MATRIX.json",
        "planned_cases": matrix["planned"],
        "executed_capability_and_mutation_probes": len(exec_rows) + len(mut_rows),
        "planned_requirement_matrix_rows_unrun": len(planned),
        "executed_probes": exec_rows,
        "executed_mutations": mut_rows,
        "planned_matrix_blocked": [
            {"id": r["id"], "test_id": r["test_id"], "kind": r["kind"],
             "source_locator": r["source_locator"], "actual": None,
             "blockers": r.get("blockers")}
            for r in planned
        ],
        "note": "Every executed case's raw stdout/stderr lives under RAW/ with the listed paths.",
    })
    return d


# ---------------------------------------------------------- 8 MUTATIONS_18
EXECUTED_MUT = {
    "M01": ("mut_m01", "REJECT", "VALIDATOR_FAIL_CLOSED_TRUSTED_PACKAGE_SHA_MISMATCH"),
    "M03": ("mut_m03", "REJECT", "PI_SEMANTIC_FAIL"),
    "M04": ("mut_m04", "ACCEPT", "NOT_DETECTED_VALIDATOR_PASS"),
    "M05": ("mut_m05", "REJECT", "SCHEMA_ADDITIONAL_PROPERTIES_REJECTED"),
    "M06": ("mut_m06", "ACCEPT", "NOT_DETECTED_VALIDATOR_PASS"),
    "M11": ("mut_m11", "REJECT", "CLAIM_CEILING_REJECTED"),
    "M12": ("mut_m12", "REJECT", "CLAIM_CEILING_REJECTED"),
    "M14": ("mut_m14", "REJECT", "STALE_PROVIDER_REJECTED"),
    "M16": ("mut_m16", "ACCEPT", "NOT_DETECTED_VALIDATOR_PASS"),
    "M18": ("mut_m18", "REJECT", "SCHEMA_ADDITIONAL_PROPERTIES_REJECTED"),
}
NOT_RUN_MUT = {
    "M02": "plugin helper body inside frozen R5 corpus bytes not reachable without mutating frozen source",
    "M07": "legacy T01 fixture bytes not present in admitted physical source root",
    "M08": "64-bridge RQ02->T27 miswiring requires the frozen bridge registry bytes",
    "M09": "PI-01 vendor title fixture bytes not admitted",
    "M10": "WP-01 approval-ignore requires the owner WP/RBWI artifact bytes",
    "M13": "technology rename requires the frozen TechnologyAdmission ledger bytes",
    "M15": "RQ06->T22 mapping requires the frozen trace-crosswalk bytes",
    "M17": "duplicated RQ64 case requires the frozen registry projection bytes",
}


def build_mutations():
    rows = []
    for r in mutations["rows"]:
        mid = r["id"]
        row = {
            "id": mid,
            "mutation": r["mutation"],
            "expected": r["expected"],
            "planned_first_fail": r["first_fail"],
            "actual_execution": None,
            "observed": None,
            "validator_verdict": None,
            "first_fail": None,
            "raw_receipt": None,
            "not_run_reason": None,
        }
        if mid in EXECUTED_MUT:
            pid, observed, detail = EXECUTED_MUT[mid]
            p = all_probes.get(pid)
            row["actual_execution"] = "EXECUTED"
            row["observed"] = observed
            row["validator_verdict"] = detail
            row["first_fail"] = detail
            row["raw_receipt"] = p["stdout_file"] if p else None
            row["detected"] = observed == "REJECT"
        else:
            row["actual_execution"] = "NOT_RUN"
            row["observed"] = "NOT_RUN"
            row["not_run_reason"] = NOT_RUN_MUT.get(mid, "unconstructible in this lane")
        rows.append(row)
    d = base()
    detected = [r["id"] for r in rows if r.get("detected")]
    not_detected = [r["id"] for r in rows if r["observed"] == "ACCEPT"]
    not_run = [r["id"] for r in rows if r["observed"] == "NOT_RUN"]
    d.update({
        "artifact": "MUTATIONS_18.json",
        "executed": len(detected) + len(not_detected),
        "detected": len(detected),
        "not_detected": len(not_detected),
        "not_run": len(not_run),
        "rows": rows,
        "detected_ids": detected,
        "not_detected_ids": not_detected,
        "not_run_ids": not_run,
        "genuine_findings": [
            "M04 (ProfileBinding ASSURED->LITE) is NOT detected: validator PASS. Assurance-downgrade mutation slips through.",
            "M06 (domain oracle expected changed to 999) is NOT detected: validator PASS.",
            "M16 (trace atom digest mismatched, to_hash='f'*64) is NOT detected: validator PASS.",
        ],
        "note": "Observed outcomes are reported verbatim from RAW/mut_*.stdout.txt; no output was reconstructed.",
    })
    return d


# ------------------------------------------------------------- 9 EFFECTS_5
def build_effects():
    rows = [
        {"effect_id": "EFF-1", "plane": "SKILLS",
         "subject": "AVR/HGK 10/6 raw pieces; references nested; trigger/nontrigger; Curator stage/install/retire",
         "positive_acceptance": "Reconstruct byte equality from original source; invoke pinned host loader; deny fake pointer and unapproved retire",
         "negative": "Forge reply without real same-run independently read-back evidence => BLOCK",
         "positive_readback": "PARTIAL_LOCAL: cap_avr_skill_pack exit 0 PASS 8/8 skills, 56/56 cases (loader presence/parity)",
         "negative_readback": "NOT_RUN",
         "disposition": "NOT_RUN",
         "reason": "Byte-exact 10/6 reconstruction and Curator staged/installed/retired transitions need the frozen raw pieces as a real runnable subject; only the loader self-run was reachable locally."},
        {"effect_id": "EFF-2", "plane": "HERMES",
         "subject": "G1/route required=served; usage nonce; stdin/file; timeout child cleanup",
         "positive_acceptance": "Pin executable, sealed route and raw stdout+stderr; independent same-run receipt; deny provider-direct substitute",
         "negative": "Forge reply without real same-run independently read-back evidence => BLOCK",
         "positive_readback": "PARTIAL_LOCAL: cap04_hermes_version exit 0 (real stdout captured)",
         "negative_readback": "NOT_RUN",
         "disposition": "BLOCKED_HITL",
         "reason": "Sealed route / required=served arm audit cannot be certified because served runtime (0.21.5) differs from declared binding (0.20.0); Owner certification required (K-06)."},
        {"effect_id": "EFF-3", "plane": "FAR",
         "subject": "query results with real retriever, grounded reference, SQLite reads",
         "positive_acceptance": "Run fixed query corpus, independent fresh SELECT, deny ack with missing row",
         "negative": "Forge reply without real same-run independently read-back evidence => BLOCK",
         "positive_readback": "PARTIAL_LOCAL: cap13_fts5_positive exit 0 MATCH hit via real SQLite FTS5",
         "negative_readback": "LOCAL: cap13_fts5_negative malformed MATCH refused",
         "disposition": "PARTIAL_LOCAL",
         "reason": "Fresh independent SELECT readback was performed locally on the probe DB; same-subject independent checker receipt still required."},
        {"effect_id": "EFF-4", "plane": "DESKTOP",
         "subject": "Windows ACL/symlink scope; FS/API/browser world-effects and rollback",
         "positive_acceptance": "Isolation + OS audit + pre/post residue; WinError1314 tracked not hidden",
         "negative": "Forge reply without real same-run independently read-back evidence => BLOCK",
         "positive_readback": "PARTIAL_LOCAL: cap_pipd_project_unsafe exit 2 (unsafe destination refused); cap03_spine_teardown exit 0",
         "negative_readback": "LOCAL: out-of-scope write refused",
         "disposition": "PARTIAL_LOCAL",
         "reason": "Full OS ACL/symlink isolation proof not run; bounded-write refusal observed."},
        {"effect_id": "EFF-5", "plane": "FABRIC_CI",
         "subject": "Owner FROZEN allowlist; commit tree blob equality; trusted verifier; secrets scan",
         "positive_acceptance": "Readback commit blob, rulesets/CODEOWNERS, trust-base PR negative, deny untrusted PR check",
         "negative": "Forge reply without real same-run independently read-back evidence => BLOCK",
         "positive_readback": "NOT_RUN",
         "negative_readback": "NOT_RUN",
         "disposition": "BLOCKED_EXTERNAL",
         "reason": "No GitHub PAT (cap15_github_publish exit 2 GITHUB_AUTH_BLOCKED); no FROZEN allowlist or ruleset available locally; no publication performed."},
    ]
    d = base()
    d.update({
        "artifact": "EFFECTS_5.json",
        "source_slot": "SLOT:25_FUNCTIONAL_EFFECT_5.json in the Owner-approved PKG",
        "rows": rows,
        "not_run_count": sum(1 for r in rows if r["disposition"] == "NOT_RUN"),
        "note": "Each effect requires real same-run readback for promotion; none may be filled by inference.",
    })
    return d


# --------------------------------------------------------- 10 GATES_A_TO_H
def build_gates():
    rows = []
    for g in gate_rows:
        rows.append({
            "gate_id": g["gate_id"],
            "predicate": g["predicate"],
            "expected": g["expected"],
            "command_or_probe": g.get("command_or_probe"),
            "raw_receipt_required": g.get("raw_receipt_required"),
            "producer": g.get("producer"),
            "independent_checker": g.get("independent_checker"),
            "candidate_binding_head": g["candidate_binding"]["head"],
            "candidate_binding_package_sha256": g["candidate_binding"]["package_sha256"],
            "invalidation": g.get("invalidation"),
            "terminal_verdict": "NOT_RUN",
            "terminal_verdict_reason": "no real receipt held; gate runner UNBOUND and prerequisites (source/compiler/admission) not satisfied in this lane",
            "claim_level": "LOCAL",
        })
    d = base()
    d.update({
        "artifact": "GATES_A_TO_H.json",
        "rows": rows,
        "not_run_count": len(rows),
        "note": "No gate verdict is filled by inference or file presence.",
    })
    return d


# ----------------------------------------------- 11 MAKER_CHECKER_SEPARATION
def build_mcs():
    arts = [
        "SUBJECT_AND_SOURCE.json", "AUTHORITY_LOCK_STATUS.json", "COMPILER_RECEIPTS/index.json",
        "REQ_TRACE_221.json", "AUDIT_24_CLOSURE.json", "K_LEDGER_CROSSWALK.json",
        "RUNNER_AND_TEST_MATRIX.json", "MUTATIONS_18.json", "EFFECTS_5.json",
        "GATES_A_TO_H.json", "MAKER_CHECKER_SEPARATION.json", "TT_CR_REGISTER.json",
        "CHECKPOINT_AND_ROLLBACK.json", "PUBLICATION_RECEIPT.json",
        "EXTERNAL_ACCEPTANCE_HANDOFF.md", "NON_CLAIMS.md",
    ]
    rows = [{"artifact": a, "producer": PRODUCER, "independent_checker": CHECKER,
             "checker_is_maker": False, "maker_verdict": "PENDING_CHECKER", "claim_level": "LOCAL"}
            for a in arts]
    d = base()
    d.update({
        "artifact": "MAKER_CHECKER_SEPARATION.json",
        "rows": rows,
        "checker_identity": CHECKER,
        "checker_model_family": "opencode-go/glm-5.3-flash",
        "maker_model_family": "opencode-go/deepseek-v4.1-flash",
        "all_verdicts": "PENDING_CHECKER",
        "note": (
            "This lane is the maker only. No artifact carries a verdict other than "
            "PENDING_CHECKER. The independent checker is a different model family and is not this writer."),
    })
    return d


# ----------------------------------------------------------- 12 TT_CR_REGISTER
def build_tt_cr():
    d = base()
    d.update({
        "artifact": "TT_CR_REGISTER.json",
        "as_of_utc": utc_now(),
        "rows": [
            {
                "id": "TT-PIPD-03",
                "title": "Source reference disposition (SRC-DOC03)",
                "status": "RESOLVED",
                "resolution": "Owner order of 2026-10-15, option A: SRC-DOC03 -> SUPPORT, governs=false",
                "authority": "Owner decision 2026-10-15 (this session)",
                "prior_state": "source reference quarantined; no canonical disposition made",
                "evidence": "Owner instruction in this round's dispatch; recorded in this receipt",
            },
            {
                "id": "TT-PIPD-04",
                "title": "Bridge-mapping question",
                "status": "OPEN",
                "question": (
                    "How should the 64 RQ bridge map onto canonical 64+129 requirement granularity "
                    "so each project child can be projected from a signed mapping? (AUD-P0-03)"),
                "scope_note": (
                    "This ticket tracks a mapping/verification question only. It is NOT an equivalent "
                    "Oracle writer and does not supersede, replace, or stand in for the Owner-approved "
                    "PKG authority anchor."),
                "must_not": ["describe itself as an equivalent Oracle writer",
                             "claim canonical authority over source semantics"],
                "owner": "PI compiler owner / HGK Owner",
                "evidence": "AUDIT_24_CLOSURE.json AUD-P0-03",
            },
            {
                "id": "TT-PIPD-05",
                "title": "Hermes runtime binding certification",
                "status": "OPEN",
                "question": (
                    "Declared runtime binding (0.20.0 / v2026.8.3) differs from served "
                    "Hermes Agent v0.21.5 (2026.9.24); certify the correct current binding."),
                "owner": "Hermes Owner",
                "evidence": "RAW/cap04_hermes_version.stdout.txt; K_LEDGER_CROSSWALK.json K-06",
            },
            {
                "id": "CR-R6-01",
                "title": "Change request: declare missing lane binary",
                "status": "OPEN",
                "question": (
                    "Lane toolchain declaration references .../Codex/bin/2e5e00daee91c61d/codex.exe "
                    "which is absent on this host; supply or re-point the declared binary."),
                "owner": "Tooling owner",
                "evidence": "RAW/cap05_lane_toolchain_resolve.stdout.txt",
            },
        ],
        "note": "Only TT-PIPD-03 is RESOLVED; all others remain OPEN pending external/Owner action.",
    })
    return d


if __name__ == "__main__":
    receipts = copy_receipts()
    built = []
    built.append(write_json("SUBJECT_AND_SOURCE.json", build_subject_and_source()))
    built.append(write_json("AUTHORITY_LOCK_STATUS.json", build_authority_lock()))
    built.append(write_json("COMPILER_RECEIPTS/index.json", build_compiler_index(receipts)))
    built.append(write_json("REQ_TRACE_221.json", build_req_trace()))
    built.append(write_json("AUDIT_24_CLOSURE.json", build_audit()))
    built.append(write_json("K_LEDGER_CROSSWALK.json", build_k_ledger()))
    built.append(write_json("RUNNER_AND_TEST_MATRIX.json", build_runner_matrix()))
    built.append(write_json("MUTATIONS_18.json", build_mutations()))
    built.append(write_json("EFFECTS_5.json", build_effects()))
    built.append(write_json("GATES_A_TO_H.json", build_gates()))
    built.append(write_json("MAKER_CHECKER_SEPARATION.json", build_mcs()))
    built.append(write_json("TT_CR_REGISTER.json", build_tt_cr()))
    print("built %d artifacts" % len(built))
    for b in built:
        print(" ", b)
