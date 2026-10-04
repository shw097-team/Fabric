# you asked

message time: 2026-08-13 13:05:48

那為何不把這基礎設施功能升格為fabric 下的"基礎設施 profile team"：「Desktop Automation」，並把cua 和ufo成為此「Desktop Automation」基礎設施中的熱插拔profile 模組，「Desktop Automation」再參考"KANBAN、OPENSPEC、GSTACK"的設計/架構/治理/流水線，在「Desktop Automation」中讓2個profile模組(cua 和ufo)進行簡單高效的協作或備援。

任務要求：
你必須針對以上項目，和全部相關資料進行「專業分析+交叉比對+深度整合」，再逐項對以上項目進行大數據搜索"2026年8月11日"以後的最新資料，搜索相關主題的「技術社群論壇(如HERMES HUB / GitHub)、網站、專欄、部落格、專業研究」，並對搜索資料進行「專業分析+交叉比對+深度整合」，再逐項對任務目標進行符合「工程專業實務作法、技術社群成熟技術者共識、不自己重複造外部現有可用輪子、整合導入進3個月熱度高的開源工具/方法」的最佳工程評估鑑定和規劃，並且不過度工程化。

---

# chatgpt response

這個方向**有成立的可能，而且比單一 `fabric-desktop-automation` Profile 更進一步**；但要先確認它會不會違反 RP-002 的「兩個 Heavy Stack、避免 Profile explosion、WorkOrder 才是 task truth」三條硬約束。我會把它當成「**Shared Infrastructure Profile Team**」候選，而不是預設第三 Heavy Stack，再用 RP-002 原文與 8/11 之後的 Cua/UFO/Hermes/Kanban/OpenSpec/gstack 現況交叉驗證。

我已把這個構想和 RP-002 的硬約束對完。**結論比上一輪更正面：可以升格成 Fabric 下的「Shared Infrastructure Profile Team：Desktop Automation」，而且這比單一 Profile 更能發揮 Cua/UFO² 的互補性。** 但兩個模組不能同時搶同一桌面寫權；要用 Hermes Kanban做單一任務真相、互斥執行與 failover，OpenSpec只管持久變更，gstack只提供方法論。

# 結論：可以，而且這比「單一 Desktop Automation Profile」更完整

你的構想**成立**。依 RP-002 v2.0 的既有設計，我會把前一版再上修成：

> **在 Fabric 下建立一個 Shared Infrastructure Profile Team：`Desktop Automation`，其中 Cua 與 UFO² 是兩個可資格化、可熱切換的 Desktop Automation Profiles / Provider Profiles；由 HGK 發 WorkOrder、Hermes Kanban 做唯一 runtime coordination，再借用 OpenSpec 的 durable-change contract 與 gstack 的工程方法論。**

這個方向沒有必要變成第三個 Heavy Stack。Master仍要求只有：

```text
HGK_ENGINEERING
SQS_FINANCIAL
```

兩個 Heavy Stack，並禁止第二 scheduler / task DB / knowledge platform。

因此我建議正式定位為：

```text
Fabric
└── Shared Infrastructure Profile Team
    └── Desktop Automation
        ├── desktop-cua
        └── desktop-ufo2
```

**不是：**

```text
Fabric
├── HGK Stack
├── SQS Stack
└── Desktop Automation Heavy Stack   ← 不需要
```

---

# 一、為什麼「Profile Team」比單一 Profile 更合理？

因為 Cua 與 UFO²不是完全同質的 executable。

### Cua

它更像：

> **低摩擦、Hermes-native、通用 desktop-control provider**

目前 Cua Driver直接提供 MCP over stdio、CLI、Python/TypeScript SDK，而且 `bounded` permission mode可以只允許 reviewed capability manifest內的 tools/resources。([GitHub](https://github.com/trycua/cua/blob/main/libs/cua-driver/README.md?utm_source=chatgpt.com))

更重要的是 Cua upstream在 **2026-08-12**仍然大量更新，近期 PR包括 Windows UIA health probe修復、permission/capability manifest、session scope與 release 0.20.0準備等。([GitHub](https://github.com/trycua/cua/pulls?utm_source=chatgpt.com))

### UFO²

它更像：

> **Windows-specialist desktop workflow agent**

官方把 UFO²定位為 stable/LTS Windows automation system，具 UIA、Win32、hybrid GUI/API、HostAgent/AppAgent，以及作為其他上層orchestrator的Windows device agent能力。([GitHub](https://github.com/microsoft/UFO/releases))

因此把兩者硬壓成：

```text
one Profile
→ runtime flag selects cua/ufo
```

雖然能做，但會隱藏：

- runtime state；
- provider-specific knowledge；
- permission；
- effective-load；
- fixtures；
- rollback；
- failure signature。

Profile Team反而更自然。

---

# 二、但我會稍微修正你的名詞：它們最好叫「Provider Profiles」

RP-002已有：

```text
ROLE != PROFILE != WORKER
TOOL != AUTHORITY
```



所以推薦：

```yaml
team_id: fabric-desktop-automation

profiles:
  - desktop-cua
  - desktop-ufo2
```

而每個Profile內再綁自己的provider：

```text
desktop-cua
  → Cua Driver

desktop-ufo2
  → UFO²
```

也就是：

> **Team是業務能力單位；Profile是runtime isolation/configuration單位；Cua/UFO²是底層provider/runtime implementation。**

這樣概念最乾淨。

---

# 三、這完全適合 Hermes Kanban

這部分幾乎是現成輪子。

Hermes current Kanban本來就是：

> durable SQLite-backed task board，跨多個 Hermes Profiles共享；每個worker是獨立OS process，而且hand-off與review都有board state。([GitHub](https://github.com/nousresearch/hermes-agent/blob/main/website/docs/user-guide/features/kanban.md))

目前 Hermes `AGENTS.md`也明確把 Kanban定成：

- durable shared board；
- dispatcher atomic claim；
- assigned profile spawn；
- stale reclaim；
- heartbeat；
- failure-limit auto-block；
- board isolation。([GitHub](https://github.com/NousResearch/hermes-agent/blob/main/AGENTS.md))

所以 Desktop Automation根本不需要自己再造：

```text
desktop task queue
desktop scheduler
desktop agent DB
desktop retry engine
```

全部不要。

---

# 四、推薦的 Team 結構其實只需要兩個 persistent/on-demand Profiles

```text
Desktop Automation Profile Team
│
├── desktop-cua
│   ├─ Cua Driver
│   ├─ UIA / capture / click / type
│   ├─ simple deterministic desktop actions
│   └─ primary fast path
│
└── desktop-ufo2
    ├─ UFO² AppAgent / bounded HostAgent
    ├─ UIA + Win32 + vision
    ├─ hybrid GUI/API
    ├─ complex workflow recovery
    └─ specialist / standby path
```

不需要再新增：

```text
desktop-orchestrator Profile
desktop-reviewer Profile
desktop-security Profile
```

因為那些已經有：

```text
Hermes/HGK orchestrator
Fabric Acceptance Officer
HGK Security
```

這符合避免 Profile explosion 的 RP-002精神。Stage-3對 SQS也是「角色很多 ≠ permanent profile很多」。

---

# 五、真正的「Team Leader」不是第三個Agent

而是：

```text
HGK WorkOrder
+
Fabric capability policy
+
Hermes deterministic routing
+
Kanban
```

也就是：

```text
                   Hermes
                     │
             desktop task card
                     │
             provider routing
              ┌──────┴──────┐
              ▼             ▼
       desktop-cua      desktop-ufo2
```

不要建立：

```text
desktop-manager-agent
```

除非以後真的證明需要一個獨立persistent state/security lifecycle。

---

# 六、Cua 與 UFO²最合理的協作方式不是「兩個一起點」

這是整套設計最重要的地方。

**同一desktop/session/app在同一時間只能有一個writer。**

否則：

```text
Cua:
click Compile

UFO:
同時 click Radar
```

會直接產生race condition。

所以 Desktop Automation Team必須繼承 RP-002：

```text
ONE_WRITER
WRITE_SET_COLLISION_FREEZE
```

的思想。Master對worktree是one-writer；桌面automation可以對應成：

```text
ONE_ACTIVE_DESKTOP_WRITER_PER_SESSION
```

這不是新增scheduler，只是Desktop capability的permission invariant。

---

# 七、最推薦的協作模型：Primary / Standby，而非Swarm

正常：

```text
WorkOrder
   ↓
desktop-cua
   ↓
PASS
```

如果失敗：

```text
desktop-cua
   ↓
failure detected
   ↓
safe checkpoint
   ↓
desktop-ufo2
   ↓
resume/recover
```

也就是：

```text
Cua = FAST PATH
UFO² = SPECIALIST RECOVERY PATH
```

至少第一版先這樣。

不需要兩個Agent同時競賽誰先完成。

---

# 八、第二種模式：按工作類別分工

等qualification結果累積後，可以形成：

| Action Class | Preferred Profile |
|---|---|
| 固定UIA control | `desktop-cua` |
| known click/type/readback | `desktop-cua` |
| 視窗/簡單dialog | `desktop-cua` |
| 複雜多步Windows workflow | `desktop-ufo2` |
| custom/nonstandard control | `desktop-ufo2` |
| UIA tree不足 | `desktop-ufo2` |
| GUI + native API hybrid | `desktop-ufo2` |
| ambiguous side effect | `BLOCKED_HITL` |

UFO²官方就是設計成在 native API可用時prefer API，GUI則作fallback，並可在同一task混合兩條路。([GitHub](https://github.com/microsoft/UFO/blob/main/documents/docs/ufo2/core_features/hybrid_actions.md))

所以它很適合接「複雜路徑」。

---

# 九、第三種模式：Shadow Verification

高風險、但不產生外部副作用的動作可以：

```text
desktop-cua
= writer

desktop-ufo2
= read-only observer
```

例如 Cua部署完 XScript後：

```text
Cua:
compile

UFO²:
read result / inspect UI state
```

或者反過來。

但重要規則：

```text
SECOND_PROFILE_WRITE = DENY
```

這可以增加 cross-provider verification，又不製造race。

不應每個操作都用shadow，否則成本太高。

---

# 十、熱插拔要有「安全切換點」

我同意你使用「熱插拔」，但工程上不能理解成：

> Cua滑鼠按到一半，瞬間換UFO接下去。

正確熱切換是：

```text
ACTION START
↓
ACTION COMPLETED
↓
READBACK
↓
CHECKPOINT
──────── safe provider switch boundary
↓
NEXT ACTION
```

或者：

```text
ACTION FAILED
↓
state readback
↓
rollback / restore
↓
checkpoint
──────── provider switch
↓
alternate provider retry
```

所以 hot-swap應綁：

```text
task/action boundary
checkpoint
known desktop state
```

不能綁任意token/LLM turn。

---

# 十一、Fabric真正需要的是一個 Desktop Capability Matrix

例如概念上：

```yaml
capability: WINDOWS_DESKTOP_AUTOMATION

providers:

  desktop-cua:
    classes:
      ui_tree: PASS
      click: PASS
      type: PASS
      screenshot: PASS
      complex_workflow: CONDITIONAL

  desktop-ufo2:
    classes:
      ui_tree: PASS
      win32: PASS
      visual_grounding: PASS
      hybrid_api_gui: PASS
      complex_workflow: PASS
```

Fabric router再依：

```text
action_class
application
version
permission
risk
historical success
known failure
```

選profile。

**不能讓LLM說：「我今天感覺用UFO好了。」**

---

# 十二、Kanban應該怎麼參考？——直接重用，不要模仿重寫

你的構想說參考Kanban。

我的修正是：

> **不要「參考Kanban設計一套 Desktop Kanban」。直接使用 Hermes Kanban。**

因為 RP-002 Stage-2就是這樣設計的：Hermes Kanban是唯一runtime coordination substrate，不另造scheduler。

Desktop task可直接長這樣：

```text
DA-001
Open XQ

DA-002
Deploy validated script
depends_on: DA-001

DA-003
Compile script
depends_on: DA-002

DA-004
Read compile result
depends_on: DA-003

DA-005
Configure PAPER strategy
depends_on: DA-004
```

assigned profile：

```text
desktop-cua
```

如果DA-003 repeated failure：

```text
reassign → desktop-ufo2
```

即可。

---

# 十三、但不需要把每一個 mouse click變成Kanban card

這會過度工程。

合理粒度是：

```text
Task:
Deploy and compile XScript candidate
```

而不是：

```text
Task1 open editor
Task2 click tab
Task3 click textbox
Task4 ctrl+a
Task5 paste
Task6 click compile
```

後者應留在 Cua/UFO profile local execution plan。

也就是：

```text
Kanban
= macro coordination

Profile
= micro execution
```

這跟 UFO² HostAgent/AppAgent本身的hierarchical設計也相容；AppAgent就是application-specific subtask executor。([GitHub](https://github.com/microsoft/UFO/blob/main/documents/docs/ufo2/app_agent/overview.md?utm_source=chatgpt.com))

---

# 十四、OpenSpec該怎麼吸收？

這裡也不要錯用。

OpenSpec應負責：

> **Desktop Automation infrastructure本身的 durable changes。**

例如：

```text
新增 UFO² provider
修改 provider routing
新增 XQ automation capability
修改 permission boundary
新增 provider fallback
改 knowledge schema
```

才走：

```text
ChangeRequest
→ OpenSpec
→ proposal
→ design
→ spec
→ tasks
→ HGK WorkOrder
→ implementation
→ Acceptance
```

RP-002原本就是這樣定義 OpenSpec：durable/brownfield Change Package method，不是 runtime authority。

而 current OpenSpec已正式支援 Hermes skills-only integration，官方 changelog也明確記錄 `openspec init --tools hermes`。([GitHub](https://github.com/Fission-AI/OpenSpec/releases?utm_source=chatgpt.com))

所以兩者磨合很好。

---

# 十五、日常 Desktop Automation task 不應跑 OpenSpec

例如：

> 今天把 XS 腳本部署到 XQ。

不要：

```text
OpenSpec proposal
→ design
→ spec
→ task
```

這是過度工程。

直接：

```text
admitted WorkOrder
→ Hermes
→ Desktop Automation Team
```

即可。

OpenSpec只處理**基礎設施變更**，不是每個基礎設施使用請求。

---

# 十六、gstack該怎麼參考？

同樣：

> **吸收方法論，不吸收它的control plane。**

RP-002已經定案：

```text
gstack full role repertoire / methodology
YES

gstack Conductor
NO

gstack /spec authority
NO

gstack /ship promotion authority
NO
```



gstack current repo也確實是完整角色方法包，涵蓋CEO、Eng、Review、QA、Release、Docs等角色。([GitHub](https://github.com/garrytan/gstack?utm_source=chatgpt.com))

所以 Desktop Team可以借下面幾個模式。

---

# 十七、適合 Desktop Automation 的 gstack 方法

### `/plan-eng-review`

用於：

```text
新增XQ workflow
provider routing變更
permission變更
```

---

### `/investigate`

非常適合：

```text
Cua在XQ某dialog失敗
UIA control消失
UFO誤判control
```

---

### `/review`

檢查：

```text
provider adapter
routing rules
state machine
```

---

### `/qa`

跑：

```text
desktop fixture regression
XQ known-pass
known-fail
restart
recovery
```

---

### `/cso`

檢查：

```text
credential isolation
MCP exposure
clipboard
screen capture
sensitive windows
```

---

### `/retro`

例如：

```text
Cua失敗 → UFO成功
```

就分析是否形成新的：

```text
provider routing candidate
```

而不是立即自行promote。

---

# 十八、因此 Desktop Automation有一條非常漂亮的「工程流水線」

### 正常runtime

```text
WorkOrder
↓
Hermes Kanban
↓
provider router
↓
desktop-cua
↓
readback
↓
PASS
```

---

### Cua失敗

```text
Cua FAIL
↓
bounded retry
↓
still FAIL
↓
checkpoint
↓
desktop-ufo2
↓
PASS
↓
record provider delta
```

---

### 重複發生

```text
same failure class repeats
↓
Fabric Evolution signal
↓
HGK
↓
gstack /investigate
↓
OpenSpec Change
↓
Codex repair
↓
QA
↓
Acceptance Officer
↓
promotion
```

這就是你所說：

> 「有問題Fabric叫HGK去升級修補。」

變成完整工程鏈。

---

# 十九、這比「每次Cua壞就切UFO」更成熟

一定要避免：

```text
Cua failure
→ UFO
→ success
→ forget
```

否則永遠靠fallback掩蓋primary defect。

應記：

```text
primary_failure_signature
fallback_success
application
application_version
control_type
action_class
```

累積到閾值就：

```text
Governed Evolution
```

這正是Fabric存在的意義。

---

# 二十、Knowledge可以讓兩個Profile真正產生協同效果

共享：

```text
fabric.desktop.approved.*
```

例如：

```text
windows.uia.*
xq.editor.*
xq.radar.*
xq.dialogs.*
xq.version.7_20.*
desktop.failure_patterns.*
```

---

### Cua可以讀

```text
Cua known control selectors
known window identity
known XQ workflow
```

### UFO可以讀

同一approved knowledge。

---

### 各自新發現

```text
desktop-cua
→ fabric.desktop.candidate.cua.*

desktop-ufo2
→ fabric.desktop.candidate.ufo.*
```

再由Fabric promotion。

這符合 RP-002「治理集中、儲存共享、知識生產分散」的Knowledge模型，而不是讓每個Agent自建第二知識庫。

UFO²自身確實也提供Knowledge Substrate，可利用docs、RAG與execution knowledge提高AppAgent能力。([GitHub](https://github.com/microsoft/UFO/blob/main/documents/docs/ufo2/core_features/knowledge_substrate/overview.md?utm_source=chatgpt.com))

因此讓它讀Fabric-scoped knowledge非常合理。

---

# 二十一、但共享Memory不能變成跨Profile裸共享

Hermes Profiles目前是完全隔離的 `HERMES_HOME`實例，各有config、keys、memory、sessions、skills。([GitHub](https://github.com/NousResearch/hermes-agent/blob/main/AGENTS.md))

所以：

> **Profile private memory 保持private。**

共享的是：

```text
Fabric-governed approved knowledge
```

不是：

```text
desktop-cua ~/.hermes/memory
↔ desktop-ufo ~/.hermes/memory
```

這條界線不要打破。

---

# 二十二、推薦的 Profile Team 最小設計

```yaml
team_id: fabric-desktop-automation

team_class: SHARED_INFRASTRUCTURE

runtime:
  engine: hermes
  coordination: kanban

profiles:

  desktop-cua:
    provider: CUA_DRIVER
    mode: PRIMARY_FAST_PATH
    lifecycle: ON_DEMAND

  desktop-ufo2:
    provider: UFO2
    mode: SPECIALIST_STANDBY
    lifecycle: ON_DEMAND

routing:
  strategy: DETERMINISTIC_CAPABILITY_ROUTE

write_policy:
  active_desktop_writer_count: 1

knowledge:
  read:
    - fabric.desktop.approved.*
    - shared.approved.desktop.*
  candidate_write:
    - fabric.desktop.candidate.*

acceptance:
  checker: FABRIC_ACCEPTANCE_OFFICER
```

這已經足夠。

---

# 二十三、不需要第三個Profile做router

Router可以直接由：

```text
Fabric Capability Matrix
+
HGK/Hermes route
```

處理。

例如：

```text
KNOWN_STABLE_UIA
→ Cua

COMPLEX_WINDOWS_WORKFLOW
→ UFO

CUA_FAILURE_RETRY_EXHAUSTED
→ UFO

UFO_FAILURE + CUA_SUPPORTED_ACTION
→ Cua

AMBIGUOUS_SIDE_EFFECT
→ HITL
```

這是deterministic routing。

Hermes現在的設計本來也鼓勵capability「活在edge」，保持core narrow，而不是什麼能力都塞進core。([GitHub](https://github.com/NousResearch/hermes-agent/blob/main/AGENTS.md))

---

# 二十四、要不要讓 Cua、UFO做Swarm？

**P0不要。**

Swarm更適合：

```text
parallel research
multiple independent analyses
evidence synthesis
```

不適合：

```text
two writers
→ same XQ desktop
```

所以 Desktop Team：

```text
SWARM_CAPABILITY = AVAILABLE
NORMAL_ROUTE = DIRECT
FAILOVER_ROUTE = SEQUENTIAL
```

只有read-only analysis例如：

> 「Cua和UFO各自分析目前UI tree，誰更有把握？」

才可以並行。

---

# 二十五、推薦的 Desktop Automation 狀態機

```text
ADMITTED
   ↓
ROUTE_PROVIDER
   ↓
ACQUIRE_DESKTOP_LEASE
   ↓
OBSERVE
   ↓
EXECUTE
   ↓
READBACK
   ├── PASS → RELEASE_LEASE → COMPLETE
   │
   └── FAIL
        ↓
     BOUNDED_RETRY
        ↓
     CHECKPOINT
        ↓
    ROUTE_ALTERNATE
        ↓
     EXECUTE
        ├── PASS → COMPLETE + EVOLUTION_SIGNAL?
        └── FAIL → BLOCK / HGK REPAIR
```

非常薄。

---

# 二十六、Desktop Lease是必要的，但不要做新Lease服務

不要發明：

```text
desktop-lock-server
```

只需把：

```text
desktop_session_id
desktop_target
writer_profile
lease_expiry
```

放進現有 ExecutionBinding/Kanban task metadata。

RP-002本來就有 delegation/lease/heartbeat/reclaim/idempotency語義。

完全重用。

---

# 二十七、Cua的 bounded manifest 正好可以成為Profile permission implementation

Cua目前 `bounded` mode只允許reviewed capability manifest裡列出的tools/resources，而且permission mode在runtime launch時固定。([GitHub](https://github.com/trycua/cua/blob/main/libs/cua-driver/README.md?utm_source=chatgpt.com))

這跟Fabric Profile permission contract天然吻合：

```text
Fabric Profile permissions
↓
compile
↓
Cua capability manifest
```

例如：

```text
desktop-cua / XQ profile

allow:
  capture
  click
  type
  window inspect

scope:
  XQ process/window

deny:
  browser
  password windows
  unrelated desktop apps
```

這是非常強的整合點。

---

# 二十八、UFO²則適合作第二個「能力不同」的Profile，而不是純備份copy

UFO²不是另一個Cua clone。

其 HostAgent/AppAgent架構、Windows-specific AppAgent與hybrid GUI/API能力可以承擔更複雜workflow。([GitHub](https://github.com/microsoft/UFO/blob/main/documents/docs/ufo2/overview.md?utm_source=chatgpt.com))

所以：

```text
desktop-ufo2
```

最好不是單純：

> Cua掛了換它。

而是有自己的certified action classes。

例如：

```text
UFO_ONLY_OR_PREFERRED:
  custom dialog recovery
  multi-app workflow
  complex XQ state navigation
  hybrid GUI/API
```

這樣兩個profiles才是真正互補。

---

# 二十九、OpenSpec + gstack + Kanban 三者應各管不同層

這點很重要。

| Layer | Owner | Desktop Team用途 |
|---|---|---|
| **Runtime coordination** | Hermes Kanban | 任務、依賴、claim、heartbeat、handoff、retry |
| **Durable change** | OpenSpec | provider/profile/router/permission重大修改 |
| **Engineering methodology** | gstack | investigate/review/QA/security/retro |
| **Normative authority** | Fabric/HGK | WorkOrder、SoD、promotion |
| **Desktop execution** | Cua/UFO² | 實際操作Windows |
| **Formal acceptance** | Acceptance Officer | 獨立驗收 |

這個SoD非常乾淨。

---

# 三十、我會怎麼命名？

我推薦：

## Team

```text
fabric-desktop-automation
```

正式名稱：

> **Fabric Desktop Automation Infrastructure Profile Team**

---

## Profiles

```text
fabric-desktop-cua
fabric-desktop-ufo2
```

不要叫：

```text
cua-agent
ufo-agent
```

避免tool identity跟profile role綁死。

---

## Capability

```text
WINDOWS_DESKTOP_AUTOMATION
```

---

## Consumer bindings

```text
HGK:
  desktop-engineering-automation

SQS:
  XQ_DESKTOP_CONTROL
```

這樣 SQS只consumer，不own infrastructure。

---

# 三十一、第一版不要做得太大

我支持你的 Profile Team方向，但**第一版仍只做以下東西**：

1. 建 `Desktop Automation` team manifest；
2. 建 `desktop-cua` distribution；
3. 建 `desktop-ufo2` distribution；
4. 共用 Hermes Kanban；
5. 一個 deterministic router；
6. 一個 desktop writer lease；
7. 一份 capability/action qualification matrix；
8. 共用Fabric Knowledge ACL；
9. Cua primary / UFO specialist；
10. XQ PAPER/no-live-write fixtures。

不要做：

-新scheduler；
-新DB；
-新RAG；
-新reducer；
-新global planner；
-自行重寫RPA；
-讓兩個profiles同時操作XQ；
-每個click建立Kanban card；
-日常task跑OpenSpec；
-每次都跑gstack整個lifecycle。

---

# 最終工程裁決

**是，我現在認為你的新方案比我前面「單一 Shared Infrastructure Profile + providers」的方案更好一級。**

不是因為多Agent一定更強，而是因為 Cua 和 UFO²實際具有：

-不同runtime；
-不同knowledge需求；
-不同permission surface；
-不同Windows操作強項；
-不同failure modes；
-不同upgrade/rollback lifecycle。

這些條件**已經足以合理化兩個 Profile identities**。

而 Hermes Kanban本身就是跨Profiles持久協作的現成基座，不需要再開發Profile Team scheduler。([GitHub](https://github.com/nousresearch/hermes-agent/blob/main/website/docs/user-guide/features/kanban.md))

因此我推薦正式收斂為：

```text
Fabric
│
└─ Desktop Automation Infrastructure Profile Team
   │
   ├─ fabric-desktop-cua
   │     └─ Cua Driver
   │
   └─ fabric-desktop-ufo2
         └─ UFO²
```

再由：

```text
HGK WorkOrder
→ ExecutionBinding
→ Hermes Kanban
→ deterministic profile routing
→ one active desktop writer
→ readback
→ failover
→ evidence
```

運作。

**Kanban直接拿來當協作基座；OpenSpec只治理基礎設施的durable changes；gstack只吸收 investigate/review/QA/security/retro 等工程方法；Fabric仍掌握permission、knowledge、acceptance、promotion與provider lifecycle。**

初始策略我仍建議：

```text
Cua = PRIMARY_FAST_PATH
UFO² = SPECIALIST_STANDBY
```

但這只是初始routing policy。

等 XQ fixtures累積證據後，可以自然演進成：

```text
Cua:
simple/stable UI actions

UFO²:
complex/custom/hybrid workflows
```

甚至某些XQ workflow讓 UFO²變primary也沒有問題。

**這個方案同時保留了「簡單、快速落地」與「真正Profile Team的韌性和自進化空間」，我認為已經接近目前這個需求的最佳架構點。**

---
Powered by [AI Exporter](https://saveai.net)