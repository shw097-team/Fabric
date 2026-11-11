# -*- coding: utf-8 -*-
"""D-24 — real readers for the legs whose evidence is a file (`source`, `stage`, `active_epoch`).

D-17 gave the third, fifth and sixth legs typed readers (`OWNER_APPROVAL_RECEIPT@1`,
`HOST_LOAD_RECEIPT@1`, `HGK_CONSUMER_RECEIPT@1`). The first two legs were left with a *label* and no
reader at all, and three defects were measured on `policy_binding.py` because of it:

1. `leg("source", digest=<64 hex>, provenance="FABRIC_POLICY_SOURCE", reader="fabric-policy-repo")`
   was accepted for **any** digest. Nothing opened a file, so a fabricated 64-hex string with no
   artifact anywhere on disk satisfied the first leg;
2. `reader` was free text, so `leg(..., reader="TOTALLY-MADE-UP-READER")` was accepted and
   `build_binding`'s `separate_readers` counted distinct *strings*, not readers that ran;
3. `build_binding` required `stage.digest == source.digest`, so a genuine YAML->JSON stage — the
   whole reason the second leg exists — was refused as `POLICY_SOURCE_STAGE_DRIFT`. The only shape
   that passed was typing the source digest as the stage digest, which is a false pass: it asserts
   the staged bytes are the source bytes.

This module is the reader those legs were missing. Each reader opens one artifact, re-derives a
sha256 from the bytes it read, and refuses rather than downgrades:

* `read_source` — the policy file itself. `digest` must be the sha256 of the bytes on disk.
  Refusals: `POLICY_SOURCE_UNREADABLE`, `POLICY_SOURCE_DIGEST_MISMATCH`.
* `read_stage` — a `FABRIC_POLICY_STAGE@1` document carrying a **producer block**
  `{source_sha256, transform, stage_sha256}` and the transformed `payload`. The staged bytes are the
  canonical JSON serialisation of `payload` (sorted keys, no spaces, UTF-8), so `stage_sha256` is a
  digest of bytes a consumer can re-derive. Refusals: `POLICY_STAGE_UNREADABLE` (not there, not
  JSON, not this schema, no usable producer block) and `POLICY_STAGE_DIGEST_MISMATCH` (declared
  `stage_sha256` is not the payload's, or the caller's expected digest is not).
* `read_active_epoch` — an `ACTIVE_POLICY_POINTER@1` document. It *declares* the active digest; when
  it also names `policy_path`, the bytes at that path are re-hashed and must match.
  Refusals: `POLICY_EPOCH_UNREADABLE`, `POLICY_EPOCH_DIGEST_MISMATCH`.

The fourth leg has a second reader, and it is registered here rather than beside the binding because
it is the same kind of thing: a reader that opens one file and re-derives what it says.

* `fabric-active-epoch-reader` (lane B's `fabric_active_epoch.read_epoch_receipt`) — a signed
  `FABRIC_ACTIVE_EPOCH@1`, whose detached Ed25519 signature is verified over the canonical body and
  whose declared policy digest is re-derived from disk. It raises `EPOCH_*` codes, not the
  `POLICY_*` ones above, and it is the only evidence that can show a *key holder* declared an epoch.

Two readers for one leg is not a collapse: they read different documents and each is recorded as
`evidence="artifact"` or `evidence="receipt"` on its `Reader`, so the binding can require the right
one and can state which kind substantiated the leg. A pointer is evidence a pointer-holder can show;
a signed declaration is evidence only a key holder can show. Neither is a host activation.

What a successful read does **not** mean: that a policy engine loaded these bytes, that the
transform was correct, or that the source is the policy the owner approved. A stage reader proves
"this artifact says it was produced from source X by transform T, and here are the staged bytes" —
X is then checked against the source leg's *verified* digest by the binding, which is the only place
both legs are in hand. This is a reader, not a native load.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Callable, NamedTuple

SCHEMA_STAGE = "FABRIC_POLICY_STAGE@1"
SCHEMA_EPOCH = "ACTIVE_POLICY_POINTER@1"

READER_SOURCE = "fabric-policy-source-reader"
READER_STAGE = "fabric-policy-stage-reader"
READER_EPOCH = "fabric-policy-epoch-reader"
#: Lane B's signed-receipt reader. A second reader for the same leg, reading a different document:
#: `FABRIC_ACTIVE_EPOCH@1` instead of `ACTIVE_POLICY_POINTER@1`. Registered here so the registry stays
#: the one place that answers "which reader may substantiate which leg".
READER_EPOCH_SIGNED = "fabric-active-epoch-reader"
READER_OWNER = "owner-receipt-reader"
READER_LOAD = "host-load-receipt-reader"
READER_ACK = "hgk-consumer-receipt-reader"

CODES = (
    "POLICY_SOURCE_UNREADABLE",
    "POLICY_SOURCE_DIGEST_MISMATCH",
    "POLICY_STAGE_UNREADABLE",
    "POLICY_STAGE_DIGEST_MISMATCH",
    "POLICY_EPOCH_UNREADABLE",
    "POLICY_EPOCH_DIGEST_MISMATCH",
    # Reused from the binding's vocabulary: a stage that declares another source is drift.
    "POLICY_SOURCE_STAGE_DRIFT",
)

_HEX64 = re.compile(r"^[0-9a-f]{64}$")


class LegReaderRefusal(Exception):
    """Typed refusal: an artifact was named but cannot substantiate its leg."""

    def __init__(self, message: str, *, code: str, leg: str | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.leg = leg

    def as_dict(self) -> dict[str, Any]:
        return {"verdict": "REFUSED", "code": self.code, "leg": self.leg, "message": str(self)}


def canonical_bytes(payload: Any) -> bytes:
    """The bytes a stage document is a digest *of*: canonical JSON, UTF-8, no whitespace."""
    return json.dumps(payload, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode()


def _hex64(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    text = value.strip().lower()
    return text if _HEX64.match(text) else None


def _read_bytes(path: str | Path, *, code: str, leg: str, what: str) -> bytes:
    target = Path(path)
    try:
        return target.read_bytes()
    except FileNotFoundError:
        raise LegReaderRefusal(f"no {what} at {target}", code=code, leg=leg) from None
    except OSError as exc:
        raise LegReaderRefusal(f"{what} {target} is not readable: {exc.strerror or exc}",
                               code=code, leg=leg) from None


def _parse_object(raw: bytes, path: str | Path, *, code: str, leg: str, what: str) -> dict:
    try:
        body = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise LegReaderRefusal(f"{what} {path} is not UTF-8 JSON: {exc}", code=code,
                               leg=leg) from None
    if not isinstance(body, dict):
        raise LegReaderRefusal(f"{what} {path} is a {type(body).__name__}, not an object",
                               code=code, leg=leg)
    return body


def read_source(path: str | Path, *, expected_digest: str | None = None) -> dict[str, Any]:
    """Read one policy source file and return the first leg's evidence.

    The digest is the sha256 of the bytes on disk — never the caller's claim. `expected_digest` is
    the caller's claim, and a disagreement is `POLICY_SOURCE_DIGEST_MISMATCH`, not a correction.
    """
    raw = _read_bytes(path, code="POLICY_SOURCE_UNREADABLE", leg="source", what="policy source")
    if not raw:
        raise LegReaderRefusal(
            f"policy source {path} is empty: a zero-byte artifact has a sha256, but it is not a "
            "policy and cannot substantiate the first leg", code="POLICY_SOURCE_UNREADABLE",
            leg="source")
    digest = hashlib.sha256(raw).hexdigest()
    if expected_digest is not None and _hex64(expected_digest) != digest:
        raise LegReaderRefusal(
            f"source digest {str(expected_digest)[:12]} is not the sha256 of {path} "
            f"({digest[:12]}): the digest has no artifact behind it",
            code="POLICY_SOURCE_DIGEST_MISMATCH", leg="source")
    return {
        "state": "OBSERVED",
        "leg": "source",
        "digest": digest,
        "reader": READER_SOURCE,
        "artifact": str(Path(path)),
        "artifact_bytes": len(raw),
        "artifact_sha256": digest,
        "verified": True,
        "note": (f"sha256 re-derived from {len(raw)} bytes at {path}; this proves the bytes exist "
                 "and hash to the digest, not that they are the policy in force"),
    }


def read_stage(path: str | Path, *, expected_digest: str | None = None,
               expected_source_sha256: str | None = None) -> dict[str, Any]:
    """Read one `FABRIC_POLICY_STAGE@1` and return the second leg's evidence.

    The document is a container, not the staged bytes: `payload` is the transformed policy and the
    staged bytes are its canonical JSON serialisation. `producer.stage_sha256` must be that
    payload's digest, and `producer.source_sha256` must be the digest of the artifact the transform
    started from. The leg's digest is the *re-derived* payload digest, so a document cannot declare
    one set of bytes and carry another.
    """
    raw = _read_bytes(path, code="POLICY_STAGE_UNREADABLE", leg="stage", what="stage artifact")
    body = _parse_object(raw, path, code="POLICY_STAGE_UNREADABLE", leg="stage",
                         what="stage artifact")
    if body.get("schema") != SCHEMA_STAGE:
        raise LegReaderRefusal(
            f"stage artifact {path} declares schema {body.get('schema')!r}, expected "
            f"{SCHEMA_STAGE!r}: an untyped JSON blob is not a stage", code="POLICY_STAGE_UNREADABLE",
            leg="stage")
    if "payload" not in body:
        raise LegReaderRefusal(f"stage artifact {path} carries no payload, so it stages no bytes",
                               code="POLICY_STAGE_UNREADABLE", leg="stage")
    producer = body.get("producer")
    if not isinstance(producer, dict):
        raise LegReaderRefusal(
            f"stage artifact {path} carries no producer block, so nothing says which source it was "
            "produced from or by what transform — the stage leg would be a claim with no origin",
            code="POLICY_STAGE_UNREADABLE", leg="stage")
    declared_source = _hex64(producer.get("source_sha256"))
    declared_stage = _hex64(producer.get("stage_sha256"))
    transform = producer.get("transform")
    if declared_source is None:
        raise LegReaderRefusal(
            f"stage artifact {path} producer.source_sha256 is "
            f"{producer.get('source_sha256')!r}, not a sha256 hex digest", code="POLICY_STAGE_UNREADABLE",
            leg="stage")
    if declared_stage is None:
        raise LegReaderRefusal(
            f"stage artifact {path} producer.stage_sha256 is {producer.get('stage_sha256')!r}, not "
            "a sha256 hex digest", code="POLICY_STAGE_UNREADABLE", leg="stage")
    if not isinstance(transform, str) or not transform.strip():
        raise LegReaderRefusal(
            f"stage artifact {path} producer.transform is {transform!r}: a stage that cannot name "
            "its transform cannot be told apart from a copy", code="POLICY_STAGE_UNREADABLE",
            leg="stage")

    staged = canonical_bytes(body["payload"])
    if not staged:
        raise LegReaderRefusal(f"stage artifact {path} stages zero bytes",
                               code="POLICY_STAGE_UNREADABLE", leg="stage")
    digest = hashlib.sha256(staged).hexdigest()
    if declared_stage != digest:
        raise LegReaderRefusal(
            f"stage artifact {path} declares stage_sha256 {declared_stage[:12]} but its payload "
            f"hashes to {digest[:12]}: the document was edited after staging",
            code="POLICY_STAGE_DIGEST_MISMATCH", leg="stage")
    if expected_digest is not None and _hex64(expected_digest) != digest:
        raise LegReaderRefusal(
            f"stage digest {str(expected_digest)[:12]} is not the sha256 of the staged bytes at "
            f"{path} ({digest[:12]})", code="POLICY_STAGE_DIGEST_MISMATCH", leg="stage")
    if expected_source_sha256 is not None and _hex64(expected_source_sha256) != declared_source:
        raise LegReaderRefusal(
            f"stage artifact {path} declares it was produced from source {declared_source[:12]}, "
            f"not from {str(expected_source_sha256)[:12]}",
            code="POLICY_SOURCE_STAGE_DRIFT", leg="stage")

    return {
        "state": "OBSERVED",
        "leg": "stage",
        "digest": digest,
        "reader": READER_STAGE,
        "artifact": str(Path(path)),
        "artifact_bytes": len(raw),
        "artifact_sha256": hashlib.sha256(raw).hexdigest(),
        "stage_bytes": len(staged),
        "stage_sha256": digest,
        "source_sha256": declared_source,
        "transform": transform.strip(),
        "verified": True,
        "note": (f"staged bytes re-derived from the payload ({len(staged)} bytes, canonical JSON); "
                 f"producer declares source {declared_source[:12]} via transform "
                 f"{transform.strip()!r}; whether that source is *this* binding's source is checked "
                 "against the source leg, not here"),
    }


def read_active_epoch(path: str | Path, *, expected_digest: str | None = None) -> dict[str, Any]:
    """Read one `ACTIVE_POLICY_POINTER@1` and return the fourth leg's evidence.

    A pointer declares which digest is active. When it also names `policy_path`, the bytes there are
    re-hashed and must equal the declaration; without a `policy_path` the leg is a declaration and
    the binding's `loaded_digest == active_epoch` check is what ties it to real bytes.
    """
    raw = _read_bytes(path, code="POLICY_EPOCH_UNREADABLE", leg="active_epoch",
                      what="active epoch pointer")
    body = _parse_object(raw, path, code="POLICY_EPOCH_UNREADABLE", leg="active_epoch",
                         what="active epoch pointer")
    if body.get("schema") != SCHEMA_EPOCH:
        raise LegReaderRefusal(
            f"epoch pointer {path} declares schema {body.get('schema')!r}, expected "
            f"{SCHEMA_EPOCH!r}", code="POLICY_EPOCH_UNREADABLE", leg="active_epoch")
    digest = _hex64(body.get("digest"))
    if digest is None:
        raise LegReaderRefusal(
            f"epoch pointer {path} digest is {body.get('digest')!r}, not a sha256 hex digest",
            code="POLICY_EPOCH_UNREADABLE", leg="active_epoch")

    pointer = Path(path)
    declared_policy = body.get("policy_path")
    checked_bytes = False
    if isinstance(declared_policy, str) and declared_policy.strip():
        target = Path(declared_policy)
        if not target.is_absolute():
            target = pointer.parent / target
        policy_raw = _read_bytes(target, code="POLICY_EPOCH_UNREADABLE", leg="active_epoch",
                                 what="policy named by the epoch pointer")
        observed = hashlib.sha256(policy_raw).hexdigest()
        if observed != digest:
            raise LegReaderRefusal(
                f"epoch pointer {path} declares {digest[:12]} but {target} hashes to "
                f"{observed[:12]}", code="POLICY_EPOCH_DIGEST_MISMATCH", leg="active_epoch")
        checked_bytes = True
    if expected_digest is not None and _hex64(expected_digest) != digest:
        raise LegReaderRefusal(
            f"epoch digest {str(expected_digest)[:12]} is not the digest {path} declares "
            f"({digest[:12]})", code="POLICY_EPOCH_DIGEST_MISMATCH", leg="active_epoch")

    return {
        "state": "OBSERVED",
        "leg": "active_epoch",
        "digest": digest,
        "reader": READER_EPOCH,
        "artifact": str(pointer),
        "artifact_bytes": len(raw),
        "artifact_sha256": hashlib.sha256(raw).hexdigest(),
        "scope": body.get("scope"),
        "epoch": body.get("epoch"),
        "digest_verified_from_bytes": checked_bytes,
        "verified": True,
        "note": ("epoch pointer read and its declared digest taken as the active digest"
                 + ("; the named policy file was re-hashed and matched" if checked_bytes
                    else "; the pointer names no policy file, so only the declaration was read")),
    }


class Reader(NamedTuple):
    """One registered reader. `leg` is the leg this reader may substantiate, and nothing else.

    `evidence` says what kind of thing the reader opens, because the two kinds are not
    interchangeable: an `"artifact"` reader re-derives a digest from bytes the caller names, while a
    `"receipt"` reader opens a document a producer signed and verifies it against a pinned key. A leg
    records which kind substantiated it, so a caller can tell a pointer from a signed declaration.
    """

    name: str
    leg: str
    read: Callable[..., dict[str, Any]]
    opens_artifact: bool = True
    evidence: str = "artifact"


def _read_owner_receipt(path: Any, **kw: Any) -> dict[str, Any]:
    import owner_approval_receipt as _reader  # local: keeps this module stdlib-only at import
    return _reader.read_owner_receipt(path, **kw)


def _read_load_receipt(path: Any, **kw: Any) -> dict[str, Any]:
    import host_load_receipt as _reader
    return _reader.read_load_receipt(path, **kw)


def _read_consumer_receipt(path: Any, **kw: Any) -> dict[str, Any]:
    import hgk_consumer_receipt as _reader
    return _reader.load_receipt(path, **kw)


def _read_epoch_receipt(path: Any, **kw: Any) -> dict[str, Any]:
    """Lane B's signed `FABRIC_ACTIVE_EPOCH@1` reader, with its refusals in this module's vocabulary.

    The code is carried through unchanged (`EPOCH_*`): the caller's own code is the honest one, and
    re-labelling "expired" as a generic provenance error would hide the reason. Only the exception
    *type* changes, so a caller of the registry can catch one class.
    """
    import fabric_active_epoch as _reader
    try:
        return _reader.read_epoch_receipt(path, **kw)
    except _reader.EpochReceiptRefusal as exc:
        raise LegReaderRefusal(f"active-epoch receipt {path} refused ({exc.code}): {exc}",
                               code=exc.code, leg="active_epoch") from None


#: Every reader this module registers, in leg order. `READERS` must be exactly this set: a name that
#: is not here is not a reader, and `policy_binding.leg()` refuses it (`POLICY_LEG_READER_UNKNOWN`).
READER_NAMES = (READER_SOURCE, READER_STAGE, READER_EPOCH, READER_EPOCH_SIGNED,
                READER_OWNER, READER_LOAD, READER_ACK)

#: The module's real readers. `policy_binding.leg()` refuses a name that is not a key here, so
#: `separate_readers` counts readers that exist rather than strings a caller typed.
READERS: dict[str, Reader] = {
    READER_SOURCE: Reader(READER_SOURCE, "source", read_source, True, "artifact"),
    READER_STAGE: Reader(READER_STAGE, "stage", read_stage, True, "artifact"),
    READER_EPOCH: Reader(READER_EPOCH, "active_epoch", read_active_epoch, True, "artifact"),
    READER_EPOCH_SIGNED: Reader(READER_EPOCH_SIGNED, "active_epoch", _read_epoch_receipt, True,
                                "receipt"),
    READER_OWNER: Reader(READER_OWNER, "owner_approved", _read_owner_receipt, True, "receipt"),
    READER_LOAD: Reader(READER_LOAD, "loaded_digest", _read_load_receipt, True, "receipt"),
    READER_ACK: Reader(READER_ACK, "consumer_ack", _read_consumer_receipt, True, "receipt"),
}


def reader_names() -> tuple[str, ...]:
    return tuple(READERS)


def is_registered(name: Any) -> bool:
    return isinstance(name, str) and name in READERS


if __name__ == "__main__":  # pragma: no cover - operator probe, not a gate
    import sys

    if len(sys.argv) < 3:
        print("usage: policy_leg_readers.py <source|stage|epoch> <path> [expected-digest]")
        raise SystemExit(2)
    which, target = sys.argv[1], sys.argv[2]
    expected = sys.argv[3] if len(sys.argv) > 3 else None
    fn = {"source": read_source, "stage": read_stage, "epoch": read_active_epoch}.get(which)
    if fn is None:
        print(f"unknown artifact kind {which!r}")
        raise SystemExit(2)
    try:
        print(json.dumps(fn(target, expected_digest=expected), ensure_ascii=False, indent=2))
    except LegReaderRefusal as exc:
        print(json.dumps(exc.as_dict(), ensure_ascii=False, indent=2))
        raise SystemExit(1)
    raise SystemExit(0)
