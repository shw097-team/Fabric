# 並行業主命令衝突記錄 — 2026-10-21

**記錄者**：本回合（FAR-MINIMAX-MANDATE-20261021，HG-KSEOS 控制平面）
**發現時間**：2026-10-21 15:37–15:42（台北時間）
**性質**：**事實記錄，不做裁決。裁決權在業主。**

## 發生了什麼

本回合依業主 15:xx 的命令，把 PLAN、EXECUTE（Codex CLI）、VERIFY/SECURITY（Codex CLI）
三車道綁定到 `opencode-go/minimax-m3.1-flash-free`（MiniMax M3.1 Flash, OPENCODE GO），
epoch 25，commit `a1bd583` + `1cbb9d2`。

**在 AO 第三次驗收執行期間，另一個 session 依據一條更新的業主命令
（`OWNER-ORDER-20261021-GPT-QUOTA-RESTORED`，記錄為「GPT 配額已恢復」）
把 pool 重綁回去**：

| 車道 | 本回合（epoch 25，已 commit） | 另一個 session（epoch 26，已 staged 未 commit） |
|---|---|---|
| PLAN | `opencode-go/minimax-m3.1-flash-free` | `openai-codex/gpt-6.1-sol` |
| EXECUTE | `opencode-go/minimax-m3.1-flash-free` | `opencode-go/deepseek-v4.1-flash` |
| VERIFY_SECURITY | `opencode-go/minimax-m3.1-flash-free` | `openai-codex/gpt-6.1-sol` |

另一個 session 的 pool `revision` 12、registry `epoch` 26，**已完整 staged**（14 個檔案，
含它自己的 `evidence/review/OWNER-ORDER-20261021-GPT-QUOTA-RESTORED/` 收據與
`tests/test_lane_policy.py` 的更新）。

## 本回合的狀態（未受影響）

本回合的兩個 commit **已在 HEAD 且已固定**：
- `a1bd583` — 三車道 MiniMax 綁定（epoch 25）
- `1cbb9d2` — route-level auth posture 同步（獨立 AO 找到的第二層缺陷）

Fabric 證據包已發布到 `pub/far-minimax-mandate-20261021`（commit `db26179`），
並通過遠端 object-DB 重算驗證（58/58 manifest digest 相符，0 缺失，0 不符，0 機密）。

**本回合沒有、也不會撤銷另一個 session 的 staged 變更。** 那是它的施工，不是本回合的。
本回合對 canonical pool／registry／assignment 的**任何後續寫入都已停止**，
以免與它互相覆蓋。

## 另一個 session 指出的、本回合的真實缺陷

它的 pool `change_log` rev 11→12 記載：

> "concurrent commit a1bd583 had moved it to minimax while simultaneously reverting declared_by
> to a text saying 'EXECUTE unchanged' -- the artifact contradicted itself."

**這個批評是對的。** 本回合的 `apply_minimax_binding.py` 把三車道 rank-1 都設成 MiniMax，
但 pool 的 `declared_by` 文字欄仍保留著「只改 PLAN 與 VERIFY、EXECUTE unchanged」的舊敘述。
**artifact 內部自相矛盾。** 這是本回合的缺陷，已被另一個 session 記錄，本回合承認。

（該 session 的 epoch-26 版本把 `declared_by` 改寫為與實際配置一致，方向正確。）

## 另一個 session 明確保留的東西

它的 rev 11→12 記載：

> "the previous rank-1 (opencode-go/minimax-m3.1-flash-free) demoted to a reachable fallback on
> both lanes and NOT removed."

**MiniMax 臂在 epoch 26 仍被保留為可達的 fallback，沒有被刪掉。**
這與本回合的設計意圖一致：本回合從頭到尾沒有刪除任何既有臂。
所以兩條命令**不是互斥的**——它們是同一條臂鏈上的不同 rank-1 選擇。

## 為什麼本回合不能自行裁決

1. **本回合收到的命令是「三車道全 MiniMax」。** 另一個 session 記錄的命令是
   「只改 PLAN 與 VERIFY/CHECKER，EXECUTE 維持 DeepSeek V4.1 Flash」，並以「GPT 配額已恢復」為由。
   兩者不能同時是「最新的業主命令」。
2. **本回合不知道另一個 session 收到的訊息時間與原文。** 它可能更晚（因而更優先），
   也可能是對業主在不同 session 裡說法的不同解讀。
3. **本回合沒有權限撤銷另一個 session 已 staged 的施工。** 就像 SBL 一樣，那是別人的工作。

## 需要業主裁決的問題（單一選擇）

**哪一條是有效的業主命令？**

- **(A) 本回合的命令有效** — 三車道全 MiniMax（epoch 25）。
  另一個 session 的 epoch-26 staged 變更應被撤回或改寫。
  本回合的 `declared_by` 矛盾需修正（可直接套用另一個 session 已寫好的敘述結構）。
- **(B) 另一個 session 的命令有效**（更晚，且業主已改變心意）— PLAN/VERIFY = `gpt-6.1-sol`，
  EXECUTE = `deepseek-v4.1-flash`（epoch 26）。
  本回合的兩個 commit 保留為**歷史與證據**（它們記錄了 MiniMax 臂的可用性實測、
  跨欄位缺陷的發現與修補、以及那個「一個事實存兩份」的治理教訓），
  但**不再代表現行配置**。
  本回合的證據包必須標註為「已被 epoch 26 取代」，不得被當成現行契約。
- **(C) 兩條都要**（若業主的意思是「MiniMax 保留為首選，GPT 在配額恢復後也可優先」）——
  那需要業主說明**在什麼條件下**用哪一個，因為 lane pool 只能有一個 rank-1。

**在業主裁決之前**，本回合的狀態是：

- canonical pool / registry / assignment 的**工作樹內容** = 另一個 session 的 epoch-26 staged 版本；
- **git HEAD** = 本回合的 `1cbb9d2`（epoch 25）；
- 兩者不一致，且**這個不一致是刻意保留的**，不是遺漏。

## 本回合不受影響、可獨立成立的產出

以下項目與「哪個 rank-1 生效」無關，全部成立：

1. **三車道 MiniMax 的 HGK admission 收據**（`ADMITTED`，`required_arm == served_arm`，
   model 實際驅動 shell 工具）——證明這個臂可用。
2. **跨欄位缺陷的發現與修補**（`a1bd583` + `1cbb9d2`）——registry 的 route rows 必須由 pool 推導；
   這是結構性教訓，與 rank-1 是誰無關。
3. **測試 oracle 的根因修補**（stub 從 `--model` 推導 provider/model）——與 rank-1 是誰無關。
4. **`tests/fixtures/` 納入版控**——clean checkout 可重建測試套件。
5. **殘留主題的實測索引**（460 項 / 120 目錄 / 2 筆 TT OPEN）與 **FAR 裁決報告**——
   仍待業主確認，數字不受影響。
6. **獨立 AO 找到第二層缺陷的原始證據**（230KB stdout）——證明「AO 必須跑在提交位元組上」的價值。

## 誠實的天花板

本回合的驗收**沒有取得 AO 自己簽署的 verdict 檔**：
第一輪 AO（540s）與第二輪 AO（900s）都完成了實質檢查，但都因為
「VERIFY_SECURITY 車道預設是唯讀沙箱，而 verdict 目標在受治理樹內」
而無法寫出 verdict 檔；第三輪改用 `--sandbox workspace-write --lane-scratch` 後，
因 pool 已被另一個 session 重綁而立即失敗（`ERR_LANE_REQUIRED_ARM_ABSENT`）。

第二輪的檢查結果已從它自己的 command outputs 逐條轉錄（`AO2_findings_transcribed.json`），
但**轉錄不等於 AO 簽署的 verdict**。要取得簽署 verdict，必須在 pool 穩定後重跑。
