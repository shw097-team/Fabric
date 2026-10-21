# FAR-20261016-021 — Decision Question (repo hygiene, front page, README, session closeout)

**Round** `PIPD-REPO-HYGIENE-AND-HANDOVER-20261016`｜**Predecessor** `FAR-20261016-020-s4-final-closeout`
**Class** in-place refresh study over an already-closed deliverable.

## The questions

- **Q1 工程衛生**：`PIPD-LS-SP` 的 repo 樹與本地工作區，現在有哪些**真實**的衛生缺陷？哪些必須修、哪些必須**不動**？
- **Q2 首頁／main 更新**：repo 首頁（root `README.md`）相對 2026-10-16 的實際狀態**過期到什麼程度**？需要的是更新，還是重寫？
- **Q3 README 重構升級**：`README.md` 是否需要「重構升級」？若已重構，重構的第二輪是不是過度工程？
- **Q4 SESSION 結案／移交**：本 SESSION 的結案與移交，應該落在**哪個既有歸宿**，才不會產生第 N 份重複文件？

## Decision criteria（逐條否決權）

1. **低阻力**：能在本地完成、不需新基礎設施、不需 Owner 以外的審批。
2. **高可行**：有可重跑的命令與可重算的證據。
3. **高工程必要性**：不修會造成**真實**損失（工作遺失、外部團隊誤讀、狀態誤判）。
4. **不過度工程化**：**既有歸宿優先**；不新增第二控制平面、不新增目錄家族、不重寫已重構的文件。
5. **對齊上位藍圖與驗收報告**：受《S4 最終獨立驗收報告》§0 STOP RULE 與 §8「**不批准**」清單約束——
   不得為小文案缺陷增設新的 Agent Runtime／全新 CI framework／第九 Skill／大規模 Blueprint 重寫／
   `.hgk` 全量 Git history 遷移／公開 Plugin Directory 施工。

## Pre-committed constraint

裁決**不得**把任何 S4 核心修補重新打開（報告 §0 STOP RULE 五類未命中）；本輪只處理
**文件真實性、本地衛生、結案移交**三類，且**產品程式 0 行變更**。
