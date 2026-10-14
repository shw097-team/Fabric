# Independent check — advisory verdict and our own recomputation

> `NOT_EXTERNALLY_ACCEPTED · NOT_MERGED · NOT_RELEASED · NOT_PRODUCTION · NO_LIVE_WORLD_EFFECT`
> Presence of this file, of a verdict, or of a matching digest is **not** a pass.

## 車道

| 項目 | 值 |
|---|---|
| 車道 | `VERIFY 6`（結案複核），經 CODEX CLI 執行 |
| required / served | `opencode-go/glm-5.3-flash` ＝ `opencode-go/glm-5.3-flash`（usage receipt ok） |
| 結果 | `ok: true`、exit 0、**898.51s**、158 個命令、token 置於**訊息最末** |
| 車道自陳 verdict | **`PASS_ADVISORY`** |
| 固定案例 | C1–C6 各出現一次（逐字檢索該車道最終訊息） |

車道自陳的天花板（逐字精神）：本 verdict 只涵蓋交付包的讀取與重算，**不是**任何受測事項的
acceptance，不開啟落地權限，也不修補任何既有失敗。

## 我方對它主張的獨立重算（不採信 maker 或檢查者的自述）

| 它主張 | 我方從原始位元重算 | 結果 |
|---|---|---|
| 交付包 manifest 與 hash 清單一致 | 逐檔重算 sha256 並比對 manifest 與 `HASHES.sha256` 行數 | 相符（v3 快照 610 檔；v5 現為 632 檔） |
| 排除項有紀錄 | 檢查 134 筆排除項是否皆帶原因 | 134/134 有原因 |
| 交付集無憑證 | 對交付集全文重跑密鑰樣式掃描 | 0 命中 |
| 本機 repo 已整理 | 讀 `git status --porcelain` 與提交物件 | 3 個提交存在、工作區 **0** 筆異動 |
| 殘留缺口數字 | 重數 references 檔案 | **94** 檔（90＋4），高於 60 檔警告線 34 檔 |
| 受測體未漂移 | 重數凍結世代列數 | 370 列 |

重算結論：`LANE_CLAIMS_RECOMPUTED_AND_AGREE`。裁決腳本與其輸出隨附於回傳包
（`evidence/adjudicate_verify_6.py`、`evidence/postfreeze/verify6_adjudication.json`）。

## 本車道自陳的限制（公平揭露，不是缺陷）

- 車道所在環境無網路，**未能**從遠端獨立確認 references 清單；
- 未重跑整套 harness 測試；未重數 raw receipt 列數；
- **未**評判語意品質（deliverable 的內容好壞不在其範圍）。

## 一次自我更正（由重算抓到）

references 檔數在本回合自己的紀錄中一度寫成 **95**（我方 harness 的計數變體）；maker 的自算與今日
獨立重算皆為 **94**，故本紀錄以 94 為準，95 更正為歷史數字。

## 何以複核的是 v3 快照

`VERIFY 6` 派送時回傳包為 v3（610 檔）。其後 v4、v5 以 **additive commit** 增補結案集與更名檔案，
並未改寫已複核檔案之語意；v5 的提交位元複驗為 **632/632** 相符
（`PACKET_BYTES_REPRODUCIBLE_FROM_THE_CLONE`）。逐位元比對與匿名重跑命令見
`PUBLICATION-RECORD.md`。
