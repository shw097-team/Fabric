# D-17 — forged policy receipts, and how the third leg was made un-forgeable

This document accompanies the D-17 candidate (`fix/d17-forged-policy-receipts-20261107`). It records
what was measured, what changed, and how to reproduce every claim. It is engineering evidence for a
maintainer, not an acceptance: nothing here is merged, and no owner approval exists.

## 1. The four holes, measured before the patch

Every one of these was reproduced on `main` at `ea259bd` before any change. "ACCEPT" means
`build_binding` returned `state=BOUND` with no artifact of that kind existing anywhere on disk.

| # | Hole | Before (measured) | After (refused with) |
|---|---|---|---|
| H1 | the fifth leg had **no reader at all** — importing `host_load_receipt` raised `ModuleNotFoundError` | a caller-projected leg with `provenance=HOST_LOAD_RAW` bound; `loaded_on_host=true`, `receipt_verified=false` | `LOAD_RECEIPT_NO_PRODUCER_BLOCK` / `POLICY_LOAD_UNSUBSTANTIATED` |
| H2 | `consumer_ack_receipt=None` still set `consumer_ack_observed=True` from a caller-typed dict | `BOUND`, `ack` leg `evidence_class=HOST_RAW`, no receipt in existence | `POLICY_CONSUMER_ACK_UNSUBSTANTIATED` / `POLICY_CONSUMER_ACK_DIGEST_MISMATCH` |
| H3 | `leg()` bypass let `ACTIVE_POLICY_POINTER` substantiate the loaded leg | `BOUND`, `loaded_on_host=false` | `POLICY_LOADED_PROVENANCE_NOT_A_LOAD_RECEIPT` |
| H4 | `LEG_PROVENANCE["owner_approved"]` named two provenances and the module opened **neither** | a hand-typed dict with that label plus the source digest bound | `POLICY_OWNER_APPROVAL_UNSUBSTANTIATED` |

H4 is the one that mattered: it is what stood between a five-leg chain and `BOUND`. The rule it
illustrates is general — **a provenance label with no reader is a forgery hole**, and every leg should
be asked the same question: *which function reads this artifact?*

## 2. What the patch adds

* `host_load_receipt.py` — re-derives the policy digest from bytes and structurally validates a
  producer/process block (positive pid, plus a process-create instant, a 64-hex process identity, or a
  boot epoch).
* `owner_approval_receipt.py` — `OWNER_APPROVAL_RECEIPT@1` / `POLICY_OWNER_DIRECTIVE@1`: detached
  Ed25519 signature over the canonical body, an approving principal (OS SID + role) that is **not** the
  reading process, an ordered unexpired window, and digest equality with the bytes on disk.
* `build_binding(load_receipt=, owner_receipt=)` — the fifth and third legs now go through those
  readers. `owner_trusted_key_ids=` optionally pins the key id to a registry the caller owns; without
  it the result reports `key_trusted: False` and the binding refuses to *claim* key provenance.

## 3. The wiring matrix (reproducible)

Run `inc5/candidates/run_binding_r6_d17.py` from the round directory. It loads this consumer, feeds the
**real** `HOST_LOAD_RECEIPT@1` and `HGK_CONSUMER_RECEIPT@1`, and uses a **FIXTURE**-signed owner
approval only to reach `BOUND`.

| case | what it supplies | result |
|---|---|---|
| P1 | typed owner leg, **no receipt** | REFUSED `POLICY_OWNER_APPROVAL_UNSUBSTANTIATED` |
| P2 | FIXTURE-signed approval | **BOUND**, `claim_ceiling=AUTHOR_DESIGN_ONLY` |
| P3 | body edited after signing | REFUSED `OWNER_RECEIPT_SIGNATURE_INVALID` |
| P4 | key id absent from `owner_trusted_key_ids` | REFUSED `OWNER_RECEIPT_KEY_UNTRUSTED` |

Measured on: `policy_binding.py` `dddd1764e6ce4ec9…`, `owner_approval_receipt.py` `7157d507b478687d…`,
source and stage both `93ec36da…`.

**A FIXTURE signature proves the leg is wired and verifiable. It is not an owner approval**, and
`BOUND` at `claim_ceiling=AUTHOR_DESIGN_ONLY` does not mean the policy is in force.

## 4. Test evidence

* 47 hole tests fail on the pre-patch module (39 failures, 7 errors, all "ACCEPT where REFUSE was
  required"); 87 tests pass after.
* Every pre-existing refusal code is preserved and re-asserted
  (`test_every_pre_existing_code_is_still_emitted`).
* Regression: the six-leg build without `owner_approved` still returns `POLICY_BINDING_INCOMPLETE`
  before and after.

## 5. What is still owed

An `OWNER_APPROVAL_RECEIPT@1` signed by a **real** owner key whose `key_id` is pinned, over the policy
bytes and scope this binding names. That is an owner act; the issuer tool for it exists in the round
worktree but the agent never runs it against a real key. Until then this stays a candidate.

## 6. Two open contract questions for the maintainer

1. Should `HGK_CONSUMER_RECEIPT@1` itself require a producer/process block, the way the load receipt now
   does? Today the ack leg is verified by digest and re-read, but its producer is not structurally bound.
2. Where should owner-key provenance live? `owner_trusted_key_ids` is a caller-supplied registry today;
   if it should be a signed registry of its own, that is a contract change and belongs in a separate PR.
