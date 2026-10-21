All evidence gathered and verified. Here is the deliverable.

---

# 知識庫比對報告：HG-KSEOS 三個待處置主題 × 知識庫既有裁決／方法論／先例

**比對範圍**：`C:/Projects/Agent_Workspace/知識庫/實作相關DOC`（7,322 檔，以 `find`/`grep` 定位，未逐檔讀取）
**控制平面**：`C:/Projects/Agent_Workspace/HG-KSEOS`
**性質**：唯讀比對。未修改任何檔案、未執行 git 寫入、未 commit/push。

---

## 0. 關鍵前置發現（改變本回合的性質）

在比對開始時發現：**控制平面本身已針對本回合三個主題完成FAR 研究與索引**，位於
`C:/Projects/Agent_Workspace/HG-KSEOS/var/FAR-MINIMAX-MANDATE-20261021/`：

| 產出 | 內容 |
|---|---|
| `FAR-RULING-REPORT.md` | 五項裁決建議（A=OpenSpec 460 項、B=var/ 120 目錄、C=TT 2 項、D=模型軸、E=delegation） |
| `OPENSPEC-UNCHECKED-INDEX.md` + `openspec_unchecked_index.json` | 460 個未勾項逐 change 索引，**套用 tick 數 = 0** |
| `VAR-DISPOSITION-INDEX.md` + `var_disposition_index.json` | 120 個 var/ 目錄七類分類，**破壞性動作 = 0** |
| `research/TASK-1_RESEARCH.md` | var/ 處置裁決清單（含「不得以 receipt 存在批次標 COMPLETED」） |
| `research/TASK-2_RESEARCH.md` | TT-001/TT-002 處置裁決 |

且 `openspec/changes/far-minimax-mandate-20261021/tasks.md` §5 明確將本回合三主題列為
**Ruling A / B / C**，全部維持 `[ ]` 未勾，狀態為「Blocked on the owner's ruling (NOT done)」。

**因此本報告的定位是**：不是重新提出裁決，而是**為該裁決找出知識庫的既存依據與先例**，
並確認裁決是否與知識庫既有裁準一致、是否觸及知識庫缺口。

**重測事實**：本次唯讀重測得 460 未勾項（35 個 change 有未勾項，含 `archive/` 0 項）、`var/` 頂層 121 目錄、TT ledger `status=="OPEN"` 恰 2 筆 — 與 FAR 報告一致（業主引用的 471 / 114 為舊快照）。

---

## (a) 找到的最相關檔案清單

### A 類：直接先例（同一控制平面 / 同一產品面，可直接複用）

| # | 絕對路徑 | 為何相關 | 可複用之處 |
|---|---|---|---|
| A1 | `C:/Projects/Agent_Workspace/知識庫/實作相關DOC/SWOF/實作證據/W2R1/HGK_EBC_ACCEPTANCE_RESOLUTION.json` | **TT-001/TT-002 的原始出處**。JSON 含 `tt` 區塊逐字記錄兩筆 OPEN 的 subject/owner/close_criteria/why_not_here，另含 4 輪獨立 checker 的 13 筆 `findings_and_disposition` | 直接複用為 TT-002 的裁決證據鏈（acceptance 子範圍 revision 3 已修好，general contract 未裁定 → 帳本維持 OPEN）；TT-001 的「schema extension 超出本 ChangeSet 範圍」原文理由可直接引用 |
| A2 | `C:/Projects/Agent_Workspace/知識庫/實作相關DOC/HG-KSEOS/FAR-SWOF-KSEOS-RCA-001/IntegratedFindings.yaml` | 三車道獨立 lane 的缺陷分類。含 `EVIDENCE_SET_INCOMPLETE`（required raw artifacts present only as summary booleans）、`Candidate published without IndependentReceipt PASS`、`Non-blocking carried debt repeatedly deferred without a closure trigger (recurs)` | 「未結案項累積」「receipt 存在≠完整證據」「debt 須有 closure trigger」三條紀律的出處 |
| A3 | `C:/Projects/Agent_Workspace/知識庫/實作相關DOC/HG-KSEOS/FAR-SWOF-KSEOS-RCA-001/impl/acceptance_integrity_checks.py` | C1–C8 可執行控制點。C6 明文 `C6.published_without_checker_pass`（publication_state=PUBLISHED 但無 IndependentReceipt verdict PASS）；`_na()` 回傳 `NOT_APPLICABLE` 而非 pass；C3 要求 round identity 一致 | 「存在 receipt 不足以結案」與「不能 evaluate 不得算 pass」的可機器化實作範本 |
| A4 | `C:/Projects/Agent_Workspace/知識庫/實作相關DOC/HG-KSEOS/FAR-SWOF-KSEOS-RCA-001/ProposedEvolution.yaml` | 每個控制點都有 `blast_radius: SMALL`、`gated_on`（阻塞前提）、`catches`（對應缺陷類）、`closes_challenge_condition`。C3 明文豁免 `historical/ superseded/` 與 cumulative bundle | 「最小改動 + 阻塞前提 + 對應缺陷類」的裁決書寫格式，可直接套用於本回合三主題 |
| A5 | `C:/Projects/Agent_Workspace/知識庫/實作相關DOC/HG-KSEOS/FAR-SWOF-KSEOS-RCA-001/FAR_DELIVERY_RECEIPT.json` | `live_defect_found_and_fixed` 段落：9 輪獨立驗證都漏掉的缺陷被 control C3 抓到。含 `non_claims` 清單（NOT_EXTERNALLY_ACCEPTED / NOT_MERGED / NOT_RELEASED / NOT_PRODUCTION / NO_LIVE_WORLD_EFFECT） | 「非主張清單」格式；以及「自動化控制可補人/模型審查的漏網」的方法論依據 |
| A6 | `C:/Projects/Agent_Workspace/知識庫/實作相關DOC/HG-KSEOS/FAR-SWOF-KSEOS-RCA-001/impl/HGK-EBC-ORDERING-ORACLE-001.json` | `precedent` 欄位（既有程式碼中找可複用的既有解法）、`regression_proof.attribution`（區分 pristine-equivalent 與新引入失敗）、`non_claims` | 裁決前的「先找既有先例」步驟範本；避免重造機制的依據 |
| A7 | `C:/Projects/Agent_Workspace/知識庫/實作相關DOC/HG-KSEOS/HG-KSEOS使用說明文檔.md` | §29：TT ledger 維護流程「更新 `source-freeze/TT_LEDGER.csv` 後 `scripts\reconcile-tt.ps1`」；§25 交付判斷六項依序（含 `blocking TT = 0`）；§26 unique predicate ID 計數、duplicate ID 本身是 fail-closed defect | TT ledger 的**既有變更程序**（已存在 `scripts/reconcile-tt.ps1` → `hg_kseos.cli reconcile-tt`），TT 狀態變更不需要新機制 |
| A8 | `C:/Projects/Agent_Workspace/知識庫/實作相關DOC/HG-KSEOS/Fabric_HG-KSEOS_Convergence/驗收報告/Fabric_FAR018_FAR019_Archive_Independent_Acceptance_20261016.md` | **最接近本回合主題 1 的歸檔先例**。§1「直接發布／MERGE MAIN／暫時結案矩陣」逐項裁決（GO / 局部 PASS / HOLD）；明文「不要求修補完 M04/M06/M16、60 項 Owner 決定、221 需求測試及八個完整 Runtime Gates 才合併」；「不能把 lane 執行聲稱 PASS」（EXECUTE exit=TIMEOUT 但 writer artefacts 存在）；「不為了製造一份漂亮 PASS 重啟一整輪」 | 未完成項**不阻擋歸檔**、但**必須保留限制聲明**的裁決先例；「GO 是工程放行建議，不是替代權限」 |
| A9 | `C:/Projects/Agent_Workspace/知識庫/實作相關DOC/HG-KSEOS/Fabric_HG-KSEOS_Convergence/PROMPT/Fabric × Hermes × HG-KSEOS｜FAR-018／FAR-019 歸檔指揮薄 PROMPT.md` | 機器標頭含 `change_set: EVIDENCE_ONLY`、`max_this_round_claim: CANDIDATE_EVIDENCE_ARCHIVED_ONLY`；§4 處置矩陣：`DEFERRED_SEPARATE_OWNER_ADMITTED_CHANGESET` / `DEFERRED_OR_CONDITIONALLY_BLOCKING_ON_ACTIVATION` / `FORBIDDEN_THIS_CHANGESET`；「不可把版本差當統一分母」 | 未勾項的**三類 disposition 詞彙**（deferred / forbidden / separate changeset）可直接複用 |
| A10 | `C:/Projects/Agent_Workspace/知識庫/實作相關DOC/HG-KSEOS/Fabric_HG-KSEOS_Convergence/Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md` | dangling legacy alias 案例（`CR-PIPD-01` → `TT-PIPD-03`）：「正確判定=`EXPECTED_REJECT / NOT_EVIDENCE_OF_PASS`」，並要求加負測「把 CR-PIPD-01 當 active ticket 必 FAIL」 | **tick 語意的關鍵先例**：被取代的項目標記為 superseded 而非 tick，並配負向測試 |
| A11 | `C:/Projects/Agent_Workspace/知識庫/實作相關DOC/FAR/USER_DECISION_FAR_RETRIEVAL_2026-08-13_001.md` | USER 決策記錄的欄位格式：`decision_id / authority / decided_at / status: FROZEN / supersedes / supersession_basis / bound_into` | 若三主題裁決需業主簽核，可直接沿用此 decision record 格式（含 supersession 欄位處理未來推翻） |
| A12 | `C:/Projects/Agent_Workspace/知識庫/實作相關DOC/HG-KSEOS/FAR-SWOF-KSEOS-RCA-001/LaneD_RootCause.json` | 根因欄位含 `existing_control_state: present-but-unenforced` 與 `minimal_control`；`would_have_caught` 陣列 | 「控制已存在但未強制執行」的鑑別框架 — 對判斷某主題是補執行還是補機制很有用 |

### B 類：其他專案面（方法論可借用，裁決不可直接套用）

| # | 絕對路徑 | 為何相關 | 可複用之處（僅方法論） |
|---|---|---|---|
| B1 | `C:/Projects/Agent_Workspace/知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric/PIPD/PIPD_LS/PIPD_LS_DOC-01_2026-10-07_r2_HIGH_RETENTION_FULL_REPAIR_FULL_SUBSTANTIVE_BODY.md` | §5.1 六個 **degrade/side states**：`HOLD / TEMP_CLOSED / REWORK_REQUIRED / REJECTED / SUPERSEDED / INVALIDATED`，各含 Meaning / Canonical lifecycle effect / Exit path / Claim-ceiling effect；§10 四個 typed namespace（`lifecycle_state` / `degrade_status` / `decision` / `claim_ceiling`）與「conversion is one-way and rule-bound: none may be assigned by string resemblance」 | **最有價值的詞彙來源**：給 460 個未勾項一種不需改動生命週期的表達方式（`TEMP_CLOSED` 而非 tick）；且明示「不得注入 lifecycle_state」 — 直接防範用勾選語意污染狀態機 |
| B2 | `C:/Projects/Agent_Workspace/知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric/PIPD/PIPD-LS-SP_藍圖/PIPD-LS-SP_PIPD-EC_SGM_總藍圖.md`（L2008） | §10 Acceptance Checklist 17 項中 **15 項 `[x]`、2 項 `[ ]`**，§10.1 作者側裁決：「未勾選的兩項屬外部/後續 evidence gate，因此本檔仍不得宣稱 `INDEPENDENT_PASS / RUNTIME_QUALIFIED / RELEASED / PRODUCTION_PASS`」 | **「未勾項即封頂」的直接範本**：未勾項不必被消除，但必須限制 claim ceiling。可直接複用為 460 項處置後的封頂敘述 |
| B3 | `C:/Projects/Agent_Workspace/知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric/PIPD/PIPD-LS-SP_skeleton.md`（L226030 附近） | `FIX-09-D06-H2-3-APPARENT_PASS` fixture：「backlog item marked done despite no owner decision / receiver ACK → `BACKLOG_SCOPE_UNKNOWN`」；以及 BF12 **Residue exact-set**：`secret/token/remote/temp/cache/state/rights/license` 每類各有 `scanned_at, scope, found_count, permitted_exception, checker, remedy, post_scan_hash`，「沒有證明不得宣稱清理完成」 | **「假完成」的具名反例**（APPARENT_PASS）— 可作為 tick 驗證的負向 oracle；**Residue exact-set 欄位表**可複用為 var/ 清理證據格式 |
| B4 | `C:/Projects/Agent_Workspace/知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric/SBL/SBL_PIPD-LS-PKG/SBL_PIPD-LS-PKG_DOC-10.md`（L2918） | `raw_evidence_expectations` 欄：「只接 Owner RAW receipt；**設計檔空值不代表 PASS**」；raw missing → `NOT_EXECUTED`；`ExecutionReceipt` 的 `actual_run_state=OBSERVED|NOT_EXECUTED` / `actual_outcome=PASS|FAIL|INCONCLUSIVE|NOT_EXECUTED`；「模擬測試/本文作者 static schema PASS 不得填進 actual」 | **「空值/預期值 ≠ PASS」的欄位級硬約束** — 可複用為 var/ 目錄與 460 項的完成判定欄位規格 |
| B5 | `C:/Projects/Agent_Workspace/知識庫/實作相關DOC/PIPD/驗收報告/PIPD-LS-SP S4 修補後外部獨立複驗暨三合一小型升級實作驗收_20261013.md`（§4.4） | 裁定 `YES_SCOPED_PRE_RELEASE_HYGIENE`；「**不准歷史改寫或壓平 raw evidence**」；歷史證據政策「`source-in-repo` + `append-only evidence archive` + digest/locator handoff」「既有證據應 **archive + manifest + readback**」；並列出「不放行的過度工程」清單 | **var/ 處置的作業政策**：不刪 raw evidence、archive+manifest+readback；且有現成的「過度工程」拒絕清單可套用 |
| B6 | `C:/Projects/Agent_Workspace/知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric/【1】SWOF/SWOF_設計規劃文檔/SWOF_設計規劃文檔_DOC-07_2026-08-20_r2.md`（C02.4） | Cleanup closure 條件：停止 process、關閉 provider session/credential scope、解除 mount/lock、清理 ephemeral artifacts、保存 required raw evidence、確認 no active writer、做 residue scan；「**若無法證明乾淨，不能標 `CLEANED`，應 `QUARANTINED`**」 | 清理的**兩值**結論（CLEANED / QUARANTINED）與八項 closure 條件 |
| B7 | `C:/Projects/Agent_Workspace/知識庫/實作相關DOC/Fabric/RP-002_v2.0_DOC/RP-002_v2.0_Master_Blueprint_2026-08-12_r2.md`（L660 附近） | `idempotency:` 區塊：`idempotency_key / side_effect_class / replay_policy: SAFE_REPLAY|READBACK_BEFORE_RETRY|FORBIDDEN / prior_effect_receipt_ref`；`terminal:` 區塊：`worker_exit_zero_is_pass: false`；`session_end_is_terminal: false` | **TT-002 的跨實體冪等契約雛形**（`side_effect_class` + `replay_policy` 分級 + `prior_effect_receipt_ref`），可直接作為「明定跨 entity 拒絕契約」的結構參考 |
| B8 | `C:/Projects/Agent_Workspace/知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric/PIPD/PIPD-LS-SP_PIPD-PKG/PIPD-LS-SP_PIPD-PKG-01_2026-10-08_r2_HIGH_RETENTION_AUDIT_REPAIR_FULL_INTEGRATED_SUBSTANTIVE_BODY.md` | `idempotency_key` 欄位規格與 deterministic reject matrix（wrong subject → 拒絕）；PKG-00 L8800：`OPS_ECP_NACK_UNRECONCILED_EFFECT`（Provider HTTP 200 與 `EFFECT_UNKNOWN` 同時出現 → 先隔離相同 idempotency_key） | TT-002 的具體拒絕碼與隔離程序 |
| B9 | `C:/Projects/Agent_Workspace/知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric/SBL/參考工程資料庫/PROMPT／實作／驗收_紀錄/PROMPT／實作／驗收_紀錄_vol-04.md`（L2536） | `openspec validate --strict` → valid；`openspec list` → **✓ Complete（23/23 task 已勾；5.5 與 5.6 標 `[~]` 並具名殘留）**；另有 `npx openspec validate --changes --strict`（L770） | **openspec 自身的完成語意**：全勾才 Complete；部分未完成用 `[~]` 具名殘留。本回合 460 項**無一**處於這種狀態 → 開啟中的 change 全部是「未完成」而非「具名殘留」 |
| B10 | `C:/Projects/Agent_Workspace/知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric/PIPD/PIPD-LS-SP_skeleton.md`（L4688 附近） | 決策詞彙 `TEMP_CLOSED` 定義；`NO_PROMOTION`；「No inference from lower authority or memory」 | 詞彙一致性佐證（與 B1 同源） |
| B11 | `C:/Projects/Agent_Workspace/知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric/PIPD/PIPD-LS-SP_PIPD-PKG/PIPD-LS-SP_PIPD-PKG-09_2026-10-08_r2_HIGH_RETENTION_AUDIT_REPAIR_FULL_INTEGRATED_SUBSTANTIVE_BODY.md` | `evidence_status: DESIGN_EXAMPLE_NOT_EXECUTED`；「本次沒有外部 runtime，因此所有上述 fixture 的 `actual=NOT_EXECUTED`，**不得填入預期決定冒充實測結果**」 | 「預期值不得填入實際欄位」的紀律 |
| B12 | `C:/Projects/Agent_Workspace/知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric/SBL/SBL_PIPD-LS-PKG/SBL_PIPD-LS-PKG_DOC-04.md` | 342 個技術候選的處置詞彙：`BORROW_ADAPTER / SECONDARY_CORPUS / OPTIONAL_ATTACK_DONOR / OBSERVABILITY_CANDIDATE / DONOR_ONLY` + `DEFERRED_OWNER_HOLD` + `OWNER_DECISION_PENDING` | 「逐項分類 + 各自 disposition」的**大規模分類詞彙表**，適用於 460 項逐項標註 |

---

## (b) 知識庫已有的裁準 vs 三主題需要的裁準 — 差距分析

### 主題 1：460 個未勾項（33 個 change）

| 面向 | 知識庫已有 | 三主題需要 | 差距 |
|---|---|---|---|
| tick 的證據要求 | **A8/A10** 已有「回填必須可交叉驗證」「被取代項標 superseded 而非 tick」「必須配負向測試」 | 每個 tick 須指名 commit 或檔案 | **無實質差距** — 已有完整範式 |
| 未勾項的表達 | **B1/B2** 已有 `TEMP_CLOSED` / 「未勾選即封頂 claim ceiling」 | 460 項各自歸類到既有狀態詞彙 | **無實質差距** — 詞彙現成 |
| 分類詞彙 | **A9** 已有 `DEFERRED_SEPARATE_OWNER_ADMITTED_CHANGESET` / `DEFERRED_OR_CONDITIONALLY_BLOCKING_ON_ACTIVATION` / `FORBIDDEN_THIS_CHANGESET`；**B12** 已有 342 項分類詞彙表 | 460 項逐項標註 | **無實質差距** |
| 「假完成」的負向 oracle | **B3** 已有 `APPARENT_PASS` fixture（標 done 但無 owner decision） | 防止未驗證的批量 tick | **無實質差距** |
| 開放中 change 的處理 | **B9** 顯示 openspec 自身語意：全勾=Complete，部分未完=`[~]` 具名殘留 | 33 個 change 無一處於此狀態 | **缺口**：知識庫**沒有**「change 全未完成時該如何處置」的裁準。openspec 的 `[~]` 語意只覆蓋「大部分完成、少數殘留」，不覆蓋「近乎全未勾」。這正是 460 項的主因 |
| 分母定義 | **A2** 有 `EVIDENCE_SET_INCOMPLETE`（summary boolean ≠ raw artifact） | 460 這個分母本身是否可作工作分母 | **缺口**：知識庫沒有「未勾項計數分母的定義裁準」（本回合 FAR 已用「38 active / 34 有未勾」解決） |
| 處置權限 | **A8** 有「GO 是工程放行建議，不是替代權限」；**A12** 有 `existing_control_state: present-but-unenforced` | 誰能關閉 460 項 | **無實質差距** |

### 主題 2：var/ 121 個頂層目錄

| 面向 | 知識庫已有 | 三主題需要 | 差距 |
|---|---|---|---|
| 「數量 ≠ 未結案回合」 | **A2** 有 `EVIDENCE_SET_INCOMPLETE`；**B4** 有 `NOT_EXECUTED` 欄位 | 拒絕把 114/121 當工作分母 | **無實質差距** |
| 清理/處置的 closure 條件 | **B6** 有八項 closure 條件 + `CLEANED`/`QUARANTINED` 二值 | 每個目錄的處置動作與證據 | **無實質差距** |
| 殘留掃描證據格式 | **B3** 有 BF12 Residue exact-set 七欄位（`scanned_at/scope/found_count/permitted_exception/checker/remedy/post_scan_hash`） | 刪除前的殘留證據 | **無實質差距** |
| 不可刪的歷史證據 | **B5** 有 `append-only evidence archive` + `archive + manifest + readback` + 「不准壓平 raw evidence」 | var/ 內含 raw evidence | **無實質差距** |
| 分類詞彙 | **A4** 有 `blast_radius` / `gated_on`；**B12** 有候選分類詞彙 | 七類分類（ROUND_ARTIFACT / ROUND_OPEN / RUNTIME_OR_CACHE / EMPTY / UNCLASSIFIED） | **部分差距**：知識庫的詞彙是**能力/候選分類**（該不該用），不是**產物生命週期分類**（是回合產物還是 runtime）。這是本回合 FAR 自行建立的 |
| **var/ 專屬的處置裁準** | — | 「var/ 這個特定目錄的產物保留政策」 | **實質缺口**：知識庫**完全沒有** HG-KSEOS `var/` 頂層的分類／歸檔／保留期方法論。`HG-KSEOS使用說明文檔.md` 只提到 `var/shared-spine/`、`var/workbench/`、`var/backups/` 三個具名子路徑用途，**無任何 var/ 整體治理規則**。B5 的 repo hygiene 政策是針對 **git tree**（PIPD repo），不是 var/ |
| 刪除授權 | **B5** 有「不放行的過度工程」；**A8** 有「需 Maintainer 明確批准」 | 刪除需業主批准 | **無實質差距** |
| 不可讀子樹 | — | 5 棵含不可遍歷子樹（10,314 次 os.walk 錯誤回呼） | **缺口**：知識庫沒有「盤點不完整時如何標記」的裁準。B3 的 `found_count` + `permitted_exception` 可借用，但 var/ 特定不可讀情境無先例 |

### 主題 3：TT ledger 2 筆 OPEN

| 面向 | 知識庫已有 | 三主題需要 | 差距 |
|---|---|---|---|
| 變更程序 | **A7** 有既有流程：`source-freeze/TT_LEDGER.csv` → `scripts\reconcile-tt.ps1` → `hg_kseos.cli reconcile-tt`（已存在，bootstrap.py:108-132） | 改變 TT 狀態 | **無實質差距** — 不需要新機制 |
| TT 登錄的治理紀律 | **A1** 有 4 輪 checker 的發現：曾在**錯誤的 spine** 登錄（project spine 而非 canonical）、行數記錯（12 vs 11） | 正確登錄與回讀 | **無實質差距** — A1 已記錄完整教訓 |
| 「部分修復不得擴張為整筆關閉」 | **A1** EBC-R2-BLK-1 處置原文；**B2** 「未勾選即封頂」 | TT-002 acceptance 子範圍已修 vs 整筆維持 OPEN | **無實質差距** — FAR 裁決 C1 與知識庫一致 |
| 冪等命名空間的跨實體契約 | **B7** 有 `idempotency:` 四欄位 + `replay_policy: SAFE_REPLAY\|READBACK_BEFORE_RETRY\|FORBIDDEN` + `prior_effect_receipt_ref`；**B8** 有 reject matrix 與 `OPS_ECP_NACK_UNRECONCILED_EFFECT` | TT-002「明定跨 entity 拒絕契約並補齊 writer」 | **部分差距**：知識庫有**結構**，但沒有**針對 canonical_events 全域 UNIQUE 跨實體**的裁決。等級是「應用 XP 設計紀律到既有 SPI」，不是「照抄既有裁決」 |
| 「存在 ≠ 綠燈」 | **A3** C6；**B4**；**B11**；**B7** `worker_exit_zero_is_pass: false` | 全主題共通 | **無實質差距** — 這是知識庫最強的一條紀律 |

### 跨主題的共同缺口

1. **知識庫沒有「HG-KSEOS 專屬的 tick / disposition 裁準文件」**。所有相關紀律散落於 8+ 個不同專案面的檔案中（A2/A3/A8/A9/A10/B1/B2/B3/B4），且彼此沒有交叉引用。FAR 裁決若要引用，須新建一份裁準文件把這些散落的紀律收斂為單一權威 — 這本身是本回合可交付的產出。
2. **知識庫沒有 HG-KSEOS `var/` 的任何治理方法論**（主題 2 的實質缺口）。B5 的 repo hygiene 是最接近的，但它治理的是 git tree blob，不是本機未版控的 var/。兩者風險模型不同（git 可 revert、var/ 不可逆）。
3. **A2 記錄了一個反覆出現的失敗模式**：`Non-blocking carried debt repeatedly deferred without a closure trigger (recurs)`。這說明「非阻塞債」若無 closure trigger 就會無限累積 — 而 460 個未勾項正是這類債的典型形態。知識庫已預警，但沒有給出 460 規模的處置機制。

---

## (c) 可複用 / 不可套用判定表

### 可直接複用（同一控制平面 / 同一產品面 / 裁決語意一致）

| 檔案 | 複用範圍 | 複用方式 |
|---|---|---|
| A1 `HGK_EBC_ACCEPTANCE_RESOLUTION.json` | 主題 3 全域 | TT-001/TT-002 的 subject/owner/close_criteria/why_not_here 原文；TT-002 裁決 C1「子範圍已修、整筆維持 OPEN」的證據鏈 |
| A2 `IntegratedFindings.yaml` | 三主題共通 | `EVIDENCE_SET_INCOMPLETE` / `published without IndependentReceipt PASS` / `carried debt without closure trigger` 作為紀律出處 |
| A3 `acceptance_integrity_checks.py` | 主題 2 / 1 | C6 `_na()` 的「不能 evaluate 不算 pass」；作為 var/ 目錄結案的機器化 oracle 範本 |
| A4 `ProposedEvolution.yaml` | 三主題 | 裁決書寫格式（`blast_radius` / `gated_on` / `catches`）— 本回合三項裁決同格式 |
| A5 `FAR_DELIVERY_RECEIPT.json` | 三主題 | `non_claims` 清單格式（NOT_EXTERNALLY_ACCEPTED / NOT_MERGED / NOT_RELEASED / NOT_PRODUCTION） |
| A6 `HGK-EBC-ORDERING-ORACLE-001.json` | 三主題 | `precedent` 欄位 =「裁決前先找既有解法」步驟；`regression_proof.attribution` |
| A7 `HG-KSEOS使用說明文檔.md` §25/§26/§29 | 主題 3 | TT ledger 變更程序（`reconcile-tt.ps1`）與 `blocking TT = 0` 交付條件 |
| A8 `Fabric_FAR018_FAR019_Archive_Independent_Acceptance_20261016.md` | 主題 1 | 未完成項不阻擋歸檔、但須保留限制聲明；「不為漂亮 PASS 重啟一整輪」；逐項 GO/HOLD 矩陣 |
| A9 `FAR-018／FAR-019 歸檔指揮薄 PROMPT.md` | 主題 1 | 三類 disposition 詞彙（DEFERRED / FORBIDDEN / separate changeset）+ `EVIDENCE_ONLY` claim ceiling 結構 |
| A10 `Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md` | 主題 1 | superseded 項標記法 + dangling alias 負向測試要求 |
| A11 `USER_DECISION_FAR_RETRIEVAL_2026-08-13_001.md` | 三主題 | 業主裁決記錄欄位格式（含 supersession 欄位） |
| A12 `LaneD_RootCause.json` | 三主題 | `existing_control_state: present-but-unenforced` 鑑別框架 |
| **本回合** `var/FAR-MINIMAX-MANDATE-20261021/` 全部 5 份產出 | 三主題 | 已完成的實測索引與裁決草案（460 / 120 / 2 的重測依據、tick=0、destructive=0） |

### 僅方法論可借用（其他專案面；詞彙可用，裁決不可套用）

| 檔案 | 可借用 | **不可套用的原因** |
|---|---|---|
| B1 `PIPD_LS_DOC-01` §5.1/§10 | 6 個 degrade state 與 4 個 typed namespace 的**詞彙與定義** | PIPD 是另一產品的生命週期規範（14 個 canonical lifecycle states）。其狀態集與 HG-KSEOS 的 WorkOrder/acceptance 模型不同；**不能把 PIPD 的 lifecycle_state 灌進 HG-KSEOS**。§10 明文禁止跨型別賦值 |
| B2 `PIPD-LS-SP_PIPD-EC_SGM_總藍圖.md` §10.1 | 「未勾選項即封頂 claim ceiling」的**敘述結構** | 該文件是 PIPD blueprint 的作者側自證，其 2 個未勾項是外部 evidence gate；460 個未勾項是工程工作缺口，性質不同。**不可套用「不需處理」的推論** |
| B3 `PIPD-LS-SP_skeleton.md` | `APPARENT_PASS` 具名反例（可當 tick 的負向 oracle）；BF12 Residue exact-set 七欄位 | PKG-09 的 `BACKLOG_SCOPE_UNKNOWN` 對應的是「provider incident 無 affected subject mapping」。460 項的失效模式不同，**只能借用「假完成必須有具名反例」的紀律，不能借用該錯誤碼** |
| B4 `SBL_PIPD-LS-PKG_DOC-10.md` | `actual_run_state` / `actual_outcome` 欄位規格；「設計檔空值不代表 PASS」 | SBL 的 DOC-10→11→12 handoff 契約。**欄位可借用，但 SBL 的 `NOT_EXECUTED` 語意綁在 SWOF Native Bridge**，不可直接當作 HG-KSEOS 460 項的狀態機 |
| B5 `PIPD-LS-SP S4 ... 實作驗收_20261013.md` §4.4 | `YES_SCOPED_PRE_RELEASE_HYGIENE` 裁決型態；「append-only evidence archive + archive/manifest/readback」；「不放行的過度工程」清單 | 該政策治理的是 **PIPD git repo 的 blob 肥大**，且明確「不准歷史改寫或壓平 raw evidence」是因為 git 有 tag/asset 保護。**var/ 是本機未版控、不可逆**，同樣政策不足，**不可直接套用**（尤其「不要此刻刪除 raw log」的結論在 var/ 需另行裁決） |
| B6 `SWOF_設計規劃文檔_DOC-07` C02.4 | 八項 cleanup closure 條件；`CLEANED`/`QUARANTINED` 二值 | SWOF 的 WorkspaceBinding/SandboxLease 語境。**方法可借用，詞彙（mount/lease/epoch）不適用於 var/ 靜態產物** |
| B7 `RP-002_v2.0_Master_Blueprint` | `idempotency:` 四欄位 + `replay_policy` 三值 + `prior_effect_receipt_ref`；`worker_exit_zero_is_pass: false` | RP-002 是 HAOS/Fabric/Hermes 聯邦架構的藍圖。**其 idempotency 契約未針對 canonical_events 的全域 UNIQUE 問題裁決過**，屬「設計語彙可借用、裁決尚不存在」 |
| B8 `PIPD-LS-SP_PIPD-PKG-01` | reject matrix 與 `OPS_ECP_NACK_UNRECONCILED_EFFECT` 隔離程序 | 對象是 ECP 層的 provider effect，不是 shared core 的 canonical_events。**不可套用為 TT-002 的解決方案** |
| B9 `驗收_紀錄_vol-04.md` L2536 | openspec 自身的完成語意（全勾=Complete / 部分=`[~]` 具名殘留）；`openspec validate --strict` / `npx openspec validate --changes --strict` 指令 | 屬 openspec 工具語意，不是治理裁準。**只可用來說明 460 項不屬 openspec 原生可接受的殘留形態** |
| B10 `PIPD-LS-SP_skeleton.md` L4688 | `TEMP_CLOSED` 詞彙一致性佐證 | 與 B1 同源，冗餘佐證 |
| B11 `PIPD-LS-SP_PIPD-PKG-09` | `DESIGN_EXAMPLE_NOT_EXECUTED` 紀律 | 設計文件層，非執行證據層 |
| B12 `SBL_PIPD-LS-PKG_DOC-04.md` | 342 項的分類詞彙表（`BORROW_ADAPTER` / `DEFERRED_OWNER_HOLD` / `OWNER_DECISION_PENDING`） | 詞彙是**技術能力候選**分類，不是**未完成工作項**分類。**可借用「每項各有 disposition + owner + 閘門」的結構，不可借用詞彙本身** |

### 明確不可套用（其他產品面）

| 檔案 | 原因 |
|---|---|
| `Fabric vNext/.../CCPS & AMC—ZOP/*`（AMC—ZOP 藍圖、AMC 地區型生產驛站） | 工業控制/生產驛站領域（ISA-95、eAMR、OEM 授權）。與 HG-KSEOS 治理無關 |
| `Fabric vNext/.../S-2W2AC_PUEMR/*`（雙足輪/輪椅/汽車底盤藍圖） | 機械設計產品面。與工程治理無關 |
| `Fabric vNext/.../【1】SWOF/SWOF／GENIE.../MSC／ECP／TQAEP/*` | SWOF/GENIE 產品線的 ECP/TQAEP 包 |
| `Fabric vNext/.../SDLC_PRW_HLPE_SKILLS_PLUGIN_R2.md`、`SWOF_ECP/TQAEP_SKILLS_PLUGIN` | SWOF/SDLC_PRW_HLPE 技能包 |
| `StoryForge/**`（1,860 檔）、`Fabric vNext/.../【2】GENIE/**` | 小說創作產品面 / GENIE 產品線 |
| `Fabric vNext/Semantic World OS Fabric/SBL/參考工程資料庫/PROMPT／實作／驗收_紀錄/vol-01..10.md`（10 檔，~9.5MB） | 屬**工作逐字稿日誌**（含 Hermes session transcript）。可作事實來源（如 B9 的 openspec 記錄），但**不是裁準文件**，不可引用為治理依據 |
| `FAR/` 下的 `藍圖&升級方案/`、`討論&設計原意/`（fabric-autonomous-research 藍圖與討論稿） | FAR 是研究機制本身的藍圖，非處置裁準 |
| `FDA/` | **未檢查** — 該目錄受環境保護，需明確授權方可讀取 |

---

## 三項裁決與知識庫一致性檢核（總結）

| 主題 | FAR 裁決 | 知識庫既有裁準 | 一致？ |
|---|---|---|---|
| 1（460 項） | A1 只回填「可交叉驗證的 19 個」且逐項附證據、不接受批次回填；A2 superseded 標 disposition 不打勾；A3 其餘 441 項不建議關閉 | A10（superseded 不 tick + 負測）、A8（逐項 GO/HOLD + 保留限制聲明）、B3（APPARENT_PASS 反例）、B2（未勾即封頂） | **完全一致** — 知識庫已有全部依據 |
| 2（var/） | B1 不刪除任何目錄（三理由：其他 session 同根寫入、不可逆、低風險需可逆）；B2 以索引作處置投影；B3 僅 5 個 runtime/empty 需業主批准；B4 32 個 UNCLASSIFIED 逐個人工 | B5（不准壓平 raw evidence、archive+manifest+readback）、B6（cleanup 八條件、CLEANED/QUARANTINED）、B3（Residue exact-set 欄位）、A2（receipt 存在≠完整） | **一致，但知識庫有實質缺口** — 沒有 HG-KSEOS `var/` 專屬方法論；B5 的 git-tree 政策不能直接套用到未版控 var/ |
| 3（TT 2 筆） | C1 TT-002 acceptance 子範圍可整理為已完成證據但整筆維持 OPEN；C2 TT-001 進獨立 change（需 schema 變更）不列入本回合收尾 | A1（TT-001 why_not_here 原文即「schema extension 超出本 ChangeSet 範圍」；TT-002 disposition 原文即「resolved on acceptance path, retained as general contract note」）、A7（既有 reconcile 程序）、B2（部分修復不擴張） | **完全一致** — FAR 裁決 C1/C2 幾乎是 A1 原文的結構化重述 |

---

## 建議（給下一個執行回合）

1. **優先複用 A8 + A9** 作為 460 項裁決的敘事骨架：未完成項不阻擋本回合收尾，但必須保留限制聲明並明列 claim ceiling；被取代項標 disposition 而非 tick。
2. **主題 3 可立即執行**（無需業主裁決的部分）：A7 顯示 `scripts/reconcile-tt.ps1` 已存在，TT ledger 狀態變更不需要新機制。
3. **主題 2 需要先補一份裁準**（知識庫缺口）：在刪除任何 var/ 目錄前，先依 B3 的 Residue exact-set 七欄位 + B6 的八項 closure 條件建立「HG-KSEOS var/ 產物分類與保留政策」文件 — 這是知識庫目前完全沒有、而本回合必須裁決的東西。
4. **不要**把 B1 的 PIPD lifecycle state 灌入 HG-KSEOS；只用其詞彙表做 460 項的**注記欄位**，狀態機仍走 HG-KSEOS 自己的 `degrade_status` 等價物。
5. **建立一份收斂裁準文件**：把 A2/A3/A8/A9/A10/B1/B2/B3/B4 的散落紀律收斂為單一權威（A2 已預警 `carried debt without closure trigger (recurs)`，收斂後可設 closure trigger 防止同樣問題復發）。

---

**檔案建立／修改**：無。本回合為唯讀比對，未寫入任何檔案、未執行 git 寫入。
**遇到的問題**：`FDA/` 子目錄受環境保護（需明確授權），未檢查；`Fabric vNext/.../驗收_紀錄_vol-01..10.md` 共 ~9.5MB 為逐字稿日誌，僅作事實佐證未作裁準引用；`du -sh var` 在 180 秒內未回傳（已改用 `find` 計數取得 121 目錄 / 169 檔案）。