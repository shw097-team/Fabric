# Verifier swarm attempt: raw evidence present, NO named verdict emitted

The sealed Codex VERIFY/SECURITY lane (write root `R7_VERIFIER_SWARM/`) executed and left extensive raw evidence
(`RAW/` 31 files, scratch clones, `artifacts/` copies), but **did not write its two named deliverables**
(`R7_VERIFIER_SWARM_VERDICT.json`, `R7_VERIFIER_SWARM_RECEIPT.md`). Dispatcher: `EXIT 3`,
`code=ERR_NO_ARM_EMITTED_NONCE`, `completion_evidence.checked=false`, `usage_receipt_ok=true`; the subject guard
was **CLEAN** (`files_before=300 files_after=300 added=0 removed=0 changed=0`, digest
`d34c8e0ddcf40904fd5f9c765aa54769ead38400dc6cc040efa4fd5d57728425` unchanged).

So there is **no verifier verdict** in this round, and none is invented here. What follows is the **orchestrator's
reading** of the checker's own raw files — an input to the next verifier attempt, explicitly not a verdict.

## What the checker's raw evidence establishes (orchestrator reading)
1. **The base identity in the blocker record was wrong and is now corrected.** `RAW/base_blob_ids.txt` lists the
   three revisions' blobs: the candidate files' pre-change ancestors equal **`9bd33a1` (r5q)**, not `a503efe`
   (`a503efe` has different `pipeline.py`/`validate.py` blobs). See the corrected
   `WS1_BLOCKER_STALE_BASELINE.json`.
2. **Rebase re-measured on two revisions** (`RAW/rebase_check_9bd33a1? .txt`, `RAW/rebase_check_main.txt`):
   on `9bd33a1` all three deltas apply (`rc=0`) and `RAW/r5q_repro.txt` shows applied == candidate sha256 for all
   three files (so the candidate *is* exactly r5q + delta); on `main` `pipeline.py` applies (`rc=0`) while
   `cli.py` (`rc=1`, fails at line 163) and `validate.py` (`rc=1`, fails at line 14, `CLAIM_LADDER` region)
   **conflict**. The blocking conclusion is unchanged: the change does not apply to `main`, and the round's
   M04/M06/M16 result is measured only on the `9bd33a1`-derived tree.
3. **The self-check harness is not a rubber stamp — and it now FAILS.** Re-run by the checker
   (`RAW/selfcheck_fullrun.txt`): `1=PASS 2=FAIL 3=FAIL 4=PASS 5=PASS 6=PASS`,
   `OVERALL_SELFCHECK_VERDICT: FAIL`, `[repair 3] residuals remain: ['2','3']`. Checks 2 and 3 are the packet
   blob-set / manifest reconciliation, which still carry the **212-blob** expectation from the earlier packet
   commit; the packet now has **227 blobs**, so the harness correctly refused to pass on stale expectations.
   Consequence: the earlier "6/6 PASS" holds only for the 212-blob packet state, and the packet's recorded
   expectations must be regenerated after every commit (or the harness re-pointed at the live manifest).
4. Its `RAW/ws4_*` copies (36,919 B readback + 39,206 B summary + 19,553 B receipt) reproduce the WS4 inputs it
   was asked to re-derive; whether the WS4 claims themselves are CONFIRMED or CHALLENGED is **not decided here** —
   that is the missing verdict.
5. Scratch state left inside the verifier's own root (not part of the guarded subject): `pipd-clone/`,
   `pipd_wt_9bd33a1/`, `pipd_wt_a503efe/`, `pipd_wt_main/`, `scratch-clone-WS1/`, `scratch-clone-WS5[b]/`,
   `tmp_verify/` (~230 MB total). Excluded from the packet publication; to be removed once the verdict lands.

Claim ceiling: LOCAL / candidate-only; no verdict is claimed, nothing is accepted or approved.
