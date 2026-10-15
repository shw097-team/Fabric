# WRITER BRIEF — R7-0 ChangeSet `R7-0-VALIDATOR-AND-CHECKER-ISOLATION`

You are the **bounded writer** on the EXECUTE lane (Codex CLI, provider/model `opencode-go/deepseek-v4.1-flash`),
admitted through HG-KSEOS. Claim ceiling is **LOCAL / candidate-only**: you do not accept, approve, release or
promote anything, and you do not write a checker verdict about your own work.

## Context you may rely on (all read-only)
- External review: `EIA-FABRIC-CONVERGENCE-R6-20261015`, findings **EIA-R6-04** (HIGH) and **EIA-R6-03** (HIGH).
- R6 raw failure evidence: `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/R6_DELIVERY/MUTATIONS_18.json`.
  Executed 10, detected 7, **not detected 3**: `M04` ProfileBinding ASSURED replaced by LITE,
  `M06` domain oracle expected changed to 999, `M16` trace atom digest mismatched. Expected result for all three is REJECT.
- Mutation driver: `.../R6_DELIVERY/RUNNERS/run_mutations.py` + `.../probe_mutations.py` (reuse them; do not rewrite the driver).
- Bound validator: `C:/Projects/Agent_Workspace/PIPD/src/pipd_ls_sp/validate.py` (`validate_record`,
  `semantic_invariants`, `validate_bundle`, `_body_hash`) plus the callers `pipeline.py` / `cli.py`.

## PRIMARY deliverable — make the three blind spots deterministic REJECTs
1. `M16 trace digest`: recompute each trace atom's digest from its own body and compare with the recorded digest
   (the record's identity/hash rule already exists for release-bound families via `_body_hash`; trace atoms are
   currently unchecked). A mismatch must produce a finding.
2. `M06 oracle expected`: the acceptance/oracle expected value must be bound to the frozen acceptance source
   (the frozen PI/acceptance digest carried by the bundle/context), not merely present as a number. A tampered
   expected value (e.g. 999) must produce a finding.
3. `M04 profile assurance downgrade`: a ProfileBinding whose assurance is weaker than the frozen requirement
   (ASSURED→LITE) must produce a finding. If the frozen requirement is not available to the validator, the
   validator must **FAIL CLOSED** with an explicit `UNBOUND_FROZEN_CONTEXT` finding instead of silently passing —
   a missing binding is not a pass.

Wiring rule: extend the validator API with an optional frozen/context argument and make the pipeline pass it.
Do not change the meaning of existing contracts, do not weaken any current predicate, and keep validation
deterministic (no LLM judge anywhere in the path).

## SECONDARY deliverable — checker write-root isolation (EIA-R6-03)
Provide a runner-level wrapper used by the VERIFY lane so that, while a checker reviews a subject, the candidate
root cannot be written: give the checker an isolated write root and apply an OS-level deny-write to the candidate
root when possible. Prove it with a **denial fixture** that actually attempts a write and is refused.
If an OS-level ACL cannot be applied in this environment, you must record `ACL_UNENFORCEABLE` with the exact
command and error — never claim isolation you did not achieve. A copy-based workaround is acceptable only if it
is described as such.

## Required outputs (write ALL of them, in this directory)
`C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R7/`
- `R7_VALIDATOR_HARDENING.md` — what changed, per blind spot: predicate, file, line, and the reasoning.
- `R7_MUTATIONS_18_RERUN.json` — re-run of the existing driver: one row per mutation with
  id / mutation / expected / observed / validator_verdict / first_fail / raw_receipt, plus totals.
  **Acceptance: M04, M06, M16 become REJECT, and the 7 previously detected mutations stay REJECT.
  The 8 mutations that were NOT_RUN stay NOT_RUN — do not fabricate executions.**
- `R7_WRITE_SET.json` — every file you changed: absolute path, bytes, sha256; plus the pre-change sha256.
- `R7_WRITER_RECEIPT.json` — what you ran, exit codes, the exact commands, the model/provider actually served,
  and an honest list of anything you could not do.
- `RAW/` — raw stdout/stderr of every command you ran (driver rerun, denial fixture, any unit check).
- a unified diff of every changed source file, as `R7_VALIDATOR_DIFF.patch` (produced with `git diff --no-index`
  or `diff -u`; the PIPD tree is not a git repository).

## Hard constraints
- Do **not** modify `EVIDENCE/CNV-PIPD-LS-SP-20261015/**` (already merged and byte-bound) or any Fabric repo file.
- Do **not** run any git write command and do not send anything to any outside host: leave both working trees
  exactly as you find them (no commits, no outbound network calls, no repository API calls).
- Do not touch the HG-KSEOS Shared Spine, its config, or any WorkOrder state.
- Do not read or print credential material; never place a token in argv, a URL, a log or an artifact.
- Do not run the 221 acceptance cases, do not claim any Gate PASS, do not upgrade any verdict.
- If a required condition cannot be met, stop and record it as a blocker with the raw error — a partial result
  reported honestly is the required outcome, a fabricated pass is a failure.
