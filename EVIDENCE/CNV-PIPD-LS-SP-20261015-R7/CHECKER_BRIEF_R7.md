# CHECKER BRIEF — independent verification of ChangeSet `R7-0-VALIDATOR-AND-CHECKER-ISOLATION`

You are the **independent checker** on the VERIFY/SECURITY lane (Codex CLI, provider/model
`opencode-go/glm-5.3-flash`). You are a different model and a different lane from the writer, and you are
**not** the Acceptance Officer: your ceiling is a candidate verdict `PENDING_OWNER`.

## What you are verifying
The writer claims, for ChangeSet R7-0:
1. the PIPD bound validator now rejects three tamper classes it previously accepted —
   `M04` ProfileBinding assurance downgraded ASSURED→LITE, `M06` domain-oracle expected value changed,
   `M16` trace-atom digest mismatch;
2. the seven mutations that were already detected remain rejected, and the eight that were never executed
   remain NOT_RUN;
3. it also delivered a checker write-root isolation wrapper with a real write-denial fixture.

## Inputs (read-only)
- Writer evidence: `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R7/`
  (`R7_VALIDATOR_HARDENING.md`, `R7_MUTATIONS_18_RERUN.json`, `R7_WRITE_SET.json`, `R7_WRITER_RECEIPT.json`,
  `R7_VALIDATOR_DIFF.patch`, `RAW/`).
- Pre-change baseline (for comparison): `.../CNV-PIPD-LS-SP-20261015/R6_DELIVERY/MUTATIONS_18.json` and the
  driver `.../R6_DELIVERY/RUNNERS/{run_mutations.py,probe_mutations.py}`.
- Changed product code: `C:/Projects/Agent_Workspace/PIPD/src/pipd_ls_sp/**`.
- Merged archive that must NOT have been touched: `EVIDENCE/CNV-PIPD-LS-SP-20261015/**` at main
  `b8ff81043e47e4b652522be34444bf52fcf4d65e` (its own readback binds 581 blobs and
  `PACKET_MANIFEST.json` sha256 `27ba42f7cb32d9f490d8897ef0205b0b70cd13bb2b7bc6344e717e5bffbd118b`).

## Required checks (each one: your own command, raw output, your own verdict)
1. **Re-run the mutation driver yourself** (not the writer's JSON) and compare with the baseline. State, per
   mutation: expected / observed / first-fail, and the totals.
2. **Read the diff** and judge whether any pre-existing predicate was weakened, bypassed, or made
   non-deterministic (an LLM or network call inside the validation path is a boundary violation).
3. **Fail-closed check**: with the frozen context unavailable, does the validator fail closed with an explicit
   finding (not silently pass)? Reproduce at least one such case.
4. **Positive/regression check**: valid, untampered records must still pass. Quote the command and result.
5. **Archive-untouched check**: independently confirm the merged archive under the R6/R6R7 prefix is unchanged
   (blob-id or API comparison), and that `main` has not moved.
6. **Isolation check**: attempt to write into the candidate root from the checker's position and report whether
   it was denied. If it was not denied, the verdict for that item is `ACL_UNENFORCEABLE` — **never a pass**.
7. **Full product suite + baseline comparison (required)**: the maker's complete run reports
   `7 failed, 319 passed, 2 skipped, 34 subtests passed` in `RAW/r7_pytest_full.stdout.txt`. The failing tests are
   `tests/test_publication_projection.py::{CliSmoke::test_write_then_check_exits_zero, CurrentTreeCoverage::*}` and
   `tests/test_tooling_executes.py::{test_cli_smoke_runs, test_export_manifest_has_no_vcs_paths,
   test_tracked_file_metric_excludes_vcs_internals}`, and the visible cause in several of them is
   `cannot resolve ref 'r5-s4-candidate' in C:\Projects\Agent_Workspace\PIPD\.git`.
   **Decide for yourself whether these 7 are pre-existing or introduced by the change**: run the same tests against
   the pre-change sources (the writer's pre-change snapshot is under `RAW/pre_change/`; copy them into a scratch copy
   of the tree rather than editing the live product tree) and report the comparison. A failure caused only by the
   change is a `CHALLENGED`; a failure that reproduces on the pre-change tree is `CONFIRMED_PRE_EXISTING`.
8. **Unverifiable claims**: list every writer claim you could not independently check, and why.

## Output (write ALL of these, nowhere else)
`C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R7/R7_CHECKER/`
- `R7_CHECKER_VERDICT.json` — schema `CNV-PIPD-LS-SP-20261015-R7/CHECKER-VERDICT/1` with
  `overall_verdict` (one of `PENDING_OWNER`, `CHALLENGED`), one row per check (id, claim, method, command,
  raw_evidence_ref, result `CONFIRMED`/`CHALLENGED`/`UNVERIFIABLE`, note), `unverifiable_claims`,
  `boundary_violations`, `first_fail`, and `claim_ceiling: "LOCAL, candidate verdict for the Owner"`.
- `R7_CHECKER_RECEIPT.md` — human-readable account of what you ran, what you found, and what you could not decide.
- `RAW/` — raw stdout/stderr for every command you ran.

## Hard constraints
- Do not modify the writer's outputs, the product source, or anything under `EVIDENCE/`. You may write only in
  your own `R7_CHECKER/` directory.
- Do not run any git write command and do not send anything to any outside host; do not call repository APIs to change state.
- Never read or print credential material.
- Do not run the 221 acceptance cases, do not claim any Gate PASS, and do not issue an acceptance or approval.
- A disagreement is a valid result: report `CHALLENGED` with the raw evidence rather than smoothing it over.
