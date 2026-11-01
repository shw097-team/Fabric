I’ll read the brief and the applicable repository instructions to identify the requested work and its execution boundaries.
NONCE-ECHO: FAR-PLAN-FCD83136

The single structural reason is **maker-controlled compliance**: the maker can produce the research output and reach closure without dispatching all three lanes. Instructions leave receipt production dependent on the actor they constrain.

The single mechanism is a **mandatory, fail-closed round state machine** that owns dispatch and closure.

What must be true: every governed research round enters that state machine; its frozen mandate requires PLAN, EXECUTE, and VERIFY; no alternate path can mark the round complete. Each receipt must bind the round, nonce, subject, requested lane, and actually served arm, with valid usage evidence and successful exit. Missing, stale, mismatched, or inconclusive evidence must prevent closure.

EXECUTE should build one bounded work package: wire the existing dispatch and evidence gates into the authoritative round lifecycle so mandatory lane dispatch and receipt validation are unavoidable prerequisites to closure. Add deterministic tests proving a valid three-receipt round can close, omission of each lane prevents closure, and foreign receipts or alternate closure paths cannot bypass enforcement.

This response is planning content; it does not itself establish a passing PLAN receipt.