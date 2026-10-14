# WO-SKCV-20261014-APPLY phase 2 — real guarded apply and rollback with immutable pre-image

Maker = Codex CLI opencode-go/deepseek-v4.1-flash. PLAN/oracle = current Hermes owner route. Checker = fresh GLM lane, not you. Bounded single step inside CWD candidates/apply; claim ceiling PARTIAL_APPLY_TOOLING. Keep the phase-1 validator and do not delete its phase1_result.json or fixtures.

Phase 1 delivered guarded_apply.py with validation and dry-run only; live apply and rollback are explicitly refused with ERR_LIVE_NOT_IMPLEMENTED. Deliver the real implementation now, still exercised only against your own fixtures under tests/_work:

1. Extend guarded_apply.py with an atomic writer: write to a temp file in the target directory, flush, then os.replace into place; never truncate a target in place.
2. Before any write, copy each target's exact current bytes into an immutable pre-image store inside the candidate root, keyed by target path plus digest, and keep a per-round ledger of every pre-image.
3. Re-check each target's digest immediately before its write and refuse with a typed stale-preimage error if it moved since validation; refuse the whole plan before touching anything if any pre-image is missing or stale.
4. After the write, read the bytes back and re-hash every target; a mismatch is a typed post-write error.
5. Implement rollback that restores each touched target from the pre-image store atomically, then re-hashes to prove exact original bytes are back. Rollback must refuse if an unrelated post-apply drift is detected on a target it would overwrite.
6. Keep the review/scope/binding gates from phase 1: an advisory review may gate this explicitly scoped owner-authorized local engineering operation but is NOT canonical authority; never mint an acceptance token, never self-grant, never widen an existing grant.
7. Add fixture tests executed against tests/_work only: successful apply with readback, rollback roundtrip restoring exact original bytes, stale pre-image refusal before any write, mid-failure compensation restoring all touched files, path-escape and junction refusal, and rollback refusal on post-apply drift. Name any case the host cannot supply and do not count a skip as a pass.
8. Record actual commands, the qualified interpreter, pass/fail/skip counts, named ran/skipped cases and every fixture request/response in phase2_result.json, labelling fixtures FIXTURE_ONLY, live_effects_claimed limited to the fixture roots, and listing what remains unwired (canonical admission-reader binding and any real-target authorization).

Constraints: no cap, threshold, policy or lock change; no write outside the candidate root; no claim of canonical acceptance; the fixture grants stay non-portable and must be labelled as such. Stop after step 8.
