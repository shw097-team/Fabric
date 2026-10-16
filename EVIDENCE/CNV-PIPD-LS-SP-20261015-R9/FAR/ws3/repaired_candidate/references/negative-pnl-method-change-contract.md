# 負回測處置 × 方法變更契約（六冊權威證據，唯讀研究）

> 建立 2026-08-20（FAR 研究子任務實證）。當用戶要求「依設計規畫，把某策略負回測
> 的處置流程／方法變更契約查清楚」或「方法/策略何時該換、怎麼換」——先讀本檔。
> 這是 **source-to-prose 唯讀證據庫**（引原文+doc+行號），不是執行 SOP；要落地執行
> 閉環請搭配 `references/method-finalization-contract.md`（SQS 工程 DOC-07/09/02）。
> 本 session 為純唯讀，**未寫任何檔**——研究輸出即 JSON，這是慣例。

## 六冊真實檔案根（≠ 任務給的相對路徑；皆在 C:\Projects\Agent_Workspace\知識庫\）
1. **FSDT-Stack 專業技術文檔** `SQS-THC & TW-ICT_FSDT-Stack_SSOT\TW-ICT_FSDT-Stack_專業技術文檔\DOC-00..29`
2. **SQS-THC 工程開發文檔** `...\SSOT\SQS-THC_工程開發文檔\DOC-00..12`
3. **TW-ICT v3.0 專業技術文檔** `SQS-THC資料庫\TW-ICT_v3.0_專業技術文檔\DOC-00..11`（檔名實為 `TW-ICT_專業技術文檔_v3.0_DOC-XX`）
4. **RBWI v3.0.0** `SQS-THC資料庫\TW-ICT_FSDT-Stack設計開發\【1】TW-ICT_FSDT-Stack\【1】TW-ICT_FSDT-Stack\TW-ICT_RBWI_v3.0.0_r2_2026-07-30.md`（多處副本，用此根）
5. **Spartoi RUNBOOK v2.0.0 / P1 執行手冊 v2.1.0** `...\【2】台股當沖隔日沖流程\【2】(舊版)Spartoi｜台股當沖隔日沖\`

## 定位技巧（快速找到集中處）
- 先對整冊跑 keyword 計數 by file（`grep -c`）找出濃度：本任務 Method Change/Slow?Loop/Fast?Loop 集中在
  FSDT DOC-14(82)、DOC-25(12)、DOC-29(13)；RESEARCH_ONLY/MethodSpec 在 DOC-12、DOC-20(CH-23)、DOC-29；
  overfit guard 在 DOC-05/20/25。再用 headings（`grep -E '^#{1,4} '`）縮到章節，最後 read_file 精讀。
- **翻譯陷阱**：六冊幾乎不寫字面「負回測／負PnL」。它被拆成 3 個機制 = 研究狀態機終端
  (REJECTED/QUARANTINED) + NegativeResult-is-an-asset + overfit-rescue guard。查「負回測」會 0 hit，
  要查 RESEARCH_ONLY / REJECTED / QUARANTINED / NegativeResult / MethodChange / 獨立驗證。

## 1) 負回測要不要換／怎麼換（Synthesis）
負 PnL 的反應不是「重跑」、不是盤中臨改、也不是直接換。正確鏈：
- **Fast Loop 原樣承接**：只執行凍結有效包；負結果→把 JobCard BLOCKED、記 NegativeResult，必要時
  EmergencyRiskChange 降級 NO_TRADE。Fast Loop **禁止** Method/Risk mutation。
- **落終端分支**：→ REJECTED/QUARANTINED；失敗是資產（CounterEvidence/NegativeResult/Incident 入庫），
  **禁止刪除失敗工件重跑至成功**（overfit-rescue guard；DOC-20 明文）。
- **要修/要換必走 Slow-Loop MethodChange**：新 ExperimentSpec、可反駁假說、active baseline、
  Independent Validation、Paper/Shadow、禁止同日 activation；新候選 supersede 舊版但 **不改寫歷史**，
  須保留 rollback pointer。換與不換界線 = 「Fast Loop 禁止改 Method/Risk；只有 Slow Loop 能改方法」。

## 2) MethodChange 契約（RBWI v3.0.0 §6，最權威）
單行引原文，用了就直接引用：
- Fast Loop 禁止「OpenSpec proposal、Codex 改碼、Skill 安裝、WIKI promotion、Method/Risk mutation、
  無界 retry、多數決覆寫 Veto、autonomous broker write」（L269）。
- MethodChange/OperationChange/EngineeringChange/EmergencyRiskChange 皆為 Change、**盤中不可建立/啟用**
  （EmergencyRisk 僅可降風險）（L283-287）；DailyRunExecutionPackage 不是 Change（L287-289）。
- MethodChange 狀態機：PROPOSED→DOMAIN_SPECIFIED→QUANT_QUESTION_FROZEN→REVIEWING→APPROVED_FOR_IMPLEMENTATION
  →IMPLEMENTED→INDEPENDENT_VALIDATION→PAPER_SHADOW→APPROVED_FOR_ACTIVATION|REJECTED→ACTIVATED→
  DRIFTED|REVOKED|ROLLED_BACK|ARCHIVED（L329-340）。
- validator 硬拒：無 active baseline / 無可反駁假說 / 未列 downstream consumers / 缺 ExperimentSpec /
  同日 activation / Risk Veto（L372）。
- Engineer/Reviewer Path：「只施工已批准 Change；Fast Loop 禁止改 Method/Risk」（L84）；
  「未有 Paper/Shadow/NRTV 證據時不得升級狀態」（L91）。
- FSDT DOC-14 CH-D14-03 invariant：FastRunning 不可直接回 SlowDraft 改 active truth；
  回饋必須產生新候選+新版本（L222）；學習候選只送 DOC-25、不直接回寫 active policy（L195）。

## 3) MethodSpec / Model 從 RESEARCH_ONLY 升級門檻（不自我裁決、positive PnL ≠ acceptance）
- **DOC-25 Lane B（Method）**：EVIDENCE_ASSESSED→INDEPENDENT_VALIDATION→VALIDATED|INCONCLUSIVE|REJECTED→
  PAPER_IF_POLICY_REQUIRES→OWNER_APPROVAL→CHANGE_PACKAGE。Independent validation「REQUIRED by impact」。
  DDD-D25-03：同一 maker 自驗不能作唯一證據；checker 重用 maker cache → INCONCLUSIVE，另派 checker。
- **DOC-25 Q9**：Q9-D3 禁止直接 canonical mutation（RAG/Agent/Skill/模型只能提 candidate/proposal）；
  Q9-D4 參數需版本化 Authority；Q9-D5 class-specific stage ceiling。Legal transitions：DEFER≠PASS/DENY；
  FAIL/REJECTED 可由新 candidate supersede 但不改寫歷史；QUARANTINE 擋下游；Live 全類 FORBIDDEN。
- **DOC-20**：「通過仍不等於 paper/shadow/live 或 PASS_REPLACEMENT」（CH-04/23/30 反覆）；研究 FSM
  IDEA→ADMITTED→RUNNING→EVALUATED→CANDIDATE|REJECTED|QUARANTINED 單向，任何回 RUNNING 須新 ExperimentSpec+
  新 run lineage；CH-23 METHOD_DRAFT→ASSUMPTIONS_CHECKED→ADMITTED|REJECTED + GATE-D20-METHOD +
  ERR_METHOD_ASSUMPTION_UNTESTED；CH-30 backtest 事件驅動重播 + GATE-D20-BACKTEST。
- **DOC-12**：REGISTERED→COMPILED→READY/RESEARCH_ONLY/FAILED→STALE；adapter 未認證/缺 OOS receipt →
  RESEARCH_ONLY/ADAPTER_NOT_CERTIFIED；「即使 components 全過也不能進 setup gate」（E.8 Silver Bullet 案例 L1741）。

## 4) 候選策略選定權威鏈（TW-ICT v3.0 DOC-05）
權威編譯序：完整 Universe（Rule/Data/Eligibility/Capability hard gates）→ Liquidity/Cost/Capacity/Borrow
hard gates → CandidateTier+CandidatePool → MTFResponsibilityMap → BiasHypothesis（有反證/期限/checker 的
假說，非多數決投票）→ 五分支(Base/Bull/Bear/Unknown/Tail)ScenarioTree → TradeHypothesis →
ACK/REJECT/ROUTE_BACK/WAIT/NO_TRADE（L57-68）。否定輸出是合法等價輸出，不是失敗（L51）。
Authority P0>P1>…>P5>CONTROL>SUPPORT；R79 編譯 Bias/Scenario/TradeHypothesis；DOC-05 不產下單指令、
不可接管 DOC-06 的 setup/no-trade/veto 決策。

## 5) Spartoi CA-METHOD / CA-BACKTEST（回測-修補-定案鏈）
- P1 手冊 v2.1.0 JobCard：SF-05 CA-METHOD（DSL primitives→methodcards≥3，每張須 time_window+
  time_invariants_handling；缺失→Fail-Closed、禁 SF-06/SF-08）；SF-06 CA-BACKTEST（回測→績效/風險摘要；
  全數回測失敗→Fail-Closed；資料<365天→backtest_quality=LOW；指標失敗→NO_METRICS；驗收 date≥365 天 &
  sample≥100 & ≥1 card 完整指標；失敗→禁 SF-07/SF-08）。後續 SF-07 CA-TA→SF-08 CA-SELECT→…
- RUNBOOK v2.0.0：週級「回測→分析→修補→方法定案」（L1004）；MethodCard PLACEHOLDER→BOUND 升級需
  CA-METHOD 產出 + SEM³ 三 Gate + GATE-BACKTEST-PASS（§7.3 L2248-2257）；Fail-Closed 缺失 methodcard→
  BLOCK_RELEASE（L3354-3357）。CA-BACKTEST 本身無負PnL 專屬分支——負結果由 Fail-Closed/LOW/NO_METRICS 承接，
  與 FSDT Slow-Loop 一致。

## 交付慣例
本類純研究子任務輸出 **JSON {checker, findings[{item,locator,evidence}], negative_pnl_disposition,
method_change_contract, selection_authority, recommendation, verdict}**（禁寫檔）。locator 一律
「doc名 + §/CH + L行號」，evidence 直接引原文短句，方便 parent/下游直接改用。
