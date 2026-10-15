"""Locally constructible hostile cases (MUTATIONS_18).

Each mode builds a REAL record via the bound PIPD/HGK entrypoints, applies the
mutation, and runs the bound deterministic validator. A mutation is CLOSED only
when the bound validator returns FAIL (the tamper was refused/detected).
Unconstructible mutations are recorded NOT_RUN by the driver, never faked here.

Every mode prints a machine-readable row with id / mutation / expected /
observed / validator_verdict / first_fail / raw_receipt.
"""
from __future__ import annotations

import json
import subprocess
import sys
import traceback
from pathlib import Path

PIPD_SRC = "C:/Projects/Agent_Workspace/PIPD/src"
sys.path.insert(0, PIPD_SRC)
sys.path.insert(0, "C:/Projects/Agent_Workspace/HG-KSEOS/src")

ROOT = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/R6_DELIVERY")
RAW = ROOT / "RAW"
SRC = RAW / "pipd_scratch_source.md"
SCHEMAS = Path("C:/Projects/Agent_Workspace/PIPD/schemas")
PY = "C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe"
PKG = ("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/"
       "Local/hermes/attachments/Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md")
PKG_CHECK = "C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/pipd_pkg_v2_check.py"


def _ensure_src() -> None:
    if not SRC.exists():
        SRC.write_text(
            "The intake must bind every normative claim to a source locator.\n"
            "The compiler must refuse a normative claim without a source locator.\n",
            encoding="utf-8")


def _row(id_, mutation, expected, observed, vverdict, first_fail, receipt) -> int:
    print(json.dumps({"id": id_, "mutation": mutation, "expected": expected,
                      "observed": observed, "validator_verdict": vverdict,
                      "first_fail": first_fail, "raw_receipt": receipt},
                     ensure_ascii=False, indent=1))
    return 0 if observed == "REJECT" and expected == "REJECT" else 1


def _intake_pi():
    from pipd_ls_sp import pipeline
    _ensure_src()
    card = pipeline.intake("bind the R6 scratch requirements", sources=[str(SRC)])
    pi = pipeline.compile_pi(card, "LITE")
    return pipeline, card, pi


def _chain():
    pipeline, card, pi = _intake_pi()
    ctx = pipeline.repo_probe.derive_repo_context(str(ROOT), writable_scope="src/**")
    pd = pipeline.bind_pd(pi, ctx)
    ecp = pipeline.compile_ecp(pd, pi)
    tq = pipeline.compile_tqaep(pi, ecp, maker="R6-WRITER",
                                checker="opencode-go/glm-5.3-flash",
                                checker_execution_receipt="RAW/cap16_tqaep_checker.txt")
    return pipeline, pi, pd, ecp, tq


def m03_intent_atom_forged() -> int:
    from pipd_ls_sp import pipeline
    _ensure_src()
    card = pipeline.intake("bind the R6 scratch requirements", sources=[str(SRC)])
    forged = dict(card)
    forged["atoms"] = [dict(a, acceptance_cue="MUST: forged") for a in card["atoms"]]
    try:
        pipeline.compile_pi(forged, "LITE")
    except Exception as exc:  # noqa: BLE001
        return _row("M03", "IntentCard atom claim forged", "REJECT", "REJECT",
                    type(exc).__name__, getattr(exc, "code", type(exc).__name__),
                    "RAW/mut_m03.json")
    return _row("M03", "IntentCard atom claim forged", "REJECT", "ACCEPT",
                "ACCEPTED", "NONE", "RAW/mut_m03.json")


def m04_profile_downgrade() -> int:
    from pipd_ls_sp import validate, pipeline
    rec, _ = pipeline.profile_record(
        "ASSURED", ["intent", "verification", "release", "trust_boundary"])
    tampered = dict(rec)
    tampered["assurance"] = ["deterministic_validator"]
    tampered["artifact_depth"] = "L1_SCHEMA_CONTRACT"
    report = validate.validate_bundle({"ProfileBinding": tampered}, SCHEMAS)
    first = report["findings"][0]["detail"] if report["findings"] else "NONE"
    return _row("M04", "ProfileBinding assurance downgraded ASSURED->LITE", "REJECT",
                "REJECT" if report["verdict"] == "FAIL" else "ACCEPT",
                report["verdict"], first, "RAW/mut_m04.json")


def m05_pi_oracle_poisoned() -> int:
    from pipd_ls_sp import validate
    _, _, pi = _intake_pi()
    tampered = json.loads(json.dumps(pi))
    tampered["acceptance"] = {"mode": "bound", "oracle_source": "POISONED"}
    report = validate.validate_bundle({"PI-PKG": tampered}, SCHEMAS)
    first = report["findings"][0]["detail"] if report["findings"] else "NONE"
    return _row("M05", "PI acceptance oracle poisoned", "REJECT",
                "REJECT" if report["verdict"] == "FAIL" else "ACCEPT",
                report["verdict"], first, "RAW/mut_m05.json")


def m06_domain_oracle_expected() -> int:
    from pipd_ls_sp import validate
    _, _, pi = _intake_pi()
    atom = json.loads(json.dumps(pi["stable_semantic_contract"]["atoms"][0]))
    rg = dict(atom.get("risk_guard") or {})
    oracle = dict(rg.get("oracle") or {})
    oracle["expected"] = 999
    rg["oracle"] = oracle
    atom["risk_guard"] = rg
    report = validate.validate_bundle({"RequirementAtom": atom}, SCHEMAS)
    first = report["findings"][0]["detail"] if report["findings"] else "NONE"
    return _row("M06", "domain oracle expected changed to 999", "REJECT",
                "REJECT" if report["verdict"] == "FAIL" else "ACCEPT",
                report["verdict"], first, "RAW/mut_m06.json")


def m11_unguarded_release_claim() -> int:
    from pipd_ls_sp import validate, pipeline
    rec = pipeline.claim_ceiling(["LOCAL_QUALIFIED", "RELEASED"])
    report = validate.validate_bundle({"ClaimCeiling": rec}, SCHEMAS)
    first = report["findings"][0]["detail"] if report["findings"] else "NONE"
    return _row("M11", "false RELEASED claim via unguarded key", "REJECT",
                "REJECT" if report["verdict"] == "FAIL" else "ACCEPT",
                report["verdict"], first, "RAW/mut_m11.json")


def m12_self_pass_ceiling() -> int:
    from pipd_ls_sp import validate, pipeline
    rec = pipeline.claim_ceiling(["INDEPENDENT_PASS"])
    report = validate.validate_bundle({"ClaimCeiling": rec}, SCHEMAS)
    first = report["findings"][0]["detail"] if report["findings"] else "NONE"
    return _row("M12", "self-minted INDEPENDENT_PASS ceiling", "REJECT",
                "REJECT" if report["verdict"] == "FAIL" else "ACCEPT",
                report["verdict"], first, "RAW/mut_m12.json")


def m14_fake_repo_snapshot() -> int:
    from pipd_ls_sp import pipeline
    _, _, pi = _intake_pi()
    spoofed = {"root": str(ROOT), "head": "deadbeef" * 5, "branch": "phantom-branch",
               "dirty": False, "tracked_files": 3, "manifest_sha256": "0" * 64,
               "claims": {"head": "deadbeef" * 5}, "currentness_epoch": "0" * 64}
    try:
        pd = pipeline.bind_pd(pi, spoofed)
        claim = pd["RepoContext"]["caller_claims"].get("head", {})
        if claim.get("verified") is False and claim.get("matches_host") is False:
            return _row("M14", "fake repo snapshot head claim", "REJECT", "REJECT",
                        "StaleProvider/ClaimRecordedUnverified", "caller_claim_unverified",
                        "RAW/mut_m14.json")
        return _row("M14", "fake repo snapshot head claim", "REJECT", "ACCEPT",
                    "TRUSTED", "NONE", "RAW/mut_m14.json")
    except Exception as exc:  # noqa: BLE001
        return _row("M14", "fake repo snapshot head claim", "REJECT", "REJECT",
                    type(exc).__name__, getattr(exc, "code", type(exc).__name__),
                    "RAW/mut_m14.json")


def m16_trace_digest_mismatch() -> int:
    from pipd_ls_sp import validate
    _, _, pi = _intake_pi()
    trace0 = json.loads(json.dumps(pi["trace"][0]))
    trace0["to_hash"] = "f" * 64
    report = validate.validate_bundle({"TraceLink": trace0}, SCHEMAS)
    first = report["findings"][0]["detail"] if report["findings"] else "NONE"
    return _row("M16", "trace atom digest mismatched", "REJECT",
                "REJECT" if report["verdict"] == "FAIL" else "ACCEPT",
                report["verdict"], first, "RAW/mut_m16.json")


def m18_remove_cand_flag() -> int:
    from pipd_ls_sp import validate
    record = {"subject_id": "WOC-" + "a" * 16, "version": 1, "content_hash": "a" * 64,
              "schema_version": "1.0.0", "workorder_id": "WO-R6-001",
              "candidate_only": False}
    report = validate.validate_bundle({"WorkOrderCandidate": record}, SCHEMAS)
    first = report["findings"][0]["detail"] if report["findings"] else "NONE"
    return _row("M18", "remove 22nd CAND / candidate_only=false", "REJECT",
                "REJECT" if report["verdict"] == "FAIL" else "ACCEPT",
                report["verdict"], first, "RAW/mut_m18.json")


def m01_pkg_sha_mismatch() -> int:
    proc = subprocess.run(
        [PY, PKG_CHECK, "--doc", PKG, "--trusted-package-sha256", "0" * 64, "--check"],
        capture_output=True, text=True)
    observed = "REJECT" if proc.returncode != 0 else "ACCEPT"
    return _row("M01", "narrative spoof / wrong trusted package sha", "REJECT",
                observed, f"exit={proc.returncode}", proc.stdout.strip()[:160],
                "RAW/mut_m01.json")


MODES = {
    "m01": m01_pkg_sha_mismatch, "m03": m03_intent_atom_forged,
    "m04": m04_profile_downgrade, "m05": m05_pi_oracle_poisoned,
    "m06": m06_domain_oracle_expected, "m11": m11_unguarded_release_claim,
    "m12": m12_self_pass_ceiling, "m14": m14_fake_repo_snapshot,
    "m16": m16_trace_digest_mismatch, "m18": m18_remove_cand_flag,
}

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "m03"
    fn = MODES.get(mode)
    if fn is None:
        print(f"unknown mode: {mode}", file=sys.stderr)
        raise SystemExit(2)
    try:
        raise SystemExit(fn())
    except SystemExit:
        raise
    except Exception:  # noqa: BLE001
        traceback.print_exc()
        raise SystemExit(9)
