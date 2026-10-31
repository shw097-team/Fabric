# Fabric 發布事故記錄 — FAR-LANE-REMEDIATION-20261021 分支被其他 session 共用

**記錄時間**：2026-10-21（本回合，FAR-MINIMAX-MANDATE-20261021）
**分支**：`pub/far-lane-remediation-20261021`
**遠端 HEAD（發現時）**：`8fdb9f39124fdd47812a61dd54646a170549307b`

## 兩個真實問題（皆為事實陳述，非推測）

### 問題 1：`b72b02c` 誤提交了 177 個不屬於本回合的檔案

`b72b02c`（上一回合的初始 publish）使用了寬泛的
`git add EVIDENCE/FAR-LANE-REMEDIATION-20261021` 與後續的索引操作，
實際把整個 `fabric-autonomous-research/` 目錄一併納入索引。

該 commit 的頂層路徑分佈（`git show --name-only b72b02c` 的實測）：

| 檔案數 | 路徑 |
|---:|---|
| 177 | `fabric-autonomous-research/runs/...` |
| 30 | `EVIDENCE/FAR-LANE-REMEDIATION-20261021/`（本回合的真正產出） |
| 1 | `INTEGRATION/KNOWN-FINDINGS.md` |
| 1 | `FABRIC/UPGRADE-INDEX.md` |
| 1 | `fabric-autonomous-research/methods/aris-vendor` |
| 1 | `stage/RP002-STAGE-HGK/CF1/vendor/contextforge` |

**也就是說，177 個檔案是別的 session 的產物，被我上一回合的發布動作帶進了證據分支。**
這違反了「只提交本回合聚焦檔案」的原則。

### 問題 2：另一個 session 在我的發布分支上提交並推送

`8fdb9f3` 的作者是 `RP-002 HGK <hgk-rp002@local>`，提交時間
`Wed Oct 21 14:33:03 2026 +0800`（本回合執行期間），內容為
`far(r7): FAR-20261021-023-sbl-r7-residual-closure artifact set`——
即 SBL 施工的產物。

遠端 `refs/heads/pub/far-lane-remediation-20261021` 的 HEAD 現為 `8fdb9f3`，
即**SBL session 的產物已經透過這條分支發布到遠端**。

## 本回合的處置

1. **本回合的 epoch-25 證據不再推到這條分支。**
   改用獨立分支 `pub/far-minimax-mandate-20261021`，基於 `origin/main` (`bcd9104`)。
   理由：與 SBL session 共用一條發布分支會持續造成互相污染，雙方都無法確定自己發布的內容。

2. **本回合對 `fabric-autonomous-research/` 的寫入次數仍然是 0。**
   `8fdb9f3` 是別的 session 的 commit，不是本回合的動作；本回合的
   `SBL-EXCLUSION-NOTE.md` 記錄的是「本回合零寫入」，該陳述仍然成立。
   兩件事必須分開：*本回合沒寫* ≠ *分支上沒有 SBL 內容*。

3. **問題 1 的補救需要業主決策**（本回合不自行執行）：
   - 選項 A：保留現狀（`b72b02c` 的 177 個檔案留在分支歷史中）。
   - 選項 B：重寫分支歷史以剔除那些檔案。這需要 force-push，會改寫已發布的 SHA，
     且 SBL session 已在該分支上工作，重寫會影響它。
   - 選項 C：新分支乾淨發布（= 本回合採用的），舊分支標記為 contaminated，交由業主處置。

   **本回合採 C**，因為它不破壞任何已發布的 SHA、不影響其他 session、也不對別人的產物
   做刪除決定。

## 對「證據可被外部驗收官重算」的影響

`EVIDENCE/FAR-LANE-REMEDIATION-20261021/` 的 45 檔 manifest 本身仍可獨立重算
（上一回合已從遠端 commit 物件庫驗證 45/45 digest 相符）。問題 1 影響的是
「那條分支上還混了別人的檔案」這一點，**不影響** manifest 內 45 檔的完整性。

## 給外部驗收官的明確指示

驗收 `pub/far-minimax-mandate-20261021`（本回合的乾淨發布），
不要驗收 `pub/far-lane-remediation-20261021`（已被 SBL session 共用並推送其產物）。
