# -*- coding: utf-8 -*-
"""WP-FHS-02 / D-17 — typed reader for the fifth leg's `HOST_LOAD_RECEIPT@1`.

Before this module the repository had a *producer* for the loaded leg in the round tree
(`inc4/candidates/host_load_receipt.py`) and **no reader at all** in Fabric, so `build_binding`
accepted `loaded_digest` from whatever dict the caller passed. A receipt with a perfectly valid
envelope over the real policy bytes and no producer block was indistinguishable from a produced one:
nothing in Fabric opened the document.

This reader closes that. It opens one `HOST_LOAD_RECEIPT@1`, re-derives the digest of the policy
bytes from disk, and refuses the document unless it also carries a **producer/process block** that
identifies the OS process that read those bytes:

* `process` (or, failing that, `producer`) must be an object;
* `pid` must be a positive integer (a bool is not an int here);
* it must carry a process-start identity (`process_create_time_utc` and/or
  `process_identity_sha256`) **or** a boot identity (`boot_epoch_s`), because a pid alone is
  recycled by the OS and proves nothing;
* whatever is present must be structurally consistent: `ppid` a non-negative int, a parseable
  timezone-aware ISO-8601 process start that is not before the boot instant and not in the future,
  a 64-hex process identity, a positive boot epoch.

Refusals are typed (`LoadReceiptRefusal.code`) and every one of them is a *refusal*, never a
downgrade: a load receipt that fails any check cannot become the fifth leg. What a successful read
still does **not** mean: `host_policy_active`, or that a policy engine consumed these bytes. This
module proves "a process read and re-read these bytes"; it holds no key and signs nothing, so the
pid is only as trustworthy as the producer that wrote the file.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import re
from pathlib import Path
from typing import Any, NoReturn

SCHEMA = "HOST_LOAD_RECEIPT@1"
READER = "host-load-receipt-reader"
LEG = "loaded_digest"
PROVENANCE = "HOST_LOAD_RAW"
EVIDENCE_CLASS = "HOST_RAW"
LOAD_STATE = "LOAD_OBSERVED"

#: Codes already used by the round's load producer/driver (`inc4/candidates/hgk_consumer_receipt_run.py`)
#: are kept verbatim so an operator reads the same vocabulary on both sides of the receipt.
CODES = (
    "LOAD_RECEIPT_UNREADABLE",
    "LOAD_RECEIPT_MALFORMED",
    "LOAD_RECEIPT_SCHEMA_MISMATCH",
    "LOAD_RECEIPT_SELF_HASH_MISMATCH",
    "LOAD_RECEIPT_STATE_NOT_LOADED",
    "LOAD_RECEIPT_SCOPE_MISMATCH",
    "LOAD_RECEIPT_SUBJECT_MISMATCH",
    "LOAD_RECEIPT_EPOCH_MISMATCH",
    "LOAD_RECEIPT_NOT_HOST_RAW",
    "LOAD_RECEIPT_READBACK_FAILED",
    "LOAD_RECEIPT_POLICY_UNREADABLE",
    "LOAD_RECEIPT_DIGEST_MISMATCH",
    # D-17, new: the two refusals this reader exists for.
    "LOAD_RECEIPT_NO_PRODUCER_BLOCK",
    "LOAD_RECEIPT_PRODUCER_BLOCK_INVALID",
)

_HEX64 = re.compile(r"^[0-9a-f]{64}$")
#: Clock skew tolerated when comparing a self-declared process start / boot instant with "now".
_SKEW_S = 300


class LoadReceiptRefusal(Exception):
    """Typed refusal: a document was found but cannot substantiate the fifth leg."""

    def __init__(self, message: str, *, code: str, leg: str = LEG) -> None:
        super().__init__(message)
        self.code = code
        self.leg = leg

    def as_dict(self) -> dict[str, Any]:
        return {"verdict": "REFUSED", "code": self.code, "leg": self.leg, "message": str(self)}


def _not_observed(path: Path, code: str, reason: str, **expected: Any) -> dict[str, Any]:
    """No receipt was read. Shaped deliberately unlike a leg: no digest, provenance or reader."""
    return {"state": "NOT_OBSERVED", "code": code, "reason": reason, "leg": None,
            "kind": LEG, "path": str(path), "evidence_class": "NOT_OBSERVED",
            "expected": expected}


def _canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _parse_utc(value: Any) -> _dt.datetime | None:
    """Parse an ISO-8601 instant; return None when it is not one. Naive values are not accepted."""
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


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def validate_process_block(body: dict[str, Any], *, now: _dt.datetime | None = None) -> dict[str, Any]:
    """Structural validation of the producer/process block. Returns the block or refuses.

    A pid on its own is not an identity: pids are recycled, so the block must also carry a process
    start (time and/or a 64-hex process identity) or a boot instant. Anything present beyond that is
    checked for type and internal consistency rather than trusted.
    """
    now = now or _dt.datetime.now(_dt.timezone.utc)

    def refuse(why: str, code: str = "LOAD_RECEIPT_PRODUCER_BLOCK_INVALID") -> NoReturn:
        raise LoadReceiptRefusal(f"producer/process block: {why}", code=code)

    block = body.get("process")
    where = "process"
    if block is None:
        block = body.get("producer")
        where = "producer"
    if block is None:
        refuse("the receipt carries no process block and no producer block, so no OS process is "
               "named as having read the bytes — a hand-written body cannot substantiate a load",
               code="LOAD_RECEIPT_NO_PRODUCER_BLOCK")
    if not isinstance(block, dict):
        refuse(f"{where} is a {type(block).__name__}, not an object",
               code="LOAD_RECEIPT_NO_PRODUCER_BLOCK")
    if "pid" not in block or block.get("pid") is None:
        refuse(f"{where} carries no pid, so nothing identifies the reading process",
               code="LOAD_RECEIPT_NO_PRODUCER_BLOCK")

    pid = block["pid"]
    if not _is_int(pid):
        refuse(f"{where}.pid is {pid!r} ({type(pid).__name__}), not an integer")
    if pid <= 0:
        refuse(f"{where}.pid is {pid}, which no live process can hold")

    if "ppid" in block and block["ppid"] is not None:
        ppid = block["ppid"]
        if not _is_int(ppid) or ppid < 0:
            refuse(f"{where}.ppid is {ppid!r}, not a non-negative integer")

    start = block.get("process_create_time_utc")
    identity = block.get("process_identity_sha256")
    boot = block.get("boot_epoch_s")

    has_start = isinstance(start, str) and bool(start.strip())
    has_identity = isinstance(identity, str) and bool(identity.strip())
    has_boot = boot is not None and boot != ""
    if not (has_start or has_identity or has_boot):
        refuse(f"{where} names pid {pid} but no process start (process_create_time_utc / "
               "process_identity_sha256) and no boot epoch (boot_epoch_s): a bare pid is recycled "
               "by the OS and identifies nothing",
               code="LOAD_RECEIPT_NO_PRODUCER_BLOCK")

    start_dt = None
    if has_start:
        start_dt = _parse_utc(start)
        if start_dt is None:
            refuse(f"{where}.process_create_time_utc is {start!r}, not a timezone-aware ISO-8601 "
                   "instant")
        if start_dt > now + _dt.timedelta(seconds=_SKEW_S):
            refuse(f"{where}.process_create_time_utc is {start!r}, after the current instant "
                   f"{now.isoformat()} — a process cannot start in the future")
    elif identity is not None and not has_identity:
        refuse(f"{where}.process_identity_sha256 is not a non-empty string")

    if has_identity and not _HEX64.match(str(identity).strip().lower()):
        refuse(f"{where}.process_identity_sha256 is {identity!r}, not a sha256 hex digest")

    if has_boot:
        if isinstance(boot, bool) or not isinstance(boot, int) or boot <= 0:
            refuse(f"{where}.boot_epoch_s is {boot!r}, not a positive integer epoch")
        boot_i = boot
        if boot_i > now.timestamp() + _SKEW_S:
            refuse(f"{where}.boot_epoch_s is {boot_i}, after the current instant "
                   f"{int(now.timestamp())}")
        if start_dt is not None and start_dt.timestamp() + _SKEW_S < boot_i:
            refuse(f"{where}.process_create_time_utc is {start!r}, before the boot instant "
                   f"{boot_i} — the process and the boot identity describe different host histories")

    if "hostname" in block and block["hostname"] is not None:
        if not isinstance(block["hostname"], str) or not block["hostname"].strip():
            refuse(f"{where}.hostname is {block['hostname']!r}, not a non-empty string")

    return block


def _resolve_policy(receipt_path: Path, body: dict[str, Any],
                    raw_path: str | Path | None) -> Path:
    if raw_path is not None:
        return Path(raw_path)
    policy = body.get("policy")
    declared = policy.get("path") if isinstance(policy, dict) else None
    if not isinstance(declared, str) or not declared.strip():
        raise LoadReceiptRefusal(
            "receipt names no policy.path, so the loaded bytes cannot be re-read",
            code="LOAD_RECEIPT_POLICY_UNREADABLE")
    candidate = Path(declared)
    return candidate if candidate.is_absolute() else (receipt_path.parent / candidate)


def read_load_receipt(path: str | Path, *, expected_scope: str | None = None,
                      expected_subject: str | None = None,
                      expected_epoch: int | str | None = None,
                      policy_path: str | Path | None = None) -> dict[str, Any]:
    """Read and verify one `HOST_LOAD_RECEIPT@1`.

    Returns the fifth leg on success (`state="OBSERVED"`), a `NOT_OBSERVED` marker when the file is
    absent/unreadable, and raises `LoadReceiptRefusal` for every other defect — in particular
    `LOAD_RECEIPT_NO_PRODUCER_BLOCK` and `LOAD_RECEIPT_PRODUCER_BLOCK_INVALID`.
    """
    receipt_path = Path(path)
    expected = {"scope": expected_scope, "subject": expected_subject, "epoch": expected_epoch}
    try:
        raw_bytes = receipt_path.read_bytes()
    except FileNotFoundError:
        return _not_observed(receipt_path, "LOAD_RECEIPT_UNREADABLE",
                             f"no load receipt at {receipt_path}", **expected)
    except OSError as exc:
        return _not_observed(receipt_path, "LOAD_RECEIPT_UNREADABLE",
                             f"load receipt {receipt_path} is not readable: {exc.strerror or exc}",
                             **expected)

    try:
        body = json.loads(raw_bytes.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise LoadReceiptRefusal(f"load receipt {receipt_path} is not UTF-8 JSON: {exc}",
                                 code="LOAD_RECEIPT_MALFORMED") from None
    if not isinstance(body, dict):
        raise LoadReceiptRefusal(f"load receipt {receipt_path} is a {type(body).__name__}, not an "
                                 "object", code="LOAD_RECEIPT_MALFORMED")

    if body.get("schema") != SCHEMA:
        raise LoadReceiptRefusal(
            f"receipt schema is {body.get('schema')!r}, expected {SCHEMA!r}",
            code="LOAD_RECEIPT_SCHEMA_MISMATCH")

    declared_self = body.get("self_sha256")
    if not isinstance(declared_self, str) or not _HEX64.match(declared_self.strip().lower()):
        raise LoadReceiptRefusal(
            f"receipt self_sha256 is {declared_self!r}, so the body cannot be shown unedited",
            code="LOAD_RECEIPT_SELF_HASH_MISMATCH")
    observed_self = hashlib.sha256(
        _canonical({k: v for k, v in body.items() if k != "self_sha256"})).hexdigest()
    if observed_self != declared_self.strip().lower():
        raise LoadReceiptRefusal(
            "receipt self_sha256 does not match its body "
            f"({declared_self[:12]} != {observed_self[:12]}): the document was edited after sealing",
            code="LOAD_RECEIPT_SELF_HASH_MISMATCH")

    if body.get("state") != LOAD_STATE:
        raise LoadReceiptRefusal(
            f"receipt state is {body.get('state')!r}; only {LOAD_STATE} describes a load",
            code="LOAD_RECEIPT_STATE_NOT_LOADED")

    if expected_scope is not None and body.get("scope") != expected_scope:
        raise LoadReceiptRefusal(
            f"receipt scope is {body.get('scope')!r}, expected {expected_scope!r}",
            code="LOAD_RECEIPT_SCOPE_MISMATCH")
    if expected_subject is not None and body.get("subject") != expected_subject:
        raise LoadReceiptRefusal(
            f"receipt subject is {body.get('subject')!r}, expected {expected_subject!r}",
            code="LOAD_RECEIPT_SUBJECT_MISMATCH")
    if expected_epoch is not None and str(body.get("epoch")) != str(expected_epoch):
        raise LoadReceiptRefusal(
            f"receipt epoch is {body.get('epoch')!r}, expected {expected_epoch!r}",
            code="LOAD_RECEIPT_EPOCH_MISMATCH")

    if body.get("evidence_class") != EVIDENCE_CLASS or body.get("provenance_hint") != PROVENANCE:
        raise LoadReceiptRefusal(
            f"receipt evidence_class/provenance_hint are {body.get('evidence_class')!r}/"
            f"{body.get('provenance_hint')!r}; only {EVIDENCE_CLASS}/{PROVENANCE} may fill the "
            "loaded leg", code="LOAD_RECEIPT_NOT_HOST_RAW")

    readback = body.get("readback")
    if not isinstance(readback, dict) or readback.get("identical") is not True:
        raise LoadReceiptRefusal(
            "receipt does not record a byte-identical readback (readback.identical is not true), "
            "so it does not show the reader saw the same bytes twice",
            code="LOAD_RECEIPT_READBACK_FAILED")

    policy = body.get("policy")
    declared_digest = policy.get("sha256") if isinstance(policy, dict) else None
    if not isinstance(declared_digest, str) or not _HEX64.match(declared_digest.strip().lower()):
        raise LoadReceiptRefusal(
            f"receipt policy.sha256 is {declared_digest!r}, not a sha256 hex digest",
            code="LOAD_RECEIPT_DIGEST_MISMATCH")

    # D-17: the producer/process block is validated *before* the bytes are read. A document that
    # cannot name the process that claims to have read them is refused even if the bytes match.
    process = validate_process_block(body)

    policy_file = _resolve_policy(receipt_path, body, policy_path)
    try:
        observed_digest = _sha256_file(policy_file)
    except OSError as exc:
        raise LoadReceiptRefusal(
            f"loaded bytes {policy_file} are not readable: {exc.strerror or exc}",
            code="LOAD_RECEIPT_POLICY_UNREADABLE") from None
    if observed_digest != declared_digest.strip().lower():
        raise LoadReceiptRefusal(
            "receipt policy.sha256 does not match the bytes on disk "
            f"({declared_digest[:12]} != {observed_digest[:12]})",
            code="LOAD_RECEIPT_DIGEST_MISMATCH")

    return {
        "state": "OBSERVED",
        "leg": LEG,
        "digest": observed_digest,
        "provenance": PROVENANCE,
        "reader": READER,
        "scope": body.get("scope"),
        "epoch": body.get("epoch"),
        "observed_at": str(body.get("generated_at") or ""),
        "evidence_class": EVIDENCE_CLASS,
        "subject": body.get("subject"),
        "policy_path": str(policy_file),
        "policy_bytes": len(policy_file.read_bytes()),
        "receipt_sha256": hashlib.sha256(raw_bytes).hexdigest(),
        "receipt_path": str(receipt_path),
        "process": process,
        "verified": True,
        "note": ("the loaded bytes were re-hashed by this reader and the receipt names the OS "
                 "process (pid plus process start or boot identity) that read them; this is a "
                 "read, never an activation"),
    }


def is_verified_load_leg(candidate: Any) -> bool:
    """True only for a dict this reader produced for the fifth leg (structural, re-checkable)."""
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
            and isinstance(candidate.get("receipt_sha256"), str)
            and isinstance(candidate.get("process"), dict))


if __name__ == "__main__":  # pragma: no cover - operator probe, not a gate
    import sys

    if len(sys.argv) < 2:
        print("usage: host_load_receipt.py <receipt.json> [scope subject epoch]")
        raise SystemExit(2)
    args = sys.argv[1:]
    try:
        out = read_load_receipt(args[0],
                                expected_scope=args[1] if len(args) > 1 else None,
                                expected_subject=args[2] if len(args) > 2 else None,
                                expected_epoch=args[3] if len(args) > 3 else None)
    except LoadReceiptRefusal as exc:
        print(json.dumps(exc.as_dict(), ensure_ascii=False, indent=2))
        raise SystemExit(1)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    raise SystemExit(0 if out.get("state") == "OBSERVED" else 1)
