NONCE-ECHO: FAR-EXECUTE-DAF3215D

# EXECUTE brief

Question:
In under 150 words: a governed research round must leave three lane receipts. Name the one structural reason a maker skips them, and the one mechanism that removes it.

PLAN output:
I’ll read the referenced brief and repository instructions to identify the requested work and its execution gates.
NONCE-ECHO: FAR-PLAN-2CA6B375

The structural reason is that the maker controls both execution and closure: if receipts remain optional attachments, it can finish the work and declare completion without dispatching all three lanes.

The mechanism is a mandatory, fail-closed closure gate outside the maker’s discretion.

For closure to succeed, PLAN, EXECUTE, and VERIFY_SECURITY must each have a valid receipt bound to the same round and mandate. Each receipt must prove the required arm actually served, with matching lane, permitted rank, nonce, usage evidence, and successful exit. Missing or invalid evidence must block closure.

EXECUTE should build one work package: enforce this gate at every round-closing entry point, with deterministic tests for valid receipts, missing lanes, mismatched arms, stale bindings, and bypass attempts.

This is a candidate proposal; no dispatched PLAN receipt is claimed.

Build exactly one work package from the plan. Do NOT read the repository and do not go looking for governance files -- everything you need is in this brief; measured, a build brief that sends the arm into the repo stalls past 600s, the same brief kept self-contained finishes in 14s. Report what you produced.

Begin your reply with the nonce line exactly as given above, verbatim.
