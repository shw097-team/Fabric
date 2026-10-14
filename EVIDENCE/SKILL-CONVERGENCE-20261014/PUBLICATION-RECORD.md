# Publication record

> `NOT_EXTERNALLY_ACCEPTED · NOT_MERGED · NOT_RELEASED · NOT_PRODUCTION · NO_LIVE_WORLD_EFFECT`
> Publishing is not promoting: making bytes public grants nothing and accepts nothing.

## A. 完整回傳包（現址：本 repo 的分支；曾短暫落在 `shw097-team/PIPD-LS-SP`）

| 項目 | 值 |
|---|---|
| 分支 | `feat/skill-convergence-return-20261014` |
| 最終 tip | `dcdc46295bacd829f1bd1d611f3b478e3646a93e` |
| 內容 | 632 檔／5,540,242 bytes（含全部 lane 逐字稿與 trace、契約、harness、manifest、結案集） |
| 修訂鏈 | v1 → v5，全部為 **additive commit**（未改寫既有檔案語意） |
| `main` | 未移動（`f4021aeff9c016cfb14f17e68a0c570ed4e825c5`） |

**逐位元驗證**：提交位元複驗 `committed_blob_match: 632 / mismatch: 0`，工作樹同為 632/632，
verdict `PACKET_BYTES_REPRODUCIBLE_FROM_THE_CLONE`。
**匿名重跑**：免憑證 clone 後執行入口文件命令 → `files 638 mismatch []`、`scan NO_HITS`
（計數 638／5,558,771／排除 134 一致），verdict `ENTRY_DOCUMENT_COMMAND_SUCCEEDS_ANONYMOUSLY`。

**落點更正（2026-10-14）**：此包最初落在另一個 repo（`shw097-team/PIPD-LS-SP`，分支
`feat/skill-convergence-return-20261014`，tip `e8997254c369957fb8b3a137aacb3c84d9d458ee`）。owner 指出本回合的
落點應為 Fabric repo 之後，本包以**相同位元**改發佈於**本 repo 的分支**
`evidence/skill-convergence-20261014-full-packet`（tip `df411fbd2ff6db2fc1f1b03120756194a9f76b81`，641 檔在樹，
含 `BRANCH-NOTE.md`），並**刪除** PIPD-LS-SP 上的該分支（刪除回應 204、複查 404）。該 repo 的 `main` 全程為
`f4021ae`，未動；被刪除的 tip 其位元與本 repo 該分支相同，仍可復原。

## B. 策展投影 → `shw097-team/Fabric`（本 mirror）

| 項目 | 值 |
|---|---|
| 分支 | `docs/skill-convergence-20261014` → 併入 `main` |
| 內容 | `EVIDENCE/skill-convergence-20261014/`（本目錄）、`FABRIC/README.md` 升級、`FABRIC/UPGRADE-INDEX.md`、根 `README.md` 指標與狀態、`INTEGRATION/MANIFEST.json` 與 `INTEGRATION/KNOWN-FINDINGS.md` 更新 |
| 發布依據 | owner 直接下達的變更指令（mirror §4.5 的 reviewed change-set：分支＋審核清單＋merge） |

## C. 一次目標修正（為什麼這份紀錄存在）

本回合的 Fabric 側整理（`.gitignore`、`HYGIENE_MANIFEST_20261014.json`、首頁/文檔提交）原先**只落在
本機 `Fabric/` working copy**，該 repo **沒有任何 remote**；而回傳包被推到 `PIPD-LS-SP`。也就是說：

- `shw097-team/Fabric`（本 mirror）在本 change-set 之前**沒有**收到本回合的任何實作與證據；
- 本回合早期的結案文字把 Fabric 首頁描述為「已升級」，實際上當時只是**已提交**（把既有 README 納入
  版本控制），**沒有**為本回合升級首頁——本 change-set 補上該節，並在此更正前述說法。

Owner 追問「有沒有把東西堆到正確的 REPO」後，本次檢查（repo 身分、分支、main tip、以及憑證能力的
可逆寫入探測）確認：mirror `main` 停在 `71de521e80470ee1c9a808bf26d42c4eaedf803e`（2026-10-13 發布），
本回合未在其上新增任何 commit。

## D. 憑證處置

- 憑證僅在執行時由 owner 指定檔案讀入，**未**進入 argv、URL、log 或任何提交內容；本紀錄只記長度與
  家族（`github_pat`，93 字元），**值一律 [REDACTED]**。
- 寫入能力以**可逆探測**證明：於 mirror 建立指向既有 commit 的臨時 ref → `201`，隨即刪除 → `204`，
  殘留 ref 檢查為 `404`。探測本身不建立任何新物件。
- 收尾時已刪除本機的臨時 clone 與 credential helper，並確認 helper 檔案不存在。

## E. 本回合的兩起自我揭露事件

1. **v4 的靜默排除**：v4 的 manifest 曾把 `closure/handover/CHECKPOINT_*.md` 列為已交付，但 repo 自身
   的 `.gitignore` 規則把它從 commit 排除；提交位元回讀抓到「blob 不存在」而**拒絕**宣稱可重現，
   v5 以改名修正。教訓已回寫至 `remote-repo-publication` skill（發布前以 `git check-ignore` 逐檔檢查）。
2. **目標 repo 修正**：即 C 段。兩起事件都寫進交付樹內，而不是留在本機草稿。
