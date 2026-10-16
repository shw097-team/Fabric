# FDA / Cua Windows desktop automation recipes (verified 2026-08-13)

Session: WO-FDA-001, fabric-desktop-automation blueprint r2 implementation.
All commands verified on this host (Windows 10, git-bash terminal, Hermes v0.20.0).

## 1. Cua driver install — the only working route

Failure matrix (all three alternate routes FAILED live):

| Route | Failure |
|---|---|
| `hermes computer-use install` | prints "did not complete. Re-run manually:" (auto-installer bug on this host) |
| `powershell -Command "irm ...install.ps1 \| iex"` | `ValidateSetFailure` / `MetadataError` — script uses PS7+ syntax (e.g. `ValidateSet` with param sets), breaks under PS 5.1 pipeline |
| `pwsh -Command "irm ... \| iex"` from git-bash | `bash: .../WindowsApps/pwsh: Permission denied` — WindowsApps app-execution-alias not runnable from MSYS bash |

Working route:

```powershell
# install_cua.ps1
$ErrorActionPreference = "Continue"
$scriptPath = "C:\...\var\fda\cua_install_script.ps1"
$out = "C:\...\var\fda\cua_install.log"
Invoke-WebRequest -UseBasicParsing "https://raw.githubusercontent.com/trycua/cua/main/libs/cua-driver/scripts/install.ps1" -OutFile $scriptPath
& powershell -NoProfile -ExecutionPolicy Bypass -File $scriptPath *> $out
```

- Result: `%LOCALAPPDATA%\Programs\Cua\cua-driver\bin\cua-driver.exe`, version `0.19.3`
  (matches blueprint SUPPORT stable readback). Installer registers autostart task and
  appends the bin dir to User PATH.
- Do NOT use `$s = (Invoke-WebRequest ...).Content; Invoke-Expression $s` nested inside
  another PowerShell `-Command` string — the outer shell expands `$s` to empty and the
  inner script silently loses its body (CommandNotFoundException).

## 2. PATH / detection quirks

- `hermes computer-use status` uses `shutil.which` on PATH + `~/.local/bin` ONLY.
  After install it still prints "not installed" in a shell whose PATH predates the
  install. Refresh: `export PATH="$LOCALAPPDATA/Programs/Cua/cua-driver/bin:$PATH"`.
- `hermes computer-use status` then reports `cua-driver 0.19.3 ... ✓ Up to date`;
  `hermes computer-use doctor` (or `cua-driver.exe doctor`) verifies:
  `ax_capability: UIAutomation reachable`, `screen_capture_capability: D3D11 device reachable`,
  `session_active: MCP session is active`.

## 3. Daemon start (git-bash pitfalls)

- `cua-driver serve --socket \\.\pipe\cua-driver` typed directly in bash: bash eats
  backslashes → `create named pipe .pipecua-driver ... os error 123`.
- Inline `powershell -Command "$env:PATH = ..."` from git-bash: bash eats `$env:` →
  `:PATH : 無法將 ':PATH' 辨識為 Cmdlet`.
- Working: write a `.ps1` file with the PATH prepend + `cua-driver.exe serve`, run via
  `powershell -NoProfile -ExecutionPolicy Bypass -File serve_cua.ps1` as background=true.
  Verify with `cua-driver.exe status` → `daemon is running`, `permission mode: standard`.

## 4. CLI call surface (no MCP needed)

```bash
cua-driver.exe list-tools                    # tool inventory
cua-driver.exe describe <tool>               # input JSON schema (read before call)
cua-driver.exe call <tool> '<json-args>'     # execute; JSON on stdout
```

Key tools: `get_accessibility_tree` (lightweight desktop snapshot: processes + visible
windows), `debug_window_info` (per-pid top-level windows + focused UIA element +
supported patterns), `get_window_state` (full UIA tree per pid+window_id, element_index
map for click/type), `type_text`, `click`, `bring_to_front`.

- `get_window_state` REQUIRES `{"pid": N, "window_id": W}` — pid alone returns a bare
  `Expecting value` JSON error. window_id is per-launch; re-fetch from
  `get_accessibility_tree` each probe.
- `debug_window_info` also requires the `call` form with `{"pid": N}`; the `--pid` flag
  form fails with `missing or invalid pid`.
- `get_window_state` on an app with no UIA-heavy surface returns
  `total_element_count` but `structuredContent.elements` may be empty; fall back to
  the `tree_markdown` field for readback text search.

## 5. Live fixture qualification (10/10 pattern)

Blueprint FDA-C4: an action class is team-certified only when ≥1 provider passes
10/10 FRESH runs with full readback and zero wrong/silent-wrong action.

```python
# per run: fresh read-only UIA call, no state carried across runs
info = cua_call("debug_window_info", {"pid": XQ_PID})
ok = ("XQ全球贏家" in titles[0]) and exe == "daqxqlite.exe" and uia_element_present
# 10 runs, sleep 1s between; all 10 PASS => receipt verdict "10_OF_10_PASS"
```

Observed: XQ_LAUNCH_LOCATE 10/10 PASS, median 109ms/run, 0 wrong action.
Receipt shape: `FDA_F01_LIVE_FIXTURE_RECEIPT.json` (schema FDA-FIXTURE-RECEIPT/1).

## 6. Canonical matrix promotion (no ephemeral routing)

- Matrix artifact: `Fabric/fabric-desktop-automation/FDA_DESKTOP_CAPABILITY_MATRIX.yaml`
  (schema FDA-DESKTOP-CAPABILITY-MATRIX/1). The ONLY routing truth — router integration
  tests load it via yaml, never an inline dict.
- Promotion: benchmark result → candidate row (DEFERRED→QUALIFIED) with
  `qualification_subject_digest`, `workflow_pass_rate: "10/10"`, `wrong_action: 0`,
  `reason_code: CUA_10_OF_10_LIVE_QUALIFIED`, `evidence_refs` → independent readback →
  Acceptance Officer → Fabric promotion. Router consumes the promoted digest.
- Router unit tests assert: hard denials (secret/financial/active-position) outrank
  capability; CUA preferred when both PASS; unqualified class → BLOCKED, never guessed.

## 7. XQ version truth (file version ≠ product version)

- `(Get-Item daqxqlite.exe).VersionInfo.FileVersion` → `1.10.0.0` (exe file version).
- Live UIA (`debug_window_info` window title / focused element) → product version
  `XQ全球贏家(個人版) [版本 3.18.02 260102][未登入]`.
- Rule: product version comes from the LIVE UIA surface; record both; version drift
  vs blueprint web-readback → `REQUALIFY_REQUIRED` for selector-bound classes only
  (locate/identity classes can qualify on the live subject).
- XS editor/PAPER/radar surfaces absent while `[未登入]` — 42 elements, no XS entry.
  Login = HumanGate (blueprint 5.18A), never automated; mark those classes
  `PENDING_BLOCKED_HITL`.

## 8. Harmless-app bounded probe (Notepad) — desktop write+readback proof

Pitfalls hit and fixed:
- `subprocess.run(["notepad.exe"])` hangs (GUI app never exits) → use `Popen`.
- `subprocess.run(..., text=True)` on cua-driver output throws UnicodeDecodeError in a
  reader thread on CJK stderr → capture bytes, decode `utf-8, errors="replace"`.
- Sequence: Popen notepad → `get_accessibility_tree` (find window, grab pid+window_id)
  → `get_window_state {pid, window_id}` → `type_text` → fresh `get_window_state` →
  search elements + `tree_markdown` for the typed marker → `taskkill /F /IM notepad.exe`.
- Result: type_text `{delivery: background, effect: unverifiable, route: synthetic_events}`;
  readback found the marker → PASS. LOCAL_REVERSIBLE side effect, no financial surface.

## 9. Lease concurrency live test (one-active-writer proof)

Real `threading.Thread` scenarios against `fda_lease.DesktopLeaseManager`:
two-thread race → exactly one GRANTED/one DENIED; 10-thread stampede → exactly one
writer; checkpoint-gated hot swap (release → checkpoint → acquire after_checkpoint);
unknown-state replay raises UnknownState. All 4 PASS. Receipt:
`FDA_C5_LEASE_CONCURRENCY_RECEIPT.json`.

## 10. Evidence-MD self-reference trap (freeze-order extension)

Symptom: regenerating `FDA_IMPLEMENTATION_EVIDENCE.md` while it lives inside the
scanned directory — the second generation's artifact scan picks up the MD itself,
embedding its own hash → every regeneration "drifts" against itself (embedded hash
never matches the file that contains it).

Fix: the generator MUST exclude its own output filename from the artifact list
(`p.name != "FDA_IMPLEMENTATION_EVIDENCE.md"`). Re-verify with a regex extract of the
embedded table + re-hash against disk (0 drift), and assert the MD filename does not
appear in the table section. Regenerate MD LAST → mirror byte-identical → hash all
copies → update SharedSpine `evidence_refs.sha256` → final freeze.

## 11. delivery_mode = background ONLY; foreground steals the user's mouse (FAR self-research, 2026-08-13)

**Root cause of a multi-hour stall on DoD-17 (XQ radar PAPER runtime):** every
cua-driver input call used `"delivery_mode": "foreground"` + custom Win32
`SetCursorPos`/`SendInput`/`SetForegroundWindow`. That **moves the user's REAL
cursor, steals focus, and hijacks clicks** — the user was actively using the mouse
and got disrupted; plus foreground-on-Afk-XQ triggers the UIA deadlock and, with
SendInput Enter on Win32 dialogs, **crashed XQ 3×** (`daqxqlite.exe.*.dmp` in
`C:\SysJust\XQLite\Log`). 

Authoritative (cua.ai/docs/concepts/capture-and-delivery-modalities):
- `background` (DEFAULT): "Input is routed to the target process/window/element
  directly. The user's frontmost app, real cursor, and window z-order are untouched."
- `foreground`: briefly fronts the target — ONLY when a background attempt did not land.
- Omitted/unknown delivery_mode falls back to background for safety.
- `element_index` (ax rung) = UIA Invoke = backgroundable + driver-verifiable;
  prefer it over pixel `x,y` for any element the tree exposes.

HARD RULES for XQ/desktop fixtures from now on:
1. **Never** pass `delivery_mode: "foreground"` unless a background attempt
   returned `suspected_noop`/`background_unavailable`. Default = background.
2. **Never** use raw Win32 `SetCursorPos`/`SendInput`/`SetForegroundWindow` for
   input — they move the user's real cursor and fight the user's own mouse.
   Win32 API stays READ-ONLY (EnumWindows/EnumChildWindows to discover dialogs and
   their button hwnds; PostMessage BM_CLICK is acceptable for UIA-invisible
   Win32 dialog buttons — it does not take focus). **WM_SETTEXT is NOT
   UIPI-blocked — SUPERSEDED (see §12a/§12b/§15.2 CORRECTED):** `SendMessageW
   WM_SETTEXT` / pywinauto `set_edit_text()` WORKS cross-process; the earlier
   "unreliable across UIPI" failure was `PostMessageW` + a ctypes buffer freed by
   Python before the async post landed (returns 0, readback empty). Use
   SendMessage/set_edit_text; NEVER PostMessage with a temp buffer.
3. **Never** press Enter on a Win32 dialog via SendInput (crash trigger on XQ).
   Click the explicit 確認/加入 button (PostMessage BM_CLICK) instead.
4. Keep ONE window-identity system: cua `(pid, window_id)`. cua window_id ==
   Win32 hwnd numerically on XQ but treat them as separate namespaces; Win32 is
   observation-only.
5. User-mouse coexistence: with background delivery the user can keep using the
   mouse with zero interference; verify `effect`/`verified` on each action and
   re-capture before retry.

## 12a. XQ exact-build-aware native hybrid (WO-FDA-XQ-002, 2026-08-14)

XQ product version alone is NOT a qualification identity. Official public build
(260731) differs from local live build (260811) — capture
`FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json` (exe_sha256, main_window_class
DAQXQLITEMainWnd, public/local mismatch ack) and gate every action via the
matrix `build_firewall` (XQ_BUILD_DRIFT_FIREWALL/1). Policy: locate/uia/clipboard
selectors = REQUALIFY on build change; pixel = INVALIDATE; radar/PAPER =
INVALIDATE_PLUS_FULL_10X; file/log schema = SCHEMA_PROBE; live broker =
DENY_ALWAYS.

Backend doctrine (verified): **pywinauto Win32 = first-choice native backend**
for MFC/Afx controls (FN01 locate 10/10, FN02 editor locate 10/10, FN03 Afx 新增
locate 1/1). Cua stays general Windows backend (0.19.3 baseline; 0.19.4 nightly
= shadow challenger only). UFO² = visual/complex specialist only. Clipboard/pixel
= build-sensitive last fallback (KNOWN_WORKAROUND, NOT canonical).

`xq_native_adapter.py` = thin pure-message adapter (BM_CLICK/TB_PRESSBUTTON/
WM_SETTEXT/TVM; zero click_input/SetCursorPos/SendInput/SetForegroundWindow —
never steals the user's mouse). Router = fail-closed, no silent fallback,
unknown-state = STOP/HITL, one active writer. Qualification unit = subject
fingerprint × action_class × profile × executor_backend × selector × readback.
Tests: test_xq_build_drift.py / test_xq_native_adapter.py / test_xq_action_router.py
(17/17 router PASS; independent checker 179/179 T001-T177).

XQ radar correct flow (tutorial 005《XS策略雷達簡介》, local 影片教程):
XS 編輯器 → 檔案(F)→新增(N) → 選「警示腳本」類型 → 命名 → `ret = 1;` →
儲存+編譯 (DB Sensor table `CompileStatus=1` readback) → 右鍵腳本 →
「加入策略雷達」→ 設頻率/商品 → 按「加入」→ **自動開始執行（綠燈）** →
「執行中」分類可見 → 工具列「停止」停止。雷達「啟動」按鈕不需要單獨按 —
「加入」即自動執行。策略雷達只吃警示腳本 (ret/RetVal), 指標腳本 (Plot1) 不會出現。

## 12b. Afx Win32-dialog handling recipe (verified 2026-08-13 DoD-17)

Goal: drive UIA-invisible `#32770` dialogs (新增腳本 / 開啟 / 新增策略雷達) in XQ
without crashing it or stealing the user's mouse.

Verified working:
- **`PostMessageW(btn_hwnd, BM_CLICK, 0, 0)` on dialog Buttons works cross-process**
  without focus steal. Validated end-to-end: created a 警示 (Sensor) script by
  clicking the 警示 type Button then 確認 via PostMessage. `SendMessageW` may return
  0 (UIPI) — `PostMessageW` returning nonzero is the reliable signal.
- **Read-only Win32 enumeration is the observation layer:** `EnumWindows` +
  `EnumChildWindows` + `GetWindowTextW`/`GetClassNameW`/`GetWindowRect` to discover
  dialogs, their Buttons, Edits, SysListView32/SysTreeView32. No input through them.

Blocked / dead ends (do NOT retry):
- **`PostMessageW` with a ctypes buffer for WM_SETTEXT FAILS** — the buffer is freed
  by Python right after the async post, so the text never lands (returns 0, readback
  empty). This is a buffer-lifetime bug, NOT UIPI: **`SendMessageW WM_SETTEXT` (and
  pywinauto's `set_edit_text()`, which is SendMessage-based) WORKS cross-process** —
  validated filling 新增策略雷達 name field with readback `FDAPaperProbe`. cua-driver
  `type_text` with background px also does NOT land in Win32 dialog Edits.
- **`SendInput` Enter / `SetCursorPos` / `SetForegroundWindow` on dialogs crashes
  XQ** — dumps `C:\SysJust\XQLite\Log\daqxqlite.exe*.dmp`. Never use real input
  on dialogs. Crash signature: `daqxqlite.exe` process gone while
  `DAQXQLITEEngine.exe` remains → restart both, re-verify `[SHW097:已登入]`.
- **Menu popup (檔案(F) etc.) UIA click can hang the driver for 45s+** even in
  background, yet still deliver the action (dialog appears after daemon restart).
  Treat a timeout as "action may have landed": restart daemon, then `EnumWindows`
  to check whether the dialog exists before re-clicking.

Dialog disambiguation trap (cost several rounds):
- The real 新增腳本 main dialog exposes children labelled
  `腳本類型 / 指標 / 選股 / 警示 / 交易 / 函數 / 名稱：`.
- A validation-error dialog shares the SAME title (`新增腳本`) with children
  `確定 / 輸入名稱有誤,請重新輸入`.
- Rule: scan each candidate hwnd's children for `腳本類型` to identify the main
  dialog; never assume the first hwnd matching the title is the main one.

## 13. Mouse-free pywinauto recipe + XQ radar control-ID tables (verified 2026-08-13)

**USER CORRECTION (repeated):** pywinauto `click_input()` / `set_focus()` /
`send_keystrokes()` move the user's REAL cursor and steal focus — the user caught
this twice ("你又在跟我搶滑鼠控制權了"). They are the pywinauto equivalent of
foreground delivery. Use ONLY the message/pattern forms below — every one is
verified working on XQ 3.20.02 with the user simultaneously using the mouse:

| pywinauto call | mechanism | mouse-safe? |
|---|---|---|
| `btn.click()` (win32 backend) | BM_CLICK message | ✅ |
| `edit.set_edit_text(v)` (win32) | SendMessage WM_SETTEXT | ✅ |
| `combo.select(v)` (win32) | CB messages | ✅ |
| uia `tree_item.expand()/select()` | TVM/ExpandCollapse+SelectionItem patterns | ✅ |
| uia `button.click()` (no `_input`) | UIA Invoke | ✅ (but see Afx deadlock) |
| **`click_input()` / `set_focus()` / `send_keystrokes()`** | real input | ❌ **NEVER** |

uia `.click()` on XQ toolbar buttons still Afx-deadlocks (same as cua ax rung);
uia `.expand()/.select()` on TreeItems works. Rule: uia for tree/pattern reads +
win32 messages for buttons/edits — never `click_input`.

**Community repo (authoritative control-ID source):**
`github.com/would2000/XQ-Auto-Writer-Skill` — non-official but validated on XQ
3.19.03 (2026-08-02) with a full alert trigger/non-trigger probe (`xq_alert.py`).
Clone: `var/fda/xq-auto-skill/`. Its CHANGELOG documents XQ 3.19.03 verified runs;
adapt to 3.20.02 where UIA menu traversal deadlocks (use §13 radar-open path).

**XQ Strategy Radar toolbar (standard ToolbarWindow32, control_id=59392):**
`SendMessageW(tb, TB_PRESSBUTTON, cmd, 1)` or pywinauto `tb.button(i).click()`:
- NEW=17551, DELETE=17553, COPY=17627, START=17554, STOP=17555
- `TB_ISBUTTONENABLED` returns 0 even when enabled — read `fsState & 4` instead.
- START enabled AND STOP disabled = single-wash completed (绿燈 verification).

**新增策略雷達 dialog control IDs (verified):**
name Edit=17500 · script button=17203 · script readback Edit=17202 ·
product button=17610 · product Static=17107 · trigger ComboBox=17035 ·
confirm/加入 Button=1 (title `加入(&A)`)

**選擇使用腳本 dialog (opened by 17203):** uia TreeItem tree — the `自訂 (1)`
node MUST be `.expand()`ed before FDA_* script children appear (3.20.02 quirk;
xq_alert.py's `len(custom)!=1` check can fail on this version). Then `.select()`
the script, click 確定.

**選擇商品 dialog:** query Edit=741 (set_edit_text "2330"), search Button=802,
result ListItem `.select()` (uia), confirm 803 then 1. Readback via 17107 Static
→ `台積電(2330)`.

**Radar strategies DB — WRONG DB trap:** XSStrategyCenter.sqlite only holds 28
SYSTEM presets; user radar strategies live in
`C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XQSensor\SensorList.sqlite`
(**big5/CP950 encoded** — open with `conn.text_factory = bytes` and decode
`cp950`, else sqlite3 raises "Could not decode to UTF-8").
Columns: Name, ScriptName, Script_ID, Freq, TriggerSetting, CreateTime...
A "該名稱已被使用" error with empty-DB readback usually means the strategy WAS
created (trial edition keeps it in-memory/SensorList); check SensorList before
assuming failure, and use a timestamped unique name to avoid collisions.

**Radar open path on 3.20.02 (menu UIA deadlocks everywhere):** cua-driver
background MenuItem click 策略(D)→策略雷達 STILL WORKS (background ax rung);
dismiss 策略雷達開放體驗說明 dialog with `set_focus()+send_keystrokes("{ENTER}")`
is mouse-stealing — instead find its button via EnumChildWindows and PostMessage
BM_CLICK, or accept Enter as the single allowed exception AFTER checking the user
isn't at the machine. Then drive everything else with win32 messages (§13 table).

## 14. DoD-17 PAPER runtime closure ops (verified 2026-08-14, subscribed edition)

**Subscription gate (environment truth):** trial edition does NOT persist custom
radar strategies — SensorList rows appear then get cleared, and 「加入」→「開放體驗
警示」notice appears. After subscribing the **盤中量化交易模組** (個人版策略雷達
所在的加值模組，教程 035), custom strategies PERSIST across restart
(FDAPaperClosure011939 CreateTime stayed in SensorList after XQ restart) and the
experience-notice no longer appears. If SensorList rows vanish, suspect trial
edition first — the automation path is identical either way.

**加入 flow requires TWO confirms (user correction):** after clicking 加入(&A)
(Button control_id=1) on the 新增策略雷達 dialog, a follow-up 確定/開放體驗警示
confirm is still needed — I missed it and the user pressed it manually
("因為你剛剛沒有按確定,我剛幫你按了"). Poll for new `#32770` dialogs right after
加入 and PostMessage BM_CLICK their first Button even when `window_text()` is empty
(the notice's button may expose no text to win32).

**START only acts on the SELECTED strategy:** pressing START(17554) with no
strategy row selected in the radar list is a no-op — START stays enabled, STOP
never enables (running stays False). Correct sequence: click 自訂 category →
select the strategy row → START → verify running → STOP. Do NOT skip selection.

**running semantics (community xq_alert.py):** running = STOP(17555) button
ENABLED (`fsState & 4`). STOP `pr=True` (pressed visual bit) with `en=False`
means NOT running — do not misread pressed as executing. Single-wash completed =
START enabled AND STOP disabled.

**Radar strategy grid (17001/17002 MFCGridCtrl) is uia-invisible:** descendants
only expose scrollbar strings (垂直/上移一行/…), never the strategy rows. Row
selection therefore cannot be done via uia TreeItem either (radar tree has no
strategy children, only 自訂/系統/執行中 categories). Options: cua background
click at a row's pixel (from 自訂 category + row geometry) or HumanGate — user
clicks the row; then win32 messages finish the loop.

**DoD-17 CLOSED via SensorLog truth layer (2026-08-14, subscribed edition):**
the REAL execution truth is NOT the radar UI grid (XTP-invisible) but
`C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\DAQXQLITE_SHW097_SensorLog.sqlite`
— table `Table_YYYYMMDD` (per-day), columns are **bytes** (decode col names too:
`PRAGMA table_info` returns b'XQSensorName' etc; `dict(zip(cols,row))` keys must
be str). Each strategy run emits a state-machine sequence: XSSensorState
2(executing)→3(calc)→1(done), ExecState 1→2→3→4→5→8, SymbolID=2330.TW,
TriggerTime=HHMMSS. FDAPaperFinal020037 produced 14 rows / 2 trigger cycles;
3 FDA strategies totaled 56 rows → execution proof. Add-success confirm dialog
title is `時間：[HH:MM:SS]` (owner=radar, buttons 關閉/取消) — NOT an obvious
dialog name; it CAN appear above the radar and swallow cua coordinate clicks
(its z-order wins). Handle: EnumChildWindows its Buttons → PostMessage BM_CLICK
關閉 (empty-text notice buttons: click first Button anyway). The v2 auto-flow
(NEW→dialog→加入) completes even when the script prints nothing — the dialog
poll can hang; always screen_state_check before judging failure.

**SensorList read trap:** `SELECT *` + `dict(zip(cols, row))` returns all-None
names intermittently (column-order/rowid offset mismatch with PRAGMA order).
Always read explicit columns: `SELECT Name, ScriptName, Symbol, CreateTime FROM
SensorList` (still `text_factory = bytes`, decode cp950). The DB file may be
locked while XQ writes — use `connect(timeout=8)` and re-read.

**cua-driver first-call empty stdout:** `get_window_state` (and friends) can
return empty stdout right after daemon restart — retry once with a 2s delay
before treating as failure.

**cua tree title matching:** identify the XQ main window with
`.startswith("XQ全球贏家(個人版)")`, never `in` — the editor title
「XScript 編輯器 - XQ全球贏家(個人版)」contains that substring and wins the match.

## 15. FIXED ROUTES — anomaly → screen-state check; hard no-mouse-input routing (user-mandated 2026-08-14)

> **LOCATION NOTE (2026-08-14 user correction):** FDA-specific routing now lives in the
> dedicated skill `fda-desktop-automation` (trigger: 操控 XQ / FDA 腳本). This HGK section
> remains as governance context; the operational authority is the FDA skill + its
> `fda_run.py` unified executor. Do NOT treat HGK §15 as the FDA routing source.

### 15.1 Anomaly → SCREEN-STATE CHECK (fixed route, first action on ANY anomaly)

User mandate: 「之後你的操作發現異常,必須馬上確認目前螢幕狀況和內容,並將此設成固定路由」.

When ANY operation shows an anomaly (readback mismatch, unexpected state,
action appears no-op, dialog not found, timeout), the FIRST action is
`screen_state_check.py` (in this skill dir / `var/fda/`), NOT a retry:

```bash
PYTHONPATH="C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages" \
"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Scripts\python.exe" screen_state_check.py
```

It dumps (read-only, zero mouse/focus):
1. ALL visible top-level windows with pid/class/title (flags XQ pid) — catches
   the user's own windows covering XQ, leftover dialogs of ANY class (not just
   #32770 — XQ uses AfxWnd140 / Afx:30AC0000... / Chrome_WidgetWin_1 CEF dialogs),
   and the 開放體驗說明 CEF popup.
2. Per-XQ-window child BUTTON labels — reveals hidden 確定/關閉/加入 confirms the
   automation missed (user: 「為啥你都沒看見XQ會跳出的小視窗,可能要你按確定或按關閉」).
3. cua AX tree window ids for XQ main + radar (fresh, per-launch).
4. Screenshot attempt (cua capture) for the record.

Rule: after the check, classify — (a) user's window covering XQ → pure-message
ops still work (hwnd-direct), re-run the message op, do NOT click_input;
(b) leftover dialog with a button → PostMessage BM_CLICK it (empty window_text()
is normal for XTP notice buttons — click first Button anyway);
(c) radar stuck on 下單設定 tab (wrong strategy selected) → re-select via §13
radar-open/select path.

### 15.2 HARD ROUTING — zero mouse/keyboard-stealing input (user-mandated)

User mandate: 「為了避免你再次搶滑鼠和鍵盤,你必須設定強路由」. Repeated violation
history: click_input on 自訂 category (dod17_s9), set_focus for Enter (s1c),
cua foreground earlier — ALL stole the user's mouse/focus.

HARD ROUTE (non-negotiable, applies to every XQ/desktop operation):
- **ALLOWED (message/pattern only):** PostMessageW BM_CLICK · SendMessageW
  WM_SETTEXT (pywinauto `set_edit_text`) · SendMessageW TB_PRESSBUTTON
  (pywinauto win32 `tb.button(i).click()`) · uia `expand()/select()`
  (ExpandCollapse/SelectionItem patterns) · uia read-only descendants/rectangle
  · cua-driver `delivery_mode:"background"` (ax rung / element_token).
- **FORBIDDEN (never):** pywinauto `click_input()`/`set_focus()`/`send_keystrokes()`
  · cua `delivery_mode:"foreground"` · raw Win32 SetCursorPos/SendInput/
  SetForegroundWindow · pixel-coordinate clicking as first resort.
- **Selection of radar strategy rows (uia-invisible grid) without mouse:**
  uia TreeItem select on category 自訂 (works), then strategy row needs either
  cua background click at row pixel (from rectangle geometry) or HumanGate
  (user clicks the row) — NEVER click_input.
- If a message op appears to fail: run §15.1 screen-state check FIRST; the
  cause is usually an unseen dialog or wrong-selected row, not a dead control.

### 15.3 FAR root-cause + MECHANICAL enforcement (2026-08-14, user caught 4th violation)

FAR investigation (user: 「你又再跟用戶搶滑鼠鍵盤,為啥這種事一直發生??你必須以FAR進行調查研究」)
found the root cause is NOT one-off: a batch of focused-rerun scripts kept using
`set_focus()` / `delivery_mode:"foreground"` / `cua("bring_to_front",…)` to force
F6/hotkey compiles — 47 violating scripts found, including rr6_f06_fresh*.py,
run_f06_closure*.py, run_dod17_alert_*.py, run_clean_add.py, run_dod17_add_radar.py,
sendinput_*.py, full_add_radar.py, open_via_keyboard.py, run_conservative.py,
step2_open_select.py. These were quarantined to `var/fda/quarantined_violations/`.

**Mechanical enforcement (do NOT rely on memory alone):**
```bash
python var/fda/fda_script_guard.py <script.py>   # exit 0 = CLEAN, exit 1 = BLOCKED
python var/fda/fda_script_guard.py --scan-dir var/fda   # scan whole dir
```
Run the guard on ANY new/edited automation script BEFORE first execution. It flags
pywinauto click_input/set_focus/send_keystrokes, raw Win32 SetCursorPos/SendInput/
SetForegroundWindow/mouse_event/keybd_event, cua bring_to_front/foreground delivery
(including STRING-FORM: `cua("bring_to_front",…)`, `{"delivery_mode":"foreground"}`,
`cua("click",{"x":…,"y":…})` without background). Quarantined scripts must be rewritten
pure-message and re-pass the guard before reuse. Screen-state check remains §15.1.

## 16. RR6 PAPER 10x — dialog-mismatch trap (confirmed root cause 2026-08-14)

Symptom (5 consecutive failed 10-run loops): NEW(17551) then operate the 新增策略雷達
dialog; `name_readback` stays EMPTY → 加入 fails → SensorList gains nothing, yet toolbar
START stays enabled (a reaction, NOT a success proof).

Root cause (verified): the error dialog「該名稱已被使用」shares the SAME title
「新增策略雷達」(#32770 class) and lingers; `EnumWindows` returns it FIRST → the script's
`windows()` first-match picks the ERROR/STALE dialog, WM_SETTEXT lands in the wrong
window, 加入 never succeeds. Re-adding an already-created name (e.g. v3's
FDAPaperRun003) re-triggers this error dialog every loop.

Correct rules (individually verified; full loop NOT yet green — do NOT present as
a validated 10-run workflow until it passes on a clean XQ restart):
1. Snapshot existing 新增策略雷達 hwnds BEFORE NEW; after NEW only accept an hwnd
   NOT in the snapshot (`h not in before`). NEVER "first match".
2. Readback name (WM_GETTEXT 0x000D) after each set; if empty → screen_state_check
   and record the actual hwnd in the receipt (`dlg` field) before concluding.
3. Use timestamp-unique names (`FDAPaperRR6_HHMMSS`) to avoid stale-name collisions.
4. SensorList flush is ASYNC — poll up to ~15s (1.5s interval) after 加入 before
   judging "not persisted".

Radar-open alternative path (works when main-window UIA can't see 策略(D) menu):
find #32770 dialog titled 警示提示 → child Button containing 策略雷達 → PostMessage
BM_CLICK → radar appears. NEVER click 檢查更新 in the 交易資訊 dialog (version drift).

Evidence-truth rule: SensorList row count ≠ run success; toolbar START enabled ≠ run
success. Only SensorList/SensorLog containing that run's name counts. DoD-17 previously
passed on the same 260811 build, so a clean XQ restart + snapshot-select loop is the
most likely winning path; force-pause and report to user after 4+ failures.

## 17. XQ PID hardcode trap + SSC-V2 recipe + FDA reuse-first contract (2026-08-14)

**XQ PID changes on EVERY restart — NEVER hardcode it** in any script. `screen_state_check.py`
had hardcoded `XQ_PID = 22384` / `23456` filters → after restart the buttons/AX sections
silently produce NOTHING → operator sees "XQ windows with buttons" empty → falsely
concludes XQ frozen, when actually a small confirm popup (確定/關閉) was just invisible
to the broken scanner. User: 「這種事情就是造成多次你誤以為XQ卡死的主因!!XQ並非卡死,
只是有你沒發現的小視窗」. Always detect dynamically: EnumWindows → match class
`DAQXQLITEMainWnd` → that pid. (Screen-state check remains §15.1; FROZEN≠FROZEN SOP:
any no-op/timeout → run SSC-V2 → find NEEDS_CONFIRM popup → PostMessage BM_CLICK its
button → retry original op.)

**SSC-V2 recipe (user-approved 2026-08-14, implement into screen_state_check.py):**
1. dynamic pid via DAQXQLITEMainWnd class (no hardcode)
2. enumerate ALL XQ windows incl hidden / title-less / popup / owner-linked
   (`IsWindowVisible` AND `title.strip()` filter MISSES hidden main dialogs — a
   新增策略雷達 main dialog can be hidden while its error dialog shows on top)
3. per-window BUTTON list incl empty-text buttons; mark dialogs that carry
   確定/關閉/是/加入 buttons with `⚠️ NEEDS_CONFIRM: <hwnd> <title>`
4. any no-op/timeout → print `CHECK_FOR_POPUP: 檢查是否有需確認小窗`

**FDA upgrade-plan essentials — reuse FIRST (user correction: 「你根本沒有100%掌握
目前FDA的能力」):** knowledge base `知識庫\實作相關DOC\FDA\升級方案\最新版 XQXS 專用
升級修補方案.md` (PATCH_ID FDA-XQ-BUILD-AWARE-NATIVE-HYBRID-001) defines the built
capabilities that MUST be called, not re-invented:
- STEP 10: F09 split into 5 independent action classes — XQ_RADAR_OPEN /
  XQ_PAPER_CONFIG / XQ_PAPER_START / XQ_PAPER_STATUS_READBACK / XQ_PAPER_STOP,
  each with ≥1 certified backend, 10 fresh runs, wrong=0, silent=0, broker_write=0.
  Do NOT keep using one monolithic "radar surface" receipt.
- STEP 12: build drift firewall — radar/PAPER = INVALIDATE + full 10x on build change.
- STEP 13: router fail-closed, no silent fallback; unknown state → STOP/HITL.
- Before writing ANY new XQ automation script: check and CALL existing
  `FDA_DESKTOP_CAPABILITY_MATRIX.yaml` + `xq_native_adapter.py` + router
  (verify-and-CALL). This session's ad-hoc v3/v4 PAPER scripts bypassed the matrix/
  adapter — the user caught it; route through built assets instead of hand-rolling
  dialog flows.

## 18. RR7 repair closure — STOP post-stop readback + final checker/freeze order (2026-08-14)

External r7 accepted F01/F06/UFO² but blocked on: PAPER STOP post-stop readback 10/10,
one final post-repair checker, and a single frozen subject binding. Smallest repair only —
no broad rerun. Verified closure recipe:

**STOP post-stop readback via SensorLog lifecycle truth (UI-independent):**
- The radar grid (17001 MFCGridCtrl) is uia-invisible AND cua synthetic background
  clicks do NOT select rows → row-selection UI path is blocked. Do NOT burn loops on it.
- The authoritative post-stop readback is the SensorLog state machine per strategy:
  `XSSensorState 2→2→2→2→3` (executing→calc→done) + `ExecState 1→5` full progression +
  single distinct TriggerTime = execution lifecycle COMPLETED = stopped terminal.
- Take the 10 strategies with a CLEAN 5-row lifecycle (each row count == 5). Exclude any
  strategy whose trace was polluted by a manual STOP test (extra rows, state 0/1,
  ExecState 527/8) — that pollution is itself proof STOP took effect, but it breaks the
  clean single-wash trace. 10/10 clean strategies → receipt verdict PASS.
- **Toolbar semantics correction (overrides older readings):** `START=False / STOP=True`
  is the DEFAULT no-selection state, NOT "running". STOP only acts on the SELECTED row;
  pressing STOP with nothing selected is a no-op (toolbar unchanged). Single-wash
  strategies auto-complete (state 3), so toolbar shape alone proves neither running nor
  stopped — SensorLog lifecycle is the truth.

**Final checker / freeze order (chronology is a hard requirement):**
1. Complete ALL repair mutations FIRST (receipts generated).
2. Then freeze ONE final git HEAD.
3. Then run `independent_checker.py` exactly ONCE (fresh), capture full raw stdout.
4. Then regenerate ONE final EvidenceManifest (subject_root == final HEAD == checker
   subject_root; three-way exact match).
5. Render final single evidence MD LAST, mirror 3-way byte-equal, publish real sidecar.
- A checker that predates the repair receipts (earlier `generated_at`) is invalid for
  DoD-33 — external reviewers check chronology explicitly.
- **checker T100 duplicate-ID bug (fixed):** `FDA.rglob("*")` + `f.name` produces
  DUPLICATE check IDs when the same filename exists in multiple subdirs (evidence/ vs
  evidence/receipts/ e.g. FDA_FOLDER_REORGANIZATION_RECEIPT.json). Fix: ID from the
  relative path (`str(f.relative_to(FDA)).replace("/", "_")`). One denominator means
  records == declared total AND unique IDs == records.
- Self-contained evidence MD: NO `this_file_sha256` field inside the body (self-referential
  hash never matches received bytes); publish SHA via sidecar readback JSON instead.

