"""Probe the STRONGER attacker who re-issues identity after tampering.

If a mutation recomputes content_hash over its edited body, the self-digest rule no longer fires;
only the frozen-reference binding (trace endpoint / oracle expectation / profile requirement) can
catch it. These cases prove those bindings are load-bearing, not redundant with the body hash.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, "C:/Projects/Agent_Workspace/PIPD/src")
from pipd_ls_sp import pipeline, validate  # noqa: E402
from pipd_ls_sp.util import canonical_json, sha256_text  # noqa: E402

SCHEMAS = Path("C:/Projects/Agent_Workspace/PIPD/schemas")
SRC = ("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/"
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
    ctx = pipeline.frozen_validation_context(pi)

    # M16-strong: tamper to_hash AND re-issue identity -> body hash passes.
    t = reseal(json.loads(json.dumps(pi["trace"][0])))
    t["to_hash"] = "f" * 64
    reseal(t)
    rep = validate.validate_bundle({"TraceLink": t}, SCHEMAS, ctx)
    print("M16-strong (resealed, with frozen ctx) verdict:", rep["verdict"], "| first_fail:", first(rep))
    rep = validate.validate_bundle({"TraceLink": t}, SCHEMAS)
    print("M16-strong (resealed, no frozen ctx) verdict:", rep["verdict"], "| first_fail:", first(rep))

    # M06-strong: poison oracle.expected AND re-issue identity.
    a = json.loads(json.dumps(pipeline.atoms_of(pi)[0]))
    a["risk_guard"]["oracle"]["expected"] = 999
    reseal(a)
    rep = validate.validate_bundle({"RequirementAtom": a}, SCHEMAS, ctx)
    print("M06-strong (resealed, with frozen ctx) verdict:", rep["verdict"], "| first_fail:", first(rep))
    rep = validate.validate_bundle({"RequirementAtom": a}, SCHEMAS)
    print("M06-strong (resealed, no frozen ctx) verdict:", rep["verdict"], "| first_fail:", first(rep))

    # M04-strong: downgrade assurance but KEEP the ASSURED profile name, re-issue identity.
    rec, _ = pipeline.profile_record("ASSURED", ["intent", "verification", "release", "trust_boundary"])
    d = json.loads(json.dumps(rec))
    d["assurance"] = ["deterministic_validator"]
    d["artifact_depth"] = "L1_SCHEMA_CONTRACT"
    reseal(d)
    rep = validate.validate_bundle({"ProfileBinding": d}, SCHEMAS, ctx)
    print("M04-strong (resealed, with frozen ctx) verdict:", rep["verdict"], "| first_fail:", first(rep))
    rep = validate.validate_bundle({"ProfileBinding": d}, SCHEMAS)
    print("M04-strong (resealed, no frozen ctx) verdict:", rep["verdict"], "| first_fail:", first(rep))

    # unknown profile, resealed -> must fail closed UNBOUND_FROZEN_CONTEXT (no silent pass)
    u = json.loads(json.dumps(rec)); u["profile"] = "MYSTERY"; reseal(u)
    rep = validate.validate_bundle({"ProfileBinding": u}, SCHEMAS)
    print("PROFILE-unknown (resealed) verdict:", rep["verdict"], "| first_fail:", first(rep))


if __name__ == "__main__":
    main()
