# W1 R2 — L0/L1/L2 write-back packet

The owner ruled that the evidence qualified but the authority had to be granted, and that an independent
review lane must certify the write-back first. This folder is that chain, end to end.

| file | what it is |
|---|---|
| `WRITEBACK_PROPOSAL.json` | the 12 amendments that were reviewed; each carries its layer, claim, evidence and non-claims |
| `LANE_WRITEBACK_REVIEW_R1.json` | round 1: 6 SUSTAIN, 2 REJECT, 3 missing → NOT_QUALIFIED |
| `LANE_WRITEBACK_REVIEW_R2.json` | round 2: 9 SUSTAIN, 1 REJECT, 3 missing → NOT_QUALIFIED |
| `LANE_WRITEBACK_REVIEW_R3.json` | round 3: 12 SUSTAIN, 0 REJECT, MISSING none → **WRITEBACK_QUALIFIED** |
| `WRITEBACK_VERDICT_R*.md` | each reviewer's verdict as returned, verbatim |
| `WRITEBACK_LEDGER.json` | per-layer before/after sha256, byte counts, prefix assertion, backup path |
| `REVIEW_CONVERGENCE.json` | the convergence audit: VERIFY 3→1→1→1→1→1→0 (monotone), write-back 3→3→0 |

Write method: **append-only**. Each layer file keeps every existing byte and gains a delimited annex
(`WRITEBACK:W1R2:2026-11-14:BEGIN/END`); the ledger asserts `after.startswith(before)` before and after the
write, and a timestamped copy of the original sits beside each file.

Claim ceiling: the amendments record measured facts and owner rulings. They do not assert native admission,
independent acceptance or release.