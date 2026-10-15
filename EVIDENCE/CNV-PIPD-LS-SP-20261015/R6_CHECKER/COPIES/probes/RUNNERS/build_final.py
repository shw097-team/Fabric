#!/usr/bin/env python3
"""R6 bounded-writer delivery builder, part 3: R6_WRITE_SET.json and
R6_WRITER_RECEIPT.json.

Hashes every file actually written under R6_DELIVERY (excluding __pycache__ and
the write set itself), then emits the writer receipt with claims, ceilings,
capabilities qualified/blocked, boundary violations, non-actions, and the exact
rerun command for every executed probe.
"""
import hashlib
import json
import os
from datetime import datetime, timezone

ROOT = r"C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015"
DEL = os.path.join(ROOT, "R6_DELIVERY")
RUNNERS = os.path.join(DEL, "RUNNERS")

PRODUCER = "Codex CLI bounded writer EXECUTE lane (opencode-go/deepseek-v4.1-flash)"
CHECKER = "opencode-go/glm-5.3-flash (independent; not this writer)"

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


def write_json(name, obj):
    path = os.path.join(DEL, name)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return path


def base(refs=None):
    return {
        "producer": PRODUCER,
        "produced_utc": utc_now(),
        "source_hashes_used": SOURCE_HASHES_LIST,
        "raw_evidence_refs": refs or [],
        "verdict": "PENDING_CHECKER",
        "claim_level": "LOCAL",
    }


def cmd_str(command):
    """Render a command list as a runnable one-line PowerShell command."""
    parts = []
    for tok in command:
        if isinstance(tok, str) and (" " in tok or "\\" in tok or "/" in tok):
            parts.append('"' + tok.replace('"', '`"') + '"')
        else:
            parts.append(str(tok))
    return " ".join(parts)


def collect_reruns():
    """One rerun record per executed probe across all record files."""
    records = []
    seen = set()
    for fname in ["capability_probes.json", "supplement_probes.json",
                  "cap03_records.json", "mutation_records.json"]:
        p = os.path.join(RUNNERS, fname)
        if not os.path.exists(p):
            continue
        for rec in load(p):
            pid = rec["probe_id"]
            if pid in seen:
                continue
            seen.add(pid)
            records.append({
                "probe_id": pid,
                "record_file": "R6_DELIVERY/RUNNERS/" + fname,
                "command": rec["command"],
                "rerun_command": cmd_str(rec["command"]),
                "cwd": rec["cwd"],
                "exit_code": rec["exit_code"],
                "started_utc": rec["started_utc"],
                "stdout_file": rec["stdout_file"],
                "stderr_file": rec["stderr_file"],
                "stdout_sha256": rec.get("stdout_sha256"),
                "stderr_sha256": rec.get("stderr_sha256"),
            })
    records.sort(key=lambda r: r["probe_id"])
    return records


def collect_write_set():
    entries = []
    for dirpath, dirnames, filenames in os.walk(DEL):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for fn in filenames:
            if fn.endswith(".pyc"):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, DEL).replace("\\", "/")
            if rel == "R6_WRITE_SET.json":
                continue
            entries.append({
                "path": "R6_DELIVERY/" + rel,
                "bytes": os.path.getsize(full),
                "sha256": sha256_file(full),
            })
    entries.sort(key=lambda e: e["path"])
    return entries


if __name__ == "__main__":
    reruns = collect_reruns()

    # ---- R6_WRITER_RECEIPT.json -------------------------------------------
    capabilities = [
        {"capability": "native-prompt-compiler", "status": "QUALIFIED_LOCAL",
         "evidence": ["RAW/cap01_compiler_lint.stdout.txt", "RAW/cap01_compiler_activation.stdout.txt",
                      "RAW/cap01_compiler_acceptance.stdout.txt", "RAW/cap01_compiler_hash.stdout.txt",
                      "RAW/cap01_compiler_duplication.stdout.txt"],
         "note": "lint/activation/acceptance/hash/duplication all exit 0; PROMPT_COMPILE_PASS."},
        {"capability": "approved-document-verifier", "status": "BLOCKED_EXTERNAL",
         "evidence": ["RAW/cap02_pkg_check_run.stdout.txt", "RAW/cap02_pkg_check_locked.stdout.txt"],
         "note": "exit 30 FAIL_CLOSED MISSING_EXTERNAL_OWNER_APPROVED_LOCK; --check locked exit 30 SOURCE_PHYSICAL_MISSING.",
         "missing_condition": "external Owner-approved lock + physical source bytes for AUDIT_..._FULL_DESTRUCTIVE_2026-10-15(1).md",
         "smallest_unblock": "supply the Owner-approved lock file and the missing physical source document"},
        {"capability": "HGK-typed-spine-and-lifecycle", "status": "QUALIFIED_LOCAL",
         "evidence": ["RAW/cap03_spine_positive.stdout.txt", "RAW/cap03_spine_negative.stdout.txt",
                      "RAW/cap03_spine_acceptance.stdout.txt", "RAW/cap03_spine_fk_negative.stdout.txt"],
         "note": "positive/negative/acceptance exit 0; illegal transition refused; FK refused."},
        {"capability": "Hermes-canonical-runtime", "status": "BLOCKED_HITL",
         "evidence": ["RAW/cap04_hermes_version.stdout.txt"],
         "note": "served Hermes Agent v0.21.5 (2026.9.24) vs declared 0.20.0/v2026.8.3 (K-06).",
         "missing_condition": "Owner certification of the correct runtime binding",
         "smallest_unblock": "Owner certifies current runtime binding or re-points HG-KSEOS/config/hermes.json"},
        {"capability": "Codex-EXECUTE-DeepSeek", "status": "BLOCKED_EXTERNAL",
         "evidence": ["RAW/cap05_lane_toolchain_resolve.stdout.txt"],
         "note": "declared lane binary .../Codex/bin/2e5e00daee91c61d/codex.exe absent; resolve exit 3 ERR_LANE_TOOLCHAIN_BINARY_MISSING.",
         "missing_condition": "declared lane toolchain binary",
         "smallest_unblock": "supply or re-point the declared codex.exe path in the lane manifest"},
        {"capability": "Codex-VERIFY-GLM", "status": "BLOCKED_EXTERNAL",
         "evidence": ["RAW/checker_independent_run.stdout.txt"],
         "note": "check_acceptance_independent.py exit 1, verdict FAIL, denominator 92, 2 FAILs (TST-025, TST-048).",
         "missing_condition": "independent GLM verify arm producing ACCEPT with denominator 92",
         "smallest_unblock": "Owner supplies the GLM verify arm / fixes the 2 failing TST cases"},
        {"capability": "Hermes-Kanban", "status": "QUALIFIED_LOCAL",
         "evidence": ["RAW/cap07_kanban_boards.stdout.txt"], "note": "hermes kanban boards list exit 0."},
        {"capability": "Hermes-Swarm", "status": "QUALIFIED_LOCAL",
         "evidence": ["RAW/cap08_swarm_help.stdout.txt"], "note": "hermes kanban swarm --help exit 0."},
        {"capability": "gstack-advisory", "status": "QUALIFIED_LOCAL",
         "evidence": ["RAW/cap11_gstack_positive.stdout.txt", "RAW/cap11_gstack_negative.stdout.txt"],
         "note": "positive/negative exit 0."},
        {"capability": "OpenSpec-brownfield", "status": "QUALIFIED_LOCAL",
         "evidence": ["RAW/cap12_openspec_version.stdout.txt"], "note": "openspec --version exit 0 = 1.8.0."},
        {"capability": "AVR-HGK-Skill-loader", "status": "QUALIFIED_LOCAL",
         "evidence": ["RAW/cap_avr_skill_pack.stdout.txt"], "note": "exit 0 PASS 8/8 skills, 56/56 cases."},
        {"capability": "FAR-SQLite-FTS5", "status": "QUALIFIED_LOCAL",
         "evidence": ["RAW/cap13_fts5_positive.stdout.txt", "RAW/cap13_fts5_negative.stdout.txt",
                      "RAW/cap13_fts5_teardown.stdout.txt"],
         "note": "FTS5 positive/negative/teardown exit 0."},
        {"capability": "bounded-FS-API-Desktop", "status": "QUALIFIED_LOCAL",
         "evidence": ["RAW/cap_pipd_project_unsafe.stdout.txt"], "note": "unsafe destination refused exit 2."},
        {"capability": "approval-gated-GitHub", "status": "BLOCKED_EXTERNAL",
         "evidence": ["RAW/cap15_github_publish.stdout.txt"],
         "note": "github_publish.py exit 2 PAT_PRESENT=false verdict GITHUB_AUTH_BLOCKED.",
         "missing_condition": "GitHub PAT (off-limits to this lane; no secret material may be read)",
         "smallest_unblock": "Owner authorizes a publication lane that holds the PAT"},
        {"capability": "pipd-route-intake", "status": "QUALIFIED_LOCAL",
         "evidence": ["RAW/cap_pipd_intake.stdout.txt", "RAW/cap_pipd_intake_missing.stdout.txt",
                      "RAW/cap_pipd_intake_ambiguous.stdout.txt"],
         "note": "intake exit 0; missing/ambiguous refused."},
        {"capability": "pipd-authority-source", "status": "QUALIFIED_LOCAL",
         "evidence": ["RAW/cap_pipd_intake_pkg.stdout.txt"], "note": "intake-pkg exit 0."},
        {"capability": "pipd-profile-tailor", "status": "QUALIFIED_LOCAL",
         "evidence": ["RAW/cap_pipd_profile_ok.stdout.txt", "RAW/cap_pipd_profile.stdout.txt"],
         "note": "profile-ok exit 0; unknown axis refused (exit 9)."},
        {"capability": "pipd-pi-compile", "status": "QUALIFIED_LOCAL",
         "evidence": ["RAW/cap_pipd_compile_pi.stdout.txt", "RAW/cap_pipd_compile_pi_tamper.stdout.txt"],
         "note": "compile-pi exit 0; tamper refused."},
        {"capability": "pipd-pd-bind", "status": "QUALIFIED_LOCAL",
         "evidence": ["RAW/cap_pipd_bind_pd.stdout.txt", "RAW/cap_pipd_bind_pd_nocxt.stdout.txt"],
         "note": "bind-pd exit 0; no-RepoContext refused."},
        {"capability": "pipd-execution-contract", "status": "QUALIFIED_LOCAL",
         "evidence": ["RAW/cap_pipd_ecp.stdout.txt"], "note": "ecp exit 0."},
        {"capability": "pipd-assurance-tqaep", "status": "QUALIFIED_LOCAL",
         "evidence": ["RAW/cap_pipd_tqaep.stdout.txt", "RAW/cap_pipd_tqaep_self.stdout.txt",
                      "RAW/cap_pipd_tqaep_noreceipt.stdout.txt"],
         "note": "tqaep exit 0; self/noreceipt refused."},
        {"capability": "pipd-package-project", "status": "QUALIFIED_LOCAL",
         "evidence": ["RAW/cap_pipd_claim_ladder_ok.stdout.txt", "RAW/cap_pipd_claim_ceiling.stdout.txt"],
         "note": "project-unsafe exit 2; claim ladder LOCAL_QUALIFIED."},
    ]
    qualified = [c["capability"] for c in capabilities if c["status"] == "QUALIFIED_LOCAL"]
    blocked = [c for c in capabilities if c["status"].startswith("BLOCKED")]

    mutations = load(os.path.join(DEL, "MUTATIONS_18.json"))

    receipt = base(refs=["RUNNERS/capability_probes.json", "RUNNERS/supplement_probes.json",
                         "RUNNERS/cap03_records.json", "RUNNERS/mutation_records.json",
                         "RAW/cap_checkpoint_drill.json"])
    receipt.update({
        "artifact": "R6_WRITER_RECEIPT.json",
        "round": "CNV-PIPD-LS-SP-20261015-R6",
        "lane": "EXECUTE (Codex CLI bounded writer, opencode-go/deepseek-v4.1-flash)",
        "claim_ceiling": "LOCAL",
        "final_status": "PARTIAL",
        "status_rationale": ("Real capability probes ran and are captured raw, but multiple "
                             "capabilities are BLOCKED_EXTERNAL/HITL, 3 executed mutations were NOT "
                             "detected, and 0/221 requirement cases / 0/8 gates / 0/24 AUD closures "
                             "are complete. This is a partial candidate, not a ready set."),

        "authoritative_order": {
            "file": "compiler_native_output_R5/thin-prompt.md",
            "sha256": SOURCE_HASHES["compiler_native_output_R5/thin-prompt.md"],
            "compiler_state": "PROMPT_COMPILE_PASS",
            "rule": "file 7 governs over the writer brief where they disagree",
        },

        "claims": [
            {"claim": "22 ACTIVE_REQUIRED capabilities probed on this host",
             "ceiling": "LOCAL", "result": "17 QUALIFIED_LOCAL, 4 BLOCKED_EXTERNAL, 1 BLOCKED_HITL"},
            {"claim": "18 hostile mutation cases attempted", "ceiling": "LOCAL",
             "result": "10 executed (7 detected, 3 NOT detected), 8 NOT_RUN (frozen R5 corpus bytes unreachable)"},
            {"claim": "checkpoint/rollback drill performed on own WriteSet", "ceiling": "LOCAL",
             "result": "mutation detected by re-hash; rolled back to exact original sha; re-verified"},
            {"claim": "221 planning requirement cases traced", "ceiling": "LOCAL",
             "result": "0 executed; all BLOCKED_NOT_RUN / REAL_RUNNER_NOT_BOUND"},
            {"claim": "24 AUD findings classified", "ceiling": "LOCAL",
             "result": "0 CLOSED_WITH_EVIDENCE; all OPEN/BLOCKED_EXTERNAL/NOT_RUN"},
            {"claim": "8 evidence gates A..H assessed", "ceiling": "LOCAL",
             "result": "0 passed; all NOT_RUN (no real receipt held)"},
            {"claim": "K-ledger crosswalk materialized", "ceiling": "LOCAL",
             "result": "0 mapped; 20 explicitly UNMAPPED (no guessing)"},
        ],
        "claim_ceiling_statement": ("No artifact in this delivery carries a verdict other than "
                                    "PENDING_CHECKER, and no claim above LOCAL is made. Acceptance "
                                    "is reserved for the independent Acceptance Officer."),

        "capabilities": capabilities,
        "capabilities_qualified": qualified,
        "capabilities_blocked": [{"capability": c["capability"], "status": c["status"],
                                  "missing_condition": c.get("missing_condition")} for c in blocked],
        "capability_counts": {"ACTIVE_REQUIRED": 22, "QUALIFIED_LOCAL": len(qualified),
                              "BLOCKED_EXTERNAL": sum(1 for c in blocked if c["status"] == "BLOCKED_EXTERNAL"),
                              "BLOCKED_HITL": sum(1 for c in blocked if c["status"] == "BLOCKED_HITL")},

        "mutations_summary": {
            "executed": mutations["executed"], "detected": mutations["detected"],
            "not_detected": mutations["not_detected"], "not_run": mutations["not_run"],
            "detected_ids": mutations["detected_ids"],
            "not_detected_ids": mutations["not_detected_ids"],
            "not_run_ids": mutations["not_run_ids"],
            "genuine_findings": mutations["genuine_findings"],
        },

        "blocked_external": [
            "Codex-EXECUTE-DeepSeek: declared lane binary .../Codex/bin/2e5e00daee91c61d/codex.exe absent (ERR_LANE_TOOLCHAIN_BINARY_MISSING)",
            "Codex-VERIFY-GLM: checker arm exit 1, verdict FAIL (TST-025, TST-048); no GLM accept arm",
            "approved-document-verifier: external Owner-approved lock + physical source bytes missing",
            "approval-gated-GitHub: no PAT (and secret material is off-limits to this lane)",
            "221 planning requirement cases: source physical / admission not bound",
            "8 hostile mutations (M02,M07,M08,M09,M10,M13,M15,M17): frozen R5 corpus bytes unreachable",
            "24 AUD findings: independent checker receipts / external authority conditions absent",
            "8 evidence gates A..H: no real gate runners bound",
            "K-ledger: remote_main read-only only; no authorized mapping sources",
        ],

        "boundary_violations": [],
        "boundary_statement": (
            "No write occurred outside R6_DELIVERY/. Nothing under C:/Projects/Agent_Workspace/API KEY/ "
            "was read, copied, or referenced. The source corpus and Shared Spine were not modified. "
            "No network egress and no repository publication occurred."),

        "did_not_do": [
            "No repository publication, no network egress, no remote operations.",
            "No secret/credential material read, copied, or referenced.",
            "No verdict other than PENDING_CHECKER; no self-acceptance.",
            "No claim above LOCAL.",
            "No modification of the source corpus or Shared Spine (no raw SQL state mutation).",
            "No closure of AUD findings, gates, or requirement cases by inference or file presence.",
            "No K-ledger mapping guessed; unmapped entries marked explicitly.",
            "No re-authoring of the Owner-approved PKG authority anchor.",
        ],

        "disagreements_with_writer_brief": [
            {
                "topic": "ACC range",
                "brief": "ACC-001..ACC-262 plus planning rows (=> 221)",
                "file_7": "ACC-001..ACC-279 (adds CNV-01..CNV-19 ACC-244..262, 16 delivery artifacts ACC-263..278, CNV-USER-JOURNEY ACC-279)",
                "resolution": "file 7 wins: REQ_TRACE_221.json enumerates 279 requirement rows; DENOMINATOR 221 stays 64 RQ parents + 129 children + 28 legacy T (planning rows), with CNV rows recorded separately.",
                "recorded_in": ["REQ_TRACE_221.json disagreement_note"],
            },
            {
                "topic": "thin-prompt sha256 prefix",
                "brief": "sha256 prefix 2f247960d5f1",
                "observed": "2f246796c3b927170a90ed7dd3f4307e913579db2efb56b307cbc2377a1cb77f",
                "resolution": "The file actually read (file 7) hashes to 2f246796c3b9...; the brief's stated prefix does not match the file present on disk. Recorded as a minor mismatch; the on-disk file governs.",
                "recorded_in": ["SUBJECT_AND_SOURCE.json"],
            },
        ],

        "executed_probe_count": len(reruns),
        "rerun_commands": reruns,
        "rerun_command_note": ("Each entry gives the record file, exact argv, one-line PowerShell "
                               "rerun_command, cwd, exit code, UTC, and raw stdout/stderr paths+hashes."),

        "checker": {"identity": CHECKER, "model_family": "opencode-go/glm-5.3-flash",
                    "relationship": "independent checker; different family from this writer",
                    "checker_is_writer": False},
        "producer_model_family": "opencode-go/deepseek-v4.1-flash",

        "pending_checker_note": ("All 16 top-level artifacts plus RAW/ and RUNNERS/ are candidate "
                                 "evidence. Nothing is accepted; verdicts remain PENDING_CHECKER."),
    })
    write_json("R6_WRITER_RECEIPT.json", receipt)
    final_sha = sha256_file(os.path.join(DEL, "R6_WRITER_RECEIPT.json"))

    # ---- R6_WRITE_SET.json -------------------------------------------------
    # Computed AFTER the receipt is written so R6_WRITER_RECEIPT.json is included
    # with a stable hash. R6_WRITE_SET.json excludes only itself (self-hash is
    # impossible); its own hash is emitted on stdout below.
    write_set = collect_write_set()
    write_set_doc = base()
    write_set_doc.update({
        "artifact": "R6_WRITE_SET.json",
        "note": ("Every file this lane wrote under R6_DELIVERY, with bytes and sha256. "
                 "__pycache__/.pyc are excluded. R6_WRITE_SET.json excludes only itself; "
                 "R6_WRITER_RECEIPT.json IS included (hash below). R6_WRITE_SET.json's own "
                 "hash is emitted by RUNNERS/build_final.py stdout."),
        "root": "R6_DELIVERY/",
        "receipt_sha256": final_sha,
        "file_count": len(write_set),
        "total_bytes": sum(e["bytes"] for e in write_set),
        "files": write_set,
    })
    write_json("R6_WRITE_SET.json", write_set_doc)
    ws_sha = sha256_file(os.path.join(DEL, "R6_WRITE_SET.json"))
    print(json.dumps({
        "wrote": ["R6_WRITE_SET.json", "R6_WRITER_RECEIPT.json"],
        "write_set_files": len(write_set),
        "write_set_sha256": ws_sha,
        "receipt_sha256": final_sha,
        "rerun_records": len(reruns),
        "capabilities": receipt["capability_counts"],
    }, ensure_ascii=False))
