# Oversized-SKILL Handling Route (FAR-on-FAR 2026-08-14, UD-SKILL-GUARD-2026-08-14-001)

任何 SKILL 超過 ~100KB（觸碰 skill_manage limit）時的**強制處理路由**。
2026-08-14 實證：手動瘦身造成 2 處結構破壞（`**` 殘留、換行被吃）+ skill_manage
patch 4 次 100k-limit 失敗 + 並行 session 覆寫。

## HARD ROUTE（優先序）

```
SKILL 過大
  ├─ 1. 拆分+路由（首選，禁止直接瘦身）
  │     a. 機械化拆分器 skill_split.py：掃 sections → 大段（>3KB）搬入 references/step-*.md
  │        （保留原文 bytes，不手動改寫——手動 edit = 斷鏈風險）
  │     b. 主檔留 3 行指標：section 名 + 觸發條件 + 檔路徑
  │     c. 主檔「Routing map」段：操作類型 → 載入哪個 references 檔
  │     d. 拆後跑 skill_guard.py post → PASS 才放行
  ├─ 2. 不適合拆分時 → GUARDED SLIM（瘦身後必須自檢查+測試+評比）
  │     a. 事前：skill_guard.py pre（baseline）
  │     b. 瘦身：只刪冗餘/重複（不得改語意），保留全文 references 指標
  │     c. 事後：skill_guard.py post（dangling refs / orphan patterns / size）
  │     d. 測試：被瘦身 section 的關鍵操作元素 grep 數不減（如 write_file not patch）
  │     e. 評比：比較 pre/post stats（size/refs/sections），確認無升級倒退
  │     f. 驗收：以上全 PASS 才准放行使用
  └─ 3. 放行後：更新記憶/文件，記錄本次處理（size before/after, guard 結果）
```

## 為什麼（FAR 自身研究 2026-08-14）

- 手動瘦身 1 次事件 → 2 處結構破壞 + 4 次工具失敗 + 1 次並行覆寫
- skill_manage patch 在 >100k 時失敗（limit），逼迫手動 edit（高風險）
- references 模式已驗證可行（12+ 檔），機械搬移無手動編輯風險
- 搬走即失聯風險：routing map 必須明確「操作 → 載入哪個檔」

## 工具

- `var/fda/skill_guard.py <skill_dir> pre|post` — 結構完整性檢查（dangling refs/
  orphan patterns/換行被吃/大小），PASS/BLOCKED
- `skill_split.py`（可選建置）— 機械化 sections 拆分器

## 驗證

- 拆分/瘦身後：skill_guard.py post = PASS
- 關鍵元素 grep 測試 = 不減
- pre/post stats 比較 = 無倒退


---

## 處理記錄 2026-08-15 — WO-HGK-SKILL-SPLIT-001（hgk-governed-execution 拆分）

- **對象**: hgk-governed-execution SKILL.md（拆分前 103,481 chars / 107,604 B → BLOCKED）
- **方式**: 方案 A 機械拆分（`var/a2/skill_split_exec.py`，byte-exact，無手動改寫）
- **搬移 7 段**（references/）: step-pitfalls-checklist.md / step-9-fda-cua-operations.md /
  support-files-index.md / step-6d-evidence-closure-pipeline.md / step-evidence-only-contract-a.md /
  step-10-external-provider-tool-enablement.md / step-verify-only-lane.md
- **主檔**: 新增 `## Routing map`（When to use 之後）+ 每段 3 行指標；Step 9-0/9-0a gate 全文保留 inline
- **驗證**: skill_guard pre (SIZE BLOCKED baseline) → post **PASS**（36,802 B, 26 sections）；
  T2 關鍵元素 grep 不減 PASS；T3 位元組重建 diff **byte-identical PASS**；T4 0 新增孤兒 PASS；
  T5 hooks 路徑 PASS；T6' union 提及 40 ≥ 23 PASS；冷啟動 canary C1-C4 依結果
- **教訓**: 拆分器 off-by-one（range 替換後跳行）與 pointer 尾端換行陷阱——dry-run + 重建驗證是必要防護；
  並行 session 會在 references/ 寫新檔（孤兒 baseline 豁免機制必要）

---

## 拆分後複檢清單（2026-08-15 複核 round 實證，WO-HGK-SKILL-SPLIT-001 recheck）

拆分完成 ≠ 驗證結束。複檢至少要跑（maker 掃描 + fresh-context AO 雙重）：

1. **反向重建（losslessness 的決定性證明）**：把 step 檔塞回 pointer 位置 + 移除新增段（Routing map）
   → 與拆分前 bytes 比對（byte-identical）。陷阱：塞回的 step 檔若是**已修補版**（如索引附加條目）
   會 ≠ 原始 slice——用記錄在案的原始 slice sha 截取前段重建（本 WO：索引前 15,232B sha 77b6d2ec90e6）。
2. **真原始檔基準留存**：拆分當下就把 SKILL.md 原 bytes 存一份（var/a2/）供日後稽核——事後重建補留
   （107,604B sha 25c8c244）可行但多繞一圈。
3. **索引完整性**：被搬移的 Support files 索引**不會自動包含新 step 檔**——拆分後必須檢查並補條目
   （+自索引條目）；否則 Routing map 指它做「全部支援檔說明」但查不到新檔（R5 實例）。
4. **孤兒 delta 基準**：先盤點既存孤兒（baseline 豁免），驗收判「**0 新增孤兒**」而非「0 孤兒」。
5. **方向性引用（moved 檔內 above/below/§）**：多數是內部自洽（指向同檔內規則）或字面量（`# replaced below`）
   或指向未搬移檔（fda-desktop-automation-cua.md）——逐一判斷，不要直接判 FAIL。
6. **AO/複核期間的檔案變動歸因**：mtime 變動先釐清是否為 orchestrator 本人修復（非第三方 session）。
7. **size 語義**：skill_guard 的 size 是 **chars** 非 bytes（36,802 chars vs 39,511B on-disk）——回報兩者都給。
8. **冷啟動 canary**（fresh leaf 只給主檔）：驗證 Routing map 串聯真的能把 agent 帶到對應 references 檔
   （C1-C4：操作細節/閉環/排查/索引查找）；canary 的 BLOCK 路徑 prompt 勿含意圖動詞（見 runtime-notes §5）。
