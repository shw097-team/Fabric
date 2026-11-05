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
"""
from __future__ import annotations

import hashlib
import json
import re
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

    return leg("consumer_ack", digest=digest.lower(), provenance=receipt["provenance"],
               reader=CONSUMER_ACK_RECEIPT_READER, scope=scope, epoch=epoch,
               observed_at=str(receipt.get("observed_at") or ""),
               evidence_class=CONSUMER_ACK_RECEIPT_EVIDENCE_CLASS,
               note=("read from HGK_CONSUMER_RECEIPT@1; digest re-derived from the acknowledged "
                     f"bytes (receipt {str(receipt.get('receipt_sha256') or '')[:12]})"))


def build_binding(*, policy_ref: str, scope: str, epoch: int | str,
                  legs: list[dict[str, Any]], subject: str = "WP-FHS-02",
                  consumer_ack_receipt: dict[str, Any] | None = None) -> dict[str, Any]:
    """Assemble the six-leg record, refusing every collapse the W1 NEG list names.

    `consumer_ack_receipt` is optional. `None` keeps the previous behaviour exactly (the caller's
    sixth leg is used as supplied). A dict from `hgk_consumer_receipt.load_receipt` replaces the
    sixth leg with raw evidence; anything that fails verification refuses, so a receipt can never
    loosen a binding.
    """
    by_leg = {item["leg"]: item for item in legs}
    if consumer_ack_receipt is not None:
        by_leg["consumer_ack"] = _consumer_ack_from_receipt(
            consumer_ack_receipt, subject=subject, scope=scope, epoch=epoch)
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
    active = by_leg["active_epoch"]
    if loaded["digest"] != active["digest"]:
        raise PolicyBindingRefusal(
            "loaded bytes differ from the active epoch bytes "
            f"({loaded['digest'][:12]} != {active['digest'][:12]}): "
            "WP-FHS-02.FIRST_FAIL:POLICY_NOT_LOADED",
            code="WP-FHS-02.FIRST_FAIL:POLICY_NOT_LOADED")
    if by_leg["stage"]["digest"] != by_leg["source"]["digest"]:
        raise PolicyBindingRefusal(
            "staged bytes differ from the source bytes without a recorded re-issue",
            code="POLICY_SOURCE_STAGE_DRIFT")

    from_receipt = consumer_ack_receipt is not None
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
        "host": {"loaded_on_host": loaded["provenance"] in {"HOST_LOAD_RAW", "CONSUMER_LOAD_RECEIPT"}
                 and loaded.get("evidence_class") == "HOST_RAW",
                 "consumer_ack_observed": by_leg["consumer_ack"].get("evidence_class") == "HOST_RAW",
                 "loaded_digest_reader": loaded["reader"],
                 "consumer_ack_reader": by_leg["consumer_ack"]["reader"],
                 "consumer_ack_receipt_verified": bool(from_receipt)},
        "not_claimed": ["policy effective", "consumer consumption", "release",
                        HOST_POLICY_ACTIVE_NOT_CLAIMED["receipt" if from_receipt else "no_receipt"]],
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
