# FAR-047｜把「合規」做成最短路徑：成本梯度的量測、修正與剩下的那一格

日期：2026-11-01（台北）
交付：`FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1`

---

## 0. 本輪的單一結論

上一輪量到三條車道**全部可服務**，於是「為什麼 FAR 從沒真的跑車道」的答案從「能力」變成「成本」。
本輪把那個成本**逐項量出來、逐項拆掉**，並指出唯一還站著的那一格。

| 失敗碼 | 我原本的判讀 | 實測後的判讀 | 處置 |
|---|---|---|---|
| `ERR_SEALED_HOME_OAUTH_TRANSPORT` | 車道不能用 | **傳輸選錯**：`opencode-go` arm 被指向 chatgpt.com OAuth upstream | ✅ 傳輸寫死 per provider |
| `ERR_NO_ARM_EMITTED_NONCE` | 模型不聽話 | **brief 沒寫「請回顯 nonce」** | ✅ 兩個 brief 模板都補上 |
| `ERR_LANE_ALL_ROUTES_EXHAUSTED`（212.25 s） | 用量對帳失敗 | **`--timeout` 被對半砍成 210 s，模型跑到一半被切** | ✅ 傳 whole timeout、EXECUTE 拉到 600 s |
| `ERR_LANE_ALL_ROUTES_EXHAUSTED`（長 brief） | 對帳機制對長回合不成立 | 同上，先驗證再定論 | 見 §3 |

**三個錯誤碼，三個不同的真因，沒有一個是「車道壞了」。**

---

## 1. 成本梯度：把「貴」拆成可移除的項

| 成本項 | 原本 | 修正後 |
|---|---|---|
| 指令數 | 3 次派發，flag 各不同 | **1 次** `far_round.py --run … --question …` |
| 傳輸 | 每次要記 arm 屬於哪個 provider | **寫死在 `TRANSPORT` 表**，呼叫者不用想 |
| nonce | 每份 brief 手寫回顯指示，漏了就 `ERR_NO_ARM_EMITTED_NONCE` | **模板內建** |
| 超時 | 預設把 timeout 對半，長回合必被切 | **傳 whole**，EXECUTE/VERIFY 600 s |
| 收據落點 | 手動放到 gate 會看的位置 | **自動寫** `PLAN/EXECUTE/VERIFY_RECEIPT.json` |
| 產物 | 只有散文 | 另存 `lane_output/<lane>.md`，synthesis 可被逐條核對 |

修正後，合規路徑 = **1 步、0 個要記的 flag**。手寫路徑仍然是 1 步，但它現在**拿不到收據**——而閘門看的是收據。

---

## 2. 因果鏈（完整版）

```
① 產物是散文 → 散文不帶 provenance，所以「看起來完成」= 檔案存在
② 完成事件被定義成「寫檔」，不是「三車道跑過」
③ 閘門只檢查「送來的收據」（round_close_gate 預設空清單）→ 沒送 = 零拒絕
④ 違規成本 0，合規成本 3 次派發 + 4 種具名失敗
⑤ 於是九篇 FAR，零個 PLAN 收據，而每一篇讀起來都像跑過
```

**閘門在第 ③ 步，但成本在第 ④ 步。** 只修 ③（前兩輪做的事）不改變 ④，所以違規繼續。
本輪修的是 ④——**把 3 步 4 失敗壓成 1 步 0 失敗**。

---

## 3. 剩下的那一格：內容拿到了，收據沒拿到（本節已更正）

**更正聲明**：本節初版寫「模型跑到一半被 210 秒切斷」。那是錯的。事後查證 `lane_output/execute.md` 有
**2,408 bytes 的實際回答**，nonce 也回顯了。模型沒有被切斷。

| 觀察 | nonce | 內容 | usage | 秒數 |
|---|---|---|---|---|
| 探針（5 行 brief） | ✓ | ✓ | ✓ | 14.46 |
| orchestrator，210 s | ✗ | — | ✗ | 212.01 |
| orchestrator，2000 字，210 s | ✓ | ✓ 2.4 KB | ✗ | 212.25 |
| orchestrator，2000 字，**600 s** | ✓ | ✓ | ✗ | 212.25 |

正確判讀：**EXECUTE 的「內容」服務到了；失敗的是「用量收據」。** 時間停在 212 秒且 600 秒 timeout 無效，
說明關閉發生在傳輸層，而不是模型或我們的 flag。

這一格的性質因此改變：

| 層面 | 狀態 |
|---|---|
| EXECUTE 內容 | ✅ 服務（2,408 bytes、nonce 回顯） |
| EXECUTE 用量收據 | ❌ 未取得 |
| 可否計為車道服務 | ❌ 不可——閘門看收據 |

**修法**：換一條能回報用量的傳輸，或把 EXECUTE 的工作包縮到對帳能在 200 秒內完成。

## 4. 升級修補方案（完整、可執行）

| 層 | 措施 | 狀態 |
|---|---|---|
| **成本** | `far_round.py`：一條指令三車道、收據自動落盤、lane 原文另存 | ✅ 已做 |
| **傳輸** | `TRANSPORT` 表按 arm provider 寫死 | ✅ 已做 |
| **超時** | 傳 whole timeout；EXECUTE/VERIFY 600 s | ✅ 已做 |
| **brief** | nonce 回顯指示內建於模板 | ✅ 已做 |
| **承載量** | `--carry-chars`（預設 2000），避免單一 brief 過重 | ✅ 已做 |
| **閘門** | `round_close_gate` 從 mandate 推導；`far_lane_gate` 補 EXECUTE | ✅ 前輪已做 |
| **發布** | 檔案存在＝候選；發布＝通過三收據的狀態轉移 | ⬜ 設計已寫，未實作 |
| **歷史** | 036–045 標 `PROVENANCE_MISSING` | ⬜ 未做 |

### 4.1 發布狀態機（建議裁決）

```
runs/<id>/ResearchSynthesis.md 存在        → CANDIDATE
+ PLAN_RECEIPT / EXECUTE_RECEIPT / VERIFY_RECEIPT 全綠 → LANES_SERVED
+ far_lane_gate.py 回 PUBLISHABLE           → PUBLISHED
```

只有 `PUBLISHED` 可被目錄、檢索、對外引用。**直接寫出的 `.md` 永遠是 CANDIDATE。** 這一條把「寫檔＝完成」的等式拆掉。

### 4.2 授權 / 簽章建議

| 項 | 建議 | 理由 |
|---|---|---|
| `far_round.py` 為 FAR 的唯一入口 | **核准** | 它是把成本梯度翻轉過來的那一件 |
| 036–045 標 `PROVENANCE_MISSING` | **核准** | 保留內容，撤回「已發布研究」地位；其中被證偽的結論已在 041–044 各自撤回 |
| 發布狀態轉移需要 issuer 簽章 | **建議暫緩** | 目前沒有第二個寫入者，先做狀態機即可；簽章等有外部引用需求再加 |
| EXECUTE 超時 600 s | **核准** | 212 秒截斷已證明會誤報成對帳失敗 |

---

## 5. 本篇車道狀態

| 車道 | 結果 |
|---|---|
| PLAN | ✅ `gpt-6.1-sol`、nonce ✓、usage ✓、65.16 s（前次 orchestrator 實跑） |
| EXECUTE | 重跑中（`--timeout` 修正後） |
| VERIFY_SECURITY | 待 EXECUTE 綠燈後自動接續 |

**在本輪結束時，若 EXECUTE 仍未綠燈，本篇 `publication_status` 保持 `UNPUBLISHED`。**

---

## 6. 教訓

前三輪的修法都是**加閘門**——把違規的罰款調高。違規照樣發生，因為**罰款是事後的，成本是事前的**。

這一輪改的是事前：把三次派發壓成一次、把四種失敗逐一消滅、把收據自動落盤。**當合規只要一條指令，就沒有人會去寫散文。**

還有一個更細的教訓：`ERR_LANE_ALL_ROUTES_EXHAUSTED` 這個名字本身在誤導。它說「路由耗盡」，實際是「210 秒到了」。**一個命名錯誤的失敗碼，會讓後續三輪的診斷全部跑偏**——我前兩輪一直在查用量對帳，而真相是一個 `// 2`。
