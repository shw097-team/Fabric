# SESSION 結案：FHS vNEXT W1 R2 施工／發行，W2 藍圖草案

**日期**：2026-11-14　**工作根**：`<WORKSPACE>\FHS_NEXT` ＋ `…\FHS_NEXT_Workspace\W1_R2_CONSTRUCTION_20261114`
**身分**：FHS_NEXT 工作 profile（W0 級：source-bound 施工、在地檢查、作者設計；不得自簽原生／獨立／發行以外之狀態）

---

## 一、本 SESSION 的最終狀態（逐項實測）

| 標的 | 狀態 | 落點 | 實測依據 |
|---|---|---|---|
| `FHS_vNEXT_PLP_W0` | `W0_SCOPE_COMPLETE` | `FHS_NEXT/deliverables/FHS_vNEXT_PLP_W0/` | `CURRENT.json` 可讀；本輪未動 |
| `FHS_vNEXT_PLP_W1` | **`RELEASED`**（r2） | `FHS_NEXT/deliverables/FHS_vNEXT_PLP_W1/`＋產品 repo main＋Fabric main | `verify_current.py` → `drift: []`、`PASS`；`ops/selfcheck.py` 16/16 |
| `FHS_vNEXT_PLP_W2` | **`CANDIDATE_NOT_APPROVED`**（藍圖草案・實質正文） | `FHS_NEXT/deliverables/FHS_vNEXT_PLP_W2/` | `CURRENT.json` 兩件 sha 回讀 OK；`open: [A7]` |
| L0／L1／L2 回寫 | 已落筆、sha 一致 | 知識庫 FHS 文件集 | `docs/WRITEBACK_LEDGER.json`；`build/asset_audit.py` 重算 live sha = ledger |

## 二、資產層級稽核（回答「有沒有放錯層」）

`build/asset_audit.py` → `out/ASSET_AUDIT_2026-11-14.json`，判定 **`ALL_PRIMARY`**（3 標的、0 FAIL、`round_only: []`）。

- **主用層**：W0（`W0_SCOPE_COMPLETE`）、W1（`RELEASED`）。W1 三件簽章綁定物 ＋ 5 件補充交付皆在主用層，逐檔 sha 由 `verify_current` 檢核。
- **候選層**：W2 依 owner 裁決以「藍圖草案・實質正文」身分存在，`not_claimed` 明列 `W2_EXECUTED`／`W2_SPEC_APPROVED`。**沒有一件已過審內容被放進候選層或可棄層。**
- **本輪發現並修正的真實錯放**：五件 W1 成文交付（`W1_REPO_ENTRY`、`WP11_HOST_PLAN`、`WP07_COMMANDER_ABC`、`CLOSEOUT`、`DELIVERY.json`）原本**只存在於輪次資料夾**，未進主用層——已升格為 `supplementary/`（43,051 bytes），並以 `SUPPLEMENTARY_INDEX.json` 明確標示「**不在** owner 簽章綁定的三件之內」，避免冒充簽章集。
- **取代關係**：舊 `W1_R2_CONSTRUCTION_PACK_2026-11-14.zip` 由 r2 交付包取代（成員 sha 相同、改為交付名），記於 `supplementary/SUPERSEDED.json`，不再對外散佈。

## 三、工程衛生（724 → 506 檔，53.0 → 47.7 MB）

`build/hygiene.py` → `docs/HYGIENE_2026-11-14.json`，每一筆刪除都記「理由＋刪除前 file/bytes/manifest_sha256」：

| 動作 | 標的 | 理由 |
|---|---|---|
| delete | `build/__pycache__` | 建置殘留，可重建 |
| delete | `out/_m.json` | 暫存 stdout 捕獲（已在 manifest 宣告 volatile） |
| delete | `sbx/`（212 檔、5.19 MB） | 探針複本與變異沙箱，屬可重建暫存 |
| archive | 2 份 foreign dispatch log | 他人寫入、從未採用為本輪證據，移入 `_archive/foreign_logs/` |

**必須講清楚的代價**：`WRITE_MANIFEST_APPROVED` 的 352 檔中有 212 檔位於 `sbx/`，退役後**不再可逐檔回讀**。已寫 `out/SANDBOX_RETIREMENT.json`（逐檔 path/bytes/sha 清單）並在 `WRITE_MANIFEST_APPROVED.json` 加 `retirement` 註記；量測結論由 `out/` 收據承載，W1 交付物與發行不受影響（`verify_current` PASS 可證）。可重跑 `build/wp05_*`、`build/wp17*` 重建，但時間戳不同，不視為同一證據。

## 四、W1 交付與發行（實測數字）

- 正文 r2：`120,834 bytes`／`sha256 a704a962…`；base r1 `115,090 bytes` 位元保留於 offset 4,366、CRLF 0
- 附錄 r2：`10,946 bytes`／`33cb2637…`；交付包 r2：`88,513 bytes`（9 成員，CRC 與成員 sha 逐檔回讀）
- 驗收：十輪 VERIFY，最終 `APPROVE_RELEASE_CANDIDATE`；失敗集合 `3→1→1→1→1→1→0`（單調不增）
- 回寫：三輪，僅 R3 `WRITEBACK_QUALIFIED`；L0 `365,153→368,440`、L1 `7,256,694→7,259,405`、L2 `2,759,509→2,763,972`
- 發行：owner 口令窗 `WIN-fa49502ba14d`、`signature_verified=true`、payload `63429de9…`、狀態 `RELEASE_GRANTED`
- Repo：Fabric PR #60 `14e3d497`、#61 `75dbc725`、#62 `9c529cba`；產品 repo `shw097-team/FHS_vNEXT`（private）main 已含 `RELEASED` 現況與 5 件補充交付

## 五、本 SESSION 未主張、未完成

- **未主張**：`NATIVE_SIGNED`、`INDEPENDENT_PASS`、原域接受、跨波接收方簽收（`DELIVERED_NOT_RECEIVED`）
- **W2 A7 未過**：24 輪迴圈，A1–A6／A8–A10 長期 PASS，A7（驗收門可執行）仍有缺口；停在上限屬預先寫定的治理條件，續跑需 owner 一句話
- **原生准入**：記 `NATIVE_ADMISSION_UNPROBED`（三支探針：`file_missing`、argparse 例外、`ERR_GATE_NO_INPUT_DIGEST`），不得寫成「已拒絕」或「已准入」
- **四工具**（GSTACK／MATT／GSD／Spec Kit）：均未安裝；依藍圖不屬 W1，GSTACK 為 W3 受限試點、Spec Kit／Matt 資格化後 default-on、GSD 卡來源 pin／license
- **分支保護**：`PUT /branches/main/protection`、`POST /rulesets` 回 403（fine-grained PAT 缺 `Administration: write`）；owner 已裁定 repo 狀態為最高裁決，**不列缺口**

## 六、證據索引

| 主題 | 路徑 |
|---|---|
| 交付與現況 | `FHS_NEXT/deliverables/FHS_vNEXT_PLP_W1/{CURRENT.json,MANIFEST_W1.json,verify_current.py,supplementary/}` |
| 發行 | `…/W1_R2_CONSTRUCTION_20261114/out/{RELEASE_BODY_FHS_vNEXT_PLP_W1.json,RELEASE_RECORD.json}` |
| 稽核與衛生 | `…/out/ASSET_AUDIT_2026-11-14.json`、`…/docs/HYGIENE_2026-11-14.json`、`…/out/SANDBOX_RETIREMENT.json` |
| 裁定與更正 | `…/docs/{OWNER_RULINGS_W1R2.json,CORRECTIONS.json,WRITEBACK_LEDGER.json}` |
| W2 候選 | `FHS_NEXT/deliverables/FHS_vNEXT_PLP_W2/{CURRENT.json,MANIFEST_W2.json,W2_PROGRESS.md}` |

## 七、一句話

**W1 已受界施工、受審、回寫、並由 owner 親簽發行，全部落在主用層；W2 是尚未過審的藍圖草案，被正確地放在候選層；本輪產生的暫存已按生命週期清理並留下可稽核紀錄。**
