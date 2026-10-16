# Community XQ automation solution — XQ-Auto-Writer-Skill (research 2026-08-13)

Found via GitHub search during FAR self-research for FDA DoD-17 (XQ strategy radar
PAPER runtime). A non-official but **live-verified** open-source project that solves
the exact class of problem: driving XQ 全球贏家 UI (XS editor, strategy radar,
screener) programmatically with readback verification.

Repo: `https://github.com/would2000/XQ-Auto-Writer-Skill` (README 58KB, AGENTS.md,
`docs/XQ-OPERATION-CONSTITUTION.md`). Author's changelog claims live verification on
**XQ 3.19.03, 2026-08-02**: alert trigger/non-trigger 1/0 verified, screener 50/0/32,
autotrade smoke on 2330. That is one minor version below our host (3.20.02) — the
methodology transfers; the UIA-deadlock edges below are 3.20.02-specific.

Official GitHub org `sysjust-xq` (嘉實資訊) hosts only script-content repos
(vscode-xs, XS_Blocks, XScript_Preset, XQStrategy) — no API/automation tooling.

## Key control IDs (strategy radar window) — the hard-won constants

```python
# xq_alert.py — toolbar commands (standard ToolbarWindow32, control_id=59392)
NEW_COMMAND    = 17551   # 新增策略雷達
DELETE_COMMAND = 17553
COPY_COMMAND   = 17627   # 複製策略雷達
START_COMMAND  = 17554   # 啟動
STOP_COMMAND   = 17555   # 停止
RADAR_TITLE    = "策略雷達 - XQ全球贏家(個人版)"

# 新增策略雷達 dialog control IDs
name_edit       = 17500   # Edit 名稱
script_edit     = 17202   # Edit 腳本設定
product_static  = 17107   # Static 執行商品 readback (e.g. 台積電(2330))
trigger_combo   = 17035   # ComboBox 觸發設定 (單次洗價模式 / K棒內單次觸發 ...)
toolbar         = 59392   # ToolbarWindow32
search_edit     = 33005   # Edit 搜尋 (strategy list filter)
tab_ctrl        = 17003   # SysTabControl32 (內容/觸發商品/執行紀錄)
grid_strategies = 17001   # MFCGridCtrl strategy list
grid_exec_log   = 17002   # MFCGridCtrl 執行紀錄
param_list      = 45243   # SysListView32 parameter table
param_edit      = 45041   # Edit in-place parameter editor
trigger_tree    = 33035   # Tree 觸發日期節點, label format HH:MM:SS(N)
# 選擇使用腳本 dialog: 自訂 root TreeItem expand -> exact-name TreeItem -> control_id=1 Button
# 選擇商品 dialog: query Edit control_id=741, search Button 802, select 803, ok 1
```

## Toolbar activation via pywinauto (win32 backend) — no mouse, no UIA

```python
from pywinauto import Desktop
d32 = Desktop(backend="win32")
radar = d32.window(title=RADAR_TITLE)
toolbar = radar.child_window(control_id=59392, class_name="ToolbarWindow32").wrapper_object()
def command_index(tb, cid):
    for i in range(tb.button_count()):
        if tb.button(i).info.idCommand == cid:
            return i
def press_command(tb, cid):
    tb.button(command_index(tb, cid)).click()   # win32 TB_PRESSBUTTON — no cursor move
def command_enabled(tb, cid):  # TBSTATE_ENABLED = bit 2 (value 4)
    return bool(tb.button(command_index(tb, cid)).info.fsState & 4)
```

`toolbar.button(i).click()` on the win32 backend sends the toolbar button-press
message — unlike `click_input()`, it does NOT move the real cursor.

## Start/verify pattern (green-light proof, no live trading)

1. `press_command(toolbar, NEW_COMMAND)` → 新增策略雷達 dialog appears.
2. Fill name (Edit 17500), select script via 選擇使用腳本 chooser (自訂 tree),
   select product (2330 → readback 台積電(2330) via Static 17107), set trigger
   mode 單次洗價模式 (ComboBox 17035), readback all four, click ok (control_id=1).
3. **Wash-complete proof**: `command_enabled(START_COMMAND) and not
   command_enabled(STOP_COMMAND)` → single wash finished (strategy auto-starts on
   加入; the START button is not pressed separately).
4. Trigger readback: 觸發商品 tab → Tree 33035 nodes matching `^\d{2}:\d{2}:\d{2}\(\d+\)$`;
   N>0 for a triggering script (red case), N==0 + completed for non-trigger (green
   control case). Evaluated pair: `true_count>0 and false_count==0 and false_completed`.
5. Cleanup: search_exact → verify script+product readback → STOP if running →
   DELETE (17553) → confirm dialog (control_id=1).

`xq_alert.py` runs the whole red/green pair; exit 0 = success, 2 = mismatch,
3 = automation_error. Uses a search-sentinel (`__Codex_Alert_No_Match_7B2E__`) to
prove the strategy list filter works before searching exact names; refuses to
overwrite existing strategies.

## pywinauto dual-backend rules (learned on XQ 3.20.02)

- **win32 backend**: reliable for top-level windows, dialogs by title, standard
  controls by control_id. Use for toolbar commands + dialogs.
- **uia backend**: needed for MenuItems and tree/list descendants. `click_input()`
  on menu items is the community pattern (briefly fronting the app — accepted there).
- **3.20.02 regression vs 3.19.03**: `Desktop(backend="uia").window(
  class_name="DAQXQLITEMainWnd")` succeeds, but any
  `main.descendants(control_type="MenuItem")` traversal **hangs the Afx UIA
  provider** (same deadlock class as cua-driver R-FDA-011). Symptom: script
  timeouts at open_radar even though a minimal exists() probe passes. Workarounds:
  (a) open the radar window via cua-driver background menu click (previously
  verified), then switch to win32 backend for everything inside the radar window;
  (b) close the XS editor to shrink the UIA surface; (c) if the provider is fully
  stuck, restart XQ + cua daemon.
- **Scintilla (XS editor content)**: the editor's source pane is a Scintilla
  control. Set text purely by message: `SCI_SETTEXT=2181` via
  `win32gui.SendMessage(handle, 2181, 0, remote_addr)` with the source in a
  RemoteMemoryBlock (encode CP950 + NUL); verify with `SCI_GETTEXTLENGTH=2183` +
  `SCI_GETTEXT=2182`. This bypasses both UIPI (WM_SETTEXT block) and the keyboard.
  `replace_editor_text()` in xq_compile.py has the full recipe.

## XQ radar state model (from sensor-learning-guide.md distillation)

Seven layers, each needs its own evidence: script compiled → radar references
script/params/frequency/scope → strategy started with clean data prep → `ret`
fires on a wash → XQ records trigger+time → notification sent → (if trading) order
sent. "有訊號" ≠ "已通知" ≠ "已委託" ≠ "已成交". Never let one layer's proof stand
in for the next.

## Version downgrade to 3.19.03: INFEASTBLE (verified 2026-08-13)

When the 3.20.02 UIA deadlock blocks progress, the obvious escape is "downgrade
XQ to 3.19.03 (community-verified)". Do NOT re-investigate — it was checked and
closed:

- **No installer obtainable anywhere**: GitHub repo search (XQLite 3.19 / XQ 3.19.03 /
  xq.com.tw update exe) → 0 hits; official download page (xq.com.tw/download) is
  JS-rendered, exposes no versioned installers; update-server guesses
  (update.xq.com.tw / sysjust.com.tw) don't resolve; no installer cached under
  `C:\SysJust\XQLite` (only `uninst.exe` + runtime installers).
- **Local Backup is user-data only**: `C:\SysJust\XQLite\Backup\20260813-152240\3.18.02\`
  holds User/Data + SHW097 settings (1.8MB), NOT the 3.18.02/3.19.03 binaries.
- **Downgrade risks anyway**: login state (SHW097), XSStrategyCenter.sqlite schema,
  and symbol-list formats may not be backward-compatible.
- Verdict: stay on 3.20.02; work around the UIA deadlock (see pywinauto rules
  above: cua-driver background click to open radar, win32 backend inside the radar
  window, XS editor closed to shrink UIA surface). If the user asks "回推 3.19.03?",
  answer: installer unobtainable, and the workarounds are cheaper.

## Remaining blocker (as of session end 2026-08-13)

DoD-17 closed: parameterized alert script FDA_PAPER_ALERT created + compiled
(DB Sensor table CompileStatus=1). Open: getting the radar window open on 3.20.02
(the uia MenuItem traversal deadlock blocks xq_alert.py's open_radar at
`DAQXQLITEMainWnd` lookup). Candidate next steps, in order: (1) restart XQ, open
radar via cua-driver background menu click (previously verified), then run
xq_alert.py with the radar already open (its open_radar returns the existing
window); (2) win32 WM_COMMAND menu invocation; (3) user manually opens the radar
once (HumanGate assist) then hand off to pywinauto win32.

## Parameterized alert-script template (for red/green control pairs)

```xs
{@type:sensor}
Input: Trigger(1);
SetInputName(1, "1觸發，0不觸發");
if Trigger = 1 then ret = 1;
```
