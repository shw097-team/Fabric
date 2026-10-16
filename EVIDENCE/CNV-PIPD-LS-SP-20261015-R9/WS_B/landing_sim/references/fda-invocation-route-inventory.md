# FDA 調用路徑與已登記受治理路由盤點（Lane B audit，2026-08-15 驗證）

## 何時用
在 HGK/Fabric/SQS/Hermes 全 stack 中盤點「可能自動調用 FDA（桌面自動化）的位置」與
「既有已登記、會使用 FDA 的受治理路由」（WO/route id + 治理綁定）。
重跑此類稽核（Lane A/C、升級前檢查、guardrail/攔截面驗證、委派到期複查）直接照此路徑搜索。

## 搜索面地圖（每一層都要查，不能只查 repo）
1. **Hermes cron**：`hermes cron list` + 直接讀 `C:\Users\user\AppData\Local\hermes\cron\jobs.json`
   - CLI 只列 active；jobs.json 含 paused/disabled 與完整 prompt/script 欄位（判斷是否引用 FDA/XQ 的唯一依據）
   - executions.db 可查歷史（python sqlite3）
2. **Hermes kanban**：`hermes kanban boards list` + 直接查 `C:\Users\user\AppData\Local\hermes\kanban\boards\<slug>\kanban.db` 的 tasks 表
   - **CLI 的 COUNTS「(empty)」不可信**：2026-08-15 實例 CLI 顯示 fda-* 四 board 全空，DB 實際有任務
     （fda-guardrail-research 7 筆、fda-implementation 7 筆、fda-integrity-check 3 筆、fda-upgrade-research 4 筆，含 WO id 線索）
3. **Hermes skills/plugins/hooks**：`skills/.usage.json`（created_by/last_used 證據）、plugins/ hooks/ desktop-plugins/ gateway-service/ 目錄（通常為空；空本身是結論的一部分）
4. **Windows 排程**：`schtasks /query /fo csv 2>/dev/null | iconv -f UTF-16LE -t UTF-8 | grep -iE "fda|xq|cua"`
   - 原始輸出是 UTF-16，直接 grep 只會得到 `Binary file (standard input) matches`；cua-driver serve 的 `-AutoStart` Scheduled Task 可能註冊也可能沒有
5. **HGK**：control/（agents/prompts/skills/runtime）、config/、registries/、src/hg_kseos/、scripts/、var/fda/
6. **Fabric**：fabric-desktop-automation/（含 governance/、evidence/receipts/）、profiles/、FAR_EXECUTION_BINDING.json
7. **SQS-THC**：adapters/、workflows/、agents/、control/、docs/、STATUS_VECTOR.json、requirements/MC_REGISTRY.yaml、實作執行/CHECKPOINT_CSB.json

## 治理綁定檔（優先讀，別從零推斷）
- `Fabric/fabric-desktop-automation/FDA_EXECUTION_BINDING.json`（BIND/DEL/LS id、issuer/assignee、expires_at、candidate_write_set）
- `WO_FDA_XQ_002.yaml` 等 WO 檔（parent、scope、acceptance_predicates）
- `governance/FDA_ROUTE_CHECK.yaml`（lane route disposition：NATIVE/HITL 等）
- `governance/FDA_DEFERRED_SEMIAUTO_CONTRACT.yaml`（SQS_LIVE_TRADING=NOT_AUTHORIZED、FDA_V1=LOCAL/PAPER/SHADOW/NO-LIVE-WRITE）
- SQS `adapters/xq-read-watch.yaml`（TS-010 唯讀 watch：watch_only/HITL_ONLY/RADAR_ONLY）

## 陷阱（本機實證）
- git-bash **無 sqlite3 CLI**（exit 127）→ 用 `python -c "import sqlite3; ..."` 查 kanban/cron DB
- 全 repo grep FDA 關鍵字會淹沒在 evidence/review 鏡像檔（HGK/SQS/Fabric 三邊 byte-equal 鏡像）
  → 查「程式碼調用點」要排除 evidence/ 或分目錄 grep；control/ 零命中本身是有意義的發現，不是搜索失敗
- kanban「(empty)」≠ 無任務：以 DB tasks 表為準
- **delegation/lease 有 expiry**：稽核時必須檢查 expires_at（DEL-FDA-001 於 2026-08-15 到期）
- 判定「會自動觸發」時連 gateway 狀態一起查：`hermes cron list` 會顯示 gateway 未運行 → 排程根本不會 fire

## 2026-08-15 盤點結論快照（重查時須更新）
- 唯一 active cron = SQS Daily TWSE OHLCV Auto-Update（資料管線 daily_twse_update.py，**非 FDA**）；gateway 未運行
- Windows 無 fda/xq/cua 排程任務（cua-driver -AutoStart 未註冊）
- HGK control/config/registries：**零 FDA/XQ 引用**
- SQS **無 FDA 路由**：workflows/xq/ 僅 .gitkeep；xq-read-watch 為唯讀 watch 非 FDA；CHECKPOINT_CSB `xq_xs: NOT_STARTED`
- 已登記受治理路由：WO-FDA-001（BIND-FDA-001/DEL-FDA-001/LS-FDA-001，board fda-implementation）、
  WO-FDA-XQ-002、WO-HGK-FDA-GUARD-RESEARCH-001、WO-HGK-FDA-UPGRADE-RESEARCH-001、
  WO-HGK-FDA-UPGRADE-INTEGRITY-CHECK-001、FDA NATIVE lane disposition、deferred semiauto contract
- 結論：stack 中**無任何自動觸發 FDA 的排程點**；FDA 執行皆手動、經 fda_run.py + screen_state_check + 雙 skill 路由、
  落在 WO-FDA-001 lineage 之下
- 未受治理風險點：`var/fda/run_codex_router.ps1`（danger-full-access delegation 重跑無防護、綁定僅靠 prompt 內嵌 WO id）、
  var/fda 歷史腳本（bg*.py/dod17_*.py）直接 `python` 執行可繞 fda_run.py guard、SQS workflows/xq 空目錄為未來未綁 WO 路由的潛在位置
