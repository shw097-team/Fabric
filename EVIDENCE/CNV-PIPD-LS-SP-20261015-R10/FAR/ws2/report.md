# ws2 — Candidate-vs-landed inventory + closure requirements (FAR round R10, workspace 2)

Produced 2026-10-16 (Taipei). Claim ceiling: **LOCAL / candidate-only** — this is a read-only research record;
nothing was modified, applied, or published by this workspace. The orchestrator must re-derive before treating
any row as accepted.

## 1. Method and scope

- Live canonical skill tree: `C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/skills/` (56 skill dirs with SKILL.md, incl. `software-development/*`, `governed-write-admission`, `hgk-lifecycle-admission` at top level).
- Candidate roots searched (read-only):
  1. `C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014/candidates/` — subdirs `avr/skill`, `hgk/skill`, `apply/`, `consumer/`.
  2. `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R9/` — `CANDIDATE_V2/`, `FAR/ws3/repaired_candidate/`, `WS_B/drill|landing_sim|preimage|own`.
  3. `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8/` — `WS_A/sim/drill|drill_pre|live|live2`.
- Comparison unit: whole candidate tree vs its canonical skill dir (name taken from each SKILL.md frontmatter), per-file `sha256` + byte size; diff line counts for diverging `.md` files. `__pycache__` excluded. Raw data: `raw/tree_compare.json`, `raw/file_diffs.json`, `raw/canon_skill_dirs.json`, `raw/candidate_name_map.json`.

## 2. Landed state per candidate tree

| Candidate | Canonical target | files (cand/canon) | landed? |
|---|---|---|---|
| R9 `WS_B/landing_sim` | hgk-governed-execution | 125/125 | **YES — byte-identical (all 125 files)** |
| R9 `CANDIDATE_V2` | hgk-governed-execution | 111/125 | **identical subset** — all 111 present files byte-identical; 14 later-canonical files not carried |
| R9 `FAR/ws3/repaired_candidate` | hgk-governed-execution | 110/125 | **identical subset** — same, 14 later-canonical files not carried |
| SKCV `hgk/skill` | hgk-governed-execution | 109/125 | NO — 16 canonical-only files incl. `verifying-lane-declaration-changes.md`; `step-verify-only-lane.md` differs (6029 B vs live 7994 B) |
| SKCV `avr/skill` | adversarial-verification-rounds | 30/31 | NO — live `SKILL.md` 23151 B vs cand 22091 B; live `verifier-lane-handover.md` 29708 B vs cand 1-line absorption marker; `acceptance-negatives-and-controls.md` live-only |
| R9 `WS_B/preimage` | hgk-governed-execution | 122/125 | NO by design — this is the **pre-image** (old 105116 B SKILL.md, full-text references) + `PREIMAGE_MANIFEST.json`; exactly the rollback base for the R9 apply |
| R9 `WS_B/drill` | hgk-governed-execution | 121/125 | NO by design — same pre-image family (drill subject of the rollback rehearsal) |
| R8 `WS_A/sim/live`, `live2` | adversarial-verification-rounds | 31/31 | NO — only `SKILL.md` (`+1/−19` lines) vs live; live also restored `verifier-lane-handover.md` |
| R8 `WS_A/sim/drill` | adversarial-verification-rounds | 28/31 | NO — pre-slim subject (101488 B SKILL.md; 7 full-text references vs live absorption markers) |
| R8 `WS_A/sim/drill_pre` | (no frontmatter name) | — | ABSENT mapping — `drill_pre/preimage/*` and `drill_pre2/` carry `PREIMAGE_MANIFEST.json`; treated as older pre-image generations, not live candidates |

Key semantics, grounded in R9 records: the canonical `hgk-governed-execution` was **already landed** in R9 by
guarded overlay (SKILL.md 105,116 → 21,026 B, zero deletions, pre-image kept, rollback drilled —
`R9_LEDGER.json` `applied_state`, `side_effects_disclosed[].SE-04`). `CANDIDATE_V2` and
`repaired_candidate` are post-apply snapshots of that landed state (identical subsets); `preimage`/`drill`
preserve the pre-apply bytes on purpose. Both AVR pre-slim trees (SKCV `avr/skill`, R8 `sim/drill`) are
**superseded** by the R8 guarded apply (R8_LEDGER `side_effects[]`: SKILL.md 101,488→21,332 B — since
further revised live: 23,151 B), with live tree carrying three files (`acceptance-negatives-and-controls.md`,
`topic-source-remainder.md`, `topics/*`) that those candidates predate.

### hgk trio, live canonical state (measured)

- `hgk-governed-execution` SKILL.md = 21,026 B, sha256 `60a4d9b3c79fc9e7…` (matches `R9_LEDGER.applied_state` and `R10/SESSION_LEDGER_R10.json` side-effect note exactly).
- `hgk-kanban-and-lane-routing` SKILL.md = 86,198 B, sha256 `2d61c117e83ec8bd…` — **has no candidate at any searched root**; nothing pending.
- `hgk-lifecycle-admission` (top-level) — **largely ABSENT on disk: SKILL.md 0 bytes** (empty file, present but 0 B; `references/` populated). Cannot determine intended content from disk; flag to orchestrator.

### Leaf candidate artifacts with NO canonical counterpart (ABSENT landed counterpart)

`candidates/apply/guarded_apply.py` (52,296 B), `apply/patch/hgk-lane-dispatch.py` (128,634 B), `apply/patch/lane-dispatch-timeout-capture.patch`, `consumer/tools/skill_manager_{tool,batch,guards}.py` + `skill_linter.py`, R8/R9 `hgk_admission_r{8,9}.py`, `publish_r{8,9}.py`, `dispatch_r9.py`, `WS_B/apply_tool.py`, `ws_a_skill_slim_regression.py`. These are round-local tooling/workflow sources; no counterpart exists in the live skill tree (the live tree's skill `scripts/` dirs carry only the skill-shipped helpers listed in the TSV). Whether HG-KSEOS repo internals already carry equivalents was NOT determined (out of scope — repo tree not audited file-by-file).

## 3. What could NOT be determined (explicit)

- **hgk-lifecycle-admission/SKILL.md is 0 bytes** on the live tree — cannot determine whether that is corruption, pending landing, or deliberate; no candidate for it exists at any searched root. ABSENT verdict: no basis to reconstruct.
- `SKCV .../consumer/` and `apply/` test-fixture subtrees (`_work`, `_lintcheck*`, `pytest-tmp`, `_pytest_tmp`) were not fully traversed (test fixtures, Windows-locked dirs in two cases); their intent is test scaffolding, per `phase*_result.json` siblings — judged irrelevant to the inventory; the four tool sources listed above ARE included.
- No candidate was found for `hgk-kanban-and-lane-routing` or `hgk-lifecycle-admission` at the three roots searched, beyond what is in §2. Whether other roots (e.g. inside the Fabric peer checkout, read-only to this task) carry candidates was not measured.
- The byte-exactness of R9 `WS_B/own` (orchestrator gate JSONs) against live tree is moot — those are records, not candidate payload; recorded as no-canon-counterpart class in the TSV via the leaf row for `apply_tool.py` only. Full `own/` contents were inspected by listing, not hashed (they are receipts, not skills).

## 4. Closure requirements — summary (full record: `closure_requirements.json`)

17 required items, each with the precedent file+field demonstrating it. Headline shape (all locators in the JSON):

- **CR-01..02 identity & ceiling:** `R9_LEDGER.json` `claim_ceiling`, `mission`, `changeset`, `hgk_project`.
- **CR-03..05 blockers, incidents, side effects:** `R8_LEDGER.json` `blockers[]` carry owner+evidence; `R9_LEDGER.json` `side_effects_disclosed[]` (SE-04 canonical tree change + rollback); always reversible/irreversible classification.
- **CR-06 resume playbook with copy-paste commands:** `R7/CHECKPOINT_STATE_20261016.json` `resume_playbook[]` (steps with `cmd`/`expected`/`note`).
- **CR-07 model/lane binding in force:** `R9_RUNTIME_BINDING.json` (`mandate`, per-plane binding_sha256, ranks) and `R10/SESSION_LEDGER_R10.json` `control_plane_in_force` (registry epoch 21, admission_status per lane, SoD status, CONFLICT_R10_F1).
- **CR-08 credential posture:** token file by path only, never printed/argv/URL; `R7/CHECKPOINT_STATE_20261016.json` `resume_preconditions` + `R10/SESSION_LEDGER_R10.json` side-effect `credentials`.
- **CR-09..10 published-state table + verdict classification:** `R7/CHECKPOINT_STATE_20261016.json` `published` / `verdicts` (valid / self-report / missing).
- **CR-11 environment facts:** R7 HANDOVER_CHECKPOINT §7 (worktrees, lane home, relay port, dirty-tree/do-not-fix disclosures).
- **CR-12 corrections forced by the checker:** `R9_SYNTHESIS.md` dedicated section (including recording the checker's own breach).
- **CR-13 falsification conditions:** `R8_SYNTHESIS.md` §6.
- **CR-14 honest not-done:** `R9_LEDGER.json` `verification.not_established[]`; R8_SYNTHESIS §4.
- **CR-15 live re-verification of current facts at closure:** R7 `branch_heads_reverified_by_api: true`; precedent for failure to do this: R9-F12 (route rebound between measurement and handover).
- **CR-16 the checkpoint itself is published:** R7 `checkpoint_commit` (head 20446c06, 306 blobs, readback clean).
- **CR-17 candidate-vs-landed inventory is itself a standing item:** R8-F5 and R9-B1 are why (a repair earlier shipped a candidate that lost a live reference).

Package shape precedent: one prose checkpoint + one machine state file, cross-referencing their siblings
(`R7/HANDOVER_CHECKPOINT_20261016.md` + `CHECKPOINT_STATE_20261016.json` with `reference_files` map).

## 5. Files written by this workspace (only these)

- `candidate_inventory.tsv` — 57 data rows (10 tree-level candidate rows + 27 per-file diverging rows + 14 no-counterpart leaf rows + header).
- `closure_requirements.json` — 17 required items + manifest-shape precedent, each with precedent locator.
- `report.md` — this file.
- `raw/canon_skill_dirs.json`, `raw/candidate_name_map.json`, `raw/tree_compare.json`, `raw/file_diffs.json` — command outputs/comparison evidence.

No writes outside `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R10/FAR/ws2/`; scratch
probes lived in the Hermes scratch dir (outside all restricted trees); no git command, no network, no credential read.
