# WS-A RECEIPT — repair and guarded landing of the slimmed `adversarial-verification-rounds` skill

- Round: `CNV-PIPD-LS-SP-20261015` / ChangeSet `R8-0`; HGK project `CNV-R8-SKILL-SLIM-EIA-CLOSURE`, WorkOrder lineage `WO-TS-CLOSURE-01..04`.
- Authority: PKG v2.0.0 G-A (Skills) + EIA-R6-09 + K-16/K-17.
- **Claim ceiling: LOCAL / candidate-only.** This is a maker receipt — a claim, not an acceptance. No independent verification, no promotion, no canonical acceptance is claimed. The orchestrator's re-run is the evidence.

## 0. Reader's summary

- Repaired candidate main file: 21332 bytes (was 22091 with 10 `SKCV-SLICE` marker lines); cap 100,000. Live SKILL.md before this turn: 101,488 bytes (over cap).
- Landing actions: 3 added, 7 replaced, 21 retained untouched (31 target paths).
- Excluded stale absorption: `references/verifier-lane-handover.md` — the stub recorded `aebb35ea…`; the live file had moved to `2126b82e…`. Carried the current live file verbatim instead of absorbing.
- Step 6 harness on the repaired candidate (against the frozen originals): **PASS**.
- Step 8 harness on the live tree (with the originals-witness `--live`): **PASS**.
- Rollback drill: PASS — 28 files restored byte-for-byte after a 31-file landing.

## 1. What ran (commands, exit codes)

All commands run under `C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe` (pwsh). Nothing was written outside `WS_A/` and the live skill directory.

| # | Command | Exit |
|---|---|---|
| 1 | `Copy-Item -Recurse -Force <frozen>/candidates/avr/skill WS_A/repaired_candidate` (30 files) | 0 |
| 2 | `python WS_A/tools/s2_repair_skill_md.py` | 0 |
| 3-4 | `python WS_A/tools/s34_stale_refs.py` | 0 |
| 5 | `python WS_A/tools/s5_loss_proof.py` | 0 |
| 6 | `python <harness> --subject WS_A/repaired_candidate --out WS_A/logs/step6_default.json` | 0 |
| 7 | `python WS_A/tools/landing.py --src WS_A/repaired_candidate --dst <live> --preimage WS_A/apply/preimage --receipt WS_A/apply/APPLY_RECEIPT.json` | 0 |
| 8a | `python <harness> --subject <live> --out WS_A/logs/step8_selflive.json` | 1 |
| 8b | `python <harness> --subject <live> --live <frozen-baseline> --out WS_A/logs/step8_live.json` | 0 |
| — | `python WS_A/tools/rollback_drill.py` | 0 |

Exit code is the harness's own `verdict==PASS` gate (0) / otherwise (1).

## 2. Repair (step 2)

- Marker lines removed: **10** (`^=+\s*SKCV-SLICE`).
- Before: 22091 bytes, sha256 `eaf6172b9031f3f0a70671ca5f2b8fd10408ba1f6979e90d235e0ff2e7c60f2f`.
- After: 21332 bytes, sha256 `930cb1aab12d3cab1ef910b079e18b67a4294baf2a09f8ac33ef7c49e45b4b05`.
- Now starts with `---`: True; frontmatter `name: adversarial-verification-rounds`, `version: 1.0.0`; remaining marker lines: 0.

## 3. Excluded stale absorption (steps 3-4)

7 absorbed-reference stubs were re-verified against the **current** live bytes:

| reference | recorded sha256 | current live sha256 | result |
|---|---|---|---|
| `checker-binding-and-false-defect-signals.md` | `31ae9774cd4e245c…` | `31ae9774cd4e245c…` | VERIFIED |
| `finding-classification.md` | `6055fcd360b24dfa…` | `6055fcd360b24dfa…` | VERIFIED |
| `independent-verification-hygiene.md` | `9da3a1278235d437…` | `9da3a1278235d437…` | VERIFIED |
| `lane-harness-and-admission-gate.md` | `61bdb0cd1763f749…` | `61bdb0cd1763f749…` | VERIFIED |
| `sealed-evidence-corpus.md` | `276955b67c30961e…` | `276955b67c30961e…` | VERIFIED |
| `verdict-artifact-and-budget.md` | `79efb0c631348071…` | `79efb0c631348071…` | VERIFIED |
| `verifier-lane-handover.md` | `aebb35ea0ef523de…` | `2126b82ea61da0d5…` | STALE_MISMATCH |

- **EXCLUDED_STALE_ABSORPTION** `verifier-lane-handover.md`: stub recorded `aebb35ea0ef523de9d64940081706fc62bd36fb4712abe51ef8baa19e3dd939b`, but the live file is now `2126b82ea61da0d5ffb48c0474bffa5c8c640941de3608dcf43fe697ab328972` (29708 bytes). The current live file was copied verbatim into the repaired candidate; the stale stub was discarded. No newer live text was silently overwritten by stale absorbed text.

## 4. Loss proof from bytes (step 5)

- (a) current live bytes appear verbatim at the recorded topic offset for every absorbed reference: **True**.
- (b) every live `SKILL.md` line longer than 40 bytes survives in (repaired SKILL.md U topic files U carried-live references): **True** (999 lines, 0 lost).
- Raw output: `WS_A/s5_loss_proof.txt`, `WS_A/s5_loss_proof.json`. Step verdict: **PASS**.

## 5. Harness results (steps 6 and 8)

The harness file changed at 2026-10-16 11:02 (after this brief was written at 10:56): C4 became marker-based and a `--live` flag was added. This matters for step 8 — see the note below.

| check | step 6 (repaired candidate) | step 8 (live, `--live`=originals witness) | step 8 (live, default `--live`=live) |
|---|---|---|---|
| C1_capacity | PASS | PASS | PASS |
| C2_loader_shape | PASS | PASS | PASS |
| C3_link_intake | PASS | PASS | PASS |
| C4_lossless | PASS | PASS | FAIL |
| C5_controls | PASS | PASS | PASS |
| **overall** | **PASS** | **PASS** | **FAIL** |

**Why step 8 needs the originals-witness.** C4 compares each absorbed stub's recorded sha against `LIVE/references/<name>`. After landing, the live tree's own `references/<name>` slots *are* the stubs, so the default self-referential invocation (`--live` unset = live tree) cannot pass by construction — there is no residual copy of the originals left in that path. The updated harness's `--live` flag exists exactly to point C4 at the tree the stubs absorbed from. The frozen baseline `HG-KSEOS/var/SKILL-CONVERGENCE-20261014/baseline/adversarial-verification-rounds` is that originals witness.

- Originals-witness check: baseline sha256 == the recorded stub sha for all 6 absorbed references: **PASS**.
- Raw JSON: `WS_A/logs/step6_default.json`, `WS_A/logs/step8_live.json`, `WS_A/logs/step8_selflive.json`, `WS_A/sim/reg2.json`, `WS_A/sim/regression_postland_baseline.json`.

## 6. Guarded landing (step 7)

Target live dir: `C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\skills\software-development\adversarial-verification-rounds`

- Pre-image: byte copy of **every pre-existing target path** in `WS_A/apply/preimage/` + `WS_A/apply/preimage/PREIMAGE_MANIFEST.json`.
- Policy: add files the candidate has and the live tree lacks; replace files whose bytes differ; **never delete** a live file the candidate lacks.

### Before/after per path

| path | action | before bytes | before sha256 | after bytes | after sha256 |
|---|---|---|---|---|---|
| `SKILL.md` | replaced | 101488 | `4be690a4feaee5ba` | 21332 | `930cb1aab12d3cab` |
| `references/attacking-a-gate-implementation.md` | retained_untouched | 4408 | `e742c44409518efe` | 4408 | `e742c44409518efe` |
| `references/checker-binding-and-false-defect-signals.md` | replaced | 5403 | `31ae9774cd4e245c` | 237 | `78e748905957696f` |
| `references/checker-contract-authoring.md` | retained_untouched | 7366 | `d41bd7a4b5b102fa` | 7366 | `d41bd7a4b5b102fa` |
| `references/checker-dispatch-frozen-subject.md` | retained_untouched | 3120 | `9a3d18f383fee61e` | 3120 | `9a3d18f383fee61e` |
| `references/cross-model-verification-lessons.md` | retained_untouched | 24668 | `5f94085d5afabebd` | 24668 | `5f94085d5afabebd` |
| `references/delivered-tree-vs-gate-verification.md` | retained_untouched | 9041 | `3efc0afdf652bf09` | 9041 | `3efc0afdf652bf09` |
| `references/finding-classification.md` | replaced | 3707 | `6055fcd360b24dfa` | 244 | `7bf5a31c25946faf` |
| `references/git-tree-integrity-signals.md` | retained_untouched | 5652 | `6218935c20b76312` | 5652 | `6218935c20b76312` |
| `references/independent-verification-hygiene.md` | replaced | 3385 | `9da3a1278235d437` | 244 | `a512f1661d0c2dd1` |
| `references/lane-handover-hygiene.md` | retained_untouched | 4149 | `d9601528f160d8c5` | 4149 | `d9601528f160d8c5` |
| `references/lane-harness-and-admission-gate.md` | replaced | 22476 | `61bdb0cd1763f749` | 237 | `32bf3608a9a6d538` |
| `references/locally-executable-gates.md` | retained_untouched | 4398 | `b238f5ab8ee93e6a` | 4398 | `b238f5ab8ee93e6a` |
| `references/mandate-completion-audit.md` | retained_untouched | 9726 | `6976882d8394a9f6` | 9726 | `6976882d8394a9f6` |
| `references/post-verdict-drift.md` | retained_untouched | 4999 | `2123ca231639dc6f` | 4999 | `2123ca231639dc6f` |
| `references/probe-and-claim-discipline.md` | retained_untouched | 2688 | `67f7bb8726d8baeb` | 2688 | `67f7bb8726d8baeb` |
| `references/probe-shape-and-false-red.md` | retained_untouched | 2757 | `79e758357a842831` | 2757 | `79e758357a842831` |
| `references/round-closeout-and-handover.md` | retained_untouched | 5175 | `1f9ad53b039882ff` | 5175 | `1f9ad53b039882ff` |
| `references/route-scheme-enforcement.md` | retained_untouched | 16184 | `e943f00cd9af8a86` | 16184 | `e943f00cd9af8a86` |
| `references/sealed-evidence-corpus.md` | replaced | 4816 | `276955b67c30961e` | 243 | `04847b7a128a7960` |
| `references/sqlite-wal-forensics.md` | retained_untouched | 3764 | `90349088ec7bfac8` | 3764 | `90349088ec7bfac8` |
| `references/topic-source-remainder.md` | added | 0 | `` | 82592 | `15d6ab99131f46d2` |
| `references/topics/lane-harness-and-handover.md` | added | 0 | `` | 55417 | `84b546f1429089ff` |
| `references/topics/verification-and-acceptance-lane.md` | added | 0 | `` | 18144 | `8b3a6945b3f9bfb1` |
| `references/verdict-artifact-and-budget.md` | replaced | 5032 | `79efb0c631348071` | 242 | `fca40ed375dedcaa` |
| `references/verification-control-defects.md` | retained_untouched | 5839 | `2a4c6459d1f3c02c` | 5839 | `2a4c6459d1f3c02c` |
| `references/verifier-lane-handover.md` | retained_untouched | 29708 | `2126b82ea61da0d5` | 29708 | `2126b82ea61da0d5` |
| `references/verify-lane-performance.md` | retained_untouched | 8600 | `a44081e44177fdbd` | 8600 | `a44081e44177fdbd` |
| `scripts/freeze-subject-and-guard.py` | retained_untouched | 6532 | `4aa4a8bcd974ee87` | 6532 | `4aa4a8bcd974ee87` |
| `scripts/run-gate-matrix.py` | retained_untouched | 8727 | `0964d650229219b2` | 8727 | `0964d650229219b2` |
| `references/acceptance-negatives-and-controls.md` | retained_untouched | 3426 | `6002199a54d3b7de` | 3426 | `6002199a54d3b7de` |

Tree-level counts: added=3, replaced=7, retained_untouched=21 (target paths 31; candidate files 30; live files before 28).

- Rollback: `WS_A/apply/rollback.py` (restores every pre-image byte-for-byte, deletes every added file). Drill: **PASS**.

## 7. Honest gaps / limits

- **Maker claim only.** No independent checker has run; nothing is accepted, approved, promoted, or canonical-verified.
- **The harness file changed mid-turn** (mtime 11:02, after the 10:56 brief). I ran the current version. Its C4 is marker-based and it adds `--live`; a caller following the brief literally (`--subject <live>` with no `--live`) will see C4 FAIL by construction after landing, because the live absorbed-reference slots become the stubs. The pass requires `--live` = the originals witness.
- **`references/verifier-lane-handover.md` is not the frozen-round bytes.** It is the current live file (`2126b82e…`, 29,708 bytes), carried verbatim. The frozen round's recorded target (`aebb35ea…`, 26,549 bytes) is not present in the landed tree. This is the honest handling of a tree that moved after the freeze.
- **`references/topics/*` and `topic-source-remainder.md` are the frozen round's absorbed text**, landed verbatim. The absorbed stubs are tiny pointer files; the harness treats any file carrying an `absorbed ->` marker as a stub regardless of size.
- **Live-tree drift is possible after this turn** (the runtime curator can advance it); byte-exactness holds at the moment of this receipt only.
- I did not read, copy, or print any credential material, and made no git writes and no external network calls.

## 8. Artifacts in `WS_A/`

- `repaired_candidate/` — repaired candidate tree (30 files).
- `apply/APPLY_RECEIPT.json`, `apply/preimage/` (+`PREIMAGE_MANIFEST.json`), `apply/rollback.py`.
- `logs/step6_default.json`, `logs/step8_live.json`, `logs/step8_selflive.json`, `logs/step5.txt`.
- `s2_repair_result.json`, `s34_stale_refs_result.json`, `s5_loss_proof.{txt,json}`, `baseline_witness.json`, `rollback_drill_result.json`.
- `live_preimage_snapshot.txt`, `live_postimage_snapshot.txt`.
- `tools/` — the scripts above; `sim/` — post-landing simulations and the rollback drill.
