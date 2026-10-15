# R7-0 checker disposition — which checker output is authoritative, and why

ChangeSet `R7-0-VALIDATOR-AND-CHECKER-ISOLATION`. Claim ceiling: **LOCAL / candidate-only**.

## The three attempts
| attempt | lane receipt code | disposition | what it is |
|---|---|---|---|
| 1 | `ERR_CHECKER_MUTATED_SUBJECT` (changed=14) | **VOID** | kept at `R7_CHECKER_ATTEMPT1_VOID/` with `DISPATCHER_VOID_ATTEMPT1.json`. The lane's own mutation re-run wrote its raw receipts in place over the frozen subject `_handover/CNV-PIPD-LS-SP-20261015/R6_DELIVERY/`. Correct guard behaviour. |
| 2 | `ERR_CHECKER_MUTATED_SUBJECT` (changed=0 removed=1) | **VOID (orchestrator fault)** | kept at `R7_CHECKER_ATTEMPT2_CONTENT_VOID/`. The single removed path was the gitignored byproduct `R6_DELIVERY/RUNNERS/__pycache__/probe_lib.cpython-311.pyc`, deleted **by the orchestrator**, not by the lane. The lane's own conduct in that turn was clean (added=0, changed=0). Its verdict JSON and 33 raw outputs are complete; the human-readable receipt was not written before the arm hit the lane limit. |
| 3 | `ERR_NO_ARM_EMITTED_NONCE` only (the known attribution defect, non-blocking) | **AUTHORITATIVE** | `R7_CHECKER/` — `R7_CHECKER_VERDICT.json` (schema `/3`), `R7_CHECKER_RECEIPT.md`, `RAW/`. Subject mutation: `added=0 removed=0 changed=0 → CLEAN`, with identical pre/post subject digests. |

**Read attempt 3 as the checker's verdict.** Attempts 1 and 2 are published for auditability only; they are not
evidence of anything except how the round went.

## What attempt 3 concluded
- Overall verdict `PENDING_OWNER`, `first_fail = null`, 0 boundary violations **left unrepaired**.
- `CONFIRMED` × 4:
  1. subject intact now — 300 `R6_DELIVERY` blobs equal `origin/main`, `MATCH=300 MISMATCH=0 MISSING=0`
     (its first pass reported 177 false diffs from a line-ending filter; corrected and re-stated);
  2. `M04`, `M06`, `M16` now `REJECT`, with mechanisms named (`m04` profile-binding content_hash mismatch on a
     body edit; `m06` oracle `expected=999` mismatch; `m16` TraceLink digest mismatch), and the seven previously
     detected mutations unchanged, eight still `NOT_RUN` (no constructible path on this host);
  3. no weakening — no predicate deleted or loosened; the 6 removed patch lines are call-site signature
     replacements; `UNBOUND_FROZEN_CONTEXT` fail-closed branches added;
  4. isolation fixture — two-phase raw output (write succeeds → deny ACE → write denied → ACL restored).
- `CONFIRMED_PRE_EXISTING` × 1: the product suite is `7 failed / 319 passed / 2 skipped` on **both** the changed
  and the pre-change trees, with identical failure lines → the 7 failures are not caused by this change.
- `UNVERIFIABLE` × 4: provider/model attestation for the served arm; upstream CI status; the 221 acceptance cases
  and any Gate PASS; and using attempt-1's voided evidence as primary evidence.
- **Disclosed boundary violation (by the checker, against itself):** during attempt 3 its driver re-run again wrote
  13 RAW receipts in place into the guarded subject before it detected this; it restored them byte-for-byte from
  the merged git blobs and re-verified `MATCH=300 MISMATCH=0`. Note the guard recorded `CLEAN` because it compares
  the subject digest before vs after the turn: **an intra-turn write-then-restore is invisible to it** (recorded as
  tooling finding `TF-09`). The orchestrator re-verified the subject after the turn: 300/300 blobs, 0 drift,
  0 extra files.

## What is NOT settled by any of this
- No acceptance, no approval, no merge authorisation, no Gate PASS, no production effect.
- The 221 cases, the gates `G-A..G-H`, the AUD-24 items and the effect planes remain untouched.
- Attempt 3's M04/M06/M16 rows were produced against a copy of the patched product sources under the checker's own
  root (`a3_driver/product_changed`, sha-verified) and are cross-checked against the live tree; the maker's own
  `R7_MUTATIONS_18_RERUN.json` remains a maker artifact.
