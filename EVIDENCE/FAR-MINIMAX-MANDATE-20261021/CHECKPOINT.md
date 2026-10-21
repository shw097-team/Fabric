# CHECKPOINT — FAR-MINIMAX-MANDATE-20261021

**建立時間**：2026-10-21 16:0x（台北時間）
**建立者**：本 session（HG-KSEOS 控制平面 / Fabric 證據發布）
**狀態**：**已暫停，等待業主開機後續行。**
**目的**：讓任何人（或未來的我）在不重讀 465 則對話的情況下，能精確接續。

---

## 0. 一句話現況

本回合已完成 **模型方案可行性證明**、**三車道 MiniMax 綁定**、**4 個治理缺陷的修補**、
**FAR 裁決報告（含實測索引）**、**Fabric 證據包發布（遠端 67/67 驗證通過）**；
**尚缺**一張**獨立 AO 簽署的 verdict** 與**業主對兩項裁決的確認**。

**但有一個狀況改變了整件事的前提**：另一個 session 依**更新的業主命令**
（`OWNER-ORDER-20261021-GPT-QUOTA-RESTORED`，記為「GPT 配額已恢復」）已把 lane pool
重綁回 GPT 並 **commit**（`f4a2ec4`、`bf209cf`）。**本回合的 MiniMax 指示已不是現況。**

---

## 1. 開機後第一件事：先確認現況（不要假設）

開機後執行以下三條，**先看清楚再動作**：

```bash
cd C:/Projects/Agent_Workspace/HG-KSEOS
git log --oneline -5
git status --short
./.venv/Scripts/python.exe -c "import json;d=json.load(open('config/lane-route-slots.candidate.json',encoding='utf-8'));print(json.dumps(d,ensure_ascii=False)[:800])"
```

**必須回答的問題**：業主在關機前後，是否下過新的命令？
本 checkpoint 建立時，MiniMax 指示與 GPT 重綁指示**同時存在**且互相衝突。
**在確認之前，不要做任何綁定寫入。**

---

## 2. 本回合的產出（已落地，勿重做）

### 2.1 HG-KSEOS commits

| commit | 內容 |
|---|---|
| `a1bd583` | 三車道綁定 MiniMax（epoch 25）、pool/registry/assignment、SoD SOD006-C5、AGENTS、測試修補、`tests/fixtures/` 納版控、OpenSpec change |
| `1cbb9d2` | registry route-level `auth`/`oauth`/`reasoning_effort` 同步（AO 找到的第二層缺陷） |
| `f4a2ec4` | **另一個 session**：GPT 6.1 SOL 還原 PLAN + VERIFY/SECURITY，EXECUTE 留 DeepSeek V4.1 Flash |
| `bf209cf` | **另一個 session**：pool 的 identity-overlap record 改為由 pool 推導 |

**本回合自己的 commit 只有 `a1bd583` 與 `1cbb9d2`。** 後兩個屬另一個 session，未被本回合改寫。

### 2.2 本回合產出的檔案（`var/FAR-MINIMAX-MANDATE-20261021/`，該目錄被 gitignore）

| 檔案 | 內容 |
|---|---|
| `FAR-RULING-REPORT.md` | **FAR 裁決報告（交付物）**——五項裁決 A/B/C/D/E，含知識庫交叉比對三項可複用發現 |
| `OPENSPEC-UNCHECKED-INDEX.md` + `openspec_unchecked_index.json` | 460 個未勾項逐 change 索引，含 `[~]` 具名殘留的區分說明。**套用 tick 數 = 0** |
| `VAR-DISPOSITION-INDEX.md` + `var_disposition_index.json` | 120 個 var/ 目錄七類分類。**破壞性動作 = 0** |
| `research/OPENSPEC-CLASSIFICATION.md` | OpenSpec 研究（26.8 KB） |
| `research/KNOWLEDGE-BASE-CROSSCHECK.md` | 知識庫比對（32 KB，12 A 類 + 12 B 類 + 三張判定表） |
| `SELF-REVIEW.md` | 自我研究：本回合缺陷的發現路徑分析 |
| `CONCURRENT-OWNER-ORDER-CONFLICT.md` | **並行命令衝突事實記錄（119 行）**——裁決權在業主 |
| `AO_FINAL2_PROMPT.md` | AO2 brief（已執行，未取回簽署 verdict） |
| `admission/` | 三車道 HGK admission receipts（皆 ADMITTED） |
| `probes/` | transport probe 收據、AO1/AO2 stdout（AO1 230 KB、AO2 320 KB） |
| `apply_minimax_binding.py`、`apply_assignment_derivation.py`、`apply_registry_route_sync.py` | 三個套用腳本（冪等） |
| `compare_pytest_isolated.py`、`pytest_diff.json` | 隔離 baseline 比較器與結果 |

### 2.3 Fabric 證據包（已發布並遠端驗證）

- **分支**：`pub/far-minimax-mandate-20261021`（基於 `origin/main` `bcd9104`）
- **遠端 HEAD**：`53ec0de`
- **commits**：`79f8278` → `db26179` → `077d1d5` → `53ec0de`
- **遠端驗證**：67/67 digest 相符、0 缺失、0 不符、0 機密
- **路徑**：`EVIDENCE/FAR-MINIMAX-MANDATE-20261021/`
- **注意**：Fabric repo 工作樹有**另一個 session 的 staged SBL 檔案**（`fabric-autonomous-research/runs/FAR-20261021-023-sbl-r7-residual-closure/**`）——**不要 `git add .`，不要動它們**。

### 2.4 已更新的治理記錄

- **KANBAN** board `far-minimax-mandate-20261021`：33 張卡（26 done、7 blocked）
  - DB：`%LOCALAPPDATA%\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\kanban\boards\far-minimax-mandate-20261021\kanban.db`
  - **Hermes KANBAN CLI 不可用**（schema `no such column: task_id`）→ 用 direct SQLite
  - **WAL 模式**：寫入時可能 `database is locked`（其他 session 同時寫）。用 `BEGIN IMMEDIATE` + 重試；失敗時**務必 close 連線**否則會鎖住後續寫入
- **OpenSpec** change `far-minimax-mandate-20261021/`（strict validation 通過）
- **Skill** `hgk-lane-rebinding-traps`（4 個 trap + 知識庫複用紀律 + `[~]` 區分教訓）

---

## 3. 未完的工作（精確清單）

### P0 — 業主裁決（**不可自行決定**）

**裁決 ①：並行業主命令衝突**

| 車道 | 本回合 epoch 25 | 另一個 session 的 epoch 26（已 commit） |
|---|---|---|
| PLAN | `opencode-go/minimax-m3.1-flash-free` | `openai-codex/gpt-6.1-sol` |
| EXECUTE | `opencode-go/minimax-m3.1-flash-free` | `opencode-go/deepseek-v4.1-flash` |
| VERIFY_SECURITY | `opencode-go/minimax-m3.1-flash-free` | `openai-codex/gpt-6.1-sol` |

選項：(A) MiniMax 指示有效 → 修掉 `declared_by` 矛盾並重綁；(B) GPT 重綁有效 → 本回合 commit 保留為歷史證據；(C) 兩者都要，需業主說明切換條件。

**裁決 ②：FAR 五項裁決確認**（詳見 `FAR-RULING-REPORT.md`）

- **A（OpenSpec 460 項）**：建議只回填 109 筆可交叉驗證者、120 筆標 disposition、231 筆不關閉。**0 tick 已執行，等確認。**
- **B（var/ 120 目錄）**：建議**不刪除任何目錄**。
- **C（TT 2 筆 OPEN）**：TT-002 維持 OPEN、TT-001 進獨立 change。**已驗證 `scripts/reconcile-tt.ps1` 存在，執行不需新機制。**
- **D（模型軸獨立性）**：三車道同模型 → SoD 衝突明示。
- **E（delegation plane）**：delegation 與 lane 是不同平面。

### P1 — AO 簽署 verdict（本回合唯一實質缺口）

**現況**：AO1（540s）與 AO2（900s）都完成了實質檢查，但**都沒能寫出 verdict 檔**。
**原因**：VERIFY_SECURITY 車道預設 `read-only` 沙箱 + 非變異守衛，而 verdict 目標在受治理樹內
→ 全部寫入被拒（`NEWFILE FAIL [Errno 13] Permission denied`、`MKDIR FAIL [WinError 5]`），
run 浪費整個 budget 在診斷沙箱。

**已驗證的修法**：給 AO 一個可寫的 `--lane-scratch` 路徑，AO 寫到 scratch，
由 orchestrator 搬進證據包。**受治理樹對 checker 保持唯讀是正確的，不要放寬沙箱。**

**已備妥**：`AO_FINAL2_PROMPT.md`（138 行）、可寫 scratch `%LOCALAPPDATA%\Temp\hgk-ao-final3`。
**AO2 已完成的檢查**（checks 1–11）已從其 command outputs 逐條轉錄到
`AO2_findings_transcribed.json`——**但轉錄不等於簽署的 verdict**。

**重跑指令形狀**（待 pool 穩定、業主裁決 ① 後）：
```
cd C:/Projects/Agent_Workspace/HG-KSEOS
./.venv/Scripts/python.exe scripts/hgk-lane-dispatch.py \
  --lane VERIFY_SECURITY --require-arm <現行 rank-1 arm> --force-rank 1 \
  --sandbox workspace-write --allow-sandbox-escalation \
  --lane-scratch "C:/Users/user/AppData/Local/Temp/hgk-ao-final3" \
  --codex-executable "C:/Users/user/AppData/Local/OpenAI/Codex/bin/896a0166b774037a/codex.exe" \
  ...
```
**注意**：`--require-arm` 必須改成**現行**的 rank-1，否則立即 `ERR_LANE_REQUIRED_ARM_ABSENT`。

### P2 — 已知未關的技術債

| 項目 | 狀態 |
|---|---|
| 8 個既有全庫測試失敗 | 本回合新增 0（隔離比較 BEFORE=AFTER=8 failed/436 passed/90 subtests）。屬 task-013/014/015 與 hlpe，**另一個 session 範圍，未越權修** |
| `selected_arm`/`selected_arm_identity` 缺於 PLAN 與 EXECUTE route rows | 繼承自 epoch 24。修法：讓 route sync 對所有車道寫這兩個欄位。**在 pool 被重綁時不要寫，會撞** |
| committed `config/hermes.json` 過時 | dirty 正確版與 task-014 工作耦合、含已知有問題的 `hermes.exe` trampoline，**未驗證可提交** |
| relay/local `/models` 不列 MiniMax | 實際可服務但 catalog 過期。狀態只能維持 PARTIAL |
| Windows path length | fresh clone 有 `Filename too long` 限制。可由 Git object DB 重算，但完整 checkout UX 未關 |
| 8 個既存測試失敗之外的 `1cbb9d2` 後全庫 baseline | `1cbb9d2` 後尚未重跑完整 8-failure baseline（`a1bd583` 時跑過） |

---

## 4. 開機後的建議執行順序

1. **讀第 1 節的三條命令，確認現況**（尤其：業主有沒有下新命令）
2. **向業主取得裁決 ①**（哪個命令有效）——這決定後續所有事
3. **取得裁決 ②**（FAR 五項）→ 若確認，執行：
   - A：只 tick 那 109 筆可交叉驗證者，其餘標 disposition
   - B：不刪目錄，只更新 index
   - C：用既有 `reconcile-tt` 程序（**不需新機制**）
4. **裁決 ① 定了之後，重跑 AO 取得簽署 verdict**（P1）
5. **把 AO verdict + 裁決結果 + 最終 FAR report 納入 Fabric 證據包**，刷新 manifest、secret scan、遠端 digest 驗證、乾淨 commit
6. **更新本 checkpoint** 為完成狀態

---

## 5. 絕對不要做的事

- **不要 `git add .`**（會掃入其他 session 的 `fabric-autonomous-research/runs/**`）
- **不要 force-push**；**不要改寫** `pub/far-lane-remediation-20261021`（含 SBL 內容）
- **不要撤銷**另一個 session 的 `f4a2ec4` / `bf209cf` 或其 staged SBL 檔案
- **不要**在裁決 ① 未定前做任何 lane 綁定寫入
- **不要**把 MiniMax 的歷史 commit 說成現行契約（證據包已明確標為「歷史」）
- **不要**在未取得裁決 ② 前 tick／刪除／關閉任何 OpenSpec 項目、`var/` 目錄或 TT ledger
- **不要**用寬泛路徑 stage Fabric（用 `git -c core.ignorecase=false add -A -- "EVIDENCE/<dir>"`）

---

## 6. 關鍵數字（實測，非引用）

| 項目 | 值 |
|---|---|
| OpenSpec active changes | 38（35 含未勾） |
| 未勾項總數 | 465 筆 `[ ]`（含本回合自己的 5 筆） |
| **其他 change 的未勾項** | **460**（34 個 change）← 業主引用的 471 是舊值 |
| `[~]` 具名殘留 | 1（`s4-final-pr18-closeout-20261016` 5.1，**不計入 460**） |
| `var/` 頂層目錄 | 121（含本回合目錄）→ 歷史候選 **120** |
| TT ledger OPEN | 恰 2（`HGK-EBC-TT-001`、`HGK-EBC-TT-002`） |
| 知識庫檔案數 | 7,322 |
| 全庫測試 BEFORE / AFTER | 8 failed, 436 passed, 90 subtests / 同（新增失敗 0） |
| Targeted suites | 141 passed, 0 failed |
| Fabric 遠端驗證 | 67/67 digest 相符、0 機密 |
| 三車道 MiniMax admission | 皆 ADMITTED（`required_arm == served_arm`） |

---

## 7. 環境速查

- **HG-KSEOS**：`C:/Projects/Agent_Workspace/HG-KSEOS`（`.venv/Scripts/python.exe`）
- **Fabric**：`C:/Projects/Agent_Workspace/Fabric`
- **知識庫**：`C:/Projects/Agent_Workspace/知識庫/實作相關DOC`
- **Canonical Hermes**：`%LOCALAPPDATA%\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\config.yaml`
- **Codex CLI**：`C:/Users/user/AppData/Local/OpenAI/Codex/bin/896a0166b774037a/codex.exe`（**舊路徑 `e78bad…` 已失效**）
- **frontdoor**：`127.0.0.1:10100`／**relay**：`127.0.0.1:10101`
- **governed Codex home**：`%LOCALAPPDATA%\HG-KSEOS\codex-hermes`
- **askpass helper**：`%LOCALAPPDATA%\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\cache\scratch\gh-askpass.cmd`
- **PAT 來源**：`C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt`（**絕不輸出內容**）

---

## 8. 本回合自我研究的一句話

綠燈不等於沒有缺陷：本回合的自檢閘門（drift + targeted suite）全綠，
但**獨立 AO 在提交位元組上**仍找到 registry 的第二份 auth posture 副本——
**因為該缺陷結構上就在閘門的盲區裡**（閘門比對 projection 與現場，不比對 artifact 自身內部）。
同時，兩個研究代理的數字差異（35 vs 34）都是正確的（是否含本回合 change），代理的 `[~]` 宣稱則被我實測推翻並修正。
**下一步的檢測 effort 應放在「閘門看不到的地方」，不是更多同類閘門。**

---

## 9. 非同步研究代理的失敗通知（2026-10-21 16:0x 收到）— **不需補救**

關機前收到 `deleg_dc8b6492` task-0 的失敗通知：`HTTP 429: The usage limit has been reached`。

**這個失敗不影響任何交付物。** 理由（皆已實測驗證）：

| 事實 | 驗證方式 |
|---|---|
| task-0 的實質計數**早已 Recover** | 從 `state.db` 子 session `20261021_142457_de97f0`（175 則訊息）取回，寫成 `research/OPENSPEC-CLASSIFICATION.md`（35,677 bytes、303 行） |
| 該報告**涵蓋全部 34 個 change / 460 筆** | §3.1 分布 16+2+5+5+4+2 = 34 change、185+32+75+69+99 = 460 筆，加總完全吻合 |
| 指定的 10 個 owner-gated／superseded change **全部涵蓋** | `sod-independent-verify-enforcement`、`hgk-r10-session-closure`、`gcm-noninteractive-default-containment`、`hgk-r11-session-handover`、`hgk-round3-lane-rebind`、`lane-mandate-rebinding-and-d01-revocation`、`lane-verify-dual-routing-and-plan-high`、`verification-artifact-contract`、`strict-declaration-20261011`、`hermes-incident-2026-10-05-repair` 皆在報告內 |
| task-1（var/）與 task-2（TT ledger）**已完成** | `research/TASK-1_RESEARCH.md`（7,057 bytes）、`research/TASK-2_RESEARCH.md`（3,646 bytes）皆存在且已納入 Fabric 證據包 |
| 無存活子代理 | `delegate_task list` → 0 live |
| 數字仍與現況一致 | 現況重測：38 active / 35 含未勾 / 465 筆 `[ ]` + 1 筆 `[~]`；排除本回合 = 34 change / **460** |

**開機後不要重跑這三份研究。** 只需要在裁決 ② 獲確認後，
依 `research/` 下的報告執行**已核准的那部分**（目前是 0 tick / 0 刪除 / 0 關閉）。

### 一個值得記下的比對陷阱

我第一次比對「報告涵蓋哪些 change」時用了錯誤的正則（只抓表格首欄），
得出「只有 25 個 change 被覆蓋、460−385 = 75 筆有缺口」的**錯誤結論**。
實際上 `lane-health-repair-20261011`（4 筆）在 §5 阻塞項表內、格式不同所以沒被正則抓到。
**這是「用工具驗證工具產物」時正則本身會出錯的實例**——
差一步就會重跑一份 3 分鐘的研究去補一個不存在的缺口。
