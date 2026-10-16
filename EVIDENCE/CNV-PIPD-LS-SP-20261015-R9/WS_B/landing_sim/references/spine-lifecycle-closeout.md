# Closing an HG-KSEOS lifecycle round without fabricating a verdict

Use when a governed lifecycle project has real, independently checked work but the plan-derived
workorders do not all map to work that was actually performed — i.e. when someone asks you to
"write the spine result" or "advance it to DELIVERED".

## Read the control plane before writing anything

- Verdict vocabulary is binary: `record_workorder_result(..., verdict)` accepts only `PASS` -> `VERIFIED`
or `FAIL` -> `FAILED`. There is no `PARTIAL`, `WITHDRAWN` or `DE_SCOPED`.
- `writer == checker` is refused (`ERR_WORKORDER_SELF_REVIEW`) — always pass a genuinely different lane.
- A workorder only leaves `CREATED` via `PASS`/`FAIL`. `rollback_workorder` is reachable **only from
`VERIFIED`**, so it is not an escape hatch from `CREATED`: it needs a `PASS` first.
- No API sets `CANCELLED` on a workorder. The delivery guard accepts `{VERIFIED, ROLLED_BACK, CANCELLED}`
but only `VERIFIED` is reachable in practice.
- Plan stages are **keyword-derived** (`_derive_tasks`), not a fixed template: a goal phrased as
research silently injects a "Knowledge pipeline / build RAG-KG ingestion" stage that a defect-repair
round will never perform. Check the derived task titles against what was actually done.

## The rule that matters

Never write a `PASS` for a stage that was not performed just to unlock `DELIVERED`. Disclosure in an
evidence file cannot cure a false row in the canonical store, and `DELIVERED` is not worth a lie. When
a false verdict is the only route, the correct outcome is that the project does **not** reach
`DELIVERED` — say so plainly instead.

## The honest, low-resistance close-out

1. `register_evidence` for every artifact the close-out will cite (id, kind, locator, sha256, producer,
   checker). Do this before referencing them.
2. `record_workorder_result(PASS)` **only** for stages with work that was actually done and checked.
   Leave unperformed stages `CREATED` and name them.
3. Resolve the acceptance honestly. Its oracle is often a plan-stage fact ("plan taskspecs admitted +
   workorders created") that is provably satisfied by the spine's own rows — that is a real `PASS`.
   A lease is required: `acquire_lease(acc, actor, token, ttl)`, then `resolve_acceptance(acc,
   verdict=..., evidence_ref=..., actor=..., token=..., expected_version=0, idempotency_key=...,
   requirement_id=...)`.
4. Record the delivered subset with the control plane's own mechanism: `checkpoint(project_id,
   evidence_refs=[...])`. The lifecycle docstring is explicit — *wave/subset closure is recorded via
   checkpoints, not by claiming project delivery*.
5. Terminate in the truthful side state: `transition(project_id, "BLOCKED_HITL", trigger=...,
   workorder_refs=[<the unperformed stage>], evidence_refs=[...])`. `BLOCKED_HITL` is correct when one
   human scope decision is genuinely outstanding.
6. Read it all back and put the readback (denominator before/after, states, acceptance verdict) in the
   closure receipt. `required_local_scope_open` = open workorders + open acceptances.

## Pitfalls

- **Dual state, not a contradiction.** `projects.state` is the registry layer (`ACTIVE` at creation,
  never updated by the lifecycle controller); delivery truth lives only in `project_lifecycles.state`.
  `ACTIVE` + `BLOCKED_HITL` is normal — state it so nobody reads it as "project missing".
- **Registering evidence before amending the file staleness.** If a registered artifact is edited
  afterwards, its registered digest is a pre-change snapshot. Register a `-02` evidence id bound to the
  post-change bytes and list both digests; never silently overwrite.
- **Column names differ from the state names**: the acceptances table column is `verdict`, not `state`.
- **`SharedSpine.connect()` is a context manager** — use `with spine.connect() as conn:`, not
  `spine.connect().execute(...)`.
- **Kanban `complete` needs evidence**: it refuses an empty completion
  (`completion_blocked_empty_result`) — pass `--result`/`--summary`. There is no `--json` flag on it.
- Keep the payload free of the strings the fail-closed review gate guards, and design the close-out so
  it needs no gate token at all.
