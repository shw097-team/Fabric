# HG-KSEOS（冷啟動入口 / Landing Page）

> 本文件是新 Hermes / GPT / operator session 的冷啟動入口頁，不是 normative authority。
> 治理規則、權威來源與施工細節以 `AGENTS.md`、`docs\HG-KSEOS使用說明文檔.md`（User Guide）與 `control\` 工件為準。
> **Current claim**: `HG-KSEOS_LOCAL_DELIVERY_PASS — EXTERNAL FINAL ACCEPTED`（保留，不重寫）。
> **A-3 delta claim ceiling**: `HGK_SQS_A3_OPERABILITY_STEERING_READY`（never production / live / remote）。

## 1. 這是什麼

HG-KSEOS 是受治理的多閘門本機交付系統（governed multi-gate local delivery system）：把「使用者目標 → 來源 → 需求 → 設計 → 計畫 → WorkOrder → 實作 → 測試 → 修補 → 獨立驗收 → reducers → local delivery」整條鏈路自動化，並以 immutable evidence、independent checker 與 fail-closed 閘門維持可稽核性。所有 canonical mutation 都必須走 typed Shared Spine API 並發出 immutable event 與 evidence / rollback reference。

## 2. 角色與控制面

- **HGK（HG-KSEOS）= 唯一 governance / normative / WorkOrder / evidence / release control plane**：authority、admission、checker、reducers、release 都由 HGK 擁有。
- **Hermes = governed runtime / orchestration plane**：Kanban、`/goal`、SessionDB、checkpoint、tool recovery、compression、approvals。
- **Codex CLI = primary bounded executor**：tracked implementation 的 bounded writer，只寫 admitted writable root。
- **SQS-THC = financial domain stack**（`C:\Projects\Agent_Workspace\SQS-THC`）：在 HGK governance 之下運作，不建立第二 control plane。

## 2a. 控制平面能力（current，engineering-base 已實作）

以下兩項為受治理的 engineering-base ChangeSet，已實作、測試並經獨立驗收：

### 2a.1 Canonical acceptance resolver（`HGK-EBC-ACCEPTANCE-RESOLUTION-001`）

- `SharedSpine.resolve_acceptance(...)` ＋ `TRANSITIONS['acceptance']`：acceptance 的 canonical transition 由 **SharedSpine / domain owner** 執行。
- 保留 canonical event / audit trace；`subject` / `evidence` binding **fail-closed**；stale / conflicting 一律拒絕；identical replay **idempotent**；transaction **atomic**。
- **禁止 consumer 以直接 SQL bypass domain API**（spine 自身的 repository / transaction 實作仍可依既有架構使用內部 persistence SQL）。
- 測試：`tests/test_acceptance_resolution.py`。

### 2a.2 Ordering oracle（`HGK-EBC-ORDERING-ORACLE-001`）

- **排序一律用隱式 `rowid`（單調插入序），不得用 wall-clock `created_at`。** `created_at` 只有秒級精度，同一秒的兩列會讓排序決策變成任意。
- 已修正的四處：`lifecycle.py` checkpoint 的 current-workorder 選擇（＝ admission 序，最關鍵）、`lifecycle.py` 近期 transitions、`knowledge.py` memory 記錄、`evidence_graph.py` 的 qualified 形式。
- Guard：`tests/test_ordering_oracle.py`（含 source 掃描 + 分歧證明）。
- 前例：`evidence_graph.py` 既有的 `ORDER BY rowid`。

## 3. Canonical Root 與檔案位置

- **Canonical root**: `C:\Projects\Agent_Workspace\HG-KSEOS`（HG-KSEOS 的 canonical product/control root）。其他 root（如 SQS / Fabric）可由 WorkOrder 另行 admitted；不代表整個系統只有一個 writable filesystem root。
- **`docs\HG-KSEOS使用說明文檔.md`** = full User Guide（Part I-VIII，含 §31c A-3 Operability Delta）。
- **`AGENTS.md`** = repository 級指令（governed execution 規則）。
- **`control\`** = governance artifacts（RBWI/WP 控制工件）。
- **SSOT packs**（P0-CIP / 實作前開發文檔包）目前位於 `C:\Projects\Agent_Workspace\知識庫\HG-KSEOS_SSOT`（source-resolved；以 fresh-read 為準）。
- **construction-acceptance-prompt-compiler**（compiler skill 套件：SKILL.md + steering profiles + tests）目前位於 `C:\Projects\Agent_Workspace\知識庫\實作相關DOC\HG-KSEOS\construction-acceptance-prompt-compiler`（source-resolved；以 fresh-read 為準）。

## 4. 如何驗證 canonical Hermes 綁定

```text
'C:\Users\user\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe' --version
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\hermes-core.ps1 -Action Verify
```

預期：`Hermes Agent v0.20.0 (2026.8.3)`，commit `3c27eb6234bf91b8ceee9e9071591b31e9b148cb`（`config/hermes.json` `HGK-HERMES-BINDING/2`）。

## 5. Doctor / 健康檢查

```text
PYTHONPATH=C:\Projects\Agent_Workspace\HG-KSEOS\src '.venv\Scripts\python.exe' -m hg_kseos --root 'C:\Projects\Agent_Workspace\HG-KSEOS' doctor
```

健康 = `blocking` 為空且 `verdict` 為 `PASS`。

## 6. 普通任務入口

普通任務（含 SQS）一律走 SharedSpine typed admission：register requirement → freeze → taskspec → workorder（`writer=codex`）。精確 API 序列見 User Guide §31c（A-3 Operability Delta）。不允許 bypass WorkOrder 直接實作。

## 7. 自動路由概念

HGK router 依任務形狀做 deterministic 分類（不手動強迫）：

- **Direct** = small atomic task（bounded execution，不強迫 card）。
- **Kanban** = durable / cross-role / restart-surviving（Hermes Kanban，thin adapter）。
- **Swarm** = 獨立平行 lane（同一 control plane 下 admission）。
- **Codex** = tracked 實作（bounded executor；每個 admitted writable root 只有一個 writer）。

## 8. 邊界

- **RP-002**（`HGK-REFERENCE-PROJECT-002`）= 目前 state `SELF_HOSTING_CUTOVER` / `FROZEN_PRESERVED`：有 prior historical execution / partial self-hosting history；不得 mutate。勿從本 README 推斷下一個 executable gate；任何 RP-002 執行前，fresh-read 目前 RP-002_v2.0 blueprint/handoff 與 current state。本 README 不宣稱 RP-002 PASS。
- **Knowledge K1 / KG1 治理** = `DEFERRED_TO_RP002`。
- **Production** = `NOT_CLAIMED`（local delivery PASS ≠ production authorized）。
- **SQS live trading** = `NOT_AUTHORIZED`（LOCAL / PAPER / NO-LIVE-WRITE default）。
