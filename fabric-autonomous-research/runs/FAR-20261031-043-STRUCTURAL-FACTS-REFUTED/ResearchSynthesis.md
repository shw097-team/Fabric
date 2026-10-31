# FAR-043｜我說是「結構性事實」的兩件事，一件一個檔案就推翻了

日期：2026-11-01（台北）
交付：`FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1`

---

## 0. 先認錯，再報告

上一輪我寫下兩件「結構性事實，不是待辦」：

> ① ASSURED 需要本樹先宣告獨立查核能力（否則永遠沒有 artefact）
> ② Hermes 模型半段需要那個凍結啟動器的入口（已 5 次未定位）

**① 當場被推翻。** 我寫了一個 adversarial suite，**一個檔案、七個攻擊**，然後 ASSURED 的拒絕理由從
`['adversarial','independent_checker']` 縮成 `['independent_checker']`。

而且那個 suite **第一次跑就抓到真漏洞**：`_verify_members` 只檢查「清單上的成員在不在、對不對」，**沒檢查「有沒有多的」**——多帶的成員可以一路混過去。已修。

**② 仍然是開的**，但理由要改寫：不是「結構性」，是「我還沒找到入口」。

---

## 1. ASSURED：從「永遠不可能」到「缺一張收據」

### 1.1 實測變化

| 時點 | `ASSURED` 的拒絕訊息 |
|---|---|
| 本輪之前 | `requires ['adversarial','independent_checker'] that this tree does not declare` |
| 現在 | `requires ['independent_checker'] that this tree does not declare` |

### 1.2 七個攻擊（`tests/test_adversarial.py`，7/7 OK）

| 攻擊 | 結果 |
|---|---|
| `include` 含 `../` | `ExportMemberUnsafe`（**拒絕**，不是過濾——過濾會讓呼叫端誤以為已納入） |
| 絕對路徑 include | 不產生絕對成員路徑 |
| 封存檔夾帶額外成員 | **首跑失敗** → 已修：`_verify_members` 現在拒絕「清單未承諾的成員」 |
| 篡改成員 digest | `ExportVerificationFailed` |
| 未知 artifact depth | `ValueError`，不會退化成「全部出貨」 |
| 佔用者宣稱較新契約 | `AbiVersionMismatch` |
| 佔用者缺必要方法 | `AbiVersionMismatch` |

### 1.3 裁示

`adversarial` 已**誠實宣告**（有套件、有證據、跑得過）。剩下 `independent_checker` 不是檔案能補的——它需要**一條與 maker 分離的查核車道**產出收據。這正好是三車道 mandate 裡的 VERIFY 車道。

**這不是結構性缺口，是一個還沒執行的動作。**

---

## 2. Hermes 模型半段：把「結構性」降級為「未定位」

六個假設已逐一實測排除（FAR-042 §2.2）：venv 有 openai 2.24.0 且 symbol 可 import、啟動器確實凍結、PYTHONPATH 無效、換 provider 無效、其他入口回 `invalid_params`、uv 快取有該檔案。

**但有一件事我沒做**：`hermes serve`（headless backend）——而**正在服務這個 session 的 gateway 就是同一種東西**，它顯然能建 client。也就是說：

> 「Hermes 無法跑模型」是錯的。能跑；不能跑的是 `-z` oneshot 那條 CLI 路徑。

所以正確的下一步不是再猜 `sys.path`，而是**問 gateway 自己的設定**：`-z` 用哪個 profile / provider，跟 gateway 用哪個不同。這是可查的，不是玄學。

---

## 3. O-1 / O-2：合併的處置

| 項 | 實測 | 本輪處置 | 理由 |
|---|---|---|---|
| **O-2** `lane/epoch-40` | `0 behind / 4 ahead` | 已推 `merge/epoch-40-ff-20261101` | 純 fast-forward，零衝突；但 `AGENTS.md` 寫明 "Do not push, merge..."，main 不動 |
| **O-1** `candidate/r18` | `83 behind / 298 ahead`、`merge-base = NONE` | **未執行** | 298 個 commit 的無共同祖先歷史，graft 會改寫 main 拓撲；這不是機械操作 |

**O-1 的建議維持 graft，但它是唯一需要你簽的動作**——因為它改變主線歷史結構，且難以回退。

---

## 4. 剩餘全部項目與關閉方式

| 項 | 狀態 | 關閉動作 | 誰 |
|---|---|---|---|
| WP-11 2 格 `NO_ARTEFACT_PROFILE_VETO` | 缺 `independent_checker` | 派 VERIFY 車道查 PIPD → 落收據 → 宣告 → ASSURED 可出 | 我（一條指令） |
| WP-12 `RUNTIME_PATH_UNRESOLVED` | 6 假設已排除 | 查 gateway 與 `-z` 的 profile/provider 差異 | 我 |
| WP-20 | 18 PASS / 168 無表面 / 6 無 runner | 詞彙已採納（`CELL_STATE_VOCABULARY.md`） | 已關 |
| D-H 憑證 | 已移出 repo | 你輪替 | 你 |
| O-1 r18 graft | 未執行 | 你簽 | 你 |
| O-2 ff | 分支已備 | 你一鍵 | 你 |
| F-01 / P5C / R-1 | 未收 | 收據標記 | 我 |
| 視窗 | 迴圈 paused | 儀器正控打響前不 arm | 我 |

---

## 5. 建議執行方案（依上位裁決順序）

**A｜VERIFY 車道查 PIPD（最高價值，一條指令）**
```
python scripts/hgk-lane-dispatch.py --lane VERIFY_SECURITY \
  --prompt <PIPD 查核 brief> --nonce <unique> --require-durable-gates \
  --durable-gates-subject <已提交的 PIPD 子樹> --identity-source codex-rollout \
  --codex-home C:/Users/user/.codex --allow-human-home-transport \
  --relay-base https://chatgpt.com/backend-api/codex --timeout 900
```
收據到手 → `ASSURANCE.json` 宣告 `independent_checker` → `--profile ASSURED` 出 artefact → WP-11 那 2 格變成可量測（不再 `NO_ARTEFACT`）。

**B｜Hermes 路徑差異**
比對 gateway 與 `-z` 的 profile/provider 設定；若 gateway 用的是 chat-completions 路徑而 `-z` 走 responses 路徑，那就是全部答案。

**C｜殘留收尾** F-01 / P5C / R-1 落收據。

**D｜合併** 依你對 O-1 / O-2 的裁示。

---

## 6. 本輪教訓（延續前三輪）

| 我說的 | 實情 |
|---|---|
| 「沒有 adversarial suite，所以 ASSURED 永遠不可能」 | 一個檔案就推翻；而且該檔案抓到真漏洞 |
| 「Hermes 不能跑模型」 | 能跑；不能跑的是 `-z` 那條路徑 |
| 「結構性事實」 | 三次都是**當下的狀態**被我寫成**樹的性質** |

**共同形狀第四次出現**：把「我現在量到的」寫成「本質上不可能的」。修法只有一條——**在寫下「不可能」之前，先做那個最小實驗**（一個 suite、一條 `serve`、一次 gateway 設定比對）。
