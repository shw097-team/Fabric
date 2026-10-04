# Fabric Desktop Automation TEAM — Shared Infrastructure Profile Team

schema: FDA-TEAM/1
team_id: fabric-desktop-automation
team_class: SHARED_INFRASTRUCTURE_PROFILE_TEAM
heavy_stack: false
project_id: HGK-REFERENCE-PROJECT-002
blueprint_artifact: fabric-desktop-automation_藍圖_v2026.08.13-r2 (PASS)
capability_id: WINDOWS_DESKTOP_AUTOMATION
runtime_engine: HERMES
coordination: PROJECT_SCOPED_KANBAN (board: fda-implementation)
task_truth: HGK WORKORDER (WO-FDA-001 lineage)
normative_control_plane: HG-KSEOS
independent_checker: ACCEPTANCE_OFFICER (VERIFY_ONLY)
external_acceptance: GRANTED (FDA_FINAL_EXTERNAL_ACCEPTANCE_REPORT_2026-08-14_R11_ALL_PASS)
profile_team_active: PASS (r11 external acceptance 2026-08-14)
accepted_scope: LOCAL / PAPER / NO-LIVE-WRITE (Fabric-governed bounded Windows desktop automation)
candidate_root: be576bebe7672093039bfe7dbc265f25aa0a1164
evaluator_sha256: 9009713fd70392d64b84dcf0c1319adb5cfef51d260cd196c831c960f1bbe22e
canonical_manifest_sha256: a349633610e7414024c23f590829433cdcabe68e5ebd9e4aa641a528dc93c0d4

## Profile refs
- fabric-desktop-cua   → provider CUA_DRIVER          (initial_mode: PRIMARY_FAST_PATH)
- fabric-desktop-ufo2  → provider MICROSOFT_UFO2       (initial_mode: SPECIALIST_STANDBY)

## Machine artifact refs
- capability_matrix_ref: FDA_DESKTOP_CAPABILITY_MATRIX (Fabric/fabric-desktop-automation/FDA_DESKTOP_CAPABILITY_MATRIX.yaml)
- allowed_assignee_profiles: [fabric-desktop-cua, fabric-desktop-ufo2]
- router_owner: HGK_CURRENT_ROUTER (deterministic action-class route; canonical input = FDA_DESKTOP_CAPABILITY_MATRIX)
- coordination_owner: HERMES_PROJECT_SCOPED_KANBAN
- execution_binding_ref: CURRENT_RP002_EXECUTION_BINDING (parent RP002-EXECUTION-BINDING/2, no child fork; desktop overlay only)
- writer_policy_ref: FDA_ONE_ACTIVE_DESKTOP_WRITER (one active desktop writer per session; second writer DENY)
- knowledge_policy_ref: CURRENT_FABRIC_KNOWLEDGE_POLICY (KG1 namespace model; fabric.* namespace; candidate-only write)
- interop_refs:
  - OASF: oasf-record/1 (current route active — extend same-subject lineage)
  - CONTEXTFORGE: current CF1 route (registration when gateway route selected; not in per-click data path)
  - MCP: stdio/in-process local only; no network enablement without separate change
  - A2A: REQUIRED_WHEN_ROUTED; same-host default = Kanban/local
  - OPENTELEMETRY: INHERIT_CURRENT_PARENT_CONDITIONAL_EMBEDDED (no standalone FDA collector)
- acceptance_ref: CURRENT_FABRIC_ACCEPTANCE_PACK (independent Acceptance Officer, fresh context)
- breakglass_policy_ref: CURRENT_RP002_BREAK_GLASS (Fabric/control/BREAK_GLASS_POLICY.yaml, RP002-BREAK-GLASS/1)

## Hard invariants (fail-closed)
- HEAVY_STACK_COUNT remains 2 (HGK_ENGINEERING + SQS_FINANCIAL); FDA_IS_HEAVY_STACK = false
- WORKORDER_IS_TASK_TRUTH = true; KANBAN_IS_COORDINATION_ONLY = true
- ROLE != PROFILE != WORKER; CAPABILITY != PROVIDER
- ONE_ACTIVE_DESKTOP_WRITER_PER_SESSION = true; SECOND_CONCURRENT_WRITER = DENY
- PROVIDER_SWITCH_REQUIRES: READBACK + CHECKPOINT + KNOWN_DESKTOP_STATE + LEASE_TRANSFER
- FDA desktop profiles MAY NOT: CREATE_WORKORDER / CHANGE_FINANCIAL_TRUTH / CHANGE_RISK_AUTHORITY /
  SELF_ACCEPT / SELF_PROMOTE / CREATE_SECOND_KNOWLEDGE_PLATFORM
- SQS_LIVE_TRADING = NOT_AUTHORIZED; FDA v1 = LOCAL / PAPER / SHADOW / NO-LIVE-WRITE
- credential/MFA entry = HUMAN ONLY; unknown desktop state = BLOCKED_HITL (never auto-failover)
- parent tool matrix rows preserved additively; missing parent row = FAIL_CLOSED

## Operating routing (operational authority = fda-desktop-automation skill + AGENTS.md)
- **異常 → 查螢幕實況（第一動作，禁止直接判卡死）**: 任何操作異常/readback 不符/timeout →
  先跑 `var/fda/screen_state_check.py`（SSC-V2：動態 pid、含 hidden 視窗、NEEDS_CONFIRM 標記）。
  **XQ 很少真的卡死——通常是有沒看見的小視窗（新增成功通知/停止確認/警示提示）需處理**；
  XTP 自繪按鈕 BM_CLICK 無效 → PostMessageW(dlg, WM_CLOSE)。確認螢幕實況後才處置。
- **不和用戶搶鍵盤滑鼠（零滑鼠/零焦點硬路由）**: 禁 click_input/set_focus/send_keystrokes/
  SetCursorPos/SendInput/SetForegroundWindow/cua foreground/bring_to_front；只准
  PostMessage/SendMessage/pywinauto tb.button(i).click()/uia pattern/cua background/screen_state_check。
- **成功流程整合**: 完整 XQ 操作流程（開雷達→建 PAPER→engine-truth 驗證）見
  fda-desktop-automation skill §0 QUICKSTART + docs/FDA_USER_GUIDE.md §5/§6（verified control IDs、
  SensorLog LIKE 陷阱、SensorList flush 延遲、REUSE-FIRST asset registry）。新 session 操作 FDA
  前必讀 AGENTS.md + 載入 fda-desktop-automation skill。

## SoD / authority ceiling
- HGK decides whether a task exists, its owner, write boundary, acceptance, promotion.
- Hermes claims, dispatches, heartbeats, checkpoints, hands off providers.
- Cua/UFO2 execute bounded desktop action/workflow only — never project/domain authority.
- Acceptance Officer verifies in fresh read-only context; maker never self-accepts.

## Consumer binding
- HGK_ENGINEERING: IDE / installer / GUI-only local engineering tool capability binding.
- SQS_FINANCIAL: XQ_DESKTOP_CONTROL (PAPER/no-live-write; XQ read-watch adapter semantics preserved;
  UI screenshots are consistency evidence, never Financial Truth).

## Notes
- This TEAM artifact is NOT an Authority Matrix, WorkOrder truth, scheduler, task DB, or tool registry.
- Schema resolution: current RP002-PROFILE-TEAM-MANIFEST/1 extended additively (new instance rows +
  team_artifacts entry); no schema fork, no second manifest authority, old HGK/SQS/ASSURANCE rows preserved.
- Materialized 2026-08-13 as part of FDA ChangeSet (WO-FDA-001).
