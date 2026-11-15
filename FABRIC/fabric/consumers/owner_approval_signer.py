# -*- coding: utf-8 -*-
"""D-24 — the missing *signing* side of `OWNER_APPROVAL_RECEIPT@1`.

`owner_approval_receipt.py` is a reader only: on merged `main` nothing in the repository could
produce a document it would accept, so the third leg could only ever be exercised with a hand-written
fixture. This module is the issuer, and it exists to make two specific forgeries impossible to commit
by accident:

1. **self-signing.** A receipt whose signing key is the reading principal's key proves nothing — the
   process that reads the approval would also have written it. The signer refuses when the signing
   key's public half equals any reader public key it is told about (`--reader-public-key-b64`,
   `FABRIC_READER_PUBLIC_KEY_B64`, `--reader-key-file`), when the signing `key_id` is the reader's
   key id, or when the principal SID is the reader's SID.
2. **a key inside the repository tree.** A private key committed under the repo is a key the
   repository can leak, diff, archive and review; the receipt it signs would look like evidence while
   its secret is source. The signer refuses to open such a path — before it even checks existence, so
   an in-tree path cannot be probed for existence either.

It also refuses a TTL outside `[1 minute, 30 days]`, a missing key file, a policy it cannot read, an
empty principal, and (by default) overwriting an existing receipt. Before publishing it writes a
sibling temporary file and re-reads it with `owner_approval_receipt.read_owner_receipt`; a receipt its
own reader would refuse is deleted, never renamed into place.

What this does NOT do: it does not know whether the key belongs to the Policy Owner, it does not
activate anything, and a receipt it signs is only as trustworthy as the custody of the key file the
operator points it at. `--key-id` is a label; pinning it (`owner_trusted_key_ids=`) is the reader's
job and the caller's decision.
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
from typing import Any

SCHEMA_APPROVAL = "OWNER_APPROVAL_RECEIPT@1"
SCHEMA_DIRECTIVE = "POLICY_OWNER_DIRECTIVE@1"
SCHEMAS = (SCHEMA_APPROVAL, SCHEMA_DIRECTIVE)
ALGS = ("ED25519",)

TTL_MIN_S = 60
TTL_MAX_S = 30 * 24 * 3600

CODES = (
    "OWNER_SIGN_PRINCIPAL_MISSING",
    "OWNER_SIGN_KEY_MISSING",
    "OWNER_SIGN_KEY_INSIDE_REPO",
    "OWNER_SIGN_KEY_UNUSABLE",
    "OWNER_SIGN_SELF_SIGNED",
    "OWNER_SIGN_TTL_OUT_OF_BOUNDS",
    "OWNER_SIGN_TIME_INVALID",
    "OWNER_SIGN_POLICY_UNREADABLE",
    "OWNER_SIGN_TARGET_EXISTS",
    "OWNER_SIGN_VERIFIER_UNAVAILABLE",
    "OWNER_SIGN_SELF_CHECK_FAILED",
)

_HEX64 = re.compile(r"^[0-9a-f]{64}$")


class OwnerSigningRefusal(Exception):
    """Typed refusal: no owner approval was written, and why."""

    def __init__(self, message: str, *, code: str) -> None:
        super().__init__(message)
        self.code = code

    def as_dict(self) -> dict[str, Any]:
        return {"verdict": "REFUSED", "code": self.code, "message": str(self)}


def repo_root(start: Path | None = None) -> Path | None:
    """The enclosing repository root, found by walking up for a `.git` entry (dir or worktree file)."""
    here = (start or Path(__file__)).resolve()
    for candidate in (here, *here.parents):
        if (candidate / ".git").exists():
            return candidate
    return None


def _key_outside_repo(key_path: Path, root: Path | None) -> None:
    if root is None:
        return
    try:
        key_path.resolve().relative_to(root.resolve())
    except ValueError:
        return
    raise OwnerSigningRefusal(
        f"the private key {key_path} is inside the repository tree {root}; a key the repository can "
        "leak cannot sign an owner approval", code="OWNER_SIGN_KEY_INSIDE_REPO")


def _b64(value: Any) -> bytes | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        return base64.b64decode(value.strip(), validate=True)
    except (binascii.Error, ValueError):
        return None


def _public_raw(private_key: Any) -> bytes:
    from cryptography.hazmat.primitives import serialization
    return private_key.public_key().public_bytes(encoding=serialization.Encoding.Raw,
                                                 format=serialization.PublicFormat.Raw)


def _load_private_key(key_file: str | Path, root: Path | None) -> Any:
    """Load one Ed25519 private key from raw seed, hex seed, base64 seed or PKCS8 PEM."""
    key_path = Path(key_file)
    # Containment is checked before existence on purpose: an in-tree path must not even be probed.
    _key_outside_repo(key_path, root)
    if not key_path.exists():
        raise OwnerSigningRefusal(
            f"no private key at {key_path}; this signer holds no key and will not invent one",
            code="OWNER_SIGN_KEY_MISSING")
    try:
        raw = key_path.read_bytes()
    except OSError as exc:
        raise OwnerSigningRefusal(f"private key {key_path} is not readable: {exc.strerror or exc}",
                                  code="OWNER_SIGN_KEY_UNUSABLE") from None
    try:
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    except ImportError:
        raise OwnerSigningRefusal(
            "the Ed25519 signer (package `cryptography`) is not importable on this host, so no "
            "approval can be signed", code="OWNER_SIGN_VERIFIER_UNAVAILABLE") from None

    if raw.lstrip().startswith(b"-----BEGIN"):
        try:
            loaded = serialization.load_pem_private_key(raw, password=None)
        except (ValueError, TypeError) as exc:
            raise OwnerSigningRefusal(f"private key {key_path} is not a usable PKCS8 key: {exc}",
                                      code="OWNER_SIGN_KEY_UNUSABLE") from None
        if not isinstance(loaded, Ed25519PrivateKey):
            raise OwnerSigningRefusal(
                f"private key {key_path} is a {type(loaded).__name__}, not an Ed25519 key",
                code="OWNER_SIGN_KEY_UNUSABLE")
        return loaded

    text = raw.strip()
    seed: bytes | None = None
    if len(text) == 64 and re.fullmatch(rb"[0-9a-fA-F]{64}", text):
        seed = bytes.fromhex(text.decode())
    else:
        decoded = _b64(text.decode("ascii", "ignore"))
        if decoded is not None and len(decoded) == 32:
            seed = decoded
        elif len(raw) == 32:
            seed = raw
    if seed is None:
        raise OwnerSigningRefusal(
            f"private key {key_path} is neither a 32-byte Ed25519 seed (raw, hex or base64) nor a "
            "PKCS8 PEM key", code="OWNER_SIGN_KEY_UNUSABLE")
    return Ed25519PrivateKey.from_private_bytes(seed)


def _reader_public_keys(*, reader_public_key_b64: str | None, reader_key_file: str | Path | None,
                        env: dict[str, str]) -> set[bytes]:
    """Every public key this signer was told belongs to the *reader* side, as raw 32 bytes."""
    candidates: list[str | bytes | None] = [reader_public_key_b64,
                                            env.get("FABRIC_READER_PUBLIC_KEY_B64")]
    keys: set[bytes] = set()
    for candidate in candidates:
        raw = _b64(candidate)
        if raw is not None and len(raw) == 32:
            keys.add(raw)
    if reader_key_file is not None:
        path = Path(reader_key_file)
        try:
            blob = path.read_bytes()
        except OSError:
            blob = b""
        raw = _b64(blob.decode("ascii", "ignore")) if blob else None
        if raw is not None and len(raw) == 32:
            keys.add(raw)
        elif len(blob) == 32:
            keys.add(blob)
        elif blob.lstrip().startswith(b"-----BEGIN"):
            try:
                from cryptography.hazmat.primitives import serialization
                from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
                loaded = serialization.load_pem_public_key(blob)
                if isinstance(loaded, Ed25519PublicKey):
                    keys.add(loaded.public_bytes(encoding=serialization.Encoding.Raw,
                                                 format=serialization.PublicFormat.Raw))
            except (ImportError, ValueError, TypeError):
                pass
    return keys


def sign_owner_approval(*, policy: str | Path, scope: str, epoch: int | str | None,
                        key_file: str | Path, key_id: str, out: str | Path,
                        principal_sid: str, role: str, ttl_minutes: int = 1440,
                        subject: str = "WP-FHS-02", schema: str = SCHEMA_APPROVAL,
                        display: str | None = None, reader_public_key_b64: str | None = None,
                        reader_key_file: str | Path | None = None, reader_sid: str | None = None,
                        reader_key_id: str | None = None, repo_root_override: Path | None = None,
                        now: _dt.datetime | None = None, overwrite: bool = False,
                        env: dict[str, str] | None = None) -> dict[str, Any]:
    """Sign one owner approval the reader will accept, or refuse and write nothing.

    `principal_sid`/`role` name the approving principal. `reader_public_key_b64` /
    `reader_key_file` / `FABRIC_READER_PUBLIC_KEY_B64`, `reader_sid` / `FABRIC_READER_SID` and
    `reader_key_id` / `FABRIC_READER_KEY_ID` describe the process that will *read* the approval; a
    signing key, key id or SID equal to any of them is refused as self-signing.
    """
    env = dict(os.environ if env is None else env)
    now = now or _dt.datetime.now(_dt.timezone.utc)

    if schema not in SCHEMAS:
        raise OwnerSigningRefusal(
            f"schema {schema!r} is not one this reader accepts {list(SCHEMAS)}",
            code="OWNER_SIGN_KEY_UNUSABLE")
    if not isinstance(principal_sid, str) or not principal_sid.strip():
        raise OwnerSigningRefusal(
            "no approving principal: an approval that names nobody cannot be attributed",
            code="OWNER_SIGN_PRINCIPAL_MISSING")
    if not isinstance(role, str) or not role.strip():
        raise OwnerSigningRefusal("no principal role: an approval names the role it acts in",
                                  code="OWNER_SIGN_PRINCIPAL_MISSING")
    if not isinstance(scope, str) or not scope.strip():
        raise OwnerSigningRefusal("scope is empty; an approval is scoped", code="OWNER_SIGN_PRINCIPAL_MISSING")
    if not isinstance(key_id, str) or not key_id.strip():
        raise OwnerSigningRefusal("key_id is empty; an approval names its signing key",
                                  code="OWNER_SIGN_KEY_UNUSABLE")

    ttl_s = ttl_minutes * 60 if isinstance(ttl_minutes, int) and not isinstance(ttl_minutes, bool) \
        else None
    if ttl_s is None or not (TTL_MIN_S <= ttl_s <= TTL_MAX_S):
        raise OwnerSigningRefusal(
            f"ttl_minutes is {ttl_minutes!r}; an approval window must be between "
            f"{TTL_MIN_S // 60} and {TTL_MAX_S // 60} minutes — shorter cannot be observed and "
            "longer is not a window", code="OWNER_SIGN_TTL_OUT_OF_BOUNDS")

    policy_file = Path(policy)
    try:
        policy_bytes = policy_file.read_bytes()
    except OSError as exc:
        raise OwnerSigningRefusal(
            f"approved bytes {policy_file} are not readable: {exc.strerror or exc}",
            code="OWNER_SIGN_POLICY_UNREADABLE") from None

    root = repo_root_override if repo_root_override is not None else repo_root()
    private_key = _load_private_key(key_file, root)
    signing_public = _public_raw(private_key)

    reader_sid = reader_sid if reader_sid is not None else env.get("FABRIC_READER_SID")
    reader_key_id = reader_key_id if reader_key_id is not None else env.get("FABRIC_READER_KEY_ID")
    if reader_sid and principal_sid.strip() == str(reader_sid).strip():
        raise OwnerSigningRefusal(
            f"the approving principal is the reading principal (sid {principal_sid!r}): a "
            "self-signed approval is not an owner approval", code="OWNER_SIGN_SELF_SIGNED")
    if reader_key_id and key_id.strip() == str(reader_key_id).strip():
        raise OwnerSigningRefusal(
            f"the signing key_id {key_id!r} is the reading key: a self-signed approval is not an "
            "owner approval", code="OWNER_SIGN_SELF_SIGNED")
    if signing_public in _reader_public_keys(reader_public_key_b64=reader_public_key_b64,
                                            reader_key_file=reader_key_file, env=env):
        raise OwnerSigningRefusal(
            "the signing key's public half is the reader principal's key: the process that reads "
            "the approval would also have written it", code="OWNER_SIGN_SELF_SIGNED")

    issued = now.astimezone(_dt.timezone.utc)
    expires = issued + _dt.timedelta(seconds=ttl_s)
    body: dict[str, Any] = {
        "schema": schema,
        "kind": "OWNER_APPROVAL" if schema == SCHEMA_APPROVAL else "POLICY_OWNER_DIRECTIVE",
        "subject": subject.strip(),
        "scope": scope.strip(),
        "epoch": epoch,
        "policy": {"path": str(policy_file.resolve()),
                   "sha256": hashlib.sha256(policy_bytes).hexdigest(),
                   "bytes": len(policy_bytes)},
        "principal": {"sid": principal_sid.strip(), "role": role.strip(),
                      "display": display or f"{role.strip()} ({principal_sid.strip()})"},
        "issued_at": issued.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "expires_at": expires.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "key": {"key_id": key_id.strip(), "alg": "ED25519",
                "public_key_b64": base64.b64encode(signing_public).decode()},
        "producer": {"tool": "owner_approval_signer.sign_owner_approval", "version": "1",
                     "generated_at": issued.strftime("%Y-%m-%dT%H:%M:%SZ")},
    }
    if epoch is not None and not (isinstance(epoch, int) and not isinstance(epoch, bool)):
        raise OwnerSigningRefusal(f"epoch is {epoch!r}, not an integer", code="OWNER_SIGN_TIME_INVALID")

    import owner_approval_receipt as reader  # the reader this signer must satisfy

    message = reader.canonical_body(body)
    body["signature"] = {
        "key_id": key_id.strip(),
        "alg": "ED25519",
        "sig_b64": base64.b64encode(private_key.sign(message)).decode(),
        "signed_body_sha256": hashlib.sha256(message).hexdigest(),
    }

    out_path = Path(out)
    if out_path.exists() and not overwrite:
        raise OwnerSigningRefusal(
            f"{out_path} already exists; an approval is not overwritten by default "
            "(pass overwrite=True deliberately)", code="OWNER_SIGN_TARGET_EXISTS")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = out_path.with_name(out_path.name + ".tmp")
    tmp_path.write_text(json.dumps(body, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    try:
        reread = reader.read_owner_receipt(tmp_path, expected_scope=body["scope"],
                                           expected_epoch=epoch, reader_sid=reader_sid,
                                           reader_key_id=reader_key_id, now=now)
    except reader.OwnerReceiptRefusal as exc:
        tmp_path.unlink(missing_ok=True)
        raise OwnerSigningRefusal(
            f"the produced approval does not satisfy the reader ({exc.code}): {exc}",
            code="OWNER_SIGN_SELF_CHECK_FAILED") from None
    if reread.get("state") != "OBSERVED":
        tmp_path.unlink(missing_ok=True)
        raise OwnerSigningRefusal(
            f"the produced approval did not read back ({reread.get('code')})",
            code="OWNER_SIGN_SELF_CHECK_FAILED")
    tmp_path.replace(out_path)
    return {"state": "SIGNED", "path": str(out_path), "schema": schema,
            "digest": reread["digest"], "principal": reread["principal"],
            "key_id": reread["key_id"], "issued_at": reread["issued_at"],
            "expires_at": reread["expires_at"], "receipt_sha256": reread["receipt_sha256"],
            "note": ("signed and re-read; the signature proves the key holder signed, never that "
                     "the key belongs to the Policy Owner")}


def _main(argv: list[str]) -> int:  # pragma: no cover - operator CLI, exercised via subprocess
    import argparse

    parser = argparse.ArgumentParser(description="sign one OWNER_APPROVAL_RECEIPT@1")
    parser.add_argument("--policy", required=True)
    parser.add_argument("--scope", required=True)
    parser.add_argument("--epoch", type=int, default=None)
    parser.add_argument("--subject", default="WP-FHS-02")
    parser.add_argument("--key-file", required=True)
    parser.add_argument("--key-id", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--principal-sid", required=True)
    parser.add_argument("--role", required=True)
    parser.add_argument("--display", default=None)
    parser.add_argument("--ttl-minutes", type=int, default=1440)
    parser.add_argument("--schema", default=SCHEMA_APPROVAL, choices=list(SCHEMAS))
    parser.add_argument("--reader-public-key-b64", default=None)
    parser.add_argument("--reader-key-file", default=None)
    parser.add_argument("--reader-sid", default=None)
    parser.add_argument("--reader-key-id", default=None)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args(argv)
    try:
        out = sign_owner_approval(policy=args.policy, scope=args.scope, epoch=args.epoch,
                                  key_file=args.key_file, key_id=args.key_id, out=args.out,
                                  principal_sid=args.principal_sid, role=args.role,
                                  ttl_minutes=args.ttl_minutes, subject=args.subject,
                                  schema=args.schema, display=args.display,
                                  reader_public_key_b64=args.reader_public_key_b64,
                                  reader_key_file=args.reader_key_file,
                                  reader_sid=args.reader_sid, reader_key_id=args.reader_key_id,
                                  overwrite=args.overwrite)
    except OwnerSigningRefusal as exc:
        print(json.dumps(exc.as_dict(), ensure_ascii=False, indent=2))
        return 1
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":  # pragma: no cover
    import sys

    raise SystemExit(_main(sys.argv[1:]))
