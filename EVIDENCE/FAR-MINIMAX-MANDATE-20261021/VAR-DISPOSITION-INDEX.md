# var/ 處置索引（本回合產出）

- 產出時間（UTC）：`2026-10-21T06:27:27.354909Z`
- 範圍：`var/` 頂層目錄（不含本回合自身的輸出目錄）
- **實測目錄數：120**（業主引用的 114 為舊快照）
- **本回合執行的破壞性動作：0**（未刪除、未搬移、未改名）

## 為什麼「目錄數」不能直接當成「未結案回合數」

| 類別 | 數量 | 意義 |
|---|---|---|
| `ROUND_OPEN` | 8 | 回合產物，且其連結的 openspec change 仍有未勾項 |
| `ROUND_ARTIFACT` | 75 | 回合產物，但沒有可連結的 change |
| `SUPPORT_ARTIFACT` | 0 | 支援性證據（lane probe、發布包） |
| `RUNTIME_OR_CACHE` | 3 | runtime / cache / DB / 備份 —— **從來不是回合** |
| `EMPTY` | 2 | 空目錄 |
| `UNREADABLE` | 0 | 存在但讀不到 |
| `UNCLASSIFIED` | 32 | 需業主裁決 |

## 完整逐目錄索引

| 目錄 | 檔案數 | 不可讀子樹 | 類別 | 連結的 change | 建議動作 |
|---|---:|---:|---|---|---|
| `FABRIC-CLOSEOUT-20261013` | 4 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `FABRIC-OPEN-ITEMS-20261013` | 21 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `FABRIC-REPO-ASSESS-20261013` | 27 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `FABRIC-REPO-PUBLISH-20261013` | 7 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `FAR-CLOSURE-20261021` | 16 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `FAR-CLOSURE-20261021-R2` | 35 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `FAR-CLOSURE-20261021-R3` | 23 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `FAR-CLOSURE-PUBLISH-20261021` | 6 | 0 | `UNCLASSIFIED` | — | owner ruling required; do not auto-close and do not delete |
| `FAR-FBKREORDER-20261021` | 33 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `FAR-GOV-SKILLS-20261014` | 83 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `FAR-LANE-ENFORCEMENT-RCA-20261015` | 124 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `FAR-LANE-REPAIR-20261014` | 105 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `FAR-LANE-REUSE-RCA-20261015` | 193 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `FAR-LANE-ROUTE-REBIND-20261015` | 42 | 0 | `UNCLASSIFIED` | — | owner ruling required; do not auto-close and do not delete |
| `FAR-LANE-VERSION-MIX-20261021` | 26 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `FAR-REMEDIATION-20261021` | 18 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `FAR-REMEDIATION-AND-CLOSURE-20261016` | 1455 | 120 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `FAR-RO-TOOLREFUSAL-20261014` | 43 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `FAR-STACK-HYGIENE-20261013` | 252 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `LANE-ENFORCEMENT-APPLY-20261015` | 414511 | 10143 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `LANE-RELIABILITY-CLOSURE-20261016` | 961 | 40 | `ROUND_OPEN` | `hgk-lane-reliability-closure-20261016` | reconcile the linked change's unchecked tasks first; close only with a per-item ruling |
| `R5-20261014-s4-r4-closeout` | 17 | 0 | `UNCLASSIFIED` | — | owner ruling required; do not auto-close and do not delete |
| `R5-PREFLIGHT` | 28 | 0 | `UNCLASSIFIED` | — | owner ruling required; do not auto-close and do not delete |
| `R5R-20261014` | 5 | 0 | `UNCLASSIFIED` | — | owner ruling required; do not auto-close and do not delete |
| `R5R-20261014-s4-preview4-focused-close` | 4061 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `R5R3-20261016-preview4-closeout` | 7 | 0 | `UNCLASSIFIED` | — | owner ruling required; do not auto-close and do not delete |
| `R5S-20261015-s4-preview4-verify-close` | 62 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `R5Y-20261014-gpt-plugin-publication` | 6 | 0 | `UNCLASSIFIED` | — | owner ruling required; do not auto-close and do not delete |
| `R5Y-20261014-gpt-plugin-publication-recheck` | 6 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `R5Z-20261014-session-conformance` | 139 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `R5Z-20261014-session-conformance-arm3` | 3 | 0 | `UNCLASSIFIED` | — | owner ruling required; do not auto-close and do not delete |
| `R5Z-20261014-session-conformance-arm4` | 3 | 0 | `UNCLASSIFIED` | — | owner ruling required; do not auto-close and do not delete |
| `R5Z-20261014-session-conformance-arm5` | 3 | 0 | `UNCLASSIFIED` | — | owner ruling required; do not auto-close and do not delete |
| `R5Z-20261014-session-conformance-recheck` | 3 | 0 | `UNCLASSIFIED` | — | owner ruling required; do not auto-close and do not delete |
| `R6-20261014-far-remediation-and-repair` | 46 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `R6-CHKS` | 71 | 0 | `UNCLASSIFIED` | — | owner ruling required; do not auto-close and do not delete |
| `R7-20261014-merge-hygiene-closeout` | 29 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `R7-LANES` | 54 | 0 | `UNCLASSIFIED` | — | owner ruling required; do not auto-close and do not delete |
| `ROUND3-LANE-REBIND-AND-CLOSURE-20261016` | 760 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `S4R3FAR-20261013-decision-and-handover` | 63 | 0 | `UNCLASSIFIED` | — | owner ruling required; do not auto-close and do not delete |
| `S4R3FAR-probe` | 3 | 0 | `UNCLASSIFIED` | — | owner ruling required; do not auto-close and do not delete |
| `S4R3X-20261013-f006-and-stageb-successor` | 33 | 0 | `UNCLASSIFIED` | — | owner ruling required; do not auto-close and do not delete |
| `SKILL-CONVERGENCE-20261014` | 1854 | 3 | `ROUND_OPEN` | `hgk-skill-convergence-20261014` | reconcile the linked change's unchecked tasks first; close only with a per-item ruling |
| `SQS-THC-PUBLICATION-20261015` | 3 | 0 | `UNCLASSIFIED` | — | owner ruling required; do not auto-close and do not delete |
| `_SKCV_PUBLISH_20261014` | 160 | 0 | `UNCLASSIFIED` | — | owner ruling required; do not auto-close and do not delete |
| `__pycache__` | 18 | 0 | `RUNTIME_OR_CACHE` | — | NOT a round: exclude from the unfinished-round denominator; retention decided by the owner |
| `a2` | 793 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `a3` | 532 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `backups` | 11 | 0 | `RUNTIME_OR_CACHE` | — | NOT a round: exclude from the unfinished-round denominator; retention decided by the owner |
| `cnv-ea-r7r11-20261016` | 9 | 0 | `UNCLASSIFIED` | — | owner ruling required; do not auto-close and do not delete |
| `codex-app-server-logs` | 0 | 0 | `EMPTY` | — | confirm and remove only with owner approval (a directory the tool created and never used) |
| `codex-home-g3-003` | 3 | 0 | `UNCLASSIFIED` | — | owner ruling required; do not auto-close and do not delete |
| `codex-relay` | 1 | 0 | `UNCLASSIFIED` | — | owner ruling required; do not auto-close and do not delete |
| `far` | 81 | 0 | `ROUND_OPEN` | `far-lane-remediation-20261021` | reconcile the linked change's unchecked tasks first; close only with a per-item ruling |
| `far-018` | 6 | 0 | `ROUND_OPEN` | `hgk-cnv-far018-far019-archive` | linked to an openspec change with no local receipt: inspect and disposition |
| `far-019` | 6 | 0 | `ROUND_OPEN` | `hgk-cnv-far018-far019-archive` | linked to an openspec change with no local receipt: inspect and disposition |
| `far-ao-independence-20261010` | 166 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `far-doc-update-20261013` | 11 | 0 | `UNCLASSIFIED` | — | owner ruling required; do not auto-close and do not delete |
| `far-exec-identity-001` | 44 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `far-exec-identity-002` | 119 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `far-execute-model-expansion` | 22 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `far-hermes-incident-rca-001` | 57 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `far-iao-lane-skip-20261012` | 2468 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `far-lane-health-repair-20261011` | 186 | 0 | `ROUND_OPEN` | `lane-health-repair-20261011` | reconcile the linked change's unchecked tasks first; close only with a per-item ruling |
| `far-lane-route-slots-012` | 53 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `far-lane-sod-003` | 907 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `far-lane-sod-004` | 26 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `far-lane-sod-005` | 15 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `far-lane-sod-006` | 63 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `far-lane-sod-007` | 3655 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `far-lane-sod-008-console-window-20261008` | 12 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `far-lane-sod-009-supervisor-governance-20261008` | 2 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `far-lane-sod-010-converge` | 78 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `far-lane-sod-011-router-window` | 5736 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `far-lane-verify-002` | 88 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `far-oauth-window-20261010` | 20 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `far-pending-decisions-20261013` | 4 | 0 | `UNCLASSIFIED` | — | owner ruling required; do not auto-close and do not delete |
| `far-plan-enforcement-011` | 186 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `far-planning-intelligence-fit-012` | 24 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `far-strict-declaration-20261011` | 72 | 0 | `ROUND_OPEN` | `strict-declaration-20261011` | reconcile the linked change's unchecked tasks first; close only with a per-item ruling |
| `far-swof-kseos-rca-001` | 25 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `far-verify-drift-20261012` | 35 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `far-verify-lane-noverdict-20261012` | 36 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `far-verify-model-misselection-20261012` | 33 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `far-w6-closure-decision-20261012` | 16 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `far-w6-mandate-alignment-20261012` | 16 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `far-w6-nextstep-decision-20261012` | 19 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `far-w6-plan-sod-reconciliation-20261012` | 18 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `fda` | 1635 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `hermes-disposable` | 24655 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `hermes-qualification` | 5 | 0 | `UNCLASSIFIED` | — | owner ruling required; do not auto-close and do not delete |
| `hgk-gcm-apply-20261013` | 227 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `hgk-gcm-containment-20261013` | 127 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `hgk-gcm-repair-20261013` | 310 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `hgk-gcm-repair2-20261013` | 41 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `hgk-solution-apply-20261012` | 65049 | 8 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `lane-health-20261011` | 26 | 0 | `UNCLASSIFIED` | — | owner ruling required; do not auto-close and do not delete |
| `lane-resolutions` | 36 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `lane-route-001` | 32 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `modred` | 5 | 0 | `UNCLASSIFIED` | — | owner ruling required; do not auto-close and do not delete |
| `opencodex-backup` | 3944 | 0 | `RUNTIME_OR_CACHE` | — | NOT a round: exclude from the unfinished-round denominator; retention decided by the owner |
| `pciv` | 118 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `provider-failover-routing` | 2955 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `rbwi-fullrun-001` | 54 | 0 | `UNCLASSIFIED` | — | owner ruling required; do not auto-close and do not delete |
| `releases` | 1 | 0 | `UNCLASSIFIED` | — | owner ruling required; do not auto-close and do not delete |
| `repair` | 12 | 0 | `ROUND_OPEN` | `hermes-incident-2026-10-05-repair` | reconcile the linked change's unchecked tasks first; close only with a per-item ruling |
| `research` | 4 | 0 | `UNCLASSIFIED` | — | owner ruling required; do not auto-close and do not delete |
| `rollback-proof` | 2 | 0 | `UNCLASSIFIED` | — | owner ruling required; do not auto-close and do not delete |
| `rounds` | 58 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `rp002-stage1` | 92 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `shared-spine` | 1 | 0 | `UNCLASSIFIED` | — | owner ruling required; do not auto-close and do not delete |
| `swof-construction-002` | 64 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `swof-construction-002-r4` | 3 | 0 | `UNCLASSIFIED` | — | owner ruling required; do not auto-close and do not delete |
| `swof-construction-002-w2` | 32 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `swof-construction-002-w2-repair-001` | 405 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `swof-precon-001` | 80 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `swof-w1-r4-evidence-cleanup` | 51 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `swof-w1-r4-final-closure` | 13 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
| `wiki-rebuild` | 0 | 0 | `EMPTY` | — | confirm and remove only with owner approval (a directory the tool created and never used) |
| `workbench` | 12180 | 0 | `ROUND_ARTIFACT` | — | attach to the change it evidences; no receipt-based auto-close |
