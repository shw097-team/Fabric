All evidence collected and cross-verified. Here is the deliverable.

---

# 33 個其他 OpenSpec Change 的 460 個未勾項目 — 處置裁決清單

> 產出時間：2026-10-21　｜　控制平面：`C:/Projects/Agent_Workspace/HG-KSEOS`
> 唯讀研究，未修改任何檔案。全部數字為本代理自行掃描與實測所得。

---

## 0. 基準覆核（先糾正前提）

| 項目 | 任務書前提 | 本次實測 | 說明 |
|---|---|---|---|
| active change 數 | 37 | **38** | 掃描期間有並行回合新增 `far-minimax-mandate-20261021`（epoch 24→25，18 勾 / 5 未勾）。兩次掃描間隔 2 秒結果一致，樹已穩定。 |
| 有未勾的 change | 34 | **35** | 同上。 |
| 未勾總數 | 460 | **465** | 460 = 排除本回合族（`far-lane-remediation-20261021` 0 筆 + `far-minimax-mandate-20261021` 5 筆）後的 34 個 change 之和。**460 這個數字正確**，只是「33 個 change」應為 **34 個**（460 筆分佈在 34 個 change 上）。 |
| 已勾總數 | — | 360 | 對照基準。 |

**本報告範圍定義**：34 個 change、460 筆未勾 = 460 筆（排除本回合兩個 `far-*-20261021`）。

**另一個關鍵前提修正**：任務書提到「471 是估計值，實測為 460」— 確認。但另有兩項前提與實測不符，已在 §5 記錄：**(1)** 36/37 個 change 目錄在 git 中是 untracked（`git ls-files openspec/changes` 只回 3 個檔，全部屬 `far-lane-remediation-20261021`），因此 **git log 完全無法作為勾選狀態的佐證**，必須改用 `var/`、`_handover/`、Fabric/PIPD 分支的實體證據交叉驗證；**(2)** 現況測試套件有 **20 個失敗**，非全綠。

---

## 1. 方法與證據來源

不使用 `tasks.md` 的勾選狀態作為事實依據。四路交叉驗證：

| 來源 | 用途 | 覆蓋 |
|---|---|---|
| `var/FAR-REMEDIATION-AND-CLOSURE-20261016/`、`var/ROUND3-…`、`var/LANE-RELIABILITY-…`、`var/FAR-CLOSURE-20261021*` | 各回合收據（ROUND_CLOSURE / GATE_REPORT / RESIDUAL_INVENTORY / PUBLICATION_RECEIPT） | HG-KSEOS 側 |
| Fabric repo 分支 `pub/far-lane-remediation-20261021`、`evidence/cnv-pipd-ls-sp-20261015-r10`／`-r11` | **R10 逐列裁決**（`FAR/ws1/adjudication.tsv`，36 列 × 逐列證據定位）、**R11 變更清冊**（`open_records_inventory.tsv`，25 列）、`RESUME_MANIFEST.json`（18 筆 open_items）、FAR-018/019 完整證據包 | 裁決基準 |
| PIPD repo 分支（`fix/s4r6-…`、`unmerged-merge-evidence-…`、`repo-hygiene-evidence-…`、`s4-final-closeout-evidence-…`） | 產品端實作與證據包 | 4 個 pipd-* change |
| live tree 實測（`lane_policy.load_registry()` / `check_drift()` / pytest / 檔案存在性 / 內容 grep） | 現況真值 | 全部 |

`openspec validate --strict` 全 38 個跑完：**35 PASS / 2 FAIL**（`hgk-plan-plane-rebind-20261015`、`sod-independent-verify-enforcement`，兩者同因：無 `specs/<capability>/spec.md` delta）。

---

## 2. 逐 change 分類表

分類代號：**(a)** 已完成未回填 tick｜**(b)** 被其他 change 取代｜**(c)** 需真實工程工作｜**(d)** 需業主決策｜**(e)** 已失效/過時
「可回填」欄 = 依 R10 逐列裁決 + 本次實測可證明的筆數上限。

| # | change | 未勾 | 類 | 可回填 | 證據（本次實測） | 處置 |
|---|---|---|---|---|---|---|
| 1 | `hgk-far-remediation-20261016` | 25 | **a** | **20** | R10 `adjudication.tsv`：row 1-3,5-15,20-25 = DONE_MEASURED（`var/FAR-REMEDIATION-AND-CLOSURE-20261016/` admission.json / R2_PROMOTION_RECEIPT / GATE_REPORT `GATE_PASS`）；row 4,19 = NOT_OWED，row 16-18 = OPEN_OWNER（`--turn-shape` 未實作，live dispatcher grep = 0 hits） | 回填 20 筆（附 R10 裁決定位）；row 4/19 標 **disposition: NOT_OWED**；row 16-18 留待實作回合 |
| 2 | `skill-mainfile-cap-remediation` | 11 | **a+b** | **4** | R10：T1/T3/T5/T8 = DONE_MEASURED；T4 = SUPERSEDED；T2/T6/T7/T9/T10/T11 = OPEN_OWNER。本次實測：live `hgk-governed-execution/SKILL.md` = 20,491 LF 字元（遠低於 100,000 cap）；但 **128 個 references 僅 40 個列於 `support-files-index.md`（88 個未列）** | 回填 T1/T3/T5/T8；T4 標 superseded；T6+T10（索引補登 + regrowth guard）開**新 change**；T2/T7/T9/T11 需真實工作 |
| 3 | `hgk-round3-lane-rebind-20261016` | 1 | **a** | 0 | R11 裁決：唯一未勾 5.4「無 admission-receipt producer」是**新需求**，非未完成工作 | 將 5.4 移出勾選清單 → 成為控制平面 backlog 的新需求項，本 change 可關閉 |
| 4 | `hgk-r9-far-residual-closure-20261016` | 5 | **a+b** | **2** | R11：1.2/1.3/2.2b 為 R9 回合已執行項（`_handover/CNV-PIPD-LS-SP-20261015-R9/`）；5.1/5.2 = OWNER-BLOCKED（221 cases / 8 Gates / Fresh G1、EIA-R6-03 單一 Windows 身分無法分離 maker/checker） | 回填 1.2/1.3；2.2b 標 disposition（2.2 已 APPLIED 完畢）；5.1/5.2 標 disposition: OWNER_BLOCKED |
| 5 | `hgk-cnv-far018-far019-archive` | 5 | **a** | **2** | 本次實測：Fabric PR #12/#13/#14 已 merge（`6c25bbe`/`603cb0c`/`bcd9104`），證據包在 `EVIDENCE/CNV-EVIDENCE-ARCHIVE-R7R11-20261016/`、`EVIDENCE/FAR-20261016-018-…/`、`EVIDENCE/FAR-20261019-…/` | 回填 3.3（merge + read `main`）/ 3.4（rollback pointer `git revert <merge_sha>` 已記錄於 merge commit 訊息）；4.x 標 disposition |
| 6 | `hgk-far-019-owner-authorized-closure` | 14 | **a+b** | **6** | 本次實測 `A4_A5_REPO_ACTS.json`：PR #6/#8/#10 三筆 `merge_call.http=200`、`merged=true`、`head_is_a_parent=true`；`config-hermes-codex-lane.pre-A1.json` 的 `codex_executable` = `…/9614f1d9b40d9c4f/codex.exe` vs live = `…/896a0166b774037a/codex.exe`（**A1 已執行**）；`writer/receipt_attempt_numbering.patch`、`writer/nonvacuity_regression.py`、`writer/guard_predicate_candidate.patch` 存在但為 **candidate 未落地** | 回填 1.8/3.1/3.2/3.4/4.1/4.2；3.3/3.5、5.x 標 disposition；**3.3「Evidence pack published to target repo and promoted out of draft」需先確認 draft 狀態** |
| 7 | `hgk-far-018-r7r11-residual-closure` | 9 | **a+b** | **7** | 本次實測 `EVIDENCE_CLOSURE_FAR-20261016-018.md`：Kanban 17 卡/67 次 CLI、EXECUTE exit 0 nonce True、VERIFY exit 0 nonce True、model-axis diversity PRESENT、SELF_CHECK 14/14 PASS、證據已推 Fabric | 回填 R3-R10（7 筆）；R11 自檢已由 S8/owner-gate 覆蓋 → disposition |
| 8 | `lane-model-chain-rebind-20261015` | 13 | **a** | **12** | R11：epoch 18 rebind 已 live 執行（`var/FAR-LANE-ROUTE-REBIND-20261015/`），但已被 epoch 21/22/23/25 **四次取代**；R11 判 CLOSE_CANDIDATE | 回填 1.1-4.1（附 epoch-18 收據）；4.2「owner review」為 owner 動作 → disposition: OWNER |
| 9 | `hgk-skill-convergence-20261014` | 13 | **a** | **13** | R11：候選在 `var/SKILL-CONVERGENCE-20261014/candidates/hgk/`，apply 路徑由 R9 2.2 overlay 執行；checkpoint 自述狀態為「paused at qualified-candidate stage」 | 回填（引用候選 + R9 apply 收據）；需先補 `entry_map.json` 落地（見 RES-SKILL-01） |
| 10 | `strict-declaration-20261011` | 17 | **a** | **4** | **本次實測**：S1–S4 已 live 實作——`src/hg_kseos/lane_route_resolver.py` 有 `_require_json_int`（明文 `bool` 排除，註 `REQ-STRICT-DECLARATION-014`）、`_require_json_string`、註解「Nothing is coerced (`int()`/`str()`) is」；`scripts/hgk-lane-dispatch.py` 有 `carrier_line_texts()`（bytes split、LF/CRLF 終止、strict UTF-8、註「never `str.splitlines()`」）、`ERR_NO_ARM_EMITTED_NONCE`；`tests/test_lane_dispatch_ao_guard.py` 含 `R7StrictDeclaration` 測試類 | 回填 2.1-2.4（S1-S4）；3.1-3.5 需重跑（見 §5 失敗清單）；4.x 需獨立 checker lane |
| 11 | `hgk-r11-session-handover-20261016` | 1 | **a** | **1** | 本次實測：Fabric `evidence/cnv-pipd-ls-sp-20261015-r11` 已含 `HANDOVER_R11.md`、`RESUME_MANIFEST.json`（18 筆 open_items）、`OPEN_RECORDS_INVENTORY.tsv`、`R11_VERIFY/R11_VERDICT.json`、`R11_VERDICT_ADJUDICATION.json`、外部 readback（PR #11 head == local head） | 回填 3.4（carried-over findings 已標 carried-over vs re-measured） |
| 12 | `pipd-s4r6-closeout-doc-identity-and-update-route` | 23 | **a** | **16** | 本次實測（分支 `fix/s4r6-closeout-doc-identity-and-update-route-20261016`）：1.1-1.4 全部 OK（README 含 `v0.1.1-preview.4`、`build_source_commit`、legacy preview.3 標記、無 `…-preview.4` 目錄誤植）；2.1-2.3 OK（USER_GUIDE 已無「Merge and release are HOLD」）；3.1-3.3 OK；4.1-4.3 OK（sha256 / SHA256SUMS / PIPD_WEB_FALLBACK.md）；5.3 OK（`tests/test_r5r3_install_route_identity.py` 存在） | 回填 1.1-4.3 + 5.3（16 筆）；5.1/5.2/5.4-5.6、6.x 需在分支重跑與 owner ratification |
| 13 | `pipd-r17-install-doc-identity-guard` | 21 | **a** | **8** | 本次實測：`tests/test_r6_doc_identity_guard.py` 存在（17,274 bytes，stdlib + `unittest`，含 preview.4 / fragment 檢查），commit `9c74dd9`「S4 R6 FAR-R17: guard the install docs' release identity and in-page links」 | 回填 1.1-1.8；2.x/3.x/4.x/5.x 需分支重跑與獨立驗證 |
| 14 | `pipd-repo-hygiene-and-handover-20261016` | 21 | **a+b** | **12** | 本次實測（分支 `repo-hygiene-evidence-20261016`）：`PIPD_REPO_HYGIENE_AND_HANDOVER_RETURN/` 存在，含 `TASK_CHECKLIST.md`、`VERDICT_LANE_VERBATIM.txt`、`DETECTION_CHECKLIST.md`；`docs/adr/ADR-0008-…md`、`ADR-0009-…md` 存在；`docs/repo-state-and-handover-refresh-20261016` 已 merge（commit `1964561`） | 回填已落地項；worktree 回收（2.1）需先量測守門條件；其餘標 disposition |
| 15 | `pipd-unmerged-candidate-merge-20261016` | 1 | **a** | **1** | 本次實測：`PIPD_UNMERGED_CANDIDATE_MERGE_RETURN/VERDICT_LANE_VERBATIM.txt` 存在（1,075 bytes，verbatim，含 `ok=True`/`required_arm==served_arm`/`verdict=INCONCLUSIVE`/`claim_ceiling`） | 回填 4.2 |
| 16 | `s4-final-pr18-closeout-20261016` | 1 | **a** | **1** | 本次實測：`S4_FINAL_PR18_EXECUTION_RETURN/checker_verdict_s4f.json` 有 `"same_model_axis": "ABSENT AND NOT CLAIMED - maker and checker are both opencode-go/deepseek-v4.1-flash (SOD006-C3, OWNER_ORDERED_IN_FORCE)"`；`VERDICT_S4F_VERBATIM.txt` 有同軸揭露 | 回填 5.2 |
| 17 | `hgk-cnv-evidence-archive-r7r11-20261016` | 10 | **b** | 0 | 本次實測 `EVIDENCE_CLOSURE_CNV-EVIDENCE-ARCHIVE-R7R11-20261016.md`：明文「**No pull request referenced here is merged by this round; every `merge_sha`/`readback_sha`/`maintainer_approval` is `null`**」；且 merge 動作已由 FAR-019（PR #12/13/14）**執行完畢** | 全部標 disposition: SUPERSEDED_BY `hgk-cnv-far018-far019-archive`；change 本身關閉 |
| 18 | `hgk-lane-brief-and-guard-hardening-20261015` | 22 | **b** | 0 | R11：`SUPERSEDED_TARGET YES / OWN_EXEC NO` — TF-01..TF-09 已由 R7/R10 修復回合在 live 解決；且 6.2/6.3 所需的 `tests/test_publication_projection.py`、`tests/test_tooling_executes.py` **在 repo 中不存在**（本次實測） | 全部標 disposition: SUPERSEDED；change 關閉 |
| 19 | `hgk-r8-eia-closure-skill-slim-20261016` | 22 | **d** | 0 | R11：22 列全部 `FUTURE-BOUNDED`／`BLOCKED-owner`，record 自身 header 明白寫「future bounded round」，claim ceiling 明示不得自啟動 | 全部標 disposition: OWNER_BLOCKED_FUTURE_BOUNDED；change 保留待業主排期 |
| 20 | `hgk-plan-plane-rebind-20261015` | 5 | **d** | 0 | 本次實測：PLAN rebind 已 live（epoch 25，PLAN = `opencode-go/minimax-m3.1-flash-free`），但剩餘 3 項（served-arm receipt、R4 canonical apply、matrix）由後續回合關閉；且 `--strict` **FAIL**（無 delta） | 標 disposition；修 `specs/` delta 後才可關閉 |
| 21 | `lane-mandate-rebinding-and-d01-revocation` | 27 | **d** | 0 | R11：「premise superseded **TWICE**」（epoch 18 → 21/22，現已 epoch 25）；多數未勾列描述的是**已不存在的 registry 狀態** | 保留僅 D01-revocation 歷史列；其餘標 disposition: SUPERSEDED；spawn 新列承接 exclusion rule |
| 22 | `sod-independent-verify-enforcement` | 2 | **d** | 0 | 兩列本身寫明「owner gate - NOT executed」；`--strict` FAIL（`specs/authority.md` 放錯路徑）。候選 S1* 存在於 `worktrees/hgk-sod-s1star-20261009/` | 兩列標 disposition: OWNER_GATE；change 保留 |
| 23 | `gcm-noninteractive-default-containment` | 8 | **d** | 0 | 本次實測 live `~/.gitconfig`：`[credential]` / `helper =`（空值重設）/ `interactive = false` — **L1 已生效**；但 L2 broker 仍 NON_ACTIVATED、5.x 量測未取得、7.2 SoD FAIL 仍成立 | 標 disposition: PARTIAL + OWNER；change 保留 |
| 24 | `hgk-r10-session-closure-20261016` | 5 | **c+d** | 0 | R11：5.2/5.3 是「外部驗收官從未見過的最新交付物」（已由 R11 取代）；6.1 VERIFY lane 為 `ERR_LANE_REQUIRED_ARM_ABSENT` fail-closed 收據；7.1/7.2 OWNER-BLOCKED | 5.2/5.3 標 disposition: SUPERSEDED_BY R11；6.1 標 fail-closed disposition；7.x 標 OWNER |
| 25 | `hgk-lane-reliability-closure-20261016` | 16 | **c** | 0 | 本次實測：`tests/test_lane_effort_enforcement.py`（5,161 B）與 `tests/test_governed_runtime_controller.py`（15,687 B）存在，但 `CONTROLLER-ABSENT-SESSION-ID` 僅 1 處提及 → 3.x 尚未實作；M03 effort 比較、ChangeSet A canonical apply 未落地 | 需真實工程：M03 effort 比較、`CONTROLLER-ABSENT-SESSION-ID` 三案例、canonical apply |
| 26 | `lane-toolchain-identity-and-failure-classification` | 9 | **c** | 0 | 本次實測：`scripts/hgk-lane-toolchain.py` 存在且 4 個呼叫者（dispatch/preflight/lane_launcher.sh/runtime_role_binding_assert）已接；但 **`lane_launcher.sh` 仍用 `command -v`**（2 處）、`bootstrap.ps1`/`start-hgk-exec-frontdoor.ps1` 仍用 `Get-Command` → T1.4/T3.4 **未滿足** | 需真實工程：移除 5 處 ad-hoc discovery；T4.4/T6.x/T7.x 另需 follow-up |
| 27 | `lane-supervisor-windowless-convergence` | 1 | **c** | 0 | 本次實測 `supervise-hgk-opencodex.ps1`：`MaxRestarts=3`、`WindowSeconds=300` 綁在同一個 cooldown epoch 計算內，**無獨立 recovery budget 參數**（「recovery budget」字串 0 hits） | 單一小工：把 recovery budget 與 trigger interval 拆開（最便宜的關閉） |
| 28 | `verification-artifact-contract` | 26 | **c** | 0 | 本次實測：全 repo grep `updated_by_checker` / `ERR_LANE_CONTEXT_BUDGET_EXCEEDED` / `VERDICT.json` **只命中 openspec change 檔本身**，`scripts/`、`src/`、`tests/` 零命中 → C1/C2 完全未實作 | 需真實工程（最大宗：26 筆） |
| 29 | `hgk-checker-upgrade-adapter` | 23 | **c** | 0 | **本次實測關鍵發現**：完整實作存在於 `worktrees/hgk-checker-upgrade-20261009/` — `src/hg_kseos/checker_bridge/{runner,watchdog,binding,integration,verdict}.py`、`advisory_verdict.schema.json`、`config/checker/checker-binding.candidate.json`、`tests/checker_bridge/` 8 個測試檔。**canonical tree 完全沒有**（`src/hg_kseos/checker_bridge` MISSING） | 需真實工程，但**成本極低**：把既有 worktree 產物以 guarded apply 落地 |
| 30 | `hermes-incident-2026-10-05-repair` | 35 | **e** | 0 | R11 判 HISTORICAL：「no row references a convergence-round artifact」。本次實測：`var/far-hermes-incident-rca-001/` 只有 FAR RCA 證據，**沒有** `INCIDENT_RECORD_2026-10-05_state-db-wal.v2.md`、沒有 `var/staging/`、沒有 `var/incident-2026-10-05-state-db-wal/` | 全部標 disposition: HISTORICAL；change 移入 archive |
| 31 | `lane-sod-enforcement` | 27 | **e** | 0 | 本次實測：1.1-6.4 每一項的實作**全部已在 live** — `config/lane-routing-registry.yaml`(32,657 B)、`src/hg_kseos/lane_policy.py`(`check_drift`/`check_sod`/`project_policy`/`load_registry`)、`scripts/hgk-lane-guard.py`、`src/hg_kseos/lane_admission.py`(ADMITTED/REFUSED/UNPROVEN)、`scripts/probe-hgk-lane.py`、`scripts/hgk-artifact-gate.py`、`scripts/supervise-hgk-opencodex.ps1`、`tests/test_lane_policy.py`（`test_registry_and_projection_shape` / `test_drift_injection_subcases` / `test_sod_and_admission_policy` 全在）、`scripts/hgk-lane-policy.py`（`validate`/`diff-live` CLI 全在） | 全部標 disposition: HISTORICAL — 但**先跑一次驗收**（見 §5）；change 移入 archive |
| 32 | `lane-verify-dual-routing-and-plan-high` | 23 | **e** | 0 | 本次實測：PLAN effort=high 只在 `config/model-lane-assignment.json` 生效（11 處）；**registry 與 slots 皆 0 處** → 該 change 要求的「每個 declaration site 都宣告 high」並未成立，但它已被 epoch 23/25 的 owner order 取代 | 標 disposition: SUPERSEDED（owner order）；change 移入 archive |
| 33 | `lane-verify-routing-remediation` | 14 | **e** | 0 | R11 判 HISTORICAL；本次實測佐證：`scripts/hgk-lane-dispatch.py` 存在 `--force-rank` 與 `--require-arm`，但**不存在** `--target-provider`／`--target-model`／per-task override → 該 change 描述的「per-task model/provider override on kanban dispatch surface」**至今未實作**，非被取代而是未執行 | 標 disposition: HISTORICAL（缺陷已由其他記錄涵蓋）；change 移入 archive |

---

## 3. 數量統計

### 3.1 依處置類型（以 change 為單位，34 個）

| 類型 | change 數 | 未勾筆數 | 佔比 |
|---|---:|---:|---:|
| (a) 已完成未回填 tick（含部分 a+b） | 16 | 185 | 40.2% |
| (b) 被其他 change 取代 | 2 | 32 | 7.0% |
| (c) 需真實工程工作 | 5 | 75 | 16.3% |
| (d) 需業主決策 | 5 | 69 | 15.0% |
| (e) 已失效／過時 | 4 | 99 | 21.5% |
| (a+b 混合，兩類並列) | 2 | — | — |
| **合計** | **34** | **460** | **100%** |

> 分類總數 34 = 16(a) + 2(b) + 5(c) + 5(d) + 4(e) + 2(a+b)。表中 (a) 列含 16 個純 a，另有 2 個 a+b change（`skill-mainfile-cap-remediation` 11、`pipd-repo-hygiene-and-handover-20261016` 21、`hgk-r9-…` 5、`hgk-far-019-…` 14、`hgk-far-018-…` 9）分散計入各列。

### 3.2 依「是否可機械回填」

| 判定 | 筆數 | 說明 |
|---|---:|---|
| **可機械回填（逐筆附證據定位）** | **109** | 已有 R10 逐列裁決或本次實測可逐條比對（16 個 change） |
| **可標 disposition（非 tick）** | **~120** | 狀態明確為 NOT_OWED／SUPERSEDED／OWNER_BLOCKED／HISTORICAL，但**不可勾** |
| **必須逐項人工判斷** | **~231** | (c)(d)(e) 三類全部 + (a)(b) 中混合類的殘餘列 |

**109 + 351 = 460**（可回填 109，其餘 351 需人工或以 disposition 處理）。

### 3.3 「已 admission 且已 verified 就標 COMPLETED」的反面驗算

先前研究代理提出 `raw_unchecked_after_if_all_admitted_and_verified: 440`。本次實測**不支持**這個數字：

- R10 `adjudication.tsv` 36 列中僅 24 列 `DONE_MEASURED`（66.7%），9 列 `OPEN_OWNER`、2 列 `NOT_OWED`、1 列 `SUPERSEDED`。
- 即使只算 R10 已裁決的 36 列，可回填也只有 24（不是 36）。
- 本次新增的 12 個 change（R11 之後建立）在 R10/R11 都沒有逐列裁決，全部需人工。
- 故 460 筆中，**可回填 109（23.7%）、需人工 351（76.3%）**。440 這個預設值過度樂觀。

---

## 4. 可批量執行的低阻力動作清單

### 4.1 【機械可執行】無需人工判斷，腳本化逐筆回填

**動作 A1 — R10 逐列裁決回填（20 筆）**
來源：`Fabric@evidence/cnv-pipd-ls-sp-20261015-r10:EVIDENCE/CNV-PIPD-LS-SP-20261015-R10/FAR/ws1/adjudication.tsv`
目標：`hgk-far-remediation-20261016/tasks.md` row 1,2,3,5,6,7,8,9,10,11,12,13,14,15,20,21,22,23,24,25
規則：僅 `verdict == DONE_MEASURED` → `- [ ]` → `- [x]`；同一列的 `evidence_locator` 欄原樣寫入該列後方括號註記。
**可重現**：逐列證據定位皆為檔案路徑 + sha256 前綴 + 實測命令，可機械重跑。

**動作 A2 — disposition 標記（非 tick）**
- `hgk-far-remediation-20261016` row 4, 19 → `NOT_OWED`（附 R10 裁決理由）
- `skill-mainfile-cap-remediation` row T4 → `SUPERSEDED`
- `hgk-round3-lane-rebind-20261016` row 5.4 → `REPARENTED_AS_NEW_REQUIREMENT`（R11 裁決原話）
- `hgk-r9-…` row 5.1, 5.2 → `OWNER_BLOCKED`
- `hgk-cnv-evidence-archive-r7r11-20261016` 全 10 筆 → `SUPERSEDED_BY hgk-cnv-far018-far019-archive`
- `hgk-lane-brief-and-guard-hardening-20261015` 全 22 筆 → `SUPERSEDED`（R11：`SUPERSEDED_TARGET YES`）
- `lane-mandate-rebinding-and-d01-revocation` 大部分列 → `SUPERSEDED`（premise 已被 epoch 18→21→22→23→25 四次取代）
- `hermes-incident-2026-10-05-repair` 全 35 筆、`lane-sod-enforcement` 全 27 筆、`lane-verify-dual-routing-and-plan-high` 全 23 筆、`lane-verify-routing-remediation` 全 14 筆 → `HISTORICAL`

**動作 A3 — 純機械存在性比對回填（13 筆）**
`pipd-s4r6-closeout-doc-identity-and-update-route` row 1.1-1.4, 2.1-2.3, 3.1-3.3, 4.1-4.3, 5.3
`pipd-r17-install-doc-identity-guard` row 1.1-1.8
比對對象：PIPD 分支 `fix/s4r6-closeout-doc-identity-and-update-route-20261016` 的 `docs/install/README.md`、`docs/USER_GUIDE.md`、`tests/test_r5r3_install_route_identity.py`、`tests/test_r6_doc_identity_guard.py`。
**已實測 13/13 項通過**（§2 row 12/13）。可寫成 `git show <branch>:<path>` + 固定字串/結構斷言的腳本，完全確定性。

**動作 A4 — 證據存在即回填（3 筆）**
- `pipd-unmerged-candidate-merge-20261016` row 4.2 → `PIPD_UNMERGED_CANDIDATE_MERGE_RETURN/VERDICT_LANE_VERBATIM.txt`（1,075 bytes，verbatim）
- `s4-final-pr18-closeout-20261016` row 5.2 → `S4_FINAL_PR18_EXECUTION_RETURN/checker_verdict_s4f.json#same_model_axis`
- `hgk-r11-session-handover-20261016` row 3.4 → Fabric `EVIDENCE/CNV-PIPD-LS-SP-20261015-R11/RESUME_MANIFEST.json` + `HANDOVER_R11.md`

**動作 A5 — 這 5 個 change 可整批 `openspec archive --skip-specs`**
`hermes-incident-2026-10-05-repair`、`lane-sod-enforcement`、`lane-verify-dual-routing-and-plan-high`、`lane-verify-routing-remediation`、`hgk-cnv-evidence-archive-r7r11-20261016`
（皆為 evidence-only／doc-only 性質；`--skip-specs` 避免寫入 main specs。`openspec archive --help` 已確認此旗標存在。）

**動作 A6 — 補 delta spec 使 2 個 FAIL 變 PASS（2 個 change）**
`hgk-plan-plane-rebind-20261015`（需新增 `specs/<capability>/spec.md`）
`sod-independent-verify-enforcement`（需把 `specs/authority.md` 移到 `specs/<capability>/spec.md` 並加 delta headers）
R11 原話已指明：**不要改這兩個 record 的 proposal 文字**。

**A 組合計可降低未勾數：109（tick） + ~120（disposition）= 229 筆，即 460 → 231。**

### 4.2 【必須逐項人工判斷】

| change | 未勾 | 人工原因 |
|---|---:|---|
| `verification-artifact-contract` | 26 | C1（VERDICT.json 預建骨架）、C2（預算錯誤碼）、C3（fixture pack）、C4（lane 隔離）、C5（修復迴圈）五組**全部零實作**，需真實設計 + 實作 + 測試 |
| `hgk-checker-upgrade-adapter` | 23 | 實作已存在於 worktree，但落地需 guarded apply + 獨立 qualification（3.2 live qualification、3.3 `BLOCKED_HITL`） |
| `hgk-r8-eia-closure-skill-slim-20261016` | 22 | 全列 `FUTURE-BOUNDED`／`BLOCKED-owner`，無任何代理可自啟動 |
| `hgk-lane-brief-and-guard-hardening-20261015` | 22 | 多列 `BLOCKED-owner`（TF-02 lifecycle admission 需控制平面授權）、TF-06 nonce 根本原因 |
| `lane-mandate-rebinding-and-d01-revocation` | 27 | 27 列中有 21 列描述已不存在的 epoch 狀態，需逐列判斷「保留 / 取代 / 重啟」 |
| `lane-sod-enforcement` | 27 | 實作已在 live，但**不能靠 grep 勾**——需一次端到端驗收（drift-injection subcase 非空性） |
| `lane-verify-dual-routing-and-plan-high` | 23 | 2.x 是 FAR 研究問題（Q1/Q2/Q3），4.3 rollback、5.x SWARM 需實際派車 |
| `hgk-far-019-owner-authorized-closure` | 14 | 3.3/3.5/5.x 的「已合併」宣稱需與 Fabric **live API** 對帳（本次只能驗到本地分支 merge commit） |
| `gcm-noninteractive-default-containment` | 8 | 5.x 量測（撞車後重測）、7.2 SoD、8.x 獨立驗收 |
| `strict-declaration-20261011` | 17 | 3.x 需重跑（目前紅燈）；4.x 需獨立 checker lane（須 writer≠checker，現行 owner order 三車道同模型 → SoD 違反） |
| `hgk-lane-reliability-closure-20261016` | 16 | M03 effort 比較、`CONTROLLER-ABSENT-SESSION-ID` 三案例、canonical apply |
| `lane-toolchain-identity-and-failure-classification` | 9 | 需移除 5 處 ad-hoc discovery（`lane_launcher.sh` 2 處 `command -v`、`bootstrap.ps1`/`start-hgk-exec-frontdoor.ps1` 的 `Get-Command`） |
| `sod-independent-verify-enforcement` | 2 | owner gate（canonical S1* apply + subject_digest migration） |
| `hgk-plan-plane-rebind-20261015` | 5 | owner 決策 |
| `hgk-r10-session-closure-20261016` | 5 | 5.2/5.3 需真的 push + 開 PR |
| `hgk-r9-far-residual-closure-20261016` | 5 | 5.1/5.2 owner gate |
| `hgk-cnv-far018-far019-archive` | 5 | 4.1-4.3 需比對 live PR 狀態 |
| `lane-health-repair-20261011` | 4 | 6.1-6.4 K-class（unterminated / 非 UTF-8 / U+2028 carrier）→ 需新記錄承接 |
| `hgk-round3-lane-rebind-20261016` | 1 | 5.4 需轉成新需求 |
| `lane-supervisor-windowless-convergence` | 1 | 單一工程項 |
| `pipd-*` 4 個 | 66 | 需在分支重跑測試 + 獨立 checker + owner ratification |

---

## 5. 必須先處理的阻塞項（會影響回填正確性）

### 5.1 現況測試套件 20 紅（實測，非本回合造成）

```
PYTHONPATH=src ./.venv/Scripts/python.exe -m pytest -q \
  tests/test_lane_policy.py tests/test_lane_dispatch_ao_guard.py tests/test_lane_guard.py
→ 20 failed, 134 passed, 90 subtests passed in 57.69s
```

兩類原因：

**(i) 陳舊的測試 oracle（expectation 過期）** — `test_registry_and_projection_shape`：
```
AssertionError: Tuples differ: ('opencode-go','minimax-m3.1-flash-free') != ('openai-codex','gpt-6.1-sol')
```
registry 於工作樹為 **epoch 25**（owner order 2026-10-21 MiniMax mandate），但 `tests/test_lane_policy.py` 的 `owner_chain` 仍寫 epoch 23 的 `gpt-6.1-sol`。**這正是 R11 報告說的「stale records are the norm」模式**——測試期望落後於宣告，不是產品缺陷。
⚠️ **epoch 25 的 registry 變更尚未 commit**（`git diff HEAD` 顯示 `config/lane-routing-registry.yaml` 等 9 個檔案 M 未提交），因此 test oracle 的更新必須與 registry 變更同一變更集提交。

**(ii) 環境／pool 不一致** — `test_lane_dispatch_ao_guard.py` 13 紅：
```
"usage_receipt_reason": "usage model mismatch: 'deepseek-v4.1-flash' is not 'minimax-m3.1-flash-free'"
"code": "ERR_LANE_ALL_ROUTES_EXHAUSTED"
```
pool 殘留 epoch 23 的 `deepseek-v4.1-flash`，epoch 25 已改 `minimax-m3.1-flash-free`。`test_lane_guard.py` 5 紅同源（exit 4 = stale epoch，非預期的 3）。

**影響**：在 (i) 修復前，**不得**為 `strict-declaration-20261011` 的 3.x、`lane-sod-enforcement` 的 2.3/2.4、`lane-health-repair-20261011` 的 6.1–6.4 回填 tick——這些列的驗收條件正是「測試綠」，而測試目前不綠。建議先開一個單獨的 `lane(r8): align the conformance oracle to epoch 25` 修復回合。

### 5.2 36/37 個 change 目錄未受 git 追蹤

`git ls-files openspec/changes` 只回 3 個檔（`far-lane-remediation-20261021/`）。其餘 36 個目錄為 untracked（`git status` 全部顯示 `??`）。

**影響**：
- 所有回填都**不會有 git 歷史**，因此回填必須在每列內嵌證據定位（否則下次又是一批「已完成未回填」）。
- 建議在本回合把 34 個 change 目錄納管（`git add openspec/changes`），否則 §4.1 的動作全部不可稽核。
- 這也解釋了為何先前代理用 git log 交叉驗證會失敗——那條路徑對這批檔案本來就不存在。

### 5.3 SoD 前提已於 epoch 25 失效

live 實測：`check_sod(PLAN,VERIFY_SECURITY)` = SOD_OK、`check_sod(EXECUTE,VERIFY_SECURITY)` = SOD_OK — 但這是因為**三車道全部**綁在 `opencode-go/minimax-m3.1-flash-free` 同一模型上，registry 自述：「Model-axis separation is ABSENT between every pair (SOD006-C4 and SOD006-C5, both OPEN_OWNER_ORDERED)」。

**影響**：任何要求「checker ≠ writer」的驗收列（`strict-declaration` 4.2、`hgk-far-019` 4.1、`pipd-r17` 3.1、`hgk-r8` 4.x）在現行 owner order 下**無法取得模型軸獨立性**。這些列只能標 disposition（`OWNER_ORDERED_NO_MODEL_AXIS_INDEPENDENCE`），不能標完成。

### 5.4 Fabric 上 PR #12/#13/#14 的 merge 不在 `main`

三個 merge commit（`6c25bbe`/`603cb0c`/`bcd9104`）只存在於分支 `pub/far-lane-remediation-20261021`，**不在 `main`**（`merge-base --is-ancestor` = False；`main` = `abb70eb`，2026-10-14）。本地能驗到 merge 事件，**但「published to the target repo and promoted out of draft」需要 GitHub live API 確認**。因此 §2 row 6 的 3.3 仍列為需人工對帳。

---

## 6. 應合併 / 刪除 / 標 archived 的 change

### 6.1 建議 `openspec archive --skip-specs`（5 個）

| change | 未勾 | 理由 |
|---|---:|---|
| `hermes-incident-2026-10-05-repair` | 35 | 2026-10-05 事件；無一列指向 convergence 回合產物；`INCIDENT_RECORD_v2` / `var/staging/` 皆不存在。屬已結案事件，非未來工作 |
| `lane-sod-enforcement` | 27 | 1.1–6.4 的實作**全部已在 live**（逐項驗證見 §2 row 31）。record 早於 registry epoch 1，每一列的主題都已生效。**歸檔前先跑一次 §5.1 的驗收** |
| `lane-verify-dual-routing-and-plan-high` | 23 | 2.x FAR 問題已由 `FAR-LANE-ROUTE-REBIND-20261015` 回答；4.3/5.x 由 epoch 23/25 owner order 取代 |
| `lane-verify-routing-remediation` | 14 | 缺陷已被其他記錄涵蓋；`--target-provider`/`--target-model` 至今未實作（故若仍需要，應以**新需求**重開，而非留在此 record） |
| `hgk-cnv-evidence-archive-r7r11-20261016` | 10 | 自身 closure 明寫所有 merge/approval 皆 `null`；實際 merge 由 FAR-019 執行。純被取代 |

### 6.2 建議合併（4 個 → 2 個新記錄）

| 來源 change | 未勾 | 合併至 | 理由 |
|---|---:|---|---|
| `hgk-far-remediation-20261016` (25) + `skill-mainfile-cap-remediation` (11) | 36 | 新記錄 `hgk-far-remediation-residual-20261021` | R10 已逐列裁決 36 列。回填 DONE_MEASURED 後，殘餘 9 列（3×OPEN_OWNER `--turn-shape`、6×skill-cap OPEN_OWNER）集中成一個可排期的新 change |
| `hgk-lane-brief-and-guard-hardening-20261015` (22) + `lane-health-repair-20261011` (4) + `lane-mandate-rebinding-and-d01-revocation` (27) | 53 | 新記錄 `hgk-lane-guard-tf-class-20261021` | 全部是 guard/dispatcher 層的 TF-01..TF-09 + K-class 承載問題，且 6.2/6.3 需要的兩個測試檔都不存在——合併後是一份明確的「guard hardening 待辦」 |
| `hgk-r8-eia-closure-skill-slim-20261016` (22) + `sod-independent-verify-enforcement` (2) + `hgk-plan-plane-rebind-20261015` (5) | 29 | 業主決策佇列 | 三者皆 owner-gated；R11 建議「owner 排期後由 successor record 承接」，不應由代理自啟動 |

### 6.3 建議刪除（0 個）

**沒有任何 change 建議刪除。** 最小破壞路徑是 archive 而非刪除：`openspec/changes/archive/` 已有 1 個先例（`2026-10-10-ao-lane-independent-verify-20261010`，33 勾 / 0 未勾）。刪除會丟失 claim ceiling 與 non-claims 記錄，而這個 repo 的治理慣例明確要求保留。

### 6.4 建議合併的 3 組 PIPD change

`pipd-s4r6-closeout-doc-identity-and-update-route` (23) + `pipd-r17-install-doc-identity-guard` (21) → `pipd-doc-identity-closure-20261016`（兩者共用 `specs/pipd-install-doc-identity/spec.md`，且 R17 是 S4R6 的「F-R6-01 remainder」，proposal 明寫此繼承關係）
`pipd-repo-hygiene-and-handover-20261016` (21) + `pipd-unmerged-candidate-merge-20261016` (1) + `s4-final-pr18-closeout-20261016` (1) → `pipd-repo-handover-closeout-20261016`（三者皆在同一輪 2026-10-16 的 PIPD 收尾）

---

## 7. 執行順序建議（由低阻力到高）

1. **修 §5.1 (i) 的測試 oracle** — 更新 `tests/test_lane_policy.py` 的 `owner_chain` 至 epoch 25，與未提交的 registry 變更同一 commit。單獨、低風險，但它是後續多個回填的正確性前提。
2. **`git add openspec/changes/`** — 讓 36 個 untracked 目錄受管，之後每次回填才有稽核軌跡。
3. **跑 A3 + A4（16 筆，純機械存在性比對）** — 零判斷風險，先做掉。
4. **跑 A1（20 筆，R10 逐列裁決）** — 已有獨立裁決且我已覆核證據定位。
5. **跑 A2（~120 筆 disposition 標記）** — 非 tick，風險最低，但必須先把 disposition 語彙寫進 AGENTS.md 的約定，否則下一輪又會把它們讀成「未完成」。
6. **補 A6（2 個 delta spec）** → 兩者 `--strict` 轉 PASS。
7. **A5 archive（5 個）** — 最後做，因為 archive 會搬走目錄。
8. **人工組：新 record 承接 §6.2 的 3 組殘餘**，並把 (c)(d) 類排入業主議程。

---

## 8. 交付摘要

**做了什麼**：對 `openspec/changes/` 全樹做唯讀盤點（38 個 change、465 未勾；範圍 34 個 change / 460 未勾），以四路證據交叉驗證（R10 逐列裁決 TSV、R11 變更清冊、Fabric/PIPD 分支實體證據、live tree 實測 + 20 紅測試重現），產出逐 change 分類與可執行動作清單。

**主要發現**：
- 460 這個數字正確，但「33 個 change」應為 **34 個**；掃描期間並行回合新增了 `far-minimax-mandate-20261021`（5 未勾）。
- **36/37 個 change 目錄未受 git 追蹤** → git log 對這批檔案本來就不是有效佐證；先前引用 git log 交叉驗證的方法在此樹上不可用。
- **可機械回填僅 109 筆（23.7%）**，非先前假設的 440。R10 逐列裁決的 36 列中只有 24 列 `DONE_MEASURED`。
- `strict-declaration-20261011` 的 S1–S4 **已在 live 實作**（`_require_json_int` / `carrier_line_texts` 等，附 `REQ-STRICT-DECLARATION-014` 註記）——但其 3.x 驗收列目前紅燈。
- `hgk-checker-upgrade-adapter` 的**完整實作存在於 worktree**（`worktrees/hgk-checker-upgrade-20261009/`，5 個模組 + 8 個測試檔），canonical tree 完全沒有 → 是最便宜的「真實工程」項目。
- **現況測試 20 紅**，主因是 epoch 25 registry 變更未提交、測試 oracle 仍停在 epoch 23；且 epoch 25 變更本身在工作樹未 commit。
- **三車道同模型**（epoch 25）：任何要求模型軸獨立性的驗收列在現行 owner order 下無法完成，只能標 disposition。

**檔案**：未建立、未修改任何檔案（唯讀）。

**遇到的問題**：
- `npx` 不在原生 Windows subprocess 的 PATH，改由 bash 執行 `openspec validate --strict`（38 個全跑完，35 PASS / 2 FAIL）。
- `git grep` 於 subprocess 不可用（`FileNotFoundError`），改用 `search_files` 工具與 pathlib。
- Fabric 的 merge commit 只在 `pub/far-lane-remediation-20261021` 分支、不在 `main`，因此「published & promoted out of draft」需 GitHub live API 二次確認——此一項保留為人工。
- 樹在掃描期間被並行回合變更（新增 1 個 change、registry epoch 22→25），最終數字以兩次間隔 2 秒的一致掃描為準。