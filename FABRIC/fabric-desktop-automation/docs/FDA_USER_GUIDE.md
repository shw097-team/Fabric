# FDA（fabric-desktop-automation）完整使用手冊

```yaml
schema: FDA-USER-GUIDE/1
artifact_id: FDA_USER_GUIDE
version: 1.1
subject: fabric-desktop-automation（Windows 桌面自動化 Shared Infrastructure Profile Team）
blueprint: fabric-desktop-automation_藍圖_v2026.08.13-r2
team_artifact: fabric-desktop-automation/TEAM.md
normative_control_plane: HG-KSEOS（HGK）
runtime_engine: HERMES
last_updated: 2026-08-14 (r11)
document_class: OPERABILITY（A-3 class）
external_acceptance: GRANTED (FDA_FINAL_EXTERNAL_ACCEPTANCE_REPORT_2026-08-14_R11_ALL_PASS)
profile_team_active: PASS
accepted_scope: LOCAL / PAPER / NO-LIVE-WRITE
claim_ceiling: 本手冊為操作指引，非 Authority Matrix / WorkOrder truth / 驗收證據；
  FDA 驗收 ≠ 實單交易授權（SQS_LIVE_TRADING = NOT_AUTHORIZED）≠ 生產自主 ≠ 遠端部署
```

---

## 1. FDA 是什麼

**FDA = fabric-desktop-automation**，是 Fabric/HG-KSEOS 下的 **Shared Infrastructure Profile Team**（共享基礎設施 Profile 團隊），提供**受治理的 Windows 桌面自動化能力**——特別是對 **XQ 全球贏家（XQLite）** 這類 Windows 桌面應用的自動化操作。

### 1.1 定位（不是什麼）

| 是 | 不是 |
|---|---|
| 受治理的 Windows desktop 自動化共享能力 | 自動交易系統（SQS_LIVE_TRADING = NOT_AUTHORIZED） |
| 多 provider 的 desktop 操作抽象（Cua / pywinauto / UFO²） | 金融 Truth 來源（Financial Truth 屬 SQS） |
| XQ 讀取/監控/腳本編譯/策略雷達 PAPER 操作 | 第二個 orchestrator / scheduler / task DB / 知識平台 |
| 證據驅動、fail-closed 的桌面操作 | 生產環境自主權（PRODUCTION_AUTONOMY = NOT_CLAIMED） |

### 1.2 核心架構

```text
Fabric / HG-KSEOS
        ↓
WorkOrder + ExecutionBinding（HGK Shared Spine）
        ↓
Hermes（orchestration）/ Kanban（coordination）
        ↓
FDA deterministic router（fda_router.py）
        ↓
XQ BUILD DRIFT FIREWALL（build-aware 路由）
        ↓
FDA_DESKTOP_CAPABILITY_MATRIX.yaml（唯一路由真相）
        ↓
┌────────────────────────────────────┐
│ fabric-desktop-cua  profile        │
│   native backend → pywinauto Win32 │
│   general backend → Cua Driver     │
├────────────────────────────────────┤
│ fabric-desktop-ufo2 profile        │
│   UFO² → complex/visual specialist │
└────────────────────────────────────┘
        ↓
ONE ACTIVE DESKTOP WRITER（fda_lease.py）
        ↓
XQ / XScript（桌面目標）
        ↓
native/file/log readback → Evidence → 獨立 Acceptance
```

---

## 2. 安裝與環境需求

### 2.1 硬體/軟體需求

| 項目 | 需求 |
|---|---|
| OS | Windows 10+（本機驗證環境 Windows 10） |
| 目標應用 | XQ 全球贏家 XQLite（本機驗證版本 3.20.02 build 260811） |
| Python | 3.11（`.venv`） |
| Cua driver | `%LOCALAPPDATA%\Programs\Cua\cua-driver\bin\cua-driver.exe`（0.19.3） |
| pywinauto | 0.6.9（Win32 native backend） |
| UFO² | v3.0.8（specialist，keyless via opencode-go） |
| XQ 登入 | SHW097 已登入（HumanGate，不自動化登入） |

### 2.2 Cua driver 安裝（唯一可用路徑）

```powershell
# install_cua.ps1
$ErrorActionPreference = "Continue"
$scriptPath = "C:\...\var\fda\cua_install_script.ps1"
$out = "C:\...\var\fda\cua_install.log"
Invoke-WebRequest -UseBasicParsing "https://raw.githubusercontent.com/trycua/cua/main/libs/cua-driver/scripts/install.ps1" -OutFile $scriptPath
& powershell -NoProfile -ExecutionPolicy Bypass -File $scriptPath *> $out
```

> 注意：`hermes computer-use install`（auto-installer bug）、`irm ... | iex`（PS5.1 ValidateSetFailure）、`pwsh`（WindowsApps Permission denied）全部失敗——**只有下載 script 後用 `-File` 執行這條路徑可行**。

### 2.3 Daemon 啟動（git-bash 陷阱）

```powershell
# serve_cua.ps1（背景執行）
$env:PATH += ";$env:LOCALAPPDATA\Programs\Cua\cua-driver\bin"
cua-driver.exe serve
```

```bash
# 驗證
export PATH="$LOCALAPPDATA/Programs/Cua/cua-driver/bin:$PATH"
cua-driver.exe status        # daemon is running
cua-driver.exe doctor        # UIA + D3D11 reachable
```

> 陷阱：inline `powershell -Command` 從 git-bash 會被吃掉 `$env:` 與反斜線——**務必寫成 .ps1 檔再 `-File` 執行**。

### 2.4 Python 依賴

```bash
cd "C:\Projects\Agent_Workspace\HG-KSEOS"
env -u PYTHONPATH ".venv\Scripts\python.exe" -m pip install --target ".venv\Lib\site-packages" "pywinauto==0.6.9"
```

> 陷阱：`pywinauto` 需要 `pywin32` postinstall + DLL copy；UFO² 需要 `langchain==0.2.17`（≥0.3 移除了 `langchain.docstore`）。

---

## 3. 核心概念

### 3.1 Action Class（動作類別）

一個 action class = 一個可驗證的桌面操作單元，例如：

| Action Class | 說明 | 資格化狀態 |
|---|---|---|
| `XQ_LAUNCH_LOCATE` | 定位 XQ 主視窗 | QUALIFIED（Cua 10/10 + pywinauto 10/10） |
| `XS_COMPILE_PASS` | XS 腳本編譯成功 | QUALIFIED（Cua 10/10 file-readback） |
| `XS_COMPILE_FAIL_READBACK` | 編譯失敗錯誤讀回 | QUALIFIED（10/10） |
| `XQ_PAPER_CONFIG` | 策略雷達設定 | QUALIFIED_SURFACE（radar open + readback） |
| `XQ_LOG_EXPORT_READBACK` | 日誌/匯出讀回 | QUALIFIED（4/4） |

### 3.2 Provider（執行者）

| Provider | backend | 角色 |
|---|---|---|
| **CUA** | cua-driver 0.19.3（UIA） | 通用 Windows 桌面執行 |
| **PYWINAUTO_WIN32** | pywinauto 0.6.9（Win32 消息） | **MFC/Afx native 首選**（純消息，零滑鼠） |
| **UFO2** | Microsoft UFO² v3.0.8 | 複雜/視覺 specialist |

### 3.3 Qualification（資格化）單位

```text
XQ subject fingerprint × action_class × profile × executor_backend × selector × readback
```

**最小資格化 = 一個 action class × 一個 backend，10 次 fresh runs 全 PASS、wrong_action=0、silent_wrong_action=0。**

---

## 4. Build-Aware 路由（XQ BUILD DRIFT FIREWALL）

### 4.1 XQ 版本真相（重要）

```text
exe file version（1.10.0.0）≠ live product version（3.20.02 build 260811）
```

- **Runtime identity 永遠讀 live UIA surface**（視窗標題 `[版本 3.20.02 260811]`）
- exe file version 只保留為 metadata，**不是 promoted runtime identity**
- 官方 public build（260731）≠ 本機 local build（260811）→ `exact_public_match: false` → `LOCAL_BUILD_QUALIFICATION_REQUIRED`

### 4.2 Fingerprint receipt

每次操作前確認 `FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json`：

```yaml
subject:
  product_version: 3.20.02
  product_build: 260811
  exe_sha256: 6c0c7cbc54a3b5827926866ee8d907718e15eb74cf35e935a8c7ac2a7c9c4abe
  main_window_class: DAQXQLITEMainWnd
public_release_binding:
  exact_public_match: false
  disposition: LOCAL_BUILD_QUALIFICATION_REQUIRED
```

### 4.3 Build 改變時的處置（drift firewall policy）

| Action 類型 | Build 改變時 |
|---|---|
| process/window locate | REQUALIFY |
| Win32 selector | REQUALIFY |
| UIA selector | REQUALIFY |
| clipboard | REQUALIFY |
| pixel coordinate | **INVALIDATE** |
| radar/PAPER | **INVALIDATE + full 10x** |
| file/log schema | SCHEMA_PROBE（異常才 invalidate） |
| live broker | **永遠 DENY** |

---

## 5. 執行者操作指南

### 5.1 硬規則：delivery_mode = background ONLY

> **user-mandated（2026-08-13/14）**：任何輸入操作**只能**用 background delivery。

| ✅ 允許 | ❌ 禁止 |
|---|---|
| cua background click（element_token / ax rung） | cua `delivery_mode: "foreground"` |
| PostMessageW BM_CLICK（dialog 按鈕） | 自寫 `SetCursorPos` / `SendInput` / `SetForegroundWindow` |
| SendMessageW WM_SETTEXT / pywinauto `set_edit_text()` | pywinauto `click_input()` / `set_focus()` / `send_keystrokes()` |
| TB_PRESSBUTTON（toolbar 命令） | pixel-click 作為第一手段 |
| uia `expand()/select()`（pattern） | 在 Win32 dialog 上 SendInput Enter（**XQ 崩潰觸發器**） |

### 5.2 異常處理固定路由（user-mandated）

**任何操作異常 → 第一個動作是 screen_state_check.py（不是重試）：**

```bash
PYTHONPATH="C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages" \
"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Scripts\python.exe" screen_state_check.py
```

它 dump：所有可見視窗（含你的視窗、標記 XQ pid）、每個 XQ 視窗的按鈕文字（抓 確定/關閉/加入 小窗）、cua AX tree、截圖。

### 5.3 fda_router.py（deterministic router）

```python
from fda_router import Request, route, failover

req = Request(
    app="XQ", app_version="XQLite-3.20.02-260811",
    action_class="XS_COMPILE_PASS", risk_class="read_only",
    requires_secret=False, financial_side_effect=False,
    active_position_policy_mutation=False,
)
provider = route(req, matrix)   # 'CUA' / 'UFO2' / 'BLOCKED' / 'HITL'
```

路由規則：
- `requires_secret` → **HITL**（人類輸入 credential）
- `financial_side_effect` → **HITL**
- `active_position_policy_mutation` → **BLOCKED**
- 未在 matrix 中資格化 → **BLOCKED**（不猜測）
- failover 只在 `DETECTED_FAIL` / `SAFE_HALT` 且 alternate certified 時發生

### 5.4 fda_lease.py（one active writer）

```python
from fda_lease import DesktopLeaseManager, LeaseDenied, UnknownState

lease = DesktopLeaseManager()
lease.acquire("session-1", "fabric-desktop-cua")
lease.checkpoint("session-1", "ref-1", desktop_state_digest=...)
lease.transfer("session-1", "fabric-desktop-cua", "fabric-desktop-ufo2")
lease.release("session-1", "fabric-desktop-ufo2")
```

- **second writer → LeaseDenied**（同時只允許一個 desktop writer）
- **unknown state → UnknownState**（永不自動 replay/failover）
- provider 切換必須：readback → checkpoint → known state → lease transfer

### 5.5 xq_native_adapter.py（純消息 adapter）

```python
import xq_native_adapter as na

main = na.find_main_window()              # 定位 DAQXQLITEMainWnd（FN01 10/10）
btn = na.find_child(dlg_hwnd, cid=1)      # 找 dialog 按鈕
na.invoke_button(dlg_hwnd, cid=1)         # PostMessage BM_CLICK（純消息）
na.set_edit_text(dlg_hwnd, cid=17500, value="MyStrategy")  # SendMessage WM_SETTEXT
na.press_toolbar(tb_hwnd, 17551)          # TB_PRESSBUTTON NEW
```

**adapter 責任只到 deterministic Win32 execution**——不做 plan/strategy/WorkOrder/acceptance。

---

## 6. XQ 操作食譜（verified）

### 6.1 開啟策略雷達

```text
cua background click 策略(D) → 策略雷達
（menu popup 會卡 UIA daemon timeout，但動作已生效 → 重啟 daemon 後檢查）
→ 若有「策略雷達開放體驗說明」dialog → 找其 Button（EnumChildWindows）→ PostMessage BM_CLICK
```

### 6.2 新增策略雷達（加入 = 自動執行）

```text
toolbar NEW(17551) → 新增策略雷達 dialog：
  名稱 Edit=17500（set_edit_text，用 timestamp 唯一名稱）
  腳本按鈕=17203 → 選擇使用腳本 dialog：
      樹「自訂 (1)」節點必須先 expand()（3.20.02 quirk）
      選 FDA_PAPER_ALERT → 確定
  商品按鈕=17610 → 選擇商品 dialog：
      query Edit=741 → set_edit_text("2330") → 搜尋 Button=802
      ListItem select → 確認 803 → 1
  觸發模式 ComboBox=17035 → select("單次洗價模式")
  readback：名稱/腳本(17202)/商品(17107)/觸發
  「加入(&A)」Button=1 → 自動開始執行
  → 立即掃描新 dialog（新增成功 = 「時間：[HH:MM:SS]」偽裝窗）→ BM_CLICK 關閉
```

> **「新增成功」dialog 陷阱**：標題是 `時間：[02:00:55]`（像時鐘窗），owner=雷達視窗，按鈕 關閉/取消——不是明顯 dialog 名，容易漏掉。

### 6.3 驗證執行（執行真相 = SensorLog，不是 UI grid）

```text
雷達 UI grid（17001/17002 MFCGridCtrl）uia 不可見（只有 scrollbar 文字）——不要用 UI 驗證執行。

真相層：C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\DAQXQLITE_SHW097_SensorLog.sqlite
  table Table_YYYYMMDD（每日），欄位名是 bytes（需 decode cp950）
  執行狀態機：XSSensorState 2(執行中)→3(計算)→1(完成)
             ExecState 1→2→3→4→5→8
  例：FDAPaperFinal020037 = 14 rows, state {2:8,3:2,1:4}, SymbolID=2330.TW

持久化：XQSensor\SensorList.sqlite（big5/CP950！text_factory=bytes）
  SELECT Name, ScriptName, Symbol, CreateTime FROM SensorList（明確欄位，避免 SELECT * 錯位）
```

### 6.4 Toolbar 狀態語義（fsState 正確讀法）

```text
讀 fsState & 4（TBSTATE_ENABLED）= 執行真相
不要讀 fsState & 2（pressed 視覺位）——XTP 的 pressed 不代表執行中

running = STOP(17555) enabled
single-wash completed = START(17554) enabled AND STOP disabled
```

### 6.5 XS 編輯器腳本編譯

```text
F6（或 menu）觸發編譯 → 讀 DB 真相：
  C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\DAQXQLITE_SHW097_Script.sqlite
  CompileStatus（1=成功, 2=錯誤）、CompileMsg、LastCompileTime
```

---

## 7. 資格化（Qualification）流程

### 7.1 10/10 fresh runs 契約

```text
action class 資格化條件：
  ≥1 provider 10/10 fresh runs
  wrong_action = 0
  silent_wrong_action = 0
  readback 存在（file/log/UIA/native）
```

### 7.2 範例：FN01 XQ_LAUNCH_LOCATE

```python
# 10 次 fresh read-only UIA/native call
for i in range(10):
    hwnd = na.find_main_window()          # pywinauto Win32（FN01）
    assert hwnd and class == "DAQXQLITEMainWnd"
    time.sleep(0.05)
# 結果：10/10 PASS → matrix PYWINAUTO_WIN32 row QUALIFIED
```

### 7.3 Matrix promotion（matrix 是唯一路由真相）

```text
benchmark result → candidate row（DEFERRED→QUALIFIED）
  + qualification_subject_digest
  + workflow_pass_rate: "10/10"
  + wrong_action: 0
  + reason_code
  + evidence_refs
→ independent readback → Acceptance Officer → Fabric promotion
```

Router 只讀 **promoted matrix digest**，不靠模型記憶。

---

## 8. 驗收與證據

### 8.1 DoD-36（藍圖 §10.1）

36 個 DoD predicates 全部 PASS（2026-08-14 現況）：
- DoD-13：UFO² effective-load 7/7（keyless via opencode-go）
- DoD-17：XQ PAPER runtime closure（SensorLog 執行真相，single-wash 10x）
- DoD-18/19：wrong_action=0 / silent_wrong_action=0
- DoD-25：SQS live broker write=0
- DoD-33：independent Acceptance Officer PASS（**final checker 194/194**，evaluator 9009713）
- DoD-35：HGK/SQS consumer binding current（260811 fingerprint）

### 8.0 外部驗收最終結果（r11 ALL PASS, 2026-08-14）

```text
FDA_FINAL_EXTERNAL_ACCEPTANCE_REPORT_2026-08-14_R11_ALL_PASS
EXTERNAL_CHALLENGE = PASS_CHALLENGE
FDA_EXTERNAL_ACCEPTANCE = GRANTED
FDA_PROFILE_TEAM_ACTIVE = PASS
accepted_scope: LOCAL / PAPER / NO-LIVE-WRITE
candidate_root: be576bebe7672093039bfe7dbc265f25aa0a1164
evaluator_sha256: 9009713fd70392d64b84dcf0c1319adb5cfef51d260cd196c831c960f1bbe22e
canonical_manifest_sha256: a349633610e7414024c23f590829433cdcabe68e5ebd9e4aa641a528dc93c0d4
驗收不授權: SQS_LIVE_TRADING / PRODUCTION_AUTONOMY / REMOTE_DEPLOYMENT（維持 NOT_AUTHORIZED / NOT_CLAIMED）
```

### 8.2 外部驗收單一證據 MD（**user-mandated 強制路由**）

> **每次內部驗收完成 → 要給外部驗收時，必須自動彙整單一全量內嵌證據 MD。**

```text
執行 pack_external_single_md.py（skill references/ 或 var/fda/）
  → 產出 FDA_EXTERNAL_FULL_EVIDENCE_<date>.md
  → 全量內嵌：7 個關鍵 receipt 全文 + SensorLog/SensorList raw rows
              + EvidenceManifest 表 + DoD counts + claim ceiling
  → freeze order: HEAD → receipts → tests → fresh checker → manifests
                  → render MD LAST → mirror byte-identical → readback → submit
```

**身份閘門**：你宣稱的 sha256 必須 = 外部 reviewer 實際收到的 bytes。

### 8.3 Independent checker

```bash
cd "C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation"
PYTHONPATH="C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages" \
"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Scripts\python.exe" independent_checker.py
# CHECKER_VERDICT: PASS / checks: 174 / failed: 0
```

---

## 9. 治理與安全邊界

### 9.1 Hard invariants（fail-closed）

```text
HEAVY_STACK_COUNT = 2（HGK + SQS）；FDA_IS_HEAVY_STACK = false
ONE_ACTIVE_DESKTOP_WRITER；SECOND_WRITER = DENY
PROVIDER_SWITCH_REQUIRES: READBACK + CHECKPOINT + KNOWN_STATE + LEASE_TRANSFER
FDA profiles MAY NOT: CREATE_WORKORDER / CHANGE_FINANCIAL_TRUTH / CHANGE_RISK_AUTHORITY
                     / SELF_ACCEPT / SELF_PROMOTE / CREATE_SECOND_KNOWLEDGE_PLATFORM
SQS_LIVE_TRADING = NOT_AUTHORIZED；FDA v1 = LOCAL / PAPER / SHADOW / NO-LIVE-WRITE
credential/MFA entry = HUMAN ONLY；unknown desktop state = BLOCKED_HITL（永不自動 failover）
```

### 9.2 SoD（職責分離）

| 角色 | 權限 |
|---|---|
| HGK | 決定 task 是否存在、owner、write boundary、acceptance、promotion |
| Hermes | claim/dispatch/heartbeat/checkpoint/handoff |
| Cua/pywinauto/UFO² | 執行 bounded desktop action only——**無 project/domain authority** |
| Acceptance Officer | 獨立 fresh read-only context 驗證；**maker 永不 self-accept** |

### 9.3 Credential 處理

- **XQ LOGIN = HumanGate**（本機自動登入視為用戶授權；agent 不觸碰 credential）
- UFO² 用 opencode-go backend（keyless，無需外部 API key）——credential 值禁止入 artifacts/receipts

---

## 10. 疑難排解

### 10.0 異常處置固定路由（第一動作，user-mandated 2026-08-14）

任何操作異常（readback 不符 / 動作看似無效 / dialog 找不到 / timeout / 崩潰 / 意外狀態）：

```text
第一步（禁止直接重試、禁止直接判卡死）
  → python var/fda/screen_state_check.py（SSC-V2）
  → 列全部視窗（含 hidden）+ 每個 XQ 視窗的按鈕 + NEEDS_CONFIRM 標記
  → 關鍵認知：XQ 很少真的卡死——通常是「有沒看見的小視窗」需確認：
     新增成功通知（title "時間：[HH:MM:SS]"）· 停止策略雷達確認 · 警示提示 ·
     「該名稱已被使用」錯誤 dialog（與主 dialog 同 title，以「加入(&A)」按鈕辨識）
第二步 依實況處置
  → 小視窗：PostMessage BM_CLICK 按鈕；XTP 自繪按鈕無效 → PostMessageW(dlg, WM_CLOSE)
  → 用戶視窗蓋住 XQ：純消息照常可用，重跑消息操作（勿點座標）
第三步 重試原操作
```

**全程不和用戶搶鍵盤滑鼠**：只准 PostMessage/SendMessage/pywinauto tb.button(i).click()/
uia pattern/cua background；**禁** click_input/set_focus/send_keystrokes/SetCursorPos/
SendInput/SetForegroundWindow/cua foreground/bring_to_front。

| 症狀 | 原因 | 解法 |
|---|---|---|
| cua UIA Invoke deadlock（Afx 新增按鈕） | R-FDA-011 class（XQ Afx UIA provider 不穩） | 用 pywinauto Win32 native（BM_CLICK/TB_PRESSBUTTON） |
| XQ 崩潰（daqxqlite.exe 消失，Engine 還在） | SendInput Enter on dialog / foreground 操作 | 重啟兩者，驗證 `[SHW097:已登入]`；禁 SendInput/foreground |
| 「新增成功」dialog 沒看到 | 標題是「時間：[HH:MM:SS]」偽裝窗 | EnumChildWindows 找 關閉 button → BM_CLICK |
| SensorList 讀到 None | SELECT * 欄位錯位 / big5 編碼 | 明確欄位 + text_factory=bytes + cp950 decode |
| START 按了沒執行 | 未選中策略列（toolbar 只作用選中項） | 加入流程本身就是自動執行；或選中策略再 START |
| cua get_window_state 空 stdout | daemon 剛重啟 | retry once（2s delay） |
| main 視窗找不到 | title 匹配用 `in` 誤中編輯器 | 用 `.startswith("XQ全球贏家(個人版)")` |
| 操作卡住但其實已生效 | menu popup 卡 UIA daemon | 重啟 daemon 後 EnumWindows 檢查 dialog 是否存在 |

---

## 11. 常見問題（FAQ）

**Q: FDA 可以下單嗎？**
A: 不行。`SQS_LIVE_TRADING = NOT_AUTHORIZED`。FDA v1 只做 LOCAL / PAPER / SHADOW / NO-LIVE-WRITE。SQS 是金融 Truth 與交易 authority。

**Q: 為什麼用 pywinauto 而不用 Cua？**
A: XQ 是 Afx/MFC 老應用，UIA Invoke 對其 toolbar/按鈕會 deadlock（R-FDA-011）。pywinauto Win32 backend 走純消息（BM_CLICK/TB_PRESSBUTTON/WM_SETTEXT），零滑鼠、零焦點，是 MFC/Afx 的 first-choice；Cua 保留為通用 Windows backend；UFO² 為 specialist。

**Q: 為什麼不能直接改 DB 啟用策略？**
A: 直接改 DB（ExecType/Enable）視為繞過 XQ 官方機制，不可行也不合治理。必須走 XQ 官方 UI/機制（警示腳本 → 加入策略雷達 → 自動執行）。

**Q: 如何知道策略真的執行了？**
A: 讀 SensorLog 真相層（DAQXQLITE_SHW097_SensorLog.sqlite Table_YYYYMMDD）——有狀態機紀錄（XSSensorState 2→3→1）才是執行證明。UI grid 不可信（XTP 自繪 uia 不可見）。

**Q: 訂閱需求？**
A: XQ 策略雷達 = 個人版**盤中量化交易模組**（教程 035）。台股進階模組**不含**策略雷達執行。訂閱後自訂策略才持久化執行。

**Q: 外部驗收需要什麼？**
A: 一個**全量內嵌的單一證據 MD**（pack_external_single_md.py 產生）——外部驗收官環境打不開 MEDIA/本地路徑，所有 raw bodies 必須內嵌在 MD 本體。身份閘門：宣稱的 sha256 = 實際提交的 bytes。

---

## 12. 參考資料

- 藍圖：`知識庫\實作相關DOC\fabric-desktop-automation\fabric-desktop-automation_藍圖_v2026.08.13-r2.md`
- Team artifact：`Fabric\fabric-desktop-automation\TEAM.md`
- 能力矩陣：`Fabric\fabric-desktop-automation\FDA_DESKTOP_CAPABILITY_MATRIX.yaml`
- 執行綁定：`Fabric\fabric-desktop-automation\FDA_EXECUTION_BINDING.json`
- Evidence：`Fabric\fabric-desktop-automation\FDA_IMPLEMENTATION_EVIDENCE.md`
- 外部驗收包：`Fabric\evidence\review\FDA_EXTERNAL_FULL_EVIDENCE_20260814.md`
- 目錄樹：`Fabric\fabric-desktop-automation\FDA_DIRECTORY_TREE.txt`（evidence/receipts/ + governance/ 子目錄）
- Skill recipes：`hermes skills\software-development\hgk-governed-execution\references\fda-desktop-automation-cua.md`（§11-15 固定路由/強路由）
- 社群參考：`github.com/would2000/XQ-Auto-Writer-Skill`（toolbar/dialog control IDs）
