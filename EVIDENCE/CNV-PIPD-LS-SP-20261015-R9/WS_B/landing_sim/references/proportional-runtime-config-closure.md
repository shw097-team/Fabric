# Proportional governance closure (Hermes runtime self-config changes)

Applies when the durable mutation is a **Hermes runtime self-configuration /
routing / throttle change** — `config.yaml` fallback chain, `rate_limits` block,
an `agent/provider_rate_limiter.py`-style wiring — and it is NOT a codex-worktree
deliverable in the HGK/SQS product tree. Full six-surface fan-out
(KANBAN + SWARM + GSTACK + OPENSPEC + codex-spawn) is OVER-governance here, and
forcing a `writer=codex` spawn for a change that lives in Hermes-core is dishonest
(no codex worktree produced it).

## When to use the proportional route (instead of full fan-out)
- Change is entirely on the Hermes side (runtime config / limiter / routing), not
  product code that a codex lane would write.
- The task is a reconfiguration of an already-admitted routing scheme, not a new
  stage/blueprint.
- User explicitly directs "比例化閉環 / 非全開六面閉環" or a proportional closure.

## Proven sequence (WO-HGK-PFR-ROUTE-002, 2026-08-24)
1. **HGK admission via SharedSpine typed API** (NOT full project lifecycle):
   `register_requirement` → acquire_lease →
   `transition_requirement(..., "FROZEN", expected_version=0, idempotency_key=FRZ-<REQ>)`
   → release_lease → `create_taskspec` (state DRAFT) → `create_workorder(WO, TS, writer=codex, ...)`
   (TS → ADMITTED, WO → CREATED). Scope the REQ wording to the exact canonical
   chain + throttle so the evidence binds to it.
2. **Single evidence MD → team evidence home FIRST** (`<team>/evidence/`), never
   Fabric-root first (Step 6B primary-home gate). Fully embed raw bodies
   (readback, markers, smoke output), not pointers.
3. **byte-identical mirror to three review roots**
   (`Fabric|HGK|SQS-THC/evidence/review/`), SHA-256 equality asserted at all three
   + primary. Verify with `cmp -s` and `sha256sum`.
4. **Independent fresh-context read-only AO lane** (delegate_task).
5. **Defer WO-result recording until the AO returns:** do NOT call
   `record_workorder_result` nor fill the evidence MD's
   `ACCEPTANCE_OFFICER_VERDICT=` preemptively. Leave a forward pointer, record
   CREATED→VERIFIED only after the real AO verdict, then re-mirror + re-bind the
   spine evidence hash if the MD changed.
6. **New-session runtime readback** after config change to confirm the canonical
   route actually materializes in a fresh process (running sessions pin the old
   provider/model).

## Claim-ceiling discipline
- Claim: wiring + order + throttle enforced at the request boundary + FIRST-hop
  fallback proven in isolated smoke. Do NOT claim full natural multi-hop
  traversal when downstream providers (e.g. OpenRouter logged out, historical
  free-tier 429, `openai` provider not materialized) were not live-proven this round.

## Relation to merge plane vs governance plane
HG-KSEOS is the sole **control plane**; Hermes is the governed **runtime/orchestration
plane**. A change Hermes makes to ITS OWN runtime config is Hermes-plane work that the
HGK control plane governs (admission + evidence + AO), not codex-lane product work.
Keep that separation when scoping the WorkOrder and when deciding which execution
surfaces genuinely apply.