# you asked

message time: 2026-08-14 00:15:36

你必須整合前述分析鑑定，再提出完整可執行的升級修補方案。


任務要求：

你必須針對以上項目，和全部相關資料進行「專業分析+交叉比對+深度整合」，再逐項對以上項目進行大數據搜索"2026年8月11日"以後的最新資料，搜索相關主題的「技術社群論壇(如XQ / GitHub)、網站、專欄、部落格、專業研究」，並對搜索資料進行「專業分析+交叉比對+深度整合」，再逐項對任務目標進行符合「工程專業實務作法、技術社群成熟技術者共識、不自己重複造外部現有可用輪子、最新版XQ/XS」的最佳工程規劃，並且不過度工程化。

---

# chatgpt response

我會把方案收斂成可直接丟給 HGK/Fabric 執行的 **focused upgrade package**：不重構 FDA，不新增第三 Heavy Stack，只修「最新版 XQ build fingerprint、action-class 路由、pywinauto native fast path、Cua/UFO fallback、PAPER runtime qualification、evidence/acceptance」。同時我會用 8/11 之後的官方 XQ／GitHub 新資料校正版本與已知 drift。

目前收斂出的修補方向不是「換掉 Cua」，而是**把最新版 XQ 當成會漂移的外部 runtime subject**：每次先辨識 exact build，再只允許該 build 已通過的 `action_class × backend × readback` 組合執行。這樣能直接吸收 3.20.x 已出現過的 copy/paste、策略雷達與自動交易 regression，而不需要重做 FDA。

# Reuse Plan｜最新版 XQ/XS 專用升級修補方案

## 0. 最終工程裁決

整合 FDA r2、目前實跑 evidence、外部 challenge review，以及本輪截至 **2026-08-14 00:15（台北）** 對 XQ 官方公告／官方論壇、Cua GitHub、Microsoft UFO、pywinauto 的重新查證後，我建議**不要重做 `fabric-desktop-automation`**，而是開一個 bounded、focused 的既有 FDA ChangeSet：

```text
PATCH_ID = FDA-XQ-BUILD-AWARE-NATIVE-HYBRID-001

核心目標：
把「固定 provider 優先序」
升級成
「XQ exact-build × action-class × backend × readback」
的 deterministic qualification。

不新增：
- 第三 Heavy Stack
- 第三 AgentOS
- 第二 scheduler
- 第二 task DB
- 第二 Knowledge/RAG
- 第三 FDA Profile
- 新 RP-002 Gate

保留：
Fabric → HGK → Hermes → FDA
one-active-writer
readback/checkpoint
maker != checker
SQS live trading NOT_AUTHORIZED
```

這符合 FDA r2 原本的「reuse first、provider fixture、action-class matrix、XQ version exact readback、affected-edge smallest repair」設計。

### 升級後建議架構

```text
Fabric / HG-KSEOS
        ↓
WorkOrder + ExecutionBinding
        ↓
Hermes / Kanban
        ↓
FDA deterministic router
        ↓
XQ BUILD DRIFT FIREWALL
        ↓
FDA_DESKTOP_CAPABILITY_MATRIX
        ↓
┌───────────────────────────────────────┐
│ fabric-desktop-cua Profile            │
│                                       │
│  native backend → pywinauto Win32     │
│  general backend → Cua Driver         │
│                                       │
├───────────────────────────────────────┤
│ fabric-desktop-ufo2 Profile           │
│  UFO² → complex/visual specialist     │
└───────────────────────────────────────┘
        ↓
ONE ACTIVE DESKTOP WRITER
        ↓
XQ / XScript
        ↓
native/file/log readback
        ↓
Evidence → independent Acceptance
```

**pywinauto 是 backend/library，不新增第三 Profile。**

---

# Evidence｜為什麼現在必須修

## 1. XQ 本身已證明「minor update 也會破壞自動化假設」

XQ 官方目前公開的最新版公告仍是 **3.20.02 / 260731**。這一版的修復清單本身包含大量直接影響 desktop automation 的 regression：更新後複製貼上失效、右鍵複製失效、策略雷達排程未啟動、自動交易長時間停在「準備中」、頁面設定保存異常等。([XQ全球贏家](https://www.xq.com.tw/announce/17400/))

你們 2026-08-13 實跑的 subject 卻明確讀到：

```text
XQLite 3.20.02 (260811)
DAQXQLITEMainWnd
```

並且已因 version drift 將 selector-bound classes 標記為 `REQUALIFY_REQUIRED`。

所以以後：

```text
application.version = 3.20.02
```

**不夠當 qualification identity。**

必須使用 exact build fingerprint。

---

## 2. 8/11 以後確實仍有新的 drift signals

XQ 官方論壇在 **2026-08-12** 有使用者表示剛升級 3.20.02 後，在「沒有交易」的情況下看到交易錯誤訊息；目前沒有官方證據證明原因就是 3.20.02，因此只能視為 drift signal，不能宣告版本 defect。([XQ全球贏家技術支援](https://forum.xq.com.tw/thread/%E4%BA%A4%E6%98%93%E9%8C%AF%E8%AA%A4%E8%A8%8A%E6%81%AF-%E8%A6%81%E5%8E%BB%E5%93%AA%E8%A3%A1%E6%9F%A5%E5%95%8F%E9%A1%8C/))

**2026-08-13** 又有「查詢商品找不到」的回報，而另一位使用者同日表示自己測試正常，這正好顯示某些異常可能是 environment/state-specific，而不是整個版本對所有使用者一致失敗。([XQ全球贏家技術支援](https://forum.xq.com.tw/thread/%E6%9F%A5%E8%A9%A2%E5%95%86%E5%93%81%E6%89%BE%E4%B8%8D%E5%88%B0/))

因此不能採：

```text
XQ 3.20.02 已驗
→ 所有 3.20.02 都相容
```

而要採：

```text
exact local XQ subject
→ exact action qualification
```

---

## 3. Cua 也不應直接丟掉

Cua 在 **2026-08-12** 發布 `cua-driver-rs 0.19.4 nightly`；該 nightly 加入 implicit lifecycle sessions、permission capability manifests，並特別修正「輸入前驗證 foreground focus」。([GitHub](https://github.com/trycua/cua/releases))

Cua 官方同時仍明確把 Driver 定位成 Windows/macOS/Linux 原生桌面 application 的 computer-use driver。([GitHub](https://github.com/trycua/cua))

但是：

```text
0.19.4 = nightly / pre-release
```

官方 release page也明確說 nightly 是 opt-in、可能不如 regular release 穩定，而且不取代 stable update discovery。([GitHub](https://github.com/trycua/cua/releases))

所以正確處置是：

```text
Cua 0.19.3 = current promoted baseline
Cua 0.19.4 nightly = shadow challenger
```

而不是直接升級。

尤其目前沒有 upstream evidence 證明 0.19.4 已解掉你們的：

```text
XQ Afx 新增 button
→ UIA Invoke
→ deadlock
```

因此該 action class仍應優先測 **pywinauto Win32**。

---

## 4. pywinauto適合作「窄 native backend」，而不是新平台

截至本輪查證，PyPI 最新 stable pywinauto 是 **0.6.9**，2025-01-06 發布；它不是近三個月熱門快速迭代框架，因此沒有理由為了追新而採 git main，但它作為成熟、窄用途 Win32 automation library 很適合 current XQ native adapter。([PyPI](https://pypi.org/project/pywinauto/?utm_source=chatgpt.com))

pywinauto 同時有 Win32/UIA backend；但你們真正需要的差異化是：

```text
backend="win32"
```

不是再加一個 UIA wrapper。

因為目前 known defect 就在 UIA Invoke route。

---

## 5. UFO²保持 specialist，不擴權

Microsoft UFO 官方最新 release 仍為 **v3.0.8，2026-08-10**，commit `96983c7`；該 release以 security hardening 為主，包括 command argument policy、HTTP/MCP security、API key environment handling等。([GitHub](https://github.com/microsoft/UFO/releases))

截至本輪搜尋，我沒有在 UFO 官方 release list看到 **8/11 之後**的新版本，因此沒有理由改掉你們目前 `v3.0.8` pin。([GitHub](https://github.com/microsoft/UFO/releases))

你們目前 evidence也明確是：

```text
UFO² v3.0.8
PIN = qualified
effective-load = BLOCKED_HITL
```

原因為 credential/HumanGate。

因此保留原裁決。

---

# Implementation Recipe｜完整可執行施工方案

## STEP 0 — 開 bounded WorkOrder，不重開 RP-002

建立例如：

```yaml
workorder_id: WO-FDA-XQ-002
change_class: PROFILE_CHANGE
parent: WO-FDA-001
objective: XQ exact-build-aware native hybrid qualification
live_broker_write: false
financial_truth_mutation: false
third_heavy_stack: false
new_profile: false
```

施工前 fresh-read：

```text
FDA_DESKTOP_CAPABILITY_MATRIX
FDA_EXECUTION_BINDING
current Cua pin
current UFO pin
current XQ process/product/build
current SQS XQ authority
```

不得因這次修改新增 RP-002 Gate。FDA r2本來就要求所有變更沿現有 HGK/Fabric entry、ExecutionBinding 與 independent Acceptance 執行。

---

## STEP 1 — 建立 `XQ_BUILD_FINGERPRINT`

不要另外建立第二套 XQ SSOT；這個 fingerprint只是一個 runtime qualification subject。

建議 receipt：

```yaml
schema: FDA-XQ-SUBJECT/1

captured_at: ...
subject:
  process_name: daqxqlite.exe
  pid: ...
  main_window_class: DAQXQLITEMainWnd

  product_version: 3.20.02
  product_build: 260811

  exe_path: C:\SysJust\XQLite\...
  exe_sha256: ...
  file_version: ...
  product_ui_version: ...

  architecture: x64|x86
  os_build: ...

surface:
  main_window_title_hash: ...
  native_child_signature: ...
  uia_root_signature: ...

public_release_binding:
  official_public_version: 3.20.02
  official_public_build: 260731
  exact_public_match: false
  disposition: LOCAL_BUILD_QUALIFICATION_REQUIRED
```

### Hard rule

```text
product version相同但build不同
≠ same qualified subject
```

特別是現在 official public `260731` 與 local live `260811` 已經不同。官方公開公告支持前者；後者來自你們 current runtime evidence。([XQ全球贏家](https://www.xq.com.tw/announce/17400/)) 

---

## STEP 2 — 在既有 Capability Matrix 加入 build validity，**不要另造 matrix**

直接升級既有：

```text
FDA_DESKTOP_CAPABILITY_MATRIX.yaml
```

不要新建第二個 `XQ_COMPATIBILITY_DB`。

每個 action row至少增加：

```yaml
action_class: XS_EDITOR_OPEN

subject_binding:
  xq_version: 3.20.02
  xq_build: 260811
  xq_exe_sha256: ...
  fingerprint_digest: ...

profile:
  id: fabric-desktop-cua

executor:
  backend: pywinauto_win32
  version: 0.6.9

selector:
  class: hwnd|win32_control_id|uia|visual|pixel
  selector_digest: ...

readback:
  class: native_window|xq_file|log|filesystem|uia|visual

qualification:
  fresh_runs: 10
  success: 10
  wrong_action: 0
  silent_wrong_action: 0

validity:
  exact_build: true
  invalidated_by:
    - XQ_BUILD_CHANGE
    - SELECTOR_SIGNATURE_CHANGE
```

router繼續讀**promoted matrix digest**，不能依模型記憶決定 route。這是 FDA r2 的既有硬契約。

---

## STEP 3 — 加入 pywinauto，但只當 `fabric-desktop-cua` 的 native backend

先以 stable：

```text
pywinauto == 0.6.9
```

作 qualification candidate；目前 PyPI latest stable就是 0.6.9。([PyPI](https://pypi.org/project/pywinauto/?utm_source=chatgpt.com))

### 不做

```text
新增 fabric-desktop-pywinauto Profile
新增 pywinauto Agent
新增 pywinauto scheduler
```

### 要做

```text
fabric-desktop-cua
├─ executor_backend=cua_driver
└─ executor_backend=pywinauto_win32
```

每一張 receipt都必須明確記：

```text
profile
executor_backend
backend_version
selector class
target XQ fingerprint
```

禁止 silent fallback。

---

## STEP 4 — 寫一個很薄的 `xq_native_adapter`

不要建立 framework。

建議只包：

```python
attach_xq()
get_main_window()
focus_xq()
open_native_menu()
find_native_control()
invoke_native_control()
focus_editor()
type_or_set_text()
send_accelerator()
read_native_window_state()
```

它的責任**只到 deterministic Win32 execution**。

不要讓它：

```text
plan tasks
choose strategy
own WorkOrder
own retry authority
own financial decisions
own acceptance
```

### Selector priority

```text
HWND/process
> control_id/class
> menu/accelerator
> UIA
> visual
> coordinate
```

---

## STEP 5 — 先攻目前真正有 defect 的 action classes

不要把全部 XQ 工作流重寫成 pywinauto。

建立 focused native challenge：

| Fixture | 目的 | pywinauto |
|---|---|---|
| FN01 | locate `DAQXQLITEMainWnd` | Win32 |
| FN02 | 策略→XScript Editor | Win32 menu |
| FN03 | `Afx 新增` button | **Win32 primary challenge** |
| FN04 | editor focus/text | native Edit if exposed |
| FN05 | F6 compile | accelerator/menu |
| FN06 | radar native surface | Win32/UIA experiment |

其中 **FN03 是 P0**。

因為 current evidence已證明：

```text
Cua 0.19.3 UIA Invoke
→ Afx button deadlock
```



如果：

```text
pywinauto Win32 FN03 = 10/10
wrong = 0
silent_wrong = 0
```

立即將這個 action class的 promoted backend改成 pywinauto。

**只改這一列。**

不是宣告：

```text
pywinauto wins XQ
```

---

## STEP 6 — 把 clipboard 從 canonical route 降級

XQ官方已經在 3.20.x 發生過複製貼上 regression，因此不應把 clipboard當 durable selector/input contract。([XQ全球贏家](https://www.xq.com.tw/announce/17400/))

文字輸入優先序改成：

```text
1 native Edit set
2 focus + deterministic keyboard typing
3 clipboard paste — exact-build qualified only
4 visual/pixel fallback
```

所以原：

```text
pixel click
+ clipboard Ctrl+V
+ Ctrl+Tab
```

保留為：

```text
KNOWN_WORKAROUND
NOT_CANONICAL_PRIMARY
BUILD_SENSITIVE
```

---

## STEP 7 — Compile的「真相層」完全不要動

F06/F07 是目前最成熟的路徑之一。

繼續：

```text
execution:
native F6 / menu / qualified click

truth:
CompileStatus
CompileMsg
LastCompileTime
```

你們 current evidence已經用 file readback把 known-good和 known-bad compile都做通，且 F06已有 10/10。

所以即使按鈕位置變了：

```text
execution adapter可以換
truth contract不要換
```

這就是新版 XQ 下最重要的 anti-drift separation。

---

## STEP 8 — Cua `0.19.4 nightly`只跑 shadow challenger

不要覆寫 0.19.3。

建立 shadow lane：

```text
baseline:
cua-driver 0.19.3

challenger:
0.19.4-nightly.20260812.31613035038
```

該 nightly有 Windows x86_64 exact artifact和SHA資訊，並加入 foreground focus驗證與 lifecycle/capability修正。([GitHub](https://github.com/trycua/cua/releases))

只跑 affected fixtures：

```text
F01 launch/focus
F03 editor
FN03 Afx new
FN04 input
F09 radar surface
```

### Promotion條件

```text
10/10
wrong_action = 0
silent_wrong_action = 0
deadlock = 0
focus_mismatch = 0
existing F01/F03 regression = 0
```

由於 upstream明確把 nightly標示為可能較不穩定，**即使跑贏，也先標 `QUALIFIED_CHALLENGER`，不要直接取代 stable baseline**。([GitHub](https://github.com/trycua/cua/releases))

---

## STEP 9 — UFO² dependency隔離與 effective-load closure

目前：

```text
UFO² = v3.0.8
```

可繼續 pin；官方目前也把它列為 latest release。([GitHub](https://github.com/microsoft/UFO/releases))

你前面指出的：

```text
pyautogui
langchain_community
```

如果是 exact UFO runtime import dependency，則：

```text
ALLOW
```

但只允許：

```text
UFO profile-bound runtime dependency
```

不能擴成：

```text
HGK adopts LangChain architecture
```

依賴關係應寫：

```text
fabric-desktop-ufo2
└─ exact UFO v3.0.8 environment
   ├─ pyautogui
   ├─ langchain / langchain_community if exact build requires
   └─ other exact pinned dependencies
```

HumanGate提供credential之後才做：

```text
import smoke
→ UFO entrypoint smoke
→ effective-load
→ bounded target-only fixture
→ network/credential negative
→ disable/rollback
```

目前這仍是 FDA Active 的 blocker之一。

---

## STEP 10 — 把 F09 拆成五個 action classes

這是本次修補的另一個 P0。

不要再用：

```text
RADAR surface open
```

代表：

```text
PAPER runtime qualified
```

改成：

```text
XQ_RADAR_OPEN
XQ_PAPER_CONFIG
XQ_PAPER_START
XQ_PAPER_STATUS_READBACK
XQ_PAPER_STOP
```

因為 XQ官方近期版本歷史已經實際出現：

```text
策略雷達排程未啟動
XS自動交易長時間準備中
```

的 regression。([XQ全球贏家](https://www.xq.com.tw/announce/17400/))

每個 class必須獨立：

```text
>=1 certified backend
10 fresh runs
wrong_action = 0
silent_wrong_action = 0
broker_write = 0
```

這也符合 FDA r2 DoD-17。

---

## STEP 11 — PAPER fixture 必須由 SQS/XQ authority admission

這一段不由 FDA自行放寬。

只允許：

```text
LOCAL
PAPER
SHADOW
NO-LIVE-WRITE
```

需要明確 admission：

```yaml
fixture:
  environment: PAPER
  broker_write: false
  live_account_effect: false
  financial_truth_owner: SQS
  desktop_executor: FDA
```

跑：

```text
config
→ readback
→ start
→ running-state readback
→ stop
→ post-stop readback
```

10×。

目前外部驗收也已經把 PAPER runtime缺口列為 focused blocker，而不是要求重做 FDA。

---

## STEP 12 — 建立 `XQ BUILD DRIFT FIREWALL`

啟動任何 XQ write-capable desktop task前：

```text
CURRENT_XQ_FINGERPRINT
        ↓
PROMOTED_XQ_FINGERPRINT
        ↓
same?
```

### Same

```text
route normally
```

### Different

不全部 FAIL；依 dependency invalidation：

| action 類型 | build 改變時 |
|---|---|
| process/window locate | REQUALIFY |
| Win32 selector | REQUALIFY |
| UIA selector | REQUALIFY |
| clipboard | REQUALIFY |
| pixel coordinate | **INVALIDATE** |
| radar/PAPER | **INVALIDATE + full 10x** |
| file/log schema | SCHEMA PROBE；異常才 invalidate |
| live broker | 永遠 DENY |

這直接延續 current evidence已有的：

```text
REQUALIFY_REQUIRED for selector-bound classes only
```

而不是另造一套 drift framework。

---

## STEP 13 — Router改成 fail-closed，禁止 silent fallback

例如：

```text
ACTION = XQ_SCRIPT_CREATE

build=260811

matrix:
pywinauto_win32 = QUALIFIED
cua_0_19_3_uiainvoke = BLOCKED_KNOWN_DEFECT
ufo2 = QUALIFIED_SPECIALIST

route:
pywinauto_win32
```

如果 pywinauto fail，只有：

```text
known no-side-effect state
+
checkpoint/readback
+
next backend certified
```

才能轉 Cua/UFO。

否則：

```text
STOP
UNKNOWN_STATE
HITL
```

FDA r2明確要求 unknown-state不自動 retry、one active writer與 no silent provider fallback。

---

## STEP 14 — 不要新增不必要的第三 Windows framework

本輪查到：

- `uiautomation`仍是可用的 Windows UIA wrapper，支援有 UI Automation provider的 MFC/WinForms/WPF等。([GitHub](https://github.com/yinkaisheng/Python-UIAutomation-for-Windows?utm_source=chatgpt.com))
- FlaUI也是成熟 .NET UI Automation wrapper。([GitHub](https://github.com/FlaUI/FlaUI?utm_source=chatgpt.com))

但這兩者目前都沒有解決一個 pywinauto Win32 + Cua + UFO² 無法處理的**已證實 XQ gap**。

而且 `uiautomation`仍然主要走 Microsoft UI Automation，對 current Afx `Invoke` defect沒有像 Win32 backend那樣明確的 path diversity。([GitHub](https://github.com/yinkaisheng/Python-UIAutomation-for-Windows?utm_source=chatgpt.com))

因此 current disposition：

```text
uiautomation = REFERENCE_CHALLENGER / NOT_ADOPT
FlaUI        = REFERENCE_CHALLENGER / NOT_ADOPT
WinAppDriver = NOT_ADOPT
new RPA      = NOT_ADOPT
```

**不要為了工具熱度擴大 dependency denominator。**

---

# Governance｜驗收與 SoD

## 1. 新版 qualification unit

以後最小驗收單位必須是：

```text
XQ subject fingerprint
× action class
× profile
× executor backend
× selector class
× readback class
```

不是：

```text
「Cua 已驗過」
```

也不是：

```text
「pywinauto 可以操作 XQ」
```

例如：

```yaml
subject: XQ-3.20.02-260811-<exe_sha>
action: XQ_SCRIPT_CREATE
profile: fabric-desktop-cua
backend: pywinauto_win32-0.6.9
selector: hwnd/control_id
readback: dialog_state
result: QUALIFIED_10_OF_10
```

---

## 2. SoD保持不變

```text
HGK
= authority / repair / WorkOrder

Hermes
= orchestration

FDA router
= deterministic action routing

pywinauto
= native execution only

Cua
= general Windows execution only

UFO²
= specialist execution only

XQ
= XScript/runtime local truth

SQS
= Financial Truth / trading authority

Acceptance Officer
= verify only
```

任何 executor都不得 self-promote。

---

## 3. 需要新增／修改的最小 artifact set

**修改，不新造平行系統：**

```text
MODIFY
FDA_DESKTOP_CAPABILITY_MATRIX.yaml
FDA_ROUTE_CHECK.yaml
FDA_EXECUTION_BINDING.json    # only parent-compatible metadata if needed
fabric-desktop-cua config/runtime contract
independent_checker.py

ADD
xq_native_adapter.py
FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json
FDA_XQ_NATIVE_QUALIFICATION_RECEIPT.json
FDA_XQ_PAPER_RUNTIME_RECEIPT.json
FDA_CUA_0194_SHADOW_RECEIPT.json

TEST
test_xq_build_drift.py
test_xq_native_adapter.py
test_xq_action_router.py
test_xq_paper_runtime_contract.py
```

不要新增：

```text
XQ database
XQ scheduler
XQ knowledge platform
XQ third profile
XQ agent framework
```

---

## 4. Acceptance Officer 必須檢查的新增 predicates

在原 DoD不變前提下，新增 implementation assertions：

```text
xq_subject_digest_present = 1
public_vs_local_build_mismatch_acknowledged = 1

stale_selector_route = 0
stale_pixel_route = 0
silent_clipboard_fallback = 0

executor_backend_explicit = 1
backend_version_explicit = 1

wrong_action = 0
silent_wrong_action = 0

paper_surface_promoted_as_runtime = 0
paper_runtime_10x = PASS

unknown_state_auto_retry = 0
simultaneous_writer = 0
broker_write = 0
```

這些是**原有 acceptance語義的具體化**，不是新 RP-002 Gates。

---

# If-No-Fit｜施工順序與最終 Promotion 條件

## 建議 HGK 按這個順序施工

```text
P0
Freeze current FDA subject
↓
Read XQ exact fingerprint
↓
Patch existing capability matrix schema fields
↓
Add pywinauto 0.6.9 as bounded native backend
↓
Implement thin xq_native_adapter
↓
Run FN01–FN06 10x
↓
Promote only winning action rows

P1
Run Cua 0.19.4 nightly shadow challenger
↓
Do not replace 0.19.3 automatically

P2
HumanGate closes UFO² effective-load
↓
Run specialist qualification

P3
SQS/XQ admits PAPER no-live fixture
↓
F09 split → OPEN/CONFIG/START/STATUS/STOP
↓
10x each applicable class

P4
Router/lease/failover/replay affected regression
↓
security/no-live negative
↓
fresh independent acceptance

P5
Patch docs
↓
regenerate exact evidence manifest
↓
external challenge review
```

---

# Promotion decision

只有以下全部成立：

```text
XQ exact subject fingerprint = bound
stale routes = 0

native action classes:
>=1 backend 10/10

PAPER mandatory action classes:
>=1 backend 10/10

wrong_action = 0
silent_wrong_action = 0
simultaneous_writer = 0
unknown_state_retry = 0

UFO2 effective-load = PASS
credential auto-access = 0

SQS broker write = 0

rollback = PASS
independent checker = PASS
external evidence subject binding = PASS
```

才可重新考慮：

```text
FDA_PROFILE_TEAM_ACTIVE = PASS
```

在此之前繼續：

```text
FDA_BLUEPRINT = PASS
FDA_PROFILE_TEAM_ACTIVE = FAIL_CLOSED
```

這與目前 external challenge review 的 smallest-repair裁決一致。

---

# 最終建議

這次最重要的升級不是「換成 pywinauto」。

而是把 FDA 的 XQ contract 從：

```text
provider → XQ
```

升級成：

```text
exact XQ build
→ action-class compatibility
→ deterministic backend
→ one writer
→ native/file/log truth
→ build-scoped evidence
```

在這個架構下：

```text
pywinauto Win32
= 已知 native/MFC action 的 first-choice backend

Cua
= general Windows / heterogeneous UI backend

UFO²
= complex semantic/visual specialist

clipboard/pixel
= build-sensitive last fallback
```

這比全面換工具穩定得多，也更能應對 XQ 3.20.x 已經證實存在的 GUI、clipboard、策略雷達、自動交易 runtime regression。([XQ全球贏家](https://www.xq.com.tw/announce/17400/))

而 8/12 Cua nightly又顯示 upstream仍在快速改善 Windows focus/lifecycle reliability，所以保留 Cua challenger lane，比把它整套拔掉更符合成熟工程 practice。([GitHub](https://github.com/trycua/cua/releases))

**因此我建議這個修補直接定名為：**

```text
FDA XQ Exact-Build-Aware Native Hybrid Upgrade
```

它是一個**focused patch，不是 FDA v3 重構**。

如果要長期維持這套 XQ automation，我也可以持續監控 XQ 官方公告／論壇與 Cua Windows Driver release，在出現新 XQ build 或新的 confirmed regression 時通知你。

---
Powered by [AI Exporter](https://saveai.net)