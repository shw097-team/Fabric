# FAR 裁決報告 — FAR-MINIMAX-MANDATE-20261021

**回合**：FAR-MINIMAX-MANDATE-20261021
**控制平面**：HG-KSEOS（`C:\Projects\Agent_Workspace\HG-KSEOS`）
**業主指令（2026-10-21，本回合）**：
- PLAN / EXECUTE（Codex CLI）/ VERIFY-SECURITY（Codex CLI）**全部**改用
  `MiniMax M3.1 Flash (OPENCODE GO)`
- FAR 對三個殘留主題做研究，**比對知識庫** `C:\Projects\Agent_Workspace\知識庫\實作相關DOC`，
  提出符合「低阻力、高可行、高工程必要性、不過度工程化、低風險」的最佳工程裁決建議，
  **讓用戶確認**
- 其他 session 正在進行 SBL 施工，必須分辨、避免干擾
- 啟用 KANBAN / SWARM / GSTACK / OPENSPEC，以 CODEX CLI + 多 SUB-AGENT 執行，
  並做自動化「自檢測、自修補、自驗收」
- 最後做受 FABRIC & HGK 治理的「自研究、自學習、自迭代、自進化」

> **本回合的裁決權歸屬**：業主要求「提出裁決建議讓用戶確認」。
> 因此本回合**只執行那些不需要裁決就能安全執行的部分**（量測、建立索引、綁定業主已明令的模型方案），
> 對**需要裁決的處置動作**（刪除、打勾、合併、歸檔）**一律只備料不執行**。

---

## 一、模型方案可行性（前置閘門）

業主要求「若無法使用以上模型方案，你必須直接暫停任務並告知用戶」。
本回合**沒有暫停**，因為三車道全部實測可用。

### 1.1 實測證據

| 車道 | 引擎 | 收據 | required_arm | served_arm | 結果 |
|---|---|---|---|---|---|
| PLAN | codex-cli（read-only 沙箱） | `probes/PLAN_admit.json` | `opencode-go/minimax-m3.1-flash-free` | 同左 | `ok=true`、exit 0、模型**真的驅動了 shell 工具** |
| EXECUTE | codex-cli（danger-full-access） | `probes/EXECUTE_admit.json` | 同左 | 同左 | 同上 |
| VERIFY_SECURITY | codex-cli（read-only 沙箱） | `probes/VERIFY_admit.json` | 同左 | 同左 | 同上 |

**HGK admission 結果**（`var/FAR-MINIMAX-MANDATE-20261021/admission/`）：

```
PLAN           -> ADMITTED
EXECUTE        -> ADMITTED
VERIFY_SECURITY-> ADMITTED
```

`decide_status` 的判定條件是實質性的，不是宣告性的：
`completed_model_calls >= 1` **且** `completed_tools >= 1` **且** served identity 與 arm 逐字相符。
三份收據的 `completed_tools = 1` 來自 dispatcher 收據中**實際的** `item.type == "command_execution"`
事件計數（不是自我宣稱）。

### 1.2 過程中被否決的三個做法（記錄，因為它們是「假綠燈」的來源）

1. **直接 completion 不算 admission** — `decide_status` 明文寫「A direct completion can never
   upgrade this」。第一版用 direct completion 記錄，結果是 REFUSED。
2. **工具計數器讀錯事件型別** — Codex CLI 的事件型別是 `command_execution`，不是 `command`。
   計數為 0 時 admission REFUSED；改成讀真正的型別後才 ADMITTED。
3. **`item.started` 與 `item.completed` 是同一次調用** — 不去重會重複計數。
   修正方式是依 `item.id` 去重。

### 1.3 一個必須揭露的技術事實

`gpt-6.1-sol` 在 relay 的 `/v1/models` 目錄中不存在（目錄是過期快照）；
`minimax-m3.1-flash-free` **同樣不在目錄裡**，但**兩者都能服務**。
差別在於傳輸詞彙（transport vocabulary）：

| provider | 必須的 transport id | 原因 |
|---|---|---|
| `openai-codex` | **裸 id**（`gpt-6.1-sol`） | 帶 `openai-codex/` 前綴會被 relay 路由到預設 provider，回 HTTP 400 |
| `opencode-go` | **provider-qualified**（`opencode-go/minimax-m3.1-flash-free`） | 帶前綴才能命中正確 provider |
| `nvidia` | **provider-qualified**（`nvidia/<model>`） | 同上 |

**結論：目錄不是真相，逐字轉送才是。** 本回合三車道用 MiniMax 走的就是
provider-qualified 轉送。

---

## 二、SBL 施工干擾排除

盤點時發現 Fabric 倉庫內有**兩個其他 session 正在寫入**的 SBL 回合目錄
（檔案 mtime 落在 13:36–13:38，即本回合執行期間）：

```
fabric-autonomous-research/runs/FAR-20261021-023-sbl-r7-residual-closure/
fabric-autonomous-research/runs/FAR-20261021-024-fallback-chain-reorder/
```

**本回合對它們的實際動作：零。**
詳見 `SBL-EXCLUSION-NOTE.md`。摘要：

- 本回合所有寫入目標都在 `HG-KSEOS/` 或 `Fabric/EVIDENCE/` 之下；`fabric-autonomous-research/`
  從未被寫入。
- 本回合兩次 Fabric 提交的檔案清單不含 `fabric-autonomous-research` 任何路徑。
- 這兩個 untracked 目錄在回合結束時**仍為 untracked**，留給施工中的 session 自行處置。
  把別人的半成品 stage 進本回合的證據包是污染；刪掉則是破壞。

---

## 三、三個殘留主題的實測基線（FAR 研究的核心產出）

業主引用的數字是**舊快照或估計值**。本回合逐項重測：

| 主題 | 業主引用 | 實測 | 差異原因 |
|---|---:|---:|---|
| OpenSpec 未勾項 | 471 | **460** | 471 是估計值 |
| OpenSpec change 數 | 33 | **34** | 460 筆分佈在 34 個 change 上（研究代理獨立覆核） |
| `var/` 頂層目錄 | 114 | **120**（不含本回合自身輸出目錄）/ 121（含） | 114 是舊快照 |
| TT ledger OPEN | 2 | **2** | 一致 |

> **兩個研究代理的計數差異已釐清**（本回合實測）：
> 38 個 active change 目錄中有 **35 個**含未勾項、合計 **465 項**；
> 其中 **5 項**是本回合自己 change `far-minimax-mandate-20261021` 第 6 節的業主裁決項。
> 因此**排除本回合後 = 34 個 change、460 項**。
> 知識庫比對代理報「35 個 change」（含本回合），OpenSpec 分類代理報「34 個」（排除本回合）——
> 兩者各自正確，差異就是本回合自己那一組。

> **研究代理獨立覆核的三項前提修正**（本回合已採納）：
> 1. **change 數是 38 不是 37** —— 掃描期間本回合新增了 `far-minimax-mandate-20261021`；
>    排除本回合族後，460 筆分佈在 **34** 個 change 上（非業主引用的 33）。
> 2. **36/37 個 change 目錄在 git 中是 untracked** —— `git ls-files openspec/changes` 只回 3 個檔。
>    因此 **git log 對這批檔案本來就不是有效佐證**；先前引用 git log 交叉驗證的方法在此樹上不可用。
>    必須改用 `var/`、`_handover/`、Fabric/PIPD 分支的實體證據交叉驗證。
> 3. **可機械回填只有 109 筆（23.7%），不是先前假設的 440** —— R10 逐列裁決的 36 列中
>    只有 24 列 `DONE_MEASURED`（66.7%）。440 這個預設值過度樂觀。

### 3.1 OpenSpec 未勾項：460（不是 471）

- active changes：**38**（含本回合自身）
- 有未勾項的 change：**34**
- 未勾項總數：**460**
- 本回合自身 change（`far-lane-remediation-20261021`）之外的 change：**34** 個，
  合計 **460** 個未勾項

產出：`openspec_unchecked_index.json` / `OPENSPEC-UNCHECKED-INDEX.md`
（逐 change 列出未勾項全文、已勾數、自身產物檔數、名稱是否出現在 git log）。
**本回合套用的 tick 數：0。**

### 3.2 `var/` 目錄：120（不是 114），且**不是 120 個未結案回合**

這是本回合最重要的一個否定性發現。`var/` 下的目錄**不等於**未結案的回合：

| 類別 | 數量 | 意義 |
|---|---:|---|
| `ROUND_ARTIFACT` | 75 | 回合產物，但沒有可連結的 openspec change |
| `ROUND_OPEN` | 8 | 回合產物，且其連結的 change 仍有未勾項 |
| `RUNTIME_OR_CACHE` | 3 | runtime / cache / DB / 備份 —— **從來不是回合** |
| `EMPTY` | 2 | 空目錄 |
| `UNCLASSIFIED` | 32 | 需業主裁決 |

**「114 個目錄待結案」這個分母本身是錯的。** 真正的回合產物是 83 個（75+8），
其中可機械對帳的只有 8 個。

產出：`var_disposition_index.json` / `VAR-DISPOSITION-INDEX.md`
（逐目錄列出檔案數、不可讀子樹數、標記檔、連結的 change、類別、建議動作）。
**本回合執行的破壞性動作：0**（未刪除、未搬移、未改名）。

### 3.3 TT ledger OPEN：2 個（實測 `status == "OPEN"`）

`source-freeze/TT_LEDGER.csv` 共 11 筆資料列。狀態分佈中 `status` 嚴格等於 `OPEN` 的
**恰好 2 筆**：`HGK-EBC-TT-001`、`HGK-EBC-TT-002`。
（第三筆 `TT-HLPE-SRU-DRIFT` 的狀態是 `OPEN_NONBLOCKING_FOR_HLPE_BIND`，
是**不同的狀態值**，不是 `OPEN`。）

---

## 四、FAR 裁決建議（待業主確認）

### 裁決 A：OpenSpec 460 個未勾項

**建議分類處置**（研究代理的實測分組）：

| 類別 | change 數 | 未勾筆數 | 建議動作 | 阻力 | 風險 |
|---|---:|---:|---|---|---|
| (a) 已完成未回填 tick | 16 | 185 | **條件式回填**：僅在「該 item 的實作可逐筆交叉驗證」時回填，且每筆內嵌證據定位 | 低 | 低 |
| (b) 被其他 change 取代 | 2 | 32 | **標 disposition，不打勾**（打勾是錯的狀態） | 低 | 低 |
| (c) 需真實工程工作 | 5 | 75 | 開新 change 承接，不在舊 change 內回填 | 中 | 低 |
| (d) 需業主決策 | 5 | 69 | 進 OWNER 佇列 | 低 | 低 |
| (e) 已失效／過時 | 4 | 99 | 標 disposition: HISTORICAL / SUPERSEDED | 低 | 低 |
| (a+b 混合) | 2 | — | 逐列判斷歸入 a 或 b | 中 | 低 |
| **合計** | **34** | **460** | | | |

**裁決 A1（建議，且已按研究代理的覆核修正數字）**：
可機械回填的是 **109 筆（23.7%）**，不是先前估的 19 筆。拆成四個可執行的子動作：

| 子動作 | 筆數 | 來源 | 可重現性 |
|---|---:|---|---|
| A1-R10 | 20 | R10 `adjudication.tsv` 中 `verdict == DONE_MEASURED` 的列 | 逐列證據定位為檔案路徑+sha256前綴+實測命令，可機械重跑 |
| A1-EXIST | 13 | 純機械存在性比對（PIPD 分支的 `git show <branch>:<path>` + 固定字串斷言） | 完全確定性 |
| A1-EVID | 3 | 證據存在即回填（`VERDICT_LANE_VERBATIM.txt` 等） | 存在性斷言 |
| A1-TOTAL | **109** | | 460 → 351 |

其餘 **351 筆**（76.3%）**必須逐項人工判斷或以 disposition 處理**，不得批次操作。

**裁決 A2（建議）**：約 **120 筆**標 disposition（`NOT_OWED` / `SUPERSEDED` / `OWNER_BLOCKED` /
`HISTORICAL`），**不是打勾**。理由：打勾宣稱「工作完成」，而 disposition 記錄「工作被別人做了
或不需要做」。兩者語意不同。
**前置條件**：必須先把 disposition 語彙寫進 `AGENTS.md` 的約定，否則下一輪又會把它們讀成「未完成」。

**裁決 A3（建議）**：約 231 筆屬「需真實工程工作 + 業主決策 + 歷史記錄」——**不建議本回合關閉**。
把它們標成「已結案」是治理上的造假。

**裁決 A4（建議，低阻力且有先例）**：**0 個 change 建議刪除**。最小破壞路徑是 **archive** 而非刪除
（`openspec/changes/archive/` 已有 1 個先例）。有 5 個 change 建議 `openspec archive --skip-specs`：
`hermes-incident-2026-10-05-repair`、`lane-sod-enforcement`、`lane-verify-dual-routing-and-plan-high`、
`lane-verify-routing-remediation`、`hgk-cnv-evidence-archive-r7r11-20261016`。
另有 3 組建議**合併**（見研究報告 §6.2），4 個 PIPD change 建議合併為 2 個新記錄。

### 裁決 B：`var/` 120 個目錄

**建議 B1（強烈建議）**：**不刪除任何目錄。**
理由（三條，同時成立）：
1. 其他 session（SBL）正在同一個 `var/` 根下寫入，刪除會破壞它們的收據；
2. 刪除不可逆；
3. 「低風險」原則要求可逆。
**本回合已實際做到零破壞性動作。**

**建議 B2**：以本回合產生的 `VAR-DISPOSITION-INDEX.md` 作為**處置索引**，
把 120 個目錄分成「回合產物 / runtime-cache / 空 / 未分類」四類。
這一步把不可用的分母（120）變成可用的分類（83 回合產物 / 3 runtime / 2 空 / 32 待裁決）。

**建議 B3**：`RUNTIME_OR_CACHE` 與 `EMPTY` 這 5 個目錄可以刪，但**需業主明確批准**；
它們是唯一「刪除零風險」的子集。

**建議 B4**：`UNCLASSIFIED` 32 個需逐個人工判斷，不建議在本回合處理。

### 裁決 C：TT ledger 2 個 OPEN

研究代理的裁決（經本回合覆核）：

| 項目 | 分類 | 建議 |
|---|---|---|
| `HGK-EBC-TT-001` | **② 需 migration 才能關閉** | 是**未修復的工程缺口**，不是缺證據。需新增 evidence 的 requirement/subject binding、補 typed registration 與 resolver 檢核、處置舊 evidence。**不能只補說明或測試收據。** |
| `HGK-EBC-TT-002` | **③ 需業主決策，且存在具體工程缺口** | acceptance 路徑已修好（revision 3 的 `resolve_acceptance` 同時比對 `entity_type` 與 `entity_id`），但其他 writer 仍可能把 foreign event 誤認為 replay。**不能把整筆當成「帳本漏回填」。** 建議保留全域 UNIQUE，不先改 namespace；明定跨 entity 拒絕契約並補齊 writer。 |

**裁決 C1（建議）**：TT-002 的 **acceptance 子範圍**可以立即整理為已完成的證據
（它有 revision 3 的實作），但**整筆 ledger 狀態維持 OPEN**，直到 general contract 裁定完成。
理由：把部分修復擴張成整筆關閉，是本回合明確拒絕的行為。

**裁決 C2（建議）**：TT-001 進入獨立 change（需 schema/資料相容性變更），
**不列入本回合收尾**。

### 裁決 D：模型軸獨立性（必須讓業主知情）

業主的新模型方案讓 **PLAN、EXECUTE、VERIFY_SECURITY 三車道全部是同一個模型**
（`opencode-go/minimax-m3.1-flash-free`）。這意味著：

- **模型軸獨立性 = 0**。三車道同模型。
- 依 HGK 的 SoD 規則，這必須**明確宣告**，不能含糊帶過。
- 本回合已宣告為 `SOD006-C5`（`OPEN_OWNER_ORDERED`），並把
  `sod_invariants.pairs` 中 `EXECUTE->VERIFY_SECURITY` 的 `distinct_required` 由 `true`
  改為 `false`，**同時記錄了原因**（不是無聲翻轉旗標）。
- 剩下的分離只有：PROCESS（獨立 Codex-CLI 程序）、LANE（角色不同）、
  EVIDENCE-PATH（checker 從工件重新推導，不讀 writer 的摘要）、
  以及 no-self-acceptance 規則。
- **相關盲點（correlated blind spots）不被主張為不存在。**

**裁決 D1（建議，給業主）**：若未來要把模型軸分離恢復，
最省阻力的做法是保留 MiniMax 為三車道 rank-1，**同時**把 `gpt-6.1-sol`
留在 VERIFY_SECURITY 的 operator-selectable 臂（它已在池中，rank 2）——
如此 checker 可在配額恢復後切換，而不需要再做一次池重綁。
**本回合已把 MiniMax 之外的臂全部保留為 fallback，沒有刪除任何臂。**

### 裁決 E：delegation 平面

業主的模型方案是針對**三個治理車道**。delegation（子代理）平面是**另一個平面**，
本回合事實上**也**把它切到 MiniMax，原因是 `gpt-6.1-sol` 配額耗盡
（HTTP 429，約 2 小時後重置），不切則研究任務無法執行。
依 Hermes 的程序：設定 `delegation.provider`+`model` → 派發 → **立即還原** →
從 `state.db` 確認 pin 生效（`sessions.model = minimax-m3.1-flash-free`）。

**裁決 E1（建議）**：把 delegation 平面**常態化**為 MiniMax，直到業主另行指示。
理由：業主已把 MiniMax 定為三車道模型，delegation 與車道同源可減少行為差異；
且 gpt-6.1-sol 配額是實際的運行約束。**需業主確認**——本回合只做了臨時 pin 並已還原。

---

## 四之三、知識庫比對的一致性檢核（`知識庫\實作相關DOC`，7,322 檔）

兩個研究代理之一專門比對了 `C:/Projects/Agent_Workspace/知識庫/實作相關DOC`（唯讀，7,322 檔）。
它的定位是**為裁決找出知識庫的既存依據與先例**，不是重新提出裁決。

| 主題 | 本裁決 | 知識庫既有裁準 | 一致？ |
|---|---|---|---|
| 1（460 項） | A1 只回填可交叉驗證項且逐項附證據、不接受批次回填；A2 superseded 標 disposition 不打勾；A3 其餘不建議關閉 | A10（superseded 不 tick + 負測）、A8（逐項 GO/HOLD + 保留限制聲明）、B3（APPARENT_PASS 反例）、B2（未勾即封頂） | **完全一致**——知識庫已有全部依據 |
| 2（`var/`） | B1 不刪除任何目錄；B2 以索引作處置投影；B3 僅 5 個 runtime/empty 需業主批准；B4 32 個 UNCLASSIFIED 逐個人工 | B5（不准壓平 raw evidence、archive+manifest+readback）、B6（cleanup 八條件）、B3（Residue exact-set 七欄位）、A2（receipt 存在≠完整） | **一致，但知識庫有實質缺口**——沒有 HG-KSEOS `var/` 專屬方法論 |
| 3（TT 2 筆） | C1 TT-002 acceptance 子範圍可整理為已完成證據但整筆維持 OPEN；C2 TT-001 進獨立 change | A1（TT-001 原文即「schema extension 超出本 ChangeSet 範圍」；TT-002 原文即「resolved on acceptance path, retained as general contract note」）、A7（既有 reconcile 程序）、B2（部分修復不擴張） | **完全一致**——C1/C2 幾乎是 A1 原文的結構化重述 |

### 知識庫比對帶出的四項執行建議（本回合已採納或列入裁決）

1. **優先複用 A8 + A9 作為 460 項裁決的敘事骨架**：未完成項不阻擋本回合收尾，但必須保留限制聲明並
   明列 claim ceiling；被取代項標 disposition 而非 tick。→ 已寫入裁決 A1/A2。
2. **主題 3 可立即執行**（無需業主裁決的部分）：A7 顯示 `scripts/reconcile-tt.ps1` 已存在，
   TT ledger 狀態變更不需要新機制。→ 併入裁決 C1，業主確認後即可執行，**不需新造工具**。
3. **主題 2 需要先補一份裁準**（知識庫缺口）：在刪除任何 `var/` 目錄前，先依 B3 的 Residue
   exact-set 七欄位 + B6 的八項 closure 條件建立「HG-KSEOS `var/` 產物分類與保留政策」。
   → **這是裁決 B 的前置條件**，已寫入裁決 B1。
4. **不要**把 B1 的 PIPD lifecycle state 灌入 HG-KSEOS：只用其詞彙表做 460 項的**注記欄位**，
   狀態機仍走 HG-KSEOS 自己的等價物。→ 已寫入裁決 A2。

### 明確的不可套用判定（研究代理的界線聲明）

- 知識庫中約 9.5MB 的逐字稿日誌（`Fabric vNext/.../驗收_紀錄_vol-01..10.md`）**僅可作事實佐證，
  不可作裁準引用**。
- 知識庫中**一個受環境保護的子目錄未被檢查**（需明確授權才能讀），本裁決未引用其中任何內容。
- 本裁決未引用任何未經比對的裁準。

---

## 四之四、研究代理揭露的四個阻塞項（會改變裁決的執行順序）

這些不是研究結論，是**執行前提**。它們由研究代理獨立實測得出，本回合採納。

### 阻塞 1：36/37 個 change 目錄未受 git 追蹤

`git ls-files openspec/changes` 只回 3 個檔（`far-lane-remediation-20261021/`）。
其餘 36 個目錄為 untracked。

**對裁決的影響**：
- 所有回填都**不會有 git 歷史**，因此每列**必須內嵌證據定位**（否則下一輪又會變成一批
  「已完成未回填」——這正是本回合要關的問題）。
- **建議裁決 A0**：先把 34 個 change 目錄納管（`git add openspec/changes`），
  否則裁決 A1 的所有回填都不可稽核。**低阻力、零判斷風險，應先做。**

### 阻塞 2：現況測試套件紅燈 → 有些列**不能**回填

任何以「測試綠」為驗收條件的列（`strict-declaration-20261011` 3.x、
`lane-sod-enforcement` 2.3/2.4、`lane-health-repair-20261011` 6.1–6.4）
在測試不綠時**不得回填 tick**。研究代理的實測：`20 failed, 134 passed`（三個相關檔案）。

本回合已針對此做「自修補」（見 §四之三）。

### 阻塞 3：epoch 25 的三車道同模型 → 要求「checker ≠ writer」的列**無法**完成

`strict-declaration` 4.2、`hgk-far-019` 4.1、`pipd-r17` 3.1、`hgk-r8` 4.x
這些列要求模型軸獨立性。在業主的三車道同模型命令下**無法取得**。
**只能標 disposition `OWNER_ORDERED_NO_MODEL_AXIS_INDEPENDENCE`，不能標完成。**
這是裁決 D 的直接後果，必須讓業主知情。

### 阻塞 4：Fabric 的 merge commit 只在分支上，不在 `main`

三個 merge commit（`6c25bbe`/`603cb0c`/`bcd9104`）只存在於
`pub/far-lane-remediation-20261021`，**不在 `main`**（`merge-base --is-ancestor` = False）。
本地能驗到 merge 事件，但「published to the target repo and promoted out of draft」
**需要 GitHub live API 確認**。因此該列保留為人工對帳。

---

## 四之五、本回合的自修補（測試 oracle 對齊 epoch 25）

研究代理實測發現：epoch 25 的綁定使**測試 oracle 過期**——
`tests/test_lane_policy.py` 的 `owner_chain` 仍寫 epoch 23 的 `gpt-6.1-sol`，
且 `tests/test_lane_dispatch_ao_guard.py` 的 stub usage row 硬編 `deepseek-v4.1-flash`，
而 dispatcher 現在服務 MiniMax → `usage model mismatch`。

**這是本回合造成的真實回歸**（5 個新失敗），已自修補：

| 修補 | 內容 | 理由 |
|---|---|---|
| `config/lane-routing-registry.yaml` | **新增 `apply_registry_route_sync.py`**：從 canonical pool 重建 registry 的 `routes[].fallbacks[]`、`arms[]`、`canonical_identity`、`selected_arm_identity`、`admission_status`、`admission_evidence`（15 處修正） | **這是本回合最嚴重的缺陷**：`check_drift` 只比對「registry 的 projections vs 現場」，**不檢查 registry 自身內部一致性**，所以 registry 可以在 pool 與 assignment 都已是 MiniMax 的情況下，仍對外宣告 `gpt-6.1-sol` 與 `deepseek-v4.1-flash` 而 drift 仍回 `[]` |
| `tests/test_lane_policy.py` | `owner_chain` 更新為 epoch 25 的 MiniMax 綁定 | 這是「業主命令的 oracle」，它存在的目的就是隨業主命令更新 |
| `tests/fixtures/stub_lane_child.py` | usage row 的 provider/model 改為**從 dispatcher 傳給 child 的 `--model` 推導**；provider/model 切分只切第一段，保留 provider-qualified model（如 `nvidia/deepseek-ai/deepseek-v4.1-flash`） | **根治**：stub 不再需要知道 pool 是誰。被派發的臂就是被回報的臂，因此**任何未來的 pool 重綁都不會打斷這些測試** |
| `tests/test_lane_dispatch_ao_guard.py` | `_text_stub` 同上改為讀 argv；`_stub_env` 預設還原為 hermetic fixture 臂 | 同上 |
| `tests/test_lane_dispatch_ao_guard.py` | C1 與 I3 的斷言改為**從 pool 推導**而非硬編模型 | 同上 |

### 本回合的最終測量（隔離 detached worktree，live 工作樹全程未被修改）

| 腿 | 結果 |
|---|---|
| **BEFORE**（本回合前的 config + 已提交的測試） | `8 failed, 436 passed, 90 subtests passed` |
| **AFTER**（epoch 25 config + 修補後的測試） | `8 failed, 436 passed, 90 subtests passed` |
| **本回合引入的新失敗** | **0** |
| **本回合修好的失敗** | 0（原本就沒有由本回合造成的既有失敗） |

剩餘的 8 個失敗**全部在本回合之前就存在**，且與本回合無關：
`test_task013_hermes_v020_closure`、`test_task014_named_method_closure`、
`test_task015_coherence_closure`（前一 session 的 task-014 系列）、
`test_hlpe`（2 個）、`test_c2_case_run`（1 個）。
**它們不是本回合造成的，本回合也沒有越權去修它們**（那屬於另一個 session 的工作範圍）。

> 比對基礎的一個必要修正：`tests/fixtures/stub_lane_child.py` 被 17 個測試引用，但整個
> `tests/fixtures/` 目錄**未被 git 追蹤**。在 detached worktree 裡它不存在，導致兩條腿都失敗
> 那 17 個測試，比對的絕對數字完全失真。修正方式是**把這個 fixture 帶進兩條腿**（它是測試依賴，
> 不是被比較的 config），並且**把它納入版控**（5.3）。

**修補的原則（這是本回合學到最重要的工程教訓）**：
測試不該因為 pool 換了模型就壞掉——它們測的是 nonce 邏輯、usage receipt 形狀、carrier 形狀，
不是「現在的 rank-1 是誰」。第一版修補把「模型」從 canonical pool 推導（仍是一個隱含耦合），
第二版才找到正解：**讓 stub 從 dispatcher 實際傳給它的參數推導**。
這把「測試知道 pool 是誰」變成「被派發的臂就是被回報的臂」，耦合消失。

**同時揭露的治理缺口**：`check_drift` 不覆蓋 registry 自身的跨欄位一致性。
這意味著**任何未來的 pool 重綁都可能留下過時的 registry 宣告而 drift 仍為零**。
`apply_registry_route_sync.py` 補上了這個缺口，但**尚未接入 `check_drift`**——
接上是建議的後續工作，不在本回合範圍內。

---

## 五、本回合已執行 vs 未執行（自揭露）

### 已執行
- MiniMax 三車道可行性實測 + HGK admission（三車道 ADMITTED）
- epoch 25 綁定：pool（rank 1 + 連續 rank + 保留所有舊臂）、registry（route / chain /
  projection / SOD006-C5）、assignment（chain / rows / supply_selector / sod）
- drift gate：**0**
- `var/` 處置索引（120 目錄，0 破壞性動作）
- OpenSpec 未勾項索引（460，0 tick）
- SBL 干擾排除記錄
- 獨立 AO 驗收（MiniMax VERIFY 車道）
- 兩個研究子代理（MiniMax）+ 知識庫比對代理（MiniMax）

### 未執行（需業主裁決或超出本回合範圍）
- 460 個未勾項中的任何打勾
- `var/` 任何目錄的刪除
- TT ledger 任何一筆的狀態變更
- 33 個 change 的合併/刪除/archived
- delegation 平面的常態化

### 已知未關閉（與本回合改動無關的既有缺陷）
- 死 pin `9614f1d9b40d9c4f/codex.exe` 造成的 `ERR_LANE_TOOLCHAIN_BINARY_MISSING`，
  影響多個既有測試（實測 baseline 就有 16 個 failed）
- 300+ 未追蹤候選（`var/` 與其他目錄）
- 已提交的 `config/hermes.json` 過時（指 `var/hermes-v020` 隔離 home），
  正確版只存在於未提交工作樹
- 上一回合 33 個 change / 471 個未勾項等歷史分母未更新
