NONCE-ECHO: FAR-VERIFY-22EBD67A

# VERIFY brief

Question:
In under 150 words: a governed research round must leave three lane receipts. Name the one structural reason a maker skips them, and the one mechanism that removes it.

PLAN output:
I’ll read the execute brief and the governing instructions around that run, then follow the brief’s one-package scope and evidence requirements.
NONCE-ECHO: FAR-EXECUTE-DAF3215D

Produced one work package: **Round-Closure Lane-Receipt Gate**.

**Objective:** Every round-closing entry point must call one shared, fail-closed validator requiring valid PLAN, EXECUTE, and VERIFY_SECURITY receipts bound to the same round and mandate. Validation covers lane identity, required-versus-served arm, permitted rank, nonce, usage evidence, success status, and exit code. Missing or invalid receipts block closure with a named error.

**Deliverables:** shared validator, wiring for every closure path, deterministic positive/negative/boundary tests, raw test evidence, and rollback instructions.

**Required tests:** complete valid set; each lane missing; arm mismatch; stale round/mandate; invalid rank/fallback; invalid nonce/usage; and bypass attempts. Negative cases must otherwise satisfy closure so the targeted defect alone causes rejection.

No repository files were inspected or changed, and no implementation receipt is claimed.

Check the work against the question, not against the writer's summary. Decide PASS or FAIL and name what you relied on.

Begin your reply with the nonce line exactly as given above, verbatim.
