# Retrospective — ROUND3-LANE-REBIND-AND-CLOSURE-20261016

## What worked

* **Reuse over invention.** The round's tool chain (lane runner, admission, freeze, gate, packet builder,
  push/PR) came from the two previous rounds with path repointing only. The rebind itself reused the
  drift-driven pattern: edit the live site, let `check_drift` name every disagreeing binding, re-bind exactly
  those, prove zero errors.
* **The measured-first discipline paid off twice.** The guard's refusal of the mandated pair and the absence
  of an admission-receipt producer were both found by *calling the product*, not by reading it. Neither would
  have surfaced from a configuration audit.
* **The receipt-over-evidence rule caught my own defects.** A single unique-match assertion per literal edit
  turned a stale anchor into `EDIT NOT UNIQUE` instead of a silent wrong-row edit; `check_drift`'s
  `COVERAGE_GAP` caught the dropped field; the product's own YAML parser caught the unquoted note.
* **The mandated lanes were exercised for real.** The EXECUTE writer's turn is the first measured serving of
  `opencode-go/deepseek-v4.1-flash` in a code-writing role (`required_arm == served_arm`, rank 1, usage
  receipt OK), and its change was then promoted and independently re-checked.

## What did not

* **Three self-inflicted defects (SC-12/13/14) in one pass.** The backup-ordering defect was the worst: it
  removed the rollback preimage at exactly the moment the tree was being changed, and only a previous round's
  frozen copy saved it. Written corrections: back up before writing, quote scalars, restore bound fields.
* **An oracle expectation of mine was wrong**, not the product's behaviour: I expected `exit 0` with
  `--admission UNPROVEN`, which the guard can never return by design. The correction is recorded rather than
  silently tightened: the ADMIT path remains unproven and gap R11 stays open.
* **A workspace-walk search overran its window** (and tripped the very long-path failure the round had just
  corrected the record about) — bounded traversal with an error handler is the fix, now in the code.
* **The publication chain is inherited, not purpose-built for this round.** Its gates and its packet rules
  are the previous rounds' and were repointed; where a check no longer applies it was rewritten, but the
  chain still carries round-specific assumptions that had to be traced by hand.

## If this round were repeated

1. Write the guard-vs-registry agreement check *first*: it is the cheapest possible test of whether an
   owner-ordered configuration is dispatchable at all.
2. Compute every digest the plan will pin **before** editing, and hold the preimages outside the tree being
   edited.
3. Treat the pool, the fixture and the projections as part of the route row, and grep for every prose string
   that states the old default — prose is a declaring surface in this repository.
