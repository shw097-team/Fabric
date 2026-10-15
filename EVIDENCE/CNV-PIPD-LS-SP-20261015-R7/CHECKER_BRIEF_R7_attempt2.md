# CHECKER BRIEF — attempt 2 (independent verification of ChangeSet `R7-0-VALIDATOR-AND-CHECKER-ISOLATION`)

You are the **independent checker** on the VERIFY/SECURITY lane (Codex CLI, provider/model
`opencode-go/glm-5.3-flash`). You are **not** the author of the change set. Report only what your own commands
show, and mark anything you cannot check as `UNVERIFIABLE`. Claim ceiling: **LOCAL / candidate-only**; your
verdict is a candidate for the Owner, never an acceptance, approval or merge authorisation.

## Why this is attempt 2 — read this first
Attempt 1 of this lane produced a substantive review, but the dispatcher **voided its verdict**:
`ERR_CHECKER_MUTATED_SUBJECT` — *"the guarded subject changed during the turn: changed=14 removed=0"*. The 14
changed files were all under the guarded subject
`C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/R6_DELIVERY/` (13 × `RAW/mut_m*.json|stdout.txt`,
plus `RUNNERS/mutation_records.json`): the re-run of the mutation driver wrote its raw receipts **in place** over
the writer's frozen receipts. The workspace copy has since been restored byte-for-byte from the merged packet
(`origin/main`, packet `EVIDENCE/CNV-PIPD-LS-SP-20261015`), recorded in `R6_DELIVERY_RAW_RESTORE.json`.
The **verdict was voided because the checker changed the subject, not because the review was wrong.** Redo the
work under a root where you cannot touch the subject.

## Write-root rules (a violation voids your own verdict again)
- Write **only** under `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R7/R7_CHECKER_ATTEMPT2/` (create it). Attempt 1's voided evidence lives in `…-R7/R7_CHECKER/` — read it, never write into it.
- **Never create, modify or delete anything under `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/`**
  — that tree contains the guarded subject `R6_DELIVERY/`. Treat it as read-only, and treat the merged git content
  as authoritative for it.
- To re-run anything that writes next to its inputs, **copy the inputs into your own root first**. In particular
  the mutation driver writes `RAW/mut_*.json` and `RUNNERS/mutation_records.json` beside the frozen records: copy
  `R6_DELIVERY/` into `R7_CHECKER/MUTCOPY/` (and the pre-change product snapshot, if used, into `R7_CHECKER/pre/`)
  and run everything there. Read-only *reads* of `R6_DELIVERY/` are fine.
- Your own evidence, verdict and raw outputs all go under your root. If you must run something that writes outside
  it, stop and record that as a blocker instead.
- Do not modify the product tree `C:/Projects/Agent_Workspace/PIPD/**` (the change under review lives there).
  Copy it if you need a scratch variant.

## Inputs
- Change set description: `…R7_VALIDATOR_HARDENING.md`, `…R7_VALIDATOR_DIFF.patch`, `…R7_WRITE_SET.json`,
  `…R7_WRITER_RECEIPT.json`, `…R7_MUTATIONS_18_RERUN.json`, raw outputs under `…RAW/` (all in the R7 dir).
- The maker's receipt names its own limits; read them and try to falsify each one.
- Frozen baseline: `…CNV-PIPD-LS-SP-20261015/R6_DELIVERY/MUTATIONS_18.json` and
  `…R6_DELIVERY/RUNNERS/probe_mutations.py` (read-only).
- Attempt 1's voided evidence is still on disk under `R7_CHECKER_ATTEMPT1_VOID/` (its own prior files, incl. a pytest output and
  an isolation re-run). You may read it as *prior work*, but every row you report must be backed by output **you**
  produced in this attempt under your root, and you must say where attempt-1 evidence was the only source.

## What to verify (same list as attempt 1)
1. **Mutation re-run (central claim)**: re-run the 18-mutation driver against the changed product tree, in your own
   copy. Confirm `M04`, `M06`, `M16` now yield `REJECT` and that the seven previously detected mutations still
   yield `REJECT`, and that the eight never-executed mutations are still `NOT_RUN`. Report the exact command and raw
   output. If any mutation's status moved the other way, that is a `CHALLENGED`.
2. **Weakening check**: read `R7_VALIDATOR_DIFF.patch` in full. Confirm no existing predicate was deleted or
   loosened, that the new predicates are reachable from the public entry points, and that the failure mode is
   fail-closed (a missing/ambiguous frozen context must produce a finding, not a silent pass).
3. **Blind-spot specifics**: for each of `M04` (profile-assurance downgrade), `M06` (oracle expected value) and
   `M16` (trace link/atom digest), show the mechanism that now rejects it and the exact evidence a reviewer can
   re-run. State plainly if any of the three is rejected for a reason other than the intended one.
4. **Determinism / no hidden oracle**: confirm the new checks depend only on the bundle and its frozen context,
   with no network, clock, randomness, or model call in the path.
5. **Archive integrity**: confirm from the repository (not from local files) that
   `EVIDENCE/CNV-PIPD-LS-SP-20261015/**` at `main` is unchanged: 581 blob ids, and
   `PACKET_MANIFEST.json` sha256 = `27ba42f7cb32d9f490d8897ef0205b0b70cd13bb2b7bc6344e717e5bffbd118b`.
   Also confirm the 14 restored `R6_DELIVERY` files now match the merged bytes (drift must be zero) — that is a
   check on the repair, not on the writer.
6. **Isolation check**: reproduce the denial fixture from your position: a write into the candidate root must
   succeed *before* the deny ACE, be **denied** after it, and the ACL must be removable/restorable afterwards.
   Report the raw output of both phases. If your environment cannot enforce it, the row is `ACL_UNENFORCEABLE` —
   **never a pass**.
7. **Full product suite + baseline comparison (required)**: the maker reports
   `7 failed, 319 passed, 2 skipped, 34 subtests passed`. Determine for yourself whether those 7 failures are
   pre-existing or caused by the change: run `python -m pytest tests -q` on the changed tree, then on a scratch
   copy with the pre-change sources from the writer's snapshot, and compare. Failures reproducing on both are
   `CONFIRMED_PRE_EXISTING`; a failure only on the changed tree is `CHALLENGED`.
8. **Unverifiable claims**: list every maker claim you could not check, and why.

## Output (write ALL of these, nowhere else)
`C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R7/R7_CHECKER_ATTEMPT2/`
- `R7_CHECKER_VERDICT.json` — schema `CNV-PIPD-LS-SP-20261015-R7/CHECKER-VERDICT/2`; per-item rows with `id`,
  `claim`, `method`, `evidence_path`, `verdict` (`CONFIRMED_PRE_EXISTING`, `CONFIRMED`, `CHALLENGED`,
  `UNVERIFIABLE`, `ACL_UNENFORCEABLE`), `note`; plus `unverifiable_claims`, `boundary_violations`, `first_fail`,
  `overall_verdict` (`PENDING_OWNER` or `CHALLENGED`) and `claim_ceiling`.
- `R7_CHECKER_RECEIPT.md` — human-readable: what you ran, exact commands, exit codes, what you checked, what you
  could not, and every place you disagree with the writer.
- `RAW/` — raw stdout/stderr of each command, incl. both pytest runs and both isolation phases.

## Hard constraints
- Do not modify the change under review, the product tree, or the guarded subject tree.
- Do not run any git write command, do not send anything to any outside host, and never read or print credential
  material.
- Do not run the 221 acceptance cases, do not claim any Gate PASS, and do not upgrade any verdict above
  `PENDING_OWNER` / `CHALLENGED`.
- If a required condition cannot be met, stop and record it as a blocker with the raw error — a partial result
  reported honestly is the required outcome; a fabricated pass is a failure.
