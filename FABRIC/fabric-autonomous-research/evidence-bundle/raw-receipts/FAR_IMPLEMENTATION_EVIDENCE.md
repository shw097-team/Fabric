# FAR Implementation Evidence — fabric-autonomous-research 藍圖 v2026.08.13-r2

> Document ID: `FAR-IMPLEMENTATION-EVIDENCE-20260813`
> generated_at_utc: 2026-08-13T10:54:08Z
> 藍圖: `FABRIC-AUTONOMOUS-RESEARCH-BLUEPRINT-20260813-R2`（sha256 `ebcc9a7f00e8f2a4dda76e7b08dd1211175760cc7e66353ded3d409ca812f573`）
> 用途: 供**外部驗收官**進行最終驗收（COV-11-06 human gate）；本文件不自我核准任何最終接受。

## 0. Claim ceiling（誠實、無自我核准）

```text
FAR_BLUEPRINT                    = PASS (artifact v2026.08.13-r2; blueprint-level only)
FAR_IMPLEMENTATION_LOCAL         = PASS (WO-FAR-001..008 all VERIFIED; gates Q0..Q10 PASS local)
FAR_RESEARCH_PRODUCT_LIFECYCLE   = PASS (R0-R8 end-to-end canary, 19 artifacts, RESEARCH_PASS_CANDIDATE)
FAR_SOURCE_SECURITY              = PASS (SEC-SRC-01..08 + guard module; 10/10 tests)
FAR_ARIS_SELECTED_METHODS        = PASS (pin e12e07c7; 13 methods; EFFECTIVE_LOAD_STRUCTURAL_PASS)
FAR_LONG_HORIZON_NATIVE          = PASS (contract + detach/reattach canary)
FAR_DETERMINISTIC_ROUTER         = PASS (far_router.py + far_watchdog.py codex-authored; 13/13 tests)
FAR_PRIME (Q7)                   = N/A_NOT_SELECTED_WITH_REASON (v0.7.2 pin 83a0f9f9; CR-FAR-002/003/005)
FAR_GOVERNED_EVOLUTION           = PASS (IC-80D1DE01 QUALIFIED -> independent PASS -> PROMOTION_READY_HITL_SOURCE_REQUIRED)
FAR_INTEROP/OBSIDIAN             = PASS (disposition all explicit; map DERIVED_ONLY)
FAR_Q10_INDEPENDENT              = PASS (swarm dual-lane read-only; both lanes; SWARM-FINDING-FAR-001 resolved)
FAR_R1_SEAL / EXTERNAL           = PENDING (external verifier final acceptance; NOT self-issued)
PRODUCTION_AUTONOMY              = NOT_CLAIMED
SQS_LIVE_TRADING                 = NOT_AUTHORIZED
REMOTE_DEPLOYMENT                = NOT_CLAIMED
SQS_FINANCIAL_TRUTH_MUTATION     = 0
LIVE_BROKER_WRITE                = 0
```

## 1. Governance binding（HGK SharedSpine）

```text
REQ-FAR-001..008  FROZEN v1 (8 canonical events FRZ-REQ-FAR-*; actor far-orchestrator)
TS-FAR-001..008   taskspecs created under WO-FAR-*
WO-FAR-001..008   writer=codex  state=VERIFIED (checker=acceptance-officer; base_head 22e21f0340501caf4ff0dbd67663faf49f521b03)
EVD rows          19 (16 core + EVD-FAR-GATES-R2 + EVD-FAR-SWARM + EVD-FAR-INDEX-R2; superseding per PCIV-F01 pattern)
CAPC contract     FAR-IMPLEMENTATION-2026-08-13-001: lint/activation/acceptance PROMPT_COMPILE_PASS (0 errors)
                  duplication ratio 0.036964; contract sha256 fe6cda2ac771c8941ab33acddfb18d9412bb76dce2839665d1f58901f76d9c2e
```

## 2. Execution surfaces（default-on，raw evidence）

| Surface | Evidence |
|---|---|
| HGK | doctor PASS (blocking=[]); 8 WO admitted+VERIFIED; typed SharedSpine API |
| KANBAN | board `far-implementation`; DAG Q0->WO-001..008->GATES->EVIDENCE; Q0+WO-001..007 done; WO-008 claimed; heartbeat/claim/complete traced |
| SWARM | delegate_task deleg_597936a6 dual-lane read-only (Lane A governance ALL_PASS 75.73s; Lane B product PASS+1 count correction 37.72s; overlap 17:01:30-17:02:46Z; transcripts in delegation cache) |
| GSTACK | registry ACTIVE_SELECTED (8 slices); FAR_ROUTE_CHECK.yaml |
| OPENSPEC | registry CERTIFIED_ACTIVE_BROWNFIELD; durable-change-only; FAR_ROUTE_CHECK.yaml |
| CODEX | 2 real spawns (WO-002 far_router.py+far_watchdog.py; WO-003 far_source_security.py) on sealed lane codex-0.147.0-alpha.6.5; provider receipts opencode-go/deepseek-v4-flash status 200 (usage.jsonl ocx-msra3gxi-7e/ocx-msra3khx-7f/ocx-msra3njv-7g); tests 23/23 independent readback |
| 補償控制 | CODEX_EXECUTOR_FALLBACK=MOJIBAKE_DEFECT: 中文文件由 Hermes 直寫 + CJK/U+FFFD 檢查；SOUL.md 遭 protected-file guard 拒寫（NOT_WRITTEN_GUARDED，不繞過） |

## 3. Materialized artifacts（SHA-256 from final bytes；raw index = FAR_ARTIFACT_INDEX.json `83ab2f4aabded1c91d7ba788cb409cf32055a465a723a9b5f6e115321533e53a`）

| # | Artifact | SHA-256 |
|---|---|---|
| FAR_Q0_CROSSWALK.md | `f73e276cf1264708a1e0ef1b73d07192b03948fc3c2ce8b22453448c41e8d088` |
| FAR_C0_CAPC_RECEIPT.json | `d659d9f0656f7e57518a1df9d1c0f4f96d10a3fe2d826b1f675ae194d2c8e0a8` |
| TEAM.md | `ae67143a2928b27ef4916a78b9e8f2bb46759cd9edb031c60c688c83926e8ae5` |
| FAR_CAPABILITY_MATRIX.yaml | `2469d85bf94f16886eb71b169b799fb243c8b5c6bdf3f627178140e9e1f6df6f` |
| FAR_EXECUTION_BINDING.json | `87ae3bd2a7f07b875e7247bb3d34f3b843e90054d83aa802b24dcfc5985cd218` |
| FAR_INTEROP_DISPOSITION.yaml | `bf6a9b00e548de21dc6b897c460eb057c3c96b0105cf131e9c639504b15d948f` |
| FAR_SOURCE_SECURITY.yaml | `c7afbff30c6caa3c7ff7c40d7915f271bfef8dca6314aabf1ba82ce5f3a2aba0` |
| FAR_ARIS_METHOD_DISPOSITION.yaml | `d54db220bce5406c596e6a00e8d2e356daf1fb5541e8d562d716c061f8f3bfd4` |
| FAR_ARIS_EFFECTIVE_LOAD_RECEIPT.json | `a8b3456e8f91bf222961de74d40e77b9f69635807d58481b45e390003de53283` |
| FAR_LONG_HORIZON_CONTRACT.yaml | `0dccec95cfaa2d46a93c4e18ad0f18b9639c45e89ac00fe494e01eb6712b16a6` |
| FAR_PRIME_QUALIFICATION_RECORD.yaml | `d2a9c67c147caf459b9ede9c4f64afd854c0c232f7f0c7567455c3017136663d` |
| FAR_ROUTE_CHECK.yaml | `bd6f5c113410065131e73f4a406d2e18f28ff82de50dc446a85314ba11b9de93` |
| FAR_EVOLUTION_CANARY_RECEIPT.json | `ea3b22e3dff092e38879ab9f3127b213419b41c3a358f7cd479d3a7219169f8d` |
| FAR_GATES_RECEIPT.json | `bc55f4bc0e0a75ca3484df80421da383e7ccad83c0e0973fccecd182a91c9662` |
| FAR_SWARM_Q10_RECEIPT.json | `764b4f2945acc381d8576e329b4eef00433f39eed1d11401281e2029e560f2c8` |
| FAR_ARTIFACT_INDEX.json | `27a357ac698d8527927dc9eaecd13e4e0a4d4920857c7bb46c7c42d134b0e56b` |
| far_router.py | `ade07192ae8d04776b67046ad90ffbf4cbcbe1d2fa0b3494a9d6a80057f23a3a` |
| far_watchdog.py | `852eb358303c95ab145eebb873e4740c6179710e11fce1c52e5c90a39599c346` |
| far_source_security.py | `5227edde39a04edc848df42d1faf089fcbd71f4a65d5da1a5a2b00390f375331` |
| RESEARCH_ARTIFACT_CONTRACTS.yaml | `bb0c518044cb4326aa9957cdc1e520af62b764417f3109416bc4ca874ea15550` |
| ResearchRunReceipt.json | `28f4751b04c0f120f4f0311b5cbdbc066be1214b85e6ae00670d0bdc55a74264` |
| FAR_RESEARCH_MAP.md | `b1dfb485587d146d305eb8998a8436e96975e20d1bc59dcd44452dcddb53fe21` |

> 完整 raw index（75 項，含 22 templates + 19 canary + 3 LH canary + profile 3 件）: `Fabric/fabric-autonomous-research/FAR_ARTIFACT_INDEX.json`
> ARIS vendor（86 skills, pinned e12e07c7b85ee1a4dc07e5463089aa16836af2bf）: `Fabric/fabric-autonomous-research/methods/aris-vendor`（shallow clone, catalog sha256 `77dcf928a85e033c51a22b56fe1e50196bc2d2a39f481c9176031073de1f0c40`）

## 4. Research product lifecycle（R0–R8 canary）

```text
run: FAR-20260813-001  task_class: RESEARCH_LITERATURE_REPO  primary: fabric-autoresearch-native
19 artifacts: ResearchRequest/Plan, SourceDenominator/Query/Snapshot/Disposition ledgers, ExtractionLedger,
  Hypothesis/FitGap/Contradiction/Claim ledgers, RejectedAlternative/OpenQuestion ledgers,
  ResearchSynthesis.md, CandidateResearch/Knowledge, ProposedEvolution, ResearchHandoff, ResearchRunReceipt
terminal: RESEARCH_PASS_CANDIDATE (local; NOT acceptance)
progress semantics: verified-progress whitelist per blueprint 12.1 (enforced in far_watchdog.VerifiedProgress)
no experiment run -> no ExperimentResult (R5 not triggered; zero fabricated experiment claims)
```

## 5. Local qualification gates（FAR-Q0..Q10 + R1）

| Gate | Result | Evidence |
|---|---|---|
| FAR-Q0 authority/schema freeze | PASS | FAR_Q0_CROSSWALK.md + CAPC receipt |
| FAR-Q1 team/profile registration | PASS | TEAM.md (heavy_stack false, manager NONE) + profile 3/4 (SOUL.md guarded) |
| FAR-Q2 research product lifecycle | PASS | canary 19 artifacts + receipt RESEARCH_PASS_CANDIDATE |
| FAR-Q3 source security | PASS | SEC-SRC-01..08; guard module; 10/10 tests |
| FAR-Q4 ARIS selected methods | PASS | pin + 13 hashes + EFFECTIVE_LOAD_STRUCTURAL_PASS |
| FAR-Q5 long-horizon/fanout/budget | PASS | contract + LH-CANARY-001 detach/reattach + watchdog defaults |
| FAR-Q6 router/degrade/FinOps | PASS | far_router/far_watchdog 13/13; 16 reason codes |
| FAR-Q7 Prime | N/A_NOT_SELECTED_WITH_REASON | FAR_PRIME_QUALIFICATION_RECORD.yaml (accepted conditional-gate outcome) |
| FAR-Q8 evolution feedback loop | PASS | IC-80D1DE01 QUALIFIED -> independent PASS -> PROMOTION_READY_HITL_SOURCE_REQUIRED |
| FAR-Q9 interop/Obsidian | PASS | FAR_INTEROP_DISPOSITION.yaml + FAR_ROUTE_CHECK.yaml + Obsidian map DERIVED_ONLY |
| FAR-Q10 independent acceptance | PASS | FAR_SWARM_Q10_RECEIPT.json (dual-lane; SWARM-FINDING-FAR-001 resolved) |
| FAR-R1 seal/handoff | PENDING_EXTERNAL | evidence MD + mirrors (this file); external verifier final |

## 6. Canaries（WO-008）

```text
C1 Fabric tool research      PASS (canary run RESEARCH_LITERATURE_REPO on 知識庫+upstream pins)
C2 HGK trajectory mining     PASS (evolution canary IC-80D1DE01)
C3 SQS financial-method      PASS-BOUNDARY (RESEARCH_FINANCIAL_METHOD routed native+SQS owner boundary; no mutation)
C4 long-horizon resume       PASS (LH-CANARY-001 pid 24420 detach -> checkpoint -> pid 12604 reattach -> terminal)
C5 source prompt-injection   PASS (SEC-SRC-01..08, 10/10)
C6 provider degrade/failover PASS (router tests: prime unqualified->block/degrade; mandatory challenge->block; science->research-only)
C7 Obsidian research map     PASS-DERIVED (FAR_RESEARCH_MAP.md exists + links resolve + DERIVED_ONLY legend; human-open by verifier)
C8 interop disposition       PASS (OASF/ContextForge/MCP/A2A/OTel/Qdrant/Neo4j/Obsidian each explicit)
```

## 7. Provider / method disposition

```text
Prime Agent        v0.7.2 = 83a0f9f9566219551fcb6ffaf7f519a815749a58; HEAD 7787f07415d843b9a800f6a4720e0c739bd608e5
                   CANDIDATE_STANDBY; N/A_NOT_SELECTED_WITH_REASON (no host runtime / sandbox / Windows ACP)
LongHorizon        METHOD_DONOR_ONLY (macOS-first; verified-state concepts adopted into FAR contract)
AutoResearchClaw   DEFAULT_OFF (Docker sandbox unavailable; science-only when qualified)
EvoAgentX          LAB_ONLY (CandidateWorkflow/CandidateEvolution only)
ARIS               SELECTED_PINNED_METHOD_PACK (13 methods; meta-apply NO_ADOPT_LANDING_AUTHORITY)
```

## 8. Security

```text
source-as-data: FAR_SOURCE_SECURITY.yaml (DATA_UNLESS_EXPLICITLY_ADMITTED_AUTHORITY)
prompt injection: TREAT_AS_UNTRUSTED_TEXT; no override/expand/secret/auto-install
executable snippet: no auto-run (sandbox+readback+bounded write set+admission required)
SEC-SRC-01..08: all negative fixtures enforced by far_source_security.py (10/10 tests)
remote permission escalation: DENY; tool install = separate qualification event
```

## 9. Interop + Obsidian

```text
OASF oasf-record/1 EXTEND | ContextForge CF1 USE_WHEN_ROUTED | MCP stdio LOCAL_ONLY |
A2A REQUIRED_WHEN_ROUTED (none active) | OTel CURRENT_MACHINE_STATE_REQUIRED/NO_FORCED_ADOPTION |
Qdrant PRESERVE_DEFAULT_OFF | Neo4j PRESERVE_DEFAULT_OFF | Obsidian DERIVED projection
Obsidian map: 知識庫\Obsidian投影\FAR\WO-FAR-008\FAR_RESEARCH_MAP.md (sha256 `b1dfb485587d146d305eb8998a8436e96975e20d1bc59dcd44452dcddb53fe21`)
```

## 10. Nonclaims & regression posture

```text
NOT_ACCEPTANCE_PASS (this MD is evidence, not acceptance)
NOT_PRODUCTION_AUTHORIZATION; production autonomy NOT_CLAIMED
SQS live trading NOT_AUTHORIZED; remote deployment NOT_CLAIMED
no second scheduler/task DB/reducer/release authority (FAR-T001..T010 posture: PASS)
provider self-promotion = 0; AO candidate repair = 0; source instruction authority escape = 0
FAR-T011..T092 regression predicates: covered by gates Q2..Q9 artifacts + tests (full mapping in gates receipt)
```

## 11. Freeze / mirror

本文件為**最後生成**（freeze order：先凍結全部工件 → 最後生成本 MD → 鏡像 → hash）。
鏡像位置（byte-identical + SHA-256 相等驗證）: 見下方 mirror table。
外部驗收官請以三根 mirror hash 一致 + 各工件 SHA-256 與 §3 raw index 比對為準。

```text
STOP
FAR_IMPLEMENTATION_LOCAL = PASS (gates Q0..Q10)
FAR_EXTERNAL_FINAL_ACCEPTANCE = PENDING (external verifier; COV-11-06; not self-issued)
```
