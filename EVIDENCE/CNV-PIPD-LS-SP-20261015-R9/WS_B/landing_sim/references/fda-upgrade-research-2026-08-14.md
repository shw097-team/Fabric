# FDA upgrade research (FAR-gate route, 2026-08-14) — known gaps + upgrade plan v1

WO: WO-HGK-FDA-UPGRADE-RESEARCH-001 · Route: UD-FAR-RESEARCH-GATE-2026-08-14-001
(any upgrade/self-evolution proposal → FAR research Gate 1 → user HITL Gate 2 → build).
Research lanes deleg_af93d60e (folder audit / skill inventory / feasibility) +
challenge deleg_d1001be6. Integrated plan: `var/a2/FDA_UPGRADE_RESEARCH_INTEGRATED_v1.md`.

## Root cause of the user complaint (2026-08-14)

User: "為啥你還要自己亂嘗試和裝工具?" + "FDA 執行又再跟用戶搶滑鼠鍵盤".
**Root cause: the "directly call qualified assets" and "no mouse stealing" rules were
99% prose in SKILL.md/references — execution relied on the model voluntarily loading
the skill. No mechanical gate existed.** The assets themselves were ALL present and
QUALIFIED (cua-driver.exe, pywinauto in HG-KSEOS venv, xq_native_adapter.py, matrix,
screen_state_check.py). Rules present ≠ rules enforced.

## Verified FDA asset state (Lane A, all on-disk)

- 5 action_classes in FDA_DESKTOP_CAPABILITY_MATRIX.yaml; 4 CUA QUALIFIED 10/10
  (XQ_LAUNCH_LOCATE / XS_COMPILE_PASS / XS_COMPILE_FAIL_READBACK /
  XQ_LOG_EXPORT_READBACK), XQ_PAPER_CONFIG = QUALIFIED_SURFACE (open+readback only).
  routing: preferred=CUA, alternate=UFO2, hot_swap_allowed=true.
- No-mouse guarantee is CODE-LOCKED: xq_native_adapter.py is pure Win32 messages
  (BM_CLICK/WM_SETTEXT/WM_GETTEXT/TB_PRESSBUTTON/WM_CLOSE; zero
  SetCursorPos/SendInput/click_input/mouse_event/SetForegroundWindow/pyautogui),
  checker T170_NATIVE_NO_MOUSE_INPUT + T171 assert it, test_xq_native_adapter.py +
  test_xq_build_drift.py double-lock it.
- FDA_PROFILE_TEAM_ACTIVE = FAIL_CLOSED (matrix promoted_at: null); live trading
  NOT_AUTHORIZED; PAPER start/stop BLOCKED_HITL (trial radar library empty).

## FDA known gaps (recorded, NOT fixed this round — candidate future WOs)

1. **Router not wired to matrix schema**: fda_router.py route() takes a FLAT dict
   (key=(app,app_version,action_class), value has cua/ufo2 'PASS' strings) but the
   matrix is NESTED (action_classes→providers→state). No build_fingerprint check,
   no build_firewall execution in router — "build-aware" holds only at test level.
   Direct-call proposals need a conversion layer before trusting route().
2. **Stale evidence ref in matrix**: XS_COMPILE_PASS cites
   FDA_F06_CLOSURE_V8_RECEIPT.json whose verdict=PARTIAL (3 steps false); the real
   10/10 credential is FDA_F06_TEN_RUN_RECEIPT.json.
3. **Version drift not closed**: F01 (XQ_LAUNCH_LOCATE 10/10) was qualified on
   XQLite 3.18.02 (260102); matrix subject is now 3.20.02-260811. Fingerprint
   receipt says exact_public_match=false, LOCAL_BUILD_QUALIFICATION_REQUIRED — no
   receipt proves 10/10 re-run on 3.20.02 for locate.
4. **UFO2 over-claim**: all 5 action_classes mark UFO2 QUALIFIED, but the only
   credential is effective-load 7/7 (not per-class 10/10 desktop fixture). Using it
   as certified alternate for failover overstates.
5. **Matrix-external capabilities**: F03 XS_EDITOR_OPEN (PASS) / F04
   XS_EDITOR_SCRIPT_LOCATE (PARTIAL) have no matrix action_class rows — no routing
   contract for them.
6. **64/64 test claim unreproducible**: tests/ has 38 def test_ + 45 check() calls;
   64 does not recompute. checker 179/179 (T001..T177) is the only current denominator.
7. **T170 coverage narrow**: only asserts no click_input(/SetCursorPos(/SendInput(;
   does NOT check SetForegroundWindow/pyautogui/mouse_event (test_xq_build_drift.py
   does add SetForegroundWindow). A future patch could slip pyautogui past T170.
8. Sema-auto ceiling: FDA_DEFERRED_SEMIAUTO_CONTRACT forbids live write / entry
   arm without separate SQS ChangeSet + authority; hot patch after arm = FORBIDDEN.

## Upgrade plan v1 (Gate 2 = user HITL pending)

| Item | What | Why |
|---|---|---|
| U1 | `fda_preflight.py` in skill references (NOT FDA tracked tree) | mechanical gate: verify 5 assets on-disk + yaml.safe_load matrix + import fda_router.route(); output JSON ROUTE + ALLOWED_INPUT_CHANNELS (CUA=background ONLY + win32 messages ONLY); exit 0=PASS / 2=BLOCKED; ZERO install/download capability |
| U2 | SKILL.md Step 9-0 "FDA 執行前強制序列" | trigger: step 0 = run preflight, no FDA op before; BLOCKED → stop+report+defect, no install attempts |
| U3 | screen_state_check.py as the ONLY anomaly entry | any failure → run it → pause + present user 2-4 options (incl HITL); no direct retry |
| U4 | prose contradiction fix | fda-desktop-automation-cua.md §11 stale "WM_SETTEXT unreliable" → SUPERSEDED (done 2026-08-14; CORRECTED = SendMessage WM_SETTEXT works) |
| U5 | record known gaps (list above), no build this round | honest claim ceiling |

## Do-NOT list (frozen asset protection)

Never modify: FDA_IMPLEMENTATION_EVIDENCE.md / FDA_EVIDENCE_MANIFEST.json /
TEAM.md / FDA_DESKTOP_CAPABILITY_MATRIX.yaml QUALIFIED states (preflight only reads
matrix) / independent_checker.py (adding T178 changes denominator 179→180 and the
whole manifest/hash chain — first version ships preflight as a standalone tool).
Do NOT put preflight inside the FDA tracked dir (pollutes evidence manifest scope).
Do NOT rewrite fda_router.py logic (preflight imports it). Do NOT give preflight any
install/download branch. Do NOT skip Gate 1/2 to build directly.

## Verification (after user approval)

1. independent_checker.py re-run stays 179/179 (denominator unchanged).
2. preflight 3-state test: normal→PASS+CUA; simulated missing asset→exit 2+BLOCKED;
   route matches test_xq_action_router.py expectations.
3. Fresh-context cold-start canary: delegate a leaf with only SKILL.md → first FDA
   action must be running preflight (proves the trigger is effective).
4. Read-only proof: hash FDA dir + references dir before/after preflight run, no new
   files, hashes equal.
