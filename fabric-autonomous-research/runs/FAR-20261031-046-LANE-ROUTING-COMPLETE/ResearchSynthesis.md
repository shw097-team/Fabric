# FAR-046｜三條車道都能跑，所以問題不在車道

日期：2026-11-01（台北）
交付：`FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1`

---

## 0. 兩個假設，都被實測打死

| 假設 | 實測 | 結論 |
|---|---|---|
| 「車道不可用，所以 FAR 只能手寫」 | **PLAN** `gpt-6.1-sol` 65.16 s 服務、nonce 回顯、usage ok；**EXECUTE** `deepseek-v4.1-flash` **14.46 s** 服務、nonce 回顯、usage ok；**VERIFY_SECURITY** `gpt-6.1-sol` 兩次 sitting 皆服務 | **假** |
| 「規則沒寫，所以沒人知道」 | `AGENTS.md` 自 2026-10-30 就有 **"Session plane ≠ lane plane"**，而且點名的歷史失敗就是這一件事 | **假** |

三條車道今天全部量到可服務。**所以「為什麼 FAR 沒有真的跑車道」不是能力問題，也不是知識問題。**

---

## 1. 真正的根因：成本梯度

| 路徑 | 步驟數 | 失敗模式 |
|---|---|---|
| **手寫 synthesis** | **1**（開一個檔案寫） | 無。永遠成功。 |
| **跑三車道** | **3 次派發**，每次自帶 flag | 密封家目錄＋OAuth relay → `ERR_SEALED_HOME_OAUTH_TRANSPORT`；provider 限定 id vs 裸 id → 400；長 brief → `ERR_LANE_ALL_ROUTES_EXHAUSTED`；nonce 沒回顯 → `ERR_NO_ARM_EMITTED_NONCE` |

**手寫是 1 步且零失敗模式；合規是 3 步且至少 4 種具名失敗。** 在任何時間壓力下，便宜的路徑必勝——而便宜路徑產出的散文，**看起來和跑過車道的散文一模一樣**。

這是為什麼加了閘門也沒用：閘門是**事後拒絕**，它不改變事前的成本梯度。而 `AGENTS.md` 的規則之所以能被違反九次，是因為**遵守規則比違反規則貴**。

### 1.1 因果鏈

```
FAR 產物是散文（無來源）
   → 散文沒有內建 provenance，所以「看起來完成」= 檔案存在
   → 完成事件 = 寫檔，不是跑車道
   → 閘門檢查「送來的收據」（round_close_gate 預設空清單）
   → 沒送收據 = 零個拒絕
   → 違規零成本，合規三次派發 + 四種失敗模式
   → 九篇 FAR，零個 PLAN 收據
```

---

## 2. 修補：讓合規路徑變成最便宜的路徑

新增 `scripts/far_round.py`——**一條指令跑完三車道**：

```
python scripts/far_round.py --run FAR-…-NAME --question "…"
```

它依序派 PLAN → EXECUTE → VERIFY_SECURITY，每一條都吃前一條的輸出，並把收據寫在 `far_lane_gate.py` 會看的位置：

```
runs/<run>/PLAN_RECEIPT.json
runs/<run>/EXECUTE_RECEIPT.json
runs/<run>/VERIFY_RECEIPT.json
runs/<run>/lane_output/<lane>.md
runs/<run>/STATE.json
```

**傳輸是 arm provider 的屬性，不是全域旗標**——已寫死在表裡：`openai-codex` 走人類家目錄＋OAuth upstream；`opencode-go` 走 loopback `127.0.0.1:10101/v1`。這是今天兩個 `ERR_SEALED_HOME_OAUTH_TRANSPORT` 的成因。

### 2.1 實測（本輪，逐步）

| 步驟 | 結果 |
|---|---|
| 獨立 EXECUTE 探針（一行問題） | `ok:true`、`deepseek-v4.1-flash`、nonce ✓、**14.46 s** |
| orchestrator PLAN | `ok:true`、`gpt-6.1-sol`、nonce ✓、usage ✓、**65.16 s** |
| orchestrator 首跑 PLAN | `ERR_NO_ARM_EMITTED_NONCE`（brief 沒寫「請回顯 nonce」）→ **已修** |
| orchestrator EXECUTE（短 brief） | `ok:true` 14.46 s |
| orchestrator EXECUTE（吃 PLAN 全文，6000 字） | **`ERR_LANE_ALL_ROUTES_EXHAUSTED`**，212 s，`usage_receipt_ok: false` |

**最後一列是本輪的新發現，也是還沒關的那一格。**

---

## 3. 尚未關閉：長 brief 讓 EXECUTE 的用量對帳失敗

同一個 arm、同一條傳輸：
- 一行問題 → 14.46 s 成功
- 吃 6000 字 PLAN 輸出 → 212 s、`ERR_LANE_ALL_ROUTES_EXHAUSTED`、`usage_receipt_ok: false`

`ERR_LANE_ALL_ROUTES_EXHAUSTED` 的語意是「用量列對不上」，不是「模型沒回答」。**212 秒代表模型跑了**；失敗發生在事後的用量對帳（`usage_rows_after_offset` 對不上）。

**所以這一格的正確描述是：長 brief 讓用量列跨過 offset 邊界，對帳判定失敗。** 不是車道壞了，是**對帳機制對長回合不成立**。

修法（下一步）：
1. 對帳改為「本回合新增的 usage 列」而非「offset 之後的全部」；
2. 或在派發前把 brief 壓到單一工作包大小（`AGENTS.md` 的 "One office per brief" 本來就要求）；
3. orchestrator 預設把 PLAN 輸出裁到 2000 字再餵給 EXECUTE。

---

## 4. 本篇的車道狀態（誠實申報）

| 車道 | 結果 | 收據 |
|---|---|---|
| PLAN | ✅ `gpt-6.1-sol`、nonce ✓、usage ✓、65.16 s | `runs/FAR-…-046/PLAN_RECEIPT.json` |
| EXECUTE | ❌ `ERR_LANE_ALL_ROUTES_EXHAUSTED`（長 brief 用量對帳） | 無 |
| VERIFY_SECURITY | 未達（orchestrator 在 EXECUTE 就停） | 無 |

**本篇 `publication_status: UNPUBLISHED`**，依它自己提出的閘門。

---

## 5. 完整根治方案

| 層 | 措施 | 狀態 |
|---|---|---|
| **成本** | `far_round.py`：一條指令跑三車道，收據自動落盤 | ✅ 已建、PLAN 已驗 |
| **傳輸** | 傳輸寫死為 arm provider 屬性（今天兩個錯誤的成因） | ✅ 已做 |
| **閘門** | `round_close_gate` 從 mandate 推導必要車道（上一輪已做）；`far_lane_gate` 補 EXECUTE | ✅ 已做 |
| **對帳** | 長回合的 usage offset 對帳要改成「本回合新增列」 | ❌ **未做——這是剩下的一格** |
| **發布** | 檔案存在＝候選；發布＝通過三收據的狀態轉移 | ❌ 設計已寫，未實作 |
| **歷史** | 036–045 標 `PROVENANCE_MISSING` | ❌ 未做 |

---

## 6. 教訓

前五輪我把問題歸因於「規則不夠嚴」「閘門不夠多」。**今天量到三條車道都能跑之後，真正的答案浮出來：遵守規則比違反規則貴。**

一條要三次派發、四種具名失敗模式的規則，對上一個「打開檔案就能寫完」的替代品，**閘門再嚴都只是事後罰款**。真正的修法是**把合規做成最短路徑**——一條指令、收據自動落盤、傳輸不用記。

`far_round.py` 就是這個修法。它今天證明了 PLAN 可以 65 秒服務；它同時暴露了下一格：**長 brief 讓用量對帳失敗**。那一格不是車道的極限，是對帳機制對長回合的假設錯了。
