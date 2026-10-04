---
document_title: HG-KSEOS 使用說明文檔
document_version: v2026.08.13-r1
updated_at: 2026-08-13
product_scope: HG-KSEOS local P0 / RP-002 v2.0 (HGK-REFERENCE-PROJECT-002)
current_status: Stage-2 externally accepted (RP-002); next gate SQP1 NOT_AUTHORIZED
authority_note: operational projection; normative truth lives in Master/Stage contracts/current machine truth
---

# HG-KSEOS 使用說明文檔

> 本文是 **projection / operational manual**，不是 authority / policy source / requirement source。
> 權威來源依 Master/Stage contracts 與 current machine truth：RP-002 master（sha `3bc4ad6c…`）、Stage-2 r2（`66c4f708…`）、subject（`946de0d7…`）、`Fabric\stage\RP002-STAGE-HGK\` 內 seal / handoff / receipts。
> **Current claim**: RP-002 v2.0 **Stage-2 externally accepted**（`Fabric\stage\RP002-STAGE-HGK\EXTERNAL_ACCEPTANCE_RECEIPT_STAGE2.yaml`，`PASS_CHALLENGE` / `GRANTED`）。Next gate = **SQP1（NOT_AUTHORIZED）**；本文件任務**不執行 Stage-3 / SQP1**。Production / live / remote 一律 `NOT_CLAIMED`。
> 歷史 local delivery lineage（Task-011..015、A-3 delta 等）保留為 accepted historical lineage，見 §33 Changelog / Historical Baselines。

---

# Part 0 — RP-002 v2.0 更新總覽（v2026.08.13-r1）

本節收斂 RP-002 v2.0 Stage-2 之後的 currentness delta；細部見對應章節。

1. **Canonical identity / root**：`C:\Projects\Agent_Workspace\HG-KSEOS` 仍是唯一 canonical local root（writable root）；`C:\Projects\Agent_Workspace\Fabric` 是 governance/assurance/interop/knowledge contract surface（唯讀契約面，不是第二 root）。
2. **HGK remains governance/control plane after self-hosting**：RP-002 Stage-2 self-hosting 後，HG-KSEOS 仍是唯一 governance / normative control plane（WorkOrder admission、SharedSpine、reducers、acceptance、release）。Fabric 不建立第二 control plane；Hermes/Codex 仍是 bounded capabilities。
3. **Hermes governed binding + role separation**：`config/hermes.json`（`HGK-HERMES-BINDING/2`，`ACTIVE_SELECTED_REINSTALL_BASELINE`）綁定 Hermes v0.20.0 / `v2026.8.3` / `3c27eb62…`。Hermes = runtime/orchestrator；HGK = normative；Hermes runtime state ≠ HGK normative state（§11）。
4. **Normal lifecycle**：goal/source → source admission → Requirement（freeze）→ TaskSpec → WorkOrder → ExecutionBinding → Profile → Hermes → Codex/tests/evidence → independent acceptance（§7）。
5. **Deterministic Direct/Kanban/Swarm selection**：user 正常不選擇 lane；router 依 task shape 決定（`ROUTE_DIRECT_ATOMIC` / `ROUTE_KANBAN_DURABLE` / `ROUTE_KANBAN_CROSS_ROLE` / `ROUTE_SWARM_PARALLEL` / `ROUTE_CODEX_TRACKED`）。Kanban = durable / project-scoped；Swarm = on demand（§8、§20、§31）。
6. **H1 Profile/TEAM/Stack + 5 stable P0 Profiles**：`hgk-orchestrator`、`hgk-coding-factory`、`hgk-engineering-reviewer`、`hgk-qa`、`hgk-security`；`ROLE ≠ PROFILE ≠ WORKER`（§9、§31）。
7. **O1 commander vs officer SoD**：`construction-commander`（dist `e682655a…`）vs `acceptance-officer`（dist `1404bb48…`）身份與 distribution digest 皆 distinct；officer `VERIFY_ONLY`，禁止 candidate write / WorkOrder create / repair / promotion / release（§31）。
8. **B1 project-scoped Kanban + canonical ExecutionBinding**：board `RP002-FABRIC-BOOTSTRAP`；binding `BIND-RP2-S2-001`（schema `RP002-EXECUTION-BINDING/2`）含 workorder、profile、delegation、lease `LS-RP2-S2-001`、budget、idempotency、workspace、candidate write-set、worker PID/heartbeat/log（§31）。
9. **F0 actual Fabric policy consumption**：6-step trace（frozen policy → HGK route/SharedSpine → admission decision → WorkOrder/Binding → Hermes dispatch → evidence）；`yaml_presence_alone: NOT_ACCEPTED`（§31）。
10. **CF1 repaired & externally accepted**：`mcp-contextforge-gateway` v1.0.7 @ commit `4092d336…`、Apache-2.0、註冊 `CF-REG-RP2-S2-001`、OASF `oasf-record/1`；401 auth-negative + authenticated positive discovery；舊 degraded state（`CF1_QUALIFICATION.json` PASS_WITH_DEGRADED_CONTEXTFORGE）僅為歷史（§31）。
11. **F1 same-subject promotion + self-hosted normal path**：`TX-RP2-S2-F1-002-REPAIRED`（`d6ebaa13…`）同 subject 綁定 ContextForge lineage；normal path = `WORKORDER → EXECUTION_BINDING → PROFILE → KANBAN`；legacy bypass = `BREAK_GLASS_ONLY`、open breakglass = 0（§31）。
12. **KG1 namespaces/ACL/provenance/promotion/revoke/provider state**：`hgk.candidate.*` / `hgk.approved.*` / `hgk.revoked.*` / `fabric.*` / `assurance.*` / `sqs.*`（stage2 read-only）/ `shared.approved.*`；agent write = candidate only；promotion = owner/gate only；revoke = tombstone；Qdrant/Neo4j default-off（§23、§31）。
13. **Knowledge Workbench / 知識庫**：`C:\Projects\Agent_Workspace\知識庫` Obsidian = human view（derived）；LLM Wiki / RAG / KG = derived；agent 產出 = candidate，approved 需 gate（§23）。
14. **Fabric relationship + evidence locations**：Fabric = contract surface；證據根 = `C:\Projects\Agent_Workspace\Fabric\stage\RP002-STAGE-HGK\`（seal/handoff/receipts）與 `C:\Projects\Agent_Workspace\Fabric\evidence\review\`（external bundle，`104d4cf2…` mirror equal）（§31）。
15. **Governed self-evolution bounded**：promotion 需 evidence-backed gap + sandbox/eval/holdout + independent verification + Human Policy Owner gate（COV-11-06）；`UNBOUNDED_SELF_MODIFICATION=0`（§9）。
16. **Prompt Compiler C0-C9**：一個 contract 一個 ChangeSet；`PROMPT_COMPILE_PASS ≠ RUNTIME_READY ≠ EXTERNAL_ACCEPTANCE`（§31）。
17. **Ordinary-user no-brain entry**：最少輸入 = `goal` + `source_paths` + `target_root`；其餘自動推導（§5）。
18. **Rollback/checkpoint/resume**：checkpoint 為 normative checkpoint；`project resume <id>` 從 checkpoint 繼續；rollback 依 pointer（§6、§21、§29）。
19. **Current status**：Stage-2 externally accepted；next gate `SQP1`（NOT_AUTHORIZED）；Stage-3 contract `NOT_YET_COMPILED`；**本文件任務未執行 Stage-3**（§2、§31、§32）。
20. **Nonclaims**：production / live / remote 一律 `NOT_CLAIMED`；`sqs_live_trading: NOT_AUTHORIZED`（§32）。
21. **Commands（語法已確認）**：`doctor`、`project start|status|resume|checkpoint|advance|intake|denominator`、`evolution status|signal|candidate`（§4、§6、§30）。
22. **Troubleshooting**：見 §31（readback、checkpoint、finding closure、Fabric evidence paths）。
23. **Changelog**：§33（歷史 lineage 與本版變更）。

---

# Part I — 5 分鐘開始

## 1. HG-KSEOS 是什麼

HG-KSEOS 是受治理的多閘門本機交付系統：把「使用者目標 → 來源 → 需求 → 設計 → 計畫 → WorkOrder → ExecutionBinding → Profile → Hermes/Codex 實作 → 測試 → 修補 → 獨立驗收 → reducers → local delivery」整條鏈路自動化，並以 immutable evidence、independent checker 與 fail-closed 閘門維持可稽核性。RP-002 v2.0 之後，HG-KSEOS 同時是 **Fabric contract surface 的實際消費者**（F0 policy consumption）。

## 2. 目前狀態

- **Current claim**: RP-002 v2.0 **Stage-2 externally accepted**（`Fabric\stage\RP002-STAGE-HGK\EXTERNAL_ACCEPTANCE_RECEIPT_STAGE2.yaml`；external verdict `PASS_CHALLENGE`、meta acceptance `GRANTED`）。claim ceiling = `RP002_STAGE2_LOCAL_ACCEPTANCE_PASS_REPAIRED_CANDIDATE` + external PASS。
- **Next gate**: `SQP1`（NOT_AUTHORIZED）；Stage-3 contract `NOT_YET_COMPILED`；resume token `RESUME:RP002_STAGE3_SQP1_ENTRY`。**本文件任務不執行 SQP1 / Stage-3。**
- **Hermes**: v0.20.0（tag `v2026.8.3`、commit `3c27eb6234bf91b8ceee9e9071591b31e9b148cb`）binding status = fresh-read `config/hermes.json`（current = `ACTIVE_SELECTED_REINSTALL_BASELINE`）；provider `opencode-go`、model `deepseek-v4-flash`。
- **HGK HEAD**: `22e21f0340501caf4ff0dbd67663faf49f521b03`（external review bundle 記錄）。
- **Named methods**: OpenSpec `CERTIFIED_ACTIVE_BROWNFIELD`；gstack `CERTIFIED_ACTIVE_SELECTED_SLICES`（`S2_ROUTER_EVIDENCE.json`）。
- **Production**: `NOT_CLAIMED`（Local Delivery / Stage-2 PASS ≠ Production Authorized）。

## 3. Canonical Root

`C:\Projects\Agent_Workspace\HG-KSEOS` 是唯一 canonical local root（writable root）。Source/Authority、Shared Spine、RBWI/WP、WorkOrder、AGENTS/SKILLS、Harness/Loop、證據與 reducers 皆在此 root。Obsidian vault、LLM Wiki 產出、RAG/KG 皆為 derived/candidate。

`C:\Projects\Agent_Workspace\Fabric` = RP-002 的 governance/assurance/interop/knowledge contract surface（policy、contracts、assurance packs、profiles、stage evidence）；HGK 任務以 consumption trace 消費它（§31 F0），Fabric 不建立第二 control plane。

## 4. 啟動與健康檢查

```text
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\doctor.ps1     # blocking 為空且 verdict=PASS 才是健康
$env:PYTHONPATH='C:\Projects\Agent_Workspace\HG-KSEOS\src'
'.venv\Scripts\python.exe' -m hg_kseos --root 'C:\Projects\Agent_Workspace\HG-KSEOS' doctor   # module form = python -m hg_kseos（已驗證）
```

## 5. 建立新專案（最少輸入；ordinary-user no-brain entry）

```text
$env:PYTHONPATH='C:\Projects\Agent_Workspace\HG-KSEOS\src'
'.venv\Scripts\python.exe' -m hg_kseos --root 'C:\Projects\Agent_Workspace\HG-KSEOS' project start --goal "<目標>" --source <路徑> --target-root <目標目錄>
```

最少輸入：`goal`、`source_paths`、`target_root`。其餘欄位自動推導；user 正常不需要選擇 lane / Agent / Skill / RAG / KG。

## 6. 查看狀態 / Resume / Checkpoint / Stop

```text
$env:PYTHONPATH='C:\Projects\Agent_Workspace\HG-KSEOS\src'
'.venv\Scripts\python.exe' -m hg_kseos --root 'C:\Projects\Agent_Workspace\HG-KSEOS' project status <project_id>
'.venv\Scripts\python.exe' -m hg_kseos --root 'C:\Projects\Agent_Workspace\HG-KSEOS' project resume <project_id>      # 中斷後從 checkpoint 恢復
'.venv\Scripts\python.exe' -m hg_kseos --root 'C:\Projects\Agent_Workspace\HG-KSEOS' project checkpoint <project_id>  # 寫入 normative checkpoint
'.venv\Scripts\python.exe' -m hg_kseos --root 'C:\Projects\Agent_Workspace\HG-KSEOS' evolution status                 # evolution 訊號/候選
```

Stop：完成後由 reducers 收尾；attempt budget 耗盡會 `FAILED + STOP_ESCALATE`（不無限遞迴）。rollback 依 WorkOrder `rollback_pointer` / `SUPERSEDED_ARTIFACTS.yaml` 還原，不做整輪重做。

---

# Part II — 一條龍 Autonomous Project Lifecycle

## 7. 流程（RP-002 v2.0 normal lifecycle）

```text
User goal / source
→ Source Discovery → Source Admission → Intent → Requirements（freeze）→ Design → Plan → TaskSpec
→ WorkOrder（writer=codex）→ ExecutionBinding → Profile 分派
→ Hermes runtime → Codex implementation → tests → repair → independent acceptance（officer VERIFY_ONLY）
→ reducers → local delivery
```

- **external GPT 不是 normal lifecycle dependency**。
- User 不需要手動選 Agent / Skill / RAG / KG / lane。
- normal unnecessary HITL = 0。
- 高風險 / authority / credential 才 HITL（見 §8）。

## 8. Automatic vs HITL + deterministic routing

```text
Task routing / Memory / RAG / KG / Skill selection / WorkOrder planning
repair / tests / independent checker / candidate evolution     AUTO
credential / destructive action / constitutional / production  HITL
```

**Lane 選擇是 deterministic 的，user 正常不選**：HGK router 依任務形狀決定（reason code 記入 WorkOrder / evidence）：

```text
ROUTE_DIRECT_ATOMIC      small atomic task → Direct（bounded execution，不強迫 card）
ROUTE_KANBAN_DURABLE     durable / long persistent objective → Hermes Kanban（project-scoped）
ROUTE_KANBAN_CROSS_ROLE  cross-role / restart-surviving → Hermes Kanban（dependency graph）
ROUTE_SWARM_PARALLEL     independent parallel lane → Swarm（on demand）
ROUTE_CODEX_TRACKED      tracked implementation / narrow repair → Codex
```

Lane ≠ execution method；KANBAN/SWARM/GSTACK/OPENSPEC/CODEX execution surfaces 仍須 raw evidence + independent checker（AGENTS.md default-on）。

## 9. Governed Evolution

```text
observe → gap → FIT-GAP → candidate → sandbox → tests/negative/security/holdout/NRTV
→ independent checker → policy gate → canary / rollback
```

Human 角色 = **Authority / Policy Gate**，不是逐步操作員。COV-11-06：promotion 需要 independent verifier + Human Policy Owner（source-resolved）；不存在「LOW risk 一律自動 promote」。`UNBOUNDED_SELF_MODIFICATION=0`；self-evolution 僅限 evidence-backed gap，且需 sandbox / eval / holdout / independent verification / promotion / canary / rollback 完整循環。

## 10. Self-Repair（兩層，不重複）

- **Hermes tool self-recovery**：terminal retry/truncation readback、write_file on-disk verify、patch already-applied no-op、search near-miss、failure hints、iteration budget。
- **HG-KSEOS product-level self-repair**：failed acceptance、requirement mismatch、security regression、architecture defect → repair WorkOrder → 獨立 recheck。
- Hermes 負責 runtime 摩擦修復；HG-KSEOS 負責產品規範性修復。

---

# Part III — Hermes v0.20 Runtime（governed binding）

## 11. 身份與所有權

- **版本**: `0.20.0` / tag `v2026.8.3` / commit `3c27eb6234bf91b8ceee9e9071591b31e9b148cb`（exact-tag 三者對齊；禁止 floating latest / `hermes update`）。
- **Canonical executable**: `C:\Users\user\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe`（config/hermes.json `HGK-HERMES-BINDING/2`，`ACTIVE_SELECTED_REINSTALL_BASELINE`；`scripts\hermes-core.ps1` PASS）。
- **Canonical HERMES_HOME**: `C:\Users\user\AppData\Local\hermes`（Scheme B 單一 runtime）。
- **Provider/model**: `opencode-go` / `deepseek-v4-flash`（base `https://opencode.ai/zen/go/v1`；憑證 `OPENCODE_GO_API_KEY` env-ref，不寫入 evidence）。
- **Governed binding / role separation**：Hermes = runtime / orchestrator（Kanban、/goal、SessionDB、checkpoint、tool recovery、compression、approvals）；HGK = normative plane；Hermes 不自行 promote、不當 release authority、其 runtime state ≠ HGK normative state。RP-002 Stage-2 實證：`B1_WORKER.log`（PID 10772）+ board `RP002-FABRIC-BOOTSTRAP` task `t_c69537e5`（F0 trace step 5）。

### 11.1 Codex Desktop / Hermes provider lane 隔離

- Human-operated Codex Desktop 只使用 `C:\Users\user\.codex`；該設定是受保護的 first-party OpenAI/ChatGPT lane，不得用編輯 `config.toml` 切換到 OpenCodex。
- Hermes Codex CLI 只使用 `%LOCALAPPDATA%\HG-KSEOS\codex-hermes` 與 `%LOCALAPPDATA%\HG-KSEOS\opencodex-hermes`。由 `scripts\start-hgk-hermes.ps1` 對自己的 process tree 注入 `CODEX_HOME` / `OPENCODEX_HOME`；禁止 `setx` 或其他全域設定。
- 驗證：`powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\start-hgk-hermes.ps1 -Action Verify`。
- 啟動：先以 `-Action StartOpenCodex` 啟動隔離 transport，再以 `-Action Hermes` 啟動 canonical Hermes。缺少 credential、錯誤 home、OpenCodex health failure 都 fail closed，不得 fallback 到 OpenAI。
- Rollback：還原或移除本 ChangeSet 新增的 launcher/binding/doc 段落；只在確認沒有 lane process 使用時移除 receipt 列出的 `%LOCALAPPDATA%\HG-KSEOS\codex-hermes`、`opencodex-hermes` 與固定 runtime 副本。不得刪除整個 `%LOCALAPPDATA%\HG-KSEOS`，且不得觸碰 `C:\Users\user\.codex`。

責任劃分：

```text
HG-KSEOS = governance / normative plane（authority、WorkOrder admission、evidence、checker、reducers、release）
Hermes   = runtime orchestration plane（Kanban、/goal、SessionDB、checkpoint、tool recovery、compression、approvals）
Codex    = bounded coding executor
OpenCodex = transport（ocx start --port 10100 後 codex 路由才可用）
OpenCode Go / DeepSeek = provider / model
Fabric   = governance/assurance/interop/knowledge contract surface（被 HGK 消費）
```

Rollback baseline：v0.18.2（tag `v2026.7.7.2`、commit `9de9c25f…`）保留為 sealed rollback baseline（RECOVERY_ONLY）。

## 12. Kanban 何時用

```text
small atomic task                    → direct/bounded execution（不強迫 card）
long persistent objective            → Hermes /goal
durable / cross-role / restart-surviving → Hermes Kanban（project-scoped）
parallel dependent tasks             → Kanban dependency graph
```

**Hermes runtime state ≠ HGK normative project state**：

```text
HGK WORKORDERS_ADMITTED → Kanban ready
HGK EXECUTING           → Kanban running
HGK BLOCKED_HITL        → Kanban blocked + governance reason
HGK REPAIRING           → repair/retry task
HGK RELEASE_REDUCING    → HGK owns（Kanban 不擁有）
HGK DELIVERED           → HGK owns（Kanban 不擁有）
```

HG-KSEOS WorkOrder → Hermes Kanban 為 thin adapter：Shared Spine 只存 workorder_id / pointer / normative state。RP-002 Stage-2：board `RP002-FABRIC-BOOTSTRAP` 為 project-scoped 實例（B1）。

## 13. `/goal` 何時用

- long-running WorkOrder → 把 WorkOrder contract 投影成 goal completion contract（outcome / verification / constraints / boundaries / stop_when）。
- **`/goal done` ≠ HG-KSEOS PASS**：goal judge 只是 runtime stop helper；final acceptance 仍須 raw evidence → independent checker → reducers → release。

## 14. Runtime checkpoint vs Normative checkpoint

- **Hermes 保存**: session、goal、worker、Kanban runtime、runtime checkpoint。
- **HG-KSEOS 保存**: project normative state、authority refs、WorkOrder IDs、session/Kanban refs、source/evidence hashes、release state、rollback pointer。
- 兩者不是鏡像；Shared Spine 只存 pointer/ref。

## 15. Tool recovery / Compression / Approvals

- Tool self-recovery 由 Hermes v0.20 提供（reuse binding matrix：duplicates=0，HG-KSEOS 無重複 wrapper）。
- Context compression 使用 Hermes v0.20（enabled；HG-KSEOS Memory/RAG/SourceUnit 不因 compression 刪除）。
- Approvals：`approvals.mode: manual`（fail-closed；不得以 `off` 作正常 profile）；`rm -rf` 等危險 pattern 觸發 `pending_approval`；Windows-native path guard 由 HGK security 層保留。

## 16. Skills 治理邊界

- Hermes 負責 skill file 機制 / loading / invocation / curator（archive-only，永不 promote）。
- HG-KSEOS 負責 candidate admission、FIT-GAP、sandbox、negative/security、holdout、NRTV、independent checker、promotion policy、COV-11-06 Human Policy Owner gate、rollback acceptance。

---

# Part IV — Named Methods（OpenSpec / gstack）

## 17. OpenSpec（brownfield spec projection）

- **身份**: `@fission-ai/openspec@1.8.0`（tag `v1.8.0`、release commit `d57889664…`、MIT、Node >=20.19）— `CERTIFIED_ACTIVE_BROWNFIELD`（`S2_ROUTER_EVIDENCE.json`）。
- **角色**: `BROWNFIELD_ENGINEERING_DEFINITION_ADAPTER`。不是 Root SSOT、不是 release authority、不是 primary writer（Codex CLI 仍為 bounded writer）。
- 使用上游官方 Hermes skills-only 整合（`.hermes/skills/openspec-*/SKILL.md`，`skills.external_dirs` 載入）。
- **流程**: brownfield 需求 → deterministic route → OpenSpec explore/propose → spec delta → HGK Requirement/ADR/WorkOrder mapping → Hermes/Codex 實作 → tests → OpenSpec validate/archive → HGK final acceptance。

## 18. Spec Kit XOR

- `brownfield → OpenSpec active`；`greenfield → Spec Kit/native profile`。禁止雙 spec owner。
- tool unavailable → 顯式 `DEGRADED` / native fallback；禁止 silent imitation。

## 19. gstack（selected advisory slices）

- **身份**: `garrytan/gstack@1.61.0.0`（commit `94993f74012782fd94416dd44b8314f6363a13a4`、MIT、bun）— `CERTIFIED_ACTIVE_SELECTED_SLICES`。
- **Selected slices（advisory only）**: `office-hours`、`plan-eng-review`、`review`、`qa`、`cso`、`ship`（`final_authority=false`）、`retro`。
- 生成：`bun run gen:skill-docs --host hermes`（54 skills，flat `gstack-*`）；`setup --host hermes` exit 0 ≠ certified（需 effective-load + real invocation）。
- 已知 pinned host-generation gap（已記錄 + thin adapter）：`gstack-review` 需要 `.hermes/skills/review/*`，generator 未生成 → adapter 把 repo `review/` 拷入 project `.hermes/skills/review/`。
- **邊界**: gstack ship ≠ ReleaseReducer；gstack review ≠ independent checker；gstack cso ≠ HGK security authority；gstack office-hours ≠ product authority。輸出 = EvidenceCandidate / advisory。

## 20. Named-Method Router（deterministic）

```text
brownfield/migration → openspec
greenfield           → XOR_GREENFIELD / native
plan                 → gstack.plan-eng-review（selected）
implementation done  → gstack.review
QA required          → gstack.qa
security-sensitive   → gstack.cso
release readiness    → gstack.ship（advisory only）
high-impact ambiguity→ gstack.office-hours
retro                → gstack.retro
其餘                 → native
```

- 決定來自 registry lookup + router（`S2_ROUTER_EVIDENCE.json`），**不是 LLM 猜測**。
- **fake invocation = prohibited**；**silent fallback = prohibited**（unavailable → 顯式 DEGRADED + certified native fallback，EvidenceEnvelope 記錄）。

## 21. Fallback / Rollback（真實存在的程序）

- Hermes v0.20 rollback baseline：v0.18.2（還原 config executable + hermes-core.ps1 驗證）。
- OpenSpec disable → native PRW fallback（移除 external_dirs 綁定 + fixture skill projection；canonical Requirement/ADR/WorkOrder 不刪）。
- gstack disable → native review/QA/security/release advisory。
- Provider failure → route DEGRADED + native fallback。
- Checkpoint/resume、package rollback：見 §Part VI 與 scripts（backup/restore-drill）。
- RP-002 rollback pointer：`Fabric\stage\RP002-STAGE-HGK\SUPERSEDED_ARTIFACTS.yaml`（被取代工件 preserved unchanged）。

---

# Part V — Governance & Knowledge

## 22. 權威與治理

- 權威順序依 source-freeze 工件；低權威來源不得覆寫高權威規則。Fabric contracts（`Fabric\control\*`）經 consumption trace 被消費（F0）。
- Canonical database: `var/shared-spine/hg-kseos.db`（單一 writer 契約）。
- 同 rank 衝突 → Conflict/TT，不靜默合併。

## 23. Knowledge Workbench（Obsidian + LLM Wiki + RAG/KG；KG1 governed）

- **Canonical source** = Git Markdown / Source Ledger / Shared Spine / Fabric contracts（frozen）。canonical ≠ RAG/KG/wiki。
- **Obsidian / 知識庫** = human workbench（`C:\Projects\Agent_Workspace\知識庫`，derived human view）；**LLM Wiki** = derived compiler（`atomicstrata/llm-wiki-compiler` v1.1.0，npm pin，isolated prefix `var/workbench/llm-wiki`）；**RAG/KG** = retrieval/reasoning surfaces（SQLite/FTS5 local-first）。
- **KG1 namespace model**（`Fabric\stage\RP002-STAGE-HGK\KG1\KG1_NAMESPACE_MODEL.json`）：`hgk.candidate.*`（agent write）、`hgk.approved.*`（promotion-gate write）、`hgk.revoked.*`（revocation-gate write + tombstone）、`fabric.*`、`assurance.*`、`sqs.*`（stage2 read-only）、`shared.approved.*`。
- **KG1 規則**：agent_write = candidate only；promotion = owner/gate only（agent 禁止 self-promote）；forget = tombstone + audit receipt；revoked/stale excluded；cross-stack export = explicit promotion（`KG1\ACCEPTANCE_RECEIPT_KG1.yaml` runtime evidence：K-001 candidate→approved→revoked + tombstone）。
- **KG1 provider state**（`KG1_PROVIDER_LEDGER.json`）：SQLite/FTS5 P0 REUSE（active）、HGK Memory P0 REUSE（candidate ≠ truth）、Qdrant/Neo4j default-off（not-installed）、pgvector conditional、Cognee P1 shadow。
- AI 編譯路徑（`llmwiki compile/refresh/query`）需要 ANTHROPIC credential → `EXTERNAL_CREDENTIAL_GATED`。
- GraphRAG / vector backend = `DEFERRED_SOURCE_BACKED`（本輪不啟用）。
- 編輯流向：filesystem/Git diff → candidate → 驗證/admission → rebuild；不得直接成為 authority。

## 24. 安全邊界

禁止：寫入來源、越出 WorkOrder admitted write-set / target-root / isolated worktree boundary、路徑穿越、reparse point、未授權網路、秘密讀取、遠端發佈、部署、production mutation。所有高風險擴權維持 HITL。證據不得保存 token/key 值。ContextForge secret policy = env-var `REFERENCE_ONLY`（`__REPLACE_ME__` fail-closed）。

---

# Part VI — Evidence / Acceptance / Release

## 25. 如何判斷 current candidate 是否可交付

依序檢查：

```text
fresh test denominator（current task/head 綁定；schema HGK-CURRENT-TEST-DENOMINATOR/2）
CoverageReducer v2 decision
UserExperienceReducer v1 decision
TST-092 independent receipt（current Task 命名 + same HEAD/package）
External Acceptance（unique hard-check IDs 全 PASS、duplicates=0）
Final Evidence（single current identity；status/counts 與 acceptance machine 一致）
blocking TT = 0
```

**ad-hoc verification ≠ canonical suite green**：前者是針對變更行為的聚焦檢查，後者是 fresh discovery 的完整套件結果。

## 26. Hard-Check denominator 語意

External Acceptance 的 hard-check denominator 按 **unique predicate ID** 計數；duplicate ID 本身是 fail-closed defect（`hard_check_row_total == hard_check_unique_id_total` 且 `duplicate_hard_check_id_count == 0`）。數量本身不是品質；不保證任何固定數字。

## 27. Evidence lineage

- Task-011/012/013/014/015 = historical accepted lineage（不可覆寫；TST-092 historical receipts immutable）。
- current closure = current candidate only（RP-002 Stage-2 externally accepted 為 current）。
- 舊 HEAD/package 保留在 Changelog / Historical Baselines，不得在普通使用章節稱 current。

## 28. Package / Release

- `scripts\package.ps1`（或 `tools/package_local.py`）產生 deterministic local ZIP + exact-set readback + manifest。
- TST-092 以獨立 checker 在 same-HEAD/same-package 上 INDEPENDENT_CASE_PASS。
- blocking TT、過期/scope-mismatch evidence、exact-set mismatch → FAIL/TEMP_CLOSED。LLM judge 不能覆寫 deterministic oracle。

## 29. 備份 / 還原

`scripts\backup.ps1`（不可覆寫 SQLite backup + SHA-256 manifest，`var/backups/`）；`scripts\restore-drill.ps1`（寫入 `worktrees/restore-drill/`，驗證 hash/integrity/schema/counts/RTO）。TT ledger：更新 `source-freeze/TT_LEDGER.csv` 後 `scripts\reconcile-tt.ps1`。

---

## 28a. Canonical acceptance resolver 與 ordering oracle（current）

**28a.1 Acceptance transition（唯一入口）**
- `SharedSpine.resolve_acceptance(...)` ＋ `TRANSITIONS['acceptance']` 是 acceptance 的唯一 canonical transition 入口；由 SharedSpine / domain owner 執行。
- 保證：canonical event / audit trace 保留；subject / evidence binding fail-closed；stale / conflicting 拒絕；identical replay idempotent；transaction atomic。
- **consumer 不得以直接 SQL bypass domain API**；spine 自身的 repository / transaction 實作可依既有架構使用內部 persistence SQL。
- 複核入口：`tests/test_acceptance_resolution.py`。

**28a.2 Ordering oracle**
- 排序一律用隱式 `rowid`（單調插入序），**不得用 wall-clock `created_at`**（秒級精度，同秒即任意）。
- 已修正四處：checkpoint 的 current-workorder 選擇（＝ admission 序）、近期 transitions、memory 記錄、qualified 形式。
- 複核入口：`tests/test_ordering_oracle.py`。

# Part VII — RP-002 v2.0 現況、Diagnostics & Troubleshooting

## 30. Diagnostics（實際存在、語法已確認命令）

```text
$env:PYTHONPATH='C:\Projects\Agent_Workspace\HG-KSEOS\src'
'.venv\Scripts\python.exe' -m hg_kseos --root 'C:\Projects\Agent_Workspace\HG-KSEOS' doctor
'.venv\Scripts\python.exe' -m hg_kseos --root 'C:\Projects\Agent_Workspace\HG-KSEOS' project start|status <id>|resume <id>|checkpoint <id>|advance <id>|intake <id>|denominator <id>
'.venv\Scripts\python.exe' -m hg_kseos --root 'C:\Projects\Agent_Workspace\HG-KSEOS' evolution status|signal --project-id <id>|candidate --project-id <id>
powershell -File .\scripts\doctor.ps1 | hermes-core.ps1 | sbom.ps1 | test.ps1 | package.ps1 | backup.ps1 | restore-drill.ps1
hermes doctor / hermes --version            # canonical v0.20 executable
openspec doctor                             # 於 OpenSpec fixture root
bun run gen:skill-docs --host hermes        # gstack 重新生成 Hermes skills
ocx status / ocx start --port 10100         # OpenCodex transport
powershell -File .\scripts\start-hgk-hermes.ps1 -Action Verify   # lane 隔離驗證
```

## 31. RP-002 v2.0 現況 / 知識狀態 / Fabric 關係 / Troubleshooting

### 31a. RP-002 v2.0 Stage-2（current）

- Stage-2 seal（repaired）：`Fabric\stage\RP002-STAGE-HGK\STAGE-2-SEAL-REPAIRED.yaml`（`12da14ac…`）；gates K1/D1/C1/H1/O1/B1/F0/CF1/F1/KG1 全 PASS。
- External acceptance：`EXTERNAL_ACCEPTANCE_RECEIPT_STAGE2.yaml`（`EXT-ACC-RP2-S2-20260813`，`PASS_CHALLENGE` / `GRANTED`）。
- Handoff：`STAGE2_TO_STAGE3_HANDOFF_REPAIRED.yaml`（`93a7da26…`；stage_from RP002-STAGE-HGK → stage_to RP002-STAGE-SQS；`STOP_FOR_EXTERNAL_GPT_REVIEW_BEFORE_STAGE3` 已解除為 VALID_FOR_NEXT_STAGE_ENTRY）。
- Resume checkpoint：`RESUME_CHECKPOINT_STAGE3_ENTRY.yaml`（current_gate SQP1 NOT_AUTHORIZED；stage3_contract NOT_YET_COMPILED；next_allowed_action COMPILE_STAGE3_CONTRACT_ONLY；resume token `RESUME:RP002_STAGE3_SQP1_ENTRY`）。
- Finding closure：`S2R_FINDING_CLOSURE.yaml`（S2-EXT-001/002/003 CLOSED_LOCAL；blocking_tt_cr=0；open_breakglass=0；unauthorized_side_effects=0；live_broker_writes=0）。
- Superseded：`SUPERSEDED_ARTIFACTS.yaml`（prior CF1 receipt、prior F1 tx `149a137e…`、prior seal `14726894…`、prior handoff、prior review bundle — preserved unchanged）。

### 31b. H1 / O1 / B1 / F0 / CF1 / F1 / KG1 重點（evidence-backed）

- **H1**：5 persistent P0 profiles（hgk-orchestrator / hgk-coding-factory / hgk-engineering-reviewer / hgk-qa / hgk-security）；`ROLE ≠ PROFILE ≠ WORKER`；TEAM/Stack artifacts（`HGK\TEAM.md`、`HGK_STACK_MANIFEST.yaml`、gstack snapshot 19 roles 0 missing）。
- **O1**：commander（`e682655a…`）vs officer（`1404bb48…`）identity + digest distinct；officer VERIFY_ONLY；SOD `Fabric\control\SOD_POLICY.yaml`；acceptance packs 8/8；`default_l2_checker_after_o1: acceptance-officer`。
- **B1**：board `RP002-FABRIC-BOOTSTRAP`、task `t_c69537e5`、binding `BIND-RP2-S2-001`（RP002-EXECUTION-BINDING/2 canonical）；worker PID 10772；`B1_WORKER.log`；lease `LS-RP2-S2-001`；idempotency `RP2-S2-B1-RUN-001`；workspace `Fabric\stage\RP002-STAGE-HGK\B1`；`worker_exit_zero_is_pass: false`。
- **F0**：6-step policy consumption trace；consumed = CHANGE_CLASS_ROUTER / SOD / ACCEPTANCE / KNOWLEDGE policy；`yaml_presence_alone: NOT_ACCEPTED`。
- **CF1**：mcp-contextforge-gateway 1.0.7 @ `4092d336…`、Apache-2.0、`CF-REG-RP2-S2-001`；runtime health 200、openapi/admin 401；auth-negative + authenticated positive discovery；OASF `oasf-record/1`（`OASF-REC-RP2-S2-001`）；**舊 degraded state 是 history only**。
- **F1**：`TX-RP2-S2-F1-002-REPAIRED`（`d6ebaa13…`）同 subject promotion；normal path `WORKORDER→EXECUTION_BINDING→PROFILE→KANBAN`（canary 4 proven instances）；legacy bypass = BREAK_GLASS_ONLY。
- **KG1**：knowledge governance ACTIVE；namespaces/ACL/provenance/promotion/revoke/provider state（§23）。

### 31c. Fabric relationship + evidence locations

- Fabric = contract surface；HGK 消費方式見 §31b F0 trace；consumer 實作 = `Fabric\fabric\consumers\hgk_policy_consumer.py`。
- **Evidence 根**：`C:\Projects\Agent_Workspace\Fabric\stage\RP002-STAGE-HGK\`（seal/handoff/receipts）與 `C:\Projects\Agent_Workspace\Fabric\evidence\review\`（external bundle `RP002_STAGE-2_KG1_EVIDENCE_FOR_EXTERNAL_REVIEW.md` sha `104d4cf2…`，Fabric/HGK mirror byte-identical；`RP002_STAGE-2_EXTERNAL_BUNDLE_HASHES.json`）。
- Master/stage 對照：`Fabric\rp002\RP002_STAGE_CROSSWALK.yaml`；gate 詞彙：`Fabric\rp002\RP002_GATE_CATALOG.yaml`（`KBN1`/`FG1` 為歷史名，不執行）。

### 31d. Troubleshooting（readback 導向）

- **status 顯示 NOT_AUTHORIZED / SQP1** → 讀 `Fabric\stage\RP002-STAGE-HGK\RESUME_CHECKPOINT_STAGE3_ENTRY.yaml`；不得自行執行 Stage-3。
- **hash 對不上** → 以 `Fabric\evidence\review\RP002_STAGE-2_EXTERNAL_BUNDLE_HASHES.json` + 各 receipt 的 raw refs 重讀；以檔案為準。
- **finding open / 修復疑慮** → 讀 `S2R_FINDING_CLOSURE.yaml` 的 evidence refs 與 `SUPERSEDED_ARTIFACTS.yaml` 的 disposition。
- **policy 是否被消費** → 檢查 consumption trace（F0 模板）；檔案存在 ≠ 被消費。
- **worker 失聯** → claim TTL + heartbeat 檢查；過期無 heartbeat → 可重新指派；沒有 ghost worker。
- **中斷恢復** → `project resume <project_id>`（§6）；checkpoint 為 normative checkpoint。

## 32. Production Boundary

**Local Delivery PASS ≠ Production Authorized**。目前 `PRODUCTION = NOT_CLAIMED`：本文件與所有 evidence 只代表 local delivery / Stage-2 狀態；未宣稱 remote CI / deploy / production 完成。`sqs_live_trading: NOT_AUTHORIZED`、`remote_deployment: NOT_CLAIMED`、`production_autonomy: NOT_CLAIMED`（external receipt non_claims）。

## 33. Changelog / Historical Baselines

**engineering-base delta（current）**：兩項受治理 ChangeSet 已實作、測試並經獨立驗收——
- `HGK-EBC-ACCEPTANCE-RESOLUTION-001`：canonical acceptance resolver（`resolve_acceptance` ＋ `TRANSITIONS['acceptance']`；consumer 禁直接 SQL；fail-closed / idempotent / atomic）。
- `HGK-EBC-ORDERING-ORACLE-001`：排序 oracle 由 wall-clock 改為隱式 `rowid`（4 站點）；guard `tests/test_ordering_oracle.py`。
兩者皆附 rollback 路徑與獨立 checker 結果；**不宣稱 production / release，也不構成第二個 control plane**。



**v2026.08.13-r1（本版）**：RP-002 v2.0 更新總覽（Part 0）；current claim 更新為 Stage-2 externally accepted；next gate SQP1 NOT_AUTHORIZED；Fabric relationship + evidence locations（§31c）；troubleshooting（§31d）；命令語法確認（§30）。

**Historical lineage（stale companion / bootstrap-only 語意，僅歷史參考，非 current）**：

- 早期施工歷史（companion / maker root / task-007..010 / Task-011 / Task-012 / Task-013 old seal / Task-014 old seal / Task-015）一律屬歷史，已由後續 sealed changeset 取代；TST-092 historical receipts（E08..E12、TASK013、HANDOFF、FINAL 等）immutable。各歷史 seal 的 HEAD/package 見對應 evidence/wave-* 工件。
- **2026-08-11 RP-001 milestone**：`HGK-REFERENCE-PROJECT-001` 已 **MILESTONE_CLOSED**（WAVE1-WAVE5 + EVO-003/004/005：15/15 WO、211/211 SQS tests、274/274 HGK suite、161/161 acceptance、EVO-005F frozen graph）。此後 SQS 任務走 normal operational loop（`execute → test → repair → continue`）。
- **2026-08-12 A-3 operability delta**：`WO-HGK-A3-001`（v2026.08.12-r2）README / User Guide / Skill steering hardening；claim ceiling = `HGK_SQS_A3_OPERABILITY_STEERING_READY`（never production / live / remote）。
- **Hermes reinstall handoff（historical）**：`C:\Projects\Agent_Workspace\Fabric\evidence\review\RP002_PRE_HERMES_REINSTALL_HANDOFF.md` / `RP002_POST_HERMES_REINSTALL_HANDOFF.md` 屬 pre/post reinstall 歷史；current binding 以 `config/hermes.json` fresh-read 為準。
- **RP-002 早期狀態**：`Fabric\rp002\CHECKPOINT.json`（CP-003，D1→C1）為 Stage-2 早期 checkpoint，屬歷史；current 以 Stage-2 seal / external receipt 為準。Knowledge K1/KG1 已於 Stage-2 完成治理（§23/§31b），不再 DEFERRED。
