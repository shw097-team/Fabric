# FAR-048｜FAR 本身的全量盤點：20 篇研究，0 篇可發布

日期：2026-11-01（台北）
交付：`FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1`

---

## 0. 一句話的現況

**20 篇 FAR，0 篇 `PUBLISHABLE`。** 只有 045（PLAN）與 046（PLAN + EXECUTE）身上有任何收據。

```
INVALID_RESEARCH  FAR-028 … FAR-044（17 篇）  receipts=[]
INVALID_RESEARCH  FAR-045  receipts=['PLAN']
INVALID_RESEARCH  FAR-046  receipts=['PLAN','EXECUTE']
INVALID_RESEARCH  FAR-047  receipts=[]
────────────────────────────────────────────
total 20 | publishable 0
```

這不是我把標準調嚴。`far_lane_gate.py` 用的是三車道收據，而這 20 篇裡有 17 篇連一張都沒有。

---

## 1. 研究面：做了什麼、證明了什麼

| 篇 | 主題 | 結論是否仍成立 |
|---|---|---|
| 028–035 | console/window、relay、22WP 狀態、ALL-PASS 執行、殘留裁決、反向修正 | 部分被 040 撤回 |
| **036** | 四宿主不共用一個載入表面 | ✅ |
| 037 | 暫停不合規、三個「我以為不行」其實可行 | ✅ |
| 038 | 續行是一台狀態機，不是一句話 | ✅（gate 10/10） |
| **039** | 視窗風暴根因：只藏一層 | ✅ |
| **040** | 撤回「已修好」：修錯站點、量測是瞎的 | ✅（正控打不響 → `PROBE_BLIND`） |
| **041** | 三個「不可能」：D-A 撤回、分母回到 192 | ✅ |
| 042 | 剩三格 | 部分被 043 推翻 |
| **043** | 「結構性事實」被一個檔案推翻 | ✅ |
| **044** | 三個 FAIL 交叉比對：一個是量測抖動 | ✅ |
| **045** | 九篇 FAR，`--lane PLAN` 零次；閘門問錯問題 | ✅ |
| **046** | 三車道全部可服務 → 根因是成本梯度 | ✅ |
| **047** | 成本梯度逐項拆除 + §3 更正 | ✅（§3 已更正） |

**被自己推翻的結論**：D-A（144 分母）、D-I（issuer 壞）、D-J（只能重建發行版）、「結構性事實」×2、Codex×ASSURED 的 FAIL、「模型被切斷」。**七次**。

這個數字本身就是這批研究的價值：**它們不是在報告成功，是在記錄同一個推理錯誤被抓住七次。**

---

## 2. 修補面：實際落地的東西

### 2.1 閘門與工具（全部有測試或實測）

| 檔案 | 作用 | 實測 |
|---|---|---|
| `round_continuation_gate.py` | 續行狀態機，五種具名拒絕 | 10/10 tests、`OK_TO_CLOSE` |
| `work_queue_block.py` | 阻斷必須帶 code+cause+unblock | 無 unblock 即 exit 2 |
| `console_guard_gate.py` | spawn 端 console 隱藏，涵蓋 `profiles/*/scripts` | 33/33 |
| `stall_monitor.py` | 重複計數開時間窗 | `findings: []` |
| `far_lane_gate.py` | FAR 需三車道收據 | 20 篇 → 0 可發布 |
| `round_close_gate.py` | **從 mandate 推導**必要車道 | `NO_LANE_RECEIPT:PLAN/EXECUTE/VERIFY_SECURITY` |
| `far_round.py` | 一條指令跑三車道、收據自動落盤 | PLAN 65.16 s ✅ |
| `review_lock.py` | maker 不得提交查核中的主體 | 實測攔阻一次 |

### 2.2 產品面（PIPD）

| 檔案 | 作用 | 測試 |
|---|---|---|
| `export_bundle.py` | profile 軸改變 bytes、assurance 下限、非一般檔成員拒絕 | 13/13 |
| `abi.py` | Need/Occupant 每次呼叫解析 | 7/7 |
| `tools/hotswap.py` | swap 由 consumer 觀察 | 5/5 |
| `tests/test_adversarial.py` | 9 個攻擊 | 9/9 |
| `ASSURANCE.json` | 宣告 4 項能力，含 `independent_checker`（非自評） | 有收據 |

### 2.3 產物

```
LITE      16 files  6dadaf36a9ec
STANDARD  56 files  9ef70b690d01
ASSURED   83 files  5624006aa2f7   ← 本輪首次產出
```

---

## 3. 驗收面：FHS 交付的 22 個工作包

```
work_queue: 19 PASS / 3 FAIL / 0 NOT_RUN     scoreboard CONSISTENT
WP-11  9 格 = 6 PASS + 3 loader-capped + 0 FAIL
WP-12  RUNTIME_PATH_UNRESOLVED（gateway HTTP 這一步未做）
WP-20  192 = 18 PASS + 168 NO_HOST_SURFACE + 6 NOT_RUN
```

---

## 4. 三個仍然開著的東西（精確）

| # | 缺口 | 精確描述 | 關閉動作 |
|---|---|---|---|
| **A** | EXECUTE 用量收據 | 內容服務到了（2,408 bytes、nonce 回顯），**只有 `usage_receipt_ok` 拿不到**；212 秒固定、600 秒 timeout 無效 → 傳輸層關閉 | 換能回報用量的傳輸，或工作包縮到 200 秒內完成對帳 |
| **B** | 發布狀態機 | `CANDIDATE → LANES_SERVED → PUBLISHED` 設計已寫，未實作 | 實作後 20 篇才有「候選 vs 已發布」之分 |
| **C** | 036–044 標記 | 仍未標 `PROVENANCE_MISSING` | 一次性批次標記 |

其餘（D-H 輪替、O-1 graft、O-2 ff、F-01、P5C、R-1、視窗正控）在 FAR-044 §4 已列，狀態未變。

---

## 5. 最佳工程裁決（建議）

| # | 裁決 | 理由 | 風險 |
|---|---|---|---|
| **1** | **承認 20 篇 FAR 全部是候選，不是已發布研究** | 這是量測結果，不是評價 | 無 |
| **2** | `far_round.py` 定為 FAR 唯一入口 | 把 3 步 4 失敗壓成 1 步 0 失敗 | 無 |
| **3** | EXECUTE 工作包上限 = 能在 200 秒內完成對帳 | 212 秒三次重現 | 大工作包需拆分 |
| **4** | 發布狀態機先做「狀態」、暫不做「簽章」 | 目前只有一個寫入者，簽章是空轉 | 無 |
| **5** | 036–044 標 `PROVENANCE_MISSING`，內容保留 | 內容有價值，地位不實 | 無 |

---

## 6. 完整可執行方案

```bash
# 1. 一次標記 17 篇無收據的 FAR（保留內容，撤回地位）
python scripts/far_mark.py --runs 028..044 --status PROVENANCE_MISSING

# 2. 發布狀態機
python scripts/far_publish.py --run <id>   # CANDIDATE -> LANES_SERVED -> PUBLISHED

# 3. EXECUTE 用量收據：先用小工作包驗證 200 秒內是否拿得到收據
python scripts/far_round.py --run FAR-…-049 --lanes execute --carry-chars 400

# 4. 通過後才讓 far_round 預設三車道
```

**第 3 步是唯一的未知**：若 200 秒內的小工作包也拿不到用量收據，那問題在傳輸層而不是回合長度，屆時要換 relay 路徑（`--relay-base` 指向 ocx 的另一個 port）。

---

## 7. 這批研究的自評

七次自我推翻、二十篇零可發布、一個失敗碼的名字騙了我三輪。

**如果只看「做了什麼」，這是一份很長的工作記錄。如果看「抓到了什麼」，它抓到的是同一件事的七個變體：**

> 在觀測不足時，默認往「不可能」或「已完成」倒；而兩者都讓下一次的判斷更難。

`far_lane_gate.py` 現在會對這 20 篇全部說 `INVALID_RESEARCH`。**那不是這批研究的失敗，是它第一次被誠實計數。**
