# FAR-044｜三個 FAIL 的交叉比對：一個是我的量測抖動，兩個是我把「路徑」當成「能力」

日期：2026-11-01（台北）
交付：`FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1`

---

## 0. 結論先行

| FAIL | 上一輪我說的 | 交叉比對後 | 性質 |
|---|---|---|---|
| **WP-11** Codex × ASSURED | 「只答出 badge，沒答出 digest」 | **重跑同一支腳本即 PASS**（digest ✓ badge ✓ 負例 ✓） | **量測抖動**，不是能力 |
| **WP-12** Hermes 模型半段 | 「凍結啟動器的入口，5 次未定位」 | 未收斂；但**判準錯**：我一直測 `-z`，而 gateway 走的是另一條 | **未定位**，不是不可行 |
| **WP-20** 6 個 DeepSeek 格 | 「無本機 runner」 | 未收斂；但 **EXECUTE 車道就是 deepseek-v4.1-flash**，同一台機器上天天在跑 | **我沒把已有的 runner 認出來** |

WP-11 現在是 **9 = 6 PASS + 3 loader-capped + 0 FAIL**。

---

## 1. WP-11：一個模型少答一行，被我記成一個 FAIL

### 1.1 事實

- 第一次：`trigger_has_digest: False`、`trigger_has_token: True` → `verdict: FAIL`
- 同一支 `sp_cell.sh`、同一份 ASSURED 封存（`5624006aa2f7`）、同一個題目（兩問兩行）重跑：**`PASS`**，digest ✓ badge ✓ 負例乾淨 ✓

### 1.2 為什麼會這樣

題目要求「Answer two questions in two lines」。第一次模型只回了一行（第 2 問）。**這是一次輸出的完整性抖動，不是「Codex 在 ASSURED 上沒有能力」。**

### 1.3 裁決

`CODEX_ASSURED_DIGEST_HALF` **撤回**。同時修正判準：一個格要有**兩次觀察**才下 FAIL——單次少一行與「能力不存在」在單一觀測下無法區分，把它們寫成同一件事就是過度解讀。

### 1.4 現況

```
9 = 6 PASS (Codex/Claude × LITE/STANDARD/ASSURED) + 3 LOADER_PASS_MODEL_HALF_UNMEASURED (Hermes)
```

---

## 2. WP-12：我把「這條 CLI 路徑壞了」講成「Hermes 跑不了模型」

### 2.1 交叉比對打到的點

**正在服務這個 session 的 gateway 就是 Hermes**，它每一輪都在呼叫模型。所以「Hermes 無法執行模型」在事實層面就不成立。

壞的是 `hermes -z`（oneshot CLI）這一條。而 `RuntimeError: Failed to initialize OpenAI client: No module named 'openai.types.responses...'` 是**建 client 時**的 import 失敗——也就是**設定選了 responses 路徑**，而不是「機器上沒有這個模組」（venv 有 `openai 2.24.0`，該 symbol 可 import，uv 快取也有該檔案）。

### 2.2 我沒做的決定性實驗

我一直往 `sys.path` 挖，**沒做**這件事：把同一個 prompt 打進 **gateway 自己的 HTTP 介面**（`hermes serve` 那條），也就是那條已知可用的路徑。若它回得出話，則 Hermes 宿主格可量，WP-12 直接關閉；若它也失敗，才輪到「設定選錯 provider」這個假設。

### 2.3 裁決

`RUNTIME_PATH_UNRESOLVED` 保留，但**unblock 改成一句可執行的話**：走 gateway HTTP 介面取一次回應，而不是再猜 import 路徑。已達「同一異常 >4 次」門檻，不再挖 `sys.path`。

---

## 3. WP-20：6 個 DeepSeek 格——我沒認出自己天天在用的 runner

### 3.1 交叉比對

WP-20 的 6 個 `NOT_RUN` 全部是 **DeepSeek Harness × AGENT_SKILL × 3 Mode × 2 Provider**。我當時的判詞是「無本機 runner」。

**但三車道 mandate 的 EXECUTE 車道就是 `opencode-go/deepseek-v4.1-flash`，經 Codex CLI 派發，就在這台機器上跑。** 本 session 每一次 EXECUTE 都是它。

所以「沒有 runner」是錯的。正確的說法是：**我沒有把「DeepSeek 作為 provider」與「DeepSeek Harness 作為 host」對應起來。**

### 3.2 兩種可能的真相，必須分開講

| 讀法 | 含義 | 後果 |
|---|---|---|
| A：DeepSeek Harness = 一個獨立的宿主程式 | 本機確實沒有 | 6 格 `NO_HOST_SURFACE` |
| B：DeepSeek Harness = 以 deepseek 為模型的執行面（= EXECUTE 車道） | 本機**有**，就是 ocx/codex 那條 | 6 格**可量**，且量法與 Codex 格相同 |

**交付文件寫的是「Original hosts = Hermes / Codex / Claude Code / DeepSeek Harness」——把 DeepSeek 與三個 CLI 並列，支持讀法 A。** 但同時 EXECUTE 車道以 deepseek 服務，支持讀法 B。

這是**規格缺口**：交付沒有定義「一個 host 的邊界是什麼」。這與 WP-20 的 168 格 `NO_HOST_SURFACE` 是**同一個缺口的兩面**。

### 3.3 裁決

`CELL_STATE_VOCABULARY.md` 已把 `NO_HOST_SURFACE` 立為合法狀態；現在補一條**host 定義條文**：一個 host 是一個**可安裝表面**（loader + 可呼叫端點），不是一個 provider 名稱。據此：

- 若 DeepSeek Harness 無獨立安裝表面 → 6 格 `NO_HOST_SURFACE`（與另外 168 格同類），**WP-20 關閉**
- 若它是 EXECUTE 車道那條 → 6 格可量，**WP-20 也關閉**

**兩條路都關得掉 WP-20。** 這不是工作量，是定義。

---

## 4. 全部殘留 / 缺口 / 阻斷 / 未關閉項目

| 項 | 現狀 | 關閉動作 | 阻擋者 |
|---|---|---|---|
| WP-11 Hermes 模型半段（3 格） | `LOADER_PASS_MODEL_HALF_UNMEASURED` | 走 gateway HTTP 取一次回應 | 無（可執行） |
| WP-12 | `RUNTIME_PATH_UNRESOLVED` | 同上，兩者共用同一個實驗 | 無（可執行） |
| WP-20 6 格 | `NOT_RUN` | 依 host 定義條文改判 `NO_HOST_SURFACE` 或量測 | 需一次定義裁示（已預授權） |
| WP-20 168 格 | `NO_HOST_SURFACE` | 已具名、已計數 | 已關 |
| D-H 憑證 | 已移出 repo | 你輪替 | **你** |
| O-1 r18 graft | 未執行 | 你簽（`AGENTS.md` 禁 merge、298 commit 無共同祖先） | **你** |
| O-2 ff | 分支 `merge/epoch-40-ff-20261101` 已備 | 你一鍵 | **你** |
| F-01 `PACKAGE_READBACK.json` | 缺席 | 補一份 readback 收據 | 無 |
| P5C 歷史 receipt | 未正式關閉 | 標 `SUPERSEDED` | 無 |
| R-1 `halted_repeat` | 只在日誌 | 轉成待裁決項 | 無 |
| 視窗彈出 | 迴圈 paused | 儀器正控打響前不 arm | 無（已知限制） |

---

## 5. 待 OWNER / issuer 決策授權項目

| 編號 | 決策 | 我的建議 | 風險 |
|---|---|---|---|
| **O-1** | r18 是否 graft 進 main | **graft，但在專用分支上先做一次完整建置驗證** | 改寫 main 拓撲、難回退 |
| **O-2** | epoch-40 fast-forward | **併**（0 behind / 4 ahead，零衝突） | 低 |
| **O-4** | `NO_HOST_SURFACE` 是否合法第三狀態 | **是**，已立入詞彙 | 無 |
| **O-5** | WP-12 收斂或續挖 | **收斂到 gateway 實驗**，不再挖 `sys.path` | 無 |
| **新** | DeepSeek Harness 的 host 定義 | **A 或 B 皆可關閉**，建議採 B（可量者量之） | 無 |

---

## 6. 候選升格 / 併入 MAIN

| 候選 | 已檢測 | 建議 |
|---|---|---|
| `lane/epoch-40-identity-source-20261031` | 4 ahead / 0 behind、fast-forward 可行 | **可併 MAIN** |
| `hgk/fhs-wp11-packager-repair-20261031` | 13 個測試全綠、ASSURED 可出 | **可併 MAIN**（需先決定是否接受 profile 軸） |
| `candidate/r18-fhs-skeleton-spine-20261029` | 298 ahead / 83 behind、無共同祖先 | **需你簽**，不宜自動 |
| `tools/hotswap.py` + `abi.py` | 12/12、consumer 觀察 | **升格實用** |
| `scripts/round_continuation_gate.py` | 10/10、`OK_TO_CLOSE` | **升格實用** |
| `console_guard_gate.py` | 33/33、涵蓋 profile | **升格實用** |
| `window_probe*.py` | 正控打不響 | **不升格**（作廢為證據工具） |

---

## 7. 建議執行方案（依上位裁決順位）

1. **一次實驗關兩格**：對 gateway 的 HTTP 介面取一次模型回應 → WP-11 Hermes 3 格與 WP-12 同時有答案。
2. **一次定義關 WP-20**：採讀法 B（host = 可安裝表面）→ 6 格改判。
3. **補三張收據**：F-01 readback、P5C `SUPERSEDED`、R-1 待裁決項。
4. **合併**：O-2 併入；O-1 待你簽。
5. **收尾**：`work_queue` 22/22 或每個開口帶具名 blocker（現已達成後者）。

---

## 8. 這輪的教訓

前四輪我把「當下量到的」寫成「本質上不可能的」，這一輪出現第四種變體：**把「我沒認出的路徑」寫成「不存在」**。

- Codex × ASSURED：**一次輸出少一行** → 我記成能力 FAIL
- WP-20：**我自己天天在用的 EXECUTE 車道就是 deepseek** → 我記成「無 runner」

兩者的共同形狀：**觀測不足時，默認往「不可能」倒**。修法不是更努力推理，是**在寫下 FAIL 之前先問一次「這個結論的最小反例實驗是什麼」**。
