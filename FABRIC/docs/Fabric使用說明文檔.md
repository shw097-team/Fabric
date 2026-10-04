---
document_title: Fabric 使用說明文檔
document_version: v2026.08.13-r1
updated_at: 2026-08-13T00:20:00+08:00
product_scope: RP-002 / RP-002 v2.0 Fabric Governance + Assurance + Interop + Knowledge Foundation
current_status: Stage-2 externally accepted
authority_note: operational projection; normative truth lives in Master/Stage contracts/current machine truth
---

# Fabric 使用說明文檔

> 本文是 RP-002 v2.0 的 **operator-facing projection**（操作投影），不是 authority / policy source / requirement source。
> 權威真相（normative truth）以 Master/Stage contracts 與 current machine truth 為準：`Fabric\rp002\RP002_STAGE_CROSSWALK.yaml`（master sha256 `3bc4ad6c…`）、`Fabric\rp002\RP002_GATE_CATALOG.yaml`、`Fabric\rp002\RP002_EXECUTION_GRAPH.yaml`，以及 `Fabric\stage\RP002-STAGE-HGK\` 下已封存的 seal / handoff / gate receipts。
> **Current status**: Stage-2 externally accepted（`Fabric\stage\RP002-STAGE-HGK\EXTERNAL_ACCEPTANCE_RECEIPT_STAGE2.yaml`，`external_verdict: PASS_CHALLENGE`、`external_meta_acceptance: GRANTED`）。Next gate = `SQP1`（NOT_AUTHORIZED）。本文件不宣稱 Stage-3 / SQP1 已執行，也不宣稱 production / live / remote。

## 0. 快速開始（讀我順序）

第一次接觸 Fabric 的 operator，依下列順序閱讀：

1. 本文件 §1–§3（身份、root、責任邊界）。
2. `Fabric\rp002\RP002_STAGE_CROSSWALK.yaml` — master/stage 對照與 digest。
3. `Fabric\rp002\RP002_GATE_CATALOG.yaml` — gate 詞彙（哪些 gate 存在、哪些歷史名不執行）。
4. `Fabric\stage\RP002-STAGE-HGK\STAGE-2-SEAL-REPAIRED.yaml` — 目前 accepted 狀態的 seal。
5. `Fabric\stage\RP002-STAGE-HGK\EXTERNAL_ACCEPTANCE_RECEIPT_STAGE2.yaml` — external acceptance 的 non-claims。
6. 依任務需要讀 §4–§15；出問題讀 §18。

**三個最重要的紀律**：FILES_FIRST（先讀實際檔案）、NO_SOURCE_NO_CLAIM（無 raw evidence 不 claim PASS）、policy presence ≠ policy consumption（檔案存在不等於被消費）。

## 1. Fabric 是什麼／不是什麼

**Fabric 是 governance / assurance / interop / knowledge 的 contract surface（契約表面）。**

- 它是策略、契約、schema、profile、assurance pack、knowledge governance 規則的家。
- 它是被其他元件**實際消費**的凍結政策與契約來源（例如 HGK router 讀取 `Fabric\control\CHANGE_CLASS_ROUTER.yaml`，見 §5、§8）。
- 它是 Stage-2 之後由 HGK 普通任務消費的 policy surface（F0 real policy consumption）。

**Fabric 不是：**

- **不是 OS**：不管理 process、不提供 kernel、不是作業系統。
- **不是 daemon / service**：沒有常駐背景服務、沒有自己的監聽埠（ContextForge gateway 是 registered 的第三方 interop 元件，不是 Fabric daemon）。
- **不是第二 scheduler**：不取代 Hermes 的 runtime orchestration；Direct/Kanban/Swarm 語義由 HGK router 決定（`Fabric\stage\RP002-STAGE-HGK\S2_ROUTER_EVIDENCE.json`）。
- **不是第二 task DB**：不取代 Shared Spine / kanban.db；不持有 normative task 狀態（WorkOrder 才是 normative task truth）。
- **不是第二 reducer**：不取代 HGK reducers / acceptance oracle（`Fabric\stage\RP002-STAGE-HGK\STAGE2_REDUCER_RECEIPT_REPAIRED.json`）。
- **不是第二 HGK**：不建立第二 control plane。
- **不是第二 knowledge platform**：不取代 HGK Memory / RAG / KG / Obsidian 的分工（見 §11）。
- **不是 Hermes 的替代品**：Hermes 仍是 runtime / orchestrator（見 §14）。
- **不是 Codex 的替代品**：Codex 仍是 bounded tracked writer。

## 2. canonical root 與主要目錄

`C:\Projects\Agent_Workspace\Fabric` 是唯一 canonical Fabric root（governance 契約面；不作為 runtime code 寫入區）。

```text
Fabric\
├─ control\            # 凍結政策：AUTHORITY_MATRIX / SOD / RISK / CHANGE_CLASS_ROUTER / ACCEPTANCE /
│                       #   BREAK_GLASS / CAPABILITY_QUALIFICATION / PROMOTION / RELEASE / EVOLUTION /
│                       #   KNOWLEDGE / MEMBER / PROFILE_STACK_REGISTRATION
├─ contracts\          # schema contracts：AUTHORITY_RECEIPT / CANDIDATE_MANIFEST / FABRIC_CHANGE_PACKAGE /
│                       #   FABRIC_COLLABORATION_ABI / PROMOTION_RECEIPT / ROLLBACK_RECEIPT
├─ assurance\          # EVIDENCE_CONTRACT / ACCEPTANCE_SCHEMA / PROFILE_ROLE_CONTRACTS /
│                       #   BOOTSTRAP_META_ACCEPTANCE_POLICY / acceptance-packs\（8 packs）
├─ profiles\           # hgk-orchestrator / hgk-knowledge-factory / hgk-document-factory /
│                       #   hgk-coding-factory / construction-acceptance-oracle（runtime-contract READMEs）
├─ rp002\              # RP-002 主體：MASTER_REF / GATE_CATALOG / EXECUTION_GRAPH / STAGE_CROSSWALK /
│                       #   PROFILE_TEAM_MANIFEST / EXECUTION_BINDING.schema / gate 工件
├─ stage\RP002-STAGE-HGK\   # Stage-2 seal / handoff / gate receipts / evidence（immutable）
├─ evidence\review\    # external review bundle 與獨立審查證據
├─ HGK\                # HGK TEAM / stack manifest / gstack 快照（Stage-2 materialized）
└─ HGK_STACK_MANIFEST.yaml
```

主要唯讀入口（operator 請先讀）：

- `Fabric\rp002\RP002_STAGE_CROSSWALK.yaml` — master/stage 對照與 digest（master `3bc4ad6c…`、stage-2 `66c4f708…`、subject `946de0d7…`）
- `Fabric\rp002\RP002_GATE_CATALOG.yaml` — 唯一 machine gate 詞彙（G0…R1；歷史名 `KBN1` / `FG1` do-not-execute）
- `Fabric\stage\RP002-STAGE-HGK\STAGE-2-SEAL-REPAIRED.yaml` — Stage-2 退出 seal（`12da14ac…`）
- `Fabric\stage\RP002-STAGE-HGK\STAGE2_TO_STAGE3_HANDOFF_REPAIRED.yaml` — Stage-2→3 handoff（`93a7da26…`）
- `Fabric\stage\RP002-STAGE-HGK\EXTERNAL_ACCEPTANCE_RECEIPT_STAGE2.yaml` — external acceptance receipt（`EXT-ACC-RP2-S2-20260813`）

## 3. 責任邊界

```text
HG-KSEOS           = control plane（normative：WorkOrder admission、SharedSpine、reducers、acceptance、release）
Hermes             = runtime / orchestrator（Kanban、/goal、checkpoint、tool recovery、compression、approvals）
Codex              = bounded tracked writer（WorkOrder writer=codex；sealed lane）
Acceptance Officer = independent verifier（O1 之後的 L2 checker；VERIFY_ONLY）
Fabric             = governance / assurance / interop / knowledge contract surface（本文件主體）
```

- HGK 是唯一 control plane；Fabric 不建立第二 control plane。
- Hermes 被 HGK 治理綁定（`HG-KSEOS\config\hermes.json`，schema `HGK-HERMES-BINDING/2`，v0.20.0）；Hermes runtime state ≠ HGK normative state。
- Acceptance Officer 在 O1 之後是 default L2 checker（`Fabric\stage\RP002-STAGE-HGK\O1\BOOTSTRAP_ACCEPTANCE_RECEIPT_O1.yaml`：`default_l2_checker_after_o1: acceptance-officer`）；officer 不得寫 candidate、不得 repair、不得 promote、不得 release。
- maker（writer/orchestrator）不得 self-accept；commander 不得簽 final AcceptanceReceipt（`O1\O1_VERIFICATION.json`：DIFFERENT_IDENTITIES、DIFFERENT_DISTRIBUTION_DIGESTS、OFFICER_VERIFY_ONLY、COMMANDER_DENIES 全 PASS）。

## 4. contract families

`Fabric\control\` + `Fabric\contracts\` + `Fabric\assurance\` 提供以下 family（每 family 有對應 schema / policy 檔案）：

| Family | 政策/契約檔案 | 主要消費者 |
|---|---|---|
| authority/governance | `AUTHORITY_MATRIX.yaml`、`MEMBER_POLICY.yaml`、`AUTHORITY_RECEIPT.schema.yaml` | HGK admission / commander |
| risk/change | `RISK_POLICY.yaml`、`CHANGE_CLASS_ROUTER.yaml`、`FABRIC_CHANGE_PACKAGE.schema.yaml` | HGK router / change class 判定 |
| SoD | `SOD_POLICY.yaml` | O1 / commander vs officer 分離 |
| acceptance/evidence | `ACCEPTANCE_POLICY.yaml`、`ACCEPTANCE_SCHEMA.yaml`、`EVIDENCE_CONTRACT.yaml`、`acceptance-packs\`（8）、`CANDIDATE_MANIFEST.schema.yaml` | acceptance-officer |
| capability qualification | `CAPABILITY_QUALIFICATION_POLICY.yaml`、`PROFILE_ROLE_CONTRACTS.yaml`、`PROFILE_STACK_REGISTRATION_POLICY.yaml` | H1 / profile runtime |
| promotion/release | `PROMOTION_POLICY.yaml`、`RELEASE_POLICY.yaml`、`PROMOTION_RECEIPT.schema.yaml` | F1 / release gate |
| BreakGlass | `BREAK_GLASS_POLICY.yaml`、`ROLLBACK_RECEIPT.schema.yaml` | failure / rollback 路徑 |
| collaboration ABI | `FABRIC_COLLABORATION_ABI.schema.yaml` | 跨 stack 契約面 |
| knowledge governance | `KNOWLEDGE_POLICY.yaml` | KG1 namespace / promotion |
| registration/interop | `rp002\RP002_EXECUTION_BINDING.schema.json`、`rp002\RP002_INTEROP_PROMOTION_TRANSACTION.yaml`、OASF `oasf-record/1` | B1 / CF1 / F1 |

Stage-1 已把 contracts 凍結（`control\STAGE1_CONTRACT_EXACT_SET.yaml`、`STAGE1_TOOL_CAPABILITY_FREEZE_MATRIX.yaml`）；Stage-2 由 HGK 實際消費（§5、§8）。

## 5. Stage-1 passive foundation → Stage-2 active consumption（F0 real policy consumption）

- **Stage-1（RP002-STAGE-FABRIC，G0/G1）**：Fabric 契約面被凍結與驗證，屬「被動 foundation」（seal `d1a219a5…`）。
- **Stage-2（RP002-STAGE-HGK，K1…KG1）**：Fabric 政策被 HGK **實際消費**。`F0\ACCEPTANCE_RECEIPT_F0.yaml`（ACC-F0-20260812）記錄 6-step policy consumer chain：

```text
frozen policy（CHANGE_CLASS_ROUTER.yaml sha 0839ead5）
→ HGK route / SharedSpine（REQ-RP2-STAGE2-001 FROZEN，EVT-b54fa975）
→ admission/classification/routing decision（S2_ROUTER_EVIDENCE.json：stage2 NATIVE、brownfield OPENSPEC、review GSTACK）
→ WorkOrder / ExecutionBinding（WO-RP2-STAGE2-001 / BIND-RP2-S2-001）
→ Hermes dispatch（kanban board RP002-FABRIC-BOOTSTRAP，task t_c69537e5，claim + heartbeat）
→ evidence（B1_WORKER.log PID 10772 + gate receipts）
```

- consumed policies 至少 4 份：`CHANGE_CLASS_ROUTER.yaml`、`SOD_POLICY.yaml`、`ACCEPTANCE_POLICY.yaml`、`KNOWLEDGE_POLICY.yaml`（`F0\F0_POLICY_CONSUMER_TRACE.json`）。
- `yaml_presence_alone: NOT_ACCEPTED`：policy 檔案存在 ≠ policy 被消費；PASS 需要 trace 級證據。

## 6. construction-commander 使用方式

Profile：`HG-KSEOS\profiles\construction-commander\distribution.yaml`（distribution digest `e682655a…`，O1 驗證）。

- Mission：classify/compile bounded engineering request → issue admitted HGK WorkOrder → request smallest bounded repair。
- Allowed：classify/compile、create/issue admitted WorkOrder、request smallest bounded repair。
- Denied：candidate code write、final AcceptanceReceipt、promotion/release（`O1\O1_VERIFICATION.json`：COMMANDER_DENIES）。
- 使用情境：human 以 commander 身份把目標/來源送進 HGK admission；commander 不寫 candidate、不簽 acceptance、不 promote。
- 實例：Stage-2 commander 簽發 `WO-RP2-STAGE2-001` 與 repair `WO-RP2-S2R-001`（delegation `DEL-RP2-S2-001`，見 `B1\B1_EXECUTION_BINDING.json`）。

## 7. acceptance-officer 使用方式（VERIFY_ONLY）

Profile：`HG-KSEOS\profiles\acceptance-officer\distribution.yaml`（distribution digest `1404bb48…`；O1 後 default L2 checker）。

- Mission：VERIFY_ONLY；fresh context；candidate 唯讀；acceptance packs 唯讀。
- Allowed write：temp、acceptance evidence、AcceptanceReceipt。
- Denied：candidate write、WorkOrder create、repair、acceptance-pack/evaluator mutation、promotion、release、deploy。
- 檢查基準：fresh_session、positive/negative fixtures、`Fabric\assurance\ACCEPTANCE_SCHEMA.yaml`、`Fabric\assurance\EVIDENCE_CONTRACT.yaml`、`Fabric\assurance\acceptance-packs\`（8 packs：hermes-runtime、kanban-runtime、knowledge、profile、provider、skill、sqs-financial-bridge、stack）。
- Officer 不能修 candidate；發現 defect 只能回報，由 maker 修、再獨立 recheck（maker ≠ checker 循環）。
- 歷史實例：ACC-B1 / ACC-F0 / ACC-CF1-REPAIRED / ACC-F1-REPAIRED / ACC-KG1 均由 acceptance-officer 簽署（`candidate_write_capability: false`）。

## 8. HGK 普通任務如何實際消費 Fabric policy

普通任務（goal/source → admission）不是直接讀 README，而是走 machine 可稽核路徑：

1. Source admission → Requirement freeze（SharedSpine EVT）→ TaskSpec → WorkOrder（writer=codex）。
2. HGK router（`hg_kseos.named_methods.route`）查 `Fabric\control\CHANGE_CLASS_ROUTER.yaml` 與 `Fabric\rp002\RP002_CHANGE_CLASS_ROUTER.yaml`，決定 route / risk class（`S2_ROUTER_EVIDENCE.json`）。
3. SoD / permission 查 `Fabric\control\SOD_POLICY.yaml`；risk 查 `RISK_POLICY.yaml`；change class 查 `CHANGE_CLASS_ROUTER.yaml`。
4. 執行期：acceptance 依 `ACCEPTANCE_POLICY.yaml` + `acceptance-packs\`；knowledge 依 `KNOWLEDGE_POLICY.yaml`（KG1 namespace 規則）。
5. 每次消費記錄 consumption trace（`F0\F0_POLICY_CONSUMER_TRACE.json` 為模板）：policy artifact + sha256 + consumer + evidence。
6. PASS 條件 = raw evidence + trace，不是「policy 檔案存在」。

consumer 實作：`Fabric\fabric\consumers\hgk_policy_consumer.py`（HGK policy consumer）。

## 9. Profile / TEAM / Stack / ExecutionBinding / Kanban 關係

- **Profile** = 能力契約（mission / allowed / denied / distribution digest）。Stage-2 驗證 5 個 persistent P0 profiles：`hgk-orchestrator`、`hgk-coding-factory`、`hgk-engineering-reviewer`、`hgk-qa`、`hgk-security`（`H1\BOOTSTRAP_ACCEPTANCE_RECEIPT_H1.yaml`；`role_not_profile_not_worker: true`）。
- **TEAM** = `Fabric\HGK\TEAM.md` / `HG-KSEOS\HGK\TEAM.md`（project team projection；P0 + governance profiles + on-demand workers）。
- **Stack** = `Fabric\HGK_STACK_MANIFEST.yaml` / `HG-KSEOS\HGK\HGK_STACK_MANIFEST.yaml`（stack_id `HGK_ENGINEERING`；authority domain、knowledge namespace、runtime engine hermes、acceptance oracle construction-acceptance-oracle、inherited capabilities）。
- **ExecutionBinding** = 單一 WorkOrder 的執行契約。`B1\B1_EXECUTION_BINDING.json`（schema `RP002-EXECUTION-BINDING/2`，canonical、無 child fork）包含：`normative.workorder_id`、`routing.topology_mode`（Stage-2 實例 = DIRECT）、`routing.profile_id`（hgk-orchestrator）、`delegation`（issuer construction-commander / assignee hgk-orchestrator / expires）、`lease`（LS-RP2-S2-001 / ttl 3600 / renewable）、`budget`（step 10 / retry 2 / no-progress detector）、`idempotency`（RP2-S2-B1-RUN-001 / safe-replay）、`runtime.workspace_or_worktree`（`Fabric\stage\RP002-STAGE-HGK\B1`）、`runtime.candidate_write_set`（`B1/*`）、`terminal.worker_exit_zero_is_pass: false`。
- **Kanban** = 協調狀態（coordination state），**不是 authority**；board `RP002-FABRIC-BOOTSTRAP` 是 Stage-2 實例（B1：task `t_c69537e5`、claim + heartbeat、toolset kanban_show/heartbeat/complete/assign/claim/link）。normative task truth 在 WorkOrder；Kanban 是 thin adapter（SharedSpine 只存 pointer/ref）。
- 關係鏈（F1 canary 證明）：`WORKORDER → EXECUTION_BINDING → PROFILE → KANBAN`（`F1\F1_POST_CUTOVER_CANARY_REPAIRED.json`）。

## 10. ContextForge / OASF / MCP / A2A 的 accepted role

- **ContextForge**：`mcp-contextforge-gateway` v1.0.7 @ commit `4092d33676f9b57d3f9e547921e9d62e36719a41`，Apache-2.0，package digest `90e2d05b…`，註冊 `CF-REG-RP2-S2-001`。lifecycle（identity/version/commit/digest/license/install/config/secret-policy/register/discover/invoke/MCP/auth-negative/disable/rollback）ALL PASS（`CF1\ACCEPTANCE_RECEIPT_CF1_REPAIRED.yaml`）。
- **Interop 角色**：MCP / A2A / REST 閘道與 registry 的 interop surface；`openapi.json` 標題為 "ContextForge AI Gateway — an AI gateway, registry, and proxy for MCP, A2A, and REST/gRPC APIs"。
- **auth 證據**：401 auth-negative（unauthenticated `/openapi.json`、`/admin` → 401）+ authenticated positive discovery（`POST /auth/login` 200、`GET /openapi.json` Bearer 200、`GET /v1/gateways` 200 → `[]`），見 `CF1\CF1_DISCOVERY_FOCUSED_RECEIPT.yaml`。
- **Secret policy**：env-var `REFERENCE_ONLY`；placeholder `__REPLACE_ME__` 在 ALL environments 被拒（fail-closed）。
- **OASF**：`oasf-record/1`，記錄 `OASF-REC-RP2-S2-001`（subject HGK-REFERENCE-PROJECT-002；`CF1\OASF_RECORD_SAMPLE.json`）。
- **F1 同 subject promotion**：`TX-RP2-S2-F1-002-REPAIRED`（digest `d6ebaa13…`）在**同一 subject**（`946de0d7…`）內把 ContextForge registration / auth-policy lineage 帶入 interop promotion transaction（`F1\F1_INTEROP_PROMOTION_TRANSACTION_REPAIRED.json`）。
- 舊的 degraded state（`CF1\CF1_QUALIFICATION.json` PASS_WITH_DEGRADED_CONTEXTFORGE）已被 `SUPERSEDED_ARTIFACTS.yaml` 標記為歷史證據，**不再作為 current truth**。

## 11. Knowledge / Memory / RAG / KG / Obsidian：canonical vs derived

- **Canonical source**：Git Markdown / Source Ledger / SharedSpine / Fabric contracts（frozen）。canonical ≠ RAG/KG/wiki。
- **Knowledge Workbench / Obsidian**：human view（`C:\Projects\Agent_Workspace\知識庫` Obsidian vault）；derived。
- **LLM Wiki / RAG / KG**：derived compilation / retrieval surfaces；任何 agent 產出都是 **candidate**。
- **KG1 namespace model**（`KG1\KG1_NAMESPACE_MODEL.json`）：`hgk.candidate.*`（agent write）、`hgk.approved.*`（promotion-gate write）、`hgk.revoked.*`（revocation-gate write + tombstone）、`fabric.*`、`assurance.*`、`sqs.*`（stage2 read-only）、`shared.approved.*`。
- **規則**：agent_write = candidate only；promotion = owner/gate only（agent 禁止 self-promote）；forget = tombstone + audit receipt；revoked/stale excluded；cross-stack export = explicit promotion（`KG1\ACCEPTANCE_RECEIPT_KG1.yaml` runtime evidence：K-001 candidate→approved→revoked + tombstone）。
- **Provider state**（`KG1\KG1_PROVIDER_LEDGER.json`）：SQLite/FTS5 P0 REUSE（active）、HGK Memory P0 REUSE（candidate ≠ truth）、Qdrant/Neo4j default-off（not-installed）、pgvector conditional、Cognee P1 shadow。
- derived knowledge 不是 authority；只有 `hgk.approved.*` 是消費級知識，且 promotion 需 gate。

## 12. Evidence / receipt / subject-candidate binding

- 每個 gate receipt（`BOOTSTRAP_ACCEPTANCE_RECEIPT_*.yaml` / `ACCEPTANCE_RECEIPT_*.yaml`）綁定：`master_digest`（`3bc4ad6c…`）、`stage_digest`（`66c4f708…`）、`subject_digest`（`946de0d7…`）、`acceptor_profile_id`（acceptance-officer）、`acceptor_distribution_digest`（`1404bb48…`）、`fresh_session`、`candidate_write_capability: false`。
- PASS 需要 raw evidence refs（`raw_evidence_refs` 指向實際檔案）+ independent lane（`independent_lane_evidence`）。
- `yaml_presence_alone: NOT_ACCEPTED`（F0）、`worker_exit_zero_is_pass: false`（B1 terminal）：存在與 exit code 都不是 PASS。
- **Subject-candidate binding**：subject digest 跨 K1..KG1 與 repair 不變（`KG1\KG1_FOCUSED_CONSISTENCY_RECEIPT.yaml`：`subject_consistency PASS`）；candidate digest 各 gate 不同（`candidate_digest` 欄位）。
- External review bundle：`Fabric\evidence\review\RP002_STAGE-2_KG1_EVIDENCE_FOR_EXTERNAL_REVIEW.md`（sha `104d4cf2…`，Fabric/HGK mirror byte-identical；`RP002_STAGE-2_EXTERNAL_BUNDLE_HASHES.json`）。

## 13. rollback / BreakGlass / failure / TT-CR

- **Rollback pointer**：`SUPERSEDED_ARTIFACTS.yaml` 保存被取代工件（prior CF1 receipt、prior F1 tx `149a137e…`、prior STAGE-2-SEAL `14726894…`、prior handoff、prior review bundle），全部 preserved unchanged。rollback 依 pointer 還原，不做整輪重做。
- **BreakGlass**：`Fabric\control\BREAK_GLASS_POLICY.yaml`；legacy bypass 僅 `BREAK_GLASS_ONLY`（F1 canary）；Stage-2 seal 的 `open_breakglass_count: 0`；BreakGlass 必須 explicit + audited。
- **Failure**：attempt budget 耗盡 → FAILED + STOP_ESCALATE；blocking TT/CR = 0 才可收斂（`S2R_FINDING_CLOSURE.yaml`：`blocking_tt_cr: 0`）。
- **TT / CR**：carried forward 到下一 gate / stage（RESUME checkpoint 保留 `tt_cr: 0`）；不靜默丟棄。
- 本次 repair（S2-EXT-001/002/003）finding closure：`S2R_FINDING_CLOSURE.yaml`（CLOSED_LOCAL、independent lanes all PASS、`unauthorized_side_effects: 0`、`live_broker_writes: 0`）。

## 14. Hermes 操作理解 chain

1. **身份/綁定**：`HG-KSEOS\config\hermes.json`（schema `HGK-HERMES-BINDING/2`，status `ACTIVE_SELECTED_REINSTALL_BASELINE`）；Hermes v0.20.0 / tag `v2026.8.3` / commit `3c27eb62…`（exact 對齊）。
2. **執行檔**：`C:\Users\user\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe`；canonical HERMES_HOME `C:\Users\user\AppData\Local\hermes`；provider `opencode-go` / `deepseek-v4-flash`（base `https://opencode.ai/zen/go/v1`）。
3. **角色**：Hermes = runtime / orchestrator（Kanban、/goal、SessionDB、checkpoint、tool recovery、compression、approvals）；被 HGK 治理綁定；不自行 promote、不當 release authority。
4. **Stage-2 實證**：`B1\B1_WORKER.log`（worker PID 10772）+ kanban board `RP002-FABRIC-BOOTSTRAP` task `t_c69537e5` claim/heartbeat/complete（F0 6-step chain step 5）。
5. **Rollback baseline**：v0.18.2（`v2026.7.7.2` / `9de9c25f…`）RECOVERY_ONLY。
6. **證據**：`HG-KSEOS\evidence\review\HG-KSEOS_HERMES_V020_*.json`（identity、provider-route、kanban、goal-contract、tool-recovery、approvals、compression、skill-governance、rollback、independent-acceptance…）。
7. **理解鏈**：Hermes runtime state ≠ HGK normative state；`/goal done` ≠ HGK PASS；final acceptance 仍需 raw evidence → independent checker → reducers → release。

## 15. 常見工作流程 examples

- **Example A — 新需求（普通任務）**：user goal/source → HGK admission（Requirement freeze → TaskSpec → WorkOrder writer=codex）→ router 決定 Direct/Kanban/Swarm → ExecutionBinding → Profile 分派 → Hermes/Codex 實作 → tests → officer VERIFY_ONLY → reducers → local delivery。查狀態：`project status <id>`；中斷恢復：`project resume <id>`。
- **Example B — 政策查詢**：想確認 change class 權限 → 讀 `Fabric\control\CHANGE_CLASS_ROUTER.yaml`（sha `0839ead5…`）+ `Fabric\control\SOD_POLICY.yaml`；不要只看 README。
- **Example C — 知識寫入**：agent 產出 → 寫入 `hgk.candidate.*` → owner/gate 審查 → promote 到 `hgk.approved.*` → revoke 走 tombstone（`KG1\KG1_RUNTIME.db` 實證）。
- **Example D — interop 登錄**：新 MCP/A2A 元件 → CF1 同款 qualification（identity/version/commit/digest/license/install/config/secret-policy/register/discover/invoke/auth-negative/disable/rollback）→ OASF record → F1 同 subject promotion transaction。
- **Example E — 驗收**：officer 開 fresh session，讀 candidate + acceptance packs（8 packs），跑 positive/negative fixtures，只寫 acceptance evidence + AcceptanceReceipt；不修 candidate。

## 16. 禁止事項與錯誤用法

- 禁止把 Fabric 當 OS / daemon / scheduler / task DB / reducer / second HGK / knowledge platform。
- 禁止「policy 檔案存在 → PASS」的 proxy 判斷（F0 `yaml_presence_alone: NOT_ACCEPTED`）。
- 禁止 maker self-accept、commander 簽 final receipt、officer 修 candidate / promote / release / deploy。
- 禁止 agent self-promote 知識、直接寫 `hgk.approved.*`、繞過 tombstone forget。
- 禁止把 derived（Obsidian / LLM Wiki / RAG / KG / 本文件）當 authority。
- 禁止以任何 docs 推斷 gate 已執行；以 `RP002_GATE_CATALOG.yaml` + stage seals + receipts 為準。
- 禁止浮動版本（floating latest）、靜默 fallback、fake invocation、未授權網路/秘密/remote/production mutation。
- 禁止改寫 immutable receipts / seal / handoff（Stage-2 已 external accepted；修復走 repair 流程並保留 superseded 原件）。
- 禁止在本文件任務內執行 Stage-3 / SQP1。

## 17. nonclaims / Stage-3 boundary

- **SQP1 NOT executed**；Stage-3 contract `NOT_YET_COMPILED`（`RESUME_CHECKPOINT_STAGE3_ENTRY.yaml`：`stage3_contract: NOT_YET_COMPILED`、`next_allowed_action: COMPILE_STAGE3_CONTRACT_ONLY`）。
- Stage-3 授權：`NOT_AUTHORIZED_UNTIL_STAGE3_CONTRACT_COMPILED`（checkpoint）＋ `NOT_AUTHORIZED_UNTIL_EXTERNAL_PASS`（handoff）；resume token `RESUME:RP002_STAGE3_SQP1_ENTRY`。
- **production / live / remote**：`production_autonomy: NOT_CLAIMED`、`sqs_live_trading: NOT_AUTHORIZED`、`remote_deployment: NOT_CLAIMED`（`EXTERNAL_ACCEPTANCE_RECEIPT_STAGE2.yaml` non_claims）。
- claim ceiling：`RP002_STAGE2_LOCAL_ACCEPTANCE_PASS_REPAIRED_CANDIDATE` + external `PASS_CHALLENGE`；Stage-2 = `EXTERNALLY_ACCEPTED`；SQS stack = `PENDING_STAGE3_NOT_YET_MATERIALIZED`（`HGK\TEAM.md` invariants）。

## 18. troubleshooting / readback 命令與證據路徑

Readback 命令（HGK CLI 語法已驗證；`PYTHONPATH` 指向 `HG-KSEOS\src`）：

```text
$env:PYTHONPATH='C:\Projects\Agent_Workspace\HG-KSEOS\src'
'.venv\Scripts\python.exe' -m hg_kseos --root 'C:\Projects\Agent_Workspace\HG-KSEOS' doctor
'.venv\Scripts\python.exe' -m hg_kseos --root 'C:\Projects\Agent_Workspace\HG-KSEOS' project status <project_id>
'.venv\Scripts\python.exe' -m hg_kseos --root 'C:\Projects\Agent_Workspace\HG-KSEOS' project resume <project_id>
'.venv\Scripts\python.exe' -m hg_kseos --root 'C:\Projects\Agent_Workspace\HG-KSEOS' project checkpoint <project_id>
```

- **Stage 證據根**：`Fabric\stage\RP002-STAGE-HGK\`（`STAGE-2-SEAL-REPAIRED.yaml`、`STAGE2_TO_STAGE3_HANDOFF_REPAIRED.yaml`、`EXTERNAL_ACCEPTANCE_RECEIPT_STAGE2.yaml`、`S2R_FINDING_CLOSURE.yaml`、`SUPERSEDED_ARTIFACTS.yaml`、`RESUME_CHECKPOINT_STAGE3_ENTRY.yaml`）。
- **Review 證據**：`Fabric\evidence\review\RP002_STAGE-2_KG1_EVIDENCE_FOR_EXTERNAL_REVIEW.md`（+ `RP002_STAGE-2_EXTERNAL_BUNDLE_HASHES.json`；mirror equal）。
- **Gate receipts**：`K1\`、`D1\`、`C1\`、`H1\`、`O1\`、`B1\`、`F0\`、`CF1\`、`F1\`、`KG1\` 下各 `*_RECEIPT*.yaml` / `*_RECEIPT*.json`。
- **常見檢查**：hash 對不上 → 以 `RP002_STAGE-2_EXTERNAL_BUNDLE_HASHES.json` 為準重讀；status 顯示 NOT_AUTHORIZED → 讀 `RESUME_CHECKPOINT_STAGE3_ENTRY.yaml`；finding open → 讀 `S2R_FINDING_CLOSURE.yaml` 的 evidence refs。

## 19. version / changelog

- `v2026.08.13-r1`（本文件）：基於 Stage-2 externally accepted 狀態撰寫；更新 external acceptance、repaired CF1/F1/KG1、RESUME checkpoint、SQP1 boundary、evidence paths。
- 歷史：`Fabric\evidence\review\RP002_EVIDENCE_FOR_EXTERNAL_REVIEW.md`（Stage-1/早期）、`RP002_POST_HERMES_REINSTALL_HANDOFF.md` / `RP002_PRE_HERMES_REINSTALL_HANDOFF.md`（Hermes reinstall 前後 handoff，historical）、`SUPERSEDED_ARTIFACTS.yaml`（被取代工件清單）。
- 本文件是 projection；每次操作前 fresh-read stage seals / machine truth，不要以本文件取代 contracts。

## 附錄 A — 常用 digest 速查（2026-08-13）

| 工件 | sha256（前 8 位） |
|---|---|
| Master r2（RP002_V2_MASTER_BLUEPRINT_20260812_R2） | `3bc4ad6c` |
| Stage-2 r2 contract | `66c4f708` |
| Subject | `946de0d7` |
| STAGE-2-SEAL-REPAIRED | `12da14ac` |
| STAGE2_TO_STAGE3_HANDOFF_REPAIRED | `93a7da26` |
| External review bundle（Fabric/HGK mirror identical） | `104d4cf2` |
| TX-RP2-S2-F1-002-REPAIRED | `d6ebaa13` |
| CHANGE_CLASS_ROUTER.yaml（frozen） | `0839ead5` |
| acceptance-officer distribution | `1404bb48` |
| construction-commander distribution | `e682655a` |
| ContextForge package digest（1.0.7） | `90e2d05b` |

完整 hash 以 `Fabric\stage\RP002-STAGE-HGK\` 與 `Fabric\evidence\review\RP002_STAGE-2_EXTERNAL_BUNDLE_HASHES.json` 為準。

## 附錄 B — 名詞對照（operator glossary）

| 名詞 | 意思（以本文件語境） |
|---|---|
| Fabric | governance / assurance / interop / knowledge 契約表面（本文件主體） |
| HG-KSEOS（HGK） | 唯一 governance / normative control plane |
| Hermes | runtime / orchestrator（Kanban、/goal、checkpoint、tool recovery） |
| Codex | bounded tracked writer（WorkOrder writer=codex） |
| Acceptance Officer | O1 之後的 independent verifier（VERIFY_ONLY） |
| Stage-2 / Stage-3 | RP-002 執行階段；Stage-2 = HGK self-hosting + Fabric activation（EXTERNALLY_ACCEPTED） |
| SQP1 | Stage-3 第一個 gate；目前 NOT_AUTHORIZED |
| WorkOrder | normative task truth（admitted 後的任務契約） |
| ExecutionBinding | 單一 WorkOrder 的執行契約（BIND-RP2-S2-001） |
| Profile | 能力契約（mission / allowed / denied / digest） |
| TEAM / Stack | 專案團隊投影 / 工程 stack 清單（HGK_ENGINEERING） |
| Kanban | 協調狀態（coordination state），不是 authority |
| Shared Spine | HGK canonical DB（typed API、單一 writer） |
| Receipt | gate 通過的 immutable 證據（綁 master/stage/subject digest） |
| Seal / Handoff | 階段退出封存 / 階段移交契約 |
| candidate / approved / revoked | KG1 知識 namespace 狀態（agent 只能寫 candidate） |
| OASF | Open Agent Service Format（oasf-record/1） |
| ContextForge | mcp-contextforge-gateway v1.0.7（MCP/A2A interop 閘道） |
| BreakGlass | 明確記錄的例外繞行路徑（BREAK_GLASS_ONLY、audited） |
| TT / CR | technical debt / change request（carried forward） |
| PROMPT_COMPILE_PASS | Prompt Compiler 對單一 contract 的編譯通過（≠ RUNTIME_READY ≠ EXTERNAL_ACCEPTANCE） |

> 本附錄僅為查閱便利；定義衝突時以 contracts / machine truth 為準。
