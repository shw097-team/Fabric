# CHECKPOINT — HG-KSEOS lane-reliability closure

Round: `LANE-RELIABILITY-CLOSURE-20261016` · Session: `20261016_104922_d455e7` · Written: 2026-10-16 (UTC+8)
Round dir: `var/LANE-RELIABILITY-CLOSURE-20261016/` · Publication: `shw097-team/Fabric`, branch
`pub/lane-reliability-closure-20261016`, packet `EVIDENCE/LANE-RELIABILITY-CLOSURE-20261016/`

## 1. What this round was asked to do

Under the current Fabric contract: HG-KSEOS is the sole control plane, canonical Hermes is its governed
Runtime/Orchestration plane, and after HGK admission the **three lanes and their model selection must be
usable and reliable**:

| lane | owner-named arm |
|---|---|
| PLAN & Orchestrator, inside Hermes | GPT-6.1-SOL-MEDIUM (OpenAI OAuth) |
| Codex bounded writer / EXECUTE, via CODEX CLI | DeepSeek V4.1 Flash (OPENCODE GO) |
| Independent Acceptance Officer / VERIFY / SECURITY, via CODEX CLI | GPT-6.1-SOL-MEDIUM (OpenAI OAuth) |

Plus: reuse the existing lanes rather than inventing them, read the previous session's repair experience,
enable KANBAN + SWARM + GSTACK + OPENSPEC, self-detect/self-repair/self-verify, then publish the
implementation and evidence to Fabric for external acceptance.

## 2. What was actually proven, and how

**PLAN plane (the owner's explicit priority).** Not read from config: a reply probe returned
`PLAN_LANE_PROBE_OK`, a tool-executing probe returned `PLAN_TOOL_PROBE_OK`, and the governed profile's own
`state.db::sessions` carries fresh rows `model=gpt-6.1-sol / billing_provider=openai-codex /
billing_base_url=https://chatgpt.com/backend-api/codex / subscription_included / oneshot`. Four separate
surfaces agree on this arm (`config/lane-route-slots.candidate.json` pool rank-1, the registry
`sod_invariants` + `SOD006-C2`, `tests/test_lane_policy.py`'s owner chain, `role_mandate.json`).

**EXECUTE lane.** `dispatch.json` for attempt `BC3`: `required_arm == served_arm ==
opencode-go/deepseek-v4.1-flash`, `usage_receipt_ok: true` (19 usage rows), `used_rank: 1`,
`nonce_present: true`, exit 0 in 74 s.

**VERIFY/SECURITY lane.** `dispatch.json` for `V1`: `required_arm == served_arm ==
openai-codex/gpt-6.1-sol`, `usage_receipt_ok: true`, `used_rank: 1`, and the guard's subject-mutation
verdict `CLEAN` (207 files and an identical digest before and after the checker ran).

## 3. What changed

- **ChangeSet B** (`scripts/runtime_role_binding_assert.py`) — the effort axis was absent
  (`grep -c effort` = 0), so a lane served at a different reasoning effort than its mandate declares was
  refused by nothing. Now gated, with exit 7 and four typed codes.
- **ChangeSet C** (`scripts/hgk-governed-runtime-controller.py`) — a blank/absent session id mapped to
  exit 3, which refused **every** mutating call for an agent with no session id. Now answered
  `{"action":"allow","reason":"no-session-id-unattributable"}`.
- **ChangeSet A** (canonical `config/…`, the only canonical mutation) — additive PLAN-plane declaration
  with this round's measured availability; registry `epoch` 19 -> 20; stale `/codex_sha256` projection
  expectation corrected; `source_of_routes` re-pinned. Canonical drift is now empty.
- B and C live in the **candidate** only. No agent promoted its own candidate.

## 4. Claim ceiling

**CANDIDATE_ONLY.** Everything was measured on this host by this session. Nothing is accepted, promoted
or merged. `hgk_canonical_acceptance: NOT_PERFORMED`. Checker verdicts are advisory.

## 5. Open residuals (do not smooth these)

1. **F1-PLAN-ROUTE-ROW-OUTLIER** — `routes[].PLAN` = `opencode-go/glm-5.3-flash` while the pool, the
   registry SoD block, the conformance test and the owner mandate all say `openai-codex/gpt-6.1-sol`.
   Recorded, NOT repaired: a rebind is outside this round's authorisation. Remediation is priced in
   `FINDINGS_F1_PLAN_ROUTE_OUTLIER.md`. Consequence:
   `tests/test_lane_policy.py::test_registry_and_projection_shape` is RED on the canonical tree.
2. **PLAN and VERIFY are the same model** (`openai-codex/gpt-6.1-sol`). Plan-vs-checker MODEL independence
   is absent; the registry carries this as `SOD006-C2` OPEN_OWNER_ORDERED. Only process/lane/evidence-path
   independence remains.
3. **EXECUTE lane-turn reliability** — attempts `BC1` and `BC2` wedged: first file written, then no
   progress, no socket, frozen CPU. `BC2` was terminated by the orchestrator on measurement, with a
   `TERMINATION.json` recording why and noting that the runner therefore never wrote its own receipt. The
   cause is turn **shaping**, not the arm — both wedged turns still show the mandated arm served. The
   remedy that worked was an **edit-only turn** (BC3, 74 s): remove test-running from the lane turn and
   keep the oracle orchestrator-side. Treat any lane turn that both edits and executes tests as a stall
   risk.
4. **The checker's V1 brief contradicted itself** (forbade all writes while requiring fixtures). The
   checker correctly returned `UNCERTAIN` rather than fabricating; the brief was repaired and `V2` re-ran.
   See `FINDINGS_CHECKER_BRIEF_V1_WRITE_CONTRADICTION.md`.
5. `E11` (five AO-guard cases) remains a named open residual from the previous round, unchanged.

## 6. Next session's first moves

1. Read the checker's `V2` verdict (`lanes/VERIFY_SECURITY/V2/CHECKER_VERDICT.json`) and confirm which
   claims are independently confirmed versus orchestration-only.
2. If the owner wants promotion: apply the candidate's two product files plus the new test module to the
   canonical tree, then re-run the named suite at the canonical root. **The promotion is the owner's
   call** — this round deliberately did not take it.
3. Price F1 for the owner; a rebind of `routes[].PLAN` is the single remaining inconsistency.
4. Reuse the edit-only turn shape for any further EXECUTE work.

## 7. Reproduction

```
R=C:/Projects/Agent_Workspace/HG-KSEOS; PY=C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe
$PY -B $R/var/LANE-RELIABILITY-CLOSURE-20261016/selfcheck.py      # full detection list
$PY -B $R/var/LANE-RELIABILITY-CLOSURE-20261016/annotate_selfcheck.py
$PY -B $R/var/LANE-RELIABILITY-CLOSURE-20261016/extract_verdicts.py
$PY -B $R/var/LANE-RELIABILITY-CLOSURE-20261016/update_d14.py
$PY -B $R/var/LANE-RELIABILITY-CLOSURE-20261016/make_closure.py
$PY -B $R/var/LANE-RELIABILITY-CLOSURE-20261016/publish_packet.py
$PY -B $R/var/LANE-RELIABILITY-CLOSURE-20261016/packet_gate.py   # must print GATE_PASS
```

Environment notes that cost time in this session: `npx` needs `shell=True` from Python; MSYS rewrites
native `//FLAG` arguments (`taskkill //PID`, `tasklist //FI` fail silently); `git -C` needs `C:/` paths,
not `/c/…`.
