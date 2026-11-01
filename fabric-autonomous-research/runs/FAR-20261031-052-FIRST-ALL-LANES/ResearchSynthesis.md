# FAR-052｜第一個走完三車道的 FAR：63 秒

日期：2026-11-01（台北）
交付：`FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1`

---

## 0. 這篇的意義不在結論，在它怎麼被產生的

這是本 corpus 二十一篇 FAR 裡，**第一篇在同一次執行中走完三條指定車道**的研究。

```
plan     ok=True  openai-codex/gpt-6.1-sol          usage ✓  22.85 s
execute  ok=True  opencode-go/deepseek-v4.1-flash   usage ✓  19.21 s
verify   ok=True  openai-codex/gpt-6.1-sol          usage ✓  21.37 s
────────────────────────────────────────────────────────────
總計 63.43 秒，三張收據，全部 nonce 回顯、全部 usage receipt ok
```

指令只有一條：

```bash
python scripts/far_round.py --run FAR-20261031-052-FIRST-ALL-LANES --question "…"
```

**這就是 FAR-046 提出的「把合規做成最短路徑」的實證。** 在那之前，三車道是 3 次派發、4 種具名失敗；現在是 1 條指令、63 秒。

---

## 1. 三條車道各自的回答

各車道原文保存在 `lane_output/plan.md`、`execute.md`、`verify.md`，不在此轉述——**轉述會變成第二手材料，而這篇的價值恰恰是「一手材料在磁碟上」。**

VERIFY 車道的角色是檢查前兩條的產出而不是複述它們；它的輸出檔就是它判定的依據。

---

## 2. 為什麼這次能成，前二十一次不能

| 障礙 | 先前 | 現在 |
|---|---|---|
| 傳輸選錯 | `ERR_SEALED_HOME_OAUTH_TRANSPORT` ×2 | 傳輸按 arm provider 寫死在表裡 |
| nonce 沒回顯 | `ERR_NO_ARM_EMITTED_NONCE` | 模板內建指示 |
| 超時被對半 | 210 s 截斷 | 傳 whole timeout |
| 承載過重 | 6000 字 → 601.92 s 無回應 | 預設 400 字 |
| **EXECUTE 被叫去讀 repo** | **601.92 s 無回應** | **brief 明令「不要讀 repo，全部在這份 brief 裡」→ 19.21 s** |

最後一列是關鍵。FAR-051 用對照組證明：同一個 arm、同一條傳輸，**叫它讀 repo 就 600 秒停滯，叫它照 brief 做就 14 秒完成**。這篇把它寫進模板，於是 EXECUTE 19.21 秒。

---

## 3. 對 FHS 交付的意義

三車道可服務一直是「被聲稱」的，現在是「被同一份執行記錄證明」的。這對 `FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1` 的意義是：

- 先前 21 篇 FAR 的結論（含撤回紀錄）**來源不完整**，已標 `PROVENANCE_MISSING`
- 從本篇起，FAR 的結論可以被追溯：誰計畫、誰執行、誰查核、各自的模型與收據

---

## 4. 剩餘

| 項 | 狀態 |
|---|---|
| 本篇 promotion | 待 `far_publish.py --promote`（gate 需先見 synthesis，本檔即為此） |
| 021 篇舊 FAR | 已標 `PROVENANCE_MISSING`，內容保留 |
| WP-12 / WP-20 / WP-11 Hermes 三格 | 未動，狀態同 FAR-048 §3 |
| 視窗正控 | 仍未打響，迴圈維持 paused |

---

## 5. 教訓

九次自我推翻之後，第十次的形狀是**「把修好的東西真的跑一次」**。

前面所有輪次都在修零件：傳輸、nonce、超時、承載、讀取面。零件全對之後，**沒有人把它們串起來跑一次**——直到這一篇。串起來的結果是 63 秒。

**這批研究最貴的一課不是任何單一發現，是「零件正確 ≠ 系統可用」**，而證明系統可用的方法只有一個：跑它。

---

## 6. 收據引用

本篇的每一項車道聲明，來源是下列三個檔案，全部在同一目錄下：

| 車道 | 收據 | 派發原文 |
|---|---|---|
| PLAN | `PLAN_RECEIPT.json` | `_plan_dispatch.json` |
| EXECUTE | `EXECUTE_RECEIPT.json` | `_execute_dispatch.json` |
| VERIFY_SECURITY | `VERIFY_RECEIPT.json` | `_verify_dispatch.json` |

各車道的原始回答在 `lane_output/plan.md`、`lane_output/execute.md`、`lane_output/verify.md`。

**本文不轉述它們的內容**——轉述會變成第二手材料，而這篇的價值是「一手材料在磁碟上，且可被獨立重讀」。
