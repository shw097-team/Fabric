# Probe shape and false red

A verifier's own fixture is a **hypothesis about the producer's shape**, and a wrong hypothesis
produces a confident WRONG FAIL. It is the mirror of a false green: the check now reports failure
exactly when the probe, not the subject, is malformed.

## The rule

**Reconstruct the fixture in the shape the REAL producer emits before writing up a defect against a
fix.** Either read the producer's resolution path, or start from the writer's own passing fixture and
vary ONLY the field under test. A refusal you cannot reproduce with the producer's shape is your
probe's bug, not theirs -- and reporting it costs the round's credibility.

Measured case: a probe hand-built config entries under one key name while the real resolver emits
another, so the code could not resolve an entry's scope, returned `INCONCLUSIVE` for every realistic
input, and the probe looked like proof of an over-block regression. Switching to the producer's shape
turned every realistic input into `PASS`. There was no defect.

## How to tell a real refusal from a probe artefact

Before escalating, run the three-way check:

1. **Producer parity** -- does the input match what the code that will call this in production emits?
   Copy the writer's own fixture; vary one field.
2. **Honest control** -- the shape the design intends to ACCEPT must still pass. A probe set where
   *everything* refuses is the signature of a probe bug, not a strict guard.
3. **Production path** -- run the real end-to-end gate. If the production gate reports CONTINUE/PASS,
   a probe-level refusal is not a regression.

A six-variant probe set that all refuse, followed by one end-to-end gate that passes, means the probe
was wrong. Do not publish the alarm before the gate has spoken.

## Withdrawal discipline

When a claim you already voiced is contradicted by better probing:

- Withdraw it **explicitly and immediately**, in the same channel it was raised.
- State that it was never written up as a defect (so no reader hunts for a defect that does not exist).
- Record the withdrawal in the round's own receipt --- a retracted alarm must not survive into a later
  summary or a final report.
- Keep the withdrawal costless to the round: a probe bug you caught yourself is evidence the check is
  real, not a blemish to be quietly dropped.

## Related traps

- A three-valued verdict (`PASS` / `FAIL` / `INCONCLUSIVE`) is only as good as the fixture: an
  `INCONCLUSIVE` produced by a missing key is indistinguishable, in the output alone, from an
  `INCONCLUSIVE` produced by a genuine unknown.
- Prefer the writer's own test fixture over a hand-built one when the writer already proved the
  honest shape passes.
