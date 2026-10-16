# Oversized-SKILL split status（2026-08-15, WO-HGK-SKILL-SPLIT-RESEARCH-001 Gate 1）

`references/oversized-skill-handling-route.md` 的執行現況姊妹檔（該檔為權威路由；本檔記錄 2026-08-15 研究後的實況與執行前置）。

## 現況（2026-08-15 實測）

- hgk-governed-execution SKILL.md = **104,817 chars（skill_manage 計）／106,278 chars（len 計）／1326 行** — 已超 100k 上限。
- **>100k 現在同時阻斷 skill_manage 的 SKILL.md patch**（實證：patch 被拒「SKILL.md content is 104,817 characters (limit: 100,000)」）——拆分不再只是載入品質問題，**是任何後續 SKILL.md 編輯的前置條件**。拆分前的教訓先寫入 references/（支援檔無大小限制），拆分時一併搬入。
- 研究報告：`var/a2/SKILL_SPLIT_RESEARCH_REPORT_v1.md`（Q1-Q5 完整方案 + 風險矩陣 + 驗證計畫）。
  - **方案 A（推薦）**：7 段機械搬入 `references/step-*.md`（byte 不變）：Pitfalls(23.8KB)、Step 9 操作細節(11.7KB)、Support files(15.1KB)、Step 6D、Contract A、Step 10、VERIFY_ONLY → 主檔 ~38.5KB。
  - 主檔必須留 inline：When to use / Architecture+Execution invariants / Routing decision matrix / **Step 9-0 + 9-0a 全文**（fda-desktop-automation skill 以「Step 9-0a」名稱引用，header 不能消失）/ RP-002 status。
  - 新增 `## Routing map` 段：操作類型 → 載入哪個 references 檔。
- 工具位置：`scripts/skill_guard.py`（較新，含 lesson 註解）vs `var/fda/skill_guard.py`（較舊副本）；ref regex 只吃 `[a-z0-9-]+\.md`（新檔名全小寫+連字號）；`skill_split.py` 不存在，執行期需建置（manifest-driven 機械搬移器）。
- **禁止反模式**：`var/fda/slim_hgk_skill.py`（s.replace 直壓內文的手動瘦身腳本）——勿沿用，拆分一律機械搬移。

## 執行前置（Gate 2 用戶確認後）

1. Gate 2 確認方案 A（或 B 保守 3 檔）
2. 建置 `scripts/skill_split.py` + 驗證腳本（T2-T6）
3. `skill_guard pre`（預期僅 SIZE BLOCKED）
4. Dry-run on copy（var/a2/wt-skill-split/）→ T1-T6 全 PASS 才進真目錄
5. 套用（新 references 檔 + 新主檔原子替換，縮短並行窗口；spine lease 寫鎖）
6. 驗證 T1-T6 + 冷啟動 canary C1-C3（fresh leaf：FDA 授權判定 / EVIDENCE_GAP 閉環 / XQ 卡死 → 各應經 Routing map 載入正確 references 檔）
7. 收尾 + 單一證據 MD + 3-root mirror
