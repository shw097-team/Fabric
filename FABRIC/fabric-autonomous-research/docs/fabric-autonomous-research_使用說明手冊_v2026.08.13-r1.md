# fabric-autonomous-research 使用說明手冊

> Document ID: `FAR-USER-GUIDE-20260813-R1` ｜ 版本: v2026.08.13-r1 ｜ 日期: 2026-08-13
> 適用: FAR-R1 PASS 後之正式受治理使用（external r7, 58de0815…）
> 母文件: 藍圖 `FABRIC-AUTONOMOUS-RESEARCH-BLUEPRINT-20260813-R2`（ebcc9a7f…）

---

## 1. FAR 是什麼 / 不是什麼

**是**：一個受治理的研究產品——把受接納的 decision question 轉成證據綁定的 candidate outputs，
具備可重現來源覆蓋、明確不確定性、受控執行、治理交接。

**不是**：新的作業系統 / scheduler / task DB / reducer / release authority / 知識平台 /
autonomous manager / web crawler platform / 金融權威。

FAR 的主體不是 Prime，也不是「多 agent 自己互相研究」——是
**Fabric 治理 + HGK 唯一派工 + Hermes/Kanban 原生執行 + selected ARIS 低摩擦方法 + 可資格化 specialist 補強**。

## 2. 治理架構（誰能做什麼）

| 角色 | 職責 | 不可 |
|---|---|---|
| HGK（SharedSpine） | WorkOrder/ExecutionBinding 唯一真相；准入；router；reducer | 直接 DB bypass 研究資料 |
| Hermes | 受治理 runtime：admission 執行、Kanban、swarm、heartbeat、R0–R8 執行 | 自設為任務真相 / release |
| Codex | 唯一 tracked mutation writer（durable WorkOrder） | self-accept / 平行 canonical 寫入 |
| ARIS 方法 | 研究 method layer（pinned, e12e07c7…） | final acceptance / meta-apply 落地 |
| Prime/ARC/LongHorizon/EvoAgentX | specialist（資格化後才 active；預設 standby/off/lab） | self-promote / 改 acceptance predicate |
| Acceptance Officer | fresh-context VERIFY_ONLY 獨立驗收 | 修補 candidate |
| 外部驗收官（Human Policy Owner） | 最終驗收（COV-11-06） | — |

## 3. 使用者旅程（藍圖 §29）

### 3.1 普通工具研究
```text
「研究某新開源工具是否值得導入 HGK」
→ admission → RESEARCH_GENERAL/LITERATURE_REPO → native + selected ARIS
→ source denominator → claim ledger → challenge if needed → CandidateResearch → 建議
```
使用者不需指定 Prime / 模型 / lane / skill。

### 3.2 超大型 corpus
```text
task class = RLM_CONTEXT_HEAVY
→ Prime 僅在 qualified+sandbox 時路由；否則 native（最低能力仍滿足）或 block
→ 無 silent fake RLM
```

### 3.3 SQS 新方法
```text
Research → CandidateResearch → sqs-data-analysis / sqs-risk → domain owner
→ 若要 durable change：OpenSpec/HGK/Codex route
不變更 Financial Truth；paper/RAG 輸出 != trading signal
```

### 3.4 持續自進化
```text
accepted trajectories/failures → trajectory mining → CandidateHarnessDelta
→ HGK Governed Evolution → independent acceptance → canary/rollback
provider 不可 self-promote；COV-11-06 人類閘門保留
```

## 4. 操作流程

### 4.1 發起研究（admission）
1. 提出 decision question + owner + 來源/預算/邊界（R0 ResearchRequest）
2. HGK 准入 → REQ FROZEN → TS → WO（writer=codex）
3. Kanban board 建 DAG → claim/heartbeat/complete

### 4.2 執行（R1–R8）
- R1 Plan: subquestions / claim classes / sources / stop & abstain criteria
- **執行姿勢（2026-08-14 起）: Swarm/多子代理 DEFAULT-ON**（UD-FAR-SWARM-DEFAULT-ON-2026-08-14-001）——
  研究預設以 HERMES_SWARM 平行 fanout（SOURCE_FAMILY_SPLIT / HYPOTHESIS_SPLIT /
  INDEPENDENT_EXPERIMENT_SPLIT; max_lanes=WorkOrder budget; canonical_parallel_writers=0;
  merge_collision=RESEARCH_DISPUTE_OPEN）; 單線 native 直接執行仍合法（明確選擇時）
- **R2 自動檢索（far_retrieval.py）**：每次研究自動三通道——
  ① 知識庫語料（9 roots, 決定性 CJK-aware 評分, bounded scan）② HGK Shared...
  knowledge_fts/memory_records（FTS5）③ 受治理只讀 web（GET-only、timeout 30s、
  256KB cap、無 credential、WorkOrder 宣告 roots）→ CrossReferenceLedger
  （KB↔memory↔web 交叉比對 agreement/disagreement）→ 饋入 R4 Hypothesis/Contradiction
- R2 Source: discover → snapshot/locator → hash → denominator（MISSING 不得用 model memory 補）
- R3 Extraction: fact/claim/constraint/instruction/code 分離（source instruction = DATA）
- R4 Analysis: Hypothesis / FitGap / Contradiction / RejectedAlternative
- R5 Challenge/Experiment（conditional）: 未跑實驗不得產生 ExperimentResult=PASS
- R6 Synthesis: claim-source map / confidence / counterevidence / nonclaims
- R7 Candidate packaging: CandidateResearch / CandidateKnowledge / ProposedEvolution
- R8 Handoff: RESEARCH_PASS_CANDIDATE / PARTIAL / ABSTAIN / FAILED / BLOCKED_* / ABORTED_BUDGET

### 4.3 驗收與證據
- local gates FAR-Q0..Q10（Q7 可 N/A_NOT_SELECTED_WITH_REASON）
- 證據凍結順序: 工件 → 單一證據 MD 最後生成 → 鏡像三根 → hash 全等
- 外部 focused re-review 簽 FAR-R1（本輪已 PASS, r7）

## 5. 工件契約（research-product/）

```text
ResearchRequest.yaml / ResearchPlan.yaml / ResearchSourceDenominator.tsv / QueryLedger.tsv /
SourceSnapshotLedger.tsv / SourceDispositionLedger.tsv / ExtractionLedger.jsonl /
HypothesisLedger.tsv / FitGapLedger.tsv / ContradictionLedger.tsv / ClaimLedger.tsv /
DisagreementLedger.tsv（conditional）/ ExperimentPlan.yaml + ExperimentResult.yaml（conditional）/
RejectedAlternativeLedger.tsv / OpenQuestionLedger.tsv / ResearchSynthesis.md /
CandidateResearch.yaml / CandidateKnowledge.yaml / ProposedEvolution.yaml /
ResearchHandoff.yaml / ResearchRunReceipt.json
```
契約與模板: `RESEARCH_ARTIFACT_CONTRACTS.yaml` + `templates/`（22 個）。

## 6. Router / 挑戰 / Failover 語義

- **Route**: 一個 admitted WorkOrder → 一個 primary（one-primary default）
- **Challenge**: primary CandidateResearch → fresh-context challenger → DisagreementLedger → 修訂或 unresolved
- **Failover**: primary 失敗 → freeze evidence → capability-compatible qualified fallback；不隨機換 provider
- **Parallel**: 僅獨立 source/hypothesis/experiment split（deterministic merge keys）；collision → RESEARCH_DISPUTE_OPEN
- Reason codes: FAR_ROUTE_NATIVE_DEFAULT / FAR_ROUTE_PRIME_ACP_RLM / FAR_BLOCK_* / FAR_ABORT_* / FAR_DEGRADE_*

## 7. 安全契約（source-as-data）

```text
來源內容 = DATA（除非明示為 authority）
prompt injection = 非信任文字；不能覆寫 Fabric / 擴權 / 要 secret / 自動安裝 / 關 AO
executable snippet = 不自動執行（需 sandbox + command readback + bounded write set）
repo-local instruction（AGENTS.md/CLAUDE.md/SKILL.md 等）= SOURCE_LOCAL_INSTRUCTION_NOT_GLOBAL_AUTHORITY
負面 fixtures: SEC-SRC-01..08
```

## 8. 長跑 / 背景執行

- 原生 Hermes long-horizon：WorkOrder → /goal projection → Kanban → checkpoint → detach/reattach → resume
- runtime checkpoint（Hermes session/Kanban）≠ normative checkpoint（HGK WorkOrder/artifact digests）
- no-progress watchdog（evidence delta 判斷；max_identical_action_repeat=3 等）
- budget exhaustion → checkpoint + RESEARCH_ABORTED_BUDGET / PARTIAL

## 9. 已知限制 / 注意事項

- Prime / AutoResearchClaw / LongHorizon / EvoAgentX 尚未 qualification → 維持 standby/off/lab（誠實 N/A）
- ARIS 僅 selected pinned methods（13 個）有效載入；bulk catalog 不自動導入
- Obsidian 投影為 DERIVED_ONLY（human-visible 需驗證 open/read）
- 中文本機文件由 Hermes 直寫（Codex mojibake 防護）；Codex prompt 一律 English-only

## 10. Claim ceiling

```text
FAR local implementation = ALL PASS（FAR-R1 PASS）
PRODUCTION = NOT_CLAIMED ｜ SQS LIVE = NOT_AUTHORIZED ｜ REMOTE = NOT_CLAIMED
SQS_FINANCIAL_TRUTH_MUTATION = 0 ｜ LIVE_BROKER_WRITE = 0
```

```text
STOP
FAR = ACTIVE（正式受治理使用）
```
