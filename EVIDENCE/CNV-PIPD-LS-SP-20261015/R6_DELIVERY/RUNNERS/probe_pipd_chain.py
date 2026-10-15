"""Same-subject probes for the PIPD-EC 13-command chain (ACC-016..ACC-022).

Exercises the REAL bound functions in C:/Projects/Agent_Workspace/PIPD/src/pipd_ls_sp.
Every probe is issued as its own process so probe_lib.capture records the real exit
code and stdout/stderr verbatim. All scratch writes land under RAW/pipd_scratch/.

Modes:
  intake           positive: intake over a clean RAW source file -> clause-bound atoms
  intake-missing   negative: source locator that does not exist -> AuthorityUnknown
  intake-ambiguous negative: compound clause with ambiguous cardinality -> IntakeInvalid
  profile          positive: profile_record computes LITE axes
  compile-pi       positive: compile_pi over the intake card -> atom set + trace
  compile-pi-tamper negative: tamper an atom -> PiSemanticFail
  bind-pd-nocxt    negative: bind_pd with no RepoContext -> RepoContextMissing
  bind-pd          positive: bind_pd against the R6_DELIVERY repo root
  ecp              positive: compile_ecp over the PD
  tqaep-self       negative: maker==checker -> TqSodFail
  tqaep-noreceipt  negative: empty checker receipt -> TqSodFail
  tqaep            positive: distinct maker/checker + receipt -> TQAEP with NOT_GRANTED
  claim-ceiling    positive: claim_ceiling(["LOCAL"])
  project-unsafe   negative: `project --out <outside>` without --allow-root -> refusal
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

PIPD_SRC = "C:/Projects/Agent_Workspace/PIPD/src"
sys.path.insert(0, PIPD_SRC)

ROOT = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/R6_DELIVERY")
SCRATCH = ROOT / "RAW" / "pipd_scratch"
SRC = ROOT / "RAW" / "pipd_scratch_source.md"
SRC_AMBIG = ROOT / "RAW" / "pipd_scratch_ambiguous.md"


def _emit(obj: dict) -> int:
    print(json.dumps(obj, ensure_ascii=False, indent=1, default=str))
    return 0 if obj.get("verdict") != "FAIL" else 1


def _fail(tag: str, exc: Exception) -> int:
    return _emit({"verdict": "FAIL", "probe": tag, "error_type": type(exc).__name__,
                  "error_code": getattr(exc, "code", None), "error": str(exc)})


def _write_scratch_sources() -> None:
    SRC.write_text(
        "# R6 PIPD scratch clause source\n"
        "The intake must bind every normative claim to a source locator.\n"
        "The compiler must refuse a normative claim without a source locator.\n"
        "The pipeline must emit a typed refusal instead of an untyped traceback.\n",
        encoding="utf-8")
    SRC_AMBIG.write_text(
        "甲、乙、丙分別對應一、二。\n",
        encoding="utf-8")


def intake() -> int:
    from pipd_ls_sp import pipeline
    _write_scratch_sources()
    card = pipeline.intake("bind the R6 scratch requirements to real source clauses",
                           sources=[str(SRC)],
                           constraints=["LOCAL_CEILING"], non_goals=["production"])
    return _emit({"verdict": "PIPD_INTAKE_OK", "subject_id": card["subject_id"],
                  "schema_version": card["schema_version"],
                  "atom_count": len(card["atoms"]),
                  "first_atom_req_id": card["atoms"][0]["req_id"],
                  "first_atom_acceptance_cue": card["atoms"][0]["acceptance_cue"]})


def intake_missing() -> int:
    from pipd_ls_sp import pipeline
    try:
        pipeline.intake("missing source", sources=[str(SCRATCH / "does_not_exist.md")])
    except Exception as exc:  # noqa: BLE001
        return _emit({"verdict": "PIPD_INTAKE_MISSING_SOURCE_REFUSED",
                      "error_type": type(exc).__name__,
                      "error_code": getattr(exc, "code", None), "error": str(exc)})
    return _emit({"verdict": "FAIL", "probe": "intake-missing",
                  "detail": "missing source was accepted"})


def intake_ambiguous() -> int:
    from pipd_ls_sp import pipeline
    _write_scratch_sources()
    try:
        pipeline.intake("ambiguous compound", sources=[str(SRC_AMBIG)])
    except Exception as exc:  # noqa: BLE001
        return _emit({"verdict": "PIPD_INTAKE_AMBIGUOUS_REFUSED",
                      "error_type": type(exc).__name__,
                      "error_code": getattr(exc, "code", None), "error": str(exc)})
    return _emit({"verdict": "FAIL", "probe": "intake-ambiguous",
                  "detail": "ambiguous compound was accepted"})


def _card() -> dict:
    from pipd_ls_sp import pipeline
    _write_scratch_sources()
    return pipeline.intake("bind the R6 scratch requirements to real source clauses",
                           sources=[str(SRC)], constraints=["LOCAL_CEILING"])


def profile() -> int:
    from pipd_ls_sp import pipeline
    rec, full = pipeline.profile_record("LITE", ["intent", "security"])
    return _emit({"verdict": "PIPD_PROFILE_OK", "subject_id": rec["subject_id"],
                  "profile": full["profile"], "assurance": full["assurance"],
                  "artifact_depth": full["artifact_depth"], "vetoes": full["vetoes"]})


def profile_ok() -> int:
    from pipd_ls_sp import pipeline
    rec, full = pipeline.profile_record("LITE", ["intent", "verification"])
    return _emit({"verdict": "PIPD_PROFILE_OK", "subject_id": rec["subject_id"],
                  "profile": full["profile"], "assurance": full["assurance"],
                  "artifact_depth": full["artifact_depth"], "vetoes": full["vetoes"]})


def compile_pi() -> int:
    from pipd_ls_sp import pipeline
    pi = pipeline.compile_pi(_card(), "LITE")
    return _emit({"verdict": "PIPD_COMPILE_PI_OK", "subject_id": pi["subject_id"],
                  "content_hash": pi["content_hash"],
                  "atom_count": len(pipeline.atoms_of(pi)),
                  "trace_count": len(pi.get("trace") or []),
                  "oracle_source": pi["acceptance"]["oracle_source"]})


def compile_pi_tamper() -> int:
    from pipd_ls_sp import pipeline
    card = _card()
    # A clause-bound claim that diverges from the re-derived atom set must be refused.
    tampered = [dict(a) for a in card["atoms"]]
    tampered[0] = dict(tampered[0])
    tampered[0]["acceptance_cue"] = "MUST: forged acceptance oracle"
    card = dict(card)
    card["atoms"] = tampered
    try:
        pipeline.compile_pi(card, "LITE")
    except Exception as exc:  # noqa: BLE001
        return _emit({"verdict": "PIPD_COMPILE_PI_TAMPER_REFUSED",
                      "error_type": type(exc).__name__,
                      "error_code": getattr(exc, "code", None), "error": str(exc)})
    return _emit({"verdict": "FAIL", "probe": "compile-pi-tamper",
                  "detail": "tampered atom claim was accepted"})


def _pi() -> dict:
    from pipd_ls_sp import pipeline
    return pipeline.compile_pi(_card(), "LITE")


def bind_pd_nocxt() -> int:
    from pipd_ls_sp import pipeline
    try:
        pipeline.bind_pd(_pi(), None)
    except Exception as exc:  # noqa: BLE001
        return _emit({"verdict": "PIPD_BIND_PD_NO_CONTEXT_REFUSED",
                      "error_type": type(exc).__name__,
                      "error_code": getattr(exc, "code", None), "error": str(exc)})
    return _emit({"verdict": "FAIL", "probe": "bind-pd-nocxt",
                  "detail": "bind_pd without a RepoContext was accepted"})


def bind_pd() -> int:
    from pipd_ls_sp import pipeline
    ctx = pipeline.repo_probe.derive_repo_context(str(ROOT), writable_scope="src/**")
    pd = pipeline.bind_pd(_pi(), ctx)
    return _emit({"verdict": "PIPD_BIND_PD_OK", "subject_id": pd["subject_id"],
                  "repo_probe": pd["RepoContext"]["probe"],
                  "degraded": pd["RepoContext"]["degraded"],
                  "head": pd["RepoContext"]["head"],
                  "readiness": pd["RepoContext"]["readiness"],
                  "currentness_state": pd["currentness"]["state"],
                  "writable_scope": pd["late_bound_construction_binding"]["writable_scope"]})


def _pd() -> dict:
    from pipd_ls_sp import pipeline
    ctx = pipeline.repo_probe.derive_repo_context(str(ROOT), writable_scope="src/**")
    return pipeline.bind_pd(_pi(), ctx)


def ecp() -> int:
    from pipd_ls_sp import pipeline
    e = pipeline.compile_ecp(_pd(), _pi())
    return _emit({"verdict": "PIPD_COMPILE_ECP_OK", "subject_id": e["subject_id"],
                  "permission": e["permission"], "idempotency": e["idempotency"],
                  "readback": e["readback"], "rollback": e["rollback"]})


def _ecp() -> dict:
    from pipd_ls_sp import pipeline
    return pipeline.compile_ecp(_pd(), _pi())


def tqaep_self() -> int:
    from pipd_ls_sp import pipeline
    try:
        pipeline.compile_tqaep(_pi(), _ecp(), maker="R6-WRITER", checker="r6-writer",
                               checker_execution_receipt="RAW/receipt")
    except Exception as exc:  # noqa: BLE001
        return _emit({"verdict": "PIPD_TQAEP_SELF_REFUSED",
                      "error_type": type(exc).__name__,
                      "error_code": getattr(exc, "code", None), "error": str(exc)})
    return _emit({"verdict": "FAIL", "probe": "tqaep-self",
                  "detail": "maker==checker aliasing was accepted"})


def tqaep_noreceipt() -> int:
    from pipd_ls_sp import pipeline
    try:
        pipeline.compile_tqaep(_pi(), _ecp(), maker="R6-WRITER",
                               checker="opencode-go/glm-5.3-flash",
                               checker_execution_receipt="")
    except Exception as exc:  # noqa: BLE001
        return _emit({"verdict": "PIPD_TQAEP_NORECEIPT_REFUSED",
                      "error_type": type(exc).__name__,
                      "error_code": getattr(exc, "code", None), "error": str(exc)})
    return _emit({"verdict": "FAIL", "probe": "tqaep-noreceipt",
                  "detail": "empty checker receipt was accepted"})


def tqaep() -> int:
    from pipd_ls_sp import pipeline
    t = pipeline.compile_tqaep(_pi(), _ecp(), maker="R6-WRITER",
                               checker="opencode-go/glm-5.3-flash",
                               checker_execution_receipt="RAW/cap16_tqaep_checker.txt")
    acc = t["acceptance"][0]
    return _emit({"verdict": "PIPD_COMPILE_TQAEP_OK", "subject_id": t["subject_id"],
                  "test_count": len(t["tests"]),
                  "distinct": acc["distinct"],
                  "claim_ceiling": acc["claim_ceiling"],
                  "independent_acceptance": acc["independent_acceptance"],
                  "case": acc["case"]})


def claim_ceiling() -> int:
    from pipd_ls_sp import pipeline
    c = pipeline.claim_ceiling(["LOCAL"])
    return _emit({"verdict": "PIPD_CLAIM_CEILING_OK", "subject_id": c["subject_id"],
                  "allowed_claims": c["allowed_claims"],
                  "forbidden_escalation": c["forbidden_escalation"]})


def claim_ladder_ok() -> int:
    from pipd_ls_sp import pipeline
    c = pipeline.claim_ceiling(["LOCAL_QUALIFIED"])
    return _emit({"verdict": "PIPD_CLAIM_CEILING_OK", "subject_id": c["subject_id"],
                  "allowed_claims": c["allowed_claims"],
                  "forbidden_escalation": c["forbidden_escalation"]})


def intake_pkg() -> int:
    from pipd_ls_sp import pipeline
    pkg = ("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/"
           "Local/hermes/attachments/Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md")
    try:
        card = pipeline.intake("converge PIPD-LS-SP under HG-KSEOS", sources=[pkg])
    except Exception as exc:  # noqa: BLE001
        return _emit({"verdict": "PIPD_INTAKE_PKG_REFUSED",
                      "error_type": type(exc).__name__,
                      "error_code": getattr(exc, "code", None), "error": str(exc)[:400]})
    return _emit({"verdict": "PIPD_INTAKE_PKG_ACCEPTED", "atom_count": len(card["atoms"])})


def project_unsafe() -> int:
    from pipd_ls_sp import cli
    outside = "C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/R6_UNSAFE_OUT"
    code = cli.main(["--root", str(ROOT), "project", "--out", outside])
    print(json.dumps({"verdict": "PIPD_PROJECT_UNSAFE_EXIT", "exit_code": code},
                     ensure_ascii=False))
    return code


MODES = {
    "intake": intake, "intake-missing": intake_missing, "intake-ambiguous": intake_ambiguous,
    "intake-pkg": intake_pkg,
    "profile": profile, "profile-ok": profile_ok,
    "compile-pi": compile_pi, "compile-pi-tamper": compile_pi_tamper,
    "bind-pd-nocxt": bind_pd_nocxt, "bind-pd": bind_pd, "ecp": ecp,
    "tqaep-self": tqaep_self, "tqaep-noreceipt": tqaep_noreceipt, "tqaep": tqaep,
    "claim-ceiling": claim_ceiling, "claim-ladder-ok": claim_ladder_ok,
    "project-unsafe": project_unsafe,
}

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "intake"
    fn = MODES.get(mode)
    if fn is None:
        print(f"unknown mode: {mode}", file=sys.stderr)
        raise SystemExit(2)
    try:
        raise SystemExit(fn())
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"verdict": "FAIL", "probe": mode,
                          "error_type": type(exc).__name__, "error": str(exc)},
                         ensure_ascii=False, indent=1))
        raise SystemExit(9)
