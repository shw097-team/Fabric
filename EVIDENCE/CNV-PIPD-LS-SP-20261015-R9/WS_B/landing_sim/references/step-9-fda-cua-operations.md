# Step 9 — FDA desktop automation operations (Fabric profile detail)

For Fabric Shared Infrastructure Profile Team work (`fabric-desktop-automation`,
`WINDOWS_DESKTOP_AUTOMATION`, XQ/XS PAPER fixtures, cua/ufo2 provider profiles):

1. **Cua driver install (the ONLY route that works on this host):** download
   `https://raw.githubusercontent.com/trycua/cua/main/libs/cua-driver/scripts/install.ps1`
   to a local file, then `powershell -NoProfile -ExecutionPolicy Bypass -File <script> *> log`.
   All other routes fail: `hermes computer-use install` exits with "did not complete"
   (auto-installer bug), `irm ... | iex` in PS 5.1 dies with `ValidateSetFailure`,
   and `pwsh` from git-bash dies with `Permission denied` (WindowsApps alias).
   Success = cua-driver at `%LOCALAPPDATA%\Programs\Cua\cua-driver\bin\cua-driver.exe`,
   User PATH updated (current shell needs `export PATH="$LOCALAPPDATA/Programs/Cua/cua-driver/bin:$PATH"`).
2. **Cua daemon:** `hermes computer-use status` only detects the driver via PATH
   (`shutil.which`) — after install it still says "not installed" until PATH refresh.
   Start the daemon from a `.ps1` file (`$env:PATH += ...; cua-driver.exe serve`) —
   inline `powershell -Command` from git-bash eats `$env:` and backslashes in
   `\\.\pipe\cua-driver`. `cua-driver doctor` / `hermes computer-use doctor` verify
   UIA + D3D11 capture reachability.
3. **CLI call surface:** `cua-driver describe <tool>` prints the input schema;
   `cua-driver call <tool> '<json-args>'` executes. `get_window_state` REQUIRES both
   `pid` AND `window_id` (window_id changes per launch — re-fetch from
   `get_accessibility_tree`); `debug_window_info` takes `{"pid": N}`. Element-indexed
   actions need a fresh `get_window_state` per (pid, window_id).
4. **Live fixture qualification (blueprint FDA-C4):** run 10 FRESH read-only UIA calls
   against the live target; class is team-certified only at 10/10 with zero wrong /
   zero silent-wrong action. Then promote the canonical
   `FDA_DESKTOP_CAPABILITY_MATRIX.yaml` row DEFERRED→QUALIFIED with reason code +
   evidence_refs (matrix is the ONLY routing truth; never ephemeral dicts).
5. **XQ version truth:** exe file version (1.10.0.0) ≠ live product version
   (live readback: 3.18.02 260102 at first probe, **3.20.02 260811 after an XQ
   auto-update the same day**). Always read product version from the live UIA
   surface (window title / `debug_window_info`); version drift →
   `REQUALIFY_REQUIRED` for selector-bound action classes only. Record BOTH
   versions in receipts (exe file version + product version).
6. **HumanGate boundary:** XS editor/PAPER/radar require XQ LOGIN — never automate
   login (blueprint 5.18A: normal human action, not BreakGlass). If the user
   enables XQ auto-login, the logged-in session (title `[SHW097:已登入]`)
   UNBLOCKS the XS editor/PAPER/radar fixtures — proceed with live qualification
   on the logged-in subject. Harmless-app probes (Notepad) prove bounded
   desktop write+readback: Popen (GUI apps hang subprocess.run), bytes-decode with
   `errors="replace"` (text-mode subprocess stderr throws UnicodeDecodeError),
   type_text then fresh get_window_state readback.
7. **XQ XS editor is an Afx/MFC app with a UIA Invoke deadlock (R-FDA-011 class,
   upstream cua-driver 0.19.3 edge):** clicking the 新增 (New) button via UIA
   element_token hangs the driver (`TimeoutExpired`, then `UIA provider
   unresponsive` until daemon restart). Workarounds that worked: (a) pixel-click
   via `{"x": frame.x + w/2, "y": frame.y + h/2}` (frame from get_window_state),
   (b) clipboard ctrl+v paste instead of type_text for syntax editors,
   (c) Ctrl+Tab to switch editor tabs, (d) kill+restart the daemon to clear a
   stuck UIA provider. XQ Win32 menu popups (策略(D)) are INVISIBLE to the UIA
   tree when opened foreground — use background click on the MenuItem and the
   items appear in the same window's tree; double-click (`"count": 2`) on
   TreeItem EXPANDS the tree (single click does not).
8. **XScript compile fixtures: verify against the REAL compiler, not the doc.**
   DOC-03's infix `if Close CrossOver ma then Plot1(ma);` is marked
   `NOT_RUNTIME_VERIFIED` and the XQLite 3.20.02 compiler REJECTS it
   (`無法辨認的字 "if Close CrossOver"`). DOC-04 SF-0137 lists `CrossOver` as a
   function_bool — the function-call form `CrossOver(Close, ma)` COMPILES
   (CompileStatus=1, empty error). Always fresh-read the authoritative doc for
   signatures, but treat the compiler's file-readback verdict as truth.
9. **XQ compile file-readback (readback hierarchy #1):**
   `C:\SysJust\XQLite\XS\Data\DAQXQLITE\<ACCOUNT>\DAQXQLITE_SHW097_Script.sqlite`
   (user scripts) and `System\XSSystem\Bin\System\System_Script.sqlite` (397
   system indicators, authority corpus) — columns `CompileStatus` (1=success,
   2=error), `CompileMsg` (exact compiler error text), `LastCompileTime`.
   Trigger compile via F6 (`press_key {"key": "f6"}`), then read the DB row —
   that is the fixture PASS/FAIL proof. F6 on an unchanged script leaves
   LastCompileTime static (still PASS — read CompileStatus, not the timestamp).
   Log/export readback: `C:\SysJust\XQLite\Log\CEF*.log` (plaintext) +
   `PrintSvc LogContent` table (LogIndex/InstanceID/LogTime/Symbol/ScriptName/
   ScriptLineNumber/LogMessage).
10. **Evidence MD self-reference trap (freeze-order extension):** when re-generating
   an evidence MD that lives INSIDE the directory it scans, the MD embeds its own
   hash → self-referential loop, every regeneration drifts. Generator MUST exclude
   the MD filename from the artifact scan. Regenerate MD LAST → mirror → hash.
11. **UFO² effective-load is KEYLESS (corrects earlier BLOCKED_HITL):** UFO² v3.0.8
   runs with Ollama local (`API_KEY: "ollama"` placeholder), a custom `BaseService`,
   or `PlaceHolderService` — no external API key, no HumanGate. Verified 7/7
   (package/llm/uia_backend/config/agents import + LLM canary) with the Hermes
   opencode-go backend: `get_env_value_prefer_dotenv("OPENCODE_GO_API_KEY")`
   (memory-only), OpenAI SDK `base_url=https://opencode.ai/zen/go/v1`,
   model `deepseek-v4-flash`, `max_tokens>=256` (smaller → finish=length, empty).
   **urllib to opencode.ai is blocked (HTTP 403 code 1010, Cloudflare)** — always use
   the OpenAI SDK. deps: `env -u PYTHONPATH` + `pip install --target
   .venv\Lib\site-packages`; pywinauto needs pywin32 postinstall + DLL copy; UFO²
   needs `langchain==0.2.17` (`langchain.docstore` removed in ≥0.3).
12. **Strategy radar trial (XQ):** 策略(D)→策略雷達(開放體驗)(L); the 試用說明 dialog is
   Win32 (UIA-invisible) — dismiss with `press_key return` ("我知道了"). Trial radar
   library is EMPTY (no strategy leaf nodes; system strategies read-only) → PAPER
   start/stop cannot run on the trial subject; record
   `QUALIFIED_SURFACE / RUNTIME_START_STOP_BLOCKED_TRIAL_LIBRARY_EMPTY` and name the
   unblock owner (SQS/XQ PAPER fixture authority). Never fake a run.
13. **delivery_mode: background ONLY (HARD — verified 2026-08-13 FAR self-research).**
   foreground + raw Win32 SetCursorPos/SendInput steals the user's real cursor and
   crashed XQ 3×. Default background; element_index ax rung preferred; Win32 =
   read-only observation + PostMessage BM_CLICK on UIA-invisible dialog buttons;
   never SendInput Enter on dialogs; user can keep using their mouse with zero
   interference. Full rules + XQ radar correct flow (警示腳本 → 加入策略雷達 →
   自動執行) in `references/fda-desktop-automation-cua.md` §11. For radar
   start/stop/verify automation, the community repo would2000/XQ-Auto-Writer-Skill
   provides live-verified toolbar command IDs + pywinauto recipe — see
   `references/xq-community-automation-solution.md`.
14. **Mouse-free desktop automation = messages + patterns only (HARD — user
   corrected TWICE 2026-08-13, "你又在跟我搶滑鼠控制權了").** pywinauto
   `click_input()`/`set_focus()`/`send_keystrokes()` move the user's REAL cursor —
   NEVER use them while the user is at the machine. Safe forms (all verified):
   `btn.click()` win32 = BM_CLICK message; `edit.set_edit_text(v)` = SendMessage
   WM_SETTEXT (works cross-process — see 14b correction); uia
   `expand()/select()` = TVM/selection patterns; uia `button.click()` = Invoke
   (but Afx-deadlocks on XQ toolbars). XQ radar control-ID tables
   (NEW=17551/START=17554/STOP=17555, 新增策略雷達 dialog ids, big5-encoded
   SensorList.sqlite location + wrong-DB trap, 選擇使用腳本 expand-quirk) in
   `references/fda-desktop-automation-cua.md` §13.
15. **Afx Win32-dialog interaction matrix (verified 2026-08-13 DoD-17 stall):**
   (a) `PostMessageW(BTN, BM_CLICK)` on dialog Buttons WORKS cross-process without
   stealing focus (validated: created a 警示腳本 by clicking 警示/確認 buttons);
   (b) **WM_SETTEXT is NOT UIPI-blocked — CORRECTED (see §13 reference):**
   `SendMessageW WM_SETTEXT` / pywinauto `set_edit_text()` WORK; the earlier
   failure was `PostMessageW` + a ctypes buffer freed by Python before the async
   post landed (returns 0, readback empty). Use SendMessage/set_edit_text, never
   PostMessage with a temp buffer;
   (c) cua-driver `type_text` background px does NOT land in Win32 dialog Edits
   (readback stays empty) — use SendMessage WM_SETTEXT / set_edit_text instead;
   (d) **SendInput Enter on a dialog CRASHES XQ** (dumps
   `C:\SysJust\XQLite\Log\daqxqlite.exe*.dmp`) — never use SendInput/SetCursorPos/
   SetForegroundWindow on dialogs;
   (e) **Dialog disambiguation:** the real 新增腳本 main dialog exposes children
   labelled 腳本類型/指標/選股/警示/交易/函數/名稱：; a validation-error dialog
   shares the SAME title (新增腳本) with children 確定/輸入名稱有誤 — scan children
   labels before acting, never assume the first hwnd with the title is the main one;
   (f) XQ crash signature: daqxqlite.exe process gone while DAQXQLITEEngine.exe
   remains — restart both, then re-verify login title `[SHW097:已登入]`;
   (g) **version downgrade 3.20.02 → 3.19.03 is INFEASTBLE** (verified
   2026-08-13): no installer obtainable (GitHub/官方下載/更新伺服器 0 hits; local
   Backup dir is user-data only, not binaries) — work around the UIA deadlock
   instead (cua background click to open radar → win32 backend inside).
16. **Failure-point pause + user discussion (user directive 2026-08-13):** when a
   failure pattern is clear (same op timing out repeatedly, all input channels
   exhausted) — pause at the NEXT failure point and present the user: closed
   wins + failure matrix + 2-4 options (incl. HumanGate manual assist) — let the
   user choose the direction; do not self-loop. Companion skill:
   `force-pause-after-4-failures` (user-owned; `hermes curator adopt` before editing).
17. **Prose rules fail at execution — pair them with mechanical gates (user
   complaint 2026-08-14: "為啥你還要自己亂嘗試和裝工具?" / "FDA 執行又再搶滑鼠").**
   The direct-call and no-mouse rules were 99% prose in SKILL.md; execution
   depended on the model voluntarily loading the skill, so it silently degraded
   to re-install attempts and foreground input. Lesson: a user-mandated HARD ROUTE
   needs an executable gate (preflight checker with exit codes, hook/approval
   blocklist), not just a checklist paragraph. FDA known gaps + upgrade plan v1
   (router-not-wired-to-matrix, UFO2 over-claim, T170 narrow coverage, 64/64
   unreproducible, stale CLOSURE_V8 ref, version drift; U1 fda_preflight.py /
   U2 Step 9-0 / U3 screen_state_check-as-only-entry / U4 prose fix / U5 record):
   `references/fda-upgrade-research-2026-08-14.md`.

Full recipes: `references/fda-desktop-automation-cua.md`.
