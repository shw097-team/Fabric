# SQS-THC 知識庫文檔研究：method/ICT 內容定位與解析慣例

用於 SQS-THC 知識庫（`C:\Projects\Agent_Workspace\知識庫\SQS-THC資料庫\`）的唯讀研究子任務。
目標：快速定位「方法/策略流程」與「當沖/ICT 技術參考」內容，避免在文件內無腦掃全文。

## 文檔結構慣例（重要——兩種格式不通用）

該知識庫的 markdown 有**兩種結構**，解析方式不同：

1. **RBWI 式**（TW-ICT_RBWI、TW-ICT_FSDT-Stack 藍圖、DOC 系列）：標準 markdown `##`/`###` heading。
   - 用 `grep -nE "^#{1,3} "` 可直接抓 TOC/章節地圖。
   - RBWI 本身有 canonical object registry（OBJ-###）與 registry 表（MTH-、CMP-、GATE-、SF-##、W-##、D-##），可用 `grep -niE "OBJ-096|MTH-00|SF-01|MethodChange"` 定位。

2. **Spartoi 式**（Spartoi RUNBOOK&WI v2.0.0、Spartoi P1 執行手冊 v2.1.0）：**沒有 markdown heading**。
   - 頂層用 `§N` 段標 + `[ANCHOR:XXX]` 錨點（如 `[ANCHOR:RW-V200-S7-METHOD-SLOT]`、`[ANCHOR:SFHB-V2-07-SF05]`）+ 表格欄位（`欄位/內容`）結構。
   - `grep -nE "^#{1,4} "` 對這些檔案**回傳空**，不是檔案壞掉，是本來就沒有 heading。
   - 正解：`grep -nE "ANCHOR:|§7|附錄A|CA-METHOD|SF-01|ICT-M###"` 抓錨點/關鍵詞列號，再用 `read_file offset=` 精讀。

## 三份關鍵文件與內容地圖

| 文件 | 方法流程節點 | ICT/當沖技術參考 | MethodCard 產出 |
|---|---|---|---|
| TW-ICT_RBWI_v3.0.0_r2 | §6 Slow Loop / MethodChange 契約（L264-372）；§22.1-22.4 Method/Operation Contracts + Setup Qualification（L3909-3967）；SF JobCards SF-01/02/05/06/09 | §4 來源清冊：TW-ICT DOC-00~11、ICT股票分析總表、Spartoi 二檔（MIGRATION_BASELINE）；§22.2 MTH-001~012 | 用 **MethodSpec**（OBJ-096）承接，不用「MethodCard」名稱 |
| Spartoi RUNBOOK&WI v2.0.0 | §7 方法欄位佔位規則（L2211-2251）；方法草案→定案（L994-1007：c 制定→f 回測定案）；CA-METHOD 子系統（L811-813） | §7 ICT-M001~107 鍵位引用 #1~#107；附錄A Crosswalk SSOT（107 條）、附錄B Conflict Ledger、附錄C；聲明「ICT 模組僅佔位、不作教學/發明」 | §5/§7.1 MethodCard（方法卡），Legacy Slot Key 雙層命名；PLACEHOLDER→BOUND 須 CA-METHOD + SEM³ 驗證 |
| Spartoi P1 執行手冊 v2.1.0 | SF-05 CA-METHOD（L923-964）組裝方法卡；SF-06 CA-BACKTEST（L967-1010）；SF-04 CA-DSL；preflight 08:55 缺 methodcard 禁交易（L700-721） | APPX-A（SF→#1-107）、APPX-B（流程節點→ICT 全項目）、APPX-C Crosswalk SSOT（Table C-1/2/3 + crosswalk.json） | /spartoi_flow/method/methodcards.jsonl（schema methodcard.schema.json），≥3 行/每卡 time_window+time_invariants_handling |

## 關鍵差異 / 易踩雷
- 「MethodCard 產出規範」**只在 Spartoi 家族**；RBWI 用方法上更嚴格的 MethodSpec/NamedModelCard 契約。比較兩者時別直接把術語對等。
- RBWI §4 來源清冊**未逐條列出**獨立的 `台股當沖_專業技術文檔_v3.0` 系列（只寫「台股當沖 candidate corpus」與 DOC-00~11）。若任務要求精確對位該系列，需另外到 `台股當沖_專業技術文檔_v3.0\` 目錄確認，別以 RBWI 清冊為準。
- Spartoi 檔內很多欄位是「表格（`欄位<tab>內容`）」而非 list，`read_file` 直讀比逐行 grep 更快看懂。
- 文件很大（RBWI 約 1.1MB / 10269 行）：先用 TOC/grep 圈定行號段，再 `read_file offset=` 精讀，不要整檔讀。

## 產出契約
此類 FAR 研究子任務的輸出是 JSON：`{source_family, findings, has_method_workflow, has_daytrading_reference, summary, quote_locations}`；`quote_locations` 附「檔案路徑 + L行號段」以便 parent 直接回驗。強調結論（outcome-first），不要 replay 過程。

> 若任務點名 **FSDT-Stack DOC 系列（DOC-29/27/28）或 TW-ICT v3.0 DOC-05/14**，另載入姊妹檔 `fsdt-stack-doc-series-research.md`：該家族 DOC 分工地圖、真實檔案根（`C:\Projects\Agent_Workspace\知識庫`）、ICT 1~107 法律地位、與「方法定案在 DOC-14 Slow Loop / 執行鏈在 v3.0 DOC-05」的速答。
