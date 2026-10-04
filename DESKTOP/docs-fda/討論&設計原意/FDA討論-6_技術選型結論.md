# you asked

message time: 2026-08-13 12:27:07

任務目標：
你必須對UFO²  這個技術選型，以「低磨合、高度適合HERMES & XQ全球贏家、快速落地可用、高落地可行性、近三個月都有更新+高討論熱度」為目標， 進行深度研究+交叉分析，UFO²是最佳的選型?或是有其他最佳選項?

任務要求：
你必須針對以上項目，和全部相關資料進行「專業分析+交叉比對+深度整合」，再逐項對以上項目進行大數據搜索"2026年8月11日"以後的最新資料，搜索相關主題的「技術社群論壇(如HERMES HUB / GitHub / XQ全球贏家)、網站、專欄、部落格、專業研究」，並對搜索資料進行「專業分析+交叉比對+深度整合」，再逐項對任務目標進行符合「工程專業實務作法、技術社群成熟技術者共識、不自己重複造外部現有可用輪子、整合導入進3個月熱度高的開源工具/方法」的最佳工程評估鑑定和規劃，並且不過度工程化。

---

# chatgpt response

我會把「最佳選型」拆成兩個不同問題評估：**誰最適合當 Fabric 的共享 Desktop Automation Profile 主體**，以及 **誰最適合當 Hermes 直接呼叫的低摩擦 executor**。這兩個答案不一定是同一個工具；若硬選單一 winner，反而可能犧牲 XQ 實際穩定性。

外部資料已把選型拉得很清楚：**如果只看「Hermes磨合成本」，Cua Driver 明顯領先；如果看「Windows/XQ複雜桌面能力」，UFO²更強；如果看「固定流程的可驗證、模型退出執行迴圈」，OpenAdapt反而是值得保留的第三候選。** 因此這題不宜用 GitHub 熱度選單一品牌，而應用同一組 XQ fixture 實測後決定 primary provider。

# 技術選型結論

**UFO²不是你這個目標下的單一最佳選型。**

如果把你的條件按優先順序排成：

1. **低磨合，直接適配 Hermes**
2. **Windows / XQ 全球贏家實機可用性**
3. **快速落地**
4. **高可靠、可 readback、可 fail-closed**
5. **近三個月仍高度活躍**
6. **能納入 Fabric Profile / Capability / Knowledge Governance**
7. **不重造輪子、不過度工程**

那麼目前最合理的排序是：

> **P0 Winner：Hermes Computer Use + Cua Driver**  
> **P1 Windows/XQ Specialist Challenger：UFO²**  
> **P2 Deterministic Replay Challenger：OpenAdapt**  
> 其他如 Agent S3、Appium Windows Driver、FlaUI、pywinauto不應成為目前主路線。

但這不是說 UFO²價值低。相反：

> **若真實 XQ fixture證明 Cua Driver在複雜 XQ UI、custom control、dialog recovery、application-local workflow 上不穩，UFO²很可能反超成 `fabric-desktop-automation` 的 primary provider。**

因此真正的最佳工程決策不是現在憑名氣指定 UFO²，而是：

> **先用 Hermes-native Cua快速落地；同一組 XQ fixture讓 UFO²挑戰；Fabric依實測結果 promotion primary/standby。**

這正符合 RP-002 的 tool lifecycle：`Consumer Need → Local Evidence → Official Probe → Capability/NFR → Security → Benchmark/Fixture → Selection → Adapter/Pilot → Consumer ACK → Drift/Requalification → Rollback/Exit`；藍圖還明確禁止用 popularity/star count取代 hard gate。

---

# 一、先鎖定 RP-002 對這個選型真正施加的約束

目前 RP-002 已經不是施工前藍圖狀態；Program-wide external report記錄 Stage-2 `K1/D1/C1/H1/O1/B1/F0/CF1/F1/KG1 = ALL PASS`，Stage-3也已完成 Profileization與final external acceptance。

因此新 Desktop Automation能力不應重新設計Fabric，而應走現有：

```text
Consumer Need
→ Fabric Capability Qualification
→ Profile / Distribution candidate
→ HGK WorkOrder
→ ExecutionBinding
→ Hermes
→ provider
→ independent acceptance
→ promotion
```

Fabric registration contract本來就允許：

```text
STACK
PROFILE_DISTRIBUTION
PROFILE
SERVICE
```

並要求 capability、permission、lifecycle、rollback，但 `registration_is_authorization=false`。

同時要守住：

```text
NO_SECOND_ORCHESTRATOR
NO_SECOND_TASK_DB
NO_SECOND_KNOWLEDGE_PLATFORM
TOOL != AUTHORITY
PROFILE != WORKER
```



以及 SQS仍維持 exactly 3 persistent profiles；Desktop Automation不應偷偷變成第四個SQS permanent profile。

所以我們現在其實是在選：

> **`WINDOWS_DESKTOP_AUTOMATION` capability 的 provider**

不是選新的 AgentOS。

---

# 二、第一名：Hermes + Cua Driver

## 為什麼它現在是 P0 winner？

最關鍵原因不是功能最多，而是：

> **Hermes upstream已經直接把 Cua Driver當 Computer Use backend。**

Current Hermes CLI直接提供：

```text
hermes computer-use install
hermes computer-use install --upgrade
hermes computer-use status
```

而 upstream明確說 installer支援 macOS、Windows、Linux。([GitHub](https://github.com/nousresearch/hermes-agent/blob/main/website/docs/reference/cli-commands.md?utm_source=chatgpt.com))

Cua Driver自己也直接提供：

- Windows/macOS/Linux；
- background native desktop control；
- click/type/verify；
- CLI；
- MCP server；
- custom clients；
- Windows PowerShell installer。([GitHub](https://github.com/trycua/cua))

所以對你現有：

```text
HGK
→ Hermes
→ Profile
```

而言，新增Cua幾乎是：

```text
Hermes
→ existing computer_use abstraction
→ Cua Driver
```

而 UFO²則至少還要做：

```text
Hermes
→ new Profile/provider adapter
→ UFO task/config/result mapping
```

因此在「低磨合」這一項，Cua明顯第一。

---

# 三、Cua 的活躍度目前也是最強的一組

截至 **2026-08-13**，Cua releases頁顯示 **2026-08-12**還在產新的 `cua-driver-rs 0.19.4 nightly`，而且同一輪更新包含：

- capability manifests套用至permission profiles；
- lifecycle sessions；
- foreground-focus verification；
- Windows local install skill pack；
- MCP permission validation；
- MCP session ownership修補。([GitHub](https://github.com/trycua/cua/releases))

2026-08-10的stable `cua-driver-rs 0.19.3`也特別修正 Windows VC runtime prerequisite，並提供 x86_64 / arm64 Windows binaries與pin-able installer/checksums。([GitHub](https://github.com/trycua/cua/releases))

這一點和 Fabric非常契合：

> capability manifest / permission profile / exact release / checksum / lifecycle。

所以從「近3個月更新熱度 + Hermes fit」看，目前沒有其他候選比它更直接。

---

# 四、但 Cua 不是無條件勝出

這也是為什麼我**不建議現在就淘汰 UFO²**。

Hermes/Cua Windows路線仍有活躍問題。

例如近期 Hermes issue報告 Windows上 Cua UIAccess helper可能在window change後失聯，導致主driver仍活著但無法capture或interaction。([GitHub](https://github.com/NousResearch/hermes-agent/issues/52951?utm_source=chatgpt.com))

Hermes也曾有 issue指出自己的 `computer_use` wrapper對 Cua responses耦合過深，driver演進可能造成wrapper hard-fail；Windows port讓這問題更明顯。([GitHub](https://github.com/NousResearch/hermes-agent/issues/47072?utm_source=chatgpt.com))

另有 Windows installer stale-lock問題直到近期仍在被追蹤。([GitHub](https://github.com/NousResearch/hermes-agent/issues/71319?utm_source=chatgpt.com))

因此：

> **Cua的優勢是「現在最快接上Hermes」，不是「已證明對XQ最穩」。**

這兩件事要分開。

---

# 五、第二名：UFO² — 我認為它是最值得保留的 XQ specialist challenger

如果評分項目換成：

> **誰最可能把一個複雜、Windows-native、沒有完整外部API的桌面應用操作好？**

我反而會給：

> **UFO²第一。**

Microsoft目前將 UFO²正式定位為：

- Windows-only automation；
- Stable / battle-tested；
- Deep Windows OS integration；
- Hybrid GUI + API；
- easy setup；
- 可成為上層orchestrator的Windows device agent。([GitHub](https://github.com/microsoft/UFO))

其 Windows能力不只是視覺mouse agent：

```text
Windows UIA
Win32
WinCOM
Visual + UIA detection
Hybrid GUI/API
Application-specific AppAgent
Knowledge substrate
```

([GitHub](https://github.com/microsoft/UFO))

對 XQ 這種桌面應用，這個 specialization具有很高潛力。

---

# 六、UFO²對 XQ 最大的技術優勢：Hybrid GUI/API

UFO²的官方 hybrid action設計是：

```text
native API available
→ API

API unavailable / insufficient
→ GUI

同一task可混用
```

它自己也明確指出 GUI-only automation對 UI drift、pixel precision、速度比較脆弱，而native API若可用則應優先使用；UFO²用 MCP把API和UIA/Win32放在同一execution layer。([GitHub](https://github.com/microsoft/UFO/blob/main/documents/docs/ufo2/core_features/hybrid_actions.md))

這非常符合 XQ。

因為 XQ目前官方公開能力本來就主要存在：

```text
XScript
XS Editor
策略雷達
自動交易中心
Log Viewer
simulation
broker integration
```

XQ在 **2026-07-23** 最新 7.20.01 / 3.20.01更新還新增了 XS Log Viewer、自動交易排程等功能；也修復了「XS自動交易長時間停在準備中」等runtime問題。([XQ全球贏家](https://www.xq.com.tw/announce/17342/?utm_source=chatgpt.com))

這說明：

> **XQ desktop自身仍是快速演進中的複雜runtime。**

所以能混合 structured control、Windows native surface、visual recovery 的 UFO²很有吸引力。

---

# 七、XQ本身也證明「真正交易execution不需要GUI Agent介入」

這對選型很重要。

XQ官方定義 XS自動交易時，交易腳本可以控制：

- 買賣方向；
- 委託數量；
- 委託價格；
- 已成交數量與價格；

並直接完成完整自動交易流程。([XQ全球贏家](https://www.xq.com.tw/learning/%E8%87%AA%E5%8B%95%E4%BA%A4%E6%98%93%E4%B8%AD%E5%BF%83%EF%BC%9A%E8%87%AA%E5%8B%95%E4%BA%A4%E6%98%93%E4%B8%AD%E5%BF%83%E5%8A%9F%E8%83%BD%E4%BB%8B%E7%B4%B9%E6%95%99%E5%AD%B8/?utm_source=chatgpt.com))

也就是我們真正要自動化的是：

```text
XQ啟動
XS部署
編譯
策略建立
設定
監看
log/export/readback
```

而不是：

```text
Hermes每次點加碼
Hermes每次點止損
Hermes每次點清倉
```

後者由 frozen XScript負責。

因此 Desktop Automation provider只需要在 **control/deployment plane**夠可靠，不需要達到高頻交易execution等級。

這大幅降低導入門檻。

---

# 八、第三個值得認真看的候選：OpenAdapt

這是本次研究中我認為最值得補進原方案的項目。

OpenAdapt目前的定位不是傳統「GUI agent」，而是：

> **把一次 demonstrated UI workflow編譯成可檢查、可replay的 deterministic workflow。**

官方目前主張：

- Windows / macOS / Linux / RDP / Citrix；
- healthy replay不需要generative model；
- consequential actions做identity gating；
- outcome verification；
- uncertainty直接halt而不是猜。([GitHub](https://github.com/OpenAdaptAI/OpenAdapt))

這種哲學跟 Fabric/HGK非常接近。

---

# 九、OpenAdapt為什麼對金融桌面特別值得注意？

它近期的工程工作非常偏：

```text
wrong-target prevention
identity verification
postcondition mining
safe halt
effect verification
```

2026-07的adversarial validation甚至刻意測：

> 「錯誤entity是否會被agent寫入」

並反覆修改identity matcher來消滅 silent wrong-action。([GitHub](https://github.com/OpenAdaptAI/openadapt-flow/blob/main/docs/validation/VALIDATION.md?utm_source=chatgpt.com))

它的 LIMITS文件也明確承認：

> screen readback只是consistency signal，不是transactional truth；若有read API / system-of-record oracle，應該優先使用。([GitHub](https://github.com/OpenAdaptAI/openadapt-flow/blob/main/docs/LIMITS.md?utm_source=chatgpt.com))

這和 SQS：

```text
XQ UI != Execution Truth
```

的哲學幾乎完全一致。

---

# 十、為什麼 OpenAdapt 沒有排第一？

兩個原因。

### 1. Hermes沒有原生整合

Cua已經在：

```text
hermes computer-use
```

裡。

OpenAdapt必須另外做provider adapter。

---

### 2. Current lifecycle仍是 Beta

OpenAdapt自己把目前 flagship lifecycle標成：

```text
Beta
```

而且 desktop/RDP/Citrix仍採 customer-controlled qualification，並沒有宣稱所有desktop application production-ready。([GitHub](https://github.com/OpenAdaptAI/OpenAdapt))

所以目前適合作：

> **後續把成功的 XQ GUI流程編譯成 deterministic replay。**

而不是第一天就拿它取代 Hermes computer_use。

---

# 十一、這反而可能形成一個很漂亮的未來演進

例如最開始：

```text
Hermes
→ UFO²/Cua
→ 找到XQ操作路徑
```

某個workflow變成熟後：

```text
successful trajectories
→ OpenAdapt compile
→ deterministic workflow
```

之後：

```text
Hermes
→ compiled XQ workflow
→ 0 LLM calls on healthy path
```

只有 drift時才：

```text
halt
→ Hermes/UFO repair
→ requalify
```

這是一個非常成熟的方向。

但我**不建議現在一次導入三套**。

---

# 十二、Agent S3 為什麼不是這裡的 Winner？

Agent S目前研究能力很強。

官方repo在 **2026-07-30**更新，Agent S3論文已被 TMLR 2026接受；repo報告其 OSWorld、WindowsAgentArena等GUI-agent benchmark成績非常強。([GitHub](https://github.com/simular-ai/agent-s))

這代表：

> GUI reasoning能力很有競爭力。

但它對你的case有三個問題。

### 問題1：它本身又是一個agent framework

你已有：

```text
Fabric
HGK
Hermes
Profile
Kanban
```

再加入 Agent S3的hierarchical computer-agent reasoning，整合磨合成本高。

### 問題2：不是Hermes-native

不像 Cua。

### 問題3：你的XQ任務其實多數不是open-ended GUI reasoning

而是：

```text
開editor
部署
compile
配置
readback
```

固定workflow。

不需要一個 OSWorld SOTA agent每次重新reason。

因此：

> **非常強，但不是最佳 fit。**

---

# 十三、Appium Windows Driver

它仍是值得知道的 structured Windows automation工具。

目前 Appium Windows Driver 在 **2026-07-29**還有 v6.1.0 release，因此維護新鮮度不差。([GitHub](https://github.com/appium/appium-windows-driver/releases?utm_source=chatgpt.com))

但是它仍依賴 Microsoft WinAppDriver server，且官方文件說：

- Windows host限制；
- Developer Mode；
- server需要另外安裝。([GitHub](https://github.com/appium/appium-windows-driver?utm_source=chatgpt.com))

WinAppDriver本身是一套 Selenium-like UI testing service，主要面向 UWP/WinForms/WPF/Win32測試。([GitHub](https://github.com/microsoft/winappdriver?utm_source=chatgpt.com))

它的問題不是不好，而是：

> **比較像 test automation driver，而不是 Hermes/Fabric agent automation provider。**

所以要自己補planning/recovery/vision/knowledge。

不如Cua/UFO²。

---

# 十四、FlaUI

FlaUI本身是很好的Windows UIA library：

```text
Win32
WinForms
WPF
Store Apps
UIA2 / UIA3
```

([GitHub](https://github.com/FlaUI/FlaUI?utm_source=chatgpt.com))

它對純 deterministic Windows automation很強。

但：

- .NET-centric；
-沒有 Hermes-native interface；
-沒有agent planner；
-沒有visual recovery；
-需要自己寫adapter/runtime。

它的latest v5.0.0更新了.NET 8與UI automation可靠性，但 release熱度不像Cua這麼高。([GitHub](https://github.com/FlaUI/FlaUI/releases?utm_source=chatgpt.com))

所以它更適合作：

> UFO/Cua遇到某個特定 control時的低層donor。

不是主Provider。

---

# 十五、pywinauto

它仍然是老牌Windows GUI automation library，支援Win32與UIA。([GitHub](https://github.com/pywinauto/pywinauto?utm_source=chatgpt.com))

但latest release是 **2025-01-06**。([GitHub](https://github.com/pywinauto/pywinauto/releases?utm_source=chatgpt.com))

直接不符合你要求的：

> **近三個月都有更新、高討論熱度。**

所以不列主選。

---

# 十六、我的加權選型評分

以下是**工程決策模型，不是上游官方benchmark**。

權重按你的目標：

| 指標 | Weight |
|---|---:|
| Hermes低磨合 | 25% |
| XQ/Windows fit | 25% |
| Reliability / fail-closed potential | 20% |
| 快速落地 | 15% |
| 近3月活躍度 | 10% |
| Fabric治理適配 | 5% |

得到：

| Candidate | Hermes fit | XQ fit | Safety | Landing | Activity | Fabric fit | 加權 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Cua Driver** | 10 | 8 | 7 | 10 | 10 | 9 | **8.85** |
| **UFO²** | 7 | 9.5 | 8 | 7.5 | 7 | 9 | **8.00** |
| **OpenAdapt** | 5 | 7 | 9.5 | 6 | 8 | 9 | **7.05** |
| Appium Windows | 4 | 6.5 | 8 | 5 | 8 | 7 | 6.13 |
| pywinauto | 5 | 7 | 7 | 7 | 2 | 7 | 6.00 |
| FlaUI | 3 | 7.5 | 8.5 | 4 | 4 | 7 | 5.68 |
| Agent S3 | 3 | 6 | 5 | 4 | 8 | 6 | 4.95 |

這個分數只用於**排序qualification優先級**，不能取代XQ真實fixture。

---

# 十七、所以 UFO² 到底是不是「最佳」？

要分三個答案。

## 「Hermes最快落地的最佳」

**不是 UFO²。**

是：

> **Cua Driver。**

因為Hermes直接有computer-use integration。([GitHub](https://github.com/nousresearch/hermes-agent/blob/main/website/docs/reference/cli-commands.md?utm_source=chatgpt.com))

---

## 「最適合複雜 Windows/XQ app-aware automation」

**UFO²很可能是最佳候選。**

特別是：

- complex dialogs；
- non-standard controls；
- UIA + Win32；
- visual grounding；
- application-local recovery；
- application knowledge；
- GUI/API hybrid。

([GitHub](https://github.com/microsoft/UFO))

但需要XQ實證。

---

## 「高風險固定流程執行得最deterministic」

**OpenAdapt是非常有競爭力的後續候選。**

特別是 stable workflow被demonstrate一次後：

```text
compile
→ inspect
→ replay
→ verify
→ halt-on-ambiguity
```

([GitHub](https://github.com/OpenAdaptAI/OpenAdapt))

---

# 十八、因此我不建議「只選 UFO²」

最佳 architecture 是：

```text
Fabric Capability
WINDOWS_DESKTOP_AUTOMATION
            │
            ▼
fabric-desktop-automation
            │
      provider registry
       ┌────┼────┐
       │    │    │
      Cua  UFO² OpenAdapt
       │    │    │
      P0   P1   DEFERRED
```

最初狀態：

```text
Cua:
CANDIDATE_PRIMARY

UFO²:
CANDIDATE_CHALLENGER

OpenAdapt:
DEFERRED_PATTERN_CANDIDATE
```

然後實測。

---

# 十九、不要現在就把 UFO² 設成 fallback

這點也值得修正。

前幾輪我曾說：

```text
Cua primary
UFO fallback
```

現在更精確應是：

```text
Cua = lowest-friction incumbent

UFO² = equal qualification challenger
```

因為我們目前沒有 XQ benchmark證據證明：

```text
Cua > UFO²
```

或：

```text
UFO² > Cua
```

真正的 Fabric做法應是讓兩者跑**同一份受控fixture**。

---

# 二十、真正應該測的 XQ benchmark

不要測OSWorld。

那跟你的產品問題距離太遠。

應測你真的需要的十二件事：

1. launch / locate XQ；
2. select exact XQ window；
3. open XS Editor；
4. locate known script；
5. create/import script；
6. paste exact content；
7. compile known-pass；
8. compile known-fail；
9. extract exact compile error；
10. create/configure PAPER auto-trading strategy；
11. read Log Viewer/status；
12. export/readback / stop paper strategy。

XQ官方最新版本已具備XS Editor、自動交易、Log Viewer與策略排程，所以這些fixture正對真實surface。([XQ全球贏家](https://www.xq.com.tw/feature/?utm_source=chatgpt.com))

---

# 二十一、Benchmark不用過度工程

第一輪不需要1000次。

我建議：

```text
12 workflows
× 10 fresh runs
= 120 workflow runs / provider
```

先比較 Cua vs UFO²。

測：

```text
workflow_pass_rate
silent_wrong_action
detected_failure
mean_recovery_count
median_completion_time
UIA/control coverage
vision_fallback_rate
human_intervention_count
XQ restart recovery
version-drift recovery
```

最重要的不是平均成功率，而是：

```text
SILENT_WRONG_ACTION = 0
```

這跟OpenAdapt近期的adversarial engineering philosophy也是一致的：遇到不能確定identity/effect時halt，而不是把不確定當success。([GitHub](https://github.com/OpenAdaptAI/openadapt-flow/blob/main/docs/validation/VALIDATION.md?utm_source=chatgpt.com))

---

# 二十二、Fabric promotion predicate

我建議第一輪很薄：

```text
silent_wrong_action = 0

critical_flow_success >= 99%
OR
failure always detected before consequential effect

compile_error_readback >= 99%

recovery_after_xq_restart >= 95%

credential_access = 0
live_order_write = 0

provider_route_explicit = 100%
silent_provider_fallback = 0
```

對live path先全部禁止。

這與你目前RP-002的 exact tool-state、no silent fallback、independent acceptance原則一致。

---

# 二十三、如果 Cua 通過，怎麼辦？

最簡單：

> **停止。**

不要因為 UFO²功能很多就把它硬裝進production path。

```text
Cua = ACTIVE_PRIMARY
UFO² = QUALIFIED_OR_DEFERRED
```

即可。

這才叫不過度工程。

---

# 二十四、如果 Cua只有簡單操作可靠，UFO²在複雜flow比較強

則採：

```text
stable known UI actions
→ Cua

complex XQ workflows
→ UFO²
```

Fabric router依fixture-certified action class決定。

不是由LLM自由選。

---

# 二十五、如果 UFO²全面勝出

那就：

```text
UFO² = ACTIVE_PRIMARY
Cua = FALLBACK
```

完全合理。

Hermes原生支持Cua並不是architectural obligation。

Fabric的核心就是：

> provider可以替換，capability/profile contract不變。

---

# 二十六、OpenAdapt什麼時候才導入？

等你累積一批：

```text
stable
repeated
successful
XQ workflows
```

例如每天都會做：

```text
開Editor
更新指定腳本
compile
讀結果
更新某策略設定
```

那時候才評估：

```text
trajectory
→ OpenAdapt compiled workflow
```

如果能把LLM從healthy path移掉，會很有價值。([GitHub](https://github.com/OpenAdaptAI/OpenAdapt))

但現在就一起導入：

> **過度工程。**

---

# 二十七、最終選型表

| 技術 | 最適角色 | 現在裁決 |
|---|---|---|
| **Hermes computer_use** | Agent-facing desktop abstraction | **ACTIVE BASE** |
| **Cua Driver** | lowest-friction executor | **P0 FIRST QUALIFY** |
| **UFO²** | Windows/XQ specialist Profile provider | **P0 PARALLEL CHALLENGER** |
| **OpenAdapt** | deterministic workflow compiler/replay | **P1/P2 DEFER** |
| Agent S3 | open-ended GUI reasoning/research | **NO ADOPT P0** |
| Appium Windows Driver | testing/structured Windows automation | SUPPORT/benchmark donor |
| FlaUI | low-level Windows UIA donor | SUPPORT_ONLY |
| pywinauto | legacy/simple Python UI automation | NO ADOPT |
| UFO³ Galaxy | cross-device orchestration | **NO ADOPT — overlaps HGK/Hermes** |

---

# 最終工程裁決

## UFO²是不是最佳？

**不是「無條件最佳」。**

在你最重視的：

> **低磨合 + Hermes適配 + 快速落地**

這個權重下，**Cua Driver目前比 UFO²更優**，因為Hermes已經原生把它當Computer Use backend，且 Cua在 **2026-08-12**仍有Windows相關nightly更新，當前開發速度非常高。([GitHub](https://github.com/nousresearch/hermes-agent/blob/main/website/docs/reference/cli-commands.md?utm_source=chatgpt.com))

但在：

> **Windows-native複雜桌面app + XQ-specific robustness**

上，**UFO²是目前最有可能勝出的challenger**，因為它有更完整的UIA/Win32/WinCOM/vision/AppAgent/hybrid GUI-API架構，而且Microsoft將UFO²明確維持為Windows automation的LTS stable方案。([GitHub](https://github.com/microsoft/UFO))

所以我現在的正式推薦不是：

```text
SELECT UFO²
```

也不是：

```text
SELECT Cua
```

而是：

```text
FABRIC CAPABILITY:
WINDOWS_DESKTOP_AUTOMATION

QUALIFICATION ROUND 1:
  Candidate A = Hermes + Cua Driver
  Candidate B = Hermes + UFO² Profile Provider

SAME XQ FIXTURE
SAME PERMISSIONS
SAME PAPER/NO-LIVE-WRITE SUBJECT
SAME ACCEPTANCE

→ Fabric selects PRIMARY
→ loser becomes STANDBY or DEFERRED
```

這是**最低風險、最低重工、最高落地成功率**的方式。

如果你要我現在只押一個做「第一個安裝與實測」：

> **先押 Cua Driver。**

如果你問「哪一個更值得為 XQ做完整 Fabric Profile qualification？」：

> **UFO²絕對值得，而且應與Cua同級進第一輪qualification。**

而 OpenAdapt則應留在第二階段：

> **等 XQ操作路徑成熟後，再判斷是否把高頻固定workflow編譯成 model-free deterministic replay。**

這個三層策略，比一開始押單一UFO²更符合 RP-002 的 Capability Qualification、provider替換、no-second-orchestrator、Knowledge/SoD治理與不過度工程原則。

---
Powered by [AI Exporter](https://saveai.net)