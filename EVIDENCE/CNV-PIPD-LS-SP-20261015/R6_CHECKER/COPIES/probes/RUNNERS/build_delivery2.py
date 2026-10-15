#!/usr/bin/env python3
"""R6 bounded-writer delivery builder, part 2: checkpoint drill record,
publication receipt, external acceptance handoff, non-claims."""
import hashlib
import json
import os
from datetime import datetime, timezone

ROOT = r"C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015"
DEL = os.path.join(ROOT, "R6_DELIVERY")
RAW = os.path.join(DEL, "RAW")

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


def write_text(name, text):
    path = os.path.join(DEL, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
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


drill_raw = load(os.path.join(RAW, "cap_checkpoint_drill.json"))


def build_checkpoint():
    d = base(["RAW/cap_checkpoint_drill.json", "RAW/cap_checkpoint_drill.stdout.txt"])
    d.update({
        "artifact": "CHECKPOINT_AND_ROLLBACK.json",
        "drill_subject": "R6_DELIVERY/CHECKPOINT_DRILL_SUBJECT.json",
        "drill_runner": "RUNNERS/checkpoint_drill.py",
        "drill_command": drill_raw["command"],
        "drill_cwd": drill_raw["cwd"],
        "drill_started_utc": drill_raw["started_utc"],
        "drill_exit_code": drill_raw["exit_code"],
        "drill_stdout_file": drill_raw["stdout_file"],
        "drill_stdout_sha256": drill_raw["stdout_sha256"],
        "snapshot_sha256": "1052061aeaae04784fb45ba2f2a5f4916f359875f54d03401c1fe0bb669f949d",
        "mutated_sha256": "938f220a787f260f4c4e4d96ef8865400a30d5849e8ff84d9cbdb39686d7ddd9",
        "restored_sha256": "1052061aeaae04784fb45ba2f2a5f4916f359875f54d03401c1fe0bb669f949d",
        "mutation_detected": True,
        "rollback_verified": True,
        "rollback_pointer": "R6_DELIVERY/CHECKPOINT_DRILL_SUBJECT.json (restored to snapshot sha)",
        "checkpoint_fields": {
            "task_id": "CNV-PIPD-LS-SP-20261015-R6",
            "source_hashes": SOURCE_HASHES_LIST,
            "current_candidate": "R6_DELIVERY (LOCAL candidate; head NOT_CREATED)",
            "completed_gates": [],
            "open_gates": ["G-A", "G-B", "G-C", "G-D", "G-E", "G-F", "G-G", "G-H"],
            "next_work_order": "supply physical sources + authoritative oracle mapping; then bind gate runners",
            "rollback_pointer": "R6_DELIVERY/CHECKPOINT_DRILL_SUBJECT.json",
            "typed_admission_ids": ["HGK_TYPED_ADMISSION_R6 ADMISSION_OK (WORKORDERS_ADMITTED)"],
            "open_tt_cr": ["TT-PIPD-04", "TT-PIPD-05", "CR-R6-01"],
            "raw_evidence_refs": ["RAW/cap_checkpoint_drill.json"],
            "resume_condition": "Owner supplies missing physical sources and certifies runtime binding",
        },
        "note": "The drill mutated, detected the mutation by re-hash, rolled back to exact original bytes, and re-verified.",
    })
    return d


def build_publication(candidates):
    d = base()
    d.update({
        "artifact": "PUBLICATION_RECEIPT.json",
        "repository_publication_performed": False,
        "network_egress_performed": False,
        "remote_operations_performed": False,
        "secret_export_performed": False,
        "source_corpus_modified": False,
        "writes_inside_writeset_only": True,
        "github": {
            "repository": "shw097-team/Fabric",
            "observed_main_sha_readonly": "266f8d65cf9b21c3b37c1c243946a5c828cf973b",
            "token_present": False,
            "draft_pr": None,
            "publish_probe": "RAW/cap15_github_publish.stdout.txt (exit 2, GITHUB_AUTH_BLOCKED)",
        },
        "candidate_path_set": candidates,
        "awaiting": "Owner-ordered handoff of the exact candidate path set + hashes to the independent Acceptance Officer",
        "note": ("This lane performed no repository publication and no network egress. The path set below is a local "
                 "candidate awaiting Owner-ordered handoff."),
    })
    return d


NON_CLAIMS = """# R6 NON_CLAIMS

producer: {producer}
produced_utc: {utc}
verdict: PENDING_CHECKER
claim_level: LOCAL

This round does NOT claim any of the following:

- No verdict, approval, release, or acceptance state is claimed. Every artifact carries `verdict=PENDING_CHECKER`.
- No claim above the LOCAL ceiling. Capability dispositions are LOCAL candidate evidence only.
- No independent acceptance. This lane is the maker; it never accepts its own work.
- No canonical admission of the 22 capabilities. Capability qualification is candidate evidence, not admission.
- No production/live/trade readiness, and no release readiness.
- No world-effect truth. Tool/provider success is recorded as an AUTHORIZED_ATTEMPT/OBSERVATION, not as CONFIRMED_EFFECT.
- No closure of any of the 24 AUD findings (all remain BLOCKED_EXTERNAL).
- No closure of the eight evidence gates G-A..G-H (all remain NOT_RUN).
- No execution of the 221 planned requirement cases (0 executed; all BLOCKED_NOT_RUN).
- No completion of the 18 hostile cases (10 executed, 8 NOT_RUN; 3 executed cases were NOT detected and are reported as gaps).
- No mapping of any K-ledger entry (all 20 remain explicitly UNMAPPED).
- No repository publication, no network egress, no remote operations, no secret export.
- No modification of the source corpus or the Shared Spine (no raw SQL state mutation).
- No re-authoring of the Owner-approved PKG authority anchor and no equivalent-Oracle-writer claim.
- No cryptographic signature claim: the Owner trust lock is an interactive attestation, not a cryptographic signature.
- No claim that the three not-detected mutations (M04, M06, M16) are harmless; they are reported as genuine detection gaps.
""".format(producer=PRODUCER, utc=utc_now())


HANDOFF = """# R6 EXTERNAL ACCEPTANCE HANDOFF

producer: {producer}
produced_utc: {utc}
verdict: PENDING_CHECKER
claim_level: LOCAL

This document tells an independent Acceptance Officer (different model family,
`opencode-go/glm-5.3-flash`, and/or the canonical AO) exactly what to re-run and what
evidence each re-run must produce. The AO must not trust any verdict in this lane.

## 0. Ground rules for the AO

- Read and hash, in order: `OWNER_TRUST_LOCK.json`, `HG-KSEOS/AGENTS.md`, `Fabric/AGENTS.md`,
  the Owner-approved PKG, the commander PROMPT, `C0_C9_CONTRACT_R5.json`,
  `compiler_native_output_R5/thin-prompt.md`.
- The compiled thin prompt (`thin-prompt.md`, sha256 `2f246796c3b927170a90ed7dd3f4307e913579db2efb56b307cbc2377a1cb77f`)
  is the authoritative job order; file 7 wins over the writer brief where they disagree.
- Re-run every command yourself; produce your own raw stdout/stderr/exit and your own hashes.

## 1. Capability qualification (22 ACTIVE_REQUIRED)

For each capability, re-run the recorded probe(s) and confirm positive/negative behavior on the
same subject. Raw evidence lives under `R6_DELIVERY/RAW/`.

- native-prompt-compiler: `python <compiler>/scripts/prompt_contract_compiler.py lint|activation|acceptance|render|hash|duplication <contract>`
  - required: exit 0 and `PROMPT_COMPILE_PASS`; evidence `RAW/cap01_compiler_*.stdout.txt`.
- approved-document-verifier: `python pipd_pkg_v2_check.py --doc <pkg> --check` and `--materialize`
  - required either way: exit 30 `FAIL_CLOSED MISSING_EXTERNAL_OWNER_APPROVED_LOCK` or `SOURCE_PHYSICAL_MISSING`.
  - unblock: supply the external Owner-approved lock and the missing physical source bytes.
- HGK-typed-spine-and-lifecycle: run `RUNNERS/probe_spine_lifecycle.py positive|negative|acceptance` and `RUNNERS/probe_spine_fk.py`
  - required: illegal transition refused; acceptance idempotency; FK refusal.
- Hermes-canonical-runtime: re-run `hermes --version`; compare to `HG-KSEOS/config/hermes.json`.
  - expected finding: served v0.21.5 (2026.9.24) vs declared 0.20.0/v2026.8.3. Owner certification needed.
- Codex-EXECUTE-DeepSeek: resolve the declared lane binary and run `runtime_role_binding_assert.py`.
  - expected: declared binary `.../Codex/bin/2e5e00daee91c61d/codex.exe` is absent (`ERR_LANE_TOOLCHAIN_BINARY_MISSING`).
- Codex-VERIFY-GLM: run `HG-KSEOS/tools/check_acceptance_independent.py`; independently confirm denominator/failures.
- Hermes-Kanban: `hermes kanban boards list`.
- Hermes-Swarm: `hermes kanban swarm --help`.
- gstack-advisory: `RUNNERS/probe_gstack_rolemap.py positive|negative`.
- OpenSpec-brownfield: `openspec --version` (full path `C:/Users/user/AppData/Roaming/npm/openspec.cmd`).
- AVR-HGK-Skill-loader: run the skill pack self-run (`--all`).
- FAR-SQLite-FTS5: `RUNNERS/probe_fts5.py positive|negative|teardown`.
- bounded-FS-API-Desktop: re-run the PIPD unsafe-destination guard (`project-unsafe`).
- approval-gated-GitHub: `python PIPD/tools/github_publish.py`; expected `GITHUB_AUTH_BLOCKED` unless a PAT is supplied.
- pipd-route-intake / pipd-authority-source / pipd-profile-tailor / pipd-pi-compile / pipd-pd-bind /
  pipd-execution-contract / pipd-assurance-tqaep / pipd-package-project:
  `RUNNERS/probe_pipd_chain.py <case>`; required: positive exit 0 and negative refusal with the recorded reason.

## 2. Requirement trace (221 planning cases)

- Re-run the 64 RQ parents, 129 children and 28 legacy T cases with a real bound runner.
- Required evidence per case: command, cwd, UTC, exit code, raw stdout/stderr, producer, independent checker.
- Current state: 0/221 executed; all BLOCKED_NOT_RUN (source physical missing / admission not run).

## 3. Hostile mutations (18)

- Re-run `RUNNERS/probe_mutations.py <m01..m18>` for each constructible case.
- Required evidence: `RAW/mut_<id>.stdout.txt` with observed outcome and validator verdict.
- The AO must specifically confirm the three gaps: M04, M06, M16 were NOT detected (validator PASS).

## 4. AUD findings (24)

- For each AUD close predicate, obtain the independent checker receipt or external authority condition.
- Required evidence: a same-subject receipt proving the stated close predicate, not a file-presence check.

## 5. Gates G-A..G-H

- Bind each gate runner, run positive/negative/first-fail, capture raw receipts, and pair with an
  independent checker. All eight are currently NOT_RUN.

## 6. Checkpoint / rollback

- Re-run `RUNNERS/checkpoint_drill.py` and verify: mutation detected by re-hash, rollback to exact
  original sha `1052061aeaae04784fb45ba2f2a5f4916f359875f54d03401c1fe0bb669f949d`.

## 7. Publication receipt

- Confirm no repository publication and no network egress occurred from this lane.

## 8. Exact evidence each re-run must produce

- command, cwd, UTC start, exit code
- raw stdout file and raw stderr file (sha256 recorded)
- producer identity and independent checker identity (different family)
- source hashes used and candidate package sha
- invalidation rule, rollback pointer, and residue readback
""".format(producer=PRODUCER, utc=utc_now())


if __name__ == "__main__":
    # Write the three non-receipt artifacts first so the publication receipt's
    # candidate path set is computed over the real, already-materialized set.
    write_json("CHECKPOINT_AND_ROLLBACK.json", build_checkpoint())
    write_text("NON_CLAIMS.md", NON_CLAIMS)
    write_text("EXTERNAL_ACCEPTANCE_HANDOFF.md", HANDOFF)
    candidates = []
    for name in ["SUBJECT_AND_SOURCE.json", "AUTHORITY_LOCK_STATUS.json", "COMPILER_RECEIPTS/index.json",
                 "REQ_TRACE_221.json", "AUDIT_24_CLOSURE.json", "K_LEDGER_CROSSWALK.json",
                 "RUNNER_AND_TEST_MATRIX.json", "MUTATIONS_18.json", "EFFECTS_5.json",
                 "GATES_A_TO_H.json", "MAKER_CHECKER_SEPARATION.json", "TT_CR_REGISTER.json",
                 "CHECKPOINT_AND_ROLLBACK.json", "EXTERNAL_ACCEPTANCE_HANDOFF.md", "NON_CLAIMS.md"]:
        p = os.path.join(DEL, name)
        if os.path.exists(p):
            candidates.append({"path": "R6_DELIVERY/" + name, "sha256": sha256_file(p),
                               "bytes": os.path.getsize(p)})
    # PUBLICATION_RECEIPT.json is intentionally excluded from its own candidate set:
    # its sha256 is unstable by construction. R6_WRITE_SET.json carries its hash.
    write_json("PUBLICATION_RECEIPT.json", build_publication(candidates))
    print("wrote CHECKPOINT_AND_ROLLBACK.json, NON_CLAIMS.md, EXTERNAL_ACCEPTANCE_HANDOFF.md, PUBLICATION_RECEIPT.json")
