# FDA auto-invoke guardrail — FAR research state + verified facts (2026-08-15)

WO-HGK-FDA-GUARD-RESEARCH-001 · Gate 2 (user HITL) PENDING at session end.
This file is the RESUME CHECKPOINT for the post-approval execution round (G5/G6);
it also carries the session-verified `HERMES_DELEGATED_CHILD_CONTEXT` refinement
(SKILL.md is at the 100KB limit — this delta lives here; see note at bottom).

## User requirement (frozen REQ-HGK-FDA-GUARD-001, FROZEN v1 EVT-95f66f4e75861ed7)

Hermes MUST NOT auto-invoke FDA unless one of:
1. user explicitly mentions FDA in the instruction;
2. executing an EXISTING REGISTERED GOVERNED ROUTE that uses FDA
   (e.g. SQS operating XQ 全球贏家 via FDA);
3. the task REQUIRES FDA → pause the task, actively ask the user, obtain
   explicit user authorization.
Route: FAR research (Gate 1) → proposal → USER CONFIRMATION (Gate 2, COV-11-06,
no self-approval) → HGK executes. Precedent: UD-FDA-UPGRADE-HITL-2026-08-14-001.

## Admission / tracking IDs (resume tokens)

- REQ-HGK-FDA-GUARD-001 FROZEN v1 (EVT-95f66f4e75861ed7); TS-HGK-FDA-GUARD-001 ADMITTED
- WO-HGK-FDA-GUARD-RESEARCH-001 CREATED, writer=codex, base_head=22e21f03,
  rollback_pointer RB-WO-HGK-FDA-GUARD-RESEARCH-001
- Admission script: HG-KSEOS/var/a2/admit_fda_guard_wo.py (typed SharedSpine, idempotent)
- Kanban board `fda-guardrail-research` DAG:
  G0 t_2da94091 done / G1 t_229e1cda running (research lanes) / G2 t_ef4252ab (challenge
  lane) / G3 t_7b288b24 (integrated plan MD) / G4 t_344406e2 (USER HITL GATE 2) /
  G5 t_1ed2a502 (HGK execution post-approval) / G6 t_18573f98 (acceptance + evidence MD)
- Route check: `hg_kseos.named_methods.route('fda-guardrail-research')` → NATIVE
  (ACTIVE_SELECTED = openspec + gstack.cso/office-hours/plan-eng-review/qa/retro/review/ship)
- Baseline: HGK doctor PASS; HGK HEAD 22e21f03 (branch codex/hgk-final-closure-002,
  porcelain 69); Fabric 243bf8fa main (porcelain 4); SQS 9a70501a main (porcelain 93);
  bootstrap acceptance MD e867010e… internal claim PASS

## Verified facts (orchestrator-side, 2026-08-15)

- **fda_preflight.py (references/) has NO authorization check** — it verifies asset
  presence + matrix route only, exit 0=PASS / 2=BLOCKED. It is the natural INNER gate to
  extend for the guardrail (auth-source must be passed and validated).
- **Hermes approvals surface (v0.20.0) is shell-command level only**:
  `approvals.mode: smart`, `deny: []` (pattern list exists, but NO conditional-allow),
  `cron_mode: deny`, `timeout: 300`. **NO prompt-content approval hook exists** —
  "user explicitly mentioned FDA" cannot be mechanically detected at the tool layer;
  design must carry it as an explicit auth-source flag supplied by the orchestrator
  (citing the user instruction) or via HITL receipts. Re-verify at execution time.
- FDA_EXECUTION_BINDING.json BIND-FDA-001: delegation DEL-FDA-001 issuer=fda-orchestrator
  assignee=fabric-desktop-cua, expires 2026-08-15T23:59:59+08:00, denied_scope incl.
  live broker write / credential access; matrix action_classes: 5 QUALIFIED + 4
  REQUALIFY_PENDING (XQ_RADAR_OPEN / XQ_PAPER_START / XQ_PAPER_STATUS_READBACK /
  XQ_PAPER_STOP — "upgrade STEP 10 split").
- Quick grep of SQS-THC for FDA/XQ tokens: only `evidence/review/` mirrors +
  SQS-THC_KNOWLEDGE_PRELOAD.json — **no formally registered SQS→FDA operational route
  found in the quick scan**. The user's "SQS 用 FDA 操作 XQ 全球贏家" example may be a
  TARGET CLASS for the allowlist (condition 2) rather than an existing route — Lane B
  (full invoke-path inventory) was in flight at session end; verify before Gate 2.
- Research lanes dispatched: deleg_ef8d8fc1 (Lane A enforcement inventory / Lane B
  invoke-path + registered-route inventory / Lane C guardrail design options A-D).

## Session-verified pitfall refinement: HERMES_DELEGATED_CHILD_CONTEXT re-injection

SKILL.md pitfall says: unset after EACH delegate_task batch. VERIFIED 2026-08-15:
while a delegation is active the var is RE-INJECTED into the terminal env on EVERY
command — a separate `unset` command does NOT persist to the next call (next command
shows VAR=[1] again), and even `hermes kanban list` fails with "could not initialize
database: delegate_task child contexts cannot mutate Kanban tasks or boards"
(`boards list` still works — read-only path). Pattern: inline the unset in the SAME
command as the kanban mutation: `unset HERMES_DELEGATED_CHILD_CONTEXT; hermes kanban …`.

## Guardrail design constraints (for the G5 execution round)

- New gate must itself be read-only, zero-install, zero-mouse (same as fda_preflight).
- Do NOT modify frozen FDA assets (FDA_IMPLEMENTATION_EVIDENCE.md,
  FDA_EVIDENCE_MANIFEST.json, matrix QUALIFIED states) without a separate ChangeSet.
- Condition-2 allowlist needs a maintained FDA_ROUTE_REGISTRY (route_id → scope →
  bound WO); owner + maintenance + verification must be defined.
- Condition-3 flow: BLOCK + pause + ask (clarify/HITL) → user authorization receipt
  becomes the auth token for the run.
