# 台股當日沖銷(T0) 主軸：四家族權威鏈與當沖方法制定流程

FAR 研究子任務（2026-08-21）產出。姊妹檔：`sqs-thc-knowledge-base-research.md`（RBWI/Spartoi 家族慣例）、
`fsdt-stack-doc-series-research.md`（FSDT DOC 系列 + TW-ICT v3.0 DOC-05 定位）。本檔補**跨四家族的當日沖銷(T0) 主軸**
整合結論與逐條 L 行號，讓未來同域 FAR 研究直接引用，不必重掃 1MB+ 文件。

## 真實檔案根（任務給的路徑常錯）
- `C:\Projects\Agent_Workspace\知識庫\SQS-THC & TW-ICT_FSDT-Stack_SSOT\` → SQS-THC_工程開發文檔(DOC-00..12)、
  TW-ICT_FSDT-Stack_專業技術文檔(DOC-00..29)、`TW-ICT_RBWI_v3.0.0_r2_2026-07-30.md`(10269 行)
- `C:\Projects\Agent_Workspace\知識庫\SQS-THC資料庫\TW-ICT專業技術文檔\【1】TW-ICT_v3.0_專業技術文檔\`
  → TW-ICT_專業技術文檔_v3.0_DOC-00..11（DOC-05 r2 8040 行、469KB）

## 主軸結論（四家族一致）：T0_DAYTRADE 是主軸，T1 隔夜是並列次要例外
- RBWI L8「**交易範圍：** T0_DAYTRADE；T1_OVERNIGHT_OR_SWING」→ 當沖(T0) 列首位 = 主軸。
- RBWI L4053/4059 + FSDT DOC-14 CH-D14-09 L3959/3965：「T0_DAYTRADE 與 T1_OVERNIGHT_OR_SWING 是不同
  OperationSpec、RiskPolicy 與 evidence obligation；T1 不是未平倉 T0 的預設結果」；含 T0/T1 OperationSpec 雙開。
- SQS 工程 DOC-02 CH05.9（L1402-1413）T0/T1 差異矩陣 + run_mode Literal['T0_DAYTRADE','T1_OVERNIGHT_OR_SWING']
  （L5354）；RBWI Operational Contract 承接於 DOC-02-S02。T0=專屬 JobCard/zero-carry/當日 scoped/收盤前 flatten。
- T1（隔夜）需逐部位 OvernightDecision=CARRY/REDUCE/FLATTEN/BLOCKED，次日重驗不自動延長（RBWI OBJ-062、
  DOC-14 CH-D14-09 SOP）；「T1 是新的隔夜風險合約…未通過即不是合法 carry」。

## 時間窗：台股 Session Phase Tree（當沖逐時段受控窗口）
- FSDT DOC-14 CH-D14-04 L272-285：PREMARKET_AUCTION_INDICATIVE→OFFICIAL_OPEN_REFERENCE→OPENING_CALIBRATION→
  S1_CONTROLLED_WINDOW→MIDDAY_REASSESSMENT→S2_CONTROLLED_WINDOW→NEW_INTENT_CUTOFF→MANAGE_ONLY/CONVERGENCE→
  POST_MARKET_RECONCILE→DAILY_ARCHIVE。
- 時間盒三分法（L260-268）：09:00 official open=MARKET_SESSION_REFERENCE；13:10 no-new-entry /
  13:20 force-flat 僅 `LEGACY_SEED_NON_NORMATIVE`（勿把它當硬性全球規則）。時間不變式 known_at ≤ effective_at < expires_at。
- 交易日內禁止 activation（RBWI L3311）；盤中只執行 frozen package（DOC-14 CH-D14-03 L186）。

## 試撮＝indicative evidence（非成交/開盤價/送單依據）
- RBWI §14（L3428-3456）+ DOC-14 CH-D14-07（L287）：試撮價非成交；opening calibration 須等 official open 與
  first tradable event 後建 append-only ScenarioTransition 或 NO_CHANGE。anti-case=把試撮委託量當成交量提前產生
  SetupQualification→禁止。

## SessionCandidatePool-S1 與試撮股池鏈（RBWI L3358-3366）
- D-04 → SessionCandidatePool PREOPEN；D-09 試撮 S1 股池 → SessionCandidatePool S1（空池合法→observe/no trade）；
  D-10 開盤校準；D-11 S1 Setup 觀察；D-12 S1 資格/風險/HITL。
- OBJ-036 CandidatePool、OBJ-037 SessionCandidatePool（state PROPOSED→ADMITTED→WATCH→EXCLUDED→EXPIRED）、
  OBJ-049 SetupQualification。

## Setup Qualification 主鏈（方法→觀察→資格，盤中 frozen）
- RBWI §22（L3909-3967）：「方法定義只能在 Slow Loop 變更；盤中只使用 frozen version。ICT 為主權威」。
- 鏈：OBJ-096 MethodSpec → OBJ-099 NamedModelCard/OBJ-100 SetupFamilyCard → SetupObservation → SetupQualification。
- 11-component non-compensating SOP（L3955）：每 component 只能 PASS/FAIL/UNKNOWN；required FAIL/UNKNOWN 不可被
  其他分數補償；QUALIFIED 只進 RiskAuthorization 不直接建 OrderIntent。
- GATE-08 SetupQualificationGate（L3202）；SF-06 S1 Qualification→Risk→HITL（L4619-4666）。
- 「不需 MethodCard 名稱」— RBWI 用 MethodSpec（OBJ-096）；MethodCard 是 Spartoi 家族用語。

## 盤中 JobCards vs Slow-loop JobCards（RBWI SF-00..17 registry L4098-5600）
- **盤中/當沖鏈**：SF-03 Pre-open Candidate/試撮、SF-04 Opening Scenario Calibration、SF-05 S1 Setup Observation、
  SF-06 S1 Qualification→Risk→HITL、SF-07 Midday Reassessment、SF-08 S2 Candidate Refresh、SF-09 S2 Setup Observation、
  SF-10 S2 Qualification→Risk→HITL、SF-11 Position Management、SF-12 Close/Reconciliation/Overnight、SF-15 Independent
  Risk Service、SF-17 Operator Cockpit。
- **Slow/控制面**：SF-00 Runtime Bootstrap、SF-01 Weekly Context、SF-02 Daily Freeze、SF-13 Replay、SF-14 Daily Archive、
  SF-16 Tool Admission。

## TW-ICT v3.0 DOC-05 當沖方法權威鏈（方法執行鏈上游）
- Executive Synthesis compile chain L53-69：
  `InstrumentMaster+Rule/Data/Eligibility/Capability → UniverseSnapshot+Included/Excluded → Liquidity/Cost/Capacity/Borrow
  gates → EvidenceDependencyGraph/EvidenceStack/CounterEvidenceSet → CandidateTier+CandidatePool+SessionCandidatePool →
  ContextPacket+MTFResponsibilityMap+ContextStack → BiasHypothesis+SMT/RS/CorrelationRegime → five-branch ScenarioTree+
  BranchSwitch → TradeHypothesis+DOC06HandoffEnvelope → ACK/REJECT/ROUTE_BACK/WAIT/NO_TRADE`。
- 16 張 Source Capsule SC-D05-01..16（L219-281）；DOC-05 只到 hypothesis 層，Setup/entry 交 DOC-06/R83（L115/119/
  L259-273；「TradeHypothesis 是研究假說，不是 SetupDecision/RiskAuthorization/OrderIntent」L3078）。

## 當沖 ICT 模組（import 依據）
- DOC-05 CH-11.7 一級技術（L2996-2998）：Full-market Denominator、Rule/Data/Eligibility Reduction、All-in Cost、
  Liquidity/Capacity/Borrow Gate、Evidence Role/Independence、Candidate Ranking、Session Pool、Stale Eviction。
- DOC-05 CH-12.7 一級技術（L4474-4476）：MTF Responsibility Mapping、ContextStack、Dealing Range、Daily/Weekly Bias、
  Counter-evidence、SMT、Relative Strength、Correlation Regime、Five-branch Tree、Branch Switch、PO3/AMD/Profile、
  TradeHypothesis、No-Trade/Route-back。
- RBWI §22.2 MTH-001..012 具名當沖方法（L3926-3939）：OTE、AMD/Power of Three、Silver Bullet、Turtle Soup、
  Judas Swing、Unicorn、Market Maker、NWOG/NDOG、Opening Range、SMT、IPDA、Institutional Order Flow；
  CMP-001..007 當沖 component 判據（BOS、MSS/CHoCH、FVG/VI、Order Block、DOL/Liquidity、Premium/Discount、CISD/Displacement）。
- 注意：DOC-29 明定 ICT 1~107 是 legacy semantic corpus + calibration reference，**不拆 107 個 owner 模組**；
  本文檔以 DOC-05 一級技術 + RBWI MTH/CMP 為當沖主軸 import 依據。

## 方法制定/選擇流程（SQS 應採四段式）
1. **上游採納**：TW-ICT v3.0 DOC-05 權威鏈（32 donor→16 capsule）建 Universe 全分母→Candidate→MTF→Scenario→
   TradeHypothesis，全鏈 hard-gate 不可補償。
2. **定案**：FSDT DOC-14 Slow-Loop Method Change（週期 review→獨立檢查→影響分析→批准/effective→每日 freeze），
   ontology = RBWI OBJ-096 MethodSpec（不用 MethodCard 名）。DOC-05 只產 hypothesis，真值定案在 Slow Loop。
3. **執行鏈**：DOC-05 CH-11/CH-12 → TradeHypothesis → DOC-06 接 Setup/Risk（R83 owner，DOC-05 不可接管）。
4. **盤中**：只執行 frozen MethodSpec，依 RBWI §22 SetupQualification→RiskAuthorization→HumanApproval→
   send-disabled OrderIntent，fail-closed；交易日內禁止改方法/風險（EmergencyRisk 除外）。

## 產出契約
同姊妹檔：JSON `{checker, findings[{item,locator,evidence}], daytrading_axis, method_selection,
ict_modules_to_import, recommendation, verdict}`；locator 附「檔 + L行號段」供 parent 回驗。outcome-first，不 replay。
