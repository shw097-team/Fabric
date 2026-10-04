# you asked

message time: 2026-08-13 12:00:20

補充和釐清：
1)目前是採"半自動"交易：SQS/XQ/XS發出進場信號和請求之後，用戶手動點擊確認進場，接著SQS/XQ/XS會直接進行一連串的「加碼、減碼、止損、止盈、清倉」的TW-ICT操盤動作，而這些「加碼、減碼、止損、止盈、清倉」的TW-ICT操盤動作，都是事先規劃好的「XS腳本」，依照事先規劃好的「關鍵價位、籌碼流動性/價格走向劇本、偏見」，腳本機械式進行操盤，所以不會有進場之後還在即時AI分析這種事發生。
2)我前述的高自動化重點，其實是在於，目前Hermes  是否對於沒有CLI接管的本地APP，也能透過其他Hermes可用的"管道、工具、功能"對目標APP進行操控(譬如對用戶目前桌面或螢幕進行滑鼠和鍵盤的控制)?或是你前述提出的方案已經解決這項問題?
3)「HGK 已經是 Agentic OS ，Hermes 已經是 orchestrator  ，如果再引入UFO²    ，就有可能產生第二個task/orchestration authority。  」→關於你前述提到的這點，目前的「Hermes  、HGK、SQS」3者已經由實作完成的FABRIC進行治理，你必須對「使用說明文檔、readme、AGENTS.md」 進行深度研究+交叉分析，再進一步以新角度逐項更新前述方案的全部內容和規劃(除了UFO²之外的項目也要更新)。

任務要求：
你必須針對以上項目，和全部相關資料進行「專業分析+交叉比對+深度整合」，再逐項對以上項目進行大數據搜索"2026年8月11日"以後的最新資料，搜索相關主題的「技術社群論壇(如HERMES HUB / GitHub)、網站、專欄、部落格、專業研究」，並對搜索資料進行「專業分析+交叉比對+深度整合」，再逐項對任務目標進行符合「工程專業實務作法、技術社群成熟技術者共識、不自己重複造外部現有可用輪子、整合導入進3個月熱度高的開源工具/方法」的最佳工程評估鑑定和規劃，並且不過度工程化。

---

# chatgpt response

我會先修正前一輪一個關鍵模型：你的交易流程不是「AI 盤中持續決策」，而是 **AI/研究階段先生成 TW-ICT 劇本與 XS 狀態機，HumanGate 只決定是否啟動該次進場；一旦進場，後續加碼/減碼/止損/止盈/清倉由已核准 XS 機械式執行**。因此這次真正要鑑定的是：**Hermes 能否可靠接管「XQ 桌面操作平面」，而不是把 AI 放進 execution loop。**

# 更新後工程鑑定：Fabric 治理下的 Hermes × HGK × SQS × XQ/XS 高自動化方案

## 先給結論

你的三點補充會**實質改變前一輪方案**，而且方向更合理。

最核心的修正是：

> **盤中真正的交易執行者應該是「事先編譯、驗證、凍結的 XScript 狀態機」，而不是 Hermes/LLM。**

因此正常交易鏈應該是：

```text
SQS / TW-ICT
  │
  ├─ 盤前/盤中候選研究
  ├─ Bias / Scenario
  ├─ 關鍵價位
  ├─ Liquidity / Flow
  ├─ Risk
  ├─ XScript generation
  └─ validation
        ↓
Hermes 自動部署 / 設定 XQ
        ↓
XQ / XS 產生 Entry Candidate
        ↓
       HUMAN
   「確認本次進場」
        ↓
══════════ Execution Boundary ══════════
        ↓
Frozen XScript State Machine
        │
        ├─ 加碼
        ├─ 減碼
        ├─ Stop Loss
        ├─ Take Profit
        └─ Flatten
        ↓
Broker / Execution Facts
        ↓
SQS reconciliation / journal
```

**進場後不需要、也不應讓 Hermes 或 AI 重新分析要不要加碼、停損、止盈。**

XQ官方本身就支援交易腳本自動控制買賣方向、數量、價格、實際成交資訊，以及完整自動交易流程；官方教材也明確說交易語法支援進場、出場、加碼、減碼，`SetPosition` 等語法就是用來描述目標部位。([XQ全球贏家](https://www.xq.com.tw/lesson/xsat/introduction/?utm_source=chatgpt.com))

這使整體架構**比我上一輪描述的還簡單、安全，而且更符合 SoD**。

---

# 一、第一個重大勘誤：這不是「AI半自動交易」，而是「HITL-armed deterministic execution」

你描述的真正模式應精確命名為：

> **Human-Authorized, Script-Autonomous Execution**

或在你目前 SQS/Fabric vocabulary裡可以定成：

```text
ENTRY_HITL_ARMED_XSCRIPT_EXECUTION
```

它不是：

```text
AI decides entry
→ AI watches market
→ AI decides add/reduce/stop
→ AI sends orders
```

而是：

```text
TW-ICT事前決策
→ 編譯成 deterministic execution policy
→ Human確認該次 entry
→ XScript依法執行整個position lifecycle
```

這個差別非常重要。

## Human真正授權的是「一份交易劇本」

HumanGate實際應綁：

```text
symbol / instrument
side
entry condition
max initial size
max total size
scale-in rules
scale-out rules
stop-loss rules
take-profit rules
flatten rules
time stop
risk ceiling
XScript version
XScript SHA256
Scenario / Bias ID
Trading Session ID
```

按下「確認進場」的語義應該是：

> **我批准這份已凍結 execution policy 在本次 session內執行。**

而不是：

> 我只批准第一張委託，後面讓AI自由決定。

這和你的原意完全不同。

---

# 二、這也代表 Hermes 不應進入 position-management fast loop

前一版我曾把：

```text
Hermes
→ XQ
→ monitoring
→ possible actions
```

放得太接近交易 execution。

更新後應拆成兩個完全不同的控制平面。

## Plane A — Automation / Operator Plane

Hermes負責：

```text
開XQ
管理視窗
進入XS Editor
匯入XScript
修改/同步candidate
compile
讀compile error
呼叫Codex修復
recompile
設定自動交易策略
設定symbol/group
設定parameters
設定paper/live profile
啟動watch/radar
讀取status/log
export/readback
reconciliation workflow
XQ crash recovery
```

## Plane B — Trading Execution Plane

XScript負責：

```text
Entry after HumanGate
Position state
Scale-in
Scale-out
Stop loss
Take profit
Time exit
Flatten
```

而：

```text
Hermes = NOT IN DECISION LOOP
LLM    = NOT IN DECISION LOOP
Codex  = NOT IN DECISION LOOP
```

這是我現在推薦的正式設計。

---

# 三、這會讓整體安全性反而大幅提高

你不是要求：

> 讓 LLM autonomously trade。

而是：

> 讓 LLM/Agent自動做 preparation / deployment / maintenance，真正execution由 deterministic XScript執行。

這符合成熟交易系統裡：

```text
Research Plane
≠
Control Plane
≠
Execution Engine
≠
Execution Truth
```

SQS engineering DOC-02本來就要求 `ExecutionEvent`是外部、append-only execution fact，不能讓XQ UI或AgentOS state取代 canonical execution truth。

所以：

> **Hermes可以自動操控XQ，但Hermes不應成為交易execution engine。**

這兩件事並不矛盾。

---

# 四、第二個問題：Hermes到底能不能操控沒有CLI/API的本地APP？

## 答案：**可以；而且我前一輪提出的 Cua Driver 路線基本上就是解這個問題。**

最新 Hermes upstream 已經有正式 `computer_use` surface。

官方CLI目前提供：

```text
hermes computer-use install
hermes computer-use install --upgrade
hermes computer-use status
```

而且 upstream installer明確涵蓋：

```text
macOS
Windows
Linux
```

([GitHub](https://github.com/nousresearch/hermes-agent/blob/main/website/docs/reference/cli-commands.md?utm_source=chatgpt.com))

Hermes自身的 current prompt/tool implementation也明確有：

- capture；
- click；
- type；
- scroll；
- background window control；
- capture-after-action；
- password/payment/permission dialog safety guard。([GitHub](https://github.com/NousResearch/hermes-agent/blob/main/agent/prompt_builder.py?utm_source=chatgpt.com))

---

# 五、Cua Driver 在 Windows 不只是「滑鼠巨集」

這一點很關鍵。

現在的 Cua Driver Windows架構同時提供：

```text
window pixels
+
UIA / MSAA accessibility tree
+
click/type/scroll/value/action
+
verification
```

而不是只靠畫面座標。官方 Cua工程說明特別指出，它必須處理：

```text
Win32
WPF
WinUI
UWP
Electron
Chromium
VCL
GTK
custom canvases
```

([GitHub](https://github.com/trycua/cua/blob/main/blog/inside-windows-computer-use.md?utm_source=chatgpt.com))

目前 Cua主repo也直接描述：

> Cua Drivers可在Windows/macOS/Linux背景操控原生desktop apps，agent可click/type/verify而不搶使用者實體cursor/focus。([GitHub](https://github.com/trycua/cua?utm_source=chatgpt.com))

所以你問：

> Hermes能不能控制使用者現在桌面上的滑鼠鍵盤去操作沒有CLI的XQ？

更精確答案是：

> **可以，而且應優先透過 UIA/window-targeted background actions，而不是單純把實體滑鼠游標搬來搬去。**

必要時才降級到前景input。

---

# 六、但有一個重要限制：你目前 HGK 綁的是 pinned Hermes v0.20.0

目前 HGK User Guide與Fabric AGENTS都把Hermes綁定為：

```text
Hermes v0.20.0
tag v2026.8.3
commit 3c27eb62...
```

Hermes是runtime/orchestrator，而HGK是sole normative control plane。 

官方目前最新release仍是 v0.20.0。([GitHub](https://github.com/NousResearch/hermes-agent/releases?utm_source=chatgpt.com))

但是 Hermes GitHub **main現在已經比v0.20 release本身繼續演進**。

所以不能因為：

> upstream現在支援Windows computer-use

就直接推導：

> 你目前HGK pinned的那個 exact v0.20 runtime已經在你的Windows/XQ上 PASS。

這仍需本機 qualification。

---

# 七、這裡 Fabric 的完成會實質改變我上一輪方案

這是這次最重要的新角度。

你說：

> Hermes、HGK、SQS現在已由完成的Fabric治理。

需要做一個語義上的精確化：

**Fabric不是runtime governor本身；Fabric是 governance / assurance / interop / knowledge contract surface，而HGK才是執行與強制這些contract的唯一control plane。**

Fabric AGENTS明確寫：

```text
Fabric = contract surface
HG-KSEOS = sole governance / normative control plane
Hermes = runtime / orchestrator
Codex = bounded tracked writer
```

而且WorkOrder才是 normative task truth。

Fabric使用說明也明確定義：

```text
policy → HGK consumer
→ WorkOrder / ExecutionBinding
→ Hermes dispatch
→ evidence
```

而不是 Fabric自己建立scheduler。

所以更新後的正確圖不是：

```text
Fabric
→ Hermes
→ UFO
→ XQ
```

而是：

```text
                    Fabric
            governance contracts
            SoD / permission
            capability qualification
            interop / evidence
                    │
                    ▼ consumed by
                  HGK
             sole control plane
                    │
             WorkOrder / Binding
                    │
                    ▼
                 Hermes
               orchestrator
                    │
           XQ Automation Profile
              ┌─────┴─────┐
              │           │
        Cua Driver       UFO²
          primary       fallback
              │           │
              └─────┬─────┘
                    ▼
                    XQ
                    │
                    ▼
              Frozen XScript
```

這個差異非常大。

---

# 八、因此 UFO² 不再需要被簡單判成「不能導入」

我前一輪說：

> UFO²可能形成第二task/orchestration authority。

這個風險仍然成立，**但現在可以被Fabric/HGK架構明確拆解與治理。**

Fabric現在已經具有：

- capability qualification；
- Profile contract；
- SoD；
- promotion；
- acceptance；
- interop；
- MCP/A2A registration；
- ContextForge；
- OASF；
- BreakGlass；
- independent Acceptance Officer。

因此現在更精確的結論是：

> **可以導入 UFO²，但只導入它的 Windows automation capability，不導入它的 task authority。**

---

# 九、UFO²應該被「降格成工具」，而不是再當AgentOS

目前 Microsoft UFO repo把 UFO²稱為 Windows Desktop AgentOS，包含自己：

```text
HostAgent
AppAgent
planning
action dispatch
knowledge
```

目前官方又已把 UFO²列為LTS / stable，UFO³ Galaxy則是active development。([GitHub](https://github.com/microsoft/ufo?utm_source=chatgpt.com))

如果直接整套部署：

```text
HGK planner
→ Hermes planner
→ UFO HostAgent planner
→ UFO AppAgent
```

仍然是錯的。

但 UFO²真正有價值的是下面這些低層能力：

```text
UICollector
AppUIExecutor
HostUIExecutor
Windows UIA
Win32
visual grounding
hybrid GUI/API actions
```

UFO²官方 architecture本身就支援UIA/Win32與visual grounding混合偵測；它的hybrid action layer也支援 API-preferred / GUI-fallback。([GitHub](https://github.com/microsoft/UFO/blob/main/documents/docs/ufo2/overview.md?utm_source=chatgpt.com))

所以更新方案：

> **抽取 executor，不採納 planner。**

---

# 十、Fabric完成後，外部工具的正確身份應該變成 Capability Provider

這同時適用：

- Cua Driver；
- UFO²；
-未來任何XQ native API；
- file watcher；
- OCR/vision fallback。

建議 Fabric裡不要建立：

```text
ufo-agent
cua-agent
xq-agent
```

而建立/註冊：

```text
Capability:
  XQ_DESKTOP_CONTROL

Providers:
  CUA_DRIVER_WINDOWS
  UFO2_WINDOWS_UI_EXECUTOR
```

HGK router最後只會看到：

```text
Capability = XQ_DESKTOP_CONTROL
```

至於選哪個provider：

```text
CUA first
↓ failure
UFO executor fallback
```

不是由產品任務自己決定。

---

# 十一、甚至不一定需要讓 ContextForge 代理每次 GUI call

Fabric現在已經把 ContextForge作為 accepted MCP/A2A interop surface，具有註冊、發現、auth-negative、promotion lineage。

但我不建議為了「Fabric治理」強迫：

```text
Hermes
→ ContextForge HTTP
→ cua-driver MCP
→ XQ
```

每個click都繞gateway。

這會增加：

- latency；
- failure surface；
- audit noise。

高CP值做法是：

### Control plane

```text
Fabric
→ capability contract / policy / registry
```

### Runtime plane

```text
Hermes
→ local stdio MCP
→ cua-driver
```

### Evidence plane

```text
provider/version
manifest
permission mode
action class
result/readback
→ HGK/Fabric receipt
```

只有未來需要跨機器、central discovery或多runtimeinterop時，才讓ContextForge進data path。

---

# 十二、Cua Driver現在特別適合Fabric的一個原因：它已經有 bounded permission mode

Cua Driver current README定義三種模式：

```text
standard
bounded
unrestricted
```

其中：

> `bounded`只允許reviewed manifest裡宣告的tools/resources。

Permission mode在process launch時固定，必須重啟才能改；`unrestricted`則需要顯式 `--dangerously-bypass-approvals`。([GitHub](https://github.com/trycua/cua/blob/main/libs/cua-driver/README.md?utm_source=chatgpt.com))

這跟Fabric的：

```text
Capability Qualification
Profile
Permission
WorkOrder
ExecutionBinding
```

幾乎一一對應。

所以我會把前一輪方案的：

```text
CUA /yolo
```

完全排除。

正式方案改為：

> **CUA bounded mode + Fabric-generated capability manifest。**

---

# 十三、建議的 XQ Desktop Capability Manifest

不要做成幾百條policy。

只需要類似：

```yaml
capability: XQ_DESKTOP_CONTROL
provider: CUA_DRIVER_WINDOWS

allowed:
  - launch_xq
  - focus_xq
  - open_xscript_editor
  - create_script
  - paste_or_import_script
  - compile_script
  - read_compile_result
  - create_automation_strategy
  - configure_symbols
  - configure_parameters
  - configure_radar
  - start_paper_strategy
  - read_runtime_status
  - export_result
  - stop_non_live_strategy

denied:
  - enter_password
  - handle_mfa
  - change_broker_credentials
  - override_risk_limits
  - mutate_frozen_script_after_arm
  - autonomous_live_entry_confirmation
```

這就是Fabric真正該做的事。

---

# 十四、你的交易模式需要新增一個非常重要的 runtime state

目前 SQS User Guide仍明確是：

```text
LOCAL / PAPER / NO-LIVE-WRITE
adapters/xq-read-watch.yaml
watch_only: true
write: false
order_path: HITL_ONLY
```



Stage-3 current prompt也仍明確寫：

```text
sqs_live_trading: NOT_AUTHORIZED
```

並且S1仍是：

```text
LOCAL/PAPER/no-live-write
```



所以：

## 你今天補充的交易模式是「新的A0設計意圖」

**不能假裝它已經在current SQS里被正式授權。**

這需要之後的合法 Stage-3 / SQS ChangeSet把原來：

```text
NO_LIVE_WRITE
```

細分。

---

# 十五、正確的交易權限狀態機應改成這樣

```text
DISARMED
   │
   ▼
SCRIPT_VALIDATED
   │
   ▼
READY_FOR_ENTRY
   │
   ▼
ENTRY_SIGNAL
   │
   ▼
AWAITING_HUMAN_ENTRY_APPROVAL
   │
   ├── reject → DISARMED
   │
   └── approve
          ↓
POSITION_ACTIVE_SCRIPT_OWNED
          │
          ├─ SCALE_IN
          ├─ SCALE_OUT
          ├─ STOP_LOSS
          ├─ TAKE_PROFIT
          └─ FLATTEN
          ↓
POSITION_CLOSED
          ↓
RECONCILIATION
```

在：

```text
POSITION_ACTIVE_SCRIPT_OWNED
```

期間：

```text
Hermes write authority = NONE
LLM trading authority   = NONE
Codex authority         = NONE
```

只有：

```text
Frozen XScript
```

能對position執行。

這正是你的原意應該被正式化的地方。

---

# 十六、HumanGate也應該從「每一張單」改成「Arm Script」

因此我修正上一輪說法。

不是：

> entry / scale-in / scale-out / exit每一次都HumanGate。

按照你現在明確補充的產品設計：

### 正常路徑只有一個交易HumanGate

```text
HUMAN_ENTRY_APPROVAL
```

它同時授權：

> 該版本 XScript在該次position lifecycle內依事前核准條件執行後續管理。

也就是：

```text
Human Approval
        │
        └─ binds:
           script_digest
           FinancialSpec
           Bias/Scenario
           RiskAuthorization
           instrument
           session
           size ceiling
           allowed actions
```

---

# 十七、這樣做有一條必要的不變量：入場後不得hot-patch腳本

如果：

```text
XScript SHA = AAA
```

人批准了AAA。

持倉中Hermes/Codex發現：

> 我覺得應該改止損。

然後把script改成：

```text
SHA = BBB
```

這是絕對不能直接生效的。

規則應是：

```text
script_digest_at_arm
==
script_digest_during_position
```

任何drift：

```text
ARM_INVALIDATED
```

新版本只可用在**下一個position**。

唯一例外應是獨立的：

```text
EMERGENCY_KILL / FLATTEN
```

安全通道。

---

# 十八、這其實讓Computer Use的重要性下降一級

前一輪看起來：

> Hermes computer-use很像是交易automation engine。

現在不是。

它真正的工作是：

## Before position

```text
deploy
compile
configure
arm
```

## During position

```text
observe
health-check
collect evidence
```

## After position

```text
readback
reconcile
journal
repair for next session
```

**真正毫秒/秒級交易execution完全不依賴LLM、MCP或desktop-control latency。**

這是架構上很大的改善。

---

# 十九、所以Hermes/CUA暫時掛掉，也不應影響已啟動交易邏輯

這應成為驗收條件。

例如：

```text
POSITION_ACTIVE_SCRIPT_OWNED
```

時故意：

```text
kill Hermes
kill cua-driver
```

如果XQ/XScript仍依 frozen execution policy完成：

```text
stop
take profit
flatten
```

那才是正確架構。

換句話說：

> **Hermes是control/deployment automation dependency，不是active-position safety dependency。**

這非常重要。

---

# 二十、最新 Hermes/Cua資料也告訴我們：這個隔離非常有必要

Hermes + cua目前已非常有用，但仍不適合放在 live execution fast loop。

官方/官方repo current issues曾記錄：

- Cua wrapper對driver structured responses的脆弱性；
- Windows UIAccess/focus相關失效案例；
- capture / vision integration mismatch等歷史問題。([GitHub](https://github.com/NousResearch/hermes-agent/issues/52951?utm_source=chatgpt.com))

這些並不代表不能用。

它們代表：

> **拿它操作編輯器/設定/部署很好；拿它當止損execution loop很差。**

而你的architecture剛好不用它做後者。

---

# 二十一、資料搬運也應更新：優先 file/native，GUI最後

XQ官方文件本身就說XScript可以把計算結果輸出到文字檔。([XQ全球贏家](https://www.xq.com.tw/xstrader/xslearnmap/?utm_source=chatgpt.com))

因此最小摩擦架構應是：

```text
XQ / XScript
       │
       ├─ local file / log
       │
       ▼
SQS inbound watcher
       │
       ├─ schema
       ├─ timestamp
       ├─ session
       ├─ reconciliation
       └─ journal
```

而不是Hermes每30秒：

```text
截圖
→ OCR
→ 看PnL
```

優先順序應固定：

```text
1. Native/file interface
2. UIA structured control
3. Win32 control
4. visual grounding
5. coordinate/pixel fallback
```

這也與UFO²目前的官方「API preferred / GUI fallback」hybrid action哲學一致。([GitHub](https://github.com/microsoft/UFO/blob/main/documents/docs/ufo2/core_features/hybrid_actions.md?utm_source=chatgpt.com))

---

# 二十二、更新後的工具選型

| 元件 | 新定位 | Priority |
|---|---|---:|
| **Hermes computer_use** | agent-facing desktop tool | P0 |
| **Cua Driver** | Windows desktop primary executor | **P0** |
| **XScript / XQ Auto Trading Center** | live deterministic execution engine | **P0** |
| File/log watcher | XQ→SQS readback | **P0** |
| Fabric Capability Profile | policy/permission/admission | **P0** |
| HGK | sole WorkOrder/control plane | **P0** |
| ContextForge | optional MCP registration/discovery/audit | P1 |
| **UFO² UI executor pieces** | secondary Windows executor | **P1 fallback** |
| UFO² HostAgent/AppAgent | unnecessary duplicated orchestration | **Do not adopt** |
| UFO³ Galaxy | cross-device orchestration; currently unnecessary | Deferred |
| own pyautogui framework | duplicated wheel | Reject |

---

# 二十三、UFO²的最新狀態讓它更適合作「fallback provider」

Microsoft current repo目前把：

- UFO²描述為stable/LTS Windows desktop agent；
- UFO³ Galaxy作active development的multi-device architecture。([GitHub](https://github.com/microsoft/ufo?utm_source=chatgpt.com))

UFO²對 Windows提供：

```text
UIA
Win32
WinCOM
vision grounding
hybrid GUI/API
```

([GitHub](https://github.com/microsoft/UFO/blob/main/documents/docs/ufo2/overview.md?utm_source=chatgpt.com))

所以如果XQ有：

- custom canvas；
- Cua抓不到control；
- UIA tree很差；
- background click不可靠；

那麼：

```text
Provider #1 = CUA
Provider #2 = UFO2 executor
```

是合理的。

不是：

```text
Orchestrator #1 = Hermes
Orchestrator #2 = UFO
```

---

# 二十四、Fabric現在甚至可以正式做provider admission / failover

這是有Fabric後的一個新能力。

可以讓同一個 Capability：

```text
XQ_DESKTOP_CONTROL
```

擁有provider ledger：

```text
CUA_DRIVER_WINDOWS
  state: ACTIVE_PRIMARY

UFO2_UI_EXECUTOR
  state: QUALIFIED_STANDBY

PIXEL_FALLBACK
  state: EMERGENCY_DEGRADED
```

HGK只看：

```text
CapabilityProfile
```

而不是讓SQS或Hermes hard-code某套工具。

這正好符合你現在已完成的：

```text
ROLE != PROFILE != WORKER
```

以及 Fabric capability qualification/profile治理。

---

# 二十五、不要讓外部MCP network-exposed

這個部分 2026-08-11後有非常值得注意的新資料。

Microsoft UFO於近期security advisory披露 Mobile MCP服務如果對 `0.0.0.0`暴露且沒有auth，可以讓remote client直接取得screenshots/UI hierarchy並注入tap/type/control等操作。([GitHub](https://github.com/microsoft/UFO/security/advisories/GHSA-24fq-m9rr-g3mm?utm_source=chatgpt.com))

另外其URL security又有近期IPv6 transition SSRF advisory。([GitHub](https://github.com/microsoft/UFO/security/advisories/GHSA-7hrg-r8xr-p8gr?utm_source=chatgpt.com))

雖然這不是UFO² Windows UI executor本身等同存在相同漏洞，但工程上給出的訊號非常明確：

## XQ computer-use runtime必須：

```text
LOCAL ONLY
```

首選：

```text
stdio
```

其次：

```text
localhost / named pipe
```

禁止：

```text
0.0.0.0
public LAN MCP
Internet-exposed MCP
```

---

# 二十六、完整更新後的最終架構

```text
┌──────────────────────────────────────────────┐
│                    Fabric                    │
│ authority / SoD / capability / risk / audit │
│ interop / knowledge / promotion contracts   │
└──────────────────────┬───────────────────────┘
                       │ consumed
                       ▼
┌──────────────────────────────────────────────┐
│                 HG-KSEOS                     │
│ WorkOrder / ExecutionBinding / Profile       │
│ SharedSpine / Acceptance / Reducer           │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│                   Hermes                     │
│ orchestration / Kanban / checkpoint          │
│ computer_use                                 │
└──────────────┬───────────────────────────────┘
               │
       XQ_DESKTOP_CONTROL
               │
       ┌───────┴────────┐
       ▼                ▼
 Cua Driver         UFO² Executor
 PRIMARY              FALLBACK
       └───────┬────────┘
               ▼
             XQ UI
               │
      deploy / compile / configure
               │
               ▼
        Validated Frozen XS
               │
        Entry Candidate
               │
             HUMAN
               │
          ENTRY APPROVAL
               │
═══════════════╪════════════════
               ▼
      XScript Execution FSM
       │       │       │
     ADD     REDUCE   STOP
       │       │       │
       └── TP / FLATTEN
               │
               ▼
             Broker
               │
               ▼
        Execution Facts
               │
               ▼
        SQS Reconciliation
```

這是我目前認為最正確的版本。

---

# 二十七、正常情況下，用戶實際只需要做什麼？

在這套架構完整 qualification後：

### ① 登入

你自己完成：

```text
XQ credentials
broker credentials
MFA
certificate
```

Hermes不讀、不打字、不保存。

---

### ② Entry HumanGate

Hermes/SQS告訴你：

```text
2330 台積電
Long

TW-ICT Scenario: ...
Entry: ...
Invalidation: ...
Max risk: ...
XS Script: SHA256 ...
Position policy: ...

ARM?
```

你按：

```text
確認
```

或 XQ裡對應的確認操作。

之後：

> **你不再介入正常position lifecycle。**

---

# 二十八、少數例外仍然需要Human

即使目標是兩個人工點，我仍建議保留fail-closed exception：

```text
MFA expired
broker certificate invalid
XQ upgrade broke UI
script/runtime mismatch
XQ crashed while position active
broker reconciliation mismatch
manual emergency kill
unexpected position
risk ceiling breach not covered by script
```

這些不是「正常流程人工」。

它們是：

```text
EXCEPTION_HITL
```

成熟系統不應為了聲稱「100%只點兩次」而自動處理不確定financial side effects。

---

# 二十九、對現有SQS文檔的必要勘誤

目前 SQS Guide仍說：

```text
SOURCE_VALID_NOT_APPLICABLE V1
無 autonomous adapter
xq-read-watch read-only
NO-LIVE-WRITE
```



所以未來施工不能只是：

> 安裝 Cua Driver。

真正應形成一個新的 Stage-3/SQS合法ChangeSet，把XQ能力模型從：

```text
V1:
READ_WATCH_ONLY
```

升成：

```text
V2:
DESKTOP_AUTOMATION
+
ENTRY_HITL_ARMED_XSCRIPT_EXECUTION
```

但：

```text
AUTONOMOUS_AI_TRADING = FORBIDDEN
```

仍然不變。

---

# 三十、建議V2能力分級

### Profile 0 — READ

```text
XQ_READ_WATCH
```

目前已有。

### Profile 1 — DESKTOP CONTROL

```text
XQ_DESKTOP_AUTOMATION
```

可：

- open；
- editor；
- import；
- compile；
- configure；
- run paper；
- readback。

### Profile 2 — SEMI-AUTO LIVE

```text
XQ_ENTRY_HITL_XSCRIPT_AUTONOMY
```

Human批准entry後：

```text
XS manages entire position
```

### Profile 3 — AI Autonomous Live

```text
REJECTED
```

不需要，也不建議。

---

# 三十一、最小施工/驗收順序

不需要大工程。

## G0 — Computer Use Qualification

在你**目前 pinned Hermes**上驗：

```text
hermes computer-use status
computer-use backend identity
Cua exact version
Windows UIA health
```

不能先upgrade latest。

---

## G1 — XQ UI Inventory

逐項驗：

```text
launch
main window
XS editor
script editor
compile
compile error
auto trading center
strategy config
symbol config
parameter config
start/stop
status
export/log
```

每個要：

```text
locate
act
readback
idempotency
failure
```

---

## G2 — Cua Primary

跑100+ deterministic replay，不需要用真錢：

```text
open editor
deploy fixture
compile known-pass
compile known-fail
read error
repair
configure paper
start
stop
export
```

測：

```text
success rate
silent-click rate
selector drift
recovery
```

---

## G3 — UFO² Fallback

只有 G2證明XQ某些control Cua不穩，才qualification UFO executor。

不是一開始就裝兩套。

---

## G4 — XScript Lifecycle

驗證：

```text
Scenario
→ XScript
→ compile
→ backtest
→ paper
→ independent validation
→ freeze digest
```

---

## G5 — HITL Arm

Human approval必須綁：

```text
exact script digest
exact strategy
exact account profile
exact symbol
risk ceiling
session
```

---

## G6 — Position Independence Canary

關鍵測試：

```text
Enter paper position
→ approve
→ position active
→ kill Hermes
→ kill cua-driver
→ XScript仍正常 scale/stop/flatten
```

這可能是整個方案最重要的驗收。

---

## G7 — Reconciliation

```text
XQ/Broker facts
→ SQS
→ ExecutionEvent
→ position
→ cash
→ PnL
→ journal
```

不可依Hermes screenshots當truth。

---

# 三十二、我現在對各項方案的更新評分

| 項目 | 前一輪 | 更新後 |
|---|---|---|
| Hermes computer-use | P0 | **P0，維持** |
| Cua Driver | P0 | **P0 Primary** |
| Full UFO² AgentOS | Reject | **仍不採用** |
| UFO²低層executor | 模糊 | **P1 Qualified Fallback** |
| UFO³ Galaxy | 未評 | **Deferred / unnecessary** |
| ContextForge代理每個click | 可考慮 | **不推薦，過度** |
| ContextForge capability registry | P1 | **有價值** |
| Fabric policy | 輔助 | **正式外部tool governance source** |
| HGK | control plane | **維持 sole control plane** |
| Hermes | orchestrator | **維持，且退出live fast loop** |
| XQ/XS | terminal | **升級：deterministic execution engine** |
| AI盤中decision | 可能 | **明確禁止/不需要** |
| HumanGate每次order | 建議 | **勘誤：正常僅entry arm一次** |
| 後續加減碼/SL/TP | HITL疑慮 | **Frozen XS自動執行** |
| GUI automation可靠性要求 | 高 | **降低，因不在position safety loop** |

---

# 最終工程裁決

你的補充讓架構變得**更好，而不是更危險**。

最終合理形態應是：

> **Hermes/HGK/Fabric/SQS負責「把正確的交易劇本做出來、驗證好、部署到XQ、設定好、監督好、事後對帳好」；真正持倉期間則由已freeze的 XScript mechanically execute TW-ICT position lifecycle。**

因此：

### 你的問題 1

**是。**  
加碼、減碼、止損、止盈、清倉都應由**事先核准的XS腳本**執行，不應再讓Hermes/AI盤中重決策。

### 你的問題 2

**是。**  
Hermes upstream目前已有Windows Computer Use，可透過 Cua Driver對沒有CLI/API的本地APP做視窗、UIA、滑鼠、鍵盤、截圖與readback控制。([GitHub](https://github.com/nousresearch/hermes-agent/blob/main/website/docs/reference/cli-commands.md?utm_source=chatgpt.com))

但：

> **你的 exact pinned Hermes + exact XQ 尚未做runtime qualification，因此目前狀態是 `TECHNICALLY_AVAILABLE / LOCALLY_UNVERIFIED`，不是CURRENT PASS。**

### 你的問題 3

Fabric完成後，我對UFO²的結論更新成：

> **不是「不能導入UFO²」，而是「不能讓UFO²成為第二orchestrator」。**

UFO²的 Windows executor/UIA/Win32/hybrid-detection能力可以作為 Fabric治理下 `XQ_DESKTOP_CONTROL`的 **P1 fallback provider**；HGK仍發WorkOrder，Hermes仍是唯一runtime orchestrator，Fabric提供contract/qualification/SoD，UFO只執行bounded UI actions。 ([GitHub](https://github.com/microsoft/UFO/blob/main/documents/docs/ufo2/core_features/hybrid_actions.md?utm_source=chatgpt.com))

---

## 最值得採取的下一個工程 ChangeSet

不是：

> `FULL XQ AI AUTONOMOUS TRADING`

而應精確命名成：

> **`SQS_XQ_XS_ENTRY-HITL_DETERMINISTIC-EXECUTION_AND_DESKTOP-AUTOMATION_V2`**

它只做兩件真正有價值的升級：

1. **XQ Desktop Automation**
   - Hermes + Cua primary；
   - UFO executor conditional fallback；
   - Fabric/HGK治理。

2. **Entry-HITL → Frozen-XScript position autonomy**
   - Human只批准entry/arm；
   - position lifecycle由XScript全自動；
   - AI永遠不進active-position execution loop。

這比「讓Hermes自己即時交易」更成熟、更簡單，也更符合你目前整套 Fabric → HGK → Hermes → SQS 架構的設計方向。

---
Powered by [AI Exporter](https://saveai.net)