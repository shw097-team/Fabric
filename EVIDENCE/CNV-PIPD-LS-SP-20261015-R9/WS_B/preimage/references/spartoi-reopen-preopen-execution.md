# Spartoi 收盤後/開盤前執行（RUNBOOK&WI v2.0.0 + P1 執行手冊 v2.1.0）

> 建立 2026-08-20（W34 資格 run 實證）。任何 resume 此 Spartoi run 或跑日級/盤中流程的 session 先讀本檔。
> 權威：Spartoi RUNBOOK&WI v2.0.0 → P1 執行手冊 v2.1.0（SF-00~SF-31 主鍵），under TW-ICT_FSDT-Stack 治理。

## 文件位置

- RUNBOOK&WI v2.0.0 / P1 v2.1.0：
  `知識庫\SQS-THC資料庫\TW-ICT_FSDT-Stack設計開發\【2】台股當沖隔日沖流程\【2】(舊版)Spartoi｜台股當沖隔日沖\`
- 治理四文檔：`知識庫\SQS-THC資料庫\` 下
  `TW-ICT_v3.0_專業技術文檔`（DOC-05 = Universe/Candidate/MTF Bias/Scenario 權威）、
  `ICT&SMC_專業技術文檔`、`台股當沖_專業技術文檔_v3.0`、`市場資訊&台股趨勢_專業技術文檔_v2.0`(DOC-01 five-clock)。

## 「收盤後、開盤前」SF 對應與交付物

| SF | 名稱 | 時相 | 交付物關鍵欄位 |
|---|---|---|---|
| SF-13 | 盤後復盤(13:30~) | 收盤後 | daily_report.json(KPI) / weekly_report.json(週五) / feedback_to_method.json |
| SF-14 | 資料管理 | 收盤後 | version_manifest.json（/spartoi_flow/{week}/ 與 /dayflow/{date}/ 落盤） |
| SF-01 | 週級分析 | 收盤後→週末 | weekly_pack.json：bias_w(PWH/PWL/direction/confidence/targets/invalidations)、W-DR/EQ50、W-LQ、weekly_list(15-35檔)、four_cards(4張)、event_flags |
| SF-02 | 盤前分析 | T-1 20:00前草案/T 04:00後定案 | daily_pack.json：bias_d_draft/final、D-DR/EQ50、IL/EL、A_list(≤16)、S1_candidates(6-10)、story_card_final |
| SF-03 | 盤前選股(08:30-09:00) | 開盤前 | S1_final_list.json(6-10)、xs_watchlist.xs、preopen_risk_report.json |

Runbook §2.1 時序：週五盤後 SF-01 → 交易日盤前 SF-02→SF-03 → 盤中 SF-04..12 → 盤後 SF-13→SF-14。
SF-00/15/16/17 貫穿全程；SF-11 收尾(13:10 禁新倉/13:20 強清)、SF-12 對帳 ROD-only。

## 實跑方法（資料層真實執行，非模板）

- 資料源：`SQS-THC\data_plane\data\backtest.duckdb` → daily_bars（258 TWSE）。
  duckdb/site-packages 在 `SQS-THC\.venv-data\Lib\site-packages`；asof/known_at 是保留字需引號。
  Python: `C:\Users\user\AppData\Local\Programs\Python\Python311\python.exe`。
- SF-01 計算位：bias_w 用等權廣度(advance_ratio)、PWH/PWL=前窗 high/low mean、W-DR EQ50=(hi+lo)/2、
  weekly_list=流動性前 30(15-35 內)含 script_score-W/risk_tags。Bias 判定：
  mean_ret>0.5%且up>dn→BULL；<-0.5%且dn>up→BEAR；否則 MIXED/RANGE。
  **實證注意**：資料窗 mean_ret≈+1.54%、up155/dn99 → BULL/MEDIUM（不要憑印象報 MIXED，
  一定要重讀 weekly_pack.json 實際 bytes 值；獨立 lane 抓出此摘述錯誤，屬 status-marker 紀律）。
- 誠實界線：SF-03 preopen(平衡價/委比/量)需 Q2/XQ live → 資格 run 用 daily-close proxy 並標
  `qualification-proxy`；SF-13 KPI 無實盤執行則 N_A/structural；不得把 proxy 當成交。
- 目錄：`SQS-THC\var\spartoi-preopen\{spartoi_flow,dayflow,archive}\`（gitignored run area）；
  evidence primary home = `SQS-THC\evidence\spartoi-preopen\`（Step 6B team evidence）。
- 覆蓋證明：`SPARTOI_PREOPEN_RUN_COVERAGE.json`（SF deliverables + artifacts index）。

## 陷阱 / 教訓

- 資料層停在 8/13（NO_CHANGE）就別硬推：分析基準週以資料內最後完整週為準，誠實標 as_of。
- polars `.pl()` 後 column name 別 alias 錯（`r` vs `w_ret` 欄名不一致會 ColumnNotFoundError）。
- 週五才出週報；非週五出 structural weekly_report 要標 week_ref。
- version_manifest 只列 runtime deliverables，排除 executor .py/自身 — AO 誠實標記 observation
  非 blocker；可在 manifest 加 tool_code_note 閉合。
- 單一 evidence MD + 三 root（HGK/SQS/FAB evidence\review\spartoi-preopen）byte-identical 鏡像。

## 誠實 PASS ≠ 交付物齊全（2026-08-21 FAR 教訓，critical）

- **AO/驗收的 "PASS" 驗的是「誠實不變量 + 資料對帳」**（無 live/fill/broker_write、sim_clock、SF-14 hash 相符），
  **不是「每個 SF JobCard 的完整輸出已交付」**。兩者是不同 claim，不可混為「全部 SF 做完」。
- 判斷某段實跑是否「完整」必須**逐一載入 canonical JobCard 的 Required Outputs/Artifacts 逐卡比對**，
  不能只看 AO verdict 是 PASS 就宣稱完整。實例：前次「Q1–Q4 done」僅是薄決策鏈子集 → 0/18 JobCard 完整。
- 全量補齊模式：`SQS-THC\var\rbwi-fullrun\full_jobcard_executor.py`（SF-00..17 一次產 18 收據）+ Spartoi
  `full_intraday_supplement.py`（SF-04..12）+ 自檢 `check_full_jobcards.py`（逐卡 DONE/PARTIAL/MISSING）。

## 週五盤後 = 真實（非 SIM）週級/復盤流程的正確時窗（2026-08-21 實證）

- **本週最後交易日收盤後，依 RUNBOOK 應跑「真實」SF-01 週級分析 + SF-13 盤後復盤**（非 SIM），
  目的：產出當週 weekly_pack（bias_w/W-DR/W-LQ/weekly_list/four_cards）以做**下週首個交易日開盤之真實準備**。
  （Spartoi RUNBOOK 明文：SF-01 週級分析 = 每週五盤後至週末；SF-13 = 13:30~。）
- **週五盤後應主動執行，勿等人問**——不要只因「本週無 live 交易」就整段退回 SIM 或留白；盤後/週級/盤前是
  資料層真實流程，應以當日真實收盤資料執行。並把「開盤 ready」分為「準備框架 ready（交付物+資料+XQ/路由已具）」
  與「完整 live 實跑 ready（需開盤段 live + FDA + HITL）」兩者皆誠實陳述。
- 執行位：`SQS-THC\var\spartoi-preopen\real_postclose_weekly.py`（真實當週收盤 → 週級包，REAL_POSTCLOSE 模式，
  evidence/…/real_postclose/）。8/xx 收盤資料當日 TWSE 即發布，`bf.update_incremental(today=<date>)` 可取得。
  **TWSE 日期為「民國 115/08/21」格式**，比對須 `any(r[0]=='115/08/21'…)`，勿用西元字串誤判為「無 8/21」。

## 閉環契約（Step 9/6C）

- 每個 Spartoi WorkOrder-bearing round 都要：fresh-context AO VERIFY_ONLY lane → 單一 MD →
  mirror 三 root → 誠實 claim ceiling（production/live NOT offered）。
- Q2-Q4/live 前置：SF-03 真實 preopen + XQ/XS 操作 → 需 live 市場 window + HITL-APPROVAL/1。
