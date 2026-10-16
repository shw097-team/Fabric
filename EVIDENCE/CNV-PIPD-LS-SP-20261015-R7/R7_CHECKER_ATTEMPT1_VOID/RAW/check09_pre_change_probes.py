"""Checker probe (R7): run M04/M06/M16 tamper cases against the PRE-CHANGE validator in the
R7_CHECKER/pre scratch tree. Expected if the blind-spot claim is true: all PASS (accepted) here.
"""
import json, sys
from pathlib import Path

sys.path.insert(0, r"C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R7/R7_CHECKER/pre/src")
from pipd_ls_sp import pipeline, validate  # noqa: E402
from pipd_ls_sp.util import canonical_json, sha256_text  # noqa: E402

SCHEMAS = Path(r"C:/Projects/Agent_Workspace/PIPD/schemas")
SRC = (r"C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/"
       "R6_DELIVERY/RAW/pipd_scratch_source.md")
IDENT = ("subject_id", "version", "content_hash", "schema_version", "trace", "_profile_meta")


def reseal(rec):
    body = {k: v for k, v in rec.items() if k not in IDENT}
    rec["content_hash"] = sha256_text(canonical_json(body))
    return rec


def first(report):
    return report["findings"][0]["detail"] if report["findings"] else "NONE"


def main():
    card = pipeline.intake("bind the R7 scratch requirements", sources=[SRC])
    pi = pipeline.compile_pi(card, "LITE")

    # M16: tamper body hash field, pre-change has no digest bound for TraceLink.
    t = json.loads(json.dumps(pi["trace"][0]))
    t["to_hash"] = "f" * 64
    rep = validate.validate_bundle({"TraceLink": t}, SCHEMAS)
    print("M16 pre-change verdict:", rep["verdict"], "| first_fail:", first(rep))

    # M06: poison oracle.expected, pre-change has no digest bound for RequirementAtom.
    a = json.loads(json.dumps(pipeline.atoms_of(pi)[0]))
    a["risk_guard"]["oracle"]["expected"] = 999
    rep = validate.validate_bundle({"RequirementAtom": a}, SCHEMAS)
    print("M06 pre-change verdict:", rep["verdict"], "| first_fail:", first(rep))

    # M04: downgrade assurance while keeping ASSURED profile name,
    # pre-change has no digest/assurance check for ProfileBinding.
    rec, _ = pipeline.profile_record(
        "ASSURED", ["intent", "verification", "release", "trust_boundary"])
    d = json.loads(json.dumps(rec))
    d["assurance"] = ["deterministic_validator"]
    d["artifact_depth"] = "L1_SCHEMA_CONTRACT"
    rep = validate.validate_bundle({"ProfileBinding": d}, SCHEMAS)
    print("M04 pre-change verdict:", rep["verdict"], "| first_fail:", first(rep))

    # fail-closed: unknown profile (no frozen requirement) pre-change.
    u = json.loads(json.dumps(rec)); u["profile"] = "MYSTERY"
    rep = validate.validate_bundle({"ProfileBinding": u}, SCHEMAS)
    print("PROFILE-unknown pre-change verdict:", rep["verdict"], "| first_fail:", first(rep))

    # positive: untouched records from this same PI must still pass pre-change.
    rep = validate.validate_bundle(
        {"PI-PKG": json.loads(json.dumps(pi)), "TraceLink": pi["trace"][0],
         "RequirementAtom": pipeline.atoms_of(pi)[0], "ProfileBinding": rec}, SCHEMAS)
    print("POSITIVE pre-change verdict:", rep["verdict"], "| first_fail:", first(rep))


if __name__ == "__main__":
    main()
