"""Deterministic validation: schema + semantic invariants over the 19 families.

Deterministic only: no LLM judge is consulted here (總藍圖 §5.9.1 responsibility split).
"""
from __future__ import annotations

from pathlib import Path
import re
from typing import Any

from . import registry
from .errors import ValidationFail

CLAIM_LADDER = ["PROMPT_COMPILE_PASS", "HGK_ADMITTED", "RUNTIME_READY", "LOCAL_QUALIFIED",
                "INDEPENDENT_PASS", "PUBLICATION_APPROVED", "RELEASED", "PRODUCTION_VERIFIED"]
RELEASE_BOUND = ("PI-PKG", "PD-PKG", "ECP", "TQAEP", "ConstructionContract")
# R7-0 hardening (EIA-R6-04 / M16). The self-describing digest rule that the release-bound
# families already enforce is extended to the identity-bearing sub-records whose body carries a
# reference an attacker can swap without re-issuing identity: a RequirementAtom (`risk_guard`),
# a ProfileBinding (`assurance`/`artifact_depth`) and a TraceLink (`to_hash`/`from_hash`). A body
# edited without re-issuing identity (e.g. a TraceLink `to_hash` replaced by 64 f's) is refused.
DIGEST_BOUND = RELEASE_BOUND + ("RequirementAtom", "ProfileBinding", "TraceLink")
# The clause polarity -> oracle expected value is a FROZEN rule of the requirement compiler
# (requirements.compile_requirements): a MUST clause expects the obligation to be `required`, a
# MUST NOT clause expects it to be `forbidden`. Binding `oracle.expected` to it means an oracle
# whose declared expectation contradicts its own clause polarity is a mismatch.
POLARITY_EXPECTED = {"MUST": "required", "MUST NOT": "forbidden"}


def _validator(schema: dict[str, Any]):
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:  # pragma: no cover
        raise ValidationFail(f"jsonschema unavailable: {exc}") from exc
    return Draft202012Validator(schema)


def validate_record(contract: str, record: dict[str, Any], schemas_dir: Path | None = None) -> list[str]:
    """Return a list of deterministic findings; empty list == schema-valid."""
    schema = registry.load_schema(contract, schemas_dir)
    v = _validator(schema)
    findings = []
    for err in sorted(v.iter_errors(record), key=lambda e: list(e.absolute_path)):
        pointer = "/" + "/".join(str(x) for x in err.absolute_path)
        findings.append(f"{contract}{pointer}: {err.message}")
    return findings


HEX64 = re.compile(r"^[0-9a-f]{64}$")


def _body_hash(record: dict[str, Any]) -> str:
    """Recompute the record digest over everything EXCEPT the identity fields.

    Lets the validator catch a record whose body was edited without re-issuing its hash.
    """
    import hashlib
    import json
    body = {k: v for k, v in record.items() if k not in ("subject_id", "version", "content_hash", "schema_version", "trace", "_profile_meta")}
    return hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode()).hexdigest()


def semantic_invariants(contract: str, record: dict[str, Any],
                        frozen_context: dict[str, Any] | None = None) -> list[str]:
    """Semantic invariants that a JSON Schema cannot express.

    ``frozen_context`` is an OPTIONAL, caller-supplied, deterministic read-only map of the frozen
    references a record must be bound to (profile requirements, oracle expectations, trace
    endpoint digests). It is never an LLM/network dependency: every value is data the caller already
    holds. ``None`` means "not available": a contract whose binding REQUIRES frozen context then
    fails closed with an explicit ``UNBOUND_FROZEN_CONTEXT`` finding instead of silently passing.
    The argument is purely additive - with ``frozen_context=None`` every check that does not require
    frozen context behaves exactly as before.
    """
    out: list[str] = []
    fc = frozen_context or {}
    ident = ("subject_id", "version", "content_hash", "schema_version")
    for field in ident:
        if field not in record:
            out.append(f"{contract}: missing universal identity field {field}")
    # C-5/C-6 repair: presence is not enough. An adversarial lane proved that null identities, a
    # non-hash content_hash and a tampered body all passed the previous presence-only check.
    for field in ident:
        if field in record and not str(record.get(field) or "").strip():
            out.append(f"{contract}: identity field {field} must be a non-empty string")
    ch = str(record.get("content_hash") or "")
    if ch and not HEX64.match(ch):
        out.append(f"{contract}: content_hash must be a 64-char lowercase sha256 hex digest")
    sid = str(record.get("subject_id") or "")
    if sid and len(sid) < 8:
        out.append(f"{contract}: subject_id is implausibly short to be a content id")
    if record.get("recomputed_body_hash_required") is True:
        pass  # explicit opt-out is itself rejected below for release-bound families
    if contract in DIGEST_BOUND and ch and len(record) > 4:
        # R7-0 (M16/M06/M04): the record must remain self-consistent - a body edited in place
        # without re-issuing identity (a swapped `to_hash`, a poisoned `oracle.expected`, a
        # downgraded `assurance`) is refused here. This generalizes the release-bound rule to the
        # identity-bearing sub-records; it strengthens, never weakens, the existing predicate.
        if ch != _body_hash(record):
            out.append(f"{contract}: content_hash does not match the record body "
                       "(body edited without re-issuing identity)")
    sv = str(record.get("schema_version") or "")
    if sv and not (re.match(r"^[0-9]+\.[0-9]+\.[0-9]+$", sv) or re.match(r"^[A-Za-z0-9_.-]+@[0-9]+$", sv)):
        out.append(f"{contract}: schema_version must be semver or <Token>@<n>")
    if contract == "ClaimCeiling":
        allowed = set(record.get("allowed_claims", []))
        forbidden = set(record.get("forbidden_escalation", []))
        if allowed & forbidden:
            out.append("ClaimCeiling: a claim cannot be both allowed and forbidden")
        # C-8 repair: a maker could previously mint claim_ceiling(['INDEPENDENT_PASS']).
        receipts = record.get("receipts") or record.get("approval_receipt")
        authority = record.get("authority") or record.get("checker_identity")
        above = [c for c in allowed
                 if CLAIM_LADDER.index(c) > CLAIM_LADDER.index("LOCAL_QUALIFIED")]
        if above and not (receipts and authority):
            out.append("ClaimCeiling: claims above LOCAL_QUALIFIED require a bound approval "
                       "receipt AND a checker identity; a maker cannot mint them unilaterally")
    if contract == "TQAEP":
        # C-3 repair. The S0 TQAEP schema declares a fixed field set (additionalProperties=false),
        # so SoD evidence is carried INSIDE the declared `acceptance` field rather than by inventing
        # a 20th family or new top-level keys. An unsigned string comparison is not SoD.
        acc = record.get("acceptance")
        entries = [a for a in acc if isinstance(a, dict)] if isinstance(acc, list) else []
        if not entries:
            out.append("TQAEP: acceptance must carry a structured separation-of-duties entry "
                       "(maker/checker never compared or persisted = unproven independence)")
        for e in entries:
            maker, checker = e.get("maker_identity"), e.get("checker_identity")
            if not (maker and checker):
                out.append("TQAEP: acceptance entry missing maker_identity/checker_identity")
            elif maker == checker or e.get("distinct") is not True:
                out.append("TQAEP: maker and checker must be distinct with distinct=true")
            elif str(e.get("checker_execution_receipt") or "") in ("", "SELF_ATTESTED", "self", "same-process"):
                out.append("TQAEP: acceptance entry needs a checker_execution_receipt that is not "
                           "self-attested (maker cannot attest its own independence)")
    if contract == "WorkOrderCandidate":
        if record.get("candidate_only") is not True:
            out.append("WorkOrderCandidate: candidate_only must be fixed true (never runtime authority)")
    if contract == "GENIEProjectionRef":
        refs = record.get("target_refs")
        want = ("ProductGraph", "Profile", "Bundle", "GENIEArtifact")
        if not isinstance(refs, (list, dict)) or not all(
                any(w in str(x) for x in (refs if isinstance(refs, list) else refs.keys())) for w in want):
            out.append("GENIEProjectionRef: target_refs must cover ProductGraph/Profile/Bundle/GENIEArtifact")
    if contract == "ExecutionBindingRef" and str(record.get("state", "")).upper() == "ACKED":
        if not (record.get("receiver_binding_id") and record.get("receiver_binding_hash")):
            out.append("ExecutionBindingRef: ACK requires a real HGK receiver binding id+hash")
    if contract == "TraceLink":
        for side in ("from", "to"):
            if not (record.get(f"{side}_type") and record.get(f"{side}_id")):
                out.append(f"TraceLink: {side} endpoint incomplete")
        # R7-0 (M16): a trace link must bind each endpoint to the FROZEN digest of the atom it
        # points at. A link whose `to_hash` was swapped (e.g. 64 f's) keeps its own content_hash
        # intact, so the self-digest check above cannot see it - the reference must be resolved
        # against the frozen subject->digest map. When that map is absent the binding cannot be
        # discharged, so the validator fails closed rather than passing an unverifiable reference.
        fc_endpoints = fc.get("trace_endpoint_hashes")
        for side in ("from", "to"):
            ref_id = record.get(f"{side}_id")
            recorded = str(record.get(f"{side}_hash") or "")
            if recorded and not HEX64.match(recorded):
                out.append(f"TraceLink: {side}_hash must be a 64-char lowercase sha256 hex digest")
            if fc_endpoints is None:
                if ref_id and recorded:
                    out.append("TraceLink: UNBOUND_FROZEN_CONTEXT: "
                               f"{side}_hash cannot be verified against a frozen subject->digest "
                               "map (frozen context not supplied); binding is unproven, not a pass")
                continue
            want = fc_endpoints.get(ref_id)
            if want is None:
                out.append(f"TraceLink: {side}_id {ref_id!r} is not present in the frozen "
                           "context (endpoint has no frozen digest to bind to)")
            elif recorded != want:
                out.append(f"TraceLink: {side}_hash does not match the frozen digest of "
                           f"{ref_id!r} (recorded {recorded[:12]}, frozen {str(want)[:12]})")
    if contract == "RequirementAtom":
        # R7-0 (M06): the oracle's `expected` value is not a free-standing number - it is DERIVED
        # from the clause polarity (MUST -> required, MUST NOT -> forbidden). A value that
        # contradicts the atom's own polarity (e.g. 999) is refused. When the frozen oracle
        # expectation for this atom is available it must match too, so the value is bound to the
        # frozen acceptance source rather than merely being present.
        rg = record.get("risk_guard")
        rg = rg if isinstance(rg, dict) else {}
        oracle = rg.get("oracle")
        oracle = oracle if isinstance(oracle, dict) else {}
        expected = oracle.get("expected")
        polarity = rg.get("polarity")
        derived = POLARITY_EXPECTED.get(polarity)
        if polarity is not None and polarity not in POLARITY_EXPECTED:
            out.append(f"RequirementAtom: risk_guard.polarity must be MUST or MUST NOT, got {polarity!r}")
        elif derived is not None and expected != derived:
            out.append(f"RequirementAtom: oracle.expected {expected!r} contradicts clause polarity "
                       f"{polarity!r} (must be {derived!r})")
        fc_oracle = fc.get("oracle_expected")
        if fc_oracle is not None:
            bound = fc_oracle.get(record.get("req_id"))
            if bound is not None and expected != bound:
                out.append(f"RequirementAtom: oracle.expected {expected!r} does not match the frozen "
                           f"acceptance expectation {bound!r} for {record.get('req_id')!r}")
    if contract == "ProfileBinding":
        # R7-0 (M04): a ProfileBinding must not assert an assurance/artifact_depth weaker than the
        # FROZEN requirement for its profile. ASSURED->LITE is a downgrade that a maker cannot
        # self-authorize. The frozen requirement is authoritative; if it is not available the
        # validator FAILS CLOSED with UNBOUND_FROZEN_CONTEXT instead of silently passing - a missing
        # binding is not a pass.
        from .profiles import PROFILES
        profile = str(record.get("profile") or "")
        req = PROFILES.get(profile)
        assurance = record.get("assurance")
        depth = record.get("artifact_depth")
        if req is None:
            out.append(f"ProfileBinding: UNBOUND_FROZEN_CONTEXT: profile {profile!r} has no frozen "
                       "requirement (unknown profile); assurance cannot be verified, not a pass")
        else:
            required_assurance = req["assurance"]
            missing = [a for a in required_assurance
                       if not (isinstance(assurance, list) and a in assurance)]
            if missing:
                out.append(f"ProfileBinding: assurance {assurance!r} is weaker than the frozen "
                           f"requirement for {profile} (missing {missing})")
            if depth != req["artifact_depth"]:
                out.append(f"ProfileBinding: artifact_depth {depth!r} is weaker than the frozen "
                           f"requirement {req['artifact_depth']!r} for {profile}")
        fc_profile = fc.get("profile_requirement")
        if fc_profile is not None:
            bound = fc_profile.get(profile)
            if bound is None:
                out.append(f"ProfileBinding: UNBOUND_FROZEN_CONTEXT: profile {profile!r} absent "
                           "from the supplied frozen profile requirement")
            else:
                b_assurance = bound.get("assurance") or []
                b_missing = [a for a in b_assurance
                             if not (isinstance(assurance, list) and a in assurance)]
                if b_missing:
                    out.append(f"ProfileBinding: assurance {assurance!r} is weaker than the supplied "
                               f"frozen requirement for {profile} (missing {b_missing})")
                if bound.get("artifact_depth") and depth != bound["artifact_depth"]:
                    out.append(f"ProfileBinding: artifact_depth {depth!r} does not match the supplied "
                               f"frozen requirement {bound['artifact_depth']!r} for {profile}")
    return out


def validate_bundle(bundle: dict[str, dict[str, Any]], schemas_dir: Path | None = None,
                    frozen_context: dict[str, Any] | None = None) -> dict[str, Any]:
    findings: list[dict[str, str]] = []
    # C-4 repair: validate_bundle({}) used to return PASS with checked=0. An empty denominator is
    # not a verification result.
    if not bundle:
        return {"verdict": "FAIL", "checked": 0,
                "findings": [{"contract": "*", "kind": "DENOMINATOR",
                              "detail": "empty bundle: zero records checked cannot be a PASS"}]}
    for contract, record in bundle.items():
        if not isinstance(record, dict):
            findings.append({"contract": contract, "kind": "SCHEMA",
                             "detail": "record must be an object"})
            continue
        for f in validate_record(contract, record, schemas_dir):
            findings.append({"contract": contract, "kind": "SCHEMA", "detail": f})
        for f in semantic_invariants(contract, record, frozen_context):
            findings.append({"contract": contract, "kind": "SEMANTIC", "detail": f})
    return {"verdict": "PASS" if not findings else "FAIL",
            "checked": len(bundle), "findings": findings}


def derive_frozen_context(source: dict[str, Any] | None = None, *,
                          trace_endpoint_hashes: dict[str, str] | None = None,
                          profile_requirement: dict[str, Any] | None = None,
                          oracle_expected: dict[str, str] | None = None) -> dict[str, Any]:
    """Assemble a deterministic frozen context for ``validate_bundle``.

    The pieces are all caller-held data; nothing here consults an LLM, the network or any clock.
    A PI package carries its atoms and trace links, so when ``source`` is a PI package the
    subject->digest endpoint map and the oracle-expected map are read straight from it. Profile
    requirements come from the frozen ``profiles.PROFILES`` table by default. Only derivable
    pieces are emitted: a map is omitted (rather than guessed) when its source is absent, so the
    validator's fail-closed branch for that binding still fires.
    """
    from .profiles import PROFILES
    ctx: dict[str, Any] = {}
    endpoint_hashes = dict(trace_endpoint_hashes or {})
    oracle_expected_map = dict(oracle_expected or {})
    if isinstance(source, dict):
        ssc = source.get("stable_semantic_contract") or {}
        for atom in ssc.get("atoms") or []:
            if atom.get("subject_id") and atom.get("content_hash"):
                endpoint_hashes.setdefault(atom["subject_id"], atom["content_hash"])
            oracle = ((atom.get("risk_guard") or {}).get("oracle") or {})
            if atom.get("req_id") and oracle.get("expected") is not None:
                oracle_expected_map.setdefault(atom["req_id"], oracle["expected"])
        if source.get("subject_id") and source.get("content_hash"):
            endpoint_hashes.setdefault(source["subject_id"], source["content_hash"])
    if endpoint_hashes:
        ctx["trace_endpoint_hashes"] = endpoint_hashes
    if oracle_expected_map:
        ctx["oracle_expected"] = oracle_expected_map
    ctx["profile_requirement"] = profile_requirement or {
        name: {"assurance": list(spec["assurance"]), "artifact_depth": spec["artifact_depth"]}
        for name, spec in PROFILES.items()}
    return ctx
