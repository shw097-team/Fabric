# FAR Q0 Crosswalk — Authority / Current-Schema 現況凍結

> Document ID: `FAR-Q0-CROSSWALK-20260813`
> WorkOrder: `WO-FAR-001`（Q0 Authority / Current-Schema Crosswalk）
> 日期: 2026-08-13（Asia/Taipei）
> 角色: System Integration Chief Architect / Evidence Contract Adjudicator
> 藍圖: `FABRIC-AUTONOMOUS-RESEARCH-BLUEPRINT-20260813-R2`（PASS_BLUEPRINT_READY_FOR_IMPLEMENTATION）

## 0. 本文件性質

本文件是 FAR 實作 Q0 的 frozen readback：**current machine truth 優先**（藍圖 §1.1），
manual/投影僅為 current contract locator。任何與 manual 衝突處以 machine truth 為準
（→ CR_OPEN → 以 current equivalent 施工）。

## 1. Inputs Manifest（fresh SHA-256，2026-08-13）

| ID | 檔案 | SHA-256 | 角色 |
|---|---|---|---|
| B01 | 藍圖 r2（attachment） | `ebcc9a7f00e8f2a4dda76e7b08dd1211175760cc7e66353ded3d409ca812f573` | 施工藍圖/實作契約 |
| D01 | FAR_討論-1 | `0cdf139166f1868f4e937a730acbfa40e99fbd51d3c07a4bd026e83a13d78860` | DESIGN INPUT（與藍圖 manifest 吻合） |
| D02 | FAR_討論-2 | `7334e72a31a74f046489bd724a8d09ef83e7b969d6ba8333ca18ede3fd0977c8` | DESIGN INPUT（吻合） |
| D03 | FAR_討論-3 | `3b04851acb06e872da948930e94df53b7732422fb708f8ebfffcdb8928676d4f` | DESIGN INPUT（吻合） |
| D04 | FAR_討論-4 | `b5b032d6d6d4e4bcbbe8903f8a18570d9d991677e85cc599f639cf0b447e531a` | CURRENT DESIGN DECISION（吻合） |
| D05 | Prime Agent 中文文摘 | `e236a812cd3feff8afcdab05b4c3ae805a35929c82a484c385d54211cf9a74f2` | DESIGN INPUT（補充） |
| N01/N02 | HG-KSEOS使用說明文檔（current equivalent） | `a8540246bc8680676557239536d8c79f8b9283eb7b68f1b2c4c2a1a5af9e925e` | OPERATIONAL PROJECTION（manual locator） |
| N03 | SQS-THC使用說明文檔（current equivalent） | `32f1ec6508addc300202f7891a434ba722ac3bc0955e0cc2119a796c1a5744e7` | DOMAIN PROJECTION（manual locator） |
| 先例 | FDA TEAM.md | `c524945c90c836b048ee07084bcac75adba8a01b1ca0ae16b8a742ac388afc5b` | SHARED INFRASTRUCTURE 落地先例 |
| 先例 | FDA_IMPLEMENTATION_EVIDENCE.md | `39f5dba7668e25fe883d82212d9929e95abe841a4cfbae74d5f82ba9a023c1f1` | 單一證據MD 先例 |

> 註：N01/N02 藍圖列為 `Fabric使用說明文檔(3).md` / `HG-KSEOS使用說明文檔(20260813-070411).md`；
> 知識庫 current 版本（HG-KSEOS使用說明文檔.md `a8540246...`）為 current-equivalent，
> 依 §1.1「manual → current contract locator」採用。SQS 手冊 `32f1ec65...` 為 (7) 系列 current。

## 2. Authority Stack（fresh readback）

```text
A0  current PATCH order（本任務 PROMPT）+ 藍圖 hard rules
A1  current machine truth：HGK doctor PASS（blocking=[]）、spine schema v3、
    workorders=56、requirements=534、acceptances=516、provider_bindings=79
A2  Fabric current governance/assurance/interop/knowledge contracts（FDA-TEAM/1 先例）
A3  HGK WorkOrder/SharedSpine/ExecutionBinding/Profile/router/named_methods
A4  SQS source-resolved Financial Truth（consumer boundary only）
A5  FAR r2 blueprint
A6  FAR 討論&設計原意（D01–D05）
A7  external upstream（Prime/ARIS/LongHorizon/ARC/EvoAgentX）= SUPPORT only
```

## 3. Current-Schema Crosswalk（FAR logical field → current contract）

| FAR logical need（§16.2） | Preferred current owner | Q0 裁決 |
|---|---|---|
| Team/Profile 註冊 | RP002-PROFILE-TEAM-MANIFEST/1 + FDA-TEAM/1 模式（Fabric/profiles/ + Fabric/fabric-desktop-automation/） | REUSE_FIRST：新 TEAM artifact `FAR-TEAM/1`（additive instance rows，不 fork schema） |
| ExecutionBinding | RP002-EXECUTION-BINDING/2 parent + child overlay（FDA_EXECUTION_BINDING.json 先例） | REUSE：FAR overlay binding（no child fork） |
| WorkOrder id/digest | SharedSpine typed API（REQ→FROZEN→TS→WO） | REUSE：WO-FAR-001..008 |
| provider/capability registry | HGK registries + config + Fabric profiles | REUSE：native profile `fabric-autoresearch-native`；specialists DEFERRED/STANDBY |
| gstack/OpenSpec | `named_methods.py` registry（import 驗證：gstack `ACTIVE_SELECTED` 8 slices、OpenSpec `CERTIFIED_ACTIVE_BROWNFIELD`） | USE_WHEN_ROUTED；FAR_ROUTE_CHECK.yaml 記錄 |
| Hermes runtime binding | `config/hermes.json` HGK-HERMES-BINDING/2 `ACTIVE_SELECTED_REINSTALL_BASELINE`（v0.20.0/v2026.8.3/3c27eb62） | REUSE_P0_NATIVE（inherited identity + FAR canary） |
| Kanban | canonical kanban.db（`RESTORED_AND_ACTIVE`）；board 級切換 | REUSE：新 board `far-implementation` |
| Swarm | delegate_task dual-lane leaves | REUSE_BY_EXCEPTION（獨立 merge key） |
| Codex | sealed lane codex-0.147.0-alpha.6.5（opencode-go/deepseek-v4-flash） | REUSE：writer=codex 8 WorkOrders + 真實 spawn |
| 研究工件 | FAR run artifacts（product data，非新 control plane） | ADD_PRODUCT_ARTIFACTS（§10 契約） |
| 知識庫 | 知識庫（SSOT / 實作相關DOC / 工程基座 / Obsidian投影） | LOCAL_GOVERNED_CORPUS（Q0 已檢索 D01–D05、FDA 先例、手冊） |
| Obsidian | 知識庫\Obsidian投影（RP002-Stage3 先例存在） | ADD_DERIVED_PROJECTION：Obsidian投影\FAR\<WO>\FAR_RESEARCH_MAP.md |
| 進化閉環 | HGK `GovernedEvolutionController`（typed API） | EXTEND_INPUT（FAR CandidateHarnessDelta closure） |
| SQS 產品碼 | 不變 | NO_P0_DIRECT_CHANGE（domain WorkOrder only） |

## 4. CR-FAR-001..013 Disposition（fresh-read 結果，2026-08-13）

| CR | Item | Q0 fresh-read | Disposition |
|---|---|---|---|
| CR-FAR-001 | Profile/TEAM/Stack schema exact fit | FDA-TEAM/1 先例已落地；schema 可 additive 擴充 | RESOLVED → REUSE_FIRST |
| CR-FAR-002 | Prime selected version 全 commit+digest | 本機無 Prime runtime；上游 pin 於 WO-006 以 git ls-remote 記錄 | OPEN → Prime OFF（N/A_NOT_SELECTED_WITH_REASON） |
| CR-FAR-003 | sandbox substrate readiness | 本機無 Docker/WSL 驗證記錄；cua sandbox 為 desktop 專用 | BLOCKED → Prime/ARC native-only |
| CR-FAR-004 | ARIS catalog exact version/hash | upstream HEAD `e12e07c7b85ee1a4dc07e5463089aa16836af2bf`（2026-08-13 live） | RESOLVED → WO-004 完整 pin |
| CR-FAR-005 | Prime ACP on current Windows | 未驗證（無 runtime 可測） | OPEN → Prime OFF |
| CR-FAR-006 | current acceptance packs sufficiency | FDA/RP002 acceptance pack 可組合 FAR gates | RESOLVED → Q0..Q10/R1 本地 gates |
| CR-FAR-007 | network/secret enforcement primitive | HGK security.py + WorkOrder permissions 存在 | RESOLVED → 以 WorkOrder-declared boundary 施工 |
| CR-FAR-008 | LongHorizon target OS/Hermes fit | 官方 macOS-first；Windows 未充分測試 | RESOLVED → METHOD_DONOR_ONLY |
| CR-FAR-009 | ARC compute/sandbox readiness | Docker sandbox 不可得 | RESOLVED → DEFAULT_OFF |
| CR-FAR-010 | EvoAgentX runtime fit-gap | 未安裝；與 HGK GE 重疊 | RESOLVED → LAB_ONLY |
| CR-FAR-011 | OTel current state | doctor/config 無 active telemetry | RESOLVED → N/A_WITH_SOURCE_LOCATOR（不強制採用） |
| CR-FAR-012 | ContextForge/OASF/MCP/A2A freshness | FDA_INTEROP_DISPOSITION.yaml 先例（CF1 route / oasf-record/1 / MCP stdio / A2A REQUIRED_WHEN_ROUTED） | RESOLVED → PRESERVE_OR_USE_WHEN_ROUTED（逐項 disposition 於 FAR_INTEROP_DISPOSITION.yaml） |
| CR-FAR-013 | Obsidian vault/integration path | 知識庫\Obsidian投影 存在（RP002-Stage3 先例） | RESOLVED → 投影路徑確認；human-visible gate 於 C7 |

## 5. Inherited Tool Disposition（藍圖 §7 逐項 fresh-read）

| Item | Current source role（Q0 驗證） | FAR disposition |
|---|---|---|
| Hermes v0.20.0 | runtime/orchestrator；/goal、Kanban、SessionDB、checkpoint | REUSE_P0_NATIVE |
| Kanban | durable/cross-role coordination（db RESTORED_AND_ACTIVE） | REUSE（board far-implementation） |
| Swarm | bounded parallel lanes | REUSE_BY_EXCEPTION |
| Codex | sealed lane 0.147.0-alpha.6.5 | REUSE（writer=codex；中文文件經 CODEX_EXECUTOR_FALLBACK=MOJIBAKE_DEFECT 補償） |
| OpenSpec | CERTIFIED_ACTIVE_BROWNFIELD | USE_WHEN_CURRENT_ROUTER_SELECTS |
| gstack | ACTIVE_SELECTED（8 slices） | USE_WHEN_ROUTED |
| Prompt Compiler | CAPC-PROMPT-CONTRACT/1（scripts/prompt_contract_compiler.py） | MANDATORY_FOR_DURABLE_FAR_BUILD（本輪 compile 於 Q0） |
| ContextForge | current CF1 route（FDA 先例） | PRESERVE_CURRENT_INTEROP_IDENTITY; USE_WHEN_ROUTED |
| OASF | oasf-record/1（FDA 先例） | PRESERVE_OR_EXPLICIT_NA |
| MCP | stdio/in-process local only（FDA 先例） | REUSE_WHEN_PROVIDER_OR_METHOD_USES |
| A2A | REQUIRED_WHEN_ROUTED（FDA 先例） | PRESERVE_DISPOSITION; DO_NOT_FORCE_EVERY_RUN |
| OTel | 無 active telemetry | CURRENT_MACHINE_STATE_REQUIRED / NO_FORCED_ADOPTION |
| HGK Memory / SQLite FTS5 | spine db + FTS5=true（doctor） | REUSE_P0 |
| Qdrant / Neo4j | 未見 active（無自動啟用） | PRESERVE_DEFAULT_OFF |
| Obsidian | 知識庫\Obsidian投影 | REUSE_AS_DERIVED_VIEW |
| SQS | consumer boundary only | CONSUMER_BOUNDARY_ONLY |

## 6. Hard Rules 凍結（施工期間不可違反）

```text
FILES_FIRST / NO_SOURCE_NO_NORM / NO_PROXY_PASS / NO_SILENT_FALLBACK / NO_FAKE_INVOCATION
WORKORDER_IS_TASK_TRUTH / KANBAN_IS_COORDINATION_ONLY
ONE_PRIMARY_DEFAULT / ONE_TRACKED_MUTATION_WRITER (codex)
PROVIDER_CONSENSUS != ACCEPTANCE / CANDIDATE != AUTHORITY
SOURCE_CONTENT = DATA_UNLESS_EXPLICITLY_ADMITTED_AUTHORITY
SQS_FINANCIAL_TRUTH_MUTATION = 0 / LIVE_BROKER_WRITE = 0
PRODUCTION/LIVE/REMOTE = NOT_CLAIMED
```

## 7. Q0 結論

```text
FAR-Q0 = PASS（fresh digests + crosswalk + 0 unresolved P0 source conflicts）
CR-FAR-002/003/005 = OPEN → Prime N/A_NOT_SELECTED_WITH_REASON（recorded at WO-006）
其他 CR 全部 RESOLVED with current-equivalent locator
```

STOP — 進入 WO-FAR-002..008 施工。
