# WS-B WRITER BRIEF — rebuild the R7-0 validator hardening on `main` and re-measure the 18 mutations

Round `CNV-PIPD-LS-SP-20261015` / ChangeSet `R8-0`. HGK project `CNV-R8-SKILL-SLIM-EIA-CLOSURE`.
Authority: PKG v2.0.0 + EIA-R6-04. Closes `BLK-R7-WS1-STALE-BASELINE` (high) carried from R7.
Claim ceiling: **LOCAL / candidate-only**; a green local run is not an acceptance and not a Gate PASS.

## Why this turn exists
R7-0 hardened three product files and measured the 18 mutations, but the hardening was authored against
`9bd33a1` (the r5q tip) — **not** against `main`. The external acceptance report (EIA-R6-04) requires that
`M04`/`M06`/`M16` be refused by the validator that ships; that property has only ever been measured on the
`9bd33a1`-derived tree. This turn rebuilds the same change on `main` and re-measures, so the claim stops
depending on a stale base.

## Verified anchors (independently re-checked before this brief was written)
| file | `9bd33a1` (= R7 pre-change) | `main` `dba4b19` | R7 post-change (target semantics) |
|---|---|---|---|
| `src/pipd_ls_sp/validate.py` | `f3da9e413cda1c7d…` | `50d69fe651cadebe…` | `5a298eb50685a9e3…` |
| `src/pipd_ls_sp/pipeline.py` | `620a5f4f03458697…` | `ace1c68c5cf2c5ac…` | `844bc5433252b2dc…` |
| `src/pipd_ls_sp/cli.py` | `29470f7f77214bea…` | `cc97660b079f7c4f…` | `eb7c54293862129d…` |

## Inputs (absolute paths)
- Product repo: `C:/Projects/Agent_Workspace/PIPD` (remote = `shw097-team/PIPD-LS-SP`). **Do not modify its
  working tree, its index, or its current branch.**
- R7 round artifacts: `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R7/`
  — `R7_VALIDATOR_DIFF.patch` (+193/−6), `R7_WRITE_SET.json`, `R7_MUTATIONS_18_RERUN.json`,
  `RAW/pre_change/{validate.py,pipeline.py,cli.py}` and the R7 post-change copies under `RAW/`.
- Mutation driver (reuse verbatim, redirect constants only):
  `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/R6_DELIVERY/RUNNERS/{probe_mutations.py,probe_lib.py,run_mutations.py}`,
  baseline `…/R6_DELIVERY/MUTATIONS_18.json`, source doc `…/R6_DELIVERY/RAW/pipd_scratch_source.md`.
- Your work root: `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8/WS_B/`

## Steps (in order; record every command, exit code and raw output)
1. Create a **new** detached worktree at `main`:
   `git -C C:/Projects/Agent_Workspace/PIPD worktree add --detach C:/Projects/Agent_Workspace/PIPD/worktrees/r8-wt dba4b19`
   Record `git -C …/r8-wt rev-parse HEAD` and confirm the three file shas equal the `main` column above.
   (Work only inside `…/worktrees/r8-wt`. If the path exists, stop and report — do not reuse or delete it.)
2. Reproduce the R7 change **on `main`**, as a semantic patch, not a blind file copy:
   - Derive it from the R7 pair (`RAW/pre_change/<f>` → R7 post-change `<f>`) with a real diff, then apply
     that diff to the `main` versions of the three files (`git apply -3` inside the worktree, or hand-resolve
     the resulting hunks — no other route).
   - Two hunks are known to conflict: `cli.py` around line 163 and `validate.py` around line 14
     (`CLAIM_LADDER` region). Resolve them **by preserving `main`'s surrounding code and re-expressing only
     the hardening intent**; if the intent cannot be expressed without guessing, STOP, record the blocker with
     the conflict text, and do not commit a guess.
   - Save the rebased patch as `WS_B/R8_0_REBASED.patch` and, per file, `WS_B/post/{validate.py,pipeline.py,cli.py}`.
   - Each rebased file must differ from its `main` counterpart **only** in the hardening's own hunks; list
     every changed hunk with line ranges in the receipt.
3. Run the repository test suite inside the worktree. Record the exact summary line and the failure list,
   and compare it against the R7 run's `7 failed, 319 passed, 2 skipped, 34 subtests passed`. Explain any
   difference caused by `main`'s own divergence — do not "fix" tests to make numbers match.
4. Re-run **all 18** mutations against the worktree tree: copy the three runner files into `WS_B/RUNNERS/`,
   change only these constants — `PIPD_SRC` → `…/worktrees/r8-wt/src`, `SCHEMAS` → `…/worktrees/r8-wt/schemas`,
   `RAW` → `WS_B/RAW` — and copy `pipd_scratch_source.md` into `WS_B/RAW/`. Note in the receipt that the
   driver is the R6/R7 one with constants redirected (no logic change); include the `diff` of the runner files
   as proof.
   Required: `M04`, `M06`, `M16` must be `REJECT`; the 7 previously-detected ids must stay detected; the 8
   `NOT_RUN` ids must each be re-judged with a reason (`NOT_CONSTRUCTIBLE_<why>` or an actual run) — do not
   silently drop them.
5. Write `WS_B/R8_MUTATIONS_18_ON_MAIN.json` (same row shape as `R7_MUTATIONS_18_RERUN.json`:
   id / mutation / expected / observed / validator_verdict / first_fail / raw_receipt, plus
   `base_commit`, `product_tree`, `driver_diff_sha256`) and `WS_B/WS_B_RECEIPT.md`.
6. Clean up only your own worktree metadata if you created and no longer need it — otherwise leave `r8-wt`
   in place; the orchestrator will re-measure from it. Never remove worktrees you did not create.

## Hard constraints (a violation voids your turn)
- Write only under `WS_B/` and inside `…/worktrees/r8-wt`. Nothing else.
- No outbound network write of any kind; no operation against any remote; do not touch `origin`; do not create branches that
  could be mistaken for a release to any outside host.
- Do not modify `C:/Projects/Agent_Workspace/PIPD`'s working tree, index, branch, or its other worktrees.
- Do not read, copy or print credential material.
- Do not run the 221 acceptance cases, do not claim any Gate PASS, do not upgrade any verdict, do not claim
  production readiness.
- If a step fails, record the blocker with raw output and continue with the remaining steps where they do not
  depend on it. An honest partial is the required outcome.
