# -*- coding: utf-8 -*-
"""D-24 — `FABRIC_ACTIVE_EPOCH@1`: the artifact the fourth leg never had.

Measured on merged `main` (`ee19049`): `FABRIC_ACTIVE_EPOCH` had **zero occurrences** in the
repository. `policy_binding.LEG_PROVENANCE["active_epoch"]` named `ACTIVE_POLICY_POINTER` and
`EPOCH_PROMOTION_RECEIPT`, and no function anywhere opened either — so the fourth leg was a
caller-typed label, and the only thing it had to satisfy was digest equality with the loaded bytes
(which the caller also supplied). That is the same defect D-17 closed for legs three, five and six,
one leg over: **a provenance label with no reader is a forgery hole**.

This module is both ends of the missing artifact:

* `produce_epoch(...)` / `python fabric_active_epoch.py produce ...` — signs one
  `FABRIC_ACTIVE_EPOCH@1` with an Ed25519 key held outside the repository tree, then re-reads its
  own output with the reader below and refuses to publish a document that does not verify.
* `read_epoch_receipt(...)` — opens one document, re-derives the digest of the policy bytes from
  disk, checks the detached signature over the canonical body, and refuses:
  an expired window, a body edited after signing, an unsigned document, a key outside the caller's
  registry, a policy digest that disagrees with the bytes or with the digest the caller expects, and
  an epoch that is not strictly greater than the previously loaded epoch.

The document says `state=EPOCH_DECLARED` and `claim_ceiling=EPOCH_DECLARED_NOT_HOST_ACTIVE` on
purpose. What a verified read proves is: *a holder of this key declared that this policy digest is
the active epoch for this scope at this time*. It does **not** prove the policy engine on any host
loaded it, that the key belongs to the Policy Owner, or that the epoch is in force. `previous_epoch`
is self-declared by the producer; a verifier that has a prior epoch must pass it as
`previous_epoch=` so the comparison is against something the document cannot choose.

No daemon, no queue, no scheduler, no state: one file in, one file out.
"""
from __future__ import annotations

import base64
import binascii
import datetime as _dt
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any, NoReturn, TypeGuard

SCHEMA = "FABRIC_ACTIVE_EPOCH@1"
READER = "fabric-active-epoch-reader"
LEG = "active_epoch"
PROVENANCE = "FABRIC_ACTIVE_EPOCH"
EVIDENCE_CLASS = "HOST_RAW"
STATE_DECLARED = "EPOCH_DECLARED"
CLAIM_CEILING = "EPOCH_DECLARED_NOT_HOST_ACTIVE"
ALGS = ("ED25519",)

#: Reader codes first, then the producer's. Both sides print the same vocabulary.
CODES = (
    "EPOCH_UNREADABLE",
    "EPOCH_MALFORMED",
    "EPOCH_SCHEMA_MISMATCH",
    "EPOCH_STATE_NOT_DECLARED",
    "EPOCH_SCOPE_MISMATCH",
    "EPOCH_SUBJECT_MISMATCH",
    "EPOCH_INVALID",
    "EPOCH_EPOCH_MISMATCH",
    "EPOCH_REGRESSION",
    "EPOCH_TIME_INVALID",
    "EPOCH_EXPIRED",
    "EPOCH_NO_SIGNER",
    "EPOCH_KEY_UNUSABLE",
    "EPOCH_KEY_UNTRUSTED",
    "EPOCH_VERIFIER_UNAVAILABLE",
    "EPOCH_SIGNATURE_INVALID",
    "EPOCH_POLICY_UNREADABLE",
    "EPOCH_DIGEST_MISMATCH",
    # producer-side refusals: a signing tool that cannot satisfy its own reader publishes nothing
    "EPOCH_SIGN_EPOCH_INVALID",
    "EPOCH_SIGN_EPOCH_NOT_GREATER",
    "EPOCH_SIGN_TTL_OUT_OF_BOUNDS",
    "EPOCH_SIGN_POLICY_UNREADABLE",
    "EPOCH_SIGN_KEY_MISSING",
    "EPOCH_SIGN_KEY_INSIDE_REPO",
    "EPOCH_SIGN_KEY_UNUSABLE",
    "EPOCH_SIGN_TARGET_EXISTS",
    "EPOCH_SIGN_SELF_CHECK_FAILED",
)

_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_SKEW_S = 300
#: A window shorter than a minute cannot be observed, and one longer than 30 days is not a window.
TTL_MIN_S = 60
TTL_MAX_S = 30 * 24 * 3600


class EpochReceiptRefusal(Exception):
    """Typed refusal: an epoch document was found (or requested) but cannot substantiate the leg."""

    def __init__(self, message: str, *, code: str, leg: str = LEG) -> None:
        super().__init__(message)
        self.code = code
        self.leg = leg

    def as_dict(self) -> dict[str, Any]:
        return {"verdict": "REFUSED", "code": self.code, "leg": self.leg, "message": str(self)}


def _not_observed(path: Path, code: str, reason: str, **expected: Any) -> dict[str, Any]:
    """No document was read. Shaped deliberately unlike a leg: no digest, provenance or reader."""
    return {"state": "NOT_OBSERVED", "code": code, "reason": reason, "leg": None, "kind": LEG,
            "path": str(path), "evidence_class": "NOT_OBSERVED", "expected": expected}


def _canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def canonical_body(body: dict[str, Any]) -> bytes:
    """The exact bytes the signature covers: the document minus its `signature` block."""
    return _canonical({k: v for k, v in body.items() if k != "signature"})


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


def _is_int(value: Any) -> TypeGuard[int]:
    return isinstance(value, int) and not isinstance(value, bool)


def verify_detached_signature(*, alg: Any, public_key_b64: Any, signature_b64: Any,
                              message: bytes) -> bool:
    """True when the detached signature verifies. Ed25519 only; a missing verifier refuses."""
    if not isinstance(alg, str) or alg.strip().upper() not in ALGS:
        raise EpochReceiptRefusal(
            f"signature alg is {alg!r}; this reader verifies {list(ALGS)} and nothing else",
            code="EPOCH_KEY_UNUSABLE")
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    except ImportError:
        raise EpochReceiptRefusal(
            "the Ed25519 verifier (package `cryptography`) is not importable on this host, so no "
            "signature can be checked and no epoch can be accepted",
            code="EPOCH_VERIFIER_UNAVAILABLE") from None
    raw_key = _b64(public_key_b64)
    raw_sig = _b64(signature_b64)
    if raw_key is None or len(raw_key) != 32:
        raise EpochReceiptRefusal(
            "the key the document names is not 32 bytes of base64-encoded Ed25519 public key",
            code="EPOCH_KEY_UNUSABLE")
    if raw_sig is None or len(raw_sig) != 64:
        raise EpochReceiptRefusal("the detached signature is not 64 bytes of base64",
                                  code="EPOCH_SIGNATURE_INVALID")
    try:
        public_key = Ed25519PublicKey.from_public_bytes(raw_key)
    except ValueError:
        raise EpochReceiptRefusal("the key the document names is not a valid Ed25519 public key",
                                  code="EPOCH_KEY_UNUSABLE") from None
    try:
        public_key.verify(raw_sig, message)
    except InvalidSignature:
        return False
    return True


def _resolve_policy(receipt_path: Path, body: dict[str, Any],
                    policy_path: str | Path | None) -> Path:
    if policy_path is not None:
        return Path(policy_path)
    policy = body.get("policy")
    declared = policy.get("path") if isinstance(policy, dict) else None
    if not isinstance(declared, str) or not declared.strip():
        raise EpochReceiptRefusal(
            "the document names no policy.path, so the epoch's bytes cannot be re-read",
            code="EPOCH_POLICY_UNREADABLE")
    candidate = Path(declared)
    return candidate if candidate.is_absolute() else (receipt_path.parent / candidate)


def read_epoch_receipt(path: str | Path, *, expected_scope: str | None = None,
                       expected_subject: str | None = None,
                       expected_epoch: int | str | None = None,
                       previous_epoch: int | str | None = None,
                       policy_path: str | Path | None = None,
                       expected_policy_sha256: str | None = None,
                       trusted_key_ids: set[str] | frozenset[str] | None = None,
                       now: _dt.datetime | None = None) -> dict[str, Any]:
    """Read and verify one `FABRIC_ACTIVE_EPOCH@1`.

    Returns the fourth leg (`state="OBSERVED"`) or a `NOT_OBSERVED` marker when the file is absent
    or unreadable; every other defect raises `EpochReceiptRefusal` with one of `CODES`.

    `previous_epoch` is the epoch the caller last loaded. When it is supplied the document's epoch
    must be *strictly greater*; when it is not, the document's own `previous_epoch` field is used,
    and that field is self-declared — which is why a caller who has a prior epoch must pass it.
    `expected_policy_sha256` pins the digest the caller already loaded, so an epoch declaration for
    other bytes is refused rather than replacing the digest the binding is about.
    """
    receipt_path = Path(path)
    now = now or _dt.datetime.now(_dt.timezone.utc)
    expected = {"scope": expected_scope, "subject": expected_subject, "epoch": expected_epoch,
                "previous_epoch": previous_epoch, "policy_sha256": expected_policy_sha256}

    try:
        raw_bytes = receipt_path.read_bytes()
    except FileNotFoundError:
        return _not_observed(receipt_path, "EPOCH_UNREADABLE",
                             f"no active-epoch receipt at {receipt_path}", **expected)
    except OSError as exc:
        return _not_observed(receipt_path, "EPOCH_UNREADABLE",
                             f"active-epoch receipt {receipt_path} is not readable: "
                             f"{exc.strerror or exc}", **expected)

    try:
        body = json.loads(raw_bytes.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise EpochReceiptRefusal(f"{receipt_path} is not UTF-8 JSON: {exc}",
                                  code="EPOCH_MALFORMED") from None
    if not isinstance(body, dict):
        raise EpochReceiptRefusal(f"{receipt_path} is a {type(body).__name__}, not an object",
                                  code="EPOCH_MALFORMED")

    if body.get("schema") != SCHEMA:
        raise EpochReceiptRefusal(
            f"schema is {body.get('schema')!r}; this reader accepts only {SCHEMA!r}",
            code="EPOCH_SCHEMA_MISMATCH")
    if body.get("state") != STATE_DECLARED:
        raise EpochReceiptRefusal(
            f"state is {body.get('state')!r}; only {STATE_DECLARED} declares an epoch",
            code="EPOCH_STATE_NOT_DECLARED")
    if expected_scope is not None and body.get("scope") != expected_scope:
        raise EpochReceiptRefusal(
            f"scope is {body.get('scope')!r}, expected {expected_scope!r}",
            code="EPOCH_SCOPE_MISMATCH")
    if expected_subject is not None and body.get("subject") != expected_subject:
        raise EpochReceiptRefusal(
            f"subject is {body.get('subject')!r}, expected {expected_subject!r}",
            code="EPOCH_SUBJECT_MISMATCH")

    epoch = body.get("epoch")
    if not _is_int(epoch) or epoch <= 0:
        raise EpochReceiptRefusal(
            f"epoch is {epoch!r} ({type(epoch).__name__}), not a positive integer",
            code="EPOCH_INVALID")
    if expected_epoch is not None and str(epoch) != str(expected_epoch):
        raise EpochReceiptRefusal(
            f"epoch is {epoch!r}, expected {expected_epoch!r}", code="EPOCH_EPOCH_MISMATCH")

    declared_previous = body.get("previous_epoch")
    if declared_previous is not None and not _is_int(declared_previous):
        raise EpochReceiptRefusal(
            f"previous_epoch is {declared_previous!r}, not an integer or null",
            code="EPOCH_INVALID")
    if previous_epoch is not None and not _is_int(previous_epoch):
        raise EpochReceiptRefusal(
            f"the caller's previous_epoch is {previous_epoch!r}, not an integer",
            code="EPOCH_INVALID")
    if previous_epoch is not None and epoch <= previous_epoch:
        raise EpochReceiptRefusal(
            f"epoch {epoch} is not strictly greater than the previously loaded epoch "
            f"{previous_epoch}: an epoch never moves backwards, so this declaration is stale",
            code="EPOCH_REGRESSION")
    if declared_previous is not None and epoch <= declared_previous:
        raise EpochReceiptRefusal(
            f"epoch {epoch} is not strictly greater than the document's own previous_epoch "
            f"{declared_previous}", code="EPOCH_REGRESSION")

    issued = _parse_utc(body.get("issued_at"))
    expires = _parse_utc(body.get("expires_at"))
    if issued is None:
        raise EpochReceiptRefusal(
            f"issued_at is {body.get('issued_at')!r}, not a timezone-aware ISO-8601 instant",
            code="EPOCH_TIME_INVALID")
    if expires is None:
        raise EpochReceiptRefusal(
            f"expires_at is {body.get('expires_at')!r}, not a timezone-aware ISO-8601 instant",
            code="EPOCH_TIME_INVALID")
    if expires <= issued:
        raise EpochReceiptRefusal(
            f"expires_at {body.get('expires_at')!r} does not follow issued_at "
            f"{body.get('issued_at')!r}", code="EPOCH_TIME_INVALID")
    if issued > now + _dt.timedelta(seconds=_SKEW_S):
        raise EpochReceiptRefusal(f"issued_at {body.get('issued_at')!r} is in the future",
                                  code="EPOCH_TIME_INVALID")
    if expires <= now:
        raise EpochReceiptRefusal(
            f"the epoch declaration expired at {body.get('expires_at')!r}; an expired declaration "
            "names no active epoch", code="EPOCH_EXPIRED")

    signature = body.get("signature")
    if not isinstance(signature, dict):
        raise EpochReceiptRefusal(
            "the document carries no detached signature block, so nothing shows a key holder "
            "declared this epoch", code="EPOCH_NO_SIGNER")
    key_id = signature.get("key_id")
    if not isinstance(key_id, str) or not key_id.strip():
        raise EpochReceiptRefusal("signature.key_id is missing or empty", code="EPOCH_NO_SIGNER")
    if not isinstance(signature.get("sig_b64"), str) or not signature["sig_b64"].strip():
        raise EpochReceiptRefusal("signature.sig_b64 is missing or empty", code="EPOCH_NO_SIGNER")
    declared_body_sha = signature.get("signed_body_sha256")
    if not isinstance(declared_body_sha, str) or not _HEX64.match(declared_body_sha.strip().lower()):
        raise EpochReceiptRefusal(
            f"signature.signed_body_sha256 is {declared_body_sha!r}, not a sha256 hex digest, so "
            "the document cannot show its body is the body that was signed",
            code="EPOCH_NO_SIGNER")
    key = body.get("key")
    if not isinstance(key, dict) or not isinstance(key.get("public_key_b64"), str):
        raise EpochReceiptRefusal(
            "the document names no key material to verify the signature against",
            code="EPOCH_KEY_UNUSABLE")
    if key.get("key_id") != key_id:
        raise EpochReceiptRefusal(
            f"signature.key_id {key_id!r} does not match key.key_id {key.get('key_id')!r}: the "
            "signature is not over the key the document names", code="EPOCH_KEY_UNUSABLE")

    key_trusted = False
    if trusted_key_ids is not None:
        if key_id.strip() not in {str(item) for item in trusted_key_ids}:
            raise EpochReceiptRefusal(
                f"key_id {key_id!r} is not in the caller's trusted key registry: a document that "
                "names its own key cannot establish key provenance by itself",
                code="EPOCH_KEY_UNTRUSTED")
        key_trusted = True

    message = canonical_body(body)
    observed_body_sha = hashlib.sha256(message).hexdigest()
    if declared_body_sha.strip().lower() != observed_body_sha:
        raise EpochReceiptRefusal(
            "the body was edited after signing (signed_body_sha256 "
            f"{declared_body_sha[:12]} != {observed_body_sha[:12]})",
            code="EPOCH_SIGNATURE_INVALID")
    ok = verify_detached_signature(alg=signature.get("alg"), public_key_b64=key.get("public_key_b64"),
                                   signature_b64=signature.get("sig_b64"), message=message)
    if ok is not True:
        raise EpochReceiptRefusal(
            f"the detached signature does not verify against key_id {key_id!r}",
            code="EPOCH_SIGNATURE_INVALID")

    policy = body.get("policy")
    declared_digest = policy.get("sha256") if isinstance(policy, dict) else None
    if not isinstance(declared_digest, str) or not _HEX64.match(declared_digest.strip().lower()):
        raise EpochReceiptRefusal(
            f"policy.sha256 is {declared_digest!r}, not a sha256 hex digest",
            code="EPOCH_DIGEST_MISMATCH")
    policy_file = _resolve_policy(receipt_path, body, policy_path)
    try:
        policy_bytes = policy_file.read_bytes()
    except OSError as exc:
        raise EpochReceiptRefusal(
            f"epoch bytes {policy_file} are not readable: {exc.strerror or exc}",
            code="EPOCH_POLICY_UNREADABLE") from None
    observed_digest = hashlib.sha256(policy_bytes).hexdigest()
    if observed_digest != declared_digest.strip().lower():
        raise EpochReceiptRefusal(
            "policy.sha256 does not match the bytes on disk "
            f"({declared_digest[:12]} != {observed_digest[:12]})",
            code="EPOCH_DIGEST_MISMATCH")
    if expected_policy_sha256 is not None \
            and observed_digest != str(expected_policy_sha256).strip().lower():
        raise EpochReceiptRefusal(
            "the epoch declares a different policy than the one this binding is about "
            f"({observed_digest[:12]} != {str(expected_policy_sha256)[:12]})",
            code="EPOCH_DIGEST_MISMATCH")

    return {
        "state": "OBSERVED",
        "leg": LEG,
        "digest": observed_digest,
        "provenance": PROVENANCE,
        "reader": READER,
        "scope": body.get("scope"),
        "epoch": epoch,
        "previous_epoch": declared_previous,
        "observed_at": body.get("issued_at"),
        "evidence_class": EVIDENCE_CLASS,
        "subject": body.get("subject"),
        "key_id": key_id.strip(),
        "key_trusted": key_trusted,
        "issued_at": issued.isoformat(),
        "expires_at": expires.isoformat(),
        "policy_path": str(policy_file),
        "policy_bytes": len(policy_bytes),
        "receipt_sha256": hashlib.sha256(raw_bytes).hexdigest(),
        "receipt_path": str(receipt_path),
        "verified": True,
        "note": ("detached signature verified against the key the document names, over the bytes "
                 "this reader re-hashed; the declaration names an epoch for a digest, never a host "
                 f"load. Key provenance is {'pinned' if key_trusted else 'NOT established (unpinned key)'}"),
    }


def is_verified_epoch_leg(candidate: Any) -> bool:
    """True only for a dict this reader produced for the fourth leg (structural, re-checkable)."""
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
            and _is_int(candidate.get("epoch"))
            and isinstance(candidate.get("receipt_sha256"), str)
            and isinstance(candidate.get("key_id"), str))


# --- producer ------------------------------------------------------------------------------------

def repo_root(start: Path | None = None) -> Path | None:
    """The enclosing repository root, found by walking up for a `.git` entry (dir or worktree file)."""
    here = (start or Path(__file__)).resolve()
    for candidate in (here, *here.parents):
        if (candidate / ".git").exists():
            return candidate
    return None


def _key_outside_repo(key_path: Path, root: Path | None) -> None:
    """Refuse a private key that lives inside the repository tree.

    A signing key in the tree is a key the repository can leak, review-diff and archive; the
    artifact it produces would then look like evidence while its secret is source. This is a
    refusal, not a warning.
    """
    if root is None:
        return
    try:
        key_path.resolve().relative_to(root.resolve())
    except ValueError:
        return
    raise EpochReceiptRefusal(
        f"the signing key {key_path} is inside the repository tree {root}; a private key in the "
        "tree is a key the repository can leak, so this producer refuses to use it",
        code="EPOCH_SIGN_KEY_INSIDE_REPO")


def _load_signing_key(key_file: str | Path, root: Path | None) -> Any:
    """Load one Ed25519 private key from raw seed, hex seed, base64 seed or PKCS8 PEM."""
    key_path = Path(key_file)
    _key_outside_repo(key_path, root)
    if not key_path.exists():
        raise EpochReceiptRefusal(
            f"no signing key at {key_path}; this producer holds no key of its own and will not "
            "invent one", code="EPOCH_SIGN_KEY_MISSING")
    try:
        raw = key_path.read_bytes()
    except OSError as exc:
        raise EpochReceiptRefusal(f"signing key {key_path} is not readable: {exc.strerror or exc}",
                                  code="EPOCH_SIGN_KEY_UNUSABLE") from None
    try:
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    except ImportError:
        raise EpochReceiptRefusal(
            "the Ed25519 signer (package `cryptography`) is not importable on this host, so this "
            "producer cannot sign anything", code="EPOCH_VERIFIER_UNAVAILABLE") from None

    seed: bytes | None = None
    if raw.lstrip().startswith(b"-----BEGIN"):
        try:
            loaded = serialization.load_pem_private_key(raw, password=None)
        except (ValueError, TypeError) as exc:
            raise EpochReceiptRefusal(f"signing key {key_path} is not a usable PKCS8 key: {exc}",
                                      code="EPOCH_SIGN_KEY_UNUSABLE") from None
        if not isinstance(loaded, Ed25519PrivateKey):
            raise EpochReceiptRefusal(
                f"signing key {key_path} is a {type(loaded).__name__}, not an Ed25519 key",
                code="EPOCH_SIGN_KEY_UNUSABLE")
        return loaded
    text = raw.strip()
    if len(text) == 64 and re.fullmatch(rb"[0-9a-fA-F]{64}", text):
        seed = bytes.fromhex(text.decode())
    else:
        decoded = _b64(text.decode("ascii", "ignore"))
        if decoded is not None and len(decoded) == 32:
            seed = decoded
        elif len(raw) == 32:
            seed = raw
    if seed is None:
        raise EpochReceiptRefusal(
            f"signing key {key_path} is neither a 32-byte Ed25519 seed (raw, hex or base64) nor a "
            "PKCS8 PEM key", code="EPOCH_SIGN_KEY_UNUSABLE")
    return Ed25519PrivateKey.from_private_bytes(seed)


def _public_b64(private_key: Any) -> str:
    from cryptography.hazmat.primitives import serialization
    raw = private_key.public_key().public_bytes(encoding=serialization.Encoding.Raw,
                                                format=serialization.PublicFormat.Raw)
    return base64.b64encode(raw).decode()


def produce_epoch(*, policy: str | Path, epoch: int, scope: str, key_file: str | Path, key_id: str,
                  out: str | Path, subject: str = "WP-FHS-02", ttl_minutes: int = 60,
                  previous_epoch: int | None = None, policy_ref: str | None = None,
                  repo_root_override: Path | None = None, now: _dt.datetime | None = None,
                  overwrite: bool = False) -> dict[str, Any]:
    """Sign one `FABRIC_ACTIVE_EPOCH@1`, re-read it, and publish it only if it verifies.

    The document is written to a sibling temporary file, read back through `read_epoch_receipt`,
    and only then renamed into place: a producer that cannot satisfy its own reader leaves no
    artifact behind. `policy.path` is recorded absolute so the reader resolves the same bytes
    regardless of where the receipt is moved; `policy_ref` is the human name of the policy.
    """
    now = now or _dt.datetime.now(_dt.timezone.utc)
    if not _is_int(epoch) or epoch <= 0:
        raise EpochReceiptRefusal(f"epoch is {epoch!r}, not a positive integer",
                                  code="EPOCH_SIGN_EPOCH_INVALID")
    if previous_epoch is not None:
        if not _is_int(previous_epoch) or previous_epoch < 0:
            raise EpochReceiptRefusal(
                f"previous_epoch is {previous_epoch!r}, not a non-negative integer",
                code="EPOCH_SIGN_EPOCH_INVALID")
        if epoch <= previous_epoch:
            raise EpochReceiptRefusal(
                f"epoch {epoch} is not strictly greater than the previously loaded epoch "
                f"{previous_epoch}; a producer may not issue a stale epoch",
                code="EPOCH_SIGN_EPOCH_NOT_GREATER")
    ttl_s = None
    if _is_int(ttl_minutes):
        ttl_s = ttl_minutes * 60
    if ttl_s is None or not (TTL_MIN_S <= ttl_s <= TTL_MAX_S):
        raise EpochReceiptRefusal(
            f"ttl_minutes is {ttl_minutes!r}; the window must be between "
            f"{TTL_MIN_S // 60} and {TTL_MAX_S // 60} minutes", code="EPOCH_SIGN_TTL_OUT_OF_BOUNDS")
    if not isinstance(scope, str) or not scope.strip():
        raise EpochReceiptRefusal("scope is empty; an epoch declares a scope", code="EPOCH_INVALID")
    if not isinstance(subject, str) or not subject.strip():
        raise EpochReceiptRefusal("subject is empty", code="EPOCH_INVALID")
    if not isinstance(key_id, str) or not key_id.strip():
        raise EpochReceiptRefusal("key_id is empty; an epoch declaration names its signing key",
                                  code="EPOCH_KEY_UNUSABLE")

    policy_file = Path(policy)
    try:
        policy_bytes = policy_file.read_bytes()
    except OSError as exc:
        raise EpochReceiptRefusal(
            f"policy bytes {policy_file} are not readable: {exc.strerror or exc}",
            code="EPOCH_SIGN_POLICY_UNREADABLE") from None

    private_key = _load_signing_key(key_file, repo_root_override if repo_root_override is not None
                                    else repo_root())
    public_b64 = _public_b64(private_key)

    issued = now.astimezone(_dt.timezone.utc)
    expires = issued + _dt.timedelta(seconds=ttl_s)
    body: dict[str, Any] = {
        "schema": SCHEMA,
        "kind": "FABRIC_ACTIVE_EPOCH",
        "state": STATE_DECLARED,
        "claim_ceiling": CLAIM_CEILING,
        "subject": subject.strip(),
        "scope": scope.strip(),
        "epoch": epoch,
        "previous_epoch": previous_epoch,
        "policy": {"path": str(policy_file.resolve()),
                   "ref": policy_ref or policy_file.name,
                   "sha256": hashlib.sha256(policy_bytes).hexdigest(),
                   "bytes": len(policy_bytes)},
        "issued_at": issued.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "expires_at": expires.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "key": {"key_id": key_id.strip(), "alg": "ED25519", "public_key_b64": public_b64},
        # Self-declared: this names the tool, not an OS process. Unlike HOST_LOAD_RECEIPT@1 there is
        # no pid claim here, because a declaration does not need to prove which process wrote it —
        # the signature is what binds the body.
        "producer": {"tool": "fabric_active_epoch.produce_epoch", "version": "1",
                     "generated_at": issued.strftime("%Y-%m-%dT%H:%M:%SZ")},
    }
    message = canonical_body(body)
    body["signature"] = {
        "key_id": key_id.strip(),
        "alg": "ED25519",
        "sig_b64": base64.b64encode(private_key.sign(message)).decode(),
        "signed_body_sha256": hashlib.sha256(message).hexdigest(),
    }

    out_path = Path(out)
    if out_path.exists() and not overwrite:
        raise EpochReceiptRefusal(
            f"{out_path} already exists; a producer does not overwrite an epoch declaration "
            "(pass overwrite=True deliberately)", code="EPOCH_SIGN_TARGET_EXISTS")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = out_path.with_name(out_path.name + ".tmp")
    tmp_path.write_text(json.dumps(body, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    try:
        reread = read_epoch_receipt(tmp_path, expected_scope=body["scope"],
                                    expected_subject=body["subject"], expected_epoch=epoch,
                                    previous_epoch=previous_epoch, now=now)
    except EpochReceiptRefusal as exc:
        tmp_path.unlink(missing_ok=True)
        raise EpochReceiptRefusal(
            f"the produced declaration does not satisfy this module's own reader ({exc.code}): "
            f"{exc}", code="EPOCH_SIGN_SELF_CHECK_FAILED") from None
    if reread.get("state") != "OBSERVED":
        tmp_path.unlink(missing_ok=True)
        raise EpochReceiptRefusal(
            f"the produced declaration did not read back ({reread.get('code')})",
            code="EPOCH_SIGN_SELF_CHECK_FAILED")
    tmp_path.replace(out_path)
    return {"state": "PRODUCED", "path": str(out_path), "epoch": epoch,
            "policy_sha256": body["policy"]["sha256"], "key_id": body["key"]["key_id"],
            "issued_at": body["issued_at"], "expires_at": body["expires_at"],
            "receipt_sha256": reread["receipt_sha256"],
            "claim_ceiling": CLAIM_CEILING,
            "note": ("signed and re-read by this module; the signature proves a key holder "
                     "declared the epoch, never that a host loaded the policy")}


def _main(argv: list[str]) -> int:  # pragma: no cover - operator CLI, exercised via subprocess
    import argparse

    parser = argparse.ArgumentParser(description="produce or read a FABRIC_ACTIVE_EPOCH@1")
    sub = parser.add_subparsers(dest="cmd", required=True)

    prod = sub.add_parser("produce", help="sign one epoch declaration")
    prod.add_argument("--policy", required=True)
    prod.add_argument("--epoch", type=int, required=True)
    prod.add_argument("--scope", required=True)
    prod.add_argument("--subject", default="WP-FHS-02")
    prod.add_argument("--key-file", required=True)
    prod.add_argument("--key-id", required=True)
    prod.add_argument("--out", required=True)
    prod.add_argument("--ttl-minutes", type=int, default=60)
    prod.add_argument("--previous-epoch", type=int, default=None)
    prod.add_argument("--overwrite", action="store_true")

    read = sub.add_parser("read", help="verify one epoch declaration")
    read.add_argument("path")
    read.add_argument("--scope", default=None)
    read.add_argument("--subject", default=None)
    read.add_argument("--epoch", type=int, default=None)
    read.add_argument("--previous-epoch", type=int, default=None)
    read.add_argument("--policy-sha256", default=None)
    read.add_argument("--trusted-key-id", action="append", default=None)

    args = parser.parse_args(argv)
    try:
        if args.cmd == "produce":
            out = produce_epoch(policy=args.policy, epoch=args.epoch, scope=args.scope,
                                subject=args.subject, key_file=args.key_file, key_id=args.key_id,
                                out=args.out, ttl_minutes=args.ttl_minutes,
                                previous_epoch=args.previous_epoch, overwrite=args.overwrite)
            print(json.dumps(out, ensure_ascii=False, indent=2))
            return 0
        out = read_epoch_receipt(args.path, expected_scope=args.scope,
                                 expected_subject=args.subject, expected_epoch=args.epoch,
                                 previous_epoch=args.previous_epoch,
                                 expected_policy_sha256=args.policy_sha256,
                                 trusted_key_ids=(set(args.trusted_key_id)
                                                  if args.trusted_key_id else None))
    except EpochReceiptRefusal as exc:
        print(json.dumps(exc.as_dict(), ensure_ascii=False, indent=2))
        return 1
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out.get("state") == "OBSERVED" else 1


if __name__ == "__main__":  # pragma: no cover
    import sys

    raise SystemExit(_main(sys.argv[1:]))
