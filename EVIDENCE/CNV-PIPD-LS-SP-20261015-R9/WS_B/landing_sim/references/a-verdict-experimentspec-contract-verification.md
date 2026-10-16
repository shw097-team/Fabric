# A判決 × ExperimentSpec 合約獨立驗證（方法定案 evidence/method-finalization）

> 建立 2026-08-21（SQS-THC 方案 B lane2 唯讀驗證實證）。當用戶要求「獨立驗證 A 判決
> (NEGATIVE_RESULT) + ExperimentSpec 合約」或「檢查 evidence\method-finalization\ 下判定
> 是否 REJECTED / 是否逃逸 overfit-rescue / spec 是否含 anti-overfit+acceptance+nonclaim」
> 時先讀本檔。純唯讀、禁寫檔，輸出 JSON {checker, verdict, items[], blocking[], summary}。
> 對照契約的深層 DOC-20/25 內容見 `references/negative-pnl-method-change-contract.md`。

## 真實根（≠ 任務給的相對路徑）
- Repo：`C:\Projects\Agent_Workspace\SQS-THC`（勿從 C:\Users\user 找；那是 home 不是 repo）。
- 待驗：`evidence\method-finalization\NEGATIVE_RESULT_*.json` + `EXPERIMENT_SPEC_*.json`。
- 鏡像：`evidence\review\method-finalization\`（byte-identical，EVIDENCE HOME RULE）。
- CODEX/provider 佐證：`CODEX_RF_PROXY_VERDICT.json`、`BACKTEST_RUN_RECEIPT_W34_*.json`。

## A 判決 (NEGATIVE_RESULT) 必查欄位
- `determination` == `REJECTED`（對映研究 FSM 終端，非 CANDIDATE/QUARANTINED）。
- `finding`：gross-only PnL 負值、gross win % < breakeven 50%、cost 放大倍率。**跨查數值**
  到所引源 `evidence/far-negative-pnl/FAR_NEGATIVE_PNL_RESEARCH_RESULT.json` 的 `root_cause`
  （-581,939 / 43% / 6.64x 一致才算）。
- `disposition_per_design`：明示 DOC-20『失敗是資產』終端、**No overfit-rescue / no silent param
  re-run**。
- `nonclaim` == LOCAL/RESEARCH；不得自稱 PAPER/live。

## ExperimentSpec 必查欄位
- `new_candidate`（如 model-ml-rf-overnight）且 `supersedes_via` == Slow-Loop MethodChange
  （Fast Loop 禁止改 Method；換法只能走 Slow Loop）。
- `anti_overfit`：new ExperimentSpec+run lineage、NO reuse maker cache、independent checker。
- `cost_model`：fee 14.25 / tax 30 / slip 5 → round_trip 68.5bp（0.685%）。
- `acceptance`：**gross>0 先於 cost-adjusted** + 'positive PnL != acceptance'。
- `nonclaim`。

## 源文對照（解析慣例）
- DOC-20/25 真根：`知識庫\SQS-THC & TW-ICT_FSDT-Stack_SSOT\TW-ICT_FSDT-Stack_專業技術文檔\`
  `TW-ICT_FSDT-Stack_專業技術文檔_DOC-20|25_2026-07-31_r2.md`。**並非** GENIE/TCA 那些同名
  DOC-20/25（false positive）。
- DOC-20 關鍵句：『禁止刪除失敗工件後重跑直到成功；失敗本身應成為 CounterEvidence/
  NegativeResult/Incident 的可檢索輸入』(L181 等)；研究 FSM 單向 `CANDIDATE|REJECTED|
  QUARANTINED`，回 RUNNING 需新 ExperimentSpec+run lineage；『通過仍不等於 paper/shadow/live
  或 PASS_REPLACEMENT』。
- DOC-25 DDD-D25-03：獨立驗證 REQUIRED by impact；maker 自驗非唯一證據；checker 重用 maker
  cache 作唯一證據 → INCONCLUSIVE 另派 checker。Lane B(Method)：EVIDENCE_ASSESSED→
  INDEPENDENT_VALIDATION→VALIDATED|INCONCLUSIVE|REJECTED→PAPER_IF_POLICY_REQUIRES。

## 陷阱（實證）
- `search_files(target="files")` 只搜檔名，不搜內容 → 找含關鍵字檔要用 content search。
- 對 `OneDrive` / `知識庫` 全樹 `grep -r` 會逾時；改用 ripgrep search_files 或先 find 定位
  真根再縮小範圍。
- 專案一律用 `23:5x` 分鐘佔位匿名化時間戳（determined_at/date）——跨工件一致，**不是 defect**。
- 粒度混淆：NEGATIVE_RESULT 的 gross PnL 是 lane0 全量分析值，而 BACKTEST_RUN_RECEIPT 是
  分窗 IS/OOS 值——不同粒度非矛盾；數值要對 FAR 源、不要對 receipt 分窗互碰。
