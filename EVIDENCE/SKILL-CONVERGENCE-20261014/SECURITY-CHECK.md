# Security check — advisory verdict, the doubts it raised, and their adjudication

> `NOT_EXTERNALLY_ACCEPTED · NOT_MERGED · NOT_RELEASED · NOT_PRODUCTION · NO_LIVE_WORLD_EFFECT`
> A verdict is not an acceptance, and repairing a lane failure is not something any verdict here does.

## 車道

| 項目 | 值 |
|---|---|
| 車道 | `SECURITY 5`（修正後重派），經 CODEX CLI 執行 |
| required / served | `opencode-go/glm-5.3-flash` ＝ `opencode-go/glm-5.3-flash`（usage receipt ok） |
| 結果 | `ok: true`、exit 0、**211.35s**、6 個固定案例、token 置於**訊息最末** |
| 車道自陳 verdict | **`PASS_ADVISORY`**（附 2 項逐位元疑點） |

## 疑點裁決（由我方從本回合自身的紀錄重算，不採信車道或 maker 的自述）

| 疑點 | 重算方式 | 裁決 |
|---|---|---|
| 凍結世代列數是否與磁碟一致 | 逐列重算 digest 並與磁碟比對 | 370 列、**0 錯** |
| 被併入的 14 個主題檔是否真的位元在位 | 對併入目標逐位元比對 | **全部在位** |
| 候選補丁的每個 patch context 是否真的命中 | 逐一套用檢查（不落地） | **18/18** 相符 |

裁決結論：`LANE_DOUBTS_RECONCILED_WITH_ROUND_RECORDS`。腳本與輸出隨附於回傳包
（`evidence/read_security5.py`、`evidence/adjudicate_security_5.py`）。

## 同 WorkOrder 的前三次失敗（完整保留，未洗成 PASS）

| 派送 | 結局 | 判為 inadmissible 的理由 |
|---|---|---|
| `SECURITY 1` | 完成但未產生 nonce | 無 nonce ⇒ 無法綁定該回合 |
| `SECURITY 3` | 逾時、0 bytes | 逾時 partial-capture 缺陷，無 verdict |
| `SECURITY 4` | `ok: true` 但僅 364 bytes／單一 token | **空答案**（只有 token、無內容）⇒ 不得計為查核 |

依事前宣告的暫停規則，`SECURITY 4` 之後**暫停**該 WorkOrder 並落
`security_workorder_pause.json`，其後在 owner 授權下以修正 brief（token 置末 ＋「至少 N 個命令與
案例 JSON 才算一回合」）重開一次並成功。**暫停不等於把任何安全案例轉為 PASS。**

## 為何空答案會被判 inadmissible

傳輸閘門只證明「這一回合有被送出、且有對應的 usage receipt」，它**不證明**任何受測事項。當 brief
把 token 放在最前面時，一個空回合也能通過閘門——這正是 `SECURITY 4` 的成因，因此 brief 改為
token 置末並加上實質內容門檻。
