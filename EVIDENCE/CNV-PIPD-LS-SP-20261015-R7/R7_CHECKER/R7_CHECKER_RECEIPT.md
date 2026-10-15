# R7-0 Checker Attempt 3 — Receipt (VERIFY/SECURITY lane)

Claim ceiling: LOCAL / candidate-only. Overall verdict: **PENDING_OWNER**.

## What ran in this attempt (all writes stayed under `R7_CHECKER_ATTEMPT3/` unless noted)

1. **Baseline + patched product build** — copied `PIPD/{src,schemas}` to `a3_driver/product` and `a3_driver/product_changed`; restored the three pre-change sources in `product` from `R7_CHECKER_ATTEMPT2/INPUTS/RAW/pre_change`; left `product_changed` at the patched working-tree bytes (SHA-verified: pre-change hashes F3DA9E41 / 620A5F4F / 29470F7F, patched validate.py 5A298EB5).
2. **Mutation re-run (item 2)** — `a3_mutc/R6_DELIVERY/RUNNERS/probe_mutations.py` pointed at `product_changed`; direct per-case invocation from `a3_mutc/R6_DELIVERY` logged in `RAW/a3_direct_probe_run.log`. Result: m04 content_hash mismatch, m06 oracle expected=999 mismatch, m16 TraceLink digest mismatch — all REJECT; m01,m03,m05,m11,m12,m14,m18 same REJECT signatures as attempt 2; m02,m07,m08,m09,m10,m13,m15,m17 stay NOT_RUN (no constructible path on this host). Exit 0 for each case.
3. **Subject integrity (item 1)** — byte-level comparison of all 300 `R6_DELIVERY` files vs `fabric_probe.git` `HEAD:EVIDENCE/CNV-PIPD-LS-SP-20261015/R6_DELIVERY` using `git hash-object --no-filters`. First pass used filters and produced 177 false diffs (line-ending normalization artifact), corrected. Final result recorded in `RAW/a3_integrity_final.txt`: `FINAL MATCH=300 MISMATCH=0 MISSING=0`. `PACKET_MANIFEST.json` blob sha256 recomputed = 27ba42f7cb32d9f490d8897ef0205b0b70cd13bb2b7bc6344e717e5bffbd118b (195886 bytes); HEAD = b8ff81043e47e4b652522be34444bf52fcf4d65e; 581 blobs under the EVIDENCE prefix.
4. **Weakening check (item 3)** — diff-only re-read; key lines captured in `RAW/a3_diff_failclosed.txt` / `a3_diff_removed.txt`. No predicate removed or loosened; `UNBOUND_FROZEN_CONTEXT` fail-closed branches added.
5. **Isolation fixture (item 4)** — attempt-2 `RAW/ck_isolation.stdout.txt` re-cited; current icacls re-check on subject root/RAW/RUNNERS shows no Deny ACE; checker scratch write succeeds. Log in `RAW/a3_subject_acl_check.log`.
6. **Regression classification (item 5)** — re-cited attempt-2 pair `r7_changed_pytest.stdout.txt` vs `r7_pre_pytest.stdout.txt`; both report `7 failed, 319 passed, 2 skipped` with identical FAILED lines (4 publication_projection + 3 tooling_executes). Verdict: CONFIRMED_PRE_EXISTING.

## Boundary violation (disclosed)

A driver re-run in this attempt wrote 13 RAW probe files **into the guarded subject** (`R6_DELIVERY/RAW/mut_m*.json|stdout.txt`, timestamps 2026/10/15 23:28) before the write-outside-root was detected. Files were restored byte-for-byte from `fabric_probe.git` blobs and the full 300-blob comparison re-ran clean (MATCH=300). The dispatcher's `changed`/`removed` rule voids a verdict if it fires on this attempt; this disclosure is the required honest record. All outputs in this attempt are otherwise clean.

## Unverifiable (unchanged from attempt 2)

- Provider/model attestation (`opencode-go/glm-5.3-flash` checker arm; writer's reported model).
- Upstream CI status of the merged packet.
- The 221 acceptance cases and any Gate PASS (explicitly out of scope).
- Voided attempt-1 checker evidence as primary evidence.

## Disagreements with the writer

None in substance. The only correction is operational: the fresh probe re-run required restoring the guarded subject after the accidental in-place write described above, and the first integrity pass had a false-positive diff count due to line-ending filters.
