# Probe and claim discipline when you are the one re-deriving a repair

You are the third party re-running someone else's claimed fix. Two failure modes bite here, and both
make YOU the error source rather than the code.

## A false RED from a mis-shaped probe inventing a defect

When your reproduction reports a NEW defect (classically "it over-blocks now", "too strict"), suspect
the PROBE's input shape before the code. Measured case: a probe hand-built config entries with an
`origin` key while the code needed a `scope` key to resolve precedence, so every realistic input
returned `INCONCLUSIVE` and read as an over-block -- yet the writer's own control passed, because it
used the real shape.

Rule: find the test that drives the real pipeline and copy ITS entry shape before calling anything a
defect. Contradicting the writer's own control is a signal to re-shape the probe, not a finding. If you
already reported it, retract in writing and record the self-correction where the round's evidence
lives: a withdrawn false defect costs nothing, a recorded false defect costs the round's credibility.

## Transient vs durable -- verify the state the caller actually uses

A claim/mutex API can expose a transient mode (acquire, report, release) alongside a durable
tombstone mode (consumed). In the transient mode two concurrent claimants BOTH succeed; only the
durable state excludes them. Measured: a clean concurrency probe returned two winners against the
default claim, while the dispatcher's real path consulted the consumed tombstone first and refused the
second with a typed already-consumed error at zero attempts.

Rule: test mutual exclusion / single-use against the state the PRODUCTION caller relies on, and state
the property exactly as verified ("within one dispatch flow the authorization is consumed once")
rather than the broader claim your probe did not establish ("any two concurrent claims must have one
loser"). Overstating the verified property is the same class of error as the false green it was meant
to prevent.

## Do not let a same-model checker inherit a PASS

When the owner's mandate binds the writer lane and the checker to the same provider/model, the verdict
is ADVISORY. Record the deviation verbatim (`sod_axis_model: NOT_SATISFIED`), put it in the verdict
itself, and state that it does **not** supersede the last different-model verdict on the same subject --
which stays on record as the strongest evidence while the advisory is only a re-derivation. The
correlated blind spot is the named failure mode and cannot be excluded from inside the same model; say
so plainly instead of performing confidence.
