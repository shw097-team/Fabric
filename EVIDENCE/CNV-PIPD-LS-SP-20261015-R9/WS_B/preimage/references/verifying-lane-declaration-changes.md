# Verifying a change to a governed lane declaration

Scope the verification to the DELTA. Auditing the whole declaration for "exhaustive consistency"
is how a small routing change turns into an afternoon.

## The failure pattern (observed, FAR-LANE-SOD-006)

The functional change - one default model's reasoning effort, plus a two-arm VERIFY route - was
implemented and gate-green about 30 minutes in. The round then ran ~1h45m longer because:

1. A verifier was asked "does the declaration agree with itself at EVERY active site?" and answered
   FAILS, naming nine stale-prose sites. Those sites were PRE-EXISTING debt from earlier revisions
   (retired NVIDIA arms named in prose, an old provider-separation narrative) and had no bearing on
   the change under test.
2. The repair for them was authored with an over-strict acceptance check ("the retired token must not
   appear anywhere"), which is unsatisfiable without rewriting immutable history. The writer resolved
   it the only way the check allowed - by replacing machine-readable identifier fields with prose -
   and that had to be repaired by a further round.
3. A verification verdict covering revision N was treated as covering revision N+1 after a repair,
   so an extra delta lane had to be spawned to close the gap.

## Rules

- **Write the verification mandate against the change, not the file.** "Verify the delta introduced by
  this change, and report pre-existing inconsistencies as out-of-scope notes" - never "verify the
  declaration is consistent everywhere". Whole-file consistency is a separate, opt-in audit.
- **Every acceptance check must name the region it applies to.** A global "must not appear anywhere"
  check in a file that carries history sections is a defect in the instruction, and the writer will
  satisfy it by degrading records. Say explicitly which regions are immutable history.
- **Never let a repair rewrite an identifier field to prose.** If a check forces a choice between
  passing the check and preserving a machine-readable record, the check is wrong. Carry the retired
  semantics in an additive field (`retired`, `retired_note`) and keep the identifier.
- **Bind every repair round to a revision.** After a repair the artifact revision advances, so any
  verdict produced against the previous revision is stale. Either re-verify the delta explicitly, or
  record the gap as an open item - never present the older verdict as covering the new head.
- **Know what the drift gate proves.** `check_drift()` compares only the pointers listed in
  `projections[].bindings`. A green gate says nothing about unlisted prose, so a clean gate is not
  evidence of a consistent document, and prose drift is invisible to it. State this whenever the gate
  is cited as evidence.
- **Verify with a diff against a byte pre-image.** Snapshot the declaration before every change and
  have the verifier enumerate changed JSON pointers from the pre-image itself, classifying each as
  intended or unintended. This catches scope overreach (extra edits nobody asked for) that no
  expectation-based gate can see.
- **Quoting a retired token in a changelog is legitimate.** A `revision_N_reason` string naming what
  was removed is history, not a defect. Do not chase it with a grep.

## Cheaper sequence for the same guarantee

1. Snapshot the file; record sha256.
2. Apply the change with the tracked writer; re-run the gate; confirm byte-identity of the JSON round-trip.
3. One independent lane verifies **the diff** plus the load-bearing claims (that the new value is the
   one the operator asked for, and that no expectation was weakened to make the gate pass).
4. One acceptance lane judges fit-to-hand-over. It must not accept.
5. Freeze once, at the end, after all writers have stopped - a freeze taken mid-flight is stale by the
   next receipt and forces a re-freeze.
