# -*- coding: utf-8 -*-
"""WP-FHS-02 — Fabric policy binding: six independently-provenanced legs.

The W1 contract (`WP-FHS-02`) does not ask for a new policy engine. It asks that the six facts a
"policy is in force" claim rests on stay *separate records with separate readers*:

    Source -> Stage -> OwnerApproved -> ActiveEpoch -> LoadedDigest -> HGK ConsumerACK

and that a document (a stage mirror, a navigation pointer, an assisted-use approval) can never stand
in for a later leg. The refusal this module exists for is

    WP-FHS-02.FIRST_FAIL:POLICY_NOT_LOADED

which fires when the loaded leg's provenance is not a host load receipt, or when the loaded bytes
differ from the active epoch's bytes.

Nothing here activates a policy: `state=BOUND` means the six legs are internally consistent at
`claim_ceiling=AUTHOR_DESIGN_ONLY` (or `FIXTURE` in a unit test). The host flags
(`loaded_on_host`, `consumer_ack_observed`) are reported as they were supplied, never inferred.

The sixth leg has a typed producer: `hgk_consumer_receipt.load_receipt` reads a
`HGK_CONSUMER_RECEIPT@1` document and re-derives the digest of the bytes it acknowledges. Passing
that result as `consumer_ack_receipt=` is the only way `build_binding` itself puts raw evidence into
`consumer_ack`; the default (`None`) leaves the caller-supplied leg untouched and adds
`host_policy_active` to `not_claimed`, so a BOUND built that way still says what it does not mean.

D-17 (2026-11-07) closed three measured collapses of that separation, all of them reachable from the
public API:

1. the fifth leg had **no reader** in Fabric, so a `HOST_LOAD_RECEIPT@1` with a valid envelope over
   the real bytes and no producer/process block — or no receipt at all — filled `loaded_digest` and
   reported `host.loaded_on_host=True`. `load_receipt=` now routes the leg through
   `host_load_receipt.read_load_receipt`, which validates the producer/process block; a leg that
   *claims* `HOST_RAW` without a receipt is refused with `POLICY_LOAD_UNSUBSTANTIATED`;
2. a caller-typed `consumer_ack` dict with `evidence_class="HOST_RAW"` and
   `consumer_ack_receipt=None` set `host.consumer_ack_observed=True`. It is now refused with
   `POLICY_CONSUMER_ACK_UNSUBSTANTIATED`, and a receipt's digest must equal the loaded policy bytes
   (`POLICY_CONSUMER_ACK_DIGEST_MISMATCH`);
3. the loaded leg only had to avoid `NON_LOADING_PROVENANCE` plus match the active digest, so
   `ACTIVE_POLICY_POINTER` (or any hand-typed value) could substantiate it once `leg()` was
   bypassed. Membership in `LOADED_PROVENANCE` is now enforced inside `build_binding`, refusing with
   `POLICY_LOADED_PROVENANCE_NOT_A_LOAD_RECEIPT`.

No refusal code was removed or renamed; the four codes above are additive.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, NoReturn

_HEX64 = re.compile(r"^[0-9a-f]{64}$")

SCHEMA = "FABRIC.PolicyLoadedConsumerACK@design"
LEGS = ("source", "stage", "owner_approved", "active_epoch", "loaded_digest", "consumer_ack")

# Which reader may substantiate a leg. A provenance outside its set is a fabrication of that leg.
LEG_PROVENANCE = {
    "source": {"FABRIC_POLICY_SOURCE", "FABRIC_POLICY_REPO_BLOB"},
    "stage": {"STAGED_ARTIFACT", "STAGE_MIRROR"},
    "owner_approved": {"OWNER_APPROVAL_RECEIPT", "POLICY_OWNER_DIRECTIVE"},
    "active_epoch": {"ACTIVE_POLICY_POINTER", "EPOCH_PROMOTION_RECEIPT"},
    "loaded_digest": {"HOST_LOAD_RAW", "CONSUMER_LOAD_RECEIPT"},
    "consumer_ack": {"HGK_CONSUMER_RECEIPT", "HGK_CONSUMER_TRACE"},
}

# Provenances that describe an artifact *about* a policy, never the policy running on a host.
NON_LOADING_PROVENANCE = {"STAGED_ARTIFACT", "STAGE_MIRROR", "NAV_ASSISTED_USE_APPROVED",
                          "DESIGN_PROJECTION", "DOCUMENT_REFERENCE"}
# They are recognised values for `loaded_digest` on purpose: the leg records what it was told, and
# `build_binding` then refuses with WP-FHS-02.FIRST_FAIL:POLICY_NOT_LOADED. Refusing at construction
# would swallow the W1 code behind a generic provenance error.
LEG_PROVENANCE["loaded_digest"] |= NON_LOADING_PROVENANCE


# The typed producer for the sixth leg. Kept as values (not an import) so this module stays the
# dependency root; `tests/test_hgk_consumer_receipt.py` asserts these agree with the reader module.
CONSUMER_ACK_RECEIPT_SCHEMA = "HGK_CONSUMER_RECEIPT@1"
CONSUMER_ACK_RECEIPT_PROVENANCE = "HGK_CONSUMER_RECEIPT"
CONSUMER_ACK_RECEIPT_READER = "hgk-consumer-receipt-reader"
CONSUMER_ACK_RECEIPT_EVIDENCE_CLASS = "HOST_RAW"

# The typed producer for the fifth leg (D-17). Same rule: values, not an import, so a caller can
# read this module without the reader being importable, and `tests/test_policy_binding_forgery.py`
# asserts they agree with `host_load_receipt`.
LOAD_RECEIPT_SCHEMA = "HOST_LOAD_RECEIPT@1"
LOAD_RECEIPT_PROVENANCE = "HOST_LOAD_RAW"
LOAD_RECEIPT_READER = "host-load-receipt-reader"
LOAD_RECEIPT_EVIDENCE_CLASS = "HOST_RAW"

# The typed producer for the third leg (D-17, hole 4). Same rule: values, not an import.
OWNER_RECEIPT_SCHEMAS = ("OWNER_APPROVAL_RECEIPT@1", "POLICY_OWNER_DIRECTIVE@1")
OWNER_RECEIPT_READER = "owner-receipt-reader"
OWNER_RECEIPT_EVIDENCE_CLASS = "HOST_RAW"

# The only provenances that describe a policy *loaded on a host*. Membership is enforced in
# `build_binding`, not only in `leg()`, because a caller can build the dict by hand.
LOADED_PROVENANCE = frozenset({LOAD_RECEIPT_PROVENANCE, "CONSUMER_LOAD_RECEIPT"})

# Refusals added for D-17. Every code that existed before the patch is still emitted unchanged.
D17_REFUSAL_CODES = (
    "POLICY_LOADED_PROVENANCE_NOT_A_LOAD_RECEIPT",
    "POLICY_LOAD_UNSUBSTANTIATED",
    "POLICY_CONSUMER_ACK_UNSUBSTANTIATED",
    "POLICY_CONSUMER_ACK_DIGEST_MISMATCH",
    "POLICY_OWNER_APPROVAL_UNSUBSTANTIATED",
)

# `state=BOUND` is a claim about design consistency, never about a running host. Both wordings below
# land in `not_claimed`; the difference is only whether raw consumer evidence was supplied.
HOST_POLICY_ACTIVE_NOT_CLAIMED = {
    "no_receipt": ("host_policy_active: BOUND means the six legs are internally consistent at "
                   "claim_ceiling=AUTHOR_DESIGN_ONLY; no HGK_CONSUMER_RECEIPT@1 was supplied, so "
                   "consumer_ack is caller-supplied evidence and host policy activation is not "
                   "claimed"),
    "receipt": ("host_policy_active: a verified HGK_CONSUMER_RECEIPT@1 shows the consumer "
                "acknowledged the loaded bytes; it does not show the host policy is active, "
                "effective, or in force"),
}

# D-17 hole 4. `owner_approved` now has a reader, and what that reader did — and did not — establish
# has to be said on the record, because a verified signature is easily mistaken for an owner act.
OWNER_APPROVAL_NOT_CLAIMED = {
    "no_receipt": ("owner_approval: no OWNER_APPROVAL_RECEIPT@1 was supplied, so owner_approved is "
                   "caller-supplied evidence and the authenticity of the approval is not claimed"),
    "receipt": ("owner_approval: a detached signature verified against the key the document names, "
                "over the bytes this reader re-hashed; that the key belongs to the Policy Owner is "
                "NOT established by the document (pin trusted_key_ids or read the key registry), "
                "and a FIXTURE key proves reachability only"),
}


class PolicyBindingRefusal(Exception):
    def __init__(self, message: str, *, code: str) -> None:
        super().__init__(message)
        self.code = code

    def as_dict(self) -> dict[str, Any]:
        return {"verdict": "REFUSED", "code": self.code, "message": str(self)}


def _sha(body: Any) -> str:
    return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False).encode()).hexdigest()


def leg(kind: str, *, digest: str, provenance: str, reader: str, scope: str, epoch: int | str,
        observed_at: str = "", evidence_class: str = "FIXTURE", note: str = "") -> dict[str, Any]:
    """One leg. Refuses an unknown leg name or a provenance its reader could not have produced."""
    if kind not in LEGS:
        raise PolicyBindingRefusal(f"unknown leg: {kind}", code="POLICY_LEG_UNKNOWN")
    if not str(digest or "").strip():
        raise PolicyBindingRefusal(f"leg {kind} has no digest", code="POLICY_LEG_EMPTY")
    if provenance not in LEG_PROVENANCE[kind]:
        raise PolicyBindingRefusal(
            f"leg {kind} cannot be substantiated by provenance {provenance!r}; "
            f"allowed: {sorted(LEG_PROVENANCE[kind])}", code="POLICY_LEG_PROVENANCE_INVALID")
    return {"leg": kind, "digest": digest, "provenance": provenance, "reader": reader,
            "scope": scope, "epoch": epoch, "observed_at": observed_at,
            "evidence_class": evidence_class, "note": note}


def _order(legs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    index = {name: i for i, name in enumerate(LEGS)}
    return sorted(legs, key=lambda item: index[item["leg"]])


def _consumer_ack_from_receipt(receipt: Any, *, subject: str, scope: str,
                               epoch: int | str) -> dict[str, Any]:
    """Turn a verified `HGK_CONSUMER_RECEIPT@1` read into the sixth leg, or refuse.

    The receipt is re-checked here rather than trusted, because a caller can build any dict: a
    hand-typed `evidence_class` string must not be able to raise `consumer_ack_observed`. Any
    failure refuses with an existing code — there is no soft pass and no partially-bound record.
    """
    def refuse(why: str, code: str = "POLICY_LEG_PROVENANCE_INVALID") -> NoReturn:
        raise PolicyBindingRefusal(
            f"consumer_ack receipt cannot substantiate the sixth leg: {why}", code=code)

    if not isinstance(receipt, dict):
        refuse(f"receipt is a {type(receipt).__name__}, not a verified receipt")
    if receipt.get("state") != "OBSERVED":
        refuse(f"receipt state is {receipt.get('state')!r} "
               f"({receipt.get('code') or receipt.get('reason') or 'no reason given'}): "
               "an unobserved receipt is not evidence")
    if receipt.get("verified") is not True:
        refuse("receipt carries no reader verification marker")
    if receipt.get("evidence_class") != CONSUMER_ACK_RECEIPT_EVIDENCE_CLASS:
        refuse(f"receipt evidence_class is {receipt.get('evidence_class')!r}; only "
               f"{CONSUMER_ACK_RECEIPT_EVIDENCE_CLASS} may set consumer_ack_observed")
    if receipt.get("provenance") != CONSUMER_ACK_RECEIPT_PROVENANCE:
        refuse(f"receipt provenance is {receipt.get('provenance')!r}")
    if receipt.get("reader") != CONSUMER_ACK_RECEIPT_READER:
        refuse(f"receipt reader is {receipt.get('reader')!r}, "
               f"expected {CONSUMER_ACK_RECEIPT_READER!r}")
    if receipt.get("subject") != subject:
        refuse(f"receipt subject is {receipt.get('subject')!r}, binding subject is {subject!r}",
               code="POLICY_SIGNER_OR_EPOCH_DENY")
    if receipt.get("scope") != scope or str(receipt.get("epoch")) != str(epoch):
        refuse(f"receipt claims scope/epoch {receipt.get('scope')!r}/{receipt.get('epoch')!r}, "
               f"binding is {scope!r}/{epoch!r}", code="POLICY_SIGNER_OR_EPOCH_DENY")
    digest = receipt.get("digest")
    if not isinstance(digest, str) or not _HEX64.match(digest.lower()):
        refuse(f"receipt digest is {digest!r}, not a sha256 hex digest of acknowledged bytes")

    # The dict is a claim; the files are the evidence. Without this, a hand-built dict carrying the
    # right strings (`state=OBSERVED`, `verified=true`, `reader=…`, `evidence_class=HOST_RAW`, a hex
    # `digest`) was accepted and flipped `consumer_ack_observed`, with no bytes anywhere on disk.
    receipt_path = receipt.get("receipt_path")
    raw_path = receipt.get("raw_path")
    if not isinstance(receipt_path, str) or not receipt_path.strip():
        refuse("receipt carries no receipt_path, so the acknowledged bytes cannot be re-read")
    if not isinstance(raw_path, str) or not raw_path.strip():
        refuse("receipt carries no raw_path, so the acknowledged bytes cannot be re-read")
    consumer_id = receipt.get("consumer_id")
    if not isinstance(consumer_id, str) or not consumer_id.strip():
        refuse("receipt carries no consumer_id, so the acknowledging principal is unbound")

    import hgk_consumer_receipt as _reader  # local: keeps this module the dependency root

    # Defence in depth: the reader already refuses a non-positive ack, but this is the function that
    # sets `host.consumer_ack_observed`, so it re-checks rather than trusting its input shape.
    if not _reader.is_positive_ack(receipt.get("ack")):
        refuse(f"ack is {receipt.get('ack')!r}, which is a consumer decision NOT to acknowledge; "
               "a NACK/DEFERRED receipt is authentic but never substantiates the sixth leg",
               code="POLICY_CONSUMER_NOT_ACK")

    try:
        reread = _reader.load_receipt(receipt_path, expected_subject=subject, expected_scope=scope,
                                      expected_epoch=epoch, consumer_id=consumer_id,
                                      raw_path=raw_path)
    except _reader.HGKReceiptRefusal as exc:
        refuse(f"re-reading {receipt_path} refused ({exc.code}): {exc}")
    if reread.get("state") != "OBSERVED":
        refuse(f"re-reading {receipt_path} returned {reread.get('state')!r} "
               f"({reread.get('code') or reread.get('reason') or 'no reason given'})")
    for key in ("digest", "receipt_sha256"):
        claimed = str(receipt.get(key) or "").lower()
        observed = str(reread.get(key) or "").lower()
        if claimed != observed:
            refuse(f"claimed {key} {claimed[:12]} does not match the bytes on disk {observed[:12]}")
    digest = reread["digest"]

    return leg("consumer_ack", digest=digest.lower(), provenance=receipt["provenance"],
               reader=CONSUMER_ACK_RECEIPT_READER, scope=scope, epoch=epoch,
               observed_at=str(receipt.get("observed_at") or ""),
               evidence_class=CONSUMER_ACK_RECEIPT_EVIDENCE_CLASS,
               note=("read from HGK_CONSUMER_RECEIPT@1; digest re-derived from the acknowledged "
                     f"bytes (receipt {str(receipt.get('receipt_sha256') or '')[:12]})"))


def _loaded_from_receipt(receipt: Any, *, scope: str, epoch: int | str) -> dict[str, Any]:
    """Turn a verified `HOST_LOAD_RECEIPT@1` read into the fifth leg, or refuse.

    D-17, hole 1: the fifth leg used to have no reader at all, so a caller-supplied dict carrying
    `provenance="HOST_LOAD_RAW"` and `evidence_class="HOST_RAW"` satisfied every check while no load
    artifact existed anywhere on disk. This function accepts only

    * a path to a `HOST_LOAD_RECEIPT@1`, or
    * the dict `host_load_receipt.read_load_receipt` returned for one,

    and re-reads the document either way, so the digest is re-derived rather than trusted. The
    document's producer/process block is validated by the reader
    (`LOAD_RECEIPT_NO_PRODUCER_BLOCK` / `LOAD_RECEIPT_PRODUCER_BLOCK_INVALID`); that code is
    propagated unchanged so an operator sees the load-side reason, not a generic binding error.
    """
    def refuse(why: str, code: str = "POLICY_LEG_PROVENANCE_INVALID") -> NoReturn:
        raise PolicyBindingRefusal(
            f"loaded_digest receipt cannot substantiate the fifth leg: {why}", code=code)

    if isinstance(receipt, (str, Path)):
        path: Any = receipt
    elif isinstance(receipt, dict):
        path = receipt.get("receipt_path")
        if not isinstance(path, str) or not path.strip():
            refuse("a caller-supplied dict with no receipt_path cannot be re-read; pass the "
                   "receipt path or the result of host_load_receipt.read_load_receipt(...)")
        if receipt.get("state") != "OBSERVED":
            refuse(f"receipt state is {receipt.get('state')!r}: an unobserved load is not evidence")
        if receipt.get("verified") is not True:
            refuse("receipt carries no reader verification marker")
        if receipt.get("leg") != "loaded_digest":
            refuse(f"receipt leg is {receipt.get('leg')!r}, expected 'loaded_digest'")
        if receipt.get("provenance") not in LOADED_PROVENANCE:
            refuse(f"receipt provenance is {receipt.get('provenance')!r}; only "
                   f"{sorted(LOADED_PROVENANCE)} may fill the loaded leg")
        if receipt.get("reader") != LOAD_RECEIPT_READER:
            refuse(f"receipt reader is {receipt.get('reader')!r}, "
                   f"expected {LOAD_RECEIPT_READER!r}")
        if receipt.get("evidence_class") != LOAD_RECEIPT_EVIDENCE_CLASS:
            refuse(f"receipt evidence_class is {receipt.get('evidence_class')!r}")
        if not isinstance(receipt.get("digest"), str) or not _HEX64.match(
                str(receipt.get("digest")).lower()):
            refuse(f"receipt digest is {receipt.get('digest')!r}, not a sha256 hex digest")
    else:
        refuse(f"receipt is a {type(receipt).__name__}, not a path and not a verified receipt")

    import host_load_receipt as _reader  # local: keeps this module the dependency root

    try:
        reread = _reader.read_load_receipt(path, expected_scope=scope, expected_epoch=epoch)
    except _reader.LoadReceiptRefusal as exc:
        # The reader's own code is the honest one: "no producer block" is not "bad provenance".
        raise PolicyBindingRefusal(
            f"load receipt {path} refused ({exc.code}): {exc}", code=exc.code) from None
    if reread.get("state") != "OBSERVED":
        # Propagate the reader's own "no receipt / unreadable" code rather than a generic one.
        refuse(f"re-reading {path} returned {reread.get('state')!r} "
               f"({reread.get('code') or reread.get('reason') or 'no reason given'})",
               code=str(reread.get("code") or "POLICY_LEG_PROVENANCE_INVALID"))
    if isinstance(receipt, dict):
        for key in ("digest", "receipt_sha256"):
            claimed = str(receipt.get(key) or "").lower()
            observed = str(reread.get(key) or "").lower()
            if claimed != observed:
                refuse(f"claimed {key} {claimed[:12]} does not match the bytes on disk "
                       f"{observed[:12]}")

    return leg("loaded_digest", digest=str(reread["digest"]).lower(),
               provenance=reread["provenance"], reader=reread["reader"], scope=scope, epoch=epoch,
               observed_at=str(reread.get("observed_at") or ""),
               evidence_class=reread["evidence_class"],
               note=("read from HOST_LOAD_RECEIPT@1; digest re-derived from the policy bytes and the "
                     f"producer/process block validated (pid {reread['process'].get('pid')}, "
                     f"receipt {str(reread.get('receipt_sha256') or '')[:12]})"))


def _owner_from_receipt(receipt: Any, *, scope: str, epoch: int | str,
                        source_digest: str | None,
                        reader_sid: str | None = None,
                        trusted_key_ids: Any = None) -> dict[str, Any]:
    """Turn a verified owner approval into the third leg, or refuse.

    D-17, hole 4: `LEG_PROVENANCE["owner_approved"]` named two provenances and the module read
    neither, so a caller-typed label plus the source digest satisfied the leg. This accepts only a
    path to an `OWNER_APPROVAL_RECEIPT@1` / `POLICY_OWNER_DIRECTIVE@1` or the dict the reader
    returned for one, re-reads the document, and requires the approved digest to be the source
    digest this binding is about.
    """
    def refuse(why: str, code: str = "POLICY_LEG_PROVENANCE_INVALID") -> NoReturn:
        raise PolicyBindingRefusal(
            f"owner_approved receipt cannot substantiate the third leg: {why}", code=code)

    if isinstance(receipt, (str, Path)):
        path: Any = receipt
        policy_path = None
    elif isinstance(receipt, dict):
        path = receipt.get("receipt_path")
        if not isinstance(path, str) or not path.strip():
            refuse("a caller-supplied dict with no receipt_path cannot be re-read; pass the "
                   "receipt path or the result of owner_approval_receipt.read_owner_receipt(...)")
        if receipt.get("state") != "OBSERVED":
            refuse(f"receipt state is {receipt.get('state')!r}: an unobserved approval is not "
                   "evidence")
        if receipt.get("verified") is not True:
            refuse("receipt carries no reader verification marker")
        if receipt.get("leg") != "owner_approved":
            refuse(f"receipt leg is {receipt.get('leg')!r}, expected 'owner_approved'")
        if receipt.get("provenance") not in {"OWNER_APPROVAL_RECEIPT", "POLICY_OWNER_DIRECTIVE"}:
            refuse(f"receipt provenance is {receipt.get('provenance')!r}")
        if receipt.get("reader") != OWNER_RECEIPT_READER:
            refuse(f"receipt reader is {receipt.get('reader')!r}, "
                   f"expected {OWNER_RECEIPT_READER!r}")
        if receipt.get("evidence_class") != OWNER_RECEIPT_EVIDENCE_CLASS:
            refuse(f"receipt evidence_class is {receipt.get('evidence_class')!r}")
        if not isinstance(receipt.get("digest"), str) or not _HEX64.match(
                str(receipt.get("digest")).lower()):
            refuse(f"receipt digest is {receipt.get('digest')!r}, not a sha256 hex digest")
        policy_path = receipt.get("policy_path")
    else:
        refuse(f"receipt is a {type(receipt).__name__}, not a path and not a verified receipt")

    import owner_approval_receipt as _reader  # local: keeps this module the dependency root

    try:
        reread = _reader.read_owner_receipt(path, expected_scope=scope, expected_epoch=epoch,
                                            policy_path=policy_path, reader_sid=reader_sid,
                                            trusted_key_ids=trusted_key_ids)
    except _reader.OwnerReceiptRefusal as exc:
        raise PolicyBindingRefusal(
            f"owner approval {path} refused ({exc.code}): {exc}", code=exc.code) from None
    if reread.get("state") != "OBSERVED":
        # Propagate "no receipt / unreadable" rather than a generic provenance error.
        refuse(f"re-reading {path} returned {reread.get('state')!r} "
               f"({reread.get('code') or reread.get('reason') or 'no reason given'})",
               code=str(reread.get("code") or "POLICY_LEG_PROVENANCE_INVALID"))
    if isinstance(receipt, dict):
        for key in ("digest", "receipt_sha256"):
            claimed = str(receipt.get(key) or "").lower()
            observed = str(reread.get(key) or "").lower()
            if claimed != observed:
                refuse(f"claimed {key} {claimed[:12]} does not match the bytes on disk "
                       f"{observed[:12]}")
    if source_digest is not None and str(reread["digest"]).lower() != str(source_digest).lower():
        raise PolicyBindingRefusal(
            "the owner approved different bytes than the policy this binding is about "
            f"({str(reread['digest'])[:12]} != {str(source_digest)[:12]})",
            code="OWNER_RECEIPT_DIGEST_MISMATCH")

    return leg("owner_approved", digest=str(reread["digest"]).lower(),
               provenance=reread["provenance"], reader=OWNER_RECEIPT_READER, scope=scope,
               epoch=epoch, observed_at=str(reread.get("observed_at") or ""),
               evidence_class=OWNER_RECEIPT_EVIDENCE_CLASS,
               note=(f"read from {reread['provenance']}@1; signature verified against key_id "
                     f"{reread['key_id']!r} (key_trusted={reread['key_trusted']}), principal "
                     f"{reread['principal']['sid']}/{reread['principal']['role']}, expires "
                     f"{reread['expires_at']}")) | {
        # Carried on the leg so the record can state what was and was not established about the
        # signing key. `key_trusted` is True only when the caller pinned the key_id itself.
        "key_id": reread["key_id"],
        "key_trusted": bool(reread["key_trusted"]),
        "principal": reread["principal"],
        "expires_at": reread["expires_at"],
    }


def build_binding(*, policy_ref: str, scope: str, epoch: int | str,
                  legs: list[dict[str, Any]], subject: str = "WP-FHS-02",
                  consumer_ack_receipt: dict[str, Any] | None = None,
                  load_receipt: Any | None = None,
                  owner_receipt: Any | None = None,
                  owner_reader_sid: str | None = None,
                  owner_trusted_key_ids: Any = None) -> dict[str, Any]:
    """Assemble the six-leg record, refusing every collapse the W1 NEG list names.

    `consumer_ack_receipt` is optional. `None` keeps the previous behaviour exactly (the caller's
    sixth leg is used as supplied). A dict from `hgk_consumer_receipt.load_receipt` replaces the
    sixth leg with raw evidence; anything that fails verification refuses, so a receipt can never
    loosen a binding.

    `load_receipt` is the D-17 addition and works the same way for the fifth leg: a path to a
    `HOST_LOAD_RECEIPT@1` or the dict `host_load_receipt.read_load_receipt` returned for one. A leg
    that claims `HOST_RAW` without a receipt is refused instead of being reported as a host load.

    `owner_receipt` does the same for the third leg: a path to an `OWNER_APPROVAL_RECEIPT@1` /
    `POLICY_OWNER_DIRECTIVE@1` or the dict `owner_approval_receipt.read_owner_receipt` returned for
    one. `owner_reader_sid` / `owner_trusted_key_ids` are passed to that reader so a self-signed
    approval is refused and, when the caller owns a key registry, the named key is pinned.
    """
    by_leg = {item["leg"]: item for item in legs}
    from_receipt = consumer_ack_receipt is not None
    if from_receipt:
        by_leg["consumer_ack"] = _consumer_ack_from_receipt(
            consumer_ack_receipt, subject=subject, scope=scope, epoch=epoch)
        legs = list(by_leg.values())
    from_load_receipt = load_receipt is not None
    if from_load_receipt:
        by_leg["loaded_digest"] = _loaded_from_receipt(load_receipt, scope=scope, epoch=epoch)
        legs = list(by_leg.values())
    from_owner_receipt = owner_receipt is not None
    if from_owner_receipt:
        by_leg["owner_approved"] = _owner_from_receipt(
            owner_receipt, scope=scope, epoch=epoch,
            source_digest=(by_leg["source"]["digest"] if "source" in by_leg else None),
            reader_sid=owner_reader_sid, trusted_key_ids=owner_trusted_key_ids)
        legs = list(by_leg.values())
    missing = [name for name in LEGS if name not in by_leg]
    if missing:
        raise PolicyBindingRefusal("missing legs: " + ", ".join(missing),
                                   code="POLICY_BINDING_INCOMPLETE")

    foreign = [item["leg"] for item in legs
               if item["scope"] != scope or str(item["epoch"]) != str(epoch)]
    if foreign:
        raise PolicyBindingRefusal(
            "legs claim a different scope/epoch than the binding: " + ", ".join(sorted(foreign)),
            code="POLICY_SIGNER_OR_EPOCH_DENY")

    loaded = by_leg["loaded_digest"]
    if loaded["provenance"] in NON_LOADING_PROVENANCE:
        raise PolicyBindingRefusal(
            "loaded leg is substantiated by "
            f"{loaded['provenance']} — a document about the policy is not the policy loaded: "
            "WP-FHS-02.FIRST_FAIL:POLICY_NOT_LOADED",
            code="WP-FHS-02.FIRST_FAIL:POLICY_NOT_LOADED")
    # D-17, hole 3: `leg()` refuses a provenance outside LEG_PROVENANCE[kind], but a caller can
    # build the dict itself. Only a load receipt's provenance may substantiate this leg, and
    # ACTIVE_POLICY_POINTER / EPOCH_PROMOTION_RECEIPT are epoch declarations, never a load.
    if loaded["provenance"] not in LOADED_PROVENANCE:
        raise PolicyBindingRefusal(
            f"loaded leg is substantiated by {loaded['provenance']!r}, which is not a load-receipt "
            f"provenance {sorted(LOADED_PROVENANCE)}: an epoch pointer or a hand-typed label is "
            "not the policy loaded on this host",
            code="POLICY_LOADED_PROVENANCE_NOT_A_LOAD_RECEIPT")
    active = by_leg["active_epoch"]
    if loaded["digest"] != active["digest"]:
        raise PolicyBindingRefusal(
            "loaded bytes differ from the active epoch bytes "
            f"({loaded['digest'][:12]} != {active['digest'][:12]}): "
            "WP-FHS-02.FIRST_FAIL:POLICY_NOT_LOADED",
            code="WP-FHS-02.FIRST_FAIL:POLICY_NOT_LOADED")
    # D-17, hole 1: a leg that *claims* raw host evidence must have come from a receipt this call
    # opened. Without this a hand-typed evidence_class is a host-load claim with no host artifact.
    if not from_load_receipt and loaded.get("evidence_class") == "HOST_RAW":
        raise PolicyBindingRefusal(
            "loaded leg claims evidence_class=HOST_RAW but no HOST_LOAD_RECEIPT@1 was supplied; a "
            "caller-typed label is not a load observation (pass load_receipt=<path|reader result>)",
            code="POLICY_LOAD_UNSUBSTANTIATED")
    ack = by_leg["consumer_ack"]
    # D-17, hole 2: the sixth leg had the same collapse as the fifth — a caller-typed dict with
    # evidence_class=HOST_RAW flipped consumer_ack_observed with no receipt in existence.
    if not from_receipt and ack.get("evidence_class") == "HOST_RAW":
        raise PolicyBindingRefusal(
            "consumer_ack claims evidence_class=HOST_RAW but no HGK_CONSUMER_RECEIPT@1 was "
            "supplied; a caller-typed acknowledgement is not a consumer acknowledgement",
            code="POLICY_CONSUMER_ACK_UNSUBSTANTIATED")
    if from_receipt and str(ack["digest"]).lower() != str(loaded["digest"]).lower():
        raise PolicyBindingRefusal(
            "the consumer acknowledged different bytes than the policy loaded "
            f"({str(ack['digest'])[:12]} != {str(loaded['digest'])[:12]}): an ACK of another "
            "document does not substantiate this binding",
            code="POLICY_CONSUMER_ACK_DIGEST_MISMATCH")
    # D-17, hole 4: `owner_approved` had no reader either, so a caller-typed label plus the source
    # digest was the only thing the leg required. A HOST_RAW claim now needs the receipt.
    owner = by_leg["owner_approved"]
    if not from_owner_receipt and owner.get("evidence_class") == "HOST_RAW":
        raise PolicyBindingRefusal(
            "owner_approved claims evidence_class=HOST_RAW but no OWNER_APPROVAL_RECEIPT@1 was "
            "supplied; a caller-typed approval is not an owner approval (pass owner_receipt="
            "<path|reader result>)",
            code="POLICY_OWNER_APPROVAL_UNSUBSTANTIATED")
    if from_owner_receipt and str(owner["digest"]).lower() != str(by_leg["source"]["digest"]).lower():
        raise PolicyBindingRefusal(
            "the owner approved different bytes than the source leg "
            f"({str(owner['digest'])[:12]} != {str(by_leg['source']['digest'])[:12]})",
            code="OWNER_RECEIPT_DIGEST_MISMATCH")
    if by_leg["stage"]["digest"] != by_leg["source"]["digest"]:
        raise PolicyBindingRefusal(
            "staged bytes differ from the source bytes without a recorded re-issue",
            code="POLICY_SOURCE_STAGE_DRIFT")

    record = {
        "schema": SCHEMA,
        "subject": subject,
        "policy_ref": policy_ref,
        "scope": scope,
        "epoch": epoch,
        "legs": _order(legs),
        "digests": {name: by_leg[name]["digest"] for name in LEGS},
        "separate_readers": len({item["reader"] for item in legs}),
        "state": "BOUND",
        "claim_ceiling": "AUTHOR_DESIGN_ONLY",
        "host": {"loaded_on_host": bool(from_load_receipt)
                 and loaded["provenance"] in LOADED_PROVENANCE
                 and loaded.get("evidence_class") == "HOST_RAW",
                 "consumer_ack_observed": bool(from_receipt)
                 and ack.get("evidence_class") == "HOST_RAW",
                 "loaded_digest_reader": loaded["reader"],
                 "consumer_ack_reader": ack["reader"],
                 "load_receipt_verified": bool(from_load_receipt),
                 "owner_approval_verified": bool(from_owner_receipt),
                 "owner_key_trusted": bool(from_owner_receipt and owner.get("key_trusted")),
                 "consumer_ack_receipt_verified": bool(from_receipt)},
        "not_claimed": ["policy effective", "consumer consumption", "release",
                        HOST_POLICY_ACTIVE_NOT_CLAIMED["receipt" if from_receipt else "no_receipt"],
                        OWNER_APPROVAL_NOT_CLAIMED["receipt" if from_owner_receipt
                                                   else "no_receipt"]],
        "note": ("legs are separate records on purpose: a stage/mirror/nav document cannot "
                 "substantiate loaded_digest or consumer_ack"),
    }
    record["binding_sha256"] = _sha({k: v for k, v in record.items() if k != "binding_sha256"})
    return record


def refuse_document_claim(document: dict[str, Any]) -> dict[str, Any]:
    """A stage/mirror/nav document that marks itself loaded is refused, not upgraded.

    This is the executable form of the W1 NEG: "only a Stage/mirror or NAV_ASSISTED_USE_APPROVED
    yet labelled Loaded/Issuer".
    """
    claimed = str(document.get("state") or document.get("status") or "").upper()
    origin = str(document.get("provenance") or document.get("source") or "").upper()
    if "LOADED" in claimed or "ACTIVE" in claimed:
        if origin in {p.upper() for p in NON_LOADING_PROVENANCE}:
            raise PolicyBindingRefusal(
                f"a {origin} document claims {claimed}: "
                "WP-FHS-02.FIRST_FAIL:POLICY_NOT_LOADED",
                code="WP-FHS-02.FIRST_FAIL:POLICY_NOT_LOADED")
    return {"state": "DOCUMENT_CLAIM_NOT_A_LOAD_RECEIPT", "origin": origin, "claimed": claimed}
