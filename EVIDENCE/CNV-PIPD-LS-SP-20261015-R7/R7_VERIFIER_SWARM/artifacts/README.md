# R7-0 product-side candidate — EVIDENCE ONLY, base-bound to `a503efe`

Mission `CNV-PIPD-LS-SP-20261015`, change set `R7-0-VALIDATOR-AND-CHECKER-ISOLATION`.
Claim ceiling: **LOCAL / candidate-only**. This branch is evidence. It applies **nothing** to `src/`, and it is
**not** a merge request for product code.

## Why nothing is applied
The R7-0 change was authored in a workspace copy of the product that is **not** current `main`:
- the writer's pre-change snapshots are byte-identical to the blobs of commit **`a503efe`**
  (`ce840caadca8` validate.py, `7f21aa84c4ae` pipeline.py, `69095baeb68a` cli.py);
- `main` is **`dba4b19456777d3b597fdf71480f6423dd974243`** with different blobs for all three files
  (`7c3145cd002b`, `75799b744e8a`, `4a2e13fbbdd7`).

So the patch is a delta **against `a503efe`**. Copying the candidate files onto `main` would revert intervening
work — the net `main` → candidate delta is +164/−158 lines in `validate.py` alone, including the CE-2
refinement block. A mechanical rebase does not apply cleanly either: `pipeline.py` applies (`rc=0`) while
`validate.py` and `cli.py` conflict (`git apply --check` `rc=1`). See `REBASE_MEASUREMENT.json`.

## What is here
- `candidate_files/` — the three post-change files exactly as produced by the R7-0 writer
  (sha256 below). Evidence copies: do **not** copy them over `src/`.
- `delta/*.delta.patch` — the pure R7-0 delta (writer snapshot → candidate), i.e. what the change actually adds
  on top of `a503efe`.
- `REBASE_MEASUREMENT.json` — the measured apply/conflict result of each delta against current `main`.
- `WS1_BLOCKER_STALE_BASELINE.json` — the blocker record, with the three remediation options.
- `WS1_PIPD_COPY_VERIFICATION.json` — the byte verification of the copy step (baseline vs writer record vs candidate).
- `R7_WRITE_SET.json`, `R7_VALIDATOR_DIFF.patch`, `R7_MUTATIONS_18_RERUN.json`, `R7_WRITER_RECEIPT.json`,
  `R7_CHECKER_DISPOSITION.md` — the round's own records for context.

## What is NOT claimed
- No merge, no apply, no release, no acceptance.
- The R7-0 mutation result (M04/M06/M16 → REJECT) is measured on the **`a503efe`-derived** tree. It is
  **UNMEASURED** on any `main`-based rebase until the 18-mutation re-run is repeated there.
- The suite result attached to the round (`7 failed / 319 passed / 2 skipped`) is likewise tree-bound; the seven
  failures are pre-existing on a baseline run and are unrelated to the change.

## Re-verification (no credentials needed beyond repo read)
1. `git cat-file blob ce840caadca8` and compare with `candidate_files/` lineage — the base is `a503efe`.
2. `git apply --check delta/validate.py.delta.patch` against `main`: expect `rc=1` (conflict), matching
   `REBASE_MEASUREMENT.json`.
3. Recompute sha256 of each `candidate_files/*` and compare with the table below.
4. The independent checker verdict and the full packet live in the Fabric repo, branch
   `evidence/cnv-pipd-ls-sp-20261015-r7`, prefix `EVIDENCE/CNV-PIPD-LS-SP-20261015-R7/`
   (authoritative checker verdict at `R7_CHECKER/R7_CHECKER_VERDICT.json`).

## sha256 of the candidate files
- `validate.py` — 18422 B — `5a298eb50685a9e3185c21dd15560d1a77601ee871b58cbc3dba0df7c746e701`
- `pipeline.py` — 22461 B — `844bc5433252b2dc2327bb8c03297106489fdc1b8a35285da231a76f2909445f`
- `cli.py` — 18147 B — `eb7c54293862129d27423617c7f7dcc6410bff1b38d54589e58180f6db4af86c`
