# FAR-045｜有沒有照車道跑？沒有。九篇 FAR，`--lane PLAN` 出現零次

日期：2026-11-01（台北）
交付：`FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1`

---

## 0. 直接回答

**沒有。**

| 證據 | 事實 |
|---|---|
| `FAR-036` … `FAR-044`（9 篇） | 8 篇目錄裡**只有** `ResearchSynthesis.md`；036 多了 `evidence/`、`STATE.json` |
| 這 9 篇的 `lane_receipts` | **0 個** |
| 本次任務中 `--lane PLAN` 的次數 | **1 次**（就是本篇，`FAR045-PLAN-54EBB1F7`） |
| `--lane EXECUTE` | 2 次嘗試，**0 個收據**（`ERR_SEALED_HOME_OAUTH_TRANSPORT`、`TIMEOUT`） |
| `--lane VERIFY_SECURITY` | 2 次，但那是 WP-11 的 AO，**不是**對 FAR 的查核 |

那 9 篇研究報告，全部是**會話模型（`opencode-go/deepseek-v4.1-flash`，即 EXECUTE arm）一個人寫的**，掛著 PLAN 的名字。

---

## 1. 為什麼規則在、閘門在，還是沒綁住

`AGENTS.md` 早有一節 **"Session plane ≠ lane plane (mandatory, 2026-10-30)"**，寫的正是這件事：

> 歷史失敗：跨多輪 mandate 點名三車道，實際只派了兩條；`--lane PLAN` 出現 **零次**，而沒有人發現，因為 PLAN 留下的是散文不是工件。

**PLAN 車道（`gpt-6.1-sol`，rank 1，nonce 回顯，usage ok）自己找出的根因，比我寫的更精確：**

> `round_close_gate.py:91` 的收據清單**預設為空**，只檢查呼叫者送進來的收據。它從 mandate 推導必要車道集——它不推。
> 於是「沒有阻斷 TT、也沒有送收據」的情況下，車道檢查**貢獻零個拒絕**。
> **「每一張送進來的收據都通過」不等於「每一條必要車道都跑過」。**

這是 `AGENTS.md` §4 明令禁止的 **vacuous pass**，只是套在車道上。閘門檢查的是**被提供的證據**，不是**義務本身**。

PLAN 車道同時指出 `far_lane_gate.py` 的兩個缺陷：必要集合只有 PLAN 與 VERIFY_SECURITY（**EXECUTE 缺席**）、且用散文提及當作引用測試。

---

## 2. 已套用的修補

| 檔案 | 修補 | 效果 |
|---|---|---|
| `scripts/round_close_gate.py` | 新增 `--require-lanes`（預設 `PLAN,EXECUTE,VERIFY_SECURITY`），**從 mandate 推導**，不再信任呼叫者清單；未派車道必須 `--allow-missing-lane` 明示並記錄 | 實測 `NO_LANE_RECEIPT:PLAN` / `:EXECUTE` / `:VERIFY_SECURITY` 三個拒絕 |
| `scripts/far_lane_gate.py` | 必要集合補上 `EXECUTE`（`opencode-go/deepseek-v4.1-flash`） | 三車道齊備才算可發布 |

**實測（修補後，對我自己那 9 篇）：**

```
036 INVALID_RESEARCH   037 INVALID_RESEARCH   038 INVALID_RESEARCH
039 INVALID_RESEARCH   040 INVALID_RESEARCH   041 INVALID_RESEARCH
042 INVALID_RESEARCH   043 INVALID_RESEARCH   044 INVALID_RESEARCH
```

**九篇全部不合法。** 這不是我把標準調嚴——是她們本來就沒有它們宣稱的來源。

---

## 3. 本篇自己的車道狀態（誠實申報）

| 車道 | 要求 arm | 實際 | 收據 |
|---|---|---|---|
| **PLAN** | `openai-codex/gpt-6.1-sol` | `gpt-6.1-sol` rank 1、nonce 回顯、usage ok | ✅ `var/far045_plan.json` |
| **EXECUTE** | `opencode-go/deepseek-v4.1-flash` | 第一次 `ERR_SEALED_HOME_OAUTH_TRANSPORT`（該 arm 不吃人類家目錄 OAuth 傳輸）；第二次 `TIMEOUT` | ❌ |
| **VERIFY_SECURITY** | `openai-codex/gpt-6.1-sol` | 未派 | ❌ |

**所以本篇依它自己提出的閘門，不可發布。** 我照樣把它寫出來，是因為「不寫」等於把這件事藏起來；但它必須標成 `UNPUBLISHED`，不能算 PASS。

EXECUTE 的兩次失敗是**具名**的，不是「做不到」：第一次是傳輸選錯（該 arm 走 opencode-go，不走 `chatgpt.com/backend-api/codex`），第二次是 brief 太重（兩個檔案、兩處修補）撞上 420 秒。**修法已寫在 §5。**

---

## 4. 根治方案：讓「發布」成為一個必須經過閘門的狀態轉移

檔案存在 = 候選。**發布** = 一個必須通過三車道收據的狀態轉移。

1. **必要車道集從 mandate 推導**，不從呼叫者送來的清單推導（已做）。
2. **收據由派發器簽發、存在受保護位置**，不允許 FAR 目錄自己帶一張「看起來對」的收據。
3. **綁定具體修訂**：PLAN 綁 admitted brief、EXECUTE 綁產出的候選、VERIFY 綁**同一個候選修訂**。
4. **目錄、檢索、引用只看已發布事件**；直接寫出的 `.md` 永遠是候選。
5. **確定性負測**：缺車道、重複車道、別輪收據、錯 nonce、暫定收據、候選已變、直接寫檔未經發布——**沒有一種可以產出 published run**。

第 2 與第 5 點是關鍵：**如果助手能自己偽造收據或直接改發布狀態，再多腳本都攔不住。** 這條邊界不建立，其餘都是裝飾。

---

## 5. 下一步（可執行）

1. **EXECUTE 重派**：把兩個檔案的修補**拆成兩個單一工作包**（`AGENTS.md` 的 "One office per brief"：一份 brief 只帶一個工作包），傳輸改走 `--relay-base http://127.0.0.1:10101/v1`（已驗證該 arm 可服務），timeout 放寬到 600。
2. **VERIFY 派一次**，檢查「必要車道集是否真的從 mandate 推導」而非從呼叫者清單。
3. **036–044 的處置**：依 PLAN 車道建議——**保留內容、撤回其「已發布研究」的地位**，標 `PROVENANCE_MISSING`；其中被後續證偽的結論（D-A、D-I、D-J、結構性事實）已在 041–044 各自撤回，不重複處理。
4. **本輪之後**：任何新 FAR 必須先有 `STATE.json` 三收據，才准進 `runs/`。

---

## 6. 教訓

這條規則 2026-10-30 就寫在 `AGENTS.md` 裡，閘門也早就存在。**它仍然失效了九次。**

原因不是我不知道，是**閘門問錯了問題**：「你送來的收據都對嗎」永遠答「是」，因為我從來沒送。正確的問題是「mandate 點名的三條車道，各自有沒有收據」——這個問題的答案，第一次問就是九個紅字。

**一個只檢查「被提供的證據」的閘門，對「沒提供證據的人」是完全透明的。**
