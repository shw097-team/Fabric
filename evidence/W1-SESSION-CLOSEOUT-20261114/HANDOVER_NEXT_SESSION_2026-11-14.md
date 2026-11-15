# 移交：新 SESSION 接手（FHS vNEXT）

**移交時點**：2026-11-14　**移交人**：FHS_NEXT 工作 profile
**接手者請先讀完本檔，再讀 §3 的四份文件。**

---

## §1 三句話現況

1. **W1 已發行**（`RELEASED`）：owner 親簽、`verify_current` PASS、`selfcheck` 16/16、產品 repo 與 Fabric 皆已同步。
2. **W2 是藍圖草案**（`CANDIDATE_NOT_APPROVED`）：未過審、未實作、未交付；唯一未過判準是 A7。
3. **本輪產物已歸位**：已過審者全在主用層（`ALL_PRIMARY`，0 FAIL），暫存已按生命週期清理並留稽核紀錄。

## §2 開工前必做（依既有裁決，不可跳過）

1. 載入 skill：`fhs-w0-source-bound-work`、`governed-review-and-release`。
2. 掛載三角色：**Fabric＝治理契約／SBL＝產品工程入口／HG-KSEOS＝原生授權與驗收控制平面**，各自指出 repo/branch/commit/path/SHA。
3. 確認工作根只有兩個：`<WORKSPACE>\FHS_NEXT`（主用）與 `…\FHS_NEXT_Workspace`（施工現場）。除此之外的寫入都是越界。
4. 讀 `docs/OWNER_RULINGS_W1R2.json`（OD-1…OD-11），**業主裁定優先於藍圖推論**。

## §3 接手必讀（依序）

| # | 檔案 | 讀它的理由 |
|---|---|---|
| 1 | `FHS_NEXT_Workspace/W1_R2_CONSTRUCTION_20261114/deliverables/SESSION_CLOSEOUT_2026-11-14.md` | 本 SESSION 全貌、實測數字、未主張清單 |
| 2 | `FHS_NEXT/deliverables/FHS_vNEXT_PLP_W1/CURRENT.json` ＋ `supplementary/SUPPLEMENTARY_INDEX.json` | 主用層真相：三件簽章物＋五件補充交付 |
| 3 | `FHS_NEXT/deliverables/FHS_vNEXT_PLP_W2/{CURRENT.json,W2_PROGRESS.md}` | W2 候選現況與 A7 缺口 |
| 4 | `…/docs/{CORRECTIONS.json,WRITEBACK_LEDGER.json}` | 本輪所有自我更正（RC-1…RC-21）與回寫事實 |

## §4 三十秒自檢（複製即用）

```bash
PY=<HOST_HOME>/AppData/Local/hermes/cache/scratch/fhs_next/venv311/Scripts/python.exe
cd /c/Projects/Agent_Workspace/FHS_NEXT && $PY deliverables/FHS_vNEXT_PLP_W1/verify_current.py && $PY ops/selfcheck.py
cd /c/Projects/Agent_Workspace/FHS_NEXT_Workspace/W1_R2_CONSTRUCTION_20261114 && $PY build/asset_audit.py
```

期望：`verdict: PASS`（W1，`drift: []`、`supplementary: 5`）／`pass: 16, fail: 0`／`verdict: ALL_PRIMARY`。
任一不符 → 先查 `out/ASSET_AUDIT_2026-11-14.json` 與 `docs/HYGIENE_2026-11-14.json`，**不要**直接動手改主用層。

## §5 可接續的工作（按性質分開，不要混）

| 工作 | 前置 | 起手 | 邊界 |
|---|---|---|---|
| **W2 續審 A7** | owner 一句話（本輪停在上限是治理條件） | `build/w2_loop.py --dispatch`，判準集 A1–A10 **不得擴張** | 失敗集合必須單調不增；連續兩次成長即停；不得自加輪次 |
| **W3 波次施工** | 依 L2 全波次藍圖取 W3 指派 | 建新輪次資料夾 `…\W3_<name>_<date>` | GSTACK 僅受限試點；Spec Kit／Matt 需先資格化；GSD 卡來源 pin／license |
| **原生准入實測** | 需 HG-KSEOS 乾淨拒絕路徑 | 三支探針重跑，只記實測碼 | 取不到乾淨量測就只能寫 `NATIVE_ADMISSION_UNPROBED`，不得推論 |
| **獨立驗收** | 非製造者執行 | 沿用 R1–R10 的 nonce 歸屬＋read-only 車道 | 不得由製造者自判；不得把未回 nonce 的回合當通過 |
| **發行簽章** | owner 口令窗 | `owner_window.py open --scope owner_semantic_accept` | maker 不代簽；一次口令授權該任務全部簽章（OD-10） |

## §6 已裁決、不要再翻的六件事

1. **同模型 checker 不是缺口**（OD-1）。
2. **藍圖可複現性屬證據稽核瑕疵**，不作 W1 PASS 阻斷（OD-2）。
3. **白名單／測試範圍依上游藍圖共識**（OD-3）。
4. **例外只算兩個允許根之外**；`FHS_NEXT` 與 `FHS_NEXT_Workspace` 內不算例外（OD-7）。
5. **Owner 親設 repo 狀態為最高裁決**；分支保護 403 不列缺口（OD-6）。
6. **審查閉集凍結、失敗集合單調不增、空集合即終止**（OD-11）。

## §7 六個 reader receipts

依 `NOT_APPLICABLE_BY_DESIGN` 本不需要；owner 已表明不代簽。**不要**自行補簽或代簽；若未來要簽，只能由 owner 在口令窗內以 `original_reader_ack` 親簽（OD-9）。

## §8 命名規矩（本輪踩過）

- 檔名只描述**身份**，不描述**期望**：未過審不得叫「交付版」。
- 三段命名：**藍圖**（L0/L1/L2）→ **實質正文**（波次體裁）→ **候選版／交付版**（狀態）；W2 依 owner 裁決定名「藍圖草案・實質正文」。
- 檔名與 `CURRENT.json` 的 `state` 必須同時成立；改名要同步改內文標題、打包器、簡報產生器與索引，否則重建會生回舊名。

## §9 禁止事項（會直接毀掉可稽核性）

- 走 Codex 沙盒路由（已被 owner 明確否決）；車道一律直連 relay `127.0.0.1:10101`。
- 代簽 owner 簽章、自判獨立驗收、自行宣告 `RELEASE_GRANTED`。
- 把 `sbx/` 之類暫存當證據引用，或反之把證據當暫存刪掉而不留 retirement 紀錄。
- 用 `robocopy /MOVE` 且輸出重導（曾造成檔案遺失）；移動前先 `/L` 乾跑、留 log 與前後清單。

## §10 接手第一句話建議

> 「接手 FHS vNEXT：先跑 §4 自檢，回報三個 verdict，再依 §5 問我要做哪一項。」
