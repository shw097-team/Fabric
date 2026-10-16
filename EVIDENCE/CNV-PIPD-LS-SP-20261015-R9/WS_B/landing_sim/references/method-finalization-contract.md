# SQS-THC 方法定案閉環（方案 D pattern）: MethodSpec + BacktestProfile + 策略級回測

> 建立 2026-08-20（方案 D 執行實證）。當用戶要求「把某候選方法/策略依文檔規畫走完
> 草案→回測→自修補→定案」或「新的策略級回測定案」，先讀本檔再動手。
> 權威：SQS-THC 工程 DOC-02(D02-OBJ-007 MethodSpec)、DOC-07(WF-09→10→11→08)、
> DOC-09(CH24.4 BacktestProfile)；方法權威分層為 TW-ICT v3.0 DOC-05 + FSDT-Stack DOC-14/20
> 主、Spartoi(CA-METHOD/MethodCard) 為支持層（見 far-method-workflow 關聯）。

## 三階閉環（A→B→C 依序，皆 product code writer=codex）

| 階 | 契約 | 產出位置 (tracked tree) | 關鍵 |
|---|---|---|---|
| A | 方法定案契約 | `src/kernel/method/method_finalization.py` + `schemas/method-spec.schema.json` | MethodSpec states `DRAFT→VALIDATED→ADMITTED→SUSPENDED→RETIRED`；WF-09→10→11→08 **不可逆**；`CEILING=RESEARCH_ONLY`；non-owner write reject |
| B | 回測 profile | `src/kernel/method/backtest_profile.py` | `DRAFT→VALIDATED→ACTIVE`，VALIDATED→ACTIVE 需 **G06/G09/G11**；**雙引擎 parity**（screening vs reference replay，reference 為最終基線） |
| C | 策略級回測 | `strategy_runner.py` + `strategy_backtest.py` → `BACKTEST_RUN_RECEIPT_*.json` | 純函數信號+PnL（無 I/O/broker/network）、IS/OOS walk-forward、TWSE cost（fee 14.25bp / tax 30bp / slip 5bp）、deterministic |

MethodSpec required schema fields：`hypothesis, inputs, transforms, parameters, assumptions, invalidation, capacity, cost, owner`（另加 method_id/version/state/ceiling）；`additionalProperties=false`。WF-08 只產 `DECISION_COMPILED`，**不得 mint MethodCard**（DOC-07 L76）。

## 誠實負 PnL 紀律（本 session 實證，最重要）

- 回測「跑完」≠ 策略「有效」。**若實測 IS/OOS PnL 為負，維持 `RESEARCH_ONLY`**，不因流程跑完而自升 VALIDATED/ADMITTED。
- 收據 JSON 要放 `honest_interpretation` 區塊：empirical_outcome（實際 PnL / win rate）、
  verdict=RESEARCH_ONLY、note="流程有效性≠策略獲利性"。
- **不得 silent overfit-rescue**：不能為了把負 PnL 調正而暗中改參數。策略參數需實驗→走
  Slow-Loop Method Engineering Change（DOC-14/20），不是直接調參救。
- `positive PnL != acceptance`（DOC-09 硬規則）；無 live order / broker write。

## 執行表面（全啟用）

- **KANBAN**：每階段一張卡（D-A/D-B/D-C/D-X），claim→complete。
- **SWARM 多子代理**：deleg 雙 lane 並行驗收 —— lane1 方法契約（MethodSpec/WF/BacktestProfile/schema/test）、
  lane2 資料層重算（duckdb 重跑 + PIT + deterministic + IS/OOS 比對）。fresh-context。
- **GSTACK / OPENSPEC**：route check 記錄 `selected_route/reason_code`；本類為新增 method 模組
  （非既有 spec brownfield）→ OpenSpec `N/A_with_reason`。
- **CODEX**：writer=codex（danger-full-access + 窄 prompt）。**若 Codex CLI 因認證 route 失敗**
  （如 `'deepseek-v4-flash' is not supported when using Codex with a ChatGPT account`），
  誠實標 `CODEX_TRACKED_WRITE=NOT_COMPLETED_THIS_RUN`，改 Hermes 起草+實作+全庫 tests 驗證替代；
  **不要偽稱 codex 已寫、不要偽造 provider receipt**。

## 測試基線注意

- SQS suite 必須 `PYTHONPATH=src`（`python -m unittest discover -s tests -t .`）。
  沒帶 PYTHONPATH 會出現 199 tests / 5 ImportError（`No module named 'kernel'`）——那是誤判不是真失敗。
- 新增 method 測試放 `tests/method/`，**需 `tests/method/__init__.py`**（無則 loader 找不到 module）；
  `cp` design test → tracked tree 時遇目標目錄不存在會靜默失敗，拷完要 `ls` 確認落檔。
- 本輪：原 231 + 新增 13 = **244 tests OK** 才可宣稱基線無破損。

## CRLF / 中文路徑陷阱（本 session 兩次踩到，維護 skill references 時必看）

在 CRLF 行尾的 `.md` 檔用 patch 工具改含長中文/反斜線路徑時，路徑可能被斷在 CRLF 邊界
（實例：`evidence\rbwi-fullrun` → `evidence\r\nbwi-fullrun`，fuzzy matcher 持續 re-match 壞序列）。
- **不要重複 patch 同字串**（第二次仍用舊 index 才失敗）。
- 用 Python bytes-level replace 一次修：
  `raw=open(p,'rb').read(); raw=raw.replace(b"evidence\r\nbwi-fullrun", b"evidence\\rbwi-fullrun"); open(p,'wb').write(raw)`
  （bytes replace 對 CRLF/LF 與跳脫免疫）。
- 用 `repr()`/count 驗證壞序列歸零再繼續；write_file 大 regex 一次替換比逐段 patch 可靠。
