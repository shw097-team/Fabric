# FAR First-Use Test Evidence — FAR 首次使用測試（WO-FAR-USE-001 / run FAR-20260813-002）

> Document ID: `FAR-FIRST-USE-EVIDENCE-20260813`
> generated_at_utc: 2026-08-13T11:48:24Z
> 用途: 供外部驗收官最終驗收（COV-11-06 human gate）；本文件不自我核准最終接受。
> 母證據: `FAR_IMPLEMENTATION_EVIDENCE.md` 8c708e5c…（FAR 主落地）

## 0. Claim ceiling（誠實）

```text
FAR_FIRST_USE_RESEARCH      = PASS (run FAR-20260813-002: 20 artifacts, R0-R8 + router + watchdog 實測)
FAR_FIRST_USE_CHALLENGE     = PASS (deleg_f82657d3 REJECT-as-draft; DG01 確認冗餘)
FAR_FIRST_USE_SELF_ITERATE  = PASS (CL02 REFUTED_WITH_EVIDENCE; disposition MERGE_DELTA_AND_DELETE_DUPLICATE)
FAR_FIRST_USE_PATCH_LANDED  = PASS (reference 114->161 行 + §10/11/12; SKILL.md 註記; 草稿已刪)
FAR_FIRST_USE_INTERNAL_ACCEPTANCE = PASS (AO lane deleg_60df62df)
EXTERNAL_FINAL_ACCEPTANCE   = PENDING (外部驗收官; 不自我核准)
PRODUCTION / SQS live / REMOTE = NOT_CLAIMED / NOT_AUTHORIZED / NOT_CLAIMED
```

## 1. Governance binding（HGK SharedSpine）

```text
REQ-FAR-USE-001  FROZEN v1（canonical event FRZ-REQ-FAR-USE-001）
TS-FAR-USE-001   taskspec created
WO-FAR-USE-001   writer=codex  state=VERIFIED（checker=acceptance-officer）
EVD-FAR-USE-001  registered（run receipt sha 16ab001000f4b346…）
Kanban           board far-first-use 4/4 done（R0-R8 / CHALLENGE / PATCH / VERIFY）
```

## 2. 研究過程（FAR 首次實戰，全程用 FAR 研究 FAR）

```text
question: FAR 落地流程補進 skill references 是否有幫助？
task_class: RESEARCH_WORKFLOW_OPTIMIZATION
router 實測: route(RESEARCH_WORKFLOW_OPTIMIZATION) = HGK_GOVERNED_EVOLUTION (FAR_ROUTE_EVO_LAB)
watchdog 實測: ActionWatchdog identical-action 偵測 + BudgetGuard（far_watchdog.py）
sources: 7 項 hash-verified（證據MD/Q0/gates/swarm/skill/FDA/藍圖）
```

## 3. 自迭代閉環（candidate → challenge → 修正 → 落地）

```text
初判: CL02「skill 缺 landing recipe」= SUPPORTED → 提案新增 far-shared-infrastructure-landing.md
challenge lane (deleg_f82657d3): REJECT-as-standalone — 與 shared-infra-team-implementation.md
  （平行 session 18:56 建立、SKILL.md line 644 已引用）整類重複；真新價值 ~30%
  （Q0 crosswalk / team 工件物化 / dogfood 慣例 / specialists 誠實）
自迭代 (DG01): CL02 → REFUTED_WITH_EVIDENCE；落點 → MERGE 增量進既有 reference + DELETE 草稿
落地: reference 新增 §10/§11/§12（161 行）；SKILL.md additive 註記；草稿刪除
closure: FAR_CHALLENGE_CLOSURE.json（F1..F7 逐項 disposition）
```

## 4. 研究工件 raw index（run FAR-20260813-002，SHA-256 from final bytes）

| # | Artifact | SHA-256 |
|---|---|---|
| ResearchRequest.yaml | `19fab4830c1e73c205e113841f84f7461d590fe3cbcf494b5a149a290b610b5e` |
| ResearchPlan.yaml | `0e7f8c18058834a3c8a4fe6352562ddb1ed4884b878f77d7e2151dac8b0aac4c` |
| ResearchSourceDenominator.tsv | `f3c3def5ec2294a655a1aec3e79ef2d54ce7fd2f42ce1d6f1543089d4221282d` |
| QueryLedger.tsv | `68e6bccf27ab2796d89aafe5f84a66b2d7725cf0207b0eb72b9895bddc9db9a5` |
| SourceSnapshotLedger.tsv | `73365237310dfef9c5294b62ab09c9461fb2d6f8353029c7411b288276bca660` |
| SourceDispositionLedger.tsv | `6386672932a166c1f70576ff7c2016fe1ef5923fb9d7f46cea442650bc0c6c3e` |
| ExtractionLedger.jsonl | `9b96f9b01466dab9fa4bc696c4a27d82452d8372ac17c606f0649914c2fb42b3` |
| HypothesisLedger.tsv | `ae048f0ecc635cc923b17ebd6eafba8916dd66f541c7c3a4da29a37a141c16c2` |
| FitGapLedger.tsv | `af22b59dc2ba62d04c803f922561587331500eea9dd926d2eeade5baff95fff5` |
| ContradictionLedger.tsv | `446bbff21bef34f88c2588f6421ac00c4752d2424f75d15708c3f0d39eb394e3` |
| ClaimLedger.tsv | `0676060ee33035984e9b9dc8dce1a193aceb90973d500432fbc149b3626650aa` |
| DisagreementLedger.tsv | `d4b66dde431de39bced6f41b859914d41dd9734b4bd4254c078d66f3fba38001` |
| RejectedAlternativeLedger.tsv | `ab2052582c45d66e8eceeaab35699d8519f9275114d1f61c12b41c9ea12f15ae` |
| OpenQuestionLedger.tsv | `0d1d5ee227822f8d2b312a5b1f5df1e201274552715ca6b16c790255e556a5fc` |
| ResearchSynthesis.md | `165e28381f78e5d009e23527175b4b52db9d4ff1fb40dbf5b8c85b0841f193c2` |
| CandidateResearch.yaml | `04508e833ae29cadcc6a5b0b5b1b8a8f58a7bd0424f26497d3c2b3c5a5f91538` |
| CandidateKnowledge.yaml | `9ced4398c8005e34c2f843a6bb1bc2e5f10d800cf298952ff3d441db1921a2e3` |
| ProposedEvolution.yaml | `4bae9eaba4eea7f74f6082b9cad2236ca3928f8020c00c86a3f8f7efb79e1dc7` |
| ResearchHandoff.yaml | `2eabe56113a20320967ab729dbc67c9d75c3cfecbe9d0fb405d3c07e3ea431d5` |
| ResearchRunReceipt.json | `16ab001000f4b346cebbec43b1541f9b0f00ebd96371ea2479e66044becab9f3` |

> 完整索引: `Fabric/fabric-autonomous-research/FAR_FIRST_USE_INDEX.json`
> 其他: challenge closure `Fabric/fabric-autonomous-research/FAR_CHALLENGE_CLOSURE.json`
> skill reference（patched）: `7e403e67ebcc60ccc7080fac9119fa10fa5de0dc87e94134162d5bef8e28f010`
> SKILL.md（patched）: `70d8a7ff06668a991a85fcc2c36a448e1dd98c87a45ab47a01a51292da62fe14`
> duplicate draft `far-shared-infrastructure-landing.md`: DELETED

## 5. 內部驗收（fresh-context AO lane）

```text
lane: deleg_60df62df
verdict: PASS
checks: 7/7 PASS
detail: n/a
```

## 6. 研究結論（對外回答）

**有幫助（HELPFUL）。** FAR 落地流程（WO 分批准入→CAPC→R0-R8 canary→雙 lane swarm→凍結順序）
已被證實可重複、有價值，並已固化為 skill 的 12 節落地 recipe（§10 dogfood/自升級慣例、
§11 Q0/team 物化清單、§12 specialists 誠實規則），未來同類 Shared Infrastructure Team 落地
與自升級/自進化需求皆可照此流程辦理。研究過程本身也證明 FAR 價值：challenge lane 抓到
「新檔已存在」的 maker 盲點，避免製造重複 recipe（reuse-first）。

## 7. Nonclaims

```text
NOT_ACCEPTANCE_PASS（本 MD 是證據，非驗收）
不改寫既有已接受 reference 內容（僅 additive §10/11/12）
無新控制面｜provider 未 self-accept｜SQS/live/remote 未觸及
```

```text
STOP
FAR_FIRST_USE = PASS（research + challenge + self-iterate + patch + internal acceptance）
FAR_EXTERNAL_FINAL_ACCEPTANCE = PENDING（外部驗收官）
```
