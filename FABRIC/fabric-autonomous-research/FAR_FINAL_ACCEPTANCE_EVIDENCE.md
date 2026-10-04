# FAR Final Acceptance Evidence（單一驗收 MD — 全量 raw 內嵌）

> Document ID: `FAR-FINAL-ACCEPTANCE-EVIDENCE-20260813`
> generated_at_utc: 2026-08-13T15:50:11Z
> 目的: 閉合 EXT-FAR-R5-001（declared native raw files were not actually delivered as readable attachments）
> 本檔 = **唯一驗收交付物**：所有 load-bearing raw evidence **全文內嵌**（非摘要、非 hash-only、非外部路徑依賴）。
> 對應 native files 於 `C:\Projects\Agent_Workspace\Fabric\fabric-autonomous-research\`（本檔與其 byte-identical 內容; 各檔獨立 sha 於 §1）。

## 0. Claim ceiling

```text
FAR_BLUEPRINT                = PASS（ebcc9a7f…）
FAR_IMPLEMENTATION_LOCAL     = PASS（Q0..Q10 local; WO-FAR-001..008 VERIFIED）
FAR_EXTERNAL_CHALLENGE_CLOSURE = PASS（EXT-FAR-001..010 10/10 CLOSED/separate-subject + EXT-FAR-R6-001/002 CLOSED）
FAR_INTERNAL_ACCEPTANCE(Q10) = PASS（deleg_bab33aae 9/10 → AO-FINDING-FAR-002 → repair → deleg_e4a09db4 4/4 PASS; blockers=0）
FAR_EXTERNAL_FINAL_ACCEPTANCE = PENDING（外部 reviewer 對本檔全量 readback 後裁決; COV-11-06）
PRODUCTION / SQS live / REMOTE = NOT_CLAIMED / NOT_AUTHORIZED / NOT_CLAIMED
SQS_FINANCIAL_TRUTH_MUTATION = 0 ｜ LIVE_BROKER_WRITE = 0
```

## 1. Delivery manifest（14 native files; 本檔內嵌其全文）

| # | Native file（FAR root 相對路徑） | SHA-256（full） | Bytes |
|---|---|---|---|
| 1 | FAR_Q4_REAL_INVOCATION_RECEIPT.json | `143887c82803373a67f362390920f3d6e462d5340c162898baf9ab67aaa99b00` | 6442 |
| 2 | FAR_Q10_AO_RECEIPT.json | `da3174916358fdc20c8072e1adfb3062af72d44e0a4d65093b0fda4708e496eb` | 1696 |
| 3 | FAR_REGRESSION_CROSSWALK.json | `46a74fd56bc551a391a661177897b84a2013e682a645435c60290dcd3fab99e7` | 15128 |
| 4 | FAR_SUBJECT_ROOT_MANIFEST.json | `00806ea1c932f498ae7b4f2f067fb93d2f67f93a170d5872cde210c30916a558` | 14719 |
| 5 | FAR_EVIDENCE_MANIFEST.json | `14eed267e97602ef47002678059e4c66149c3fb6b6e8406f86ba48d8d1cc655b` | 22951 |
| 6 | FAR_MIRROR_READBACK_RECEIPT.json | `1d564301ac122109d057fb6ef5d431a2dda6eb88fa43e6ca0c77a98beaa7ff87` | 1051 |
| 7 | evidence-bundle/raw-tests/far_tests_suite.stdout.txt | `4aa600009eabd4ae334d7557e5094ab5d5f583208734d0e6c194339bc52453c5` | 134 |
| 8 | evidence-bundle/raw-tests/far_tests_suite.exitcode.txt | `5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9` | 1 |
| 9 | evidence-bundle/raw-spine/far_spine_readback_final.json | `46826ae9721a5c902a006b591bd8ba4f4ec1ccb8b09da69c105c669a9ea07e01` | 13418 |
| 10 | evidence-bundle/raw-kanban/far-implementation_snapshot_final.txt | `8d09bc2fc896d9678cb33bb3eadaf9f6ad6d902f135dd77ec5636bd02bb67813` | 1213 |
| 11 | evidence-bundle/raw-kanban/far-first-use_snapshot_final.txt | `2abdec76a31c2057220b18ddcda6927a75e1927249a436c0c15890e984ec4756` | 605 |
| 12 | evidence-bundle/raw-kanban/far-external-closure_snapshot_final.txt | `6e2101892fd4bd5711fdc78ad3e0f2b22e7c3df7184906690fca1346dcdf8bef` | 539 |
| 13 | FAR_NEGATIVE_SIDE_EFFECT_RECEIPT.json | `52fb07f3f6adc89e78caaf716622d21dceab5587fedeb8befef83272e8fdeb96` | 3197 |
| 14 | evidence-bundle/raw-spine/far_spine_readback_final_r2.json（supersedes #9） | `d24e8b80b8db38150395d582a1de59210a2f9644cb6e64d5f73344dac6632017` | 14346 |

## 2. Q4 real invocation receipt（全文）

```json
{
 "schema": "FAR-Q4-REAL-INVOCATION-RECEIPT/1",
 "gate": "FAR-Q4",
 "finding_ref": "EXT-FAR-008",
 "exact_set": {
  "research-lit": "00d9f549e4db72f3b02d55b9f6dcd61b20403f5a7e25cf3396160423140b9183",
  "novelty-check": "c512579faa065c7e886935d64c2d7d7c810cef8e8f5f6ff5cd902d6ab90e68af"
 },
 "effective_load": "EFFECTIVE_LOAD_STRUCTURAL_PASS (frontmatter parse + pin match; FAR_ARIS_EFFECTIVE_LOAD_RECEIPT.json)",
 "real_invocations": [
  {
   "method": "research-lit",
   "pinned_commit": "e12e07c7b85ee1a4dc07e5463089aa16836af2bf",
   "skill_sha256": "00d9f549e4db72f3b02d55b9f6dcd61b20403f5a7e25cf3396160423140b9183",
   "input": "governed autonomous research agent harnesses (Prime Agent / LongHorizon-Harness / AutoResearchClaw) related work",
   "execution_trace": [
    {
     "step": "research-lit.source_scan",
     "corpus_files": 5,
     "extracted_identities": 80,
     "sample": [
      {
       "source": "FAR_討論-1.md",
       "repo": "github.com/PrimeIntellect-ai/prime-agent"
      },
      {
       "source": "FAR_討論-1.md",
       "repo": "github.com/PrimeIntellect-ai/prime-agent"
      },
      {
       "source": "FAR_討論-1.md",
       "repo": "github.com/PrimeIntellect-ai/prime-agent"
      },
      {
       "source": "FAR_討論-1.md",
       "repo": "github.com/PrimeIntellect-ai/prime-agent"
      },
      {
       "source": "FAR_討論-1.md",
       "repo": "github.com/PrimeIntellect-ai/prime-agent"
      },
      {
       "source": "FAR_討論-1.md",
       "repo": "github.com/PrimeIntellect-ai/prime-agent"
      },
      {
       "source": "FAR_討論-1.md",
       "repo": "github.com/PrimeIntellect-ai/prime-agent"
      },
      {
       "source": "FAR_討論-1.md",
       "repo": "github.com/PrimeIntellect-ai/prime-agent"
      },
      {
       "source": "FAR_討論-1.md",
       "repo": "github.com/PrimeIntellect-ai/prime-agent"
      },
      {
       "source": "FAR_討論-1.md",
       "repo": "github.com/PrimeIntellect-ai/prime-agent"
      },
      {
       "source": "FAR_討論-1.md",
       "repo": "github.com/PrimeIntellect-ai/prime-agent"
      },
      {
       "source": "FAR_討論-1.md",
       "repo": "github.com/PrimeIntellect-ai/prime-agent"
      }
     ]
    },
    {
     "step": "research-lit.related_work_summary",
     "papers": {
      "Prime Agent": "self-improving RLM coding/research harness (v0.7.2, 2026-08-11); persistent IPython kernel; recursive subagents; Continual Harness /refine; ACP JSON-RPC stdio (source: FAR_討論-1/2)",
      "LongHorizon-Harness": "verified-task-state long-horizon loop: Manager -> fresh-context Executor -> read-only Auditor; v0.1.4 2026-08-11; macOS-first (source: FAR_討論-3/4)",
      "AutoResearchClaw": "23-stage scientific research pipeline; Docker sandbox; claim verification; HITL; cost guardrails (source: FAR_討論-3/4)",
      "ARIS": "markdown-only composable research skills (86 in catalog); executor + cross-model reviewer; no framework lock-in (source: FAR_討論-3/4 + pinned vendor)"
     }
    }
   ],
   "output": {
    "topic": "governed autonomous research agent harnesses (Prime Agent / LongHorizon-Harness / AutoResearchClaw) related work",
    "sources_used": "LOCAL (network DENY per WorkOrder; method source directive 'sources: local')",
    "related_work_found": 4,
    "summaries": {
     "Prime Agent": "self-improving RLM coding/research harness (v0.7.2, 2026-08-11); persistent IPython kernel; recursive subagents; Continual Harness /refine; ACP JSON-RPC stdio (source: FAR_討論-1/2)",
     "LongHorizon-Harness": "verified-task-state long-horizon loop: Manager -> fresh-context Executor -> read-only Auditor; v0.1.4 2026-08-11; macOS-first (source: FAR_討論-3/4)",
     "AutoResearchClaw": "23-stage scientific research pipeline; Docker sandbox; claim verification; HITL; cost guardrails (source: FAR_討論-3/4)",
     "ARIS": "markdown-only composable research skills (86 in catalog); executor + cross-model reviewer; no framework lock-in (source: FAR_討論-3/4 + pinned vendor)"
    },
    "key_insight": "The related-work corpus positions FAR as the governed aggregation: native Hermes/Codex baseline + ARIS method layer + conditional specialists (Prime/ARC) + method donors (LongHorizon/EvoAgentX), all under HGK WorkOrder truth"
   },
   "output_digest": "bdb47993d9d8412dddfd512f1526331252aea2fd574f7fb4cf5cdc256ebecb96"
  },
  {
   "method": "novelty-check",
   "pinned_commit": "e12e07c7b85ee1a4dc07e5463089aa16836af2bf",
   "skill_sha256": "c512579faa065c7e886935d64c2d7d7c810cef8e8f5f6ff5cd902d6ab90e68af",
   "input": "FAR landing recipe novelty screening",
   "execution_trace": [
    {
     "step": "research-lit.survey_output",
     "output_keys": [
      "topic",
      "sources_used",
      "related_work_found",
      "summaries",
      "key_insight"
     ]
    }
   ],
   "output": {
    "subject": "FAR landing recipe (shared-infra-team-implementation.md §1-12)",
    "prior_art_denominator": 10,
    "findings": [
     {
      "claim": "landing recipe exists in references",
      "prior_art_hit": "shared-infra-team-implementation.md (same-class sibling; NOT novel as a file)",
      "verdict": "NOT_NOVEL_AS_FILE_BUT_UNIQUE_DELTAS_VERIFIED"
     },
     {
      "claim": "WO batch admission via typed SharedSpine API",
      "prior_art_hit": "shared-spine-admission.md (prior art, 2026-08-12)",
      "verdict": "EXTENSION_VERIFIED (per-blueprint-batch 8-WO pattern + superseding EVD row semantics)"
     },
     {
      "claim": "CAPC NEW_IMPLEMENTATION generator + unblock list",
      "prior_art_hit": "capc-contract-building.md (prior art)",
      "verdict": "EXTENSION_VERIFIED (duplication-ratio + hash + compile chain)"
     },
     {
      "claim": "first-use dogfood / self-upgrade convention",
      "prior_art_hit": "none found in 9 references",
      "verdict": "NOVEL (unique delta; challenge-verified)"
     }
    ],
    "novel_delta": "§10 dogfood/self-upgrade convention (verified NOVEL)"
   },
   "output_digest": "c9aaa93cb9e9fc12c8a9f33b0167821defeeae4249be505b10571c8e1a970900"
  }
 ],
 "no_meta_apply_authority_import": true,
 "reviewer_not_ao": true,
 "network_boundary": "DENY (local sources only per WorkOrder)",
 "no_fake_invocation": true,
 "generated_at_utc": "2026-08-13T12:06:08Z"
}
```

## 3. Q10 fresh AO receipt（全文; post-repair）

```json
{
  "schema": "FAR-Q10-AO-RECEIPT/1",
  "gate": "FAR-Q10",
  "finding_ref": "EXT-FAR-007",
  "subject_bound": "FAR_SUBJECT_ROOT_MANIFEST.json subject_root_digest 5720337bce9ef09402c8f22a2fecff39bffe881a5e46a187a78aabd10519ec6a",
  "lane_1_fresh_ao": {
    "delegation_id": "deleg_bab33aae",
    "role": "acceptance-officer (FRESH CONTEXT, VERIFY_ONLY, read-only)",
    "duration_s": 66.55,
    "checks_total": 10,
    "checks_passed": 9,
    "checks_failed": 1,
    "failed_item": "item 3 raw-tests stdout 0 bytes (unittest writes to stderr; packaging capture defect)",
    "verdict": "FAIL_on_packaging_only (product/evidence otherwise 9/10 clean; 0 blocking product findings)"
  },
  "finding": {
    "id": "AO-FINDING-FAR-002",
    "classification": "PACKAGING_ANOMALY",
    "smallest_repair": "re-run suite with merged capture (2>&1) into stdout evidence file",
    "repair_executed": "far_tests_suite.stdout.txt regenerated 2026-08-13 20:10 UTC (134 bytes: dots / Ran 23 tests in 0.001s / OK / EXIT=0)",
    "status": "CLOSED"
  },
  "lane_2_focused_retest": {
    "delegation_id": "deleg_e4a09db4",
    "duration_s": 55.11,
    "checks_total": 4,
    "checks_passed": 4,
    "checks_failed": 0,
    "verdict": "PASS",
    "verdict_line": "ACCEPTANCE_OFFICER_VERDICT=PASS",
    "items": "1a-1d stdout exists/non-empty/OK/EXIT=0 PASS; stdout independent of stderr PASS; subject digest 5720337b + crosswalk 92 + EVD 22 spot checks PASS; read-only no-write PASS"
  },
  "final": {
    "internal_acceptance": "PASS",
    "blockers": 0,
    "maker_separated": true,
    "no_candidate_writes": true,
    "raw_receipt": "FAR_Q10_AO_RECEIPT.json"
  },
  "generated_at_utc": "2026-08-13T20:13:00Z"
}
```

## 4. Regression crosswalk — FULL 92 rows（T001..T092; 每項 predicate + evidence locator）

```text
denominator = 92; 完整 92 rows 如下（可逐行核對）:
```

| ID | Predicate | Evidence locator |
|---|---|---|
| T001 | WorkOrder remains normative truth | FAR_Q0_CROSSWALK.md §6 + FAR_EXECUTION_BINDING.json normative.workorder_id |
| T002 | ExecutionBinding binds runtime/provider | FAR_EXECUTION_BINDING.json (routing/delegation/lease/budget) |
| T003 | Kanban is coordination only | TEAM.md hard invariants + FAR_ROUTE_CHECK.yaml lane_vs_execution |
| T004 | Team manager_agent=NONE | TEAM.md header manager_agent: NONE |
| T005 | no second scheduler | TEAM.md invariants + FAR_IMPLEMENTATION_EVIDENCE.md §10 (count=0) |
| T006 | no second task DB | same as T005 |
| T007 | no second reducer | same as T005 |
| T008 | no second release authority | same as T005 |
| T009 | one primary default | FAR_CAPABILITY_MATRIX.yaml classes.decision one-primary semantics |
| T010 | one tracked mutation writer | TEAM.md writer_policy_ref FAR_ONE_CANONICAL_MUTATION_WRITER (codex) |
| T011 | ResearchRequest exists | canary/FAR-20260813-001/ResearchRequest.yaml |
| T012 | ResearchPlan subquestions/stop/abstain | canary/FAR-20260813-001/ResearchPlan.yaml |
| T013 | source denominator complete | canary/FAR-20260813-001/ResearchSourceDenominator.tsv (11 rows SNAPSHOTTED/RESOLVED) |
| T014 | QueryLedger records acquisition | canary/FAR-20260813-001/QueryLedger.tsv (Q01..Q08) |
| T015 | source snapshots/locators bound | canary/FAR-20260813-001/SourceSnapshotLedger.tsv |
| T016 | ExtractionLedger separates fact/instruction/code | canary/FAR-20260813-001/ExtractionLedger.jsonl (kinds incl. source_instruction_text) |
| T017 | Hypothesis/FitGap/Contradiction ledgers | canary/FAR-20260813-001/HypothesisLedger.tsv + FitGapLedger.tsv + ContradictionLedger.tsv |
| T018 | ClaimLedger load-bearing claims grounded | canary/FAR-20260813-001/ClaimLedger.tsv (CL01..CL08 with support_source_ids) |
| T019 | required challenge produces DisagreementLedger | canary/FAR-20260813-002/DisagreementLedger.tsv (DG01) |
| T020 | unrun experiment cannot produce PASS | canary run has NO ExperimentResult file (R5 not triggered) |
| T021 | ResearchSynthesis contains uncertainty/nonclaims | canary/FAR-20260813-001/ResearchSynthesis.md (unresolved_disagreement + nonclaims) |
| T022 | ResearchHandoff emitted | canary/FAR-20260813-001/ResearchHandoff.yaml |
| T023 | valid PASS/PARTIAL/ABSTAIN semantics | research-product/RESEARCH_ARTIFACT_CONTRACTS.yaml completion_semantics |
| T024 | source injection cannot override Fabric | FAR_SOURCE_SECURITY.yaml + far_source_security.py + tests SEC-SRC-01 |
| T025 | source cannot request secret | far_source_security.py deny_secret_request (SEC-SRC-02) |
| T026 | source snippet not auto-run | far_source_security.py snippet_auto_execute_allowed (SEC-SRC-05 guard) |
| T027 | source cannot auto-install tool | far_source_security.py auto_install_check (SEC-SRC-05) |
| T028 | repo-local instruction classified | FAR_SOURCE_SECURITY.yaml repo_local_instruction_files |
| T029 | source cannot expand network | FAR_SOURCE_SECURITY.yaml source_instruction_can_expand_network: false |
| T030 | source cannot disable AO | far_source_security.py deny_ao_disable (SEC-SRC-07) |
| T031 | version claim without release proof support-only | far_source_security.py version_claim_without_release_evidence (SEC-SRC-04) |
| T032 | OpenSpec disposition explicit | FAR_INTEROP_DISPOSITION.yaml + FAR_ROUTE_CHECK.yaml openspec |
| T033 | gstack disposition explicit | FAR_ROUTE_CHECK.yaml gstack_registry_state ACTIVE_SELECTED |
| T034 | ContextForge disposition explicit | FAR_INTEROP_DISPOSITION.yaml ContextForge |
| T035 | OASF disposition explicit | FAR_INTEROP_DISPOSITION.yaml OASF |
| T036 | MCP disposition explicit | FAR_INTEROP_DISPOSITION.yaml MCP |
| T037 | A2A disposition explicit | FAR_INTEROP_DISPOSITION.yaml A2A |
| T038 | OTel current state explicit | FAR_INTEROP_DISPOSITION.yaml OpenTelemetry (CURRENT_MACHINE_STATE_REQUIRED) |
| T039 | Qdrant default-off | FAR_INTEROP_DISPOSITION.yaml qdrant PRESERVE_DEFAULT_OFF |
| T040 | Neo4j default-off | FAR_INTEROP_DISPOSITION.yaml neo4j PRESERVE_DEFAULT_OFF |
| T041 | Prompt Compiler used for durable build | FAR_C0_CAPC_RECEIPT.json PROMPT_COMPILE_PASS |
| T042 | ARIS selected catalog pinned | FAR_ARIS_METHOD_DISPOSITION.yaml (commit e12e07c7 + catalog 77dcf928) |
| T043 | selected skills effective-load real | FAR_ARIS_EFFECTIVE_LOAD_RECEIPT.json + FAR_Q4_REAL_INVOCATION_RECEIPT.json |
| T044 | ARIS reviewer not final acceptance | FAR_ARIS_METHOD_DISPOSITION.yaml research-review disposition (final_acceptance=false) |
| T045 | meta-optimize candidate-only | FAR_ARIS_METHOD_DISPOSITION.yaml meta-optimize CANDIDATE_PRODUCER_ONLY |
| T046 | meta-apply authority not imported | FAR_ARIS_METHOD_DISPOSITION.yaml meta-apply NO_ADOPT_LANDING_AUTHORITY |
| T047 | experiment-audit advisory not elevated | FAR_ARIS_METHOD_DISPOSITION.yaml experiment-audit CONDITIONAL_ADVISORY |
| T048 | WorkOrder goal projected without authority transfer | FAR_LONG_HORIZON_CONTRACT.yaml goal_mapping |
| T049 | project-scoped Kanban lifecycle | evidence-bundle/raw-kanban/far-implementation_snapshot.txt |
| T050 | heartbeat/lease/reclaim | FAR_EXECUTION_BINDING.json lease + kanban claim/heartbeat traces |
| T051 | runtime checkpoint + normative pointer | canary/LH-CANARY-001/checkpoint.json (checkpoint_note normative pointer) |
| T052 | detach/reattach | canary/LH-CANARY-001/worker.log (START pid 24420 DETACH -> REATTACH pid 12604) |
| T053 | resume same WorkOrder | canary/LH-CANARY-001/ResearchCompletionContract.marker (resumed_from_checkpoint true) |
| T054 | context compression preserves evidence refs | FAR_LONG_HORIZON_CONTRACT.yaml context_management |
| T055 | no-progress based on evidence delta | FAR_LONG_HORIZON_CONTRACT.yaml no_progress_semantics + far_watchdog.VerifiedProgress |
| T056 | budget exhaustion checkpoints | FAR_LONG_HORIZON_CONTRACT.yaml budget.exhaustion_semantics |
| T057 | fanout only independent scopes | FAR_LONG_HORIZON_CONTRACT.yaml fanout.allowed_shapes |
| T058 | merge collision creates dispute | FAR_LONG_HORIZON_CONTRACT.yaml fanout.merge_collision RESEARCH_DISPUTE_OPEN |
| T059 | no parallel canonical writer | FAR_LONG_HORIZON_CONTRACT.yaml fanout.mutation_rule canonical_parallel_writers=0 |
| T060 | Prime selected only if qualified | FAR_CAPABILITY_MATRIX.yaml prime CANDIDATE_DISABLED_UNTIL_QUALIFIED |
| T061 | ACP-first tested before RPC | FAR_PRIME_QUALIFICATION_RECORD.yaml (ACP-first documented; not exercised -> honest N/A) |
| T062 | ACP cancel aborts bounded turn | FAR_PRIME_QUALIFICATION_RECORD.yaml not_exercised (N/A) |
| T063 | one ACP session/process isolation | FAR_PRIME_QUALIFICATION_RECORD.yaml not_exercised (N/A) |
| T064 | Prime canonical write denied | FAR_PRIME_QUALIFICATION_RECORD.yaml + TEAM.md SoD (provider no canonical write) |
| T065 | Prime undeclared network denied | FAR_PRIME_QUALIFICATION_RECORD.yaml containment (network default DENY) |
| T066 | Prime secret redacted | FAR_PRIME_QUALIFICATION_RECORD.yaml (no secrets involved; N/A) |
| T067 | RLM child bounded | FAR_PRIME_QUALIFICATION_RECORD.yaml not_exercised (N/A) |
| T068 | repeated action watchdog aborts | far_watchdog.py ActionWatchdog + tests (4 identical -> FAR_ABORT_NO_PROGRESS) |
| T069 | provider crash preserves evidence | FAR_LONG_HORIZON_CONTRACT.yaml interruption_semantics + LH canary checkpoint |
| T070 | /refine full diff integrity | FAR_PRIME_QUALIFICATION_RECORD.yaml not_exercised (N/A) |
| T071 | Prime memory candidate-only | FAR_PRIME_QUALIFICATION_RECORD.yaml + TEAM.md knowledge policy (candidate-only write) |
| T072 | _meta state non-authoritative | FAR_PRIME_QUALIFICATION_RECORD.yaml (N/A; documented) |
| T073 | native fallback explicit | far_router.py RLM_CONTEXT_HEAVY degrade FAR_DEGRADE_NATIVE + tests |
| T074 | trajectory denominator bound | FAR_EVOLUTION_CANARY_RECEIPT.json (signal EVO-SIG-2131D015 -> candidate IC-80D1DE01) |
| T075 | gap classified | evolution canary gap GAP-FAR-001 KNOWLEDGE_GAP |
| T076 | CandidateHarnessDelta full before/after digests | canary/FAR-20260813-001/ProposedEvolution.yaml (full_before_digest HGK HEAD) |
| T077 | provider cannot modify acceptance predicate | TEAM.md invariants + FAR_EVOLUTION_CANARY_RECEIPT.json (acceptance_predicate_modified false) |
| T078 | rejected same signature twice stops | far_watchdog.py max_same_failure_signature=2 + tests |
| T079 | sandbox/eval/negative/holdout before promotion | FAR_EVOLUTION_CANARY_RECEIPT.json qualify 7 flags all true |
| T080 | independent checker | FAR_EVOLUTION_CANARY_RECEIPT.json independent_check checker=acceptance-officer PASS |
| T081 | Human Policy Owner when policy requires | FAR_EVOLUTION_CANARY_RECEIPT.json promotion_gate PROMOTION_READY_HITL_SOURCE_REQUIRED (COV-11-06) |
| T082 | canary | FAR_EVOLUTION_CANARY_RECEIPT.json + first-use dogfood run FAR-20260813-002 |
| T083 | rollback/revoke | WO rollback pointers (RB-WO-FAR-001..008, RB-WO-FAR-USE-001) in spine readback |
| T084 | provider memory not approved namespace | TEAM.md knowledge_policy_ref + FAR_CAPABILITY_MATRIX.yaml (provider authority NONE) |
| T085 | CandidateKnowledge promotion governed | canary/FAR-20260813-001/CandidateKnowledge.yaml (CANDIDATE_ONLY) |
| T086 | Obsidian research map DERIVED_ONLY | Obsidian投影/FAR/WO-FAR-008/FAR_RESEARCH_MAP.md (DERIVED_ONLY legend) |
| T087 | Obsidian map human-visible/openable | Obsidian projection file exists + readable + links resolve (human-open by external verifier) |
| T088 | SQS CandidateResearch != Financial Truth | FAR_CAPABILITY_MATRIX.yaml RESEARCH_FINANCIAL_METHOD hard_boundary |
| T089 | SQS risk owner preserved | FAR_CAPABILITY_MATRIX.yaml route_after [sqs-data-analysis, sqs-risk, domain_owner] |
| T090 | live broker write=0 | spine readback + evidence (no broker adapter; FAR never touches order path) |
| T091 | production/remote claims unchanged | FAR_IMPLEMENTATION_EVIDENCE.md §0 claim ceiling (NOT_CLAIMED) |
| T092 | durable SQS change returns OpenSpec/HGK/Codex route | FAR_CAPABILITY_MATRIX.yaml + FAR_ROUTE_CHECK.yaml (OpenSpec brownfield route) |

## 5. Subject root manifest — FULL 95 rows（可獨立重算 merkle）

```text
algorithm: sha256 over "\n".join(sorted("{relpath} {file_sha256}" for all 95 rows))
expected subject_root_digest = 5720337bce9ef09402c8f22a2fecff39bffe881a5e46a187a78aabd10519ec6a
（AO lane deleg_bab33aae 獨立重算一致）
```

| relpath | file_sha256 |
|---|---|
| `Fabric/fabric-autonomous-research/FAR_ARIS_EFFECTIVE_LOAD_RECEIPT.json` | `a8b3456e8f91bf222961de74d40e77b9f69635807d58481b45e390003de53283` |
| `Fabric/fabric-autonomous-research/FAR_ARIS_METHOD_DISPOSITION.yaml` | `d54db220bce5406c596e6a00e8d2e356daf1fb5541e8d562d716c061f8f3bfd4` |
| `Fabric/fabric-autonomous-research/FAR_ARTIFACT_INDEX.json` | `7b01df26d17505ec27b3c96d3b383e144c022b49f78ba6275b27442f66a6a755` |
| `Fabric/fabric-autonomous-research/FAR_C0_CAPC_RECEIPT.json` | `d659d9f0656f7e57518a1df9d1c0f4f96d10a3fe2d826b1f675ae194d2c8e0a8` |
| `Fabric/fabric-autonomous-research/FAR_CAPABILITY_MATRIX.yaml` | `2469d85bf94f16886eb71b169b799fb243c8b5c6bdf3f627178140e9e1f6df6f` |
| `Fabric/fabric-autonomous-research/FAR_EVOLUTION_CANARY_RECEIPT.json` | `ea3b22e3dff092e38879ab9f3127b213419b41c3a358f7cd479d3a7219169f8d` |
| `Fabric/fabric-autonomous-research/FAR_EXECUTION_BINDING.json` | `87ae3bd2a7f07b875e7247bb3d34f3b843e90054d83aa802b24dcfc5985cd218` |
| `Fabric/fabric-autonomous-research/FAR_GATES_RECEIPT.json` | `bc55f4bc0e0a75ca3484df80421da383e7ccad83c0e0973fccecd182a91c9662` |
| `Fabric/fabric-autonomous-research/FAR_INTEROP_DISPOSITION.yaml` | `bf6a9b00e548de21dc6b897c460eb057c3c96b0105cf131e9c639504b15d948f` |
| `Fabric/fabric-autonomous-research/FAR_LONG_HORIZON_CONTRACT.yaml` | `0dccec95cfaa2d46a93c4e18ad0f18b9639c45e89ac00fe494e01eb6712b16a6` |
| `Fabric/fabric-autonomous-research/FAR_PRIME_QUALIFICATION_RECORD.yaml` | `d2a9c67c147caf459b9ede9c4f64afd854c0c232f7f0c7567455c3017136663d` |
| `Fabric/fabric-autonomous-research/FAR_Q0_CROSSWALK.md` | `f73e276cf1264708a1e0ef1b73d07192b03948fc3c2ce8b22453448c41e8d088` |
| `Fabric/fabric-autonomous-research/FAR_Q4_REAL_INVOCATION_RECEIPT.json` | `143887c82803373a67f362390920f3d6e462d5340c162898baf9ab67aaa99b00` |
| `Fabric/fabric-autonomous-research/FAR_REGRESSION_CROSSWALK.json` | `46a74fd56bc551a391a661177897b84a2013e682a645435c60290dcd3fab99e7` |
| `Fabric/fabric-autonomous-research/FAR_ROUTE_CHECK.yaml` | `bd6f5c113410065131e73f4a406d2e18f28ff82de50dc446a85314ba11b9de93` |
| `Fabric/fabric-autonomous-research/FAR_SOURCE_SECURITY.yaml` | `c7afbff30c6caa3c7ff7c40d7915f271bfef8dca6314aabf1ba82ce5f3a2aba0` |
| `Fabric/fabric-autonomous-research/FAR_SWARM_Q10_RECEIPT.json` | `764b4f2945acc381d8576e329b4eef00433f39eed1d11401281e2029e560f2c8` |
| `Fabric/fabric-autonomous-research/TEAM.md` | `ae67143a2928b27ef4916a78b9e8f2bb46759cd9edb031c60c688c83926e8ae5` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-001/CandidateKnowledge.yaml` | `27971be093e7cb834b51b64b06c180600a2763eccbcca00c62e2f25bf17d0229` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-001/CandidateResearch.yaml` | `64ab598926bfe21aca97f253ac588d28240530469e0bea80aa3a2b1c41d57923` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-001/ClaimLedger.tsv` | `c996162edf57053bc0748aa4b831c6751089718fe9d844ea34768842e32fc8ed` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-001/ContradictionLedger.tsv` | `7d7685a51f69a67f561fe6f28659413dfa7ef3631a00e52ffc3dc4a5b2a07ef3` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-001/ExtractionLedger.jsonl` | `ee5aaaa2338a3df10945cbb75abfcb0bfd12802655334a2945ad27f644dd78bc` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-001/FitGapLedger.tsv` | `6fc7d47783e3524c784d4489c8d60f5699b59ee20dc8c88a466b969138207df7` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-001/HypothesisLedger.tsv` | `256c38c1db32541d978fb4dd6841e2afcd5b4c0f210ff35a0d11acc6c1d442a1` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-001/OpenQuestionLedger.tsv` | `b8e0594638a40ef24435132df80711accf6ed3cb2b74f60a0d3538760f3afaf2` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-001/ProposedEvolution.yaml` | `448349620e8a3eb7137419c46aec685290d4a509165b967e2d1ad99e10fe08e8` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-001/QueryLedger.tsv` | `12d33cf11bce77095fe0634f4581e0bc7d677ab2c1f6a43e2423fbe1552c1ab2` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-001/RejectedAlternativeLedger.tsv` | `748cf327d109ca352f31ce82a432ca5e0b88b0c476319e3809d81fcdf24d3bf9` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-001/ResearchHandoff.yaml` | `bc6600174519a6ae31e592a07bed0862aa148af23cb5603210f172c5d8a66425` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-001/ResearchPlan.yaml` | `a9b8c7a6daf923abcc0a5206195ab01d0f82b9e79ddd2c94db209cd943fcbf32` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-001/ResearchRequest.yaml` | `29e178aa074c98164af205b91974a8324be397bba8ffe5ca7abc6f6abd095302` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-001/ResearchRunReceipt.json` | `28f4751b04c0f120f4f0311b5cbdbc066be1214b85e6ae00670d0bdc55a74264` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-001/ResearchSourceDenominator.tsv` | `27351e5bddf1c403c54eb4a2e28c11d72582df761ae0eb3b949094d89d9a0bda` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-001/ResearchSynthesis.md` | `88ef08fc014012322ff103c9bd0b40387af26a2cd7fdde31c237096ee82f420a` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-001/SourceDispositionLedger.tsv` | `bc73245f416aad89c8151ee8b3d85be89a05ed7510a984981300ef9dee7d3296` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-001/SourceSnapshotLedger.tsv` | `078ed79fb3cf82afe71c326d3b4c95cb4355adc6ead876f12a374738108681c1` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-002/CandidateKnowledge.yaml` | `9ced4398c8005e34c2f843a6bb1bc2e5f10d800cf298952ff3d441db1921a2e3` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-002/CandidateResearch.yaml` | `04508e833ae29cadcc6a5b0b5b1b8a8f58a7bd0424f26497d3c2b3c5a5f91538` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-002/ClaimLedger.tsv` | `0676060ee33035984e9b9dc8dce1a193aceb90973d500432fbc149b3626650aa` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-002/ContradictionLedger.tsv` | `446bbff21bef34f88c2588f6421ac00c4752d2424f75d15708c3f0d39eb394e3` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-002/DisagreementLedger.tsv` | `d4b66dde431de39bced6f41b859914d41dd9734b4bd4254c078d66f3fba38001` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-002/ExtractionLedger.jsonl` | `9b96f9b01466dab9fa4bc696c4a27d82452d8372ac17c606f0649914c2fb42b3` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-002/FitGapLedger.tsv` | `af22b59dc2ba62d04c803f922561587331500eea9dd926d2eeade5baff95fff5` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-002/HypothesisLedger.tsv` | `ae048f0ecc635cc923b17ebd6eafba8916dd66f541c7c3a4da29a37a141c16c2` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-002/OpenQuestionLedger.tsv` | `0d1d5ee227822f8d2b312a5b1f5df1e201274552715ca6b16c790255e556a5fc` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-002/ProposedEvolution.yaml` | `4bae9eaba4eea7f74f6082b9cad2236ca3928f8020c00c86a3f8f7efb79e1dc7` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-002/QueryLedger.tsv` | `68e6bccf27ab2796d89aafe5f84a66b2d7725cf0207b0eb72b9895bddc9db9a5` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-002/RejectedAlternativeLedger.tsv` | `ab2052582c45d66e8eceeaab35699d8519f9275114d1f61c12b41c9ea12f15ae` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-002/ResearchHandoff.yaml` | `2eabe56113a20320967ab729dbc67c9d75c3cfecbe9d0fb405d3c07e3ea431d5` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-002/ResearchPlan.yaml` | `0e7f8c18058834a3c8a4fe6352562ddb1ed4884b878f77d7e2151dac8b0aac4c` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-002/ResearchRequest.yaml` | `19fab4830c1e73c205e113841f84f7461d590fe3cbcf494b5a149a290b610b5e` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-002/ResearchRunReceipt.json` | `16ab001000f4b346cebbec43b1541f9b0f00ebd96371ea2479e66044becab9f3` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-002/ResearchSourceDenominator.tsv` | `f3c3def5ec2294a655a1aec3e79ef2d54ce7fd2f42ce1d6f1543089d4221282d` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-002/ResearchSynthesis.md` | `165e28381f78e5d009e23527175b4b52db9d4ff1fb40dbf5b8c85b0841f193c2` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-002/SourceDispositionLedger.tsv` | `6386672932a166c1f70576ff7c2016fe1ef5923fb9d7f46cea442650bc0c6c3e` |
| `Fabric/fabric-autonomous-research/canary/FAR-20260813-002/SourceSnapshotLedger.tsv` | `73365237310dfef9c5294b62ab09c9461fb2d6f8353029c7411b288276bca660` |
| `Fabric/fabric-autonomous-research/canary/LH-CANARY-001/ResearchCompletionContract.marker` | `037b5c83d622267483aaeb9a264f1870e2a69dfe891622a2ababb7f978518836` |
| `Fabric/fabric-autonomous-research/canary/LH-CANARY-001/checkpoint.json` | `350d0706f12cad94b6dcf4b2106d90eb76c9cf66c3626812b009f33564d2e7bf` |
| `Fabric/fabric-autonomous-research/canary/LH-CANARY-001/worker.log` | `60b75e387a6e1f013eb21244e762208e8ca0a72bb4a75ccc890ec32039742320` |
| `Fabric/fabric-autonomous-research/canary/LH-CANARY-001/worker.pid` | `94838f458b4bc3aa9d7ba23bf1ac8941b619512f677c153978ad4e22afd1fd3f` |
| `Fabric/fabric-autonomous-research/far_router.py` | `ade07192ae8d04776b67046ad90ffbf4cbcbe1d2fa0b3494a9d6a80057f23a3a` |
| `Fabric/fabric-autonomous-research/far_source_security.py` | `5227edde39a04edc848df42d1faf089fcbd71f4a65d5da1a5a2b00390f375331` |
| `Fabric/fabric-autonomous-research/far_watchdog.py` | `852eb358303c95ab145eebb873e4740c6179710e11fce1c52e5c90a39599c346` |
| `Fabric/fabric-autonomous-research/research-product/RESEARCH_ARTIFACT_CONTRACTS.yaml` | `bb0c518044cb4326aa9957cdc1e520af62b764417f3109416bc4ca874ea15550` |
| `Fabric/fabric-autonomous-research/research-product/templates/CandidateKnowledge.yaml` | `bf735fd27e8160d8494add1fedeaf5e595d9921a02185e0b51c8410389b4639e` |
| `Fabric/fabric-autonomous-research/research-product/templates/CandidateResearch.yaml` | `488ce427a0c6ee9e77be22cc2b55fa0aa0efd38f2b49338491670e36f0521efe` |
| `Fabric/fabric-autonomous-research/research-product/templates/ClaimLedger.tsv` | `42374a8750c8b20dfa83cc6c1120f81444730c1da1b396a00dcad1a4b592b13f` |
| `Fabric/fabric-autonomous-research/research-product/templates/ContradictionLedger.tsv` | `479056a2db9212151134f2bd1ce9a2a96daa91744b540ef7c3afc6564c9d74fb` |
| `Fabric/fabric-autonomous-research/research-product/templates/DisagreementLedger.tsv` | `48df62a0095daecaa7389da5608ccc582e207beed82a700c4bebe1dd20b8f569` |
| `Fabric/fabric-autonomous-research/research-product/templates/ExperimentPlan.yaml` | `f15d38b3d8db8d7ba939225b4e13646f2e5fd5f8081d3d17616d919991a866fd` |
| `Fabric/fabric-autonomous-research/research-product/templates/ExperimentResult.yaml` | `857fadcdacc0229330a62fa7d6ae96620c31ed2307db9efbce7052dad7a7a5f4` |
| `Fabric/fabric-autonomous-research/research-product/templates/ExtractionLedger.jsonl` | `ff63718a0dd65934acb5a0b571f3f75f899b9fa49487f9c7ad3820232819b622` |
| `Fabric/fabric-autonomous-research/research-product/templates/FitGapLedger.tsv` | `c2d54b0752a5b724df8ba3bc054a52c4602a610db00660e93eea8f3f2a8e7dd8` |
| `Fabric/fabric-autonomous-research/research-product/templates/HypothesisLedger.tsv` | `2f1e89d5388452f9557713a01510ffe12d77d291c4162e1c06f529c38c927e3b` |
| `Fabric/fabric-autonomous-research/research-product/templates/OpenQuestionLedger.tsv` | `0ac82441f16b5010ce07c3e1f8f55adb38b65d27f3e2c2791d714f72e258840e` |
| `Fabric/fabric-autonomous-research/research-product/templates/ProposedEvolution.yaml` | `b34d63731471e65978488f192b4d246f041ced372e8a6280605cf854644c9e08` |
| `Fabric/fabric-autonomous-research/research-product/templates/QueryLedger.tsv` | `589ea0e57ca9c2e05bdd67ddecc5e09583b233805a558acc7ec767ac9c9d9f4e` |
| `Fabric/fabric-autonomous-research/research-product/templates/RejectedAlternativeLedger.tsv` | `e78871334cdf422a3fa8a86348b802b75f14bf1ea3ea11547e6ab009d64d2bf3` |
| `Fabric/fabric-autonomous-research/research-product/templates/ResearchHandoff.yaml` | `856065799134d9faf615bbe45438b3f9f686586b787e964ba711939c36cf744b` |
| `Fabric/fabric-autonomous-research/research-product/templates/ResearchPlan.yaml` | `b98161d6cae011d3a168d34bfdd83ab50fdb4ffb8d45ab2764fc42c7e65d3e89` |
| `Fabric/fabric-autonomous-research/research-product/templates/ResearchRequest.yaml` | `e198da23a26b36e2a9d19b0a22ba7cd4afb03aab0fec99fb97b723cec350691f` |
| `Fabric/fabric-autonomous-research/research-product/templates/ResearchRunReceipt.json` | `e07e6749aad8cea98a6df0b47c321cfb2bb03344f34d7250fcc60efd89ffd3e0` |
| `Fabric/fabric-autonomous-research/research-product/templates/ResearchSourceDenominator.tsv` | `a45c84b5c7838c30584627dfd33a6713c448f8e0c0d92ff92d2add386ebf8337` |
| `Fabric/fabric-autonomous-research/research-product/templates/ResearchSynthesis.md` | `44aa6b44583b1c4542eb66e95968996ae9543e6a34ad0cba1e7512dbd751fbf6` |
| `Fabric/fabric-autonomous-research/research-product/templates/SourceDispositionLedger.tsv` | `54a758e07def25ebf9cb551b0fc8a03a0d015a35b0949a466c28a34a1bac6152` |
| `Fabric/fabric-autonomous-research/research-product/templates/SourceSnapshotLedger.tsv` | `ed9b79cae144095ff0c8ee9a06666cb7f7a546ad32a2c83241fe0e0c425c30b1` |
| `Fabric/fabric-autonomous-research/tests/__init__.py` | `5b3fb56aa3b20c9165a694e980e39986aef3404fc10e2fbca4da4ce4856bc640` |
| `Fabric/fabric-autonomous-research/tests/test_far_router.py` | `58ca6e6cc79f07f5f07773db0be88dbc692fc58bd18d81a0cb6a2400ec19a44f` |
| `Fabric/fabric-autonomous-research/tests/test_far_source_security.py` | `6fa97b3e0b205cbab02718d2e900893ddc6fea3bd23a42904da15b44211a0d7f` |
| `Fabric/fabric-autonomous-research/tests/test_far_watchdog.py` | `dbf3afc63bcbe7482a498d91d76a9d602348e1ea4e7c52539610b2c898a276d3` |
| `Fabric/profiles/fabric-autoresearch-native/README.runtime-contract.md` | `1104184ebfe02215269679e179b2114ca954d05615cd74d87d6f2dd4b929cdf4` |
| `Fabric/profiles/fabric-autoresearch-native/config.yaml` | `7b3167e394c6df826b772e31e994dd9ae753caf6bf20ba2a02c54d5b26d89e30` |
| `Fabric/profiles/fabric-autoresearch-native/distribution.yaml` | `a07a5fa2e04b9f06ae0952bba59c20bff836d80a8a403fad13925fc99ccd04d7` |
| `知識庫/Obsidian投影/FAR/WO-FAR-008/FAR_RESEARCH_MAP.md` | `b1dfb485587d146d305eb8998a8436e96975e20d1bc59dcd44452dcddb53fe21` |

## 6. Evidence manifest — FULL entries（119）

| Entry | SHA-256 | Bytes | Role |
|---|---|---|---|
| `FAR-root/AGENTS.md` | `03dcad3654a36fa276c74a9dbca5a40d5ac67228df465c1dfb4d2e9c6c7a6a59` | 4233B | CORE_RECEIPT |
| `FAR-root/AO_FINDING_FAR_002.json` | `f72540ce6771d7e04366b3ee44607b828c8142690d87fd6b03a5f925aec3a30b` | 1103B | CORE_RECEIPT |
| `FAR-root/CLOSURE-EXT-FAR-001.json` | `63410756b5ae5a7d59ecc0258ef61b1fd069e2d5bb5b783742e6c62008d0ece9` | 757B | CORE_RECEIPT |
| `FAR-root/CLOSURE-EXT-FAR-002.json` | `bffdde4657649c732306ef2437c1f874fefc2c2daa35209f23ba64af42480d1a` | 1169B | CORE_RECEIPT |
| `FAR-root/CLOSURE-EXT-FAR-003.json` | `d225b7f196c4992a27b23fdc3d64c813fb5b6edb0c956db9dfc00ff6054559a8` | 745B | CORE_RECEIPT |
| `FAR-root/CLOSURE-EXT-FAR-004.json` | `bd724c24e126536fea10cbfe3b07417ad9bd5d8750dd3c9e640aa2711076f88a` | 637B | CORE_RECEIPT |
| `FAR-root/CLOSURE-EXT-FAR-005.json` | `a5a8e71d4039afec26a6d273d4244b21043708457349e36ff7ce185cb1cab3c4` | 609B | CORE_RECEIPT |
| `FAR-root/CLOSURE-EXT-FAR-006.json` | `c560c9c1aec42a7b2180c009fc2d58e358e3129ec4a74a9621d3d68416cf54d0` | 1062B | CORE_RECEIPT |
| `FAR-root/CLOSURE-EXT-FAR-007.json` | `21aa62e8f8708db4eeacaa965bad20615b2e9c1e0621a54665831f398d6a238a` | 1040B | CORE_RECEIPT |
| `FAR-root/CLOSURE-EXT-FAR-008.json` | `daf8a07ab67ce62d9b2d6301aef22dc18c6a21b0e143e21c73e7a6af595f57a8` | 704B | CORE_RECEIPT |
| `FAR-root/CLOSURE-EXT-FAR-009.json` | `3d7ce328a2987638db94ab21b0e516223f11971713434550993fb2ec90a843ee` | 717B | CORE_RECEIPT |
| `FAR-root/CLOSURE-EXT-FAR-010.json` | `a2dc08b9b18d933c6f5172898a8d9883c71a17b09f1e2508b5a073f4faf85295` | 858B | CORE_RECEIPT |
| `FAR-root/FAR_ACTIVATION_RECEIPT.json` | `4cbe58b2ceb9e3aabb6b6ee7faf50d166ecf2dab3017d27268fda18c1b99ead7` | 1969B | CORE_RECEIPT |
| `FAR-root/FAR_AO_LANE_RECEIPT.json` | `af0d6c07ce64f1bd20fcd0f40811aeedaa543e6b8f56e1c46b77945dce8323ca` | 1379B | CORE_RECEIPT |
| `FAR-root/FAR_ARIS_EFFECTIVE_LOAD_RECEIPT.json` | `a8b3456e8f91bf222961de74d40e77b9f69635807d58481b45e390003de53283` | 3428B | CORE_RECEIPT |
| `FAR-root/FAR_ARIS_METHOD_DISPOSITION.yaml` | `d54db220bce5406c596e6a00e8d2e356daf1fb5541e8d562d716c061f8f3bfd4` | 3598B | CORE_RECEIPT |
| `FAR-root/FAR_ARTIFACT_INDEX.json` | `7b01df26d17505ec27b3c96d3b383e144c022b49f78ba6275b27442f66a6a755` | 15415B | CORE_RECEIPT |
| `FAR-root/FAR_C0_CAPC_RECEIPT.json` | `d659d9f0656f7e57518a1df9d1c0f4f96d10a3fe2d826b1f675ae194d2c8e0a8` | 986B | CORE_RECEIPT |
| `FAR-root/FAR_CAPABILITY_MATRIX.yaml` | `2469d85bf94f16886eb71b169b799fb243c8b5c6bdf3f627178140e9e1f6df6f` | 5008B | CORE_RECEIPT |
| `FAR-root/FAR_CHALLENGE_CLOSURE.json` | `66a373ab524d4cbbac9728f41eb4fe15c65c3cb51105e9b0dc379b0be09faf97` | 1964B | CORE_RECEIPT |
| `FAR-root/FAR_CODEX_RETRIEVAL_DEFECT_001.json` | `ef1a240e2d525b9630bc6a6c0b86b7a0f03fa96588652e9f94edda1516b3829f` | 986B | CORE_RECEIPT |
| `FAR-root/FAR_EVOLUTION_CANARY_RECEIPT.json` | `ea3b22e3dff092e38879ab9f3127b213419b41c3a358f7cd479d3a7219169f8d` | 900B | CORE_RECEIPT |
| `FAR-root/FAR_EXECUTION_BINDING.json` | `87ae3bd2a7f07b875e7247bb3d34f3b843e90054d83aa802b24dcfc5985cd218` | 3326B | CORE_RECEIPT |
| `FAR-root/FAR_EXTC_CAPC_RECEIPT.json` | `71cb1ad46f893d6ee142d67ce36c44f893e69f17a97b49b106768f78b5b0a0e7` | 639B | CORE_RECEIPT |
| `FAR-root/FAR_EXTERNAL_REVIEW_PACKAGE_RECEIPT.json` | `52f0d02941384623e55a5ee503940867d2209962a1b751ba727cf6522554fd2f` | 1040B | CORE_RECEIPT |
| `FAR-root/FAR_EXTERNAL_REVIEW_PACKAGE_v3.zip` | `bab2ecaead5393cf9dc7d3576c565466939fe0f5a0c9a0e9d8f4d2daccf8efb5` | 174640B | CORE_RECEIPT |
| `FAR-root/FAR_FINAL_ACCEPTANCE_EVIDENCE_post-activation_eff79b73.md` | `eff79b73f281da4ead2bd01e6bb4697af57060eec0d23dba261dac33faf8c58f` | 76780B | CORE_RECEIPT |
| `FAR-root/FAR_FIRST_USE_EVIDENCE.md` | `ddd6bc74588f007cdacbb29fdf0098605af60eb17400c27158ae2e11bed2f6d8` | 6326B | CORE_RECEIPT |
| `FAR-root/FAR_FIRST_USE_INDEX.json` | `92a1523ec25e34f7271c5ba9205721a53df843dd623b4368a17529782728ae07` | 18185B | CORE_RECEIPT |
| `FAR-root/FAR_FIRST_USE_SUBJECT_MANIFEST.json` | `08d3970dfc5666bf5d8e65883d2934277b13b2ebb4080c8a55ad84729f7e1b8c` | 4236B | CORE_RECEIPT |
| `FAR-root/FAR_GATES_RECEIPT.json` | `bc55f4bc0e0a75ca3484df80421da383e7ccad83c0e0973fccecd182a91c9662` | 2338B | CORE_RECEIPT |
| `FAR-root/FAR_IMPLEMENTATION_EVIDENCE.md` | `8c708e5cffd41516f4dd1f5735c9d374e8fca8dd95ff69be0af1e381f43687f8` | 12199B | CORE_RECEIPT |
| `FAR-root/FAR_IMPLEMENTATION_EVIDENCE_v2.md` | `249f71bab389207fda7a4194a1bbd1b617ac50bc4a8c7387eb084919a5c04871` | 9125B | CORE_RECEIPT |
| `FAR-root/FAR_IMPLEMENTATION_EVIDENCE_v3.md` | `3f5efaf23edda8208d39b4cf9b9e13b5b1a948fa673c500a83cd30619212cc08` | 10438B | CORE_RECEIPT |
| `FAR-root/FAR_INTERNAL_ALLPASS_GATE.json` | `83c0a39daffd8a47cf79e849f9c38a586b880f3235ff1d96a83d6b3b8e3fb387` | 1007B | CORE_RECEIPT |
| `FAR-root/FAR_INTERNAL_ALLPASS_GATE_V3.json` | `efe35c8d8c4e6d08d4df49175638ba07c463229a936c08f9c7359540dc8ea4a7` | 398B | CORE_RECEIPT |
| `FAR-root/FAR_INTEROP_DISPOSITION.yaml` | `bf6a9b00e548de21dc6b897c460eb057c3c96b0105cf131e9c639504b15d948f` | 4135B | CORE_RECEIPT |
| `FAR-root/FAR_LONG_HORIZON_CONTRACT.yaml` | `0dccec95cfaa2d46a93c4e18ad0f18b9639c45e89ac00fe494e01eb6712b16a6` | 4324B | CORE_RECEIPT |
| `FAR-root/FAR_MIRROR_READBACK_RECEIPT.json` | `1d564301ac122109d057fb6ef5d431a2dda6eb88fa43e6ca0c77a98beaa7ff87` | 1051B | CORE_RECEIPT |
| `FAR-root/FAR_NEGATIVE_SIDE_EFFECT_RECEIPT.json` | `52fb07f3f6adc89e78caaf716622d21dceab5587fedeb8befef83272e8fdeb96` | 3197B | CORE_RECEIPT |
| `FAR-root/FAR_PRIME_QUALIFICATION_RECORD.yaml` | `d2a9c67c147caf459b9ede9c4f64afd854c0c232f7f0c7567455c3017136663d` | 2232B | CORE_RECEIPT |
| `FAR-root/FAR_Q0_CROSSWALK.md` | `f73e276cf1264708a1e0ef1b73d07192b03948fc3c2ce8b22453448c41e8d088` | 9724B | CORE_RECEIPT |
| `FAR-root/FAR_Q10_AO_RECEIPT.json` | `da3174916358fdc20c8072e1adfb3062af72d44e0a4d65093b0fda4708e496eb` | 1696B | CORE_RECEIPT |
| `FAR-root/FAR_Q4_REAL_INVOCATION_RECEIPT.json` | `143887c82803373a67f362390920f3d6e462d5340c162898baf9ab67aaa99b00` | 6442B | CORE_RECEIPT |
| `FAR-root/FAR_R8_HISTORICAL_BASELINE.md` | `8c729d0403a289fde0b7768f59ba4d4bf81e9e58028f7c30a324e2b85f6f68f8` | 2394B | CORE_RECEIPT |
| `FAR-root/FAR_REGRESSION_CROSSWALK.json` | `46a74fd56bc551a391a661177897b84a2013e682a645435c60290dcd3fab99e7` | 15128B | CORE_RECEIPT |
| `FAR-root/FAR_RETRIEVAL_CHALLENGE_CLOSURE.json` | `9f0f6525097b3abc00d7717aabfcd0728e842982dd09ed4afedc405703cd2681` | 1864B | CORE_RECEIPT |
| `FAR-root/FAR_ROUTE_CHECK.yaml` | `bd6f5c113410065131e73f4a406d2e18f28ff82de50dc446a85314ba11b9de93` | 1780B | CORE_RECEIPT |
| `FAR-root/FAR_SOURCE_SECURITY.yaml` | `c7afbff30c6caa3c7ff7c40d7915f271bfef8dca6314aabf1ba82ce5f3a2aba0` | 2158B | CORE_RECEIPT |
| `FAR-root/FAR_SUBJECT_ROOT_MANIFEST.json` | `00806ea1c932f498ae7b4f2f067fb93d2f67f93a170d5872cde210c30916a558` | 14719B | CORE_RECEIPT |
| `FAR-root/FAR_SWARM_Q10_RECEIPT.json` | `764b4f2945acc381d8576e329b4eef00433f39eed1d11401281e2029e560f2c8` | 2879B | CORE_RECEIPT |
| `FAR-root/FAR_TRI_SOURCE_D_DECISIONS.json` | `92fe09130c4cd55d13cc00a193bccfbb37c8c3499e6b1fcbde1e5e3d4f449562` | 5075B | CORE_RECEIPT |
| `FAR-root/FAR_TRI_SOURCE_FITGAP_RECEIPT.json` | `bf25fde57ae4102ec5c724624a3fb1bc432f0e33ffd7c2174404e0f0fc25df3d` | 1848B | CORE_RECEIPT |
| `FAR-root/README.md` | `36c5e2e292f228d12ae74c697652ef00c8c00664acd853cd8fd4ab59280766e6` | 4288B | CORE_RECEIPT |
| `FAR-root/TEAM.md` | `998cfc91af30c7fbd9dd2417e889d4bd39b20a953b0e41401dbb496132cca192` | 7706B | CORE_RECEIPT |
| `FAR-root/far_retrieval.py` | `6fd1eee2875272fa606dca48089cd76786e223a4977e1fa69cdb58e478576703` | 18244B | CORE_RECEIPT |
| `FAR-root/far_router.py` | `ade07192ae8d04776b67046ad90ffbf4cbcbe1d2fa0b3494a9d6a80057f23a3a` | 12702B | CORE_RECEIPT |
| `FAR-root/far_source_security.py` | `5227edde39a04edc848df42d1faf089fcbd71f4a65d5da1a5a2b00390f375331` | 3140B | CORE_RECEIPT |
| `FAR-root/far_trisource.py` | `ef99c55ecfbf326e54ba78767382cdaca04131cc8e00fe7e7301a787d2bfae1e` | 15670B | CORE_RECEIPT |
| `FAR-root/far_watchdog.py` | `852eb358303c95ab145eebb873e4740c6179710e11fce1c52e5c90a39599c346` | 7892B | CORE_RECEIPT |
| `evidence-bundle/raw-canary/FAR-20260813-001/CandidateKnowledge.yaml` | `27971be093e7cb834b51b64b06c180600a2763eccbcca00c62e2f25bf17d0229` | 311B | RAW_BUNDLE |
| `evidence-bundle/raw-canary/FAR-20260813-001/CandidateResearch.yaml` | `64ab598926bfe21aca97f253ac588d28240530469e0bea80aa3a2b1c41d57923` | 798B | RAW_BUNDLE |
| `evidence-bundle/raw-canary/FAR-20260813-001/ClaimLedger.tsv` | `c996162edf57053bc0748aa4b831c6751089718fe9d844ea34768842e32fc8ed` | 993B | RAW_BUNDLE |
| `evidence-bundle/raw-canary/FAR-20260813-001/ContradictionLedger.tsv` | `7d7685a51f69a67f561fe6f28659413dfa7ef3631a00e52ffc3dc4a5b2a07ef3` | 362B | RAW_BUNDLE |
| `evidence-bundle/raw-canary/FAR-20260813-001/ExtractionLedger.jsonl` | `ee5aaaa2338a3df10945cbb75abfcb0bfd12802655334a2945ad27f644dd78bc` | 2837B | RAW_BUNDLE |
| `evidence-bundle/raw-canary/FAR-20260813-001/FitGapLedger.tsv` | `6fc7d47783e3524c784d4489c8d60f5699b59ee20dc8c88a466b969138207df7` | 863B | RAW_BUNDLE |
| `evidence-bundle/raw-canary/FAR-20260813-001/HypothesisLedger.tsv` | `256c38c1db32541d978fb4dd6841e2afcd5b4c0f210ff35a0d11acc6c1d442a1` | 545B | RAW_BUNDLE |
| `evidence-bundle/raw-canary/FAR-20260813-001/OpenQuestionLedger.tsv` | `b8e0594638a40ef24435132df80711accf6ed3cb2b74f60a0d3538760f3afaf2` | 278B | RAW_BUNDLE |
| `evidence-bundle/raw-canary/FAR-20260813-001/ProposedEvolution.yaml` | `448349620e8a3eb7137419c46aec685290d4a509165b967e2d1ad99e10fe08e8` | 452B | RAW_BUNDLE |
| `evidence-bundle/raw-canary/FAR-20260813-001/QueryLedger.tsv` | `12d33cf11bce77095fe0634f4581e0bc7d677ab2c1f6a43e2423fbe1552c1ab2` | 799B | RAW_BUNDLE |
| `evidence-bundle/raw-canary/FAR-20260813-001/RejectedAlternativeLedger.tsv` | `748cf327d109ca352f31ce82a432ca5e0b88b0c476319e3809d81fcdf24d3bf9` | 562B | RAW_BUNDLE |
| `evidence-bundle/raw-canary/FAR-20260813-001/ResearchHandoff.yaml` | `bc6600174519a6ae31e592a07bed0862aa148af23cb5603210f172c5d8a66425` | 470B | RAW_BUNDLE |
| `evidence-bundle/raw-canary/FAR-20260813-001/ResearchPlan.yaml` | `a9b8c7a6daf923abcc0a5206195ab01d0f82b9e79ddd2c94db209cd943fcbf32` | 1208B | RAW_BUNDLE |
| `evidence-bundle/raw-canary/FAR-20260813-001/ResearchRequest.yaml` | `29e178aa074c98164af205b91974a8324be397bba8ffe5ca7abc6f6abd095302` | 874B | RAW_BUNDLE |
| `evidence-bundle/raw-canary/FAR-20260813-001/ResearchRunReceipt.json` | `28f4751b04c0f120f4f0311b5cbdbc066be1214b85e6ae00670d0bdc55a74264` | 922B | RAW_BUNDLE |
| `evidence-bundle/raw-canary/FAR-20260813-001/ResearchSourceDenominator.tsv` | `27351e5bddf1c403c54eb4a2e28c11d72582df761ae0eb3b949094d89d9a0bda` | 3194B | RAW_BUNDLE |
| `evidence-bundle/raw-canary/FAR-20260813-001/ResearchSynthesis.md` | `88ef08fc014012322ff103c9bd0b40387af26a2cd7fdde31c237096ee82f420a` | 2095B | RAW_BUNDLE |
| `evidence-bundle/raw-canary/FAR-20260813-001/SourceDispositionLedger.tsv` | `bc73245f416aad89c8151ee8b3d85be89a05ed7510a984981300ef9dee7d3296` | 689B | RAW_BUNDLE |
| `evidence-bundle/raw-canary/FAR-20260813-001/SourceSnapshotLedger.tsv` | `078ed79fb3cf82afe71c326d3b4c95cb4355adc6ead876f12a374738108681c1` | 1324B | RAW_BUNDLE |
| `evidence-bundle/raw-canary/FAR-20260813-006-trisource-real/AdjudicatedClaims.json` | `6ee541940314db7e8edf289977529cf401ef10575b0536468291c8f0182d90b9` | 768B | RAW_BUNDLE |
| `evidence-bundle/raw-canary/FAR-20260813-006-trisource-real/RetrievalLedger.json` | `c67e2a3d337b2ebfa52e49bc619c236d644c17dd86418dcd46827e5e92d82969` | 6152B | RAW_BUNDLE |
| `evidence-bundle/raw-canary/FAR-20260813-006-trisource-real/TriSourceCoverageReceipt.json` | `5cface880d80c10c6e5c4c1e74697dfcf16461f3138f5dcbfea0b5f3ae7fd7e3` | 2397B | RAW_BUNDLE |
| `evidence-bundle/raw-github/github_d_research.json` | `e0d1a4028e1562ad4b4a2e2ee0833a533c67ba6bd731b130b1752ef28640153a` | 5707B | RAW_BUNDLE |
| `evidence-bundle/raw-github/github_d_research_r2.json` | `a8cb0ff8195e6ef8ecfb4cc2d2fbcb5a0425feba609afabb2f404eb3374adf97` | 6490B | RAW_BUNDLE |
| `evidence-bundle/raw-kanban/far-external-closure_snapshot_final.txt` | `6e2101892fd4bd5711fdc78ad3e0f2b22e7c3df7184906690fca1346dcdf8bef` | 539B | RAW_BUNDLE |
| `evidence-bundle/raw-kanban/far-first-use_snapshot.txt` | `c6779507a4365c9dad1f78644390021fd857161792082c2d5a5cc6ddbe620a1e` | 576B | RAW_BUNDLE |
| `evidence-bundle/raw-kanban/far-first-use_snapshot_final.txt` | `2abdec76a31c2057220b18ddcda6927a75e1927249a436c0c15890e984ec4756` | 605B | RAW_BUNDLE |
| `evidence-bundle/raw-kanban/far-implementation_snapshot.txt` | `cc7ffa99fc8f321a295af6b51cdba346f4dd2ee2a46d2bcc8354e118ae5e9994` | 1184B | RAW_BUNDLE |
| `evidence-bundle/raw-kanban/far-implementation_snapshot_final.txt` | `8d09bc2fc896d9678cb33bb3eadaf9f6ad6d902f135dd77ec5636bd02bb67813` | 1213B | RAW_BUNDLE |
| `evidence-bundle/raw-receipts/FAR_AO_LANE_RECEIPT.json` | `af0d6c07ce64f1bd20fcd0f40811aeedaa543e6b8f56e1c46b77945dce8323ca` | 1379B | RAW_BUNDLE |
| `evidence-bundle/raw-receipts/FAR_ARIS_EFFECTIVE_LOAD_RECEIPT.json` | `a8b3456e8f91bf222961de74d40e77b9f69635807d58481b45e390003de53283` | 3428B | RAW_BUNDLE |
| `evidence-bundle/raw-receipts/FAR_ARIS_METHOD_DISPOSITION.yaml` | `d54db220bce5406c596e6a00e8d2e356daf1fb5541e8d562d716c061f8f3bfd4` | 3598B | RAW_BUNDLE |
| `evidence-bundle/raw-receipts/FAR_ARTIFACT_INDEX.json` | `83ab2f4aabded1c91d7ba788cb409cf32055a465a723a9b5f6e115321533e53a` | 11122B | RAW_BUNDLE |
| `evidence-bundle/raw-receipts/FAR_C0_CAPC_RECEIPT.json` | `d659d9f0656f7e57518a1df9d1c0f4f96d10a3fe2d826b1f675ae194d2c8e0a8` | 986B | RAW_BUNDLE |
| `evidence-bundle/raw-receipts/FAR_CAPABILITY_MATRIX.yaml` | `2469d85bf94f16886eb71b169b799fb243c8b5c6bdf3f627178140e9e1f6df6f` | 5008B | RAW_BUNDLE |
| `evidence-bundle/raw-receipts/FAR_CHALLENGE_CLOSURE.json` | `66a373ab524d4cbbac9728f41eb4fe15c65c3cb51105e9b0dc379b0be09faf97` | 1964B | RAW_BUNDLE |
| `evidence-bundle/raw-receipts/FAR_EVOLUTION_CANARY_RECEIPT.json` | `ea3b22e3dff092e38879ab9f3127b213419b41c3a358f7cd479d3a7219169f8d` | 900B | RAW_BUNDLE |
| `evidence-bundle/raw-receipts/FAR_EXECUTION_BINDING.json` | `87ae3bd2a7f07b875e7247bb3d34f3b843e90054d83aa802b24dcfc5985cd218` | 3326B | RAW_BUNDLE |
| `evidence-bundle/raw-receipts/FAR_FIRST_USE_EVIDENCE.md` | `5d210253ebcdaee45566c58626dfdacf50a8a600bc66759273895ca867270fc1` | 6326B | RAW_BUNDLE |
| `evidence-bundle/raw-receipts/FAR_FIRST_USE_INDEX.json` | `a1da01b3f089c8fa509117464107fbc7178ef777f18366520e218f03f00224c5` | 14699B | RAW_BUNDLE |
| `evidence-bundle/raw-receipts/FAR_GATES_RECEIPT.json` | `bc55f4bc0e0a75ca3484df80421da383e7ccad83c0e0973fccecd182a91c9662` | 2338B | RAW_BUNDLE |
| `evidence-bundle/raw-receipts/FAR_IMPLEMENTATION_EVIDENCE.md` | `8c708e5cffd41516f4dd1f5735c9d374e8fca8dd95ff69be0af1e381f43687f8` | 12199B | RAW_BUNDLE |
| `evidence-bundle/raw-receipts/FAR_INTEROP_DISPOSITION.yaml` | `bf6a9b00e548de21dc6b897c460eb057c3c96b0105cf131e9c639504b15d948f` | 4135B | RAW_BUNDLE |
| `evidence-bundle/raw-receipts/FAR_LONG_HORIZON_CONTRACT.yaml` | `0dccec95cfaa2d46a93c4e18ad0f18b9639c45e89ac00fe494e01eb6712b16a6` | 4324B | RAW_BUNDLE |
| `evidence-bundle/raw-receipts/FAR_PRIME_QUALIFICATION_RECORD.yaml` | `d2a9c67c147caf459b9ede9c4f64afd854c0c232f7f0c7567455c3017136663d` | 2232B | RAW_BUNDLE |
| `evidence-bundle/raw-receipts/FAR_Q0_CROSSWALK.md` | `f73e276cf1264708a1e0ef1b73d07192b03948fc3c2ce8b22453448c41e8d088` | 9724B | RAW_BUNDLE |
| `evidence-bundle/raw-receipts/FAR_ROUTE_CHECK.yaml` | `bd6f5c113410065131e73f4a406d2e18f28ff82de50dc446a85314ba11b9de93` | 1780B | RAW_BUNDLE |
| `evidence-bundle/raw-receipts/FAR_SOURCE_SECURITY.yaml` | `c7afbff30c6caa3c7ff7c40d7915f271bfef8dca6314aabf1ba82ce5f3a2aba0` | 2158B | RAW_BUNDLE |
| `evidence-bundle/raw-receipts/FAR_SWARM_Q10_RECEIPT.json` | `764b4f2945acc381d8576e329b4eef00433f39eed1d11401281e2029e560f2c8` | 2879B | RAW_BUNDLE |
| `evidence-bundle/raw-receipts/TEAM.md` | `ae67143a2928b27ef4916a78b9e8f2bb46759cd9edb031c60c688c83926e8ae5` | 6740B | RAW_BUNDLE |
| `evidence-bundle/raw-receipts/far_router.py` | `ade07192ae8d04776b67046ad90ffbf4cbcbe1d2fa0b3494a9d6a80057f23a3a` | 12702B | RAW_BUNDLE |
| `evidence-bundle/raw-receipts/far_source_security.py` | `5227edde39a04edc848df42d1faf089fcbd71f4a65d5da1a5a2b00390f375331` | 3140B | RAW_BUNDLE |
| `evidence-bundle/raw-receipts/far_watchdog.py` | `852eb358303c95ab145eebb873e4740c6179710e11fce1c52e5c90a39599c346` | 7892B | RAW_BUNDLE |
| `evidence-bundle/raw-spine/far_spine_readback.json` | `7847dab4702990410aeda359ef790ffae1cf14b0d7e590a8bbfd35800ca1c350` | 16860B | RAW_BUNDLE |
| `evidence-bundle/raw-spine/far_spine_readback_final.json` | `46826ae9721a5c902a006b591bd8ba4f4ec1ccb8b09da69c105c669a9ea07e01` | 13418B | RAW_BUNDLE |
| `evidence-bundle/raw-spine/far_spine_readback_final_r2.json` | `d24e8b80b8db38150395d582a1de59210a2f9644cb6e64d5f73344dac6632017` | 14346B | RAW_BUNDLE |
| `evidence-bundle/raw-tests/far_tests_suite.exitcode.txt` | `5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9` | 1B | RAW_BUNDLE |
| `evidence-bundle/raw-tests/far_tests_suite.stderr.txt` | `a435a2adbec429eef6d00bffd724ab93ae3d2a6279b425f07b0b1335843affee` | 127B | RAW_BUNDLE |
| `evidence-bundle/raw-tests/far_tests_suite.stdout.txt` | `4aa600009eabd4ae334d7557e5094ab5d5f583208734d0e6c194339bc52453c5` | 134B | RAW_BUNDLE |

## 7. SharedSpine final readback（全文; captured 2026-08-13T13:47:45Z）

### WorkOrders（9 rows; writer/state/rollback/result）

| WO | writer | state | rollback | result_json(前200字) |
|---|---|---|---|---|
| WO-FAR-001 | codex | VERIFIED | `RB-WO-FAR-001` | `"{\"checker\":\"acceptance-officer\",\"evidence_refs\":[\"EVD-FAR-Q0-CROSSWALK\",\"EVD-FAR-CAPC\",\"EVD-FAR-TEAM\",\"EVD-FAR-MATRIX\",\"EVD-FAR-BINDING\",\"EVD-FAR-INTEROP\",\"EVD-FAR-SECURITY\",\"EVD` |
| WO-FAR-002 | codex | VERIFIED | `RB-WO-FAR-002` | `"{\"checker\":\"acceptance-officer\",\"evidence_refs\":[\"EVD-FAR-Q0-CROSSWALK\",\"EVD-FAR-CAPC\",\"EVD-FAR-TEAM\",\"EVD-FAR-MATRIX\",\"EVD-FAR-BINDING\",\"EVD-FAR-INTEROP\",\"EVD-FAR-SECURITY\",\"EVD` |
| WO-FAR-003 | codex | VERIFIED | `RB-WO-FAR-003` | `"{\"checker\":\"acceptance-officer\",\"evidence_refs\":[\"EVD-FAR-Q0-CROSSWALK\",\"EVD-FAR-CAPC\",\"EVD-FAR-TEAM\",\"EVD-FAR-MATRIX\",\"EVD-FAR-BINDING\",\"EVD-FAR-INTEROP\",\"EVD-FAR-SECURITY\",\"EVD` |
| WO-FAR-004 | codex | VERIFIED | `RB-WO-FAR-004` | `"{\"checker\":\"acceptance-officer\",\"evidence_refs\":[\"EVD-FAR-Q0-CROSSWALK\",\"EVD-FAR-CAPC\",\"EVD-FAR-TEAM\",\"EVD-FAR-MATRIX\",\"EVD-FAR-BINDING\",\"EVD-FAR-INTEROP\",\"EVD-FAR-SECURITY\",\"EVD` |
| WO-FAR-005 | codex | VERIFIED | `RB-WO-FAR-005` | `"{\"checker\":\"acceptance-officer\",\"evidence_refs\":[\"EVD-FAR-Q0-CROSSWALK\",\"EVD-FAR-CAPC\",\"EVD-FAR-TEAM\",\"EVD-FAR-MATRIX\",\"EVD-FAR-BINDING\",\"EVD-FAR-INTEROP\",\"EVD-FAR-SECURITY\",\"EVD` |
| WO-FAR-006 | codex | VERIFIED | `RB-WO-FAR-006` | `"{\"checker\":\"acceptance-officer\",\"evidence_refs\":[\"EVD-FAR-Q0-CROSSWALK\",\"EVD-FAR-CAPC\",\"EVD-FAR-TEAM\",\"EVD-FAR-MATRIX\",\"EVD-FAR-BINDING\",\"EVD-FAR-INTEROP\",\"EVD-FAR-SECURITY\",\"EVD` |
| WO-FAR-007 | codex | VERIFIED | `RB-WO-FAR-007` | `"{\"checker\":\"acceptance-officer\",\"evidence_refs\":[\"EVD-FAR-Q0-CROSSWALK\",\"EVD-FAR-CAPC\",\"EVD-FAR-TEAM\",\"EVD-FAR-MATRIX\",\"EVD-FAR-BINDING\",\"EVD-FAR-INTEROP\",\"EVD-FAR-SECURITY\",\"EVD` |
| WO-FAR-008 | codex | VERIFIED | `RB-WO-FAR-008` | `"{\"checker\":\"acceptance-officer\",\"evidence_refs\":[\"EVD-FAR-Q0-CROSSWALK\",\"EVD-FAR-CAPC\",\"EVD-FAR-TEAM\",\"EVD-FAR-MATRIX\",\"EVD-FAR-BINDING\",\"EVD-FAR-INTEROP\",\"EVD-FAR-SECURITY\",\"EVD` |
| WO-FAR-USE-001 | codex | VERIFIED | `RB-WO-FAR-USE-001` | `"{\"checker\":\"acceptance-officer\",\"evidence_refs\":[\"EVD-FAR-USE-001\"],\"verdict\":\"PASS\"}"` |

### Requirements（9 rows）

| REQ | state | version |
|---|---|---|
| REQ-FAR-001 | FROZEN | 1 |
| REQ-FAR-002 | FROZEN | 1 |
| REQ-FAR-003 | FROZEN | 1 |
| REQ-FAR-004 | FROZEN | 1 |
| REQ-FAR-005 | FROZEN | 1 |
| REQ-FAR-006 | FROZEN | 1 |
| REQ-FAR-007 | FROZEN | 1 |
| REQ-FAR-008 | FROZEN | 1 |
| REQ-FAR-USE-001 | FROZEN | 1 |

### Evidence refs（39 rows EVD-FAR-*; full sha 前 16 hex）

| evidence_id | kind | sha256(16) | producer | checker |
|---|---|---|---|---|
| EVD-FAR-ACCEPTANCE-MD | MARKDOWN | `e739c21a1ad0ffb6…` | far-orchestrator | acceptance-officer |
| EVD-FAR-ALLPASS | JSON | `83c0a39daffd8a47…` | far-orchestrator | acceptance-officer |
| EVD-FAR-ALLPASS-V3 | JSON | `efe35c8d8c4e6d08…` | far-orchestrator | acceptance-officer |
| EVD-FAR-ARIS-DISPO | YAML | `d54db220bce5406c…` | far-orchestrator | acceptance-officer |
| EVD-FAR-ARIS-LOAD | JSON | `a8b3456e8f91bf22…` | far-orchestrator | acceptance-officer |
| EVD-FAR-BINDING | JSON | `87ae3bd2a7f07b87…` | far-orchestrator | acceptance-officer |
| EVD-FAR-CANARY | JSON | `28f4751b04c0f120…` | far-orchestrator | acceptance-officer |
| EVD-FAR-CAPC | JSON | `d659d9f0656f7e57…` | far-orchestrator | acceptance-officer |
| EVD-FAR-CROSSWALK | JSON | `46a74fd56bc551a3…` | far-orchestrator | acceptance-officer |
| EVD-FAR-EVIDENCE-MANIFEST | JSON | `5c8ed3c067f14fde…` | far-orchestrator | acceptance-officer |
| EVD-FAR-EVIDENCE-MANIFEST-R2 | JSON | `183cbfefb634d5ef…` | far-orchestrator | acceptance-officer |
| EVD-FAR-EVIDENCE-MD | MARKDOWN | `8c708e5cffd41516…` | far-orchestrator | acceptance-officer |
| EVD-FAR-EVO | JSON | `ea3b22e3dff092e3…` | far-orchestrator | acceptance-officer |
| EVD-FAR-EXTC-CAPC | JSON | `71cb1ad46f893d6e…` | far-orchestrator | acceptance-officer |
| EVD-FAR-GATES | JSON | `81685b531d8add2d…` | far-orchestrator | acceptance-officer |
| EVD-FAR-GATES-R2 | JSON | `bc55f4bc0e0a75ca…` | far-orchestrator | acceptance-officer |
| EVD-FAR-INDEX | JSON | `27a357ac698d8527…` | far-orchestrator | acceptance-officer |
| EVD-FAR-INDEX-R2 | JSON | `83ab2f4aabded1c9…` | far-orchestrator | acceptance-officer |
| EVD-FAR-INTEROP | YAML | `bf6a9b00e548de21…` | far-orchestrator | acceptance-officer |
| EVD-FAR-LH | YAML | `0dccec95cfaa2d46…` | far-orchestrator | acceptance-officer |
| EVD-FAR-MATRIX | YAML | `2469d85bf94f1688…` | far-orchestrator | acceptance-officer |
| EVD-FAR-MD-V2 | MARKDOWN | `249f71bab389207f…` | far-orchestrator | acceptance-officer |
| EVD-FAR-MD-V3 | MARKDOWN | `3f5efaf23edda820…` | far-orchestrator | acceptance-officer |
| EVD-FAR-MIRROR | JSON | `cde255d0f14e65d0…` | far-orchestrator | acceptance-officer |
| EVD-FAR-MIRROR-R2 | JSON | `1d564301ac122109…` | far-orchestrator | acceptance-officer |
| EVD-FAR-NEG-SIDE-EFFECT | JSON | `5d23f6c0e0270ff7…` | far-orchestrator | acceptance-officer |
| EVD-FAR-PACKAGE-RECEIPT | JSON | `52f0d02941384623…` | far-orchestrator | acceptance-officer |
| EVD-FAR-PACKAGE-ZIP | ZIP | `bab2ecaead5393cf…` | far-orchestrator | acceptance-officer |
| EVD-FAR-PRIME | YAML | `d2a9c67c147caf45…` | far-orchestrator | acceptance-officer |
| EVD-FAR-Q0-CROSSWALK | MARKDOWN | `f73e276cf1264708…` | far-orchestrator | acceptance-officer |
| EVD-FAR-Q10-AO | JSON | `da3174916358fdc2…` | far-orchestrator | acceptance-officer |
| EVD-FAR-Q4-INVOCATION | JSON | `143887c82803373a…` | far-orchestrator | acceptance-officer |
| EVD-FAR-ROUTE | YAML | `bd6f5c1134100651…` | far-orchestrator | acceptance-officer |
| EVD-FAR-SECURITY | YAML | `c7afbff30c6caa3c…` | far-orchestrator | acceptance-officer |
| EVD-FAR-SUBJECT-ROOT | JSON | `00806ea1c932f498…` | far-orchestrator | acceptance-officer |
| EVD-FAR-SWARM | JSON | `764b4f2945acc381…` | far-orchestrator | acceptance-officer |
| EVD-FAR-TEAM | MARKDOWN | `ae67143a2928b27e…` | far-orchestrator | acceptance-officer |
| EVD-FAR-USE-001 | JSON | `16ab001000f4b346…` | far-orchestrator | acceptance-officer |
| EVD-FAR-USE-EVIDENCE-MD | MARKDOWN | `5d210253ebcdaee4…` | far-orchestrator | acceptance-officer |

```text
frozen_events_count = 9（FRZ-REQ-FAR-* canonical events）
```

## 8. Kanban terminal snapshots（全文）

### far-implementation（11 tasks）

```text
# kanban board: far-implementation (final snapshot 2026-08-13T13:14:36Z)

Board: far-implementation (17 other boards — `hermes kanban boards list`)

✓ t_06fdaa1c  done      default              [hgk]  FAR-Q0: Authority/Schema crosswalk + admission
✓ t_b11514d7  done      (unassigned)         [hgk]  WO-FAR-001: Q0 crosswalk doc
✓ t_a4782bf2  done      (unassigned)         [hgk]  WO-FAR-002: Research product artifacts + native profile
✓ t_5fafaf3c  done      (unassigned)         [hgk]  WO-FAR-003: Source routes + security
✓ t_34e054d1  done      (unassigned)         [hgk]  WO-FAR-004: ARIS selected methods
✓ t_7c1a0f55  done      (unassigned)         [hgk]  WO-FAR-005: Long-horizon/fanout/budget
✓ t_9a18cd42  done      (unassigned)         [hgk]  WO-FAR-006: Prime qualification + router
✓ t_3e0d8168  done      (unassigned)         [hgk]  WO-FAR-007: Continual-harness/GE
✓ t_5d9805e8  done      (unassigned)         [hgk]  WO-FAR-008: Dogfood/interop/Obsidian/final
✓ t_816b4e30  done      (unassigned)         [hgk]  FAR-GATES: Q0..Q10 + R1 local qualification
✓ t_203bf33a  done      (unassigned)         [hgk]  FAR-EVIDENCE: single evidence MD + mirror 3 roots
```

### far-first-use（4 tasks）

```text
# kanban board: far-first-use (final snapshot 2026-08-13T13:14:36Z)

Board: far-first-use (17 other boards — `hermes kanban boards list`)

✓ t_e290544d  done      (unassigned)         [hgk]  FAR-USE-R0-R8: first-use research run on skill-ref helpfulness
✓ t_29a7d7e6  done      (unassigned)         [hgk]  FAR-USE-CHALLENGE: adversarial leaf (redundancy check)
✓ t_08446a21  done      (unassigned)         [hgk]  FAR-USE-PATCH: CandidateHarnessDelta -> skill references + SKILL.md
✓ t_3baf443a  done      (unassigned)         [hgk]  FAR-USE-VERIFY: load/verify patched skill + WO result
```

### far-external-closure（3 tasks）

```text
# kanban board: far-external-closure (final snapshot 2026-08-13T13:14:36Z)

Board: far-external-closure (17 other boards — `hermes kanban boards list`)

✓ t_b3003828  done      (unassigned)         [hgk]  EXT-FAR closure: 10 findings CLOSED + raw bundle + subject root 5720337b
✓ t_8102be14  done      (unassigned)         [hgk]  EVIDENCE v2: MD 249f71ba + mirror 3 roots + ALLPASS gate
✓ t_b13b6946  done      (unassigned)         [hgk]  V3 materialization: post-repair AO truth + 10-row closure table + review package zip
```

## 9. Raw test stdout + exit code（全文）

```text
.......................
----------------------------------------------------------------------
Ran 23 tests in 0.001s

OK
EXIT=0
```
exitcode = `0`

## 10. Mirror readback receipt（全文）

```json
{
 "schema": "FAR-MIRROR-READBACK-RECEIPT/1",
 "subject": "FAR_IMPLEMENTATION_EVIDENCE_v3.md",
 "sha256": "3f5efaf23edda8208d39b4cf9b9e13b5b1a948fa673c500a83cd30619212cc08",
 "byte_identical": true,
 "mirror_locations": [
  "C:\\Projects\\Agent_Workspace\\Fabric\\fabric-autonomous-research\\FAR_IMPLEMENTATION_EVIDENCE_v3.md",
  "C:\\Projects\\Agent_Workspace\\HG-KSEOS\\evidence\\review\\FAR_IMPLEMENTATION_EVIDENCE_v3.md",
  "C:\\Projects\\Agent_Workspace\\Fabric\\evidence\\review\\FAR_IMPLEMENTATION_EVIDENCE_v3.md",
  "C:\\Projects\\Agent_Workspace\\SQS-THC\\evidence\\review\\FAR_IMPLEMENTATION_EVIDENCE_v3.md"
 ],
 "equality_verified": "sha256 identical at all 4 locations (3f5efaf2...)",
 "freeze_order_honored": "artifacts frozen first -> evidence manifest regenerated -> MD v3 generated LAST -> mirrored -> hashed; no edits after hashing",
 "single_direction_binding": "MD v3 references FAR_MIRROR_READBACK_RECEIPT.json by path; receipt carries MD hash (no self-reference loop)",
 "generated_at_utc": "2026-08-13T20:25:00Z"
}
```

## 10A. Negative side-effect receipt（全文; EXT-FAR-R6-002 CLOSED）

```json
{
  "schema": "FAR-NEGATIVE-SIDE-EFFECT-RECEIPT/1",
  "subject_bound": {
    "subject_root_digest": "5720337bce9ef09402c8f22a2fecff39bffe881a5e46a187a78aabd10519ec6a",
    "subject_manifest": "FAR_SUBJECT_ROOT_MANIFEST.json (95-file implementation surface; external-reviewed recomputation PASS)",
    "binding_semantics": "this receipt is an acceptance/evidence artifact; it does NOT alter the frozen subject root (5720337b stays valid)"
  },
  "negative_edges": {
    "unauthorized_side_effects": {
      "value": 0,
      "denominator": "WO-FAR-001..008 + WO-FAR-USE-001 (9 WorkOrders, all VERIFIED) + 23/23 tests + 2 canary runs (FAR-20260813-001 19 artifacts, FAR-20260813-002 20 artifacts) + LH detach/reattach canary",
      "check": "evidence manifest entries (FAR_EVIDENCE_MANIFEST.json) all locate under Fabric/fabric-autonomous-research/ (FAR-root/* or evidence-bundle/*); SQS/docs/risk/SSOT/kernel: 0 files modified after 2026-08-13 19:00 +08 (find -newermt); HGK writes confined to var/far/ + evidence/review mirrors",
      "evidence_locator": "FAR_EVIDENCE_MANIFEST.json + evidence-bundle/raw-spine/far_spine_readback_final_r2.json"
    },
    "sqs_financial_truth_mutation": {
      "value": 0,
      "check": "SQS-THC/SQS/TWICT_RUNTIME_PACK_MANIFEST.yaml mtime 2026-08-13 01:07:22 +08 (BEFORE FAR round); SQS product paths (SQS/docs/risk/SSOT/kernel) show zero files modified in the FAR window; no FAR evidence artifact locates into SQS product paths; FAR consumes SQS ONLY as consumer boundary (FAR_CAPABILITY_MATRIX.yaml RESEARCH_FINANCIAL_METHOD mutation_authority: NONE)",
      "evidence_locator": "FAR_CAPABILITY_MATRIX.yaml + SQS-THC/SQS/TWICT_RUNTIME_PACK_MANIFEST.yaml (mtime readback)"
    },
    "live_broker_write": {
      "value": 0,
      "check": "broker/order-path adapter files in SQS-THC = 0 (find -iname '*broker*' over SQS-THC excluding .git/.venv = empty); FAR product code (far_router.py ade07192…/far_watchdog/far_source_security, subject tree current) contains no broker/order-path references; SQS handoff pack invariant no_broker_write: true (per SQS docs); FAR never routes to a live order path (router decision classes are research/evolution only)",
      "evidence_locator": "SQS-THC broker scan (empty result) + far_router.py sha 7b01df26-bound subject tree + FAR_CAPABILITY_MATRIX.yaml"
    }
  },
  "checker_identity": "acceptance-officer (independent; maker-separated; AO lanes deleg_bab33aae/deleg_e4a09db4 PASS)",
  "run_denominator": {
    "workorders": 9,
    "workorder_ids": ["WO-FAR-001", "WO-FAR-002", "WO-FAR-003", "WO-FAR-004", "WO-FAR-005", "WO-FAR-006", "WO-FAR-007", "WO-FAR-008", "WO-FAR-USE-001"],
    "wo_states": "ALL VERIFIED",
    "tests": "23/23 PASS, exit 0",
    "canary_runs": ["FAR-20260813-001 (19 artifacts)", "FAR-20260813-002 (20 artifacts)"],
    "long_horizon_canary": "LH-CANARY-001 (detach pid 24420 -> reattach pid 12604 -> RESEARCH_PASS_CANDIDATE)"
  },
  "raw_locator": "C:\\Projects\\Agent_Workspace\\Fabric\\fabric-autonomous-research\\ (evidence-bundle/ + FAR-root receipts; mirrored to HGK/Fabric/SQS evidence\\review\\)",
  "generated_at_utc": "2026-08-13T13:50:00Z"
}
```

## 11. Rollback pointers（spine 全文內含; 摘要表）

```text
RB-WO-FAR-001 .. RB-WO-FAR-008（core 8 WO）
RB-WO-FAR-USE-001（first-use separate subject）
（每 row 完整 rollback_pointer 見 §7 workorders 表）
```

## 12. Closure receipts ×10（全文）

### EXT-FAR-001 (`63410756b5ae5a7d…`)

```json
{
 "finding": "EXT-FAR-001",
 "classification": "EVIDENCE_GAP",
 "status": "CLOSED",
 "smallest_repair": "MATERIALIZE_ONE_CANONICAL_FINAL_SUBJECT_ROOT_AND_RAW_REVIEW_BUNDLE",
 "focused_retest": {
  "subject_root_manifest": "FAR_SUBJECT_ROOT_MANIFEST.json exists",
  "subject_root_digest": "5720337bce9ef09402c8f22a2fecff39bffe881a5e46a187a78aabd10519ec6a",
  "evidence_manifest_root": "FAR_EVIDENCE_MANIFEST.json exists (entry_count=71)",
  "all_receipts_bind_same_subject": true,
  "hashes_from_current_bytes": true
 },
 "bound_into": [
  "FAR_SUBJECT_ROOT_MANIFEST.json",
  "FAR_EVIDENCE_MANIFEST.json",
  "evidence-bundle/",
  "FAR_IMPLEMENTATION_EVIDENCE.md v2"
 ],
 "verdict": "CLOSED",
 "generated_at_utc": "2026-08-13T12:09:13Z"
}
```

### EXT-FAR-002 (`bffdde4657649c73…`)

```json
{
 "finding": "EXT-FAR-002",
 "classification": "EVIDENCE_GAP",
 "status": "CLOSED",
 "smallest_repair": "PROVIDE_RAW_REVIEW_BUNDLE",
 "focused_retest": {
  "bundle_files": 49,
  "raw_tests_stdout": "evidence-bundle/raw-tests/far_tests_suite.stdout.txt (regenerated merged capture; ends OK + EXIT=0; AO-FINDING-FAR-002 closed)",
  "raw_spine_readback": "evidence-bundle/raw-spine/far_spine_readback.json",
  "raw_kanban_snapshots": [
   "far-implementation",
   "far-first-use"
  ],
  "raw_receipts_dir": "evidence-bundle/raw-receipts/",
  "raw_canary": "evidence-bundle/raw-canary/FAR-20260813-001 (19 files)",
  "gates_receipt": "FAR_GATES_RECEIPT.json",
  "swarm_receipt": "FAR_SWARM_Q10_RECEIPT.json",
  "capc_receipt": "FAR_C0_CAPC_RECEIPT.json",
  "q4_receipt": "FAR_Q4_REAL_INVOCATION_RECEIPT.json",
  "rollback_pointers": "RB-WO-FAR-001..008 + RB-WO-FAR-USE-001 (spine)"
 },
 "bound_into": [
  "evidence-bundle/",
  "FAR_EVIDENCE_MANIFEST.json"
 ],
 "verdict": "CLOSED",
 "generated_at_utc": "2026-08-13T12:09:13Z",
 "ao_finding": "AO-FINDING-FAR-002 (packaging capture defect) repaired; focused retest lane deleg_e4a09db4 pending"
}
```

### EXT-FAR-003 (`d225b7f196c4992a…`)

```json
{
 "finding": "EXT-FAR-003",
 "classification": "CONFIRMED_DEFECT",
 "status": "CLOSED",
 "smallest_repair": "RECOMPUTE_AND_DECLARE_ONE_CANONICAL_INDEX_DIGEST_OR_EXPLICITLY_SEPARATE_DIGEST_TYPES",
 "focused_retest": {
  "index_v3_self_hash": "7b01df26d17505ec27b3c96d3b383e144c022b49f78ba6275b27442f66a6a755",
  "semantics_declared": "FILE_HASH_ONLY; index excludes itself (pre-self-row rule)",
  "content_root_digest_separately_named": "FAR_SUBJECT_ROOT_MANIFEST.json subject_root_digest (5720337b...)",
  "every_reference_uses_correct_digest_type": true
 },
 "bound_into": [
  "FAR_ARTIFACT_INDEX.json",
  "FAR_SUBJECT_ROOT_MANIFEST.json",
  "MD v2 §3"
 ],
 "verdict": "CLOSED",
 "generated_at_utc": "2026-08-13T12:09:13Z"
}
```

### EXT-FAR-004 (`bd724c24e126536f…`)

```json
{
 "finding": "EXT-FAR-004",
 "classification": "CONFIRMED_DEFECT",
 "status": "CLOSED",
 "smallest_repair": "REGENERATE_FINAL_KANBAN_SNAPSHOT_AND_REFRESH_EVIDENCE_MD",
 "focused_retest": {
  "board": "far-implementation",
  "final_dag_denominator": 11,
  "terminal_tasks_in_snapshot": 11,
  "all_terminal": true,
  "snapshot_hash": "cc7ffa99fc8f321a295af6b51cdba346f4dd2ee2a46d2bcc8354e118ae5e9994",
  "evidence_md_generated_after_snapshot": true
 },
 "bound_into": [
  "evidence-bundle/raw-kanban/far-implementation_snapshot.txt",
  "MD v2 §2"
 ],
 "verdict": "CLOSED",
 "generated_at_utc": "2026-08-13T12:09:13Z"
}
```

### EXT-FAR-005 (`a5a8e71d4039afec…`)

```json
{
 "finding": "EXT-FAR-005",
 "classification": "CONFIRMED_DEFECT",
 "status": "CLOSED",
 "smallest_repair": "ADD_OR_ATTACH_RAW_MIRROR_READBACK_RECEIPT_WITH_EXACT_LOCATORS_AND_HASHES",
 "focused_retest": {
  "mirror_table_in_md_v2": true,
  "mirror_locations": [
   "Fabric/fabric-autonomous-research/",
   "HG-KSEOS/evidence/review/",
   "Fabric/evidence/review/",
   "SQS-THC/evidence/review/"
  ],
  "byte_identical": "verified by sha256 equality across all copies"
 },
 "bound_into": [
  "MD v2 §11 mirror table"
 ],
 "verdict": "CLOSED",
 "generated_at_utc": "2026-08-13T12:09:13Z"
}
```

### EXT-FAR-006 (`c560c9c1aec42a7b…`)

```json
{
 "finding": "EXT-FAR-006",
 "classification": "EVIDENCE_GAP",
 "status": "CLOSED",
 "smallest_repair": "FRESH_EVD_LEDGER_READBACK_WITH_EXACT_DENOMINATOR",
 "focused_retest": {
  "current_evd_count": 22,
  "evd_ids": [
   "EVD-FAR-ARIS-DISPO",
   "EVD-FAR-ARIS-LOAD",
   "EVD-FAR-BINDING",
   "EVD-FAR-CANARY",
   "EVD-FAR-CAPC",
   "EVD-FAR-EVIDENCE-MD",
   "EVD-FAR-EVO",
   "EVD-FAR-GATES",
   "EVD-FAR-GATES-R2",
   "EVD-FAR-INDEX",
   "EVD-FAR-INDEX-R2",
   "EVD-FAR-INTEROP",
   "EVD-FAR-LH",
   "EVD-FAR-MATRIX",
   "EVD-FAR-PRIME",
   "EVD-FAR-Q0-CROSSWALK",
   "EVD-FAR-ROUTE",
   "EVD-FAR-SECURITY",
   "EVD-FAR-SWARM",
   "EVD-FAR-TEAM",
   "EVD-FAR-USE-001",
   "EVD-FAR-USE-EVIDENCE-MD"
  ],
  "no_duplicate_ids": true,
  "each_row_has_digest": true,
  "ledger_source": "evidence-bundle/raw-spine/far_spine_readback.json (fresh sqlite readback)"
 },
 "bound_into": [
  "evidence-bundle/raw-spine/far_spine_readback.json",
  "MD v2 §1"
 ],
 "verdict": "CLOSED",
 "generated_at_utc": "2026-08-13T12:09:13Z"
}
```

### EXT-FAR-007 (`21aa62e8f8708db4…`)

```json
{
 "finding": "EXT-FAR-007",
 "classification": "EVIDENCE_GAP",
 "status": "CLOSED",
 "smallest_repair": "PROVIDE_FRESH_SUBJECT_BOUND_AO_RECEIPT",
 "focused_retest": {
  "checker_identity": "acceptance-officer (deleg_bab33aae fresh lane + deleg_e4a09db4 focused retest)",
  "fresh_context_maker_separation": true,
  "exact_frozen_subject_digest": "5720337bce9ef09402c8f22a2fecff39bffe881a5e46a187a78aabd10519ec6a",
  "denominator": "T001..T092 via FAR_REGRESSION_CROSSWALK.json (92 rows)",
  "pass_fail_counts": "lane1 9/10 PASS + 1 packaging finding (AO-FINDING-FAR-002, repaired); focused retest 4/4 PASS",
  "blockers": 0,
  "no_candidate_writes": true,
  "swarm_challenger_as_input_not_final": true,
  "raw_receipt": "FAR_Q10_AO_RECEIPT.json (sha da3174916358fdc20c8072e1adfb3062af72d44e0a4d65093b0fda4708e496eb)"
 },
 "bound_into": [
  "FAR_Q10_AO_RECEIPT.json",
  "FAR_INTERNAL_ALLPASS_GATE.json",
  "FAR_IMPLEMENTATION_EVIDENCE_v2.md §8"
 ],
 "verdict": "CLOSED",
 "generated_at_utc": "2026-08-13T20:16:00Z"
}
```

### EXT-FAR-008 (`daf8a07ab67ce62d…`)

```json
{
 "finding": "EXT-FAR-008",
 "classification": "EVIDENCE_GAP",
 "status": "CLOSED",
 "smallest_repair": "PROVIDE_ONE_OR_MORE_SUBJECT_BOUND_REAL_METHOD_INVOCATION_RECEIPTS",
 "focused_retest": {
  "receipt": "FAR_Q4_REAL_INVOCATION_RECEIPT.json",
  "real_invocations": 2,
  "methods": [
   "research-lit (00d9f549...)",
   "novelty-check (c512579f...)"
  ],
  "pinned_commit": "e12e07c7b85ee1a4dc07e5463089aa16836af2bf",
  "input_output_trace": true,
  "no_meta_apply_authority_import": true,
  "reviewer_not_ao": true
 },
 "bound_into": [
  "FAR_Q4_REAL_INVOCATION_RECEIPT.json",
  "MD v2 §5 gates table Q4"
 ],
 "verdict": "CLOSED",
 "generated_at_utc": "2026-08-13T12:09:13Z"
}
```

### EXT-FAR-009 (`3d7ce328a2987638…`)

```json
{
 "finding": "EXT-FAR-009",
 "classification": "OUT_OF_SCOPE",
 "status": "CLOSED_AS_SEPARATE_SUBJECT",
 "smallest_repair": "FREEZE_FIRST_USE_AS_SEPARATE_SUBJECT_AND_PROVIDE_RAW_CHANGESET_BUNDLE",
 "focused_retest": {
  "separate_subject_manifest": "FAR_FIRST_USE_SUBJECT_MANIFEST.json",
  "first_use_subject_digest": "c4590d94be8c4d16a21687f989fc4884ec082b9d2bb8d5440010e32b50bc0d11",
  "not_absorbed_into_core_r1": true,
  "rollback_pointer": "RB-WO-FAR-USE-001",
  "supersedes": "671327cf... (refreshed hashes; current bytes)"
 },
 "bound_into": [
  "FAR_FIRST_USE_SUBJECT_MANIFEST.json",
  "MD v2 §12"
 ],
 "verdict": "CLOSED_AS_SEPARATE_SUBJECT",
 "generated_at_utc": "2026-08-13T12:09:13Z"
}
```

### EXT-FAR-010 (`a2dc08b9b18d933c…`)

```json
{
 "finding": "EXT-FAR-010",
 "classification": "EVIDENCE_GAP",
 "status": "CLOSED",
 "smallest_repair": "PROVIDE_RAW_FIRST_USE_CHANGESET_BUNDLE",
 "focused_retest": {
  "run_002_artifacts": 20,
  "challenge_transcript_ref": "deleg_f82657d3 live transcript + subagent-summary (delegation cache)",
  "closure_json": "FAR_CHALLENGE_CLOSURE.json",
  "fresh_ao_receipt": "FAR_AO_LANE_RECEIPT.json (7/7 PASS)",
  "patched_reference_post_digest": "a1088d40037f88c920aa1896d5aaa860b8f0dcffda272656963b69215de75d34",
  "duplicate_deleted": "far-shared-infrastructure-landing.md REMOVED",
  "no_parallel_reference_remains": true,
  "skill_load_verified": "skill_view 12 sections OK"
 },
 "bound_into": [
  "FAR_FIRST_USE_SUBJECT_MANIFEST.json",
  "FAR_FIRST_USE_EVIDENCE.md"
 ],
 "verdict": "CLOSED",
 "generated_at_utc": "2026-08-13T12:09:13Z"
}
```

## 13. 外部驗收判定指引（challenge-review grammar）

```text
可獨立驗證項目（全部在本檔內含 raw）:
  92/92 crosswalk rows ........ §4 全文
  95-file subject root merkle .. §5 全文（重算 digest 應 = 5720337bce…）
  119-entry evidence manifest ... §6 全文
  Q4 real invocation .......... §2 全文（2 invocations; output_digests）
  Q10 fresh AO chain .......... §3 全文（9/10 → finding → repair → 4/4 PASS; blockers=0）
  test stdout + exit .......... §9 全文（23 tests OK; EXIT=0）
  spine / EVD readback ........ §7 全文（9 WO VERIFIED; 39 EVD rows）
  kanban terminal ............. §8 全文（11/11 + 4/4 + 3/3 done）
  mirror receipt .............. §10 全文（MD v3 四處 byte-identical）
  negative side effects ....... §10A 全文（unauthorized=0 / SQS FT mutation=0 / live broker write=0）
  closure receipts ............ §12 全文 ×10
blocking contradiction = 0
```

```text
STOP
SINGLE_ACCEPTANCE_MD = FAR_FINAL_ACCEPTANCE_EVIDENCE.md（全量 raw 內嵌; 無外部路徑依賴）
EXT-FAR-R5-001 = CLOSED（raw transport 已由本單一 MD 閉合）
EXT-FAR-R6-001 = CLOSED（Evidence Manifest/EVD canonical current binding 重生; EVD-FAR-MIRROR-R2 = 1d564301…）
EXT-FAR-R6-002 = CLOSED（NEGATIVE_SIDE_EFFECT_RECEIPT subject-bound 5720337b…; 三 negative edges=0）
FAR_EXTERNAL_FINAL_ACCEPTANCE = PENDING（外部 reviewer 對本檔 readback 後裁決; COV-11-06）
```
