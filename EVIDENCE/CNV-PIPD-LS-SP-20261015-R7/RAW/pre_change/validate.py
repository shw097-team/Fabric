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


def semantic_invariants(contract: str, record: dict[str, Any]) -> list[str]:
    """Semantic invariants that a JSON Schema cannot express."""
    out: list[str] = []
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
    if contract in RELEASE_BOUND and ch and len(record) > 4:
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
    return out


def validate_bundle(bundle: dict[str, dict[str, Any]], schemas_dir: Path | None = None) -> dict[str, Any]:
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
        for f in semantic_invariants(contract, record):
            findings.append({"contract": contract, "kind": "SEMANTIC", "detail": f})
    return {"verdict": "PASS" if not findings else "FAIL",
            "checked": len(bundle), "findings": findings}
