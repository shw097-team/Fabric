**Verdict**
- **V1 — PARTIAL.** Key injection is env-only at `ops/rotate_3lm_key.py:82`; only fingerprint/length are recorded at `ops/rotate_3lm_key.py:108`. A scan found zero exact credential hits across the three credential files and 25 workspace files. However, `ops/rotate_3lm_key.py:89`-`ops/rotate_3lm_key.py:93` persists unredacted child stdout/stderr into receipts or failure output, so secret safety depends on the probe never echoing the key.
- **V2 — PASS.** `ops/rotate_3lm_key.py:62` and `ops/rotate_3lm_key.py:64` skip backup/write when normalized pointers match, while `ops/rotate_3lm_key.py:118` always performs the probe. The second receipt shows both consumers `changed: false` and `probe.ok: true`.
- **V3 — FAIL.** Missing is code 2, but CR, empty, short, and multiline values all return code 3 at `ops/rotate_3lm_key.py:38` and `ops/rotate_3lm_key.py:41`. Malformed manifest JSON, missing manifest fields, probe timeout, and pin-backup failure also escape as untyped exit 1. The required empty/malformed distinction does not exist.
- **V4 — FAIL.** Each changed consumer is copied before write at `ops/rotate_3lm_key.py:64`, but mutation occurs at `ops/rotate_3lm_key.py:114` before the probe at `ops/rotate_3lm_key.py:118`. A probe failure exits before the receipt write at `ops/rotate_3lm_key.py:140`, leaving changed consumers without a receipt. The actual `r1_host_readback.py.bak-20261114-key` also does not match the runbook’s `.bak-<UTC>` rollback name at `RUNBOOKS/3LM_KEY_ROTATION.md:63`.
- **V5 — PASS.** The manifest declares the codex/provider/model probe at `ops/3lm_consumers.json:28`, and the key is injected through the child environment at `ops/rotate_3lm_key.py:82`. Receipts record exit 0 and `CHECKER_OK`; no HTTP endpoint is used as a gate.
- **V6 — FAIL.** Owner approval is correctly stated at `RUNBOOKS/3LM_KEY_ROTATION.md:70`, but `RUNBOOKS/3LM_KEY_ROTATION.md:28` says “本輪第一次乾跑” and `RUNBOOKS/3LM_KEY_ROTATION.md:82` says “2026-11-14 實測”. The requested `out/KEY_ROTATION.json` and `out/KEY_PROBE.json` are absent; only three dry-run/verify-only receipts exist.
- **V7 — PASS.** The design stays local and stdlib-only: file pointer, manifest, per-file backup, and manual restart. It adds no service, scheduler, secret store, or competing owner authority; the rejected alternatives align with `research-product/RejectedAlternativeLedger.tsv:2`.
- **V8 — PASS.** `research-product/ClaimLedger.tsv:2` declares two consumers; `ops/3lm_consumers.json:10` lists both; the loop at `ops/rotate_3lm_key.py:52` covers the manifest. Future consumers are addressed at `RUNBOOKS/3LM_KEY_ROTATION.md:90`.

**Most Serious Defects**
1. **Apply is not a safe transaction.** Consumers are mutated before validation, and probe failure leaves no receipt linking changes to backups. This directly undermines reversibility.
2. **Failure paths are not closed guarantees.** Empty and malformed keys share a code, several exceptions are untyped, and captured child output can bypass the intended fingerprint-only redaction.
3. **Evidence and scope do not match the claim.** The two named evidence files do not exist, no receipt records an `--apply`, and the runbook nevertheless claims this round was executed against the real credential.

**Simplifications**
1. Build and probe the complete plan first, then apply from that immutable plan using one run ID for every backup and the receipt. This removes post-write probe-failure reconciliation and timestamp mismatch.
2. Remove `--verify-only` because the non-mutating dry-run already performs the probe plus stronger consumer checks, and reduce pin refresh to a read-only drift report with an owner-applied diff. This removes one duplicate mode and one second write/backup path without weakening approval.

CLAIM_CEILING=LOCAL_CHECK_ONLY
