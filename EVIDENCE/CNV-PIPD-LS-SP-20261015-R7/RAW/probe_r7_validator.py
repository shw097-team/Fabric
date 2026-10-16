"""Direct probe of the R7-0 validator hardening (three blind spots + fail-closed + positives)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, "C:/Projects/Agent_Workspace/PIPD/src")
from pipd_ls_sp import pipeline, validate  # noqa: E402

SCHEMAS = Path("C:/Projects/Agent_Workspace/PIPD/schemas")
SRC = ("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/"
       "R6_DELIVERY/RAW/pipd_scratch_source.md")


def first(report):
    return report["findings"][0]["detail"] if report["findings"] else "NONE"


def main():
    card = pipeline.intake("bind the R7 scratch requirements", sources=[SRC])
    pi = pipeline.compile_pi(card, "LITE")

    # --- positive: the untampered PI package must PASS with the derived frozen context
    ctx = pipeline.frozen_validation_context(pi)
    pos = pipeline.validate_pi(pi, SCHEMAS)
    print("POSITIVE validate_pi verdict:", pos["verdict"], "checked:", pos["checked"],
          "findings:", len(pos["findings"]))

    # --- M16: tamper the TraceLink to_hash, validate ONLY the TraceLink (as the driver does)
    trace0 = json.loads(json.dumps(pi["trace"][0]))
    trace0["to_hash"] = "f" * 64
    rep = validate.validate_bundle({"TraceLink": trace0}, SCHEMAS, ctx)
    print("M16 (with frozen ctx) verdict:", rep["verdict"], "| first_fail:", first(rep))

    # --- M16 fail-closed: same tamper, but NO frozen context
    rep = validate.validate_bundle({"TraceLink": trace0}, SCHEMAS)
    print("M16 (no frozen ctx) verdict:", rep["verdict"], "| first_fail:", first(rep))

    # --- M16 positive: untampered TraceLink with frozen ctx must PASS
    rep = validate.validate_bundle({"TraceLink": json.loads(json.dumps(pi["trace"][0]))}, SCHEMAS, ctx)
    print("M16 positive verdict:", rep["verdict"], "| first_fail:", first(rep))

    # --- M06: poison oracle.expected to 999
    atom = json.loads(json.dumps(pipeline.atoms_of(pi)[0]))
    rg = dict(atom.get("risk_guard") or {})
    oracle = dict(rg.get("oracle") or {})
    oracle["expected"] = 999
    rg["oracle"] = oracle
    atom["risk_guard"] = rg
    rep = validate.validate_bundle({"RequirementAtom": atom}, SCHEMAS, ctx)
    print("M06 (with frozen ctx) verdict:", rep["verdict"], "| first_fail:", first(rep))
    rep = validate.validate_bundle({"RequirementAtom": atom}, SCHEMAS)
    print("M06 (no frozen ctx) verdict:", rep["verdict"], "| first_fail:", first(rep))
    rep = validate.validate_bundle({"RequirementAtom": json.loads(json.dumps(pipeline.atoms_of(pi)[0]))},
                                   SCHEMAS, ctx)
    print("M06 positive verdict:", rep["verdict"], "| first_fail:", first(rep))

    # --- M04: downgrade assurance ASSURED -> LITE
    rec, _ = pipeline.profile_record("ASSURED", ["intent", "verification", "release", "trust_boundary"])
    tampered = dict(rec)
    tampered["assurance"] = ["deterministic_validator"]
    tampered["artifact_depth"] = "L1_SCHEMA_CONTRACT"
    rep = validate.validate_bundle({"ProfileBinding": tampered}, SCHEMAS, ctx)
    print("M04 (with frozen ctx) verdict:", rep["verdict"], "| first_fail:", first(rep))
    rep = validate.validate_bundle({"ProfileBinding": tampered}, SCHEMAS)
    print("M04 (no frozen ctx) verdict:", rep["verdict"], "| first_fail:", first(rep))
    rep = validate.validate_bundle({"ProfileBinding": rec}, SCHEMAS, ctx)
    print("M04 positive (ASSURED intact) verdict:", rep["verdict"], "| first_fail:", first(rep))

    # --- unknown profile must WRITE-FAIL-CLOSED, not pass
    rogue = dict(rec); rogue["profile"] = "MYSTERY"
    rep = validate.validate_bundle({"ProfileBinding": rogue}, SCHEMAS)
    print("PROFILE-unknown fail-closed verdict:", rep["verdict"], "| first_fail:", first(rep))


if __name__ == "__main__":
    main()
