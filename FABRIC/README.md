# Fabric — contract surface（README）

> 本檔是 `Fabric/`（本地）↔ `FABRIC/`（`shw097-team/Fabric` repo）這一層的入口說明。
> **不是** normative authority：權威來源是 `AGENTS.md`、`contracts/`、`control/` 與 `docs/Fabric使用說明文檔.md`。定義衝突時以 contracts / machine truth 為準。

## 這是什麼

Fabric 是 **HG-KSEOS 的 contract surface**：它不擁有 authority，擁有的是一組可被消費的**契約與證據綁定**——policy、contracts、receipts、stage 產物與 review evidence。HG-KSEOS 是唯一 governance / normative / WorkOrder / evidence / release control plane；Fabric 是它被消費的那一面。

## 主要目錄（快速導覽）

| 路徑 | 內容 |
|---|---|
| `AGENTS.md` | Fabric 的 agent-operating projection（讀我順序、硬禁止、evidence quick map） |
| `contracts/` | contract families（可被 HGK 消費的契約本體） |
| `control/` | governance artifacts（RBWI / WP 等控制工件） |
| `rp002/` | RP-002 相關契約與現況 |
| `stage/` | stage 封存 / 移交 / gate receipts |
| `evidence/review/` | 對外 review 用的整合證據（含 byte-identical 鏡射） |
| `docs/Fabric使用說明文檔.md` | 完整使用說明 |

## 鐵則（摘要）

- **agent 只能寫 candidate**；approve / revoke / release 不是 agent 的動作。
- **不寫入憑證**到 Fabric 的 evidence / docs；secret 一律以 env-var 形式 `REFERENCE_ONLY`。
- **不聲稱 evidence 鏈沒有顯示的事**：先讀檔案，再讀綁住它的 receipt，再讀綁住 receipt 的 seal。

## 本輪新增：獨立 checker 升級（candidate）

- **鏡射證據**：`evidence/review/checker-upgrade-20261009/HGK-CHU-20261009_CHECKER_UPGRADE_EVIDENCE.md`（與 HG-KSEOS 來源 byte-identical）。
- **實作整理與上限揭露**：`HG-KSEOS/evidence/checker-upgrade-20261009/IMPLEMENTATION_SUMMARY.md`。
- **綁定規則（重要）**：獨立 checker lane 的 verdict **僅為 advisory** —— **永遠不是 OracleReceipt、永遠不是 canonical acceptance status**，**任何 Fabric contract 都不得把它當成兩者之一來消費**。canonical acceptance 只能由 authorized actor 經 typed transition 產生。
- **誠實狀態**：cutover gate 為 `TEMP_CLOSED/UNVERIFIED`，**非** accepted / released；`hgk_canonical_acceptance: NOT_PERFORMED`。

## 邊界

Stage-1 / Stage-2 的既有封存、歷史 receipts 與原 sealed 產物**不被覆寫**。本 README 只描述現況與入口，不變更任何 contract。
