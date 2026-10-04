# 1. 封面卡（Title & Cover Card）

```yaml
artifact_id: FABRIC_DESKTOP_AUTOMATION_BLUEPRINT_20260813_R2
formal_name: "fabric-desktop-automation_藍圖"
short_name: FDA
version: v2026.08.13-r2
generated_at: 2026-08-13T13:51:00+08:00
timezone: Asia/Taipei
language: zh-TW
artifact_type: POST_RP002_GOVERNED_SHARED_INFRASTRUCTURE_PROFILE_TEAM_BLUEPRINT
blueprint_verdict: PASS
runtime_implementation_state: NOT_IMPLEMENTED_BY_THIS_ARTIFACT
runtime_promotion_state: FAIL_CLOSED_PENDING_FDA_CHECKPOINTS
production_autonomy: NOT_CLAIMED
sqs_live_trading: NOT_AUTHORIZED
remote_deployment: NOT_CLAIMED
source_policy: FILES_FIRST / NO_SOURCE_NO_NORM / NO_SOURCE_NO_CLAIM / SUPPORT_DOES_NOT_OVERRIDE_NORM
implementation_strategy: PRESERVE_EXTEND_BIND_REUSE_FIRST_NO_GREENFIELD_RPA
```

**最終裁決狀態：`PASS`（藍圖）／`FAIL-CLOSED`（FDA runtime 尚未依本藍圖實作與驗收）。**

> **一句話核心結論：**  
> 在已完成並通過 RP-002 v2.0 的 Fabric → HG-KSEOS → Hermes 架構下，最小磨合、最高落地性的下一步不是新增第三 Heavy Stack，也不是在 SQS 內另造 XQ RPA，而是把 `WINDOWS_DESKTOP_AUTOMATION` 升格為 **Fabric Shared Infrastructure Profile Team：`fabric-desktop-automation`**；以 **`fabric-desktop-cua`** 與 **`fabric-desktop-ufo2`** 兩個受治理 Provider Profiles 提供互補能力，重用 Hermes Kanban / Profile / current ExecutionBinding 做調度與租約，以 Cua 作最低摩擦 fast path、UFO²作 Windows-specialist complex path，維持 one-active-writer、readback/checkpoint 熱切換、Fabric knowledge ACL、OpenSpec durable-change、gstack investigation/review/QA 方法論，以及 Acceptance Officer 獨立驗收。

---

## 1.1 Blueprint claim ceiling

本藍圖只批准架構與施工路徑，不聲稱：

```text
FDA_RUNTIME_PASS
CUA_XQ_PASS
UFO2_XQ_PASS
XQ_AUTONOMOUS_DESKTOP_PASS
SQS_LIVE_TRADING_PASS
BROKER_WRITE_PASS
PRODUCTION_AUTONOMY
REMOTE_DEPLOYMENT_PASS
```

目前可下的最高結論：

```text
FDA_BLUEPRINT = PASS
FDA_IMPLEMENTATION = NOT_YET_EXECUTED_BY_THIS_ARTIFACT
FDA_PROMOTION = FAIL_CLOSED_PENDING_QUALIFICATION
```

**NORMATIVE locator：**
- `RP-002_v2.0_Master_Blueprint_2026-08-12_r2.md`：§0「兩個 heavy Stack／不得新增 Heavy Stack、scheduler、task DB、knowledge platform」；§5 canonical machine truth；§8 Profile Runtime Contract；§11 Knowledge；§12 Operability。fileciteturn17file0
- `Fabric\AGENTS.md`：Identity / Operating rules / Hermes execution chain / Hard prohibitions。fileciteturn17file2
- `RP-002_v2.0_STAGE-2...r2`：H1 Profile runtime materialization、anti-wheel、gstack/OpenSpec boundary、B1 Kanban、F0/F1/KG1。fileciteturn19file5
- FDA 討論 1–8：本藍圖需求演化與決策 lineage。fileciteturn12file4 fileciteturn12file5 fileciteturn12file6 fileciteturn12file7 fileciteturn12file0 fileciteturn12file1 fileciteturn12file2 fileciteturn12file3

---

## 1.2 r2 實質正文 supersession / non-regression contract

本 r2 **完整取代 r1 的施工藍圖正文**，但不推翻 r1 已判定正確的主架構。r2 的變更類型是：

```text
SUBSTANTIVE_CANONICALIZATION
+ MISSING_MATERIALIZATION
+ ANTI_DOWNGRADE
+ EXECUTION_SAFETY_CLOSURE
```

以下 r1 主幹必須保持不變：

```text
Fabric Shared Infrastructure Profile Team
→ fabric-desktop-automation
→ fabric-desktop-cua + fabric-desktop-ufo2
→ HGK WorkOrder / current ExecutionBinding
→ Hermes Profile + project-scoped Kanban
→ deterministic action-class route
→ one active desktop writer
→ readback/checkpoint hot-swap
→ Fabric-governed Knowledge / SoD / independent Acceptance
```

r2 新增並升格為**正文硬契約**的項目：

```text
R2-P01  Shared Infrastructure Team materialization / schema-resolution contract
R2-P02  Canonical FDA Desktop Capability Matrix
R2-P03  Parent ExecutionBinding/2 full inheritance + idempotency/replay
R2-P04  OASF / ContextForge / MCP / A2A same-subject interop promotion lineage
R2-P05  BreakGlass bypass semantics
R2-P06  FDA tool/provider exact-set + parent tool matrix additive anti-downgrade
R2-P07  Deferred SQS/XQ semi-auto consumer safety contract
R2-P08  Prompt Compiler C0-C9 mandatory durable-entry semantics
R2-P09  OpenTelemetry inherited CONDITIONAL_EMBEDDED disposition
```

**Non-regression hard rule：**

```text
R2_MAY_ADD_OR_CLARIFY = true
R2_MAY_SILENTLY_REMOVE_R1_PASSING_CONTRACT = false
R2_MAY_DOWNGRADE_PARENT_RP002_CAPABILITY_ROW = false
R2_MAY_CREATE_SECOND_CONTROL_PLANE = false
```

若 r2 與 current RP-002 machine truth 衝突，**current same-rank/higher-rank machine truth wins**；受影響項目進 `CR_OPEN` 並停止 mutation，不允許以藍圖例子反向覆蓋 current machine contract。

# 2. 輸入清單與定位證明（Inputs Manifest）

## 2.1 NORMATIVE / project-local inputs

> **裁決優先順序：A0 current user order > current RP-002 v2.0 Master/Stage machine truth > current Fabric/HGK/SQS authority/runtime evidence > operational docs/AGENTS projection > FDA discussion decisions > SUPPORT-only upstream/web。**

| 檔名／來源 | 角色 | 定位點證明 | 狀態 |
|---|---|---|---|
| Current user order（本次 FDA 藍圖要求） | **NORMATIVE A0** | 明定全量整合 FDA討論1–8、Fabric docs、RP-002 v2.0 Master/children；要求 Web、Fail-Closed、Machine blocks | FOUND |
| `RP-002_v2.0_Master_Blueprint_2026-08-12_r2.md` | **NORMATIVE A1** | §0 hard invariants；§5 canonical gate/machine truth；§8 Profile runtime；§11 Knowledge；§12 Operability；Stage contracts | FOUND fileciteturn17file0 |
| `RP-002_v2.0_STAGE-1_FABRIC-FOUNDATION_子藍圖_2026-08-12_r2.md` | **NORMATIVE A2** | Fabric canonical contract families、Capability Qualification、SoD、Profile registration、anti-wheel / support-only supply-chain | FOUND fileciteturn15file8 |
| `RP-002_v2.0_STAGE-2_HGK_SELF-HOSTING_AND_FABRIC_ACTIVATION_子藍圖_2026-08-12_r2.md` | **NORMATIVE A2** | K1→KG1；H1 Profile Team；B1 Kanban；F0 policy consumption；F1 self-hosting；KG1 knowledge governance | FOUND fileciteturn17file1 |
| `RP-002_v2.0_STAGE-3_SQS_PROFILEIZATION_AND_CROSS-STACK_EVOLUTION_2026-08-12_r2.md` / Stage-3 supervisor | **NORMATIVE A2** | exactly 3 persistent SQS profiles；Financial Truth owner bound；PAPER/no-live-write ceiling | FOUND / exact child bytes should be fresh-read at implementation; supervisor projection FOUND fileciteturn18file7 |
| `RP002_PROFILE_TEAM_MANIFEST.yaml` | **NORMATIVE machine truth** | Master §5；current manifest is canonical profile truth | REFERENCED / actual current bytes not attached → **UNVERIFIED** fileciteturn19file1 |
| `RP002_TOOL_AND_INHERITED_CAPABILITY_MATRIX.yaml` | **NORMATIVE machine truth** | selected tool/provider state、anti-downgrade | REFERENCED / current bytes **UNVERIFIED** fileciteturn19file1 |
| `RP002_CHANGE_CLASS_ROUTER.yaml` | **NORMATIVE machine truth** | durable change routing | REFERENCED / current bytes **UNVERIFIED** fileciteturn19file1 |
| `RP002_EXECUTION_BINDING.schema.json` | **NORMATIVE machine truth** | WorkOrder ↔ Profile/Kanban runtime ABI | REFERENCED / current bytes **UNVERIFIED** fileciteturn19file1 |
| Fabric `control/` policies | **NORMATIVE current** | AUTHORITY/RISK/MEMBER/CHANGE/SOD/ACCEPTANCE/EVOLUTION/PROMOTION/KNOWLEDGE/RELEASE/BREAK_GLASS/PROFILE_STACK/CAPABILITY_QUALIFICATION | REFERENCED; exact current bytes fresh-read required fileciteturn15file8 |
| Fabric `AGENTS.md` | Operational projection importing current authority | Identity、WorkOrder truth、Kanban≠authority、ROLE≠PROFILE≠WORKER、maker≠checker、critical writes readback/hash | FOUND fileciteturn17file2 |
| `Fabric使用說明文檔.md` | Operational projection | Post-Stage2 doc-upgrade contract specifies required guide sections/path | **MISSING as actual uploaded bytes**；upgrade prompt FOUND fileciteturn16file0 |
| Fabric `README.md` | Operational index | Referenced by current AGENTS mandatory reading order | **MISSING as actual uploaded bytes**；must fresh-read during FDA-C0 |
| HGK `AGENTS.md` / User Guide / README | NORMATIVE-adjacent operational/control projection | current HGK sole control-plane + Hermes/Codex/Profile/Kanban/Fabric route | REFERENCED / current bytes not fully attached in this turn → fresh-read required fileciteturn18file0 |
| SQS current User Guide / authority | Domain authority / operational projection | XQ V1 read-watch/HITL, PAPER/no-live-write, three persistent profiles | REFERENCED / handoff evidence available fileciteturn18file9 |
| SQS Engineering DOC-02 | **NORMATIVE domain/tool/security** | CapabilityProfile, deny-by-default, broker-write absent, external XQ operation/HITL | FOUND fileciteturn18file14 |
| SQS Reference Project Supervisor | NORMATIVE historical/current-domain acceptance | XQ/XS exact identity/permission/parity/degraded/fallback; no mock PASS; LOCAL/PAPER/NO-LIVE-WRITE | FOUND fileciteturn18file15 |
| RP-002 final program acceptance | Current milestone authority | RP-002 v2.0 completed/accepted; FDA must be post-RP002 evolution, not reopen Stage-1/2/3 | FOUND in conversation/project lineage; exact final receipt bytes must be rebound during implementation |

## 2.2 FDA discussion lineage — NORMATIVE current design intent under A0

| 檔名 | 角色 | 主要決策／定位 | 狀態 |
|---|---|---|---|
| `FDA討論-1_SQS 與 XQXS 的實際協作方式.md` | Design lineage | current XQ = bounded projection/read-watch; GUI autonomous adapter not yet proven | FOUND fileciteturn12file4 |
| `FDA討論-2_能否把人工縮到「登入 + 最終下單確認」.md` | Design lineage | Hermes current upstream computer-use/Cua；target automation；Cua bounded/local-only；no yolo | FOUND fileciteturn12file5 |
| `FDA討論-3_Fabric 治理下的 Hermes × HGK × SQS × XQXS 高自動化方案.md` | **Key correction lineage** | Human-authorized frozen XScript execution；Hermes不進 active-position fast loop；Fabric/HGK bounds desktop automation | FOUND fileciteturn12file6 |
| `FDA討論-4_更符合 Fabric HGK Hermes SQS 架構.md` | Design evolution | UFO²可 Profileize；macro/micro orchestration；Host/AppAgent可 bounded local plan | FOUND fileciteturn12file7 |
| `FDA討論-5_UFO² 放在 Fabric 層更合理.md` | Design evolution | Desktop automation上移 Fabric shared infrastructure；knowledge受Fabric ACL治理；不成第三Heavy Stack | FOUND fileciteturn12file0 |
| `FDA討論-6_技術選型結論.md` | Tool qualification | Cua lowest-friction P0；UFO² Windows specialist challenger；OpenAdapt deferred deterministic replay | FOUND fileciteturn12file1 |
| `FDA討論-7_Fabric-governed 架構下Cua 是最合理 P0 預設選型.md` | Tool lifecycle | Cua缺陷優先由 Fabric→HGK修補；fundamental no-fit則rollback/switch provider | FOUND fileciteturn12file2 |
| `FDA討論-8_Fabric 下Shared Infrastructure Profile Team：Desktop Automation.md` | **Current target architecture** | Shared Infrastructure Profile Team；Cua/UFO² Provider Profiles；one writer；sequential failover；Kanban/OpenSpec/gstack分工 | FOUND fileciteturn12file3 |

## 2.3 SUPPORT-only web sources — 2026 current readback

> SUPPORT 只用於 upstream capability、活躍度、風險、整合方式與候選比較；不得覆蓋上述 NORMATIVE。

| Support area | Source 1 | Source 2 | 本藍圖用途 |
|---|---|---|---|
| Hermes Computer Use + Cua | Hermes CLI/Computer Use official repo docs：`hermes computer-use install/status`、Windows/macOS/Linux | Cua official repo/docs：Windows/macOS/Linux background control, CLI/MCP | 支持 Cua 為最低磨合 provider |
| Hermes Kanban/Profile | Hermes Kanban docs：durable shared board across Profiles | Hermes `kanban_db.py` / issue lineage：shared DB、claim/heartbeat/reclaim caveats | 直接重用 Kanban，不造 FDA scheduler |
| Cua permissions/current activity | Cua Driver README permission modes / manifest concept | Cua Releases：2026-08-12 nightly 0.19.4、stable 0.19.3 | bounded permission + active maintenance |
| UFO² Windows capability | Microsoft UFO repo：UFO² LTS / Windows UIA/Win32/WinCOM/hybrid | UFO² AppAgent docs：UIA/visual detection, MCP GUI+API, RAG, FSM | specialist provider，保留 micro-intelligence |
| OpenSpec | supported-tools / changelog：Hermes skills-only supported | workflows/commands：propose/apply/update/verify/archive，verify completeness/correctness/coherence | durable FDA infrastructure changes only |
| gstack | current README：Hermes host support、多角色工具 | skills docs：investigate/review/QA/security/retro methodology | 方法論，不接 authority |
| Supply-chain | GitHub Actions Secure Use：full SHA pins | OpenSSF 2026 Baseline / CI guide：least privilege、pinning | conditional CI/tool provenance hardening |
| SLSA | SLSA v1.2 | SLSA verifying artifacts | package/build provenance only if actual build/release route applies |
| XQ | XQ 7.20.02/3.20.02 official announcement | XQ XS docs/learning: Print/File log/output | XQ fixture version drift + file/native readback-first |
| OpenAdapt | OpenAdapt README | validation/limits docs | future stable workflow deterministic replay，P1/P2 deferred |

### Web URL index

```text
Hermes CLI / Computer Use:
https://github.com/nousresearch/hermes-agent/blob/main/website/docs/reference/cli-commands.md
https://github.com/NousResearch/hermes-agent/blob/main/toolsets.py
https://github.com/NousResearch/hermes-agent/blob/main/agent/prompt_builder.py
https://github.com/nousresearch/hermes-agent/blob/main/website/docs/user-guide/features/kanban.md
https://github.com/NousResearch/hermes-agent/blob/main/hermes_cli/kanban_db.py

Cua:
https://github.com/trycua/cua
https://github.com/trycua/cua/releases
https://cua.ai/docs/how-to-guides/driver/install

UFO²:
https://github.com/microsoft/UFO
https://github.com/microsoft/UFO/releases
https://github.com/microsoft/UFO/blob/main/documents/docs/ufo2/overview.md
https://github.com/microsoft/UFO/blob/main/documents/docs/ufo2/app_agent/overview.md

OpenSpec:
https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md
https://github.com/Fission-AI/OpenSpec/blob/main/docs/workflows.md
https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md
https://github.com/Fission-AI/OpenSpec/blob/main/CHANGELOG.md

gstack:
https://github.com/garrytan/gstack
https://github.com/garrytan/gstack/blob/main/docs/skills.md

Supply chain:
https://docs.github.com/en/actions/reference/security/secure-use
https://baseline.openssf.org/versions/2026-02-19.html
https://openssf.org/blog/2025/06/11/maintainers-guide-securing-ci-cd-pipelines-after-the-tj-actions-and-reviewdog-supply-chain-attacks/
https://slsa.dev/spec/v1.2/
https://slsa.dev/spec/v1.2/verifying-artifacts

XQ:
https://www.xq.com.tw/announce/17400/

OpenAdapt:
https://github.com/OpenAdaptAI/OpenAdapt
https://github.com/OpenAdaptAI/openadapt-flow/blob/main/docs/validation/VALIDATION.md
https://github.com/OpenAdaptAI/openadapt-flow/blob/main/docs/LIMITS.md
```

---

# 3. 權威堆疊與現況診斷（Authority Stack & RCA）

## 3.1 Authority Stack

```text
A0  Current FDA user order
 ↓
A1  RP-002 v2.0 Master r2 + current RP002 machine truth
 ↓
A2  Stage-1 / Stage-2 / Stage-3 bounded contracts + final accepted lineage
 ↓
A3  current Fabric control/contracts/assurance/profile/knowledge machine state
 ↓
A4  current HGK WorkOrder/APL/GE/router/Profile/ExecutionBinding/runtime evidence
 ↓
A5  current SQS Financial Truth/RBWI/Risk/XQ adapter/domain contracts
 ↓
A6  current operational AGENTS/User Guide/README projections
 ↓
A7  FDA discussion 1–8 current design decisions
 ↓
SUPPORT  upstream official docs / current GitHub / OpenSSF / SLSA / research
```

**Conflict rule：**

```text
same_rank_conflict
→ CR_OPEN
→ affected capability = BLOCKED
→ no promotion until current owner resolves
```

**No-Source-No-Norm：**

```text
no current A0~A6 locator
→ design may be PROPOSAL
→ runtime norm = UNVERIFIED
→ implementation must first resolve source
```

## 3.2 Current architecture diagnosis

### Preserved system truth

```text
Fabric
= governance / assurance / interop / knowledge contract surface

HG-KSEOS
= sole governance / normative control plane

Hermes
= runtime / orchestration / Profile / Kanban / checkpoint / recovery

Codex
= bounded tracked writer when coding/writing applies

Acceptance Officer
= independent VERIFY_ONLY checker

WorkOrder
= normative task truth

Kanban
= runtime coordination state, not authority

Heavy Stacks
= HGK_ENGINEERING + SQS_FINANCIAL only
```

Locator：Master r2 §0；Fabric `AGENTS.md` Identity / Operating rules。fileciteturn17file0 fileciteturn17file2

### FDA architectural delta

FDA只新增／擴充一個**共享能力組織形態**：

```text
Fabric Shared Infrastructure Profile Team:
fabric-desktop-automation

Capability:
WINDOWS_DESKTOP_AUTOMATION

Provider Profiles:
fabric-desktop-cua
fabric-desktop-ufo2
current FDA Team artifact (`TEAM.md` or current equivalent)
FDA_DESKTOP_CAPABILITY_MATRIX
```

它**不新增**：

```text
third Heavy Stack
second scheduler
second task DB
second reducer
second Knowledge platform
global desktop planner
parallel task authority
new RP002 gate
```

---

## 3.3 RCA 根因樹

### RCA-01｜早期 SQS ↔ XQ 人工搬運過多

**症狀**

```text
SQS can prepare XScript / research
→ XQ import / compile / configure / export requires user
→ repeated manual bridge
```

**根因**
1. Current XQ/XS V1只證明 read/watch/manual-terminal contract；`gui_execution_status`/autonomous adapter未被 current runtime admission證明。
2. XQ是Windows GUI runtime，缺乏已 qualification 的 Hermes desktop control binding。
3. 過去不能把 UI presence/mock當 runtime PASS。

**證據**
- FDA討論-1。fileciteturn12file4
- SQS Reference Project Supervisor XQ/XS qualification contract。fileciteturn18file15

**修復方向**
- FDA建立受治理 Windows desktop capability。
- 不改 Financial Truth owner、不把GUI當 execution truth。

---

### RCA-02｜把「Desktop Automation」誤等同「AI交易execution」

**症狀**
早期討論容易把 Hermes GUI control靠近盤中 execution。

**根因**
交易 plane 與 operator/control plane未充分拆分。

**已裁決修正**
- 使用者明確規定：進場後加碼、減碼、止損、止盈、清倉由事先規劃 XS機械式執行。
- Hermes/LLM/Codex不進active-position fast loop。
- 這是未来 SQS consumer design intent；**current RP-002 authority仍 `SQS live trading = NOT_AUTHORIZED`**，FDA P0只做 PAPER/no-live-write compatibility。

**證據**
- FDA討論-3。fileciteturn12file6
- Stage-3 current claim ceiling。fileciteturn18file7

---

### RCA-03｜UFO²「第二AgentOS」風險被過度簡化成「不能用UFO」

**症狀**
初始判斷把 UFO²視為可能與 HGK/Hermes衝突的 second orchestrator。

**根因**
混淆「local micro-planning capability」與「normative project authority」。

**已裁決修正**
- UFO²可以保留HostAgent/AppAgent/FSM/GUI+API hybrid intelligence。
- 它只在一個 admitted WorkOrder/Profile invocation內micro-plan。
- 不得建立 WorkOrder、改Fabric policy、改FinancialSpec/risk、self-promote/self-accept。

**證據**
- FDA討論-4。fileciteturn12file7
- UFO²官方 AppAgent/HostAgent是hierarchical local execution，且可作上游Galaxy的device agent（SUPPORT）。

---

### RCA-04｜把UFO²放SQS會造成重用與Profile邊界不佳

**症狀**
`SQS → UFO²`只服務XQ，HGK未來desktop-only engineering需求要再整合一次。

**根因**
Desktop automation是cross-stack infrastructure capability，不是financial domain truth。

**已裁決修正**
移到Fabric Shared Infrastructure，供HGK/SQS consumer共同使用。

**證據**
- FDA討論-5。fileciteturn12file0
- Master heavy stacks只有HGK/SQS，不新增Heavy Stack。fileciteturn17file0

---

### RCA-05｜Cua vs UFO²的「單一winner」選型會丟失互補性

**症狀**
Cua有Hermes-native低摩擦；UFO²有更深Windows/UIA/Win32/visual/hybrid能力，難以只靠紙面決定。

**根因**
兩個provider的failure modes/knowledge/runtime/permission surface不同。

**裁決**
- Cua = initial fast-path incumbent。
- UFO² = same-team specialist profile。
- 最終action-class routing由真實fixtures決定，不由品牌偏好或LLM自由猜。

**證據**
- FDA討論-6、7、8。fileciteturn12file1 fileciteturn12file2 fileciteturn12file3
- SUPPORT：Hermes直接支援Cua；UFO²有UIA+Win32+visual+hybrid。

---

### RCA-06｜熱插拔若沒有single-writer與checkpoint會產生desktop race

**症狀**
兩個profiles同時click/type同一XQ session可破壞UI state。

**根因**
Desktop不是可合併的並行worktree；side effect具順序與焦點依賴。

**裁決**
```text
ONE_ACTIVE_DESKTOP_WRITER_PER_SESSION = HARD
SECOND_WRITER = DENY
HOT_SWAP_ONLY_AFTER = READBACK + CHECKPOINT + KNOWN_STATE
```

**證據**
- FDA討論-8。fileciteturn12file3
- Fabric `AGENTS.md` one writer / WorkOrder/Kanban separation。fileciteturn17file2

---

### RCA-07｜若FDA模仿Kanban/OpenSpec/gstack會重造control plane

**症狀**
「參考」方法容易變成另建 queue/scheduler/spec/release authority。

**根因**
工具能力與authority ownership未分開。

**裁決**
- Kanban：**直接重用 Hermes Kanban**。
- OpenSpec：只處理 durable FDA infrastructure changes。
- gstack：只吸收 `/investigate`、review、QA、security、retro等方法；不採Conductor/spec/release authority。
- Fabric/HGK：保留唯一normative control。

**證據**
- Stage-2 H1/anti-wheel/gstack boundary。fileciteturn19file5
- FDA討論-8。fileciteturn12file3

---

### RCA-08｜共享Knowledge若裸共享Profile memory會形成第二Knowledge authority與洩漏

**症狀**
Cua/UFO共享XQ操作經驗很有價值，但直接互讀private memory會混入credentials、stale/non-approved knowledge。

**根因**
「共享儲存」與「共享authority」被混淆。

**裁決**
```text
private Hermes profile memory = PRIVATE
Fabric-governed approved knowledge = SHAREABLE
provider experience write = CANDIDATE_ONLY
promotion = Fabric owner/acceptance route
```

**證據**
- Master §11 namespace/producer-consumer model。fileciteturn18file5
- FDA討論-5/8。fileciteturn12file0 fileciteturn12file3

---

### RCA-09｜Cua問題不能假設HGK永遠能「修掉」

**症狀**
「Fabric會叫HGK修」可能被誤讀為永不需要provider replacement。

**根因**
把adapter defect與upstream/OS fundamental no-fit混為一談。

**裁決**
```text
repairable:
  wrapper/binding/selector/retry/readback/version-pin/fixture

possibly_nonrepairable_locally:
  upstream driver defect/UIPI limitation/custom control no-observability/binary crash/license
```

後者路由：

```text
isolate → pin/rollback → workaround/upstream patch → alternate provider
```

**證據**
- FDA討論-7。fileciteturn12file2
- SUPPORT：Hermes/Cua仍有Windows helper/claim/runtime edge issues，因此必須保留failover。

---

# 4. Web Research 摘要（2026 Support Evidence）

> **全部為 SUPPORT。任何 upstream功能只有經 FDA current local qualification後才可變成 runtime claim。**

## 4.1 Hermes + Cua：目前最低磨合的基礎路線

Hermes current CLI已將 `cua-driver`直接作為Computer Use backend，提供 `hermes computer-use install` / `install --upgrade` / `status`，且上游安裝路徑明列 Windows/macOS/Linux；Hermes `computer_use` toolset也直接把Cua描述成背景desktop control。另一方面 Cua官方repo把Driver定位為Windows/macOS/Linux native desktop control，提供CLI/MCP，適合agent直接使用。  
SUPPORT：citeturn278260search0turn278260search3turn683955search10

**FDA implication：**
- `fabric-desktop-cua`應作第一個effective-load候選。
- 不再自寫pyautogui/RPA core。
- exact local Hermes/Cua版本仍須pin/readback。

Cua release頁在2026-08-12仍有`nightly-cua-driver-rs-v0.19.4...`，stable列表包含`cua-driver-rs v0.19.3`，顯示Windows/driver線仍活躍。  
SUPPORT：citeturn683955search0

---

## 4.2 Cua permission model與Fabric高度相容

Cua Driver現有permission設計包含受manifest約束的bounded模式；Hermes prompt本身也要求不要碰password/payment/permission dialogs、不要輸入secrets、遇到持續故障用structured health/doctor路徑。  
SUPPORT：Hermes safety guidance citeturn278260search4；Cua current driver/docs/repo citeturn683955search10turn683955search7

**FDA implication：**
```text
Fabric Profile permission
→ compile to current provider permission surface
→ no unrestricted/yolo in governed FDA
```

但**exact Cua manifest schema/CLI flags必須在實作日fresh-read current upstream/local binary**，本藍圖不偽造provider schema。

---

## 4.3 Hermes Kanban就是 FDA macro-coordination substrate

Hermes官方Kanban文件把Kanban定義為跨Profiles共享的durable board，每個worker為獨立OS process；底層`kanban_db.py`也明確說Profiles collapse onto shared board，是cross-profile coordination primitive。社群issue又顯示長MCP call、reclaim、SQLite concurrency等實際failure modes，說明FDA需要 bounded tasks/heartbeat/readback，而不是再造一套scheduler。  
SUPPORT：citeturn705258search3turn705258search11turn705258search4turn705258search5

**FDA implication：**
- Kanban = macro task coordination。
- Cua/UFO local plan = micro execution。
- desktop action不拆成每click一張card。
- 不建立`desktop-task.db`。

---

## 4.4 UFO²：最強的Windows-specialist互補Profile候選

Microsoft current UFO repo把UFO²列為LTS/stable Windows automation，具 Windows UIA、Win32、WinCOM、visual+UIA detection、hybrid GUI/API、Knowledge Substrate，且可作上層Galaxy的Windows device agent；AppAgent官方文件確認它是application-specialized worker，有UIA/visual detection、MCP GUI/API execution與knowledge context。  
SUPPORT：citeturn278260search1turn658409search2turn658409search0

**FDA implication：**
- UFO²不必被拆到只剩click/type。
- 可以保留bounded HostAgent/AppAgent micro-orchestration。
- 但它不取得WorkOrder/FinancialSpec/risk/promotion/acceptance authority。

本輪search未找到**2026-08-11之後新的UFO² release tag**；current repo仍明確標示UFO² LTS/actively maintained。Latest release listing surfaced Aug-9 release lineage。  
SUPPORT：citeturn913311search5turn913311search2  
**Disposition：`CURRENT_MAINTAINED / POST_0811_NEW_RELEASE_NOT_FOUND_IN_THIS_SEARCH`。**

---

## 4.5 OpenSpec：只管durable FDA change，不進daily runtime

OpenSpec current docs把workflow設計為fluid而非rigid，核心`propose/apply/update/sync/archive`，擴展`verify`可檢查completeness/correctness/coherence；current changelog/支持工具也明確支援Hermes skills-only integration。  
SUPPORT：citeturn913311search0turn913311search7turn913311search10turn913311search13

**FDA implication：**
適用：
```text
新增/移除 provider
改 routing contract
改 permission boundary
改 knowledge schema
改 hot-swap policy
```

不適用：
```text
今天開XQ
今天compile腳本
今天讀log
```

---

## 4.6 gstack：方法論 donor，不是 FDA control plane

gstack current repo提供多角色方法，包括review、QA、security、investigate、retro，且README列出Hermes host支援；`/investigate`強調先RCA再修，適合provider/selector/UI drift事故。  
SUPPORT：citeturn658409search1turn658409search4

**FDA採用：**
```text
investigate
review
qa
cso/security
retro
plan-eng-review
```

**FDA不採用：**
```text
gstack Conductor authority
gstack /spec as canonical owner
gstack /ship as Fabric promotion/release authority
```

---

## 4.7 OpenSSF / GitHub / SLSA

GitHub官方secure-use明確建議third-party Actions以full-length commit SHA固定；OpenSSF 2026 Baseline要求CI/CD least privilege；SLSA v1.2指出provenance只有被verify才有價值。  
SUPPORT：citeturn683955search1turn683955search31turn705258search2turn683955search2turn683955search20

**FDA implication：**
- 如果FDA repo已有remote CI，third-party actions用full SHA + least permissions。
- 如果只是local Windows runtime，不為了形式新建remote CI/SLSA平台；這與RP-002本身「conditional supply-chain hardening」一致。fileciteturn16file10

---

## 4.8 XQ current surface

本輪搜索找到XQ官方 **2026-08-06** 公告：current 7.20.02/3.20.02（260731）新增/修補包括XS Log Viewer、自動交易排程、策略雷達/自動交易篩選，且修補多個GUI/XQ runtime問題。這表示XQ UI/runtime會drift，FDA不能把selector/window schema寫死成永不變。  
SUPPORT：citeturn345678search0

本輪未找到2026-08-11之後較新的XQ官方版本公告；因此：
```text
latest_verified_by_this_search = 7.20.02 / 3.20.02 (2026-08-06 announcement)
post_2026_08_11_new_release = NOT_FOUND
```

FDA readback優先順序：
```text
native/file output
→ UIA/Win32 structured state
→ visual grounding
→ coordinate/pixel fallback
```

---

## 4.9 OpenAdapt：保留為未來deterministic replay候選，不納入P0

OpenAdapt current project把自己定位為「demonstration → inspectable deterministic local workflow」，healthy path可無generative calls，且identity/outcome verification失敗會safe-halt；其validation文件公開記錄wrong-target hardening與0-silent-wrong-action的**bounded**測試結果，同時明確不把該結果宣稱成universally reliable。  
SUPPORT：citeturn138723search0turn138723search1turn138723search2

**FDA disposition：**
```text
OPENADAPT = DEFERRED_PATTERN_COMPILER_CANDIDATE
trigger = repeated stable FDA workflow + measurable benefit
```

P0不安裝，避免三套runtime同時落地。

---

## 4.10 r2 Support freshness / exact-set recheck（2026-08-13）

> 本節仍是 SUPPORT；只用來避免 r2 對工具選型資訊過時，不覆蓋 RP-002/Fabric/HGK/SQS current machine truth。

截至 2026-08-13 的官方 upstream readback沒有推翻 r1/r2 的選型方向：

| 技術 | Current support readback | r2 disposition impact |
|---|---|---|
| Hermes `computer_use` | current CLI仍提供 `hermes computer-use install/install --upgrade/status`，上游描述 installer涵蓋Windows/macOS/Linux，backend為Cua Driver | `INHERIT_ACTIVE_BASE` |
| Cua Driver | current driver/release線仍活躍；2026-08-12有0.19.4 nightly lineage，stable 0.19.3仍可見；Windows native desktop control + MCP/CLI路線維持 | `P0_PRIMARY_FAST_PATH` |
| UFO² | Microsoft current repo/release仍將UFO²列為Windows stable/LTS，支援深Windows整合與hybrid GUI+API，亦可作Galaxy device agent | `P0_SPECIALIST_STANDBY` |
| Agent S3 | 2026-07-30官方repo記錄S3論文獲TMLR 2026接受，Windows/Linux/macOS可用；仍屬額外GUI-agent framework | `NO_ADOPT_P0` |
| Appium Windows Driver | 2026-07-29 v6.1.0；仍是Windows test automation driver，依賴WinAppDriver | `SUPPORT_BENCHMARK_DONOR` |
| WinAppDriver | Selenium-like Windows application testing service；是Appium Windows Driver底層依賴之一 | `SUPPORT_DEPENDENCY_ONLY` |
| FlaUI | Windows UIA library；latest release v5.0.0仍是2025-02-25，但2026仍有社群活動 | `SUPPORT_LOW_LEVEL_DONOR` |
| pywinauto | latest release仍為2025-01-06 0.6.9 | `NO_ADOPT` |
| UFO³ Galaxy | cross-device/multi-device orchestration；與HGK/Hermes macro orchestration重疊 | `NO_ADOPT_P0_AUTHORITY_OVERLAP` |
| OpenAdapt | deterministic/inspectable workflow方向仍適合作未來stable workflow compiler | `DEFERRED_PATTERN_COMPILER_CANDIDATE` |

Support URLs：

```text
https://github.com/nousresearch/hermes-agent/blob/main/website/docs/reference/cli-commands.md
https://github.com/trycua/cua/releases
https://github.com/microsoft/UFO
https://github.com/microsoft/UFO/releases
https://github.com/simular-ai/agent-s
https://github.com/appium/appium-windows-driver/releases
https://github.com/microsoft/WinAppDriver
https://github.com/FlaUI/FlaUI/releases
https://github.com/pywinauto/pywinauto/releases
https://github.com/OpenAdaptAI/OpenAdapt
```

# 5. 完整整合藍圖（The Integrated Solution）

## 5.1 Architecture landing：最小磨合落點

```text
┌────────────────────────────────────────────────────────────┐
│                         FABRIC                             │
│ governance / SoD / capability / knowledge / acceptance    │
│ promotion / rollback / evidence / interop                  │
└─────────────────────────┬──────────────────────────────────┘
                          │ consumed by
                          ▼
┌────────────────────────────────────────────────────────────┐
│                       HG-KSEOS                             │
│ sole normative control plane                              │
│ Requirement → TaskSpec → WorkOrder → ExecutionBinding     │
└─────────────────────────┬──────────────────────────────────┘
                          │
                          ▼
┌────────────────────────────────────────────────────────────┐
│                         Hermes                             │
│ runtime/orchestrator + Profiles + project-scoped Kanban    │
└─────────────────────────┬──────────────────────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────────┐
        │ Fabric Desktop Automation Profile  │
        │ Team: fabric-desktop-automation    │
        │ Capability: WINDOWS_DESKTOP_AUTOMATION
        └─────────────────┬───────────────────┘
                          │ deterministic route
              ┌───────────┴─────────────┐
              ▼                         ▼
   fabric-desktop-cua         fabric-desktop-ufo2
   Cua Driver                 UFO² Host/AppAgent
   FAST PATH                  SPECIALIST PATH
   Hermes-native              Windows-specific
              │                         │
              └───────────┬─────────────┘
                          │
                  one active writer
                          ▼
                     Windows Apps
                     ┌────┴─────┐
                     ▼          ▼
                    XQ/XS      HGK engineering apps
                     ▲          ▲
                     │          │
             SQS consumer     HGK consumer
```

### Hard invariants

```text
HEAVY_STACK_COUNT remains 2
FDA_IS_HEAVY_STACK = false

WORKORDER_IS_TASK_TRUTH = true
KANBAN_IS_COORDINATION_ONLY = true

ROLE != PROFILE != WORKER
CAPABILITY != PROVIDER

ONE_ACTIVE_DESKTOP_WRITER_PER_SESSION = true
SECOND_CONCURRENT_WRITER = DENY

PROVIDER_SWITCH_REQUIRES:
  READBACK
  CHECKPOINT
  KNOWN_DESKTOP_STATE
  LEASE_TRANSFER

FABRIC_DESKTOP_PROFILE_MAY_NOT:
  CREATE_WORKORDER
  CHANGE_FINANCIAL_TRUTH
  CHANGE_RISK_AUTHORITY
  SELF_ACCEPT
  SELF_PROMOTE
  CREATE_SECOND_KNOWLEDGE_PLATFORM
```

---

## 5.2 Identity model

### Team

```text
team_id = fabric-desktop-automation
team_class = SHARED_INFRASTRUCTURE_PROFILE_TEAM
heavy_stack = false
```

### Capability

```text
capability_id = WINDOWS_DESKTOP_AUTOMATION
```

### Profiles

```text
fabric-desktop-cua
fabric-desktop-ufo2
```

### Providers

```text
fabric-desktop-cua  → CUA_DRIVER
fabric-desktop-ufo2 → MICROSOFT_UFO2
```

### Consumers

```text
HGK_ENGINEERING:
  capability binding examples:
    IDE / installer / GUI-only local engineering tool

SQS_FINANCIAL:
  capability binding:
    XQ_DESKTOP_CONTROL
```

**Important：** SQS不own FDA；XQ只是FDA第一個高價值consumer。

---

## 5.3 Profile runtime contract

RP-002 Stage-2要求每個Profile沿用`RP002-PROFILE-RUNTIME-CONTRACT/2`，包括distribution、commit/digest、SOUL/config/skills/MCP/fixtures、runtime identity、permissions、I/O、positive/negative fixtures、rollback；不得fork child schema。fileciteturn19file5

因此FDA應**instance化現有profile schema，不發明第二Profile schema**。

### Conceptual FDA team projection

> 下列是**藍圖映射**，不是宣稱current `RP002_PROFILE_TEAM_MANIFEST.yaml`已支援這些exact field names。實作時必須將其映射到current schema；若schema不能表示shared-infrastructure team，走最小合法schema extension / current Change Router。禁止直接寫第二manifest。

```yaml
# conceptual projection; map to current canonical schema at FDA-C0/C1.
team_id: fabric-desktop-automation
class: SHARED_INFRASTRUCTURE_PROFILE_TEAM
heavy_stack: false
runtime_engine: HERMES
coordination: PROJECT_SCOPED_KANBAN
capability: WINDOWS_DESKTOP_AUTOMATION

profiles:
  - profile_id: fabric-desktop-cua
    provider: CUA_DRIVER
    lifecycle: ON_DEMAND
    initial_mode: PRIMARY_FAST_PATH

  - profile_id: fabric-desktop-ufo2
    provider: MICROSOFT_UFO2
    lifecycle: ON_DEMAND
    initial_mode: SPECIALIST_STANDBY

writer_policy:
  max_active_writers_per_desktop_session: 1

acceptance:
  final_checker: ACCEPTANCE_OFFICER
  maker_self_accept: false
```

---

## 5.3A Shared Infrastructure Profile Extension Decision Contract

FDA不得靠概念名稱直接 materialize。施工時必須先決定 current RP-002 Profile/TEAM schema是否能表達「非Heavy Stack的共享基礎設施 Profile Team」。

### Decision algorithm

```text
fresh-read current:
  RP002_PROFILE_TEAM_MANIFEST.yaml (or current superseding machine truth)
  RP002-PROFILE-RUNTIME-CONTRACT/2
  current TEAM schema/convention
  PROFILE_STACK_REGISTRATION_POLICY
  CAPABILITY_QUALIFICATION_POLICY
  RP002_CHANGE_CLASS_ROUTER
        ↓
can current schema represent shared-infrastructure Profile Team without semantic stuffing?
        ├─ YES
        │   → REUSE current schema exactly
        │   → no new enum/schema family
        │
        └─ NO
            → route one parent-compatible governed schema evolution
            → old HGK/SQS/FABRIC_ASSURANCE instances must still validate
            → FDA instances must validate
            → heavy_stack_count remains exactly 2
            → child schema fork = 0
```

### Explicit anti-stuffing rule

不得為了避免schema evolution而把 FDA 假裝成：

```text
HGK_ENGINEERING
SQS_FINANCIAL
FABRIC_ASSURANCE
```

若它實際語義不符合上述 owner/domain。

### Required Team materialization

FDA v1 必須有**一個 current-canonical Team artifact**。若 current convention使用 `TEAM.md`，logical identity為：

```text
fabric-desktop-automation/TEAM.md
```

若 current Fabric machine family使用其他等價artifact，必須採 current exact owner/path，**不得同時再造第二份 TEAM truth**。

最低內容：

```yaml
# logical contract; map to current exact schema/field names.
team_id: fabric-desktop-automation
team_class: SHARED_INFRASTRUCTURE_PROFILE_TEAM
heavy_stack: false

profile_refs:
  - fabric-desktop-cua
  - fabric-desktop-ufo2

capability_matrix_ref: FDA_DESKTOP_CAPABILITY_MATRIX
allowed_assignee_profiles:
  - fabric-desktop-cua
  - fabric-desktop-ufo2

router_owner: HGK_CURRENT_ROUTER
coordination_owner: HERMES_PROJECT_SCOPED_KANBAN
execution_binding_ref: CURRENT_RP002_EXECUTION_BINDING
writer_policy_ref: FDA_ONE_ACTIVE_DESKTOP_WRITER
knowledge_policy_ref: CURRENT_FABRIC_KNOWLEDGE_POLICY
interop_refs:
  - CURRENT_OASF_RECORD_IF_APPLICABLE
  - CURRENT_CONTEXTFORGE_REGISTRATION_IF_APPLICABLE
acceptance_ref: CURRENT_FABRIC_ACCEPTANCE_PACK
breakglass_policy_ref: CURRENT_RP002_BREAK_GLASS
```

TEAM artifact：

```text
!= Authority Matrix
!= WorkOrder truth
!= scheduler
!= task database
!= tool registry
```

### Team acceptance

```text
TEAM_ARTIFACT_PRESENT_AND_CURRENT = PASS
TEAM_PROFILE_REFS_EXACT = PASS
TEAM_CAPABILITY_MATRIX_REF_EXACT = PASS
TEAM_ALLOWED_ASSIGNEE_SET_EXACT = PASS
TEAM_ROUTER_OWNER_CURRENT = PASS
TEAM_WRITER_INVARIANT_BOUND = PASS
TEAM_KNOWLEDGE_POLICY_BOUND = PASS
TEAM_INTEROP_REFS_DISPOSITIONED = PASS
TEAM_ACCEPTANCE_REF_EXACT = PASS
```

任一缺失：

```text
FDA-C1 = FAIL_CLOSED
```

---

## 5.3B Canonical FDA Desktop Capability Matrix

`Deterministic Provider Router` 不得以 runtime-local `dict`、LLM memory、README或歷史 benchmark作 routing truth。

FDA必須 materialize 一個**canonical additive capability view**：

```text
logical_artifact_id: FDA_DESKTOP_CAPABILITY_MATRIX
logical_schema: FDA-DESKTOP-CAPABILITY-MATRIX/1
canonical_owner: Fabric Capability Qualification policy
runtime_consumer: HGK deterministic router / Hermes binding
mutation_authority: admitted HGK WorkOrder only
promotion_authority: current Fabric promotion + independent Acceptance
rollback: previous promoted matrix digest
```

> 這個 Matrix **不是第二 Tool Registry**。Tool/provider installation/current-state truth仍由 current `RP002_TOOL_AND_INHERITED_CAPABILITY_MATRIX.yaml` 或其 successor 擁有；FDA Matrix只保存「desktop action-class qualification/routing facts」。

### Required row schema

```yaml
schema: FDA-DESKTOP-CAPABILITY-MATRIX/1
subject_digest: <current FDA subject>
application:
  id: XQ
  version: <exact current version>
action_class: XS_COMPILE

providers:
  CUA:
    provider_identity_ref: <current tool matrix row/ref>
    profile_id: fabric-desktop-cua
    state: QUALIFIED|BLOCKED|DEFERRED|QUARANTINED
    qualification_subject_digest: <sha256>
    workflow_pass_rate: <measured>
    silent_wrong_action: <integer>
    wrong_action: <integer>
    detected_failure_rate: <measured>
    mean_recovery_count: <measured>
    median_completion_time_ms: <measured>
    structured_control_coverage: <measured-or-NA>
    vision_fallback_rate: <measured-or-NA>
    human_intervention_count: <integer>
    restart_recovery_rate: <measured>
    version_drift_state: CURRENT|REQUALIFY_REQUIRED
    evidence_refs: []

  UFO2:
    provider_identity_ref: <current tool matrix row/ref>
    profile_id: fabric-desktop-ufo2
    state: QUALIFIED|BLOCKED|DEFERRED|QUARANTINED
    qualification_subject_digest: <sha256>
    workflow_pass_rate: <measured>
    silent_wrong_action: <integer>
    wrong_action: <integer>
    detected_failure_rate: <measured>
    mean_recovery_count: <measured>
    median_completion_time_ms: <measured>
    structured_control_coverage: <measured-or-NA>
    vision_fallback_rate: <measured-or-NA>
    human_intervention_count: <integer>
    restart_recovery_rate: <measured>
    version_drift_state: CURRENT|REQUALIFY_REQUIRED
    evidence_refs: []

routing:
  preferred: CUA|UFO2|BLOCKED
  alternate: CUA|UFO2|null
  reason_code: <deterministic>
  hot_swap_allowed: true|false

lifecycle:
  promoted_at: <rfc3339|null>
  prior_matrix_digest: <sha256|null>
  rollback_matrix_digest: <sha256|null>
```

### Routing tie-breaker / anti-overengineering

當同一 `application_version + action_class`：

```text
CUA = PASS
UFO2 = PASS
```

預設仍：

```text
preferred = CUA
```

除非同一subject的可比實測證據顯示 UFO² 在 reliability / required Windows capability 上有 material advantage，且該變更經 governed Matrix promotion。

禁止動態 bandit、LLM self-routing、每次run重新競賽。

Capability Matrix保存必要 diagnostic metrics，但：

```text
FDA_DESKTOP_CAPABILITY_MATRIX != SLO_PLATFORM
FDA_DESKTOP_CAPABILITY_MATRIX != OBSERVABILITY_DATABASE
```

不為了矩陣再建time-series/telemetry服務。

### Mutation rules

```text
provider benchmark result
→ candidate Matrix row
→ independent readback
→ Acceptance Officer
→ Fabric promotion
→ new promoted Matrix digest
```

禁止：

```text
provider self-updates routing row
LLM changes preferred provider ad hoc
single failed run rewrites canonical primary
historical matrix silently overwritten
```

### Historical failure input

Recurring provider failure may影響 future route only through：

```text
failure_signature
+ comparable subject/app/version/action_class
+ bounded evidence threshold
+ governed matrix promotion
```

not through ephemeral agent memory.

---

## 5.3C Parent Tool/Technology Exact-Set Anti-Downgrade Contract

Machine truth仍是：

```text
RP002_TOOL_AND_INHERITED_CAPABILITY_MATRIX.yaml
```

或 current same-authority successor。

FDA是**additive child view**：

```text
FDA_CHANGESET_MUST_NOT_DELETE_PARENT_ROW = TRUE
FDA_MISSING_PARENT_ROW != N_A
FDA_MISSING_PARENT_ROW = FAIL_CLOSED
```

任何 parent capability 的移除/替換/降級都必須另有：

```text
explicit current ChangeSet
→ owner authorization
→ replacement/fallback
→ regression
→ independent Acceptance
→ promotion/rollback
```

### FDA-specific named disposition denominator

| 技術/能力 | r2 disposition | 是否P0安裝/啟用 | FDA用途 | Anti-downgrade / rollback |
|---|---|---:|---|---|
| Hermes `computer_use` | `INHERIT_ACTIVE_BASE / REQUALIFY_EXACT_LOCAL` | current route | agent-facing desktop abstraction | current HGK/Hermes binding wins |
| **Cua Driver** | `P0_PRIMARY_FAST_PATH` | YES after qualification | lowest-friction provider | pin/current identity + rollback + UFO alternate |
| **UFO²** | `P0_SPECIALIST_STANDBY` | YES after qualification | Windows-specialist complex/hybrid path | exact pin + disable/rollback + Cua alternate |
| **OpenAdapt** | `DEFERRED_PATTERN_COMPILER_CANDIDATE` | NO P0 | future deterministic replay | separate future ChangeSet |
| **Agent S3** | `NO_ADOPT_P0` | NO | research/benchmark reference only | cannot silently become FDA orchestrator |
| **Appium Windows Driver** | `SUPPORT_BENCHMARK_DONOR` | NO P0 | structured Windows test/reference donor | no production route without separate qualification |
| **WinAppDriver** | `SUPPORT_DEPENDENCY_ONLY` | NO direct P0 | Appium Windows dependency/reference | no remote exposure by default |
| **FlaUI** | `SUPPORT_LOW_LEVEL_DONOR` | NO P0 | Windows UIA library donor | no parallel runtime/control plane |
| **pywinauto** | `NO_ADOPT` | NO | legacy/simple reference only | no fallback-by-convenience |
| **UFO³ Galaxy** | `NO_ADOPT_P0_AUTHORITY_OVERLAP` | NO | cross-device orchestration reference | forbidden as second macro orchestrator |

### Inherited RP-002 rows that FDA must explicitly preserve/disposition

At minimum FDA readback must preserve current parent rows for：

```text
Hermes Runtime
Hermes Profiles
Hermes Profile Distribution
Hermes Kanban
Hermes A2A
MCP
ContextForge
OASF
OpenTelemetry
Codex CLI / current coding provider route
OpenSpec
gstack
current Knowledge substrate/providers
GitHub Actions/OpenSSF/SLSA conditional rows
```

`OpenTelemetry`：

```text
disposition = INHERIT_CURRENT_PARENT_CONDITIONAL_EMBEDDED
if current qualified exporter/trace route active:
    correlate FDA run_id / provider / action receipt
else:
    explicit N/A or DEFER
standalone collector/platform for FDA P0 = NOT_REQUIRED
```

## 5.4 Provider responsibility split

| Capability class | Cua | UFO² | Initial route |
|---|---:|---:|---|
| app/window capture | strong candidate | strong candidate | Cua |
| known UIA element | strong candidate | strong candidate | Cua |
| click/type/scroll known control | strong candidate | strong candidate | Cua |
| simple fixed dialog | strong candidate | strong | Cua |
| custom/non-standard control | CONDITIONAL until XQ fixture | stronger theoretical fit | UFO² if certified |
| UIA sparse/ambiguous | CONDITIONAL | visual+UIA hybrid candidate | UFO² |
| complex multi-step app workflow | possible | app-local FSM advantage | UFO² if certified |
| GUI + native API hybrid | provider-dependent | explicit architecture | UFO² |
| unknown financial side effect | DENY | DENY | HITL/BLOCK |
| password/MFA/credential | DENY | DENY | HUMAN |
| current live broker write | DENY | DENY | NOT_AUTHORIZED |

**Primary/standby只是初始policy，不是永久winner。**

---

## 5.5 Macro / micro orchestration SoD

```text
HGK:
  whether task exists
  owner
  authority
  write boundary
  acceptance
  promotion

Hermes:
  claim
  dependency readiness
  Profile invocation
  Kanban heartbeat/checkpoint/retry
  provider handoff

Cua/UFO²:
  how to execute bounded desktop action/workflow

Acceptance Officer:
  fresh-context independent verification
```

UFO² HostAgent/AppAgent可保留：

```text
OBSERVE
→ SELECT_APP
→ PLAN_LOCAL_UI_STEPS
→ UIA/API/VISION EXECUTION
→ READBACK
→ LOCAL_RECOVERY
```

但不能越界到project/domain authority。

---

## 5.6 Desktop Lease：重用ExecutionBinding，不造新lock service

Conceptual metadata：

```json
{
  "desktop_session_id": "FDA-SESSION-<generated>",
  "desktop_target": {
    "host": "<current-host>",
    "application": "XQ",
    "process_identity": "<fresh-read>",
    "window_identity": "<fresh-read>"
  },
  "writer_profile": "fabric-desktop-cua",
  "lease_state": "ACTIVE",
  "lease_expiry": "<RFC3339>",
  "checkpoint_ref": "<current-kanban/evidence-ref>",
  "provider_switch_allowed": true
}
```

規則：

```text
lease exists + writer A
→ writer B write = DENY

lease transfer:
A stops actions
→ readback
→ checkpoint
→ release A lease
→ acquire B lease
→ B observes current state
→ resume
```

**Exact field location must reuse current `ExecutionBinding/2` extension or current Kanban task metadata; no `desktop-lock-server`。**

---

## 5.6A Canonical ExecutionBinding Desktop Overlay + Idempotency / Replay

FDA **不得建立 `FDA_EXECUTION_BINDING.schema.json` 之類的 child schema**。每個 desktop task仍必須 validate current Parent：

```text
RP002-EXECUTION-BINDING/2
```

並保留完整：

```text
normative.*
routing.*
delegation.*
lease.*
budget.*
idempotency.*
runtime.*
terminal.*
```

Parent required idempotency contract：

```yaml
idempotency:
  idempotency_key: string
  side_effect_class: NONE|LOCAL_REVERSIBLE|EXTERNAL_APPROVAL_GATED
  replay_policy: SAFE_REPLAY|READBACK_BEFORE_RETRY|FORBIDDEN
  prior_effect_receipt_ref: string|null
```

Desktop metadata只能作 **parent-compatible overlay / current task metadata projection**：

```yaml
desktop:
  desktop_session_id: string
  target_host: string
  application_id: string
  application_version: string
  process_identity: string|null
  window_identity: string|null
  writer_profile_id: string
  provider_identity_ref: string
  capability_matrix_digest: sha256
  desktop_state_digest: sha256|null
  checkpoint_ref: string|null
```

如果 current schema不允許 namespaced extension，使用 current authorized Kanban/ExecutionBinding metadata extension point；**不得為此 fork schema**。

### FDA action replay table

| Action class | Parent side-effect class | Replay policy | Mandatory pre-replay proof |
|---|---|---|---|
| capture / inspect / read UI | `NONE` | `SAFE_REPLAY` | target identity still exact |
| focus/open known window | `LOCAL_REVERSIBLE` | `READBACK_BEFORE_RETRY` | window/process state |
| create/import script | `LOCAL_REVERSIBLE` | `READBACK_BEFORE_RETRY` | script name/digest/current editor state |
| set XQ PAPER parameter | `LOCAL_REVERSIBLE` | `READBACK_BEFORE_RETRY` | current parameter value |
| compile script | `LOCAL_REVERSIBLE` | `READBACK_BEFORE_RETRY` | script digest + prior compile result |
| start/stop PAPER runtime | `LOCAL_REVERSIBLE` | `READBACK_BEFORE_RETRY` | current runtime state |
| export file/log | `LOCAL_REVERSIBLE` | `READBACK_BEFORE_RETRY` | prior output path/digest / duplicate policy |
| credential/MFA/permission approval | `EXTERNAL_APPROVAL_GATED` | `FORBIDDEN` for FDA automation | HumanGate only |
| current live broker side effect | `EXTERNAL_APPROVAL_GATED` | `FORBIDDEN` in FDA v1 | separate SQS authorization required |

### Stable idempotency key

Minimum semantic：

```text
hash(
  workorder_id
  + task_id
  + application_id
  + application_version
  + action_class
  + target_artifact_digest_or_target_identity
)
```

相同 logical action的 retry/reclaim 必須沿用 stable key，並查 `prior_effect_receipt_ref`。

### Reclaim / retry hard rule

```text
worker lost
→ read prior effect receipt
→ read current desktop/app state
→ classify side effect
→ apply replay_policy
```

禁止：

```text
worker_exit_unknown
→ blindly rerun click/type/start/export
```

### Consequential ambiguity

如果無法判斷 action 是否已生效：

```text
side_effect_state = UNKNOWN
→ replay = FORBIDDEN
→ provider failover = FORBIDDEN
→ BLOCKED_HITL / INCIDENT
```

One-writer只解決 concurrency，不取代 idempotency。

## 5.7 Deterministic Provider Router

### Route inputs

```text
consumer_stack
application_id
application_version
action_class
risk_class
permission_class
provider_certification_matrix
known_failure_signature
desktop_state_confidence
current_lease
```

### Route output

```text
CUA
UFO2
HITL
BLOCKED
```

### Directly usable reference implementation

```python
from dataclasses import dataclass
from typing import Literal

Provider = Literal["CUA", "UFO2", "HITL", "BLOCKED"]

@dataclass(frozen=True)
class Request:
    app: str
    app_version: str
    action_class: str
    risk_class: str
    requires_secret: bool
    financial_side_effect: bool
    active_position_policy_mutation: bool

def route(req: Request, matrix: dict) -> Provider:
    # Hard denials outrank capability.
    if req.requires_secret:
        return "HITL"
    if req.financial_side_effect:
        return "HITL"
    if req.active_position_policy_mutation:
        return "BLOCKED"

    key = (req.app, req.app_version, req.action_class)
    certified = matrix.get(key, {})

    # Deterministic policy — not LLM preference.
    if certified.get("cua") == "PASS":
        return "CUA"
    if certified.get("ufo2") == "PASS":
        return "UFO2"

    return "BLOCKED"
```

### Failover rule

```python
def failover(primary: Provider, outcome: str, alternate_certified: bool) -> Provider:
    if outcome == "PASS":
        return primary
    if outcome not in {"DETECTED_FAIL", "SAFE_HALT"}:
        # Ambiguous / wrong-effect state is never auto-failed-over.
        return "BLOCKED"
    if not alternate_certified:
        return "BLOCKED"
    return "UFO2" if primary == "CUA" else "CUA"
```

**禁止：**
```text
silent fallback
random provider choice
"LLM thinks UFO might be better"
retry after ambiguous side effect
```

---

## 5.8 Hot-swap protocol

```text
PRIMARY PROFILE
  ↓
ACTION START
  ↓
READBACK
  ├─ PASS
  │   → checkpoint
  │   → continue same provider
  │
  └─ DETECTED_FAIL / SAFE_HALT
      → no further write
      → readback desktop state
      → rollback/restore if required
      → checkpoint
      → release writer lease
      → deterministic alternate-provider eligibility
      → acquire alternate lease
      → observe current state
      → execute
```

### Never hot-swap when

```text
state = UNKNOWN
side_effect = POSSIBLY_APPLIED_BUT_UNVERIFIED
credential_dialog = PRESENT
permission_dialog = PRESENT
live_financial_effect = POSSIBLE
writer_lease = UNCLEAR
```

→ `BLOCKED_HITL / INCIDENT`.

---

## 5.8A Ordinary-user / No-brain FDA Interaction Contract

普通使用者不需要知道或手動選：

```text
fabric-desktop-cua
fabric-desktop-ufo2
Capability Matrix row
Kanban card
ExecutionBinding ID
ContextForge registration
OASF/A2A/MCP route
```

Normal UX：

```text
User goal + target app + explicit constraints
→ HGK admission/current task contract
→ current Change/Risk/Capability route
→ WorkOrder
→ deterministic FDA provider route
→ Hermes execution
→ result / blocking HumanGate only when needed
```

只問真正 blocking 的人類事項，例如：

```text
login/MFA
permission explicitly reserved to user
ambiguous consequential state
future authorized entry HumanGate
```

Tool/provider失效：

```text
runtime performs qualified degrade/failover
or
returns one actionable BLOCKED_HITL reason
```

不得要求普通使用者自己決定「請換 UFO²」「請開另一個 Kanban」「請改 MCP route」。

## 5.9 Collaboration modes

### Mode A — Fast path

```text
WorkOrder
→ Hermes Kanban
→ fabric-desktop-cua
→ readback
→ PASS
```

### Mode B — Specialist path

```text
action_class certified complex
→ fabric-desktop-ufo2
→ local AppAgent/HostAgent micro-plan
→ readback
```

### Mode C — Sequential failover

```text
Cua DETECTED_FAIL
→ checkpoint
→ UFO²
```

### Mode D — Shadow verification（selective）

```text
writer = Cua
observer = UFO² READ_ONLY
```

or reverse.

Use only for high-value non-side-effect fixtures or acceptance; **not every click**。

### Swarm

```text
NORMAL_DESKTOP_WRITE = DIRECT/SEQUENTIAL
SWARM = NOT_DEFAULT
```

Read-only analysis may use parallelism; same desktop write path may not.

---

## 5.10 Hermes Kanban integration

Kanban card granularity：

**Good**
```text
Deploy and compile XS candidate
Configure XQ PAPER strategy
Collect Log Viewer/export evidence
```

**Bad**
```text
click tab
press Ctrl+A
paste text
click button
```

Micro-actions stay insideProfile execution.

### Example macro DAG

```yaml
tasks:
  - id: FDA-XQ-001
    goal: Locate and health-check current XQ desktop
    profile: fabric-desktop-cua

  - id: FDA-XQ-002
    depends_on: [FDA-XQ-001]
    goal: Deploy validated XScript candidate
    profile: AUTO_ROUTE_WINDOWS_DESKTOP_AUTOMATION

  - id: FDA-XQ-003
    depends_on: [FDA-XQ-002]
    goal: Compile and classify result
    profile: AUTO_ROUTE_WINDOWS_DESKTOP_AUTOMATION

  - id: FDA-XQ-004
    depends_on: [FDA-XQ-003]
    goal: Configure PAPER fixture and collect readback
    profile: AUTO_ROUTE_WINDOWS_DESKTOP_AUTOMATION
```

`AUTO_ROUTE_*`是概念標籤；實作時必須映射current HGK/Hermes合法route，不能把它當新的Hermes profile name。

---

## 5.11 OpenSpec integration

### Trigger

```text
FDA durable infrastructure change
```

例如：
- add/remove provider；
- change profile permissions；
- change routing policy；
- change knowledge ACL/namespace；
- change desktop lease invariant；
- major XQ automation contract。

### Flow

```text
Finding / Change Intent
→ Fabric Change Router
→ OpenSpec propose/change artifacts (if current route selects OpenSpec)
→ HGK Requirement / TaskSpec / WorkOrder
→ Codex tracked implementation
→ tests
→ independent Acceptance Officer
→ Fabric promotion/rollback
```

### Do NOT invoke OpenSpec for

```text
ordinary XQ deploy
ordinary compile
ordinary readback
routine provider retry
```

---

## 5.12 gstack methodology integration

| Situation | gstack method | Authority ceiling |
|---|---|---|
| Provider behavior defect | `/investigate` | method only |
| Routing/profile code change | `/review` | review support |
| XQ fixture execution | `/qa` | test methodology |
| credential/MCP/screen leakage audit | `/cso` | security methodology |
| recurring Cua→UFO failover | `/retro` | learning/evolution candidate |
| architecture-changing FDA patch | `/plan-eng-review` | planning support |

Rules：

```text
gstack role/method ≠ WorkOrder authority
gstack /spec ≠ Fabric normative spec owner
gstack /ship ≠ Fabric release/promotion authority
```

---

## 5.13 ContextForge / MCP integration

### Recommended

```text
Control / registry:
Fabric + current ContextForge/OASF where admitted

Runtime:
Hermes → local stdio/in-process provider

Evidence:
provider identity/version/config/permission/action/readback
→ Fabric/HGK evidence
```

### Not recommended

```text
Hermes
→ remote HTTP gateway
→ every mouse click
```

Rationale：same-host desktop control不需要增加network hop、latency、gateway failure surface。

### Network boundary

```text
LOCAL_ONLY = default
preferred_transport = stdio / in-process
localhost/named-pipe = conditional
0.0.0.0 / LAN-exposed desktop control = DENY unless a separate security change is explicitly admitted
```

---

## 5.13A FDA Interoperability Promotion Contract — OASF / ContextForge / MCP / A2A / OTel

FDA shared infrastructure要能被 HGK/SQS **discover/consume**，但不把 registry/gateway 放進每個 click 的 runtime data path。

### Same-subject promotion lineage

若 current CF1/F1 interop contract仍為 active current route，FDA Profile/Team promotion必須形成同一 candidate/subject lineage：

```text
Profile Distribution digest(s)
→ FDA Team artifact digest
→ FDA Desktop Capability Matrix digest
→ OASF Record digest
→ ContextForge registration target digest
→ ContextForge auth-policy digest
→ explicit MCP disposition
→ explicit A2A disposition
→ SubjectAttestation digest
→ EvidenceManifest digest
→ current PromotionTransaction
```

若 current post-RP002 successor已取代上述 artifact名稱，採其 current same-authority equivalent；**不得省略 same-subject identity closure**。

### OASF

```text
role = interoperability description/schema
authority = NONE
must describe:
  capability
  profile/distribution identity
  endpoint/locator
  permission/transport metadata
  lifecycle/version
```

OASF record不能取代 FDA Capability Matrix、WorkOrder、Fabric authority。

### ContextForge

```text
role = registry/gateway/discovery where current route selects it
runtime_every_click_required = false
```

Required promotion checks when applicable：

```text
register exact promoted FDA profile/capability
discover from allowed consumer
deny from disallowed consumer
invoke/read bounded canary if current route uses gateway
disable/unregister/rollback
stale previous distribution registration = 0
```

### MCP

```text
Cua local provider:
  preferred = stdio / in-process current qualified route

UFO²:
  local/in-process or current admitted transport

unbound MCP:
  explicit N/A
```

No silent network enablement.

### A2A

```text
same-host FDA Profile coordination:
  preferred = Hermes Kanban / current local route

A2A:
  REQUIRED_WHEN_ROUTED
  not mandatory for every local desktop action
  explicit N/A if no actual FDA route uses it
```

若 A2A 被選作跨runtime/cross-stack interface：

```text
exact identity
auth-negative
invoke/readback
disable/rollback
```

皆須 qualification。

### OpenTelemetry

FDA繼承 parent：

```text
OpenTelemetry = CONDITIONAL_EMBEDDED
```

若 current qualified telemetry/exporter存在：

```text
correlate:
  workorder_id
  execution_binding_id
  run_id
  profile_id
  provider
  application
  action_class
  result
```

且不得輸出secret/screenshot sensitive payload。

若不存在：

```text
OTEL = EXPLICIT_N_A_OR_DEFER
standalone FDA telemetry platform = NO_ADOPT_P0
```

### Runtime path remains thin

```text
HGK WorkOrder
→ Hermes
→ local FDA Profile/provider
→ desktop
```

ContextForge/OASF/A2A/OTel是 interoperable identity/governance/trace surfaces，**不是新增 desktop scheduler 或 click proxy**。

## 5.14 Knowledge / Memory / RAG integration

### Existing RP-002 invariant

```text
central governance
shared substrate
distributed domain production
derived knowledge != authority
```

Master namespace baseline includes：

```text
hgk.candidate.*
hgk.approved.*
hgk.revoked.*

sqs.candidate.*
sqs.approved.*
sqs.revoked.*

fabric.*
assurance.*
shared.approved.*
```

fileciteturn18file5

### FDA namespace proposal

Only if current KG1 namespace schema allows owner-scoped subnamespaces or a governed extension is approved：

```text
fabric.desktop.candidate.*
fabric.desktop.approved.*
fabric.desktop.revoked.*
```

If current schema does **not** support this exact split：

```text
CR_OPEN-FDA-KG-001
→ use current canonical fabric namespace semantics
→ do not create a second database/RAG
```

### Read permissions

FDA common：

```text
fabric.desktop.approved.*
shared.approved.*
```

Consumer-bound, only per WorkOrder：

```text
sqs.approved.xq.*       # only if current SQS KG schema/ACL has an owner-approved equivalent
hgk.approved.tooling.*  # only if current schema has an equivalent
```

Exact namespace names beyond Master baseline are **PROPOSED/UNVERIFIED until current KG1 readback**。

### Write permissions

```text
Cua/UFO observations
→ candidate only
→ provenance + provider + app/version + action class + result
→ owner/acceptance promotion
```

### UFO² native Knowledge Substrate

Allowed：

```text
approved help docs
approved local application knowledge
approved prior execution patterns
WorkOrder-scoped task context
```

Default deny in SQS/XQ desktop profile：

```text
unrestricted Bing/web search
full SQS Financial Truth browsing
credentials
account secrets
private Hermes profile memory
```

UFO native experience may remain ephemeral/local cache, but anything intended for cross-profile reuse must enter Fabric candidate/promotion path.

---

## 5.15 Permission model

### Shared Team permission ceiling

| Permission | Cua Profile | UFO² Profile |
|---|---|---|
| inspect target app/window | ALLOW | ALLOW |
| capture target app only | ALLOW | ALLOW |
| UIA/Win32/visual observation | ALLOW if provider supports | ALLOW |
| click/type within admitted target | ALLOW bounded | ALLOW bounded |
| unrelated desktop app | DENY unless WorkOrder binds it | DENY |
| password/MFA entry | DENY | DENY |
| read secret vault | DENY | DENY |
| permission/UAC approval | DENY/HITL | DENY/HITL |
| Fabric policy mutation | DENY | DENY |
| WorkOrder creation | DENY | DENY |
| self-promotion | DENY | DENY |
| self-acceptance | DENY | DENY |
| current SQS live broker write | DENY | DENY |
| mutate frozen active-position trading policy | DENY | DENY |

### Cua provider

Use current upstream `bounded` permission capability when exact local version proves it; do not use unrestricted/yolo for FDA governed runtime.

### UFO² provider

Scope HostAgent/AppAgent to WorkOrder-local desktop task. External web/network MCP disabled by default for financial desktop work unless current WorkOrder explicitly admits it.

---

## 5.16 XQ/XS consumer binding

### Current FDA P0 scope

```text
LOCAL / PAPER / SHADOW / NO-LIVE-WRITE
```

Allowed target actions after qualification：

```text
launch/focus XQ
open XS Editor
create/import validated script
compile
read compile result/error
configure PAPER strategy/radar
configure symbols/parameters
start/stop PAPER runtime
read Log Viewer/status
export/readback
```

Current forbidden：

```text
credentials/MFA
broker account authority mutation
live entry approval automation
autonomous broker write
AI active-position trading decision
```

### XQ readback hierarchy

```text
1. XQ native/file/log output
2. structured UIA/Win32 readback
3. visual grounding
4. pixel/coordinate fallback
```

Screenshots/UI are **consistency evidence**, not Financial Truth.

### Future SQS semi-auto live compatibility

FDA can be designed so a later separately authorized SQS ChangeSet may bind：

```text
Human Entry Arm
→ frozen XScript mechanically manages position lifecycle
```

But **FDA v1 must not authorize this**. Current RP-002/SQS claim remains live-trading NOT_AUTHORIZED.fileciteturn18file7

---

## 5.16A Deferred SQS/XQ Semi-Auto Consumer Safety Contract（保留設計，不授權 live）

本節保留 FDA討論-3 的完整 consumer safety design，防止 future implementation agent把「Desktop Automation」誤升格為 active-position AI execution。

**Current runtime authority remains：**

```text
SQS_LIVE_TRADING = NOT_AUTHORIZED
FDA_V1 = LOCAL / PAPER / SHADOW / NO-LIVE-WRITE
```

因此本節是：

```text
DEFERRED_COMPATIBILITY_CONTRACT
!= CURRENT_LIVE_PERMISSION
```

### Phase boundary

```text
PRE_POSITION
  FDA eligible:
    deploy validated XScript
    compile
    configure approved XQ/PAPER settings
    readback
    prepare arm surface

ENTRY
  HUMAN_ENTRY_APPROVAL
  FDA/Hermes cannot approve on user's behalf

ACTIVE_POSITION
  owner = exact frozen XScript execution policy
  Hermes = NOT_IN_DECISION_LOOP
  Cua = NOT_IN_DECISION_LOOP
  UFO² = NOT_IN_DECISION_LOOP
  Codex = NOT_IN_DECISION_LOOP

POST_POSITION
  FDA/SQS eligible:
    readback
    export/log
    reconciliation
    journal/repair for next candidate
```

### Human Entry Approval must bind

未來若 SQS authority正式批准 semi-auto live，entry HumanGate至少必須綁：

```text
script_digest
FinancialSpec / approved scenario ref
RiskAuthorization ref
instrument / symbol
side
account_profile_ref (non-secret identity only)
session_id / validity interval
max_initial_size
max_total_size
risk ceiling
allowed scale-in / scale-out / stop / take-profit / flatten policy refs
```

Human確認語義：

```text
approve exact frozen execution policy for this bounded position lifecycle
```

不是批准 LLM 在position中自由決策。

### Frozen script invariant

```text
script_digest_at_arm == script_digest_during_position
```

任何 drift：

```text
ARM_INVALIDATED
NO HOT PATCH TO ACTIVE POSITION
```

新script只可用於下一個 position lifecycle。

Emergency safety path：

```text
EMERGENCY_KILL / FLATTEN
```

必須是獨立安全權限，不等於允許AI修改交易邏輯。

### Position independence invariant

活躍position的 deterministic risk-management safety不得依賴：

```text
Hermes availability
Cua availability
UFO² availability
LLM availability
Codex availability
MCP availability
```

### PAPER Position Independence Canary

在 future semi-auto compatibility claim前，必須於不涉及真實 broker write 的 PAPER/simulation subject驗：

```text
validated/frozen XScript
→ Human-equivalent test arm or simulation trigger
→ position-active simulation
→ deliberately stop Hermes
→ stop Cua
→ stop UFO² if present
→ XScript remains able to execute its scripted scale/stop/take-profit/flatten lifecycle
→ restart operator plane
→ readback/reconcile
```

若 current XQ PAPER fixture無法安全形成此canary：

```text
FDA_XQ_SEMIAUTO_COMPATIBILITY = UNVERIFIED
```

但不阻擋純 `FDA_PROFILE_TEAM_ACTIVE`（desktop infrastructure P0）；它只阻擋未來 semi-auto compatibility claim。

### Post-position truth

```text
XQ UI screenshot != Financial Truth
```

Post-position flow：

```text
authorized XQ/broker facts / file-log output
→ SQS validation
→ execution reconciliation
→ position/cash/PnL/journal truth per SQS authority
```

### Separate authorization

任何：

```text
live broker write
entry arm in real account
semi-auto production enablement
```

必須由**獨立 SQS ChangeSet / domain authority / risk / acceptance**授權。

FDA不得透過Profile permission偷偷打開 live write。

## 5.17 Event Matrix

| Event | Router / Owner | Action | Evidence | Escalation |
|---|---|---|---|---|
| ordinary stable desktop action | Hermes/FDA router | Cua | before/after/readback | none |
| certified complex workflow | Hermes/FDA router | UFO² | local plan + readback | none |
| Cua detected failure | Hermes | bounded retry → checkpoint → UFO if certified | failure signature + state | if repeated → GE |
| UFO detected failure | Hermes | checkpoint → Cua only if action certified | failure signature | otherwise BLOCK |
| ambiguous side effect | HGK/Fabric | STOP | state unknown receipt | HITL |
| second writer tries same session | Fabric permission | DENY | lease conflict | incident |
| login/password/MFA | HumanGate | BLOCK agent, user handles | no secret log | resume after readback |
| UAC/permission dialog | HumanGate | STOP | dialog class only | HITL |
| XQ version drift | FDA qualification | block affected action classes | version diff | requalify |
| selector/control drift | FDA | investigate; alternate if certified | failure signature | HGK repair |
| repeated same primary defect | Fabric evolution | OpenSpec/gstack investigate → HGK/Codex | candidate | Acceptance |
| Knowledge unavailable | FDA | WorkOrder explicit inputs only; no guessing | degraded receipt | block if required knowledge |
| ContextForge unavailable | FDA local runtime | continue local only if current route permits | registry/degrade receipt | no click path dependency |
| provider security advisory | Fabric tool lifecycle | quarantine/pin/rollback | advisory+version | requalify |
| no provider fits action | HGK | BLOCKED_HITL | no-fit receipt | capability evolution |
| current live financial side effect | SQS owner/Fabric | DENY | policy violation prevented | separate ChangeSet required |

---

## 5.18 Degrade Matrix

| Failure | Allowed degrade | Forbidden degrade | Final state |
|---|---|---|---|
| Cua unavailable | qualified UFO² | unqualified silent provider | DEGRADED_PROVIDER |
| UFO² unavailable | Cua only for Cua-certified action | random pixel macro | DEGRADED_PROVIDER |
| both providers unavailable | HUMAN fallback if task allows | fake PASS | BLOCKED_HITL |
| UIA unavailable | UFO visual/hybrid only if certified | blind coordinates | DEGRADED_VISUAL |
| target state unknown | HITL/restore | provider failover with unknown state | BLOCKED |
| Kanban unavailable on durable multi-step FDA task | repair Kanban / controlled checkpoint | new FDA queue DB | BLOCKED_PLATFORM |
| ContextForge unavailable | local direct provider if registry not in data path and current binding is known | unregistered new endpoint | DEGRADED_INTEROP |
| shared Knowledge unavailable | explicit WorkOrder inputs / approved local cache with provenance if current policy permits | provider free web search | DEGRADED_KNOWLEDGE |
| XQ new version | previous known-good version if rights/install policy permits; otherwise requalify | assume selectors compatible | BLOCKED_VERSION_DRIFT |
| OpenSpec unavailable for durable FDA change | current HGK legal change route | direct uncontrolled schema mutation | BLOCKED_CHANGE |
| gstack unavailable | continue base engineering method | block normal runtime solely for methodology donor | N/A_SUPPORT |
| Acceptance Officer unavailable | retain candidate only | self-promote | BLOCKED_PROMOTION |

---

## 5.18A HumanGate vs BreakGlass — governed bypass semantics

FDA需明確區分：

```text
NORMAL HUMAN ACTION
!=
BREAKGLASS
```

### Normal HumanGate / operator action

下列本身**不是 BreakGlass**：

```text
login/password/MFA handled by user
permission/UAC handled by authorized human where policy permits
future SQS Human Entry Approval
ordinary manual action when the admitted task is explicitly HUMAN-assigned
```

### BreakGlass trigger

在 post-F1 normal path：

```text
WorkOrder
→ ExecutionBinding
→ Profile
→ Kanban/Hermes
```

已被要求的 admitted machine task若**繞過 FDA governed Profile route**，例如：

```text
both providers fail
→ operator uses otherwise-forbidden legacy automation/direct machine path

or

emergency operator bypasses current FDA control to recover target state
```

必須走 current：

```text
RP002-BREAK-GLASS/1
```

或 same-authority successor。

### Required receipt

```yaml
break_glass_receipt:
  schema: RP002-BREAK-GLASS/1
  reason: <required>
  operator: <required>
  authority_ref: <required>
  subject_digest: <required>
  started_at: <required>
  expires_at: <required>
  affected_scope: <required>
  bypassed_control: <required>
  restoration_plan: <required>
  evidence_refs: []
  post_event_review: REQUIRED
  closure_receipt: <required-before-final>
```

### Rules

```text
legacy/direct bypass without BreakGlassReceipt = FAIL
BreakGlass without expiry/restoration = FAIL
BreakGlass cannot grant Financial Truth authority
BreakGlass cannot grant acceptance authority
BreakGlass cannot self-promote provider/profile
open BreakGlass > 0 = FDA promotion/release BLOCKED
closed BreakGlass requires restoration readback + post-event review
```

BreakGlass是治理例外，不是normal fallback provider。

## 5.19 Evidence model — minimal, not ceremony-heavy

Daily FDA execution receipt：

```json
{
  "workorder_id": "...",
  "execution_binding_ref": "...",
  "profile_id": "fabric-desktop-cua",
  "provider": {
    "name": "cua-driver",
    "version": "...",
    "digest_or_identity": "..."
  },
  "desktop_session_id": "...",
  "application": {
    "name": "XQ",
    "version": "..."
  },
  "action_class": "XS_COMPILE",
  "permission_profile_digest": "...",
  "before_state_ref": "...",
  "result": "PASS|SAFE_HALT|DETECTED_FAIL|BLOCKED",
  "after_state_ref": "...",
  "side_effect_class": "NONE|LOCAL_REVERSIBLE|EXTERNAL_APPROVAL_GATED",
  "fallback_used": false,
  "evolution_signal": null
}
```

**不要**每次desktop task生成大型ZIP/Final Evidence package。只有Profile/Provider promotion、milestone audit或distribution release才走完整Fabric acceptance/promotion package。

---

# 6. 工程落地計畫（Implementation & Test）

## 6.1 Implementation strategy

```text
DO NOT reopen RP-002 Stage-1/2/3
DO NOT invent RP002 gate
DO NOT create third Heavy Stack
DO NOT create FDA scheduler/task DB/RAG/reducer
DO NOT bulk install extra GUI-agent frameworks

Perform:
current readback
→ current durable-entry Prompt Compiler C0-C9 + deterministic lint = PROMPT_COMPILE_PASS
→ current Change Router classification
→ shared-infrastructure schema resolution
→ smallest legal Fabric Profile/Capability extension
→ canonical Team + FDA Desktop Capability Matrix
→ Cua/UFO profile distributions
→ parent ExecutionBinding/2 + lease + idempotency binding
→ OASF/ContextForge/MCP/A2A/OTel disposition
→ Hermes binding
→ XQ PAPER fixtures
→ one-writer/failover/idempotency/BreakGlass/security/knowledge tests
→ independent Acceptance
→ promotion
```

### Change class

Expected design intent：

```text
PROFILE/CAPABILITY governed evolution
```

The exact current enum/string (例如歷史討論中的`PROFILE_CHANGE`) is **UNVERIFIED** until `RP002_CHANGE_CLASS_ROUTER.yaml` fresh readback. Do not hard-code the historical spelling.

### Durable FDA ChangeSet entry — Prompt Compiler is REQUIRED

FDA是 durable post-RP-002 ChangeSet，因此施工前必須：

```text
resolve current construction-acceptance-prompt-compiler
(or source-authorized same-rank successor)
→ C0 source scan
→ C1 intent
→ C2 authority
→ C3 changeset
→ C4 execution scope
→ C5 runtime readiness
→ C6 user journey
→ C7 acceptance
→ C8 evidence/claim
→ C9 termination/resume
→ deterministic lint
→ PROMPT_COMPILE_PASS
```

只有當**較新的同權威 machine policy 明確 supersede**此 requirement，才能使用其 replacement；不能用自然語言推理自行宣告「不需要compiler」。

```text
compiler unavailable
and
no source-authorized equivalent control
→ BLOCKED_COMPILER_OR_EQUIVALENT_CONTROL_REQUIRED
→ mutation denied
```


---

## 6.2 Proposed change paths

> `ADD` paths below are **target design paths under existing canonical families**. Before creation, inspect current repo layout and reuse current naming/schema. Duplicate artifact = FAIL.

| Path / family | Change | Purpose | Risk |
|---|---|---|---|
| `Fabric\profiles\...` current profile convention | ADD two profile distributions | Cua/UFO² runtime isolation | High |
| current Fabric team/profile manifest location | EXTEND canonical only | register `fabric-desktop-automation` | Critical |
| `RP002_PROFILE_TEAM_MANIFEST.yaml` | EXTEND only if current post-RP002 machine truth uses it for new shared profiles | one profile truth | Critical |
| `RP002_TOOL_AND_INHERITED_CAPABILITY_MATRIX.yaml` or post-RP002 successor | ADD provider rows/states | Cua/UFO exact state/rollback | High |
| `Fabric\control\CAPABILITY_QUALIFICATION_POLICY.yaml` | MIN_PATCH only if current policy lacks desktop action-class qualification | provider admission | High |
| `Fabric\control\PROFILE_STACK_REGISTRATION_POLICY.yaml` | MIN_PATCH only if shared-infra class cannot be expressed | team/profile admission | High |
| `Fabric\control\SOD_POLICY.yaml` | MIN_PATCH | one writer / no self-accept / authority ceiling | Critical |
| `Fabric\control\KNOWLEDGE_POLICY.yaml` | MIN_PATCH only if needed | desktop candidate/approved ACL | High |
| current HGK router/binding registry | MIN_PATCH | `WINDOWS_DESKTOP_AUTOMATION` deterministic route | Critical |
| current Hermes profile distributions | ADD via existing distribution tooling | actual `fabric-desktop-cua/ufo2` load | High |
| `Fabric\assurance\acceptance-packs\...` | ADD FDA pack under current convention | independent acceptance | High |
| SQS XQ adapter/binding current owner path | MIN consumer binding | `XQ_DESKTOP_CONTROL` → FDA | Critical domain boundary |
| current FDA Team artifact (`TEAM.md` or exact current equivalent) | ADD/EXTEND_CANONICAL | team/profile/capability/assignee/router/interop binding | Critical |
| current FDA machine artifact family | ADD `FDA_DESKTOP_CAPABILITY_MATRIX` additive view | action-class qualification/routing truth | Critical |
| current ExecutionBinding/2 instance/metadata | REUSE + PARENT-COMPAT OVERLAY | lease/idempotency/replay/desktop identity | Critical |
| current OASF/ContextForge promotion artifacts | EXTEND_IF_CURRENT_ROUTE_ACTIVE | same-subject discovery/interoperability | High |
| current BreakGlass control/receipt path | REUSE | governed bypass only | Critical |
| current Prompt Compiler | REQUIRED_PRE_MUTATION | C0-C9 durable-entry qualification | Critical |
| Fabric/HGK/SQS User Guides/AGENTS | PATCH after promotion | current operability | Low |
| current knowledge governance/index | EXTEND only if schema allows | FDA knowledge namespace | High |

---

## 6.3 FDA implementation checkpoints

> **這些是本FDA ChangeSet內的 qualification checkpoints，不是新的 RP-002 Gate IDs，不得寫入 `RP002_GATE_CATALOG.yaml`。**

### FDA-C0 — Authority / Current-State Readback

Must prove：
- RP-002 final accepted baseline current and not reopened；
- exact current `RP002_PROFILE_TEAM_MANIFEST`/successor；
- exact Change Router；
- exact ExecutionBinding schema；
- current Fabric policies；
- current Hermes bound executable/version；
- current Cua state；
- current UFO² state；
- current XQ executable/version；
- current SQS XQ adapter/live claim ceiling；
- current Prompt Compiler identity/digest and `PROMPT_COMPILE_PASS`；
- current parent tool/capability matrix complete denominator；
- current Team/TEAM materialization convention；
- current OASF/ContextForge/MCP/A2A/OTel route/disposition；
- current BreakGlass policy identity。

**PASS**
```text
critical_source_missing = 0
same_rank_conflict = 0
prompt_compile_pass = true
parent_tool_rows_missing = 0
current subject digests bound
```

**FAIL**
→ `CR_OPEN / STOP MUTATION`.

---

### FDA-C1 — Shared Infrastructure Team / Profile Contract

Materialize via current schema：

```text
fabric-desktop-automation
fabric-desktop-cua
fabric-desktop-ufo2
```

Validate full existing Profile Runtime Contract fields：
distribution/version/full commit/package digest、SOUL/config/skills/MCP、permissions、I/O、fixtures、rollback。

**PASS**
```text
third_heavy_stack_created = 0
second_scheduler = 0
second_task_db = 0
schema_fork = 0
profile_effective_load positive = PASS
negative permission fixture = PASS
team_materialization = PASS
capability_matrix_schema_owner_versioning = PASS
parent_tool_matrix_additive_preservation = PASS
```

---

### FDA-C2 — Cua Qualification

Run exact current bound Hermes：

```powershell
# Read-only preflight; current local command surface must exist.
hermes computer-use status
```

If current Hermes provides doctor on the bound version, run it after command discovery; do not assume command solely from upstream main.

Qualify：
- install/source/version/digest；
- Windows UIA/capture/input；
- bounded permission；
- process lifecycle；
- target-app capture only；
- positive/negative fixtures；
- fail/rollback；
- wrapper/provider compatibility；
- independent checker。

**PASS**
→ profile state `QUALIFIED_CANDIDATE`.

---

### FDA-C3 — UFO² Qualification

Resolve：
- exact upstream/local version/commit；
- license/security advisories；
- local-only transport；
- Host/AppAgent scope；
- LLM/model provider route；
- UIA/Win32/visual/hybrid capability；
- knowledge external search OFF for XQ；
- positive/negative fixtures；
- rollback/uninstall/disable；
- independent checker。

**PASS**
→ `QUALIFIED_CANDIDATE`.

UFO² does **not** need to be always-on; default lifecycle `ON_DEMAND`.

---

### FDA-C4 — XQ PAPER Fixture Matrix

Current XQ version exact readback.

Mandatory fixtures：

```text
F01 launch/locate XQ
F02 identify exact target window/process
F03 open XS Editor
F04 locate known script
F05 create/import fixture script
F06 compile known-pass fixture
F07 compile known-fail fixture
F08 extract exact compile error
F09 configure PAPER/radar fixture
F10 read current runtime/status/Log Viewer
F11 export/file readback
F12 stop PAPER runtime / restore known state
```

Each provider：
- first qualification run: 10 fresh runs per applicable fixture；
- any `WRONG_ACTION` or silent side effect = profile/action-class FAIL；
- detected safe fail may simply mean the provider is not certified for that class；
- an action class is team-certified only if **at least one provider** passes 10/10 fresh runs with full readback and zero wrong action.

No real live broker action.

---

### FDA-C5 — Router / Lease / Hot-Swap

Test：

```text
Cua PASS
Cua safe fail → UFO transfer
UFO safe fail → Cua transfer if certified
unknown state → BLOCK (no transfer)
two writers collision → second denied
worker dies → lease recovery
XQ restart → state rebind
worker dies after possible local effect → prior-effect readback before replay
same idempotency key → no duplicated side effect
```

**PASS**
```text
simultaneous_writer_count = 0
silent_provider_fallback = 0
unknown_state_retry = 0
lease_transfer_without_checkpoint = 0
duplicate_side_effect_on_retry = 0
idempotency_contract = PASS
```

---

### FDA-C6 — Knowledge / Security / SoD

Positive：
- FDA reads approved desktop knowledge；
- WorkOrder-scoped SQS input supplied；
- provider writes candidate experience；
- owner promotion path exists。

Negative：
- Cua/UFO cannot read credentials；
- UFO web search blocked for XQ execution profile；
- cannot mutate Fabric policy；
- cannot create WorkOrder；
- cannot self-accept/promote；
- cannot modify SQS Financial Truth/risk；
- local MCP not listening on unauthorized network interfaces；
- current live broker write remains denied；
- BreakGlass bypass requires canonical receipt；
- open BreakGlass blocks promotion；
- OASF/ContextForge/MCP/A2A current route cannot create second authority；
- parent OpenTelemetry disposition preserved；
- all 9 FDA-specific selection rows + WinAppDriver dependency row have explicit disposition。

**PASS**
```text
secret_exposure = 0
authority_escape = 0
self_promotion = 0
unauthorized_network_control = 0
live_broker_write = 0
open_breakglass = 0
fda_tool_selection_missing_rows = 0
interop_subject_drift = 0
```

---

### FDA-C7 — Independent Acceptance / Promotion / Operability

Acceptance Officer fresh session verifies：
- exact candidate subject；
- C0–C6 evidence；
- capability/action matrix；
- provider versions/digests；
- rollback；
- consumer binding；
- docs currentness；
- no hidden claim expansion；
- Team artifact / Capability Matrix same-subject binding；
- ExecutionBinding idempotency/replay；
- OASF/ContextForge/MCP/A2A disposition；
- BreakGlass open count = 0；
- parent tool rows preserved/additive only。

Promotion only after exact candidate acceptance.

After promotion update：
- Fabric User Guide；
- Fabric AGENTS；
- HGK Guide/AGENTS if current projection needs it；
- SQS Guide only for actual XQ consumer state；
- no stale “autonomous adapter absent” once truly promoted；
- keep live-trading claim ceiling explicit.

---

## 6.4 Minimal XQ qualification harness design

### Fixture manifest

```yaml
fixture_set: FDA-XQ-PAPER-V1
mode: PAPER_NO_LIVE_WRITE
target_app: XQ
version: RESOLVE_AT_RUNTIME
forbidden:
  - credentials
  - live_entry
  - broker_write
  - account_permission_change

fixtures:
  - id: XQ-LAUNCH
    expected: TARGET_WINDOW_IDENTIFIED
  - id: XS-COMPILE-PASS
    artifact: known_good_fixture.xs
    expected: COMPILE_PASS
  - id: XS-COMPILE-FAIL
    artifact: known_bad_fixture.xs
    expected: KNOWN_ERROR_CLASS
  - id: XQ-PAPER-CONFIG
    expected: PAPER_PROFILE_CONFIGURED
  - id: XQ-READBACK
    expected: LOG_OR_EXPORT_READBACK_MATCH
```

Exact XScript fixture contents must come from current XQ/XS authoritative corpus, not invented by FDA.

---

## 6.5 Read-only Windows current-state preflight script

```powershell
$ErrorActionPreference = "Stop"

Write-Host "== FDA current-state preflight =="

$hermes = Get-Command hermes -ErrorAction Stop
Write-Host ("Hermes: " + $hermes.Source)

& hermes version
& hermes computer-use status

$xq = Get-Process | Where-Object {
    $_.ProcessName -match 'XQ'
} | Select-Object ProcessName, Id, Path

if (-not $xq) {
    Write-Host "XQ process: NOT_RUNNING"
} else {
    $xq | Format-Table -AutoSize
}

Write-Host "No mutation performed."
```

This script only discovers state. XQ exact process name/version/path must be resolved during FDA-C0.

---

## 6.6 Provider failure/evolution pipeline

```text
provider failure
→ classify:
   transient | adapter | workflow | provider-upstream | OS | XQ-version | permission
→ bounded retry only if side-effect-safe
→ alternate provider if certified + state known
→ record failure signature
→ task continues if safely recovered
→ recurring/material defect emits Fabric evolution candidate
→ gstack /investigate methodology if useful
→ OpenSpec durable change if current router selects it
→ HGK WorkOrder
→ Codex tracked repair
→ focused tests + affected FDA regression
→ Acceptance Officer
→ promotion/rollback
```

Do not let fallback permanently hide repeated primary defects.

Suggested evolution trigger：

```text
same_failure_signature >= 3 in rolling 20 comparable runs
OR
any silent/wrong action
OR
security/authority violation
OR
provider no-fit blocks required consumer flow
```

`3/20` is an FDA proposed operational threshold, not existing RP-002 norm; current policy may choose another threshold during implementation.

---

## 6.7 Test Tracking List

| ID | Test | Type | Required |
|---|---|---|---|
| FDA-T001 | current authority/machine readback | source | YES |
| FDA-T002 | no third Heavy Stack | architecture negative | YES |
| FDA-T003 | no second scheduler/task DB/reducer/KG | architecture negative | YES |
| FDA-T004 | both Profiles validate current runtime schema | schema | YES |
| FDA-T005 | fresh-session effective-load Cua | runtime | YES |
| FDA-T006 | fresh-session effective-load UFO² | runtime | YES |
| FDA-T007 | Cua target-app-only permission | security | YES |
| FDA-T008 | UFO² bounded WorkOrder scope | security | YES |
| FDA-T009 | credentials/MFA denied | negative | YES |
| FDA-T010 | unauthorized network listener denied | negative | YES |
| FDA-T011 | XQ launch/window identity | positive | YES |
| FDA-T012 | XS known-good compile | positive | YES |
| FDA-T013 | XS known-bad compile/error readback | negative/positive | YES |
| FDA-T014 | XQ PAPER config | positive | YES |
| FDA-T015 | XQ log/export readback | positive | YES |
| FDA-T016 | one active desktop writer | concurrency | YES |
| FDA-T017 | Cua safe-fail → UFO failover | recovery | YES |
| FDA-T018 | unknown state prevents failover | fail-closed | YES |
| FDA-T019 | provider crash/worker reclaim | recovery | YES |
| FDA-T020 | XQ restart/rebind | recovery | YES |
| FDA-T021 | Knowledge approved-read | knowledge | YES |
| FDA-T022 | provider candidate-write only | knowledge negative | YES |
| FDA-T023 | self-promotion denied | SoD | YES |
| FDA-T024 | Acceptance Officer verify-only | SoD | YES |
| FDA-T025 | current SQS live broker write denied | financial negative | YES |
| FDA-T026 | docs/AGENTS current after promotion | operability | YES |
| FDA-T027 | rollback to prior provider/profile state | rollback | YES |
| FDA-T028 | Prompt Compiler C0-C9 + lint | durable entry | YES |
| FDA-T029 | FDA Team artifact full materialization | team/runtime | YES |
| FDA-T030 | canonical Desktop Capability Matrix owner/schema/version/rollback | routing truth | YES |
| FDA-T031 | parent tool matrix additive preservation | anti-downgrade | YES |
| FDA-T032 | all FDA exact-set tool dispositions present | anti-downgrade | YES |
| FDA-T033 | ExecutionBinding idempotency/replay | recovery | YES |
| FDA-T034 | prior-effect readback prevents duplicate local effect | idempotency negative | YES |
| FDA-T035 | OASF/ContextForge same-subject promotion | interop | YES if current route applicable; otherwise explicit N/A |
| FDA-T036 | MCP/A2A explicit route or explicit N/A | interop | YES |
| FDA-T037 | OpenTelemetry parent disposition preserved | telemetry anti-downgrade | YES |
| FDA-T038 | BreakGlass unauthorized bypass denied | governance negative | YES |
| FDA-T039 | open BreakGlass blocks promotion | governance negative | YES |
| FDA-T040 | deferred XQ semi-auto contract present / no hot-patch invariant | consumer safety contract | YES |
| FDA-T041 | PAPER position-independence canary | future compatibility | REQUIRED only for `FDA_XQ_SEMIAUTO_COMPATIBILITY_PROVEN`; otherwise explicit DEFERRED |


---

## 6.8 PASS / FAIL predicates

### Blueprint acceptance（this artifact）

```text
architecture_preserves_RP002 = PASS
two_heavy_stacks_preserved = PASS
no_second_control_plane = PASS
profile_team_design_complete = PASS
provider_modularity = PASS
kanban_reuse = PASS
openspec_boundary = PASS
gstack_boundary = PASS
knowledge_governance = PASS
xq_claim_ceiling = PASS
risk_register = COMPLETE
machine_blocks = PRESENT
shared_infra_schema_resolution_contract = PRESENT
team_materialization_contract = PRESENT
capability_matrix_canonical_artifact = PRESENT
parent_execution_binding_full_inheritance = PRESENT
idempotency_replay_contract = PRESENT
breakglass_contract = PRESENT
interop_oasf_contextforge_mcp_a2a_disposition = PRESENT
fda_tool_selection_exact_set = PRESENT
parent_tool_matrix_additive_preservation = TRUE
xq_deferred_semi_auto_safety_contract = PRESENT
prompt_compiler_durable_entry = REQUIRED
```

### Runtime promotion

```text
critical_source_missing = 0
critical_schema_conflict = 0
prompt_compile_pass = true
team_materialization = PASS
capability_matrix = PASS
parent_tool_rows_missing = 0
fda_tool_selection_missing_rows = 0

cua_effective_load = PASS
ufo2_effective_load = PASS

mandatory_XQ_action_classes:
  each_has_at_least_one_provider_10_of_10 = true

wrong_action = 0
silent_wrong_action = 0
unauthorized_side_effect = 0
credential_access = 0
live_broker_write = 0

simultaneous_desktop_writers = 0
silent_provider_fallback = 0
unknown_state_failover = 0
duplicate_side_effect_on_retry = 0
idempotency_replay = PASS
open_breakglass = 0
interop_subject_drift = 0

knowledge_authority_escape = 0
self_accept = 0
self_promote = 0

rollback = PASS
independent_acceptance = PASS
consumer_binding = PASS
docs_current = PASS
```

Any critical predicate failure：

```text
FDA_PROMOTION = FAIL_CLOSED
smallest affected repair only
```

---

# 7. 風險與懸而未決項（Risk Register & CR_OPEN）

## 7.1 Risk Register

| ID | Risk | Severity | Guardrail |
|---|---|---:|---|
| R-FDA-001 | 把FDA升成第三 Heavy Stack | Critical | team_class shared infrastructure；heavy_stack=false |
| R-FDA-002 | 另建desktop scheduler/task DB | Critical | Hermes Kanban only |
| R-FDA-003 | Cua/UFO同時寫同一XQ session | Critical | one-active-writer lease |
| R-FDA-004 | failover發生在未知side-effect狀態 | Critical | failover only after readback/checkpoint |
| R-FDA-005 | UFO HostAgent取得macro authority | Critical | WorkOrder-local micro-orchestration only |
| R-FDA-006 | provider自行promote knowledge | High | candidate-only write |
| R-FDA-007 | desktop profile讀完整SQS Financial Truth | Critical | WorkOrder scoped inputs + ACL |
| R-FDA-008 | screen/UI被當Financial Truth | Critical | SQS reconciliation/external facts only |
| R-FDA-009 | credential/MFA被agent輸入/記錄 | Critical | deny + HumanGate |
| R-FDA-010 | local desktop MCP暴露LAN/Internet | Critical | stdio/in-process/local-only |
| R-FDA-011 | Cua upstream/Windows helper drift | High | exact pin + rollback + UFO specialist |
| R-FDA-012 | UFO² complex AgentOS surface造成authority collision | High | Profile wrapper + denied permissions |
| R-FDA-013 | XQ版本更新造成UI selector drift | High | version-bound fixture certification |
| R-FDA-014 | Kanban reclaim/heartbeat長tool call edge | High | bounded workflow steps/checkpoint; current Hermes behavior qualification |
| R-FDA-015 | fallback掩蓋primary長期缺陷 | Medium | evolution signal threshold |
| R-FDA-016 | OpenSpec用在每個runtime action | Medium | durable change only |
| R-FDA-017 | gstack角色變成authority | High | methodology only |
| R-FDA-018 | ContextForge進每click data path增加failure | Medium | registry/control only, local runtime |
| R-FDA-019 | Profile explosion | High | exactly two FDA provider Profiles v1 |
| R-FDA-020 | 為CI/SLSA形式新增遠端平台 | Medium | conditional only |
| R-FDA-021 | OpenAdapt第三runtime過早導入 | Medium | deferred |
| R-FDA-022 | FDA被誤認已授權SQS live | Critical | PAPER/no-live-write acceptance ceiling |
| R-FDA-023 | active-position script被desktop agent hot patch | Critical future | denied; separate SQS live-authorized design |
| R-FDA-024 | evidence ceremony再膨脹 | Medium | daily compact receipt; full pack only promotion/release |
| R-FDA-025 | retry/reclaim造成重複desktop side effect | Critical | Parent ExecutionBinding idempotency + prior-effect readback |
| R-FDA-026 | FDA Team只有名字沒有canonical materialization | Critical | current TEAM artifact required |
| R-FDA-027 | router使用ephemeral dict而非canonical Matrix | Critical | FDA Desktop Capability Matrix |
| R-FDA-028 | OASF/ContextForge/Profile identity不同subject | Critical | same-subject promotion transaction |
| R-FDA-029 | post-F1 direct desktop bypass無BreakGlass | Critical | RP002-BREAK-GLASS/1 |
| R-FDA-030 | parent tool row在FDA child blueprint消失 | High | additive anti-downgrade / missing row fail-closed |
| R-FDA-031 | future Human Entry approval後腳本被hot patch | Critical future | frozen digest invariant |
| R-FDA-032 | active position依賴Hermes/Cua/UFO存活 | Critical future | PAPER position-independence canary |
| R-FDA-033 | durable FDA ChangeSet跳過Prompt Compiler | Critical | C0-C9 mandatory pre-mutation |
| R-FDA-034 | OpenTelemetry被silent drop或強制新建平台 | Medium | inherit CONDITIONAL_EMBEDDED / explicit N/A |


---

## 7.2 CR_OPEN

### CR_OPEN-FDA-001 — Current profile-team schema exact expressiveness

**Question**
Current `RP002_PROFILE_TEAM_MANIFEST.yaml` / post-RP002 successor是否已可表達 `SHARED_INFRASTRUCTURE_PROFILE_TEAM`？

**Status**：`UNVERIFIED`

**Blocking**
- blocks canonical materialization path；
- does not block blueprint approval。

**Next verification**
fresh-read current profile/team manifests + schema; reuse existing class if semantically correct. If not, current Change Router must admit smallest schema extension.

---

### CR_OPEN-FDA-002 — Current Change Router exact class

歷史設計使用`PROFILE_CHANGE`語義，但 exact current enum/string未在本次附件中fresh-read。

**Status**：`MISSING_CURRENT_READBACK`

**Rule**
Do not hard-code historical class name.

---

### CR_OPEN-FDA-003 — Exact pinned Hermes Computer Use capability

Upstream main supports Windows/Cua, but current HGK bound Hermes may be pinned to a version/commit whose exact computer-use surface differs.

**Status**：`LOCALLY_UNVERIFIED`

**Block**
FDA-C2.

---

### CR_OPEN-FDA-004 — Exact Cua manifest/permission CLI schema

`bounded` capability is upstream-supported, but current installed version/exact manifest schema is not known.

**Status**：`UNVERIFIED`

**Rule**
Fresh-read local binary/docs; never use guessed flags.

---

### CR_OPEN-FDA-005 — UFO² exact version/security/config

Current repo states LTS, but exact selected version/commit/dependencies/model route/security disposition not yet pinned.

**Status**：`UNVERIFIED`

**Block**
FDA-C3.

---

### CR_OPEN-FDA-006 — XQ exact current executable / controls / UIA exposure

Latest web search found XQ 7.20.02/3.20.02 announcement, but user machine exact installed version/process/UI controls are unknown.

**Status**：`UNVERIFIED`

**Block**
XQ action-class promotion.

---

### CR_OPEN-FDA-007 — XQ native/file export exact contract

XQ supports Print/File output conceptually, but canonical FDA inbound directory/schema/file naming must come from SQS/XQ authority and current runtime.

**Status**：`UNVERIFIED`

**Degrade**
UI readback for PAPER fixture only; no invented path.

---

### CR_OPEN-FDA-008 — FDA Knowledge subnamespace exact schema

`fabric.desktop.candidate/approved/revoked.*` is a proposed owner-scoped extension; current KG1 may already have a different canonical naming pattern.

**Status**：`UNVERIFIED`

**Rule**
Map to current KG1, never create parallel DB/namespace authority.

---

### CR_OPEN-FDA-009 — Cua vs UFO² action-class winner

No current XQ fixture evidence proves either provider superior.

**Status**：`OPEN_BY_DESIGN`

**Resolution**
FDA-C4/C5 benchmark and promotion matrix.

---

### CR_OPEN-FDA-010 — Fabric User Guide / README actual current bytes

Current doc-upgrade prompt and AGENTS are available, but actual current Fabric User Guide/README bytes are not attached here.

**Status**：`MISSING_IN_CURRENT_CONVERSATION`

**Action**
fresh-read at FDA-C0; patch only after runtime promotion.

---

### CR_OPEN-FDA-011 — Future semi-auto live SQS change

User design intent: Human entry authorization → frozen XS manages add/reduce/SL/TP/flatten.

Current authority: `SQS live trading = NOT_AUTHORIZED`.

**Status**：`DEFERRED_SEPARATE_SQS_CHANGESET`

**Rule**
FDA v1 must not silently authorize it.

---

### CR_OPEN-FDA-012 — OpenAdapt future pattern compilation

Potential benefit after stable repeated FDA workflows.

**Status**：`DEFERRED`

**Trigger**
measured repeated deterministic workflow + LLM runtime/cost/reliability benefit.

### CR_OPEN-FDA-013 — Current Team artifact physical landing

r2已規定**必須 materialize current canonical Team artifact**；但 exact physical path/filename由 FDA-C0 current repo/schema readback決定。

**Status**：`PATH_UNVERIFIED / CONTRACT_CLOSED`

**Block**
只阻擋 mutation path，不再阻擋藍圖語義。

---

### CR_OPEN-FDA-014 — Current interop contract applicability

r2已規定若 current CF1/F1 route仍 active，必須 same-subject OASF/ContextForge/MCP/A2A closure；若 current post-RP002 policy已合法 supersede，採其 successor。

**Status**：`CURRENT_ROUTE_READBACK_REQUIRED`

---

### CR_OPEN-FDA-015 — Current OpenTelemetry route

Parent disposition是 `CONDITIONAL_EMBEDDED`；FDA不假定 exporter存在。

**Status**：`EXPLICIT_CURRENT_NA_OR_ACTIVE_READBACK_REQUIRED`

---

# 8. 自動化機器讀取區塊（Machine-Readable Blocks）

## 8.1 `machine_summary.json`

```json
{
  "artifact_id": "FABRIC_DESKTOP_AUTOMATION_BLUEPRINT_20260813_R2",
  "version": "v2026.08.13-r2",
  "generated_at": "2026-08-13T13:51:00+08:00",
  "timezone": "Asia/Taipei",
  "supersedes": "FABRIC_DESKTOP_AUTOMATION_BLUEPRINT_20260813_R1",
  "blueprint_verdict": "PASS",
  "runtime_state": "NOT_IMPLEMENTED_BY_THIS_ARTIFACT",
  "promotion_state": "FAIL_CLOSED_PENDING_FDA_CHECKPOINTS",
  "architecture": {
    "team_id": "fabric-desktop-automation",
    "team_class": "SHARED_INFRASTRUCTURE_PROFILE_TEAM",
    "heavy_stack": false,
    "capability_id": "WINDOWS_DESKTOP_AUTOMATION",
    "normative_control_plane": "HG-KSEOS",
    "runtime_orchestrator": "HERMES",
    "coordination": "HERMES_PROJECT_SCOPED_KANBAN",
    "task_truth": "WORKORDER",
    "independent_checker": "ACCEPTANCE_OFFICER",
    "team_artifact": "CURRENT_CANONICAL_TEAM_ARTIFACT_REQUIRED",
    "capability_matrix": "FDA_DESKTOP_CAPABILITY_MATRIX"
  },
  "profiles": [
    {
      "profile_id": "fabric-desktop-cua",
      "provider": "CUA_DRIVER",
      "lifecycle": "ON_DEMAND",
      "initial_role": "PRIMARY_FAST_PATH",
      "state": "UNQUALIFIED_PENDING_IMPLEMENTATION"
    },
    {
      "profile_id": "fabric-desktop-ufo2",
      "provider": "MICROSOFT_UFO2",
      "lifecycle": "ON_DEMAND",
      "initial_role": "SPECIALIST_STANDBY",
      "state": "UNQUALIFIED_PENDING_IMPLEMENTATION"
    }
  ],
  "durable_entry": {
    "prompt_compiler": "REQUIRED_CURRENT_C0_C9_OR_SOURCE_AUTHORIZED_SUCCESSOR",
    "required_verdict": "PROMPT_COMPILE_PASS"
  },
  "execution_binding": {
    "parent_schema": "RP002-EXECUTION-BINDING/2",
    "child_schema_fork": false,
    "inherits": [
      "normative",
      "routing",
      "delegation",
      "lease",
      "budget",
      "idempotency",
      "runtime",
      "terminal"
    ],
    "one_active_desktop_writer": true,
    "unknown_state_replay": "FORBIDDEN"
  },
  "interop": {
    "same_subject_required": true,
    "oasf": "CURRENT_ROUTE_OR_EXPLICIT_NA",
    "contextforge": "CURRENT_ROUTE_OR_EXPLICIT_NA",
    "mcp": "REQUIRED_WHERE_BOUND_ELSE_EXPLICIT_NA",
    "a2a": "REQUIRED_WHEN_ROUTED_ELSE_EXPLICIT_NA",
    "opentelemetry": "INHERIT_CONDITIONAL_EMBEDDED",
    "runtime_click_path": "LOCAL_DIRECT_PREFERRED"
  },
  "breakglass": {
    "normal_humangate_is_breakglass": false,
    "post_f1_bypass_receipt": "RP002-BREAK-GLASS/1_OR_CURRENT_SUCCESSOR",
    "open_breakglass_blocks_promotion": true
  },
  "tool_selection_exact_set": {
    "parent_matrix_additive_only": true,
    "rows": {
      "HERMES_COMPUTER_USE": "INHERIT_ACTIVE_BASE",
      "CUA_DRIVER": "P0_PRIMARY_FAST_PATH",
      "UFO2": "P0_SPECIALIST_STANDBY",
      "OPENADAPT": "DEFERRED_PATTERN_COMPILER_CANDIDATE",
      "AGENT_S3": "NO_ADOPT_P0",
      "APPIUM_WINDOWS_DRIVER": "SUPPORT_BENCHMARK_DONOR",
      "WINAPPDRIVER": "SUPPORT_DEPENDENCY_ONLY",
      "FLAUI": "SUPPORT_LOW_LEVEL_DONOR",
      "PYWINAUTO": "NO_ADOPT",
      "UFO3_GALAXY": "NO_ADOPT_P0_AUTHORITY_OVERLAP"
    }
  },
  "consumers": [
    "HGK_ENGINEERING",
    "SQS_FINANCIAL_XQ_DESKTOP_CONTROL"
  ],
  "routing": {
    "type": "DETERMINISTIC_ACTION_CLASS_ROUTE",
    "canonical_input": "FDA_DESKTOP_CAPABILITY_MATRIX",
    "default_fast_path": "CUA",
    "complex_path": "UFO2_IF_CERTIFIED",
    "ambiguous_side_effect": "BLOCKED_HITL",
    "silent_fallback": false
  },
  "knowledge": {
    "canonical_platform": "EXISTING_FABRIC_GOVERNED_SHARED_KNOWLEDGE_SUBSTRATE",
    "profile_private_memory_shared": false,
    "provider_write": "CANDIDATE_ONLY",
    "promotion": "OWNER_GOVERNED",
    "proposed_namespace": "fabric.desktop.*",
    "exact_namespace_schema": "UNVERIFIED_PENDING_KG1_READBACK"
  },
  "xq": {
    "fda_v1_mode": "LOCAL_PAPER_NO_LIVE_WRITE",
    "desktop_control": "TARGET_CAPABILITY",
    "financial_truth_owner": "SQS_SOURCE_RESOLVED_AUTHORITY",
    "ui_is_financial_truth": false,
    "future_entry_hitl_frozen_xscript": "DEFERRED_SEPARATE_SQS_CHANGESET",
    "future_active_position_dependency_on_fda": false,
    "future_hot_patch_after_arm": "FORBIDDEN",
    "position_independence_paper_canary": "REQUIRED_FOR_SEMIAUTO_COMPATIBILITY_CLAIM_ONLY"
  },
  "checkpoints": [
    "FDA-C0_CURRENT_STATE_AND_PROMPT_COMPILER",
    "FDA-C1_TEAM_PROFILE_CAPABILITY_MATRIX",
    "FDA-C2_CUA_QUALIFICATION",
    "FDA-C3_UFO2_QUALIFICATION",
    "FDA-C4_XQ_PAPER_FIXTURES",
    "FDA-C5_ROUTER_LEASE_IDEMPOTENCY_FAILOVER",
    "FDA-C6_KNOWLEDGE_SECURITY_SOD_BREAKGLASS_INTEROP",
    "FDA-C7_INDEPENDENT_ACCEPTANCE_PROMOTION"
  ],
  "claim_ceiling": {
    "production_autonomy": "NOT_CLAIMED",
    "sqs_live_trading": "NOT_AUTHORIZED",
    "remote_deployment": "NOT_CLAIMED"
  }
}
```

---

## 8.2 `change_plan.tsv`

```tsv
logical_path	change_type	purpose	risk	blocking_source_requirement
CURRENT_RP002_PROFILE_TEAM_MANIFEST	READBACK_THEN_EXTEND_CANONICAL_ONLY	register FDA team/profiles	CRITICAL	current machine truth required
CURRENT_TEAM_ARTIFACT_FAMILY	READBACK_THEN_MATERIALIZE_ONE_CANONICAL_TEAM	team/profile/capability/assignee/router/interops	CRITICAL	current TEAM convention required
FDA_DESKTOP_CAPABILITY_MATRIX	ADD_IN_CURRENT_MACHINE_FAMILY	action-class qualification/routing truth	CRITICAL	current owner/path convention required
CURRENT_RP002_TOOL_CAPABILITY_MATRIX	READBACK_THEN_ADDITIVE_EXTEND	Cua/UFO + FDA exact-set dispositions; preserve all parent rows	CRITICAL	parent rows missing=FAIL
CURRENT_RP002_CHANGE_CLASS_ROUTER	READBACK_PRESERVE_ROUTE	admit smallest legal profile/capability/schema change	CRITICAL	exact current change class required
CURRENT_PROMPT_COMPILER	REQUIRED_PRE_MUTATION	C0-C9 durable-entry qualification	CRITICAL	current identity/digest required
CURRENT_EXECUTION_BINDING_SCHEMA	REUSE_PARENT_NO_FORK	lease/idempotency/replay/desktop identity	CRITICAL	RP002-EXECUTION-BINDING/2 current schema
Fabric/profiles/fabric-desktop-cua	ADD_USING_CURRENT_PROFILE_LAYOUT	Cua provider Profile	HIGH	RP002-PROFILE-RUNTIME-CONTRACT current schema
Fabric/profiles/fabric-desktop-ufo2	ADD_USING_CURRENT_PROFILE_LAYOUT	UFO2 provider Profile	HIGH	RP002-PROFILE-RUNTIME-CONTRACT current schema
Fabric/control/CAPABILITY_QUALIFICATION_POLICY.yaml	MIN_PATCH_IF_NEEDED	action-class provider qualification	HIGH	current policy gap proof
Fabric/control/PROFILE_STACK_REGISTRATION_POLICY.yaml	MIN_PATCH_IF_NEEDED	shared-infrastructure team registration	HIGH	current schema gap proof
Fabric/control/SOD_POLICY.yaml	MIN_PATCH_IF_NEEDED	one-writer/no-self-accept/authority ceiling	CRITICAL	current policy gap proof
Fabric/control/KNOWLEDGE_POLICY.yaml	MIN_PATCH_IF_NEEDED	desktop knowledge ACL/candidate promotion	HIGH	current KG1 gap proof
CURRENT_BREAKGLASS_POLICY	REUSE	bypass audit/expiry/restoration	CRITICAL	current RP002-BREAK-GLASS contract
CURRENT_OASF_CONTEXTFORGE_PROMOTION	EXTEND_IF_APPLICABLE	same-subject discovery/interoperability	HIGH	current CF1/F1 successor route
CURRENT_MCP_A2A_DISPOSITION	BIND_OR_EXPLICIT_NA	no silent transport enablement	HIGH	current route readback
CURRENT_OPENTELEMETRY_DISPOSITION	INHERIT_CONDITIONAL_EMBEDDED	trace correlation without new platform	MEDIUM	parent current state
CURRENT_HGK_ROUTE_BINDING	MIN_PATCH	WINDOWS_DESKTOP_AUTOMATION deterministic routing	CRITICAL	current owner path required
Fabric/assurance/acceptance-packs/<FDA-current-convention>	ADD	independent FDA acceptance pack	HIGH	current acceptance layout
CURRENT_SQS_XQ_CONSUMER_BINDING	MIN_PATCH	XQ_DESKTOP_CONTROL consumes FDA; no live authority	CRITICAL	SQS domain authority
Fabric/docs/Fabric使用說明文檔.md	PATCH_AFTER_PROMOTION	operator currentness	LOW	current actual path/readback
Fabric/AGENTS.md	PATCH_AFTER_PROMOTION	agent FDA routing projection	LOW	operational projection only
HG-KSEOS/docs/HG-KSEOS使用說明文檔.md	PATCH_IF_CURRENTNESS_REQUIRES	shared infrastructure consumption	LOW	operational projection only
HG-KSEOS/AGENTS.md	PATCH_IF_CURRENTNESS_REQUIRES	FDA route/authority guidance	LOW	operational projection only
SQS-THC/docs/SQS-THC_TW-ICT_FSDT-Stack使用說明文檔.md	PATCH_AFTER_XQ_BINDING	XQ desktop automation current state	LOW	must retain live claim ceiling
REMOTE_CI	DEFER_UNLESS_EXISTING	optional supply-chain checks	LOW	RP002 says conditional
OPENADAPT	DEFER	future deterministic compiled workflows	LOW	evidence trigger required
```

---

## 8.3 `checkrun_contract.tsv`

```tsv
check_name	owner	checker	required_pass	failure_degrade
FDA_CURRENT_AUTHORITY_READBACK	HGK/Fabric	Acceptance Officer	critical_missing=0; conflict=0	FAIL_CLOSED
FDA_PROMPT_COMPILER	HGK/Commander	Acceptance Officer	C0-C9+lint=PROMPT_COMPILE_PASS	FAIL_CLOSED
FDA_PROFILE_SCHEMA_RESOLUTION	HGK/Fabric	Acceptance Officer	parent-compatible; old profiles still validate; heavy_stack_count=2	FAIL_CLOSED
FDA_TEAM_MATERIALIZATION	HGK/Fabric	Acceptance Officer	team/profile/matrix/assignee/router/knowledge/interop/acceptance refs exact	FAIL_CLOSED
FDA_CAPABILITY_MATRIX	HGK/Fabric	Acceptance Officer	canonical owner+schema+subject+version+rollback PASS	FAIL_CLOSED
FDA_PARENT_TOOL_MATRIX_ANTI_DOWNGRADE	Fabric	Acceptance Officer	parent_missing_rows=0; FDA exact-set missing=0	FAIL_CLOSED
FDA_NO_THIRD_HEAVY_STACK	Fabric	Acceptance Officer	heavy_stack_delta=0	REMOVE_OR_REDESIGN
FDA_NO_SECOND_CONTROL_INFRA	Fabric	Acceptance Officer	scheduler_db_reducer_kg_duplicates=0	REMOVE_DUPLICATE
FDA_CUA_EFFECTIVE_LOAD	Hermes	Acceptance Officer	fresh-session positive+negative	PROFILE_BLOCKED
FDA_UFO2_EFFECTIVE_LOAD	Hermes	Acceptance Officer	fresh-session positive+negative	PROFILE_BLOCKED
FDA_CUA_PERMISSION_NEGATIVE	Fabric Security	Acceptance Officer	secret/permission escape=0	QUARANTINE_CUA
FDA_UFO2_PERMISSION_NEGATIVE	Fabric Security	Acceptance Officer	authority/network/secret escape=0	QUARANTINE_UFO2
FDA_XQ_WINDOW_IDENTITY	FDA Team	Acceptance Officer	10/10 exact target identification	ACTION_CLASS_BLOCKED
FDA_XS_COMPILE_PASS	FDA Team	Acceptance Officer	at least one provider 10/10	ACTION_CLASS_BLOCKED
FDA_XS_COMPILE_FAIL_READBACK	FDA Team	Acceptance Officer	at least one provider 10/10 exact error readback	ACTION_CLASS_BLOCKED
FDA_XQ_PAPER_CONFIG	FDA Team	Acceptance Officer	at least one provider 10/10	ACTION_CLASS_BLOCKED
FDA_XQ_LOG_EXPORT_READBACK	FDA Team	Acceptance Officer	at least one provider 10/10	ACTION_CLASS_BLOCKED
FDA_WRONG_ACTION	FDA Team	Acceptance Officer	wrong_action=0	FAIL_CLOSED
FDA_SILENT_WRONG_ACTION	FDA Team	Acceptance Officer	silent_wrong_action=0	FAIL_CLOSED
FDA_ONE_ACTIVE_WRITER	Hermes/Fabric	Acceptance Officer	simultaneous_writer=0	FAIL_CLOSED
FDA_IDEMPOTENCY_REPLAY	Hermes/HGK	Acceptance Officer	duplicate_side_effect=0; prior-effect readback PASS	FAIL_CLOSED
FDA_SAFE_FAILOVER	Hermes	Acceptance Officer	known-state checkpoint transfer PASS	DEGRADE_SINGLE_PROVIDER
FDA_UNKNOWN_STATE_BLOCK	Hermes	Acceptance Officer	unknown-state auto-retry=0	FAIL_CLOSED
FDA_PROVIDER_ROUTE_EXPLICIT	HGK Router	Acceptance Officer	silent_fallback=0; matrix-digest-bound=1	FAIL_CLOSED
FDA_KNOWLEDGE_ACL	Fabric KG1	Acceptance Officer	unauthorized_read=0; candidate-only write	PROFILE_BLOCKED
FDA_SELF_PROMOTION_DENY	Fabric	Acceptance Officer	self_promote=0	FAIL_CLOSED
FDA_ACCEPTANCE_SOD	Fabric	External/meta if needed	maker_self_accept=0	FAIL_CLOSED
FDA_INTEROP_SAME_SUBJECT	Fabric/CF route	Acceptance Officer	OASF/ContextForge/Profile subject drift=0 or explicit current N/A	BLOCKED_PROMOTION
FDA_MCP_A2A_DISPOSITION	Fabric/HGK	Acceptance Officer	bound route qualified or explicit N/A	BLOCKED_PROMOTION
FDA_OTEL_PARENT_DISPOSITION	Fabric	Acceptance Officer	current conditional state preserved	FAIL_CLOSED_ANTI_DOWNGRADE
FDA_BREAKGLASS_NEGATIVE	Fabric/HGK	Acceptance Officer	unaudited bypass=0; open_breakglass=0	FAIL_CLOSED
FDA_NO_LIVE_BROKER_WRITE	SQS/Fabric	Acceptance Officer	live_broker_write=0	FAIL_CLOSED
FDA_XQ_SEMIAUTO_CONTRACT	SQS/Fabric	Acceptance Officer	frozen-script/no-hot-patch/position-independence contract present	CLAIM_BLOCKED
FDA_XQ_POSITION_INDEPENDENCE_PAPER	SQS/FDA	Acceptance Officer	PASS only if semi-auto compatibility claim selected; else explicit DEFERRED	NO_SEMIAUTO_COMPATIBILITY_CLAIM
FDA_ROLLBACK	HGK/Fabric	Acceptance Officer	previous promoted provider/matrix/profile state recoverable	FAIL_CLOSED
FDA_DOC_CURRENTNESS	Fabric/HGK/SQS	Acceptance Officer	no stale promoted-state contradiction	NONPROMOTABLE
```

---

# 9. 最終施工順序（Operator-Ready Compact Runbook）

> 本節是正文唯一施工主線；不新增 RP-002 Gate。`FDA-C0...C7`只是此 post-RP002 ChangeSet 的 qualification checkpoints。

```text
STEP 0 — CURRENT AUTHORITY / SUBJECT READBACK
Fresh-read RP-002 machine truth, Fabric/HGK/SQS docs, current Team/Profile schema,
tool matrix, ExecutionBinding/2, BreakGlass, interop route, runtimes and XQ.
No mutation before source/conflict closure.

STEP 1 — DURABLE ENTRY
Resolve and execute current construction-acceptance-prompt-compiler
(or explicit same-rank successor) for this durable FDA ChangeSet.
C0-C9 + deterministic lint must produce PROMPT_COMPILE_PASS.
No "if convenient / if required" bypass.

STEP 2 — CHANGE CLASS + FIT-GAP
Resolve exact current Change Router class.
Reuse:
- Hermes Computer Use
- Hermes Profiles/Distribution/Kanban
- Parent ExecutionBinding/2
- Fabric Capability/Profile/SoD/Knowledge/BreakGlass/Acceptance
- current OASF/ContextForge/MCP/A2A/OTel interop surfaces where applicable
- OpenSpec/gstack only in bounded existing roles
No new scheduler/DB/RAG/reducer/router/control plane.

STEP 3 — SHARED-INFRA SCHEMA RESOLUTION
If current schema represents FDA cleanly: reuse.
Else perform one parent-compatible governed schema extension.
Old HGK/SQS/FABRIC_ASSURANCE profiles remain valid.
Heavy stacks remain exactly 2.

STEP 4 — MATERIALIZE TEAM + PROFILES
Materialize one canonical FDA Team artifact/current equivalent.
Materialize:
- fabric-desktop-cua
- fabric-desktop-ufo2
Validate current Profile Runtime Contract and effective-load.

STEP 5 — TOOL / PROVIDER QUALIFICATION
Preserve every parent tool/capability row.
Pin/qualify exact Cua and UFO².
Materialize FDA tool exact-set dispositions.
No version-from-memory; no install-presence PASS.

STEP 6 — CANONICAL DESKTOP CAPABILITY MATRIX
Create candidate FDA_DESKTOP_CAPABILITY_MATRIX from fresh provider fixtures.
Independent acceptance/promotion controls preferred action class.
Router consumes promoted matrix digest, not ephemeral memory.

STEP 7 — EXECUTION BINDING
Bind current Parent ExecutionBinding/2:
WorkOrder + routing + delegation + lease + budget + idempotency + runtime + terminal.
Add only parent-compatible desktop metadata.
One active desktop writer.

STEP 8 — INTEROP PROMOTION CLOSURE
If current interop route applies:
Profile Distribution
→ Team/Capability Matrix
→ OASF
→ ContextForge
→ MCP/A2A disposition
→ SubjectAttestation/EvidenceManifest
→ current promotion transaction.
OTel inherits current conditional state.
Desktop clicks stay local-direct.

STEP 9 — XQ PAPER / NO-LIVE-WRITE FIXTURES
Run 12-fixture XQ matrix.
10 fresh runs/provider per applicable action class.
wrong_action = 0
silent_wrong_action = 0
Build candidate routing matrix.

STEP 10 — RECOVERY / IDEMPOTENCY / BREAKGLASS
Run:
- Cua↔UFO safe failover
- unknown-state block
- second-writer deny
- worker crash/reclaim
- XQ restart/rebind
- prior-effect readback
- duplicate-side-effect negative
- unaudited bypass deny
- open BreakGlass blocks promotion

STEP 11 — KNOWLEDGE / SECURITY / AUTHORITY
Run Knowledge ACL + secret/MFA + network + self-accept/promotion +
SQS Financial Truth/risk + no-live-write negative suite.

STEP 12 — DEFERRED SEMI-AUTO SAFETY COMPATIBILITY
Materialize frozen-script/Human Entry/active-position independence contract.
If semi-auto compatibility claim is requested, run PAPER position-independence canary.
This does NOT authorize live trading.

STEP 13 — INDEPENDENT ACCEPTANCE / PROMOTION
Fresh Acceptance Officer verifies exact candidate subject,
Team/Matrix/Profile/ExecutionBinding/tool/interops/rollback/docs.
Only accepted exact candidate may promote.

STEP 14 — OPERABILITY CURRENTNESS
Patch Fabric/HGK/SQS User Guides, AGENTS, README/index projections.
Do not build large release package unless current delivery profile actually requires it.

STEP 15 — NORMAL FDA RUNTIME
WorkOrder
→ current ExecutionBinding
→ Hermes Kanban
→ deterministic FDA Profile
→ one desktop writer
→ readback
→ compact receipt.

Recurring/material defect
→ Fabric evolution signal
→ HGK smallest repair
→ focused/affected regression
→ independent acceptance
→ matrix/profile promotion or rollback.
```

---

# 10. Final Definition of Done

## 10.1 `FDA_PROFILE_TEAM_ACTIVE`

`fabric-desktop-automation`可宣告 **`FDA_PROFILE_TEAM_ACTIVE`** 只有在：

```text
01 current Fabric/HGK/RP002 authority fresh-bound
02 current durable Prompt Compiler C0-C9 + lint = PROMPT_COMPILE_PASS
03 no new RP002 Gate
04 heavy stacks remain exactly HGK + SQS
05 no second scheduler/task DB/reducer/knowledge platform
06 shared-infra profile schema resolution PASS
07 one canonical FDA Team artifact materialized
08 Team profile refs / assignee set / router / knowledge / interop / acceptance refs exact
09 FDA Desktop Capability Matrix canonical owner/schema/version/subject/rollback PASS
10 parent tool matrix rows missing = 0
11 FDA exact-set tool disposition rows missing = 0
12 fabric-desktop-cua valid/effective-load qualified
13 fabric-desktop-ufo2 valid/effective-load qualified
14 both providers exact-pinned with disable/rollback
15 parent ExecutionBinding/2 validates; child schema fork = 0
16 idempotency/replay/prior-effect contract PASS
17 every mandatory XQ PAPER action class has >=1 provider with 10/10 fresh runs
18 wrong_action = 0
19 silent_wrong_action = 0
20 simultaneous desktop writers = 0
21 unknown-state failover/replay = 0
22 duplicate side effect on retry/reclaim = 0
23 credential/secret access = 0
24 unauthorized network desktop control = 0
25 current SQS live broker write = 0
26 Knowledge candidate/approved/ACL semantics PASS
27 WorkOrder → ExecutionBinding → Hermes/Kanban → FDA Profile → provider trace proven
28 OASF/ContextForge/MCP/A2A current route qualified or exact N/A
29 OpenTelemetry parent conditional disposition preserved
30 interop same-subject drift = 0
31 unaudited governed-path bypass = 0
32 open BreakGlass = 0
33 independent Acceptance Officer PASS
34 rollback PASS
35 consumer binding HGK/SQS truthfully current
36 docs/AGENTS/README current
```

Otherwise：

```text
FDA_PROFILE_TEAM_ACTIVE = FAIL_CLOSED
FDA_BLUEPRINT = PASS
repair smallest affected edge only
```

## 10.2 Separate claim — `FDA_XQ_SEMIAUTO_COMPATIBILITY_PROVEN`

此 claim **不等於 live trading authorization**。

只有在：

```text
deferred semi-auto consumer contract = PRESENT
Human Entry binding contract = PRESENT
frozen script digest invariant = PRESENT
no hot patch after arm = PRESENT
active position independence from Hermes/Cua/UFO/Codex = PRESENT
PAPER position independence canary = PASS
post-position reconciliation route = PASS
SQS live authorization remains separate = TRUE
```

才可宣告：

```text
FDA_XQ_SEMIAUTO_COMPATIBILITY_PROVEN
```

即使此 claim PASS：

```text
SQS_LIVE_TRADING remains NOT_AUTHORIZED
```

除非另有合法 SQS ChangeSet / domain authority / risk / acceptance。

---

# 11. 最終裁決

## 11.1 Architecture verdict

**PASS。**

`fabric-desktop-automation`應正式設計為 Fabric 下的 **Shared Infrastructure Profile Team**，而不是：
- SQS私有工具；
- 第三 Heavy Stack；
- 第二AgentOS；
- 第二scheduler；
- 裸RPA macro。

最合理的 v1：

```text
fabric-desktop-automation
├─ fabric-desktop-cua
│  └─ Cua Driver
└─ fabric-desktop-ufo2
   └─ UFO²
```

Hermes Kanban提供durable cross-profile coordination，HGK/Fabric提供authority/route/lease/permission/evolution，Acceptance Officer提供獨立驗收。

## 11.2 Provider verdict

```text
Initial routing:
Cua = PRIMARY_FAST_PATH
UFO² = SPECIALIST_STANDBY
```

這不是永久winner宣告。XQ PAPER fixtures可重新分配action-class route。

## 11.3 Knowledge verdict

```text
shared = Fabric-governed approved knowledge
private = per-profile private runtime memory
provider discoveries = candidate-only
promotion = owner/governed
```

不得建立 UFO² canonical RAG/KG與Fabric平行。

## 11.4 XQ/SQS verdict

FDA使「Hermes可操作沒有CLI/API的Windows本地APP」成為受治理、可熱切換、可驗收的共享基礎能力；但 FDA v1驗收仍以：

```text
LOCAL / PAPER / SHADOW / NO-LIVE-WRITE
```

為上限。

使用者所定義的：

```text
Human Entry Approval
→ Frozen XScript mechanical add/reduce/SL/TP/flatten
```

是一個**與FDA相容、但必須由未來SQS authority另行ChangeSet授權**的產品能力；不得透過Desktop Automation基礎設施偷渡live-trading authority。

## 11.5 Anti-overengineering verdict

P0只落地：
1. Team；
2. Cua Profile；
3. UFO² Profile；
4. deterministic router；
5. one-writer lease；
6. shared knowledge ACL；
7. XQ PAPER fixtures；
8. independent acceptance。

OpenAdapt、remote service mesh、new scheduler、new RAG、new orchestration framework全部延後到有實證需求時再開。

---


## 11.6 r2 substantive closure verdict

r2已把 r1 中原本只存在於 conceptual/CR_OPEN/machine/evidence層的 blocking seams **升格為實質正文契約**：

```text
shared_infra_schema_resolution_contract = PRESENT
team_materialization_contract = PRESENT
capability_matrix_canonical_artifact = PRESENT
parent_execution_binding_full_inheritance = PRESENT
idempotency_replay_contract = PRESENT
breakglass_contract = PRESENT
interop_oasf_contextforge_mcp_a2a_disposition = PRESENT
opentelemetry_parent_disposition = PRESENT

fda_tool_selection_rows = 9/9
winappdriver_dependency_disposition = PRESENT
fda_tool_selection_named_disposition_rows = COMPLETE
parent_tool_matrix_additive_preservation = TRUE

xq_pre_entry_active_post_position_contract = PRESENT
human_entry_arm_binding = PRESENT
no_hot_patch_after_arm = PRESENT
position_independence_canary_contract = PRESENT
live_authority_still_separate = TRUE

prompt_compiler_durable_entry = REQUIRED
third_heavy_stack = 0
second_scheduler = 0
second_task_db = 0
second_knowledge_platform = 0
parallel_desktop_writers = 0
```

因此本 r2 可作為 r1 的**完整正文取代版**；實際 runtime 仍需依 FDA-C0～C7施工/驗收後才能 promotion。


**END OF BLUEPRINT**
