# fabric-autonomous-research（FAR）— 受治理自主研究 Shared Infrastructure Team

> **Status**: `FAR-R1 = PASS`（external r7）＋ `TRI-SOURCE = ACTIVE`（WO-FAR-TRISOURCE-001）＋
> `FOCUSED_HARDENING = PASS_CHALLENGE / EXTERNAL ACCEPTANCE GRANTED`（external r3 2026-08-14,
> 15 項 falsification 全過）→ **EXTERNALLY_ACCEPTED_FOR_DECLARED_LOCAL_SCOPE**
> **Swarm/multi-subagent**: `DEFAULT-ON`（UD-FAR-SWARM-DEFAULT-ON-2026-08-14-001, ACCEPTED USER DECISION）
> **Blueprint**: `FABRIC-AUTONOMOUS-RESEARCH-BLUEPRINT-20260813-R2`（ebcc9a7f…, PASS）
> **Acceptance evidence**: `FAR_FINAL_ACCEPTANCE_EVIDENCE.md`（b0b21ced799face7…, 四處 byte-identical）
> **Class**: SHARED_INFRASTRUCTURE_PROFILE_TEAM ｜ heavy_stack: false ｜ manager_agent: NONE

FAR 是一個**受 Fabric 治理、由 HG-KSEOS（HGK）唯一派工、Hermes/Kanban 原生執行**的自主研究能力：
把一個受接納的 decision question，轉成**有來源覆蓋、有明確不確定性、有受控執行、有治理交接**的證據綁定 candidate outputs。

## 快速開始

```text
1. 提出 decision question（例如「研究某開源工具是否值得導入 HGK」）
2. HGK admission → ResearchRequest → R0–R8 研究生命周期自動展開
3. 產出 CandidateResearch / CandidateKnowledge / ProposedEvolution → 交接給 owner 決策
```

使用者**不需要**指定 Prime、模型、lane 或 skill——router 依 capability class 決定路徑。

## 核心概念

| 概念 | 說明 |
|---|---|
| R0–R8 lifecycle | Intake → Plan → Source → Extraction → Analysis → Challenge/Experiment → Synthesis → Candidate → Handoff |
| 三種 terminal product | CandidateResearch / CandidateKnowledge / ProposedEvolution（皆非 authority） |
| Router | `far_router.py` 依 capability class 決定 native/ARIS/specialist 路徑（reason codes FAR_ROUTE_*/FAR_BLOCK_*） |
| 工件契約 | `research-product/RESEARCH_ARTIFACT_CONTRACTS.yaml` + 22 templates |
| 安全 | source-as-data；prompt injection 視為非信任文字；snippet 不自動執行；SEC-SRC-01..08 |
| 自動檢索（R2 內建） | 每次研究自動三通道檢索：知識庫語料（決定性評分）+ HGK Memory/FTS5 + 受治理只讀 web（GET-only; UD-FAR-RETRIEVAL-2026-08-13-001）→ CrossReferenceLedger 交叉比對 |
| 多子代理（Swarm） | **DEFAULT-ON**（UD-FAR-SWARM-DEFAULT-ON-2026-08-14-001）: 研究預設以 HERMES_SWARM 平行執行（SOURCE_FAMILY/HYPOTHESIS/EXPERIMENT split; max_lanes=WorkOrder budget; canonical_parallel_writers=0; merge_collision=DISPUTE） |
| 長跑 | 原生 Hermes long-horizon（checkpoint / detach / reattach / resume）；Kanban 協調 |
| 自進化 | 受治理 feedback loop → CandidateHarnessDelta → HGK Governed Evolution（COV-11-06 人類閘門） |

## 目錄

```text
Fabric/fabric-autonomous-research/
├─ README.md                       ← 本檔（入口）
├─ AGENTS.md                       ← agent 導航契約
├─ TEAM.md                         ← Team 身份/能力/SoD
├─ docs/                           ← 使用說明手冊
├─ research-product/               ← R0-R8 工件契約 + 模板（22）
├─ methods/aris-vendor/            ← ARIS pinned 選定方法（e12e07c7…）
├─ canary/                         ← FAR-20260813-001 / 002 / LH-CANARY-001
├─ far_router.py / far_watchdog.py / far_source_security.py
├─ governance/（receipts + closures + configs: FAR_CAPABILITY_MATRIX.yaml / FAR_EXECUTION_BINDING.json …）
├─ evidence-bundle/                ← raw evidence（tests/spine/kanban/receipts/canary）
├─ evidence/（FAR_EVIDENCE_MANIFEST.json ← evidence root; 歷史證據 MDs; review package）
├─ FAR_SUBJECT_ROOT_MANIFEST.json  ← subject root（95 files, 5720337b…）
└─ FAR_FINAL_ACCEPTANCE_EVIDENCE.md← 單一驗收 MD（b0b21ced799face7…）
```

## 治理邊界（硬規則）

```text
HGK = 唯一 WorkOrder/ExecutionBinding/control plane ｜ Hermes = 受治理 runtime
Kanban = coordination only ｜ Codex = 唯一 tracked mutation writer
provider consensus != acceptance ｜ candidate != authority ｜ provider 不可 self-accept/promote
SQS Financial Truth mutation = 0 ｜ live broker write = 0
```

## Claim ceiling

```text
FAR local implementation = ALL PASS（FAR-R1 PASS, external r7）
PRODUCTION      = NOT_CLAIMED
SQS LIVE TRADING = NOT_AUTHORIZED
REMOTE DEPLOYMENT = NOT_CLAIMED
Prime/ARC/EvoAgentX = 未 qualification 前不自動 active
```

## 文件

- 📖 使用說明手冊: `docs/fabric-autonomous-research_使用說明手冊_v2026.08.13-r1.md`
- 🧭 AGENTS.md（agent）｜📋 TEAM.md（能力/SoD）
- 📜 驗收證據: `FAR_FINAL_ACCEPTANCE_EVIDENCE.md`（b0b21ced799face7…, mirror 三根）

```text
STOP
FAR = ACTIVE（FAR-R1 PASS; external r7 GRANTED）
```
