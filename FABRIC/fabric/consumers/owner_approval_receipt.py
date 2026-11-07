# -*- coding: utf-8 -*-
"""WP-FHS-02 / D-17 (hole 4) — typed reader for the third leg's owner approval.

The `owner_approved` leg had the same defect the other two evidence legs had, one layer worse: the
module declared `LEG_PROVENANCE["owner_approved"] = {"OWNER_APPROVAL_RECEIPT",
"POLICY_OWNER_DIRECTIVE"}` and then read nothing. Nothing opened an artifact, nothing checked a
signer, nothing compared a digest with bytes on disk — so a caller-supplied dict carrying the label
and the source digest satisfied the leg. That is why the six-leg binding could only ever reach
`BOUND` with an owner leg the code could not distinguish from a forgery.

This reader closes that. It accepts one `OWNER_APPROVAL_RECEIPT@1` (or `POLICY_OWNER_DIRECTIVE@1`),
re-derives the digest of the policy bytes it approves, and requires the document to carry:

* the **policy digest it approves** (`policy.sha256`, re-derived from `policy.path`) and a scope;
* the **approving principal**: an OS SID and a role label (`principal.sid`, `principal.role`);
* an **issued_at / expires_at pair** (timezone-aware ISO-8601, ordered, not expired);
* a **detached signature** over the document's canonical body (everything but `signature`) plus a
  `key_id` and the public key material the signature is checked against;
* a key **distinct from the reading process**: a document whose principal SID, key_id or pid is the
  reader's own is refused as a self-signed approval.

Honest limits, stated here because they bound what a PASS means:

* the reader verifies the signature against the key **the document itself names**. That proves the
  body was signed by whoever holds the matching private key; it does NOT prove the key belongs to
  the Policy Owner. Pass `trusted_key_ids=` (a registry the caller owns) to require a pinned key;
  without it the result is reported as `key_trusted: false`.
* a FIXTURE-signed receipt proves the *reader path is reachable*. It is not an owner approval and
  must never be presented as one.
* this reader signs nothing, holds no key and activates nothing: `host_policy_active` stays
  unclaimed, and `leg()`'s provenance set is unchanged.
"""
from __future__ import annotations

import base64
import binascii
import datetime as _dt
import getpass
import hashlib
import json
import os
import re
import socket
from pathlib import Path
from typing import Any, NoReturn

SCHEMA_APPROVAL = "OWNER_APPROVAL_RECEIPT@1"
SCHEMA_DIRECTIVE = "POLICY_OWNER_DIRECTIVE@1"
#: schema -> the provenance this leg may carry when the document is that schema.
SCHEMA_PROVENANCE = {
    SCHEMA_APPROVAL: "OWNER_APPROVAL_RECEIPT",
    SCHEMA_DIRECTIVE: "POLICY_OWNER_DIRECTIVE",
}
READER = "owner-receipt-reader"
LEG = "owner_approved"
EVIDENCE_CLASS = "HOST_RAW"
ALGS = ("ED25519",)

CODES = (
    "OWNER_RECEIPT_UNREADABLE",
    "OWNER_RECEIPT_MALFORMED",
    "OWNER_RECEIPT_SCHEMA_MISMATCH",
    "OWNER_RECEIPT_SCOPE_MISMATCH",
    "OWNER_RECEIPT_EPOCH_MISMATCH",
    "OWNER_RECEIPT_MISSING_PRINCIPAL",
    "OWNER_RECEIPT_NO_SIGNER",
    "OWNER_RECEIPT_SIGNER_IS_READER",
    "OWNER_RECEIPT_KEY_UNUSABLE",
    "OWNER_RECEIPT_KEY_UNTRUSTED",
    "OWNER_RECEIPT_VERIFIER_UNAVAILABLE",
    "OWNER_RECEIPT_SIGNATURE_INVALID",
    "OWNER_RECEIPT_EXPIRED",
    "OWNER_RECEIPT_TIME_INVALID",
    "OWNER_RECEIPT_POLICY_UNREADABLE",
    "OWNER_RECEIPT_DIGEST_MISMATCH",
)

_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_SKEW_S = 300


class OwnerReceiptRefusal(Exception):
    """Typed refusal: an owner approval was found but cannot substantiate the third leg."""

    def __init__(self, message: str, *, code: str, leg: str = LEG) -> None:
        super().__init__(message)
        self.code = code
        self.leg = leg

    def as_dict(self) -> dict[str, Any]:
        return {"verdict": "REFUSED", "code": self.code, "leg": self.leg, "message": str(self)}


def _not_observed(path: Path, code: str, reason: str, **expected: Any) -> dict[str, Any]:
    """No receipt was read. Shaped unlike a leg: no digest, provenance, reader or signature."""
    return {"state": "NOT_OBSERVED", "code": code, "reason": reason, "leg": None, "kind": LEG,
            "path": str(path), "evidence_class": "NOT_OBSERVED", "expected": expected}


def canonical_body(body: dict[str, Any]) -> bytes:
    """The exact bytes the signature covers: the document minus its `signature` block."""
    return json.dumps({k: v for k, v in body.items() if k != "signature"}, sort_keys=True,
                      separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def reader_identity(*, reader_sid: str | None = None,
                    reader_key_id: str | None = None) -> dict[str, Any]:
    """Who is reading. Used only to refuse an approval this very process produced itself."""
    return {
        "sid": (reader_sid if reader_sid is not None
                else os.environ.get("FABRIC_READER_SID", "")),
        "key_id": (reader_key_id if reader_key_id is not None
                   else os.environ.get("FABRIC_READER_KEY_ID", "")),
        "pid": os.getpid(),
        "user": getpass.getuser(),
        "host": socket.gethostname(),
    }


def _parse_utc(value: Any) -> _dt.datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    if text.endswith(("Z", "z")):
        text = text[:-1] + "+00:00"
    try:
        parsed = _dt.datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(_dt.timezone.utc)


def _b64(value: Any) -> bytes | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        return base64.b64decode(value.strip(), validate=True)
    except (binascii.Error, ValueError):
        return None


def verify_detached_signature(*, alg: Any, public_key_b64: Any, signature_b64: Any,
                              message: bytes) -> bool:
    """True when `signature_b64` is a valid signature over `message` by the named public key.

    Ed25519 only, and the verifier is imported lazily: a host without `cryptography` must refuse an
    approval (`OWNER_RECEIPT_VERIFIER_UNAVAILABLE`), never wave one through. `False` means the
    signature is invalid; `None`-shaped problems (bad base64, wrong key length) raise.
    """
    if not isinstance(alg, str) or alg.strip().upper() not in ALGS:
        raise OwnerReceiptRefusal(
            f"signature alg is {alg!r}; this reader verifies {list(ALGS)} and nothing else",
            code="OWNER_RECEIPT_KEY_UNUSABLE")
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    except ImportError:
        raise OwnerReceiptRefusal(
            "the Ed25519 verifier (package `cryptography`) is not importable on this host, so no "
            "signature can be checked and no approval can be accepted",
            code="OWNER_RECEIPT_VERIFIER_UNAVAILABLE") from None
    raw_key = _b64(public_key_b64)
    raw_sig = _b64(signature_b64)
    if raw_key is None or len(raw_key) != 32:
        raise OwnerReceiptRefusal(
            "the key the document names is not 32 bytes of base64-encoded Ed25519 public key",
            code="OWNER_RECEIPT_KEY_UNUSABLE")
    if raw_sig is None or len(raw_sig) != 64:
        raise OwnerReceiptRefusal(
            "the detached signature is not 64 bytes of base64", 
            code="OWNER_RECEIPT_SIGNATURE_INVALID")
    try:
        public_key = Ed25519PublicKey.from_public_bytes(raw_key)
    except ValueError:
        raise OwnerReceiptRefusal(
            "the key the document names is not a valid Ed25519 public key",
            code="OWNER_RECEIPT_KEY_UNUSABLE") from None
    try:
        public_key.verify(raw_sig, message)
    except InvalidSignature:
        return False
    return True


def _check_principal(body: dict[str, Any], reader: dict[str, Any]) -> dict[str, Any]:
    principal = body.get("principal")
    if not isinstance(principal, dict):
        raise OwnerReceiptRefusal(
            "the document names no approving principal (an OS SID and a role label), so there is "
            "no one to attribute the approval to", code="OWNER_RECEIPT_MISSING_PRINCIPAL")
    sid = principal.get("sid")
    role = principal.get("role")
    if not isinstance(sid, str) or not sid.strip():
        raise OwnerReceiptRefusal("principal.sid is missing or empty",
                                  code="OWNER_RECEIPT_MISSING_PRINCIPAL")
    if not isinstance(role, str) or not role.strip():
        raise OwnerReceiptRefusal("principal.role is missing or empty",
                                  code="OWNER_RECEIPT_MISSING_PRINCIPAL")
    if reader["sid"] and sid.strip() == str(reader["sid"]).strip():
        raise OwnerReceiptRefusal(
            f"the approving principal is this reading process (sid {sid!r}): a self-signed "
            "approval is not an owner approval", code="OWNER_RECEIPT_SIGNER_IS_READER")
    signer_pid = principal.get("pid")
    if isinstance(signer_pid, int) and not isinstance(signer_pid, bool) \
            and signer_pid == reader["pid"]:
        raise OwnerReceiptRefusal(
            f"the approving principal carries pid {signer_pid}, which is this reading process",
            code="OWNER_RECEIPT_SIGNER_IS_READER")
    return principal


def _check_times(body: dict[str, Any], now: _dt.datetime) -> tuple[_dt.datetime, _dt.datetime]:
    issued = _parse_utc(body.get("issued_at"))
    expires = _parse_utc(body.get("expires_at"))
    if issued is None:
        raise OwnerReceiptRefusal(
            f"issued_at is {body.get('issued_at')!r}, not a timezone-aware ISO-8601 instant",
            code="OWNER_RECEIPT_TIME_INVALID")
    if expires is None:
        raise OwnerReceiptRefusal(
            f"expires_at is {body.get('expires_at')!r}, not a timezone-aware ISO-8601 instant",
            code="OWNER_RECEIPT_TIME_INVALID")
    if expires <= issued:
        raise OwnerReceiptRefusal(
            f"expires_at {body.get('expires_at')!r} does not follow issued_at "
            f"{body.get('issued_at')!r}", code="OWNER_RECEIPT_TIME_INVALID")
    if issued > now + _dt.timedelta(seconds=_SKEW_S):
        raise OwnerReceiptRefusal(
            f"issued_at {body.get('issued_at')!r} is in the future", code="OWNER_RECEIPT_TIME_INVALID")
    if expires <= now:
        raise OwnerReceiptRefusal(
            f"the approval expired at {body.get('expires_at')!r}; an expired approval approves "
            "nothing", code="OWNER_RECEIPT_EXPIRED")
    return issued, expires


def _resolve_policy(receipt_path: Path, body: dict[str, Any],
                    policy_path: str | Path | None) -> Path:
    if policy_path is not None:
        return Path(policy_path)
    policy = body.get("policy")
    declared = policy.get("path") if isinstance(policy, dict) else None
    if not isinstance(declared, str) or not declared.strip():
        raise OwnerReceiptRefusal(
            "the document names no policy.path, so the approved bytes cannot be re-read",
            code="OWNER_RECEIPT_POLICY_UNREADABLE")
    candidate = Path(declared)
    return candidate if candidate.is_absolute() else (receipt_path.parent / candidate)


def read_owner_receipt(path: str | Path, *, expected_scope: str, expected_epoch: int | str | None = None,
                       policy_path: str | Path | None = None,
                       reader_sid: str | None = None, reader_key_id: str | None = None,
                       trusted_key_ids: set[str] | frozenset[str] | None = None,
                       now: _dt.datetime | None = None) -> dict[str, Any]:
    """Read and verify one owner approval. Returns the third leg or a `NOT_OBSERVED` marker.

    Every other failure raises `OwnerReceiptRefusal` with one of `CODES`. `trusted_key_ids`
    optionally pins the key the document names to a registry the caller owns; without it the
    result says `key_trusted: False` and the binding refuses to *claim* key provenance.
    """
    receipt_path = Path(path)
    now = now or _dt.datetime.now(_dt.timezone.utc)
    reader = reader_identity(reader_sid=reader_sid, reader_key_id=reader_key_id)
    expected = {"scope": expected_scope, "epoch": expected_epoch, "reader": reader["sid"] or None}

    try:
        raw_bytes = receipt_path.read_bytes()
    except FileNotFoundError:
        return _not_observed(receipt_path, "OWNER_RECEIPT_UNREADABLE",
                             f"no owner approval at {receipt_path}", **expected)
    except OSError as exc:
        return _not_observed(receipt_path, "OWNER_RECEIPT_UNREADABLE",
                             f"owner approval {receipt_path} is not readable: "
                             f"{exc.strerror or exc}", **expected)

    try:
        body = json.loads(raw_bytes.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise OwnerReceiptRefusal(f"{receipt_path} is not UTF-8 JSON: {exc}",
                                  code="OWNER_RECEIPT_MALFORMED") from None
    if not isinstance(body, dict):
        raise OwnerReceiptRefusal(f"{receipt_path} is a {type(body).__name__}, not an object",
                                  code="OWNER_RECEIPT_MALFORMED")

    schema = body.get("schema")
    if schema not in SCHEMA_PROVENANCE:
        raise OwnerReceiptRefusal(
            f"schema is {schema!r}; this reader accepts {sorted(SCHEMA_PROVENANCE)}",
            code="OWNER_RECEIPT_SCHEMA_MISMATCH")
    if body.get("scope") != expected_scope:
        raise OwnerReceiptRefusal(
            f"scope is {body.get('scope')!r}, expected {expected_scope!r}",
            code="OWNER_RECEIPT_SCOPE_MISMATCH")
    if expected_epoch is not None and body.get("epoch") is not None \
            and str(body.get("epoch")) != str(expected_epoch):
        raise OwnerReceiptRefusal(
            f"epoch is {body.get('epoch')!r}, expected {expected_epoch!r}",
            code="OWNER_RECEIPT_EPOCH_MISMATCH")

    principal = _check_principal(body, reader)
    issued, expires = _check_times(body, now)

    signature = body.get("signature")
    if not isinstance(signature, dict):
        raise OwnerReceiptRefusal(
            "the document carries no detached signature block, so nothing shows the principal "
            "approved this body", code="OWNER_RECEIPT_NO_SIGNER")
    key_id = signature.get("key_id")
    if not isinstance(key_id, str) or not key_id.strip():
        raise OwnerReceiptRefusal("signature.key_id is missing or empty",
                                  code="OWNER_RECEIPT_NO_SIGNER")
    if reader["key_id"] and key_id.strip() == str(reader["key_id"]).strip():
        raise OwnerReceiptRefusal(
            f"the signing key_id {key_id!r} is the reading key: a self-signed approval is not an "
            "owner approval", code="OWNER_RECEIPT_SIGNER_IS_READER")
    key = body.get("key")
    if not isinstance(key, dict) or not isinstance(key.get("public_key_b64"), str):
        raise OwnerReceiptRefusal(
            "the document names no key material to verify the signature against",
            code="OWNER_RECEIPT_KEY_UNUSABLE")
    if key.get("key_id") != key_id:
        raise OwnerReceiptRefusal(
            f"signature.key_id {key_id!r} does not match key.key_id {key.get('key_id')!r}: the "
            "signature is not over the key the document names",
            code="OWNER_RECEIPT_KEY_UNUSABLE")

    key_trusted = False
    if trusted_key_ids is not None:
        if key_id.strip() not in {str(item) for item in trusted_key_ids}:
            raise OwnerReceiptRefusal(
                f"key_id {key_id!r} is not in the caller's trusted key registry: a document that "
                "names its own key cannot establish key provenance by itself",
                code="OWNER_RECEIPT_KEY_UNTRUSTED")
        key_trusted = True

    message = canonical_body(body)
    declared_body_sha = signature.get("signed_body_sha256")
    if declared_body_sha is not None:
        if not isinstance(declared_body_sha, str) or not _HEX64.match(declared_body_sha.lower()):
            raise OwnerReceiptRefusal(
                f"signature.signed_body_sha256 is {declared_body_sha!r}, not a sha256 hex digest",
                code="OWNER_RECEIPT_SIGNATURE_INVALID")
        observed_body_sha = hashlib.sha256(message).hexdigest()
        if declared_body_sha.lower() != observed_body_sha:
            raise OwnerReceiptRefusal(
                "the body was edited after signing (signed_body_sha256 "
                f"{declared_body_sha[:12]} != {observed_body_sha[:12]})",
                code="OWNER_RECEIPT_SIGNATURE_INVALID")

    ok = verify_detached_signature(alg=signature.get("alg"), public_key_b64=key.get("public_key_b64"),
                                   signature_b64=signature.get("sig_b64"), message=message)
    if ok is not True:
        raise OwnerReceiptRefusal(
            f"the detached signature does not verify against key_id {key_id!r}",
            code="OWNER_RECEIPT_SIGNATURE_INVALID")

    policy = body.get("policy")
    declared_digest = policy.get("sha256") if isinstance(policy, dict) else None
    if not isinstance(declared_digest, str) or not _HEX64.match(declared_digest.strip().lower()):
        raise OwnerReceiptRefusal(
            f"policy.sha256 is {declared_digest!r}, not a sha256 hex digest",
            code="OWNER_RECEIPT_DIGEST_MISMATCH")
    policy_file = _resolve_policy(receipt_path, body, policy_path)
    try:
        observed_digest = hashlib.sha256(policy_file.read_bytes()).hexdigest()
        policy_bytes = policy_file.stat().st_size
    except OSError as exc:
        raise OwnerReceiptRefusal(
            f"approved bytes {policy_file} are not readable: {exc.strerror or exc}",
            code="OWNER_RECEIPT_POLICY_UNREADABLE") from None
    if observed_digest != declared_digest.strip().lower():
        raise OwnerReceiptRefusal(
            "policy.sha256 does not match the bytes on disk "
            f"({declared_digest[:12]} != {observed_digest[:12]})",
            code="OWNER_RECEIPT_DIGEST_MISMATCH")

    return {
        "state": "OBSERVED",
        "leg": LEG,
        "digest": observed_digest,
        "provenance": SCHEMA_PROVENANCE[schema],
        "reader": READER,
        "scope": body.get("scope"),
        "epoch": expected_epoch if expected_epoch is not None else body.get("epoch"),
        "observed_at": body.get("issued_at"),
        "evidence_class": EVIDENCE_CLASS,
        "principal": {"sid": principal["sid"].strip(), "role": principal["role"].strip(),
                      "display": principal.get("display")},
        "key_id": key_id.strip(),
        "key_trusted": key_trusted,
        "issued_at": issued.isoformat(),
        "expires_at": expires.isoformat(),
        "policy_path": str(policy_file),
        "policy_bytes": policy_bytes,
        "receipt_sha256": hashlib.sha256(raw_bytes).hexdigest(),
        "receipt_path": str(receipt_path),
        "verified": True,
        "note": ("detached signature verified against the key the document names; the approved "
                 "bytes were re-hashed by this reader. Key provenance is "
                 f"{'pinned' if key_trusted else 'NOT established (unpinned key)'}, and no policy "
                 "activation is claimed"),
    }


def is_verified_owner_leg(candidate: Any) -> bool:
    """True only for a dict this reader produced for the third leg (structural, re-checkable)."""
    if not isinstance(candidate, dict):
        return False
    return (candidate.get("state") == "OBSERVED"
            and candidate.get("verified") is True
            and candidate.get("leg") == LEG
            and candidate.get("provenance") in set(SCHEMA_PROVENANCE.values())
            and candidate.get("reader") == READER
            and candidate.get("evidence_class") == EVIDENCE_CLASS
            and isinstance(candidate.get("digest"), str)
            and bool(_HEX64.match(str(candidate.get("digest", "")).lower()))
            and isinstance(candidate.get("principal"), dict)
            and isinstance(candidate.get("key_id"), str)
            and isinstance(candidate.get("receipt_sha256"), str))


if __name__ == "__main__":  # pragma: no cover - operator probe, not a gate
    import sys

    if len(sys.argv) < 3:
        print("usage: owner_approval_receipt.py <receipt.json> <scope> [epoch] [reader_sid]")
        raise SystemExit(2)
    args = sys.argv[1:]
    try:
        out = read_owner_receipt(args[0], expected_scope=args[1],
                                 expected_epoch=args[2] if len(args) > 2 else None,
                                 reader_sid=args[3] if len(args) > 3 else None)
    except OwnerReceiptRefusal as exc:
        print(json.dumps(exc.as_dict(), ensure_ascii=False, indent=2))
        raise SystemExit(1)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    raise SystemExit(0 if out.get("state") == "OBSERVED" else 1)
