# -*- coding: utf-8 -*-
"""WP-FHS-02 — typed reader for the sixth leg's `HGK_CONSUMER_RECEIPT@1`.

The sixth leg (`consumer_ack`) used to exist only as a caller-supplied dict: `build_binding`
reported `host.consumer_ack_observed` from whatever `evidence_class` the caller typed, so the leg
could be filled by a fixture and nothing in the repository read an actual consumer artifact.

This module is a **reader**, not a new authority. It opens one receipt document written by the HGK
policy consumer, re-derives the digest of the bytes that receipt acknowledges, and returns a leg
shaped exactly like `policy_binding.leg(...)`. It grants nothing:

* it cannot activate a policy (`host_policy_active` is never claimed, not even on success);
* it does not know whether the acknowledged bytes are still the active epoch's bytes — that stays
  `build_binding`'s cross-check against `active_epoch` / `loaded_digest`;
* a receipt that does not describe *this* subject/scope/epoch/consumer is refused with a typed code
  instead of being silently re-scoped.

Honest classification: a successful read is `evidence_class="HOST_RAW"` because the digest is
recomputed from raw bytes on disk, not because a document says so. `HOST_RAW` here means "raw
consumer-emitted bytes observed by a reader", never "policy in force on a host". A receipt written by
a test is therefore still `HOST_RAW` **as an observation** — which is why the tests below assert what
it does *not* buy: no `host_policy_active`, no binding without the other five legs, and no BOUND when
verification fails.

Refusals are typed (`HGKReceiptRefusal.code`) so a caller can branch on the code. Nothing in this
module raises a bare `ValueError`/`KeyError`/`json.JSONDecodeError` on receipt content.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

SCHEMA = "HGK_CONSUMER_RECEIPT@1"
PROVENANCE = "HGK_CONSUMER_RECEIPT"
READER = "hgk-consumer-receipt-reader"
LEG = "consumer_ack"
EVIDENCE_CLASS = "HOST_RAW"

#: Every code this reader may emit. `NOT_OBSERVED`/`UNREADABLE` are returned (there is no receipt to
#: refuse); the rest are raised as `HGKReceiptRefusal`.
CODES = (
    "HGK_RECEIPT_NOT_OBSERVED",
    "HGK_RECEIPT_UNREADABLE",
    "HGK_RECEIPT_MALFORMED",
    "HGK_RECEIPT_SCHEMA_MISMATCH",
    "HGK_RECEIPT_SUBJECT_MISMATCH",
    "HGK_RECEIPT_SCOPE_MISMATCH",
    "HGK_RECEIPT_EPOCH_MISMATCH",
    "HGK_RECEIPT_CONSUMER_MISMATCH",
    "HGK_RECEIPT_DIGEST_MISMATCH",
    "HGK_RECEIPT_MISSING_ACK",
    "HGK_RECEIPT_RAW_UNREADABLE",
)

_HEX64 = re.compile(r"^[0-9a-f]{64}$")


class HGKReceiptRefusal(Exception):
    """Typed refusal: a receipt was found but cannot substantiate the sixth leg."""

    def __init__(self, message: str, *, code: str, leg: str = LEG) -> None:
        super().__init__(message)
        self.code = code
        self.leg = leg

    def as_dict(self) -> dict[str, Any]:
        return {"verdict": "REFUSED", "code": self.code, "leg": self.leg,
                "message": str(self)}


def _not_observed(path: Path, code: str, reason: str, **expected: Any) -> dict[str, Any]:
    """No receipt was read. Deliberately shaped *unlike* a leg: no digest, no provenance, no reader.

    Returning an empty leg here would let a caller paste `{}` into `build_binding` and look bound;
    `state="NOT_OBSERVED"` makes the absence visible instead.
    """
    return {"state": "NOT_OBSERVED", "code": code, "reason": reason,
            "leg": None, "kind": LEG, "path": str(path),
            "evidence_class": "NOT_OBSERVED", "expected": expected}


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _resolve_raw(receipt_path: Path, body: dict[str, Any],
                 raw_path: str | Path | None) -> Path:
    """Locate the bytes the receipt acknowledges.

    `raw_path` inside the receipt is treated as relative to the receipt's own directory so a receipt
    stays replayable next to its bytes.
    """
    if raw_path is not None:
        return Path(raw_path)
    declared = body.get("raw_path")
    if not isinstance(declared, str) or not declared.strip():
        raise HGKReceiptRefusal(
            "receipt has no raw_path, so raw_sha256 cannot be checked against any bytes",
            code="HGK_RECEIPT_RAW_UNREADABLE")
    candidate = Path(declared)
    return candidate if candidate.is_absolute() else (receipt_path.parent / candidate)


def load_receipt(path: str | Path, *, expected_subject: str, expected_scope: str,
                 expected_epoch: int | str, consumer_id: str,
                 raw_path: str | Path | None = None) -> dict[str, Any]:
    """Read and verify one `HGK_CONSUMER_RECEIPT@1` document.

    Returns a leg for the sixth leg on success (`state="OBSERVED"`), or a `NOT_OBSERVED` marker when
    the file is absent/unreadable. Every other failure raises `HGKReceiptRefusal` with a
    `HGK_RECEIPT_*` code; no native exception escapes on receipt content.
    """
    receipt_path = Path(path)
    expected = {"subject": expected_subject, "scope": expected_scope,
                "policy_epoch": expected_epoch, "consumer_id": consumer_id}

    try:
        raw_bytes = receipt_path.read_bytes()
    except FileNotFoundError:
        return _not_observed(receipt_path, "HGK_RECEIPT_NOT_OBSERVED",
                             f"no receipt at {receipt_path}", **expected)
    except OSError as exc:
        return _not_observed(receipt_path, "HGK_RECEIPT_UNREADABLE",
                             f"receipt {receipt_path} is not readable: {exc.strerror or exc}",
                             **expected)

    try:
        body = json.loads(raw_bytes.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise HGKReceiptRefusal(f"receipt {receipt_path} is not UTF-8 JSON: {exc}",
                                code="HGK_RECEIPT_MALFORMED") from None
    if not isinstance(body, dict):
        raise HGKReceiptRefusal(f"receipt {receipt_path} is a {type(body).__name__}, not an object",
                                code="HGK_RECEIPT_MALFORMED")

    if body.get("schema") != SCHEMA:
        raise HGKReceiptRefusal(
            f"receipt schema is {body.get('schema')!r}, expected {SCHEMA!r}",
            code="HGK_RECEIPT_SCHEMA_MISMATCH")
    if body.get("subject") != expected_subject:
        raise HGKReceiptRefusal(
            f"receipt subject is {body.get('subject')!r}, expected {expected_subject!r}",
            code="HGK_RECEIPT_SUBJECT_MISMATCH")
    if body.get("scope") != expected_scope:
        raise HGKReceiptRefusal(
            f"receipt scope is {body.get('scope')!r}, expected {expected_scope!r}",
            code="HGK_RECEIPT_SCOPE_MISMATCH")
    if str(body.get("policy_epoch")) != str(expected_epoch):
        raise HGKReceiptRefusal(
            f"receipt policy_epoch is {body.get('policy_epoch')!r}, expected {expected_epoch!r}",
            code="HGK_RECEIPT_EPOCH_MISMATCH")
    if body.get("consumer_id") != consumer_id:
        raise HGKReceiptRefusal(
            f"receipt consumer_id is {body.get('consumer_id')!r}, expected {consumer_id!r}",
            code="HGK_RECEIPT_CONSUMER_MISMATCH")

    ack = body.get("ack")
    if ack is None or (isinstance(ack, (dict, list, str)) and len(ack) == 0):
        raise HGKReceiptRefusal(
            "receipt carries no ack — an unacknowledged policy is not a consumer acknowledgement",
            code="HGK_RECEIPT_MISSING_ACK")

    declared_digest = body.get("raw_sha256")
    if not isinstance(declared_digest, str) or not _HEX64.match(declared_digest.lower()):
        raise HGKReceiptRefusal(
            f"receipt raw_sha256 is {declared_digest!r}, not a sha256 hex digest",
            code="HGK_RECEIPT_DIGEST_MISMATCH")

    raw_file = _resolve_raw(receipt_path, body, raw_path)
    try:
        observed_digest = _sha256_file(raw_file)
    except OSError as exc:
        raise HGKReceiptRefusal(
            f"acknowledged bytes {raw_file} are not readable: {exc.strerror or exc}",
            code="HGK_RECEIPT_RAW_UNREADABLE") from None
    if observed_digest != declared_digest.lower():
        raise HGKReceiptRefusal(
            "receipt raw_sha256 does not match the bytes it acknowledges "
            f"({declared_digest[:12]} != {observed_digest[:12]})",
            code="HGK_RECEIPT_DIGEST_MISMATCH")

    observed_at = body.get("observed_at")
    return {
        "state": "OBSERVED",
        "leg": LEG,
        "digest": observed_digest,
        "provenance": PROVENANCE,
        "reader": READER,
        "scope": expected_scope,
        "epoch": expected_epoch,
        "observed_at": observed_at if isinstance(observed_at, str) else "",
        "evidence_class": EVIDENCE_CLASS,
        "subject": expected_subject,
        "consumer_id": consumer_id,
        "receipt_sha256": hashlib.sha256(raw_bytes).hexdigest(),
        "receipt_path": str(receipt_path),
        "raw_path": str(raw_file),
        "verified": True,
        "ack": ack,
        "note": ("consumer acknowledged the bytes named by raw_sha256; this is a read of raw "
                 "bytes, never a claim that the policy is active on the host"),
    }


def is_verified_leg(candidate: Any) -> bool:
    """True only for a dict this reader produced for the sixth leg (structural, re-checkable)."""
    if not isinstance(candidate, dict):
        return False
    return (candidate.get("state") == "OBSERVED"
            and candidate.get("verified") is True
            and candidate.get("leg") == LEG
            and candidate.get("provenance") == PROVENANCE
            and candidate.get("reader") == READER
            and candidate.get("evidence_class") == EVIDENCE_CLASS
            and isinstance(candidate.get("digest"), str)
            and bool(_HEX64.match(str(candidate.get("digest", "")).lower()))
            and isinstance(candidate.get("receipt_sha256"), str))


if __name__ == "__main__":  # pragma: no cover - operator probe, not a gate
    import sys

    if len(sys.argv) < 2:
        print("usage: hgk_consumer_receipt.py <receipt.json> [subject scope epoch consumer_id]")
        raise SystemExit(2)
    args = sys.argv[1:]
    try:
        out = load_receipt(args[0],
                           expected_subject=args[1] if len(args) > 1 else "",
                           expected_scope=args[2] if len(args) > 2 else "",
                           expected_epoch=args[3] if len(args) > 3 else "",
                           consumer_id=args[4] if len(args) > 4 else "")
    except HGKReceiptRefusal as exc:
        print(json.dumps(exc.as_dict(), ensure_ascii=False, indent=2))
        raise SystemExit(1)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    raise SystemExit(0 if out.get("state") == "OBSERVED" else 1)
