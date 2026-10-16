# R8 INDEPENDENT VERIFIER BRIEF — WS-A (skill-slim landing) and WS-B (R8-0 rebuild on `main`)

Round `CNV-PIPD-LS-SP-20261015` / ChangeSet `R8-0`. HGK project `CNV-R8-SKILL-SLIM-EIA-CLOSURE`.
You are the **Independent Acceptance Officer / verifier**. The makers were: an EXECUTE lane (WS-A, WS-B) and the
in-Hermes orchestrator (WS-C, WS-D). Your verdict is a claim with a ceiling of **LOCAL / candidate-only** — you
must not issue an acceptance, an approval, a Gate PASS, or a product statement.

## Scope of this turn
Two subjects, both already produced. Judge each claim on its own evidence; do not take a maker's summary as evidence.

### Subject 1 — the canonical skills tree landing (WS-A)
- Applied tree (read-only for you): `C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/skills/software-development/adversarial-verification-rounds/`
- Pre-image (the pre-apply bytes): `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8/WS_A/apply/preimage/`
- Maker artefacts: `…/CNV-PIPD-LS-SP-20261015-R8/WS_A/` — `WS_A_RECEIPT.md`, `apply/APPLY_RECEIPT.json`, `apply/rollback.py`, `s2_repair_result.json`, `s34_stale_refs_result.json`, `s5_loss_proof.json`, `rollback_drill_result.json`, `logs/`.
- Orchestrator checks to re-test yourself: `WS_A_REGRESSION_LIVE_POSTAPPLY.json`, `WS_A_INDEPENDENT_RECHECK.json`, `WS_A_REGRESSION_AVR.json`, `WS_A_REGRESSION_HGK.json`, `WS_A_HGK_APPLY_DECISION.json`, `WS_A_LIBRARY_SCAN.json`.
- Harness you may run (read-only): `…/CNV-PIPD-LS-SP-20261015-R8/ws_a_skill_slim_regression.py` with
  `--subject <tree> --live <pre-image-or-original> --out <your path>`; interpreter
  `C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe`.
Claims to test:
1. the applied main file is within the byte budget and its frontmatter starts at byte 0 with the right identity;
2. no instructional content was lost: main-file lines and every reference's bytes survive (the harness's C4/C6);
3. the apply receipt's `before/after` table is internally consistent with the pre-image and the applied bytes
   (recompute a sample — or all — of the sha256 values yourself, do not trust the table);
4. the rollback script actually restores the pre-image (reason about it from the code; do **not** execute it against
   the live tree — if you want a live drill, do it on a copy under your own write root);
5. the claim "the HGK candidate was NOT applied and why" is true (check the live hgk skill tree is unchanged and
   that the recorded losses — `lane-conformance-gate.md`, `step-verify-only-lane.md` — really do not survive in the candidate).

### Subject 2 — WS-B rebuild of the R7-0 hardening on `main`
- Round artefacts: `…/CNV-PIPD-LS-SP-20261015-R8/WS_B/` — `R8_0_DERIVED_FROM_R7.patch`, `R8_0_REBASED.patch`, `post/{validate.py,pipeline.py,cli.py}`, `RAW/` (pytest + mutation raw), `RUNNERS/` (the reused driver with redirected constants), and (when present) `R8_MUTATIONS_18_ON_MAIN.json`, `WS_B_RECEIPT.md`.
- Rebase worktree: `C:/Projects/Agent_Workspace/PIPD/worktrees/r8-wt` (detached at `dba4b19`, three files modified).
- Reference material (R7, for cross-checks): `…/CNV-PIPD-LS-SP-20261015-R7/R7_VALIDATOR_DIFF.patch`, `R7_WRITE_SET.json`, `R7_MUTATIONS_18_RERUN.json`, `RAW/pre_change/*`.
Claims to test:
1. the rebased files differ from `main`'s versions **only** in the hardening's own hunks (read the patch; list every hunk);
2. the three post-change files' sha256 values match what the maker recorded;
3. the test-suite summary is reproduced by your own run (report the exact counts and any difference from the R7 run's
   `7 failed, 319 passed, 2 skipped, 34 subtests passed` and from `main`'s own baseline);
4. the 18-mutation table: `M04/M06/M16` REJECT, the previously detected ids stay detected, and each `NOT_RUN` row carries a
   real reason. Re-run at least `M04`, `M06`, `M16` yourself against `worktrees/r8-wt` and paste the raw output.
5. the runner adaptation is constants-only (diff the runner files against the R6 originals and say so).

## Deliverables (write ONLY under `…/CNV-PIPD-LS-SP-20261015-R8/R8_VERIFY/`)
1. `R8_VERIFY/R8_VERIFY_VERDICT.json` — per claim: `CONFIRMED` / `REFUTED` / `UNVERIFIABLE`, with the command, raw output
   excerpt, and the exact bytes/shas you measured. Include `independent_verdict` (PER_CLAIM), `refuted` list,
   `unverifiable` list, `write_root` (your own), and a `claim_ceiling` string.
2. `R8_VERIFY/R8_VERIFY_RECEIPT.md` — what you ran, what you could not run and why, plus any counterexample you found.

## Hard constraints (a violation voids your turn)
- Read-only on both subjects. Your write root is `R8_VERIFY/` **outside** every subject; state it in the verdict.
- No git state changes (no add/commit/branch/remote). No network. No credential reads.
- Do not modify the canonical skills tree, the PIPD repo or its worktrees, or any `_handover/CNV-PIPD-LS-SP-20261015*/` file outside your write root.
- Do not run the 221 acceptance cases. Do not claim a Gate PASS, an acceptance, or production readiness.
- Report `UNVERIFIABLE` honestly where you cannot reproduce something rather than inferring a pass.
