# WS4_GSTACK_RECEIPT — GSTACK named-method route-check readback (R7, 2026-10-15)

## What this round ran

- Probe (unmodified, evidence-only): `probe_gstack_rolemap.py positive` → exit 0, `GSTACK_ROLEMAP_POSITIVE_OK`
  (19 roles, 4 hard-deny surfaces, missing_disposition_count 0); `probe_gstack_rolemap.py negative` → exit 0,
  `GSTACK_ROLEMAP_NEGATIVE_OK` (0 breaches — no role host maps onto a hard-denied surface).
- Repo's own gates, live: `loader()` / `load_registry()` (epoch 19, status CANDIDATE),
  `route_for_lane` for PLAN / EXECUTE / VERIFY_SECURITY, `check_sod` on 3 pairs, `check_drift(registry=…)`
  over 90 sites, `check_exclusions` context (round exclusions empty), plus the named-method registry
  (`src/hg_kseos/named_methods.py`) read directly via `registry_snapshot()` / `route(flow)` /
  `evaluate_activation_invariants()` / `LIFECYCLE_EVIDENCE["gstack"]`.
- None of the files read below was modified; HG-KSEOS config/** untouched; no git write; no host traffic.

## ACTIVE_SELECTED evidence actually present (quoted keys)

From `src/hg_kseos/named_methods.py::NAMED_METHODS` — the only `ACTIVE_SELECTED` source in the repo
(the literal token never appears in `config/**` or `control/**`; it is a code-registry field, per
`ACTIVE_SELECTED = {tid for tid, m in NAMED_METHODS.items() if m.runtime_required_now and m.current_execution_scope != "STANDBY"}`).
Role-keyed `gstack.*` methods that are ACTIVE_SELECTED (keys quoted verbatim):

- `gstack.plan-eng-review` — `current_execution_scope: USER_AUTHORIZED_ACTIVE_SELECTED_SLICES`,
  `runtime_required_now: True`, `provider_state: CERTIFIED_ACTIVE_SELECTED_SLICES`,
  `source_disposition: CONDITIONAL_RECOMMENDED / SELECTIVE`, fallback `hgk_native_plan_review`
- `gstack.review` (same scope/state; fallback `hgk_native_review`)
- `gstack.qa` (fallback `hgk_native_qa`)
- `gstack.cso` (fallback `hgk_native_security`)
- `gstack.ship` (fallback `hgk_native_release_checklist`, `final_authority: False`)
- `gstack.office-hours` (fallback `hgk_native_prw`)
- `gstack.retro` (fallback `hgk_native_retro`)

All 7 cite the same evidence pair: `HG-KSEOS_GSTACK_IDENTITY_READBACK.json` +
`HG-KSEOS_GSTACK_HERMES_BINDING_ACCEPTANCE.json`; the gstack lifecycle map also names
`HG-KSEOS_GSTACK_SELECTED_E2E.json` (pilot) and `HG-KSEOS_GSTACK_RUNTIME_INDEPENDENT_ACCEPTANCE.json`
(independent cert). All 5 evidence files EXIST under `evidence/review/` — **presence-only check;
their content was not validated**, and `evaluate_activation_invariants()` returned all-zero buckets.

7/19 roles thus have a role-keyed ACTIVE-SELECTED method with positive route(flow) evidence.
Everything else is a named gap below.

## Per-role readback (map declaration vs live registration)

Full rows with keys and dispatch receipts per role: `WS4_GSTACK_ROLEMAP_READBACK.json` → `per_role_rows` / `gaps`.
Complete-matching set:

1. `office-hours` (ADOPT → active, router flow "ambiguity interrogation" → `gstack.office-hours`)
2. `plan-eng-review` (ADOPT → active, "plan review" → `gstack.plan-eng-review`)
3. `review` (ADOPT → active)
4. `qa` (ADOPT → active)
5. `cso` (ADOPT → active, "security review" → `gstack.cso`)
6. `ship` (SUPPORT_ONLY → active as `gstack.ship`, `final_authority=False` — consistent with the map's own SUPPORT_ONLY)
7. `retro` (ADOPT → active)

Gaps, named explicitly:

- **DECLARED_NOT_SELECTED (2)** — `autoplan`, `qa-only`. Both are ADOPTed in the map and in the
  snapshot TSV (ADOPT, both row sets agree), but no role-keyed method exists; `route("autoplan")` and
  `route("qa only")` fall onto the *shared* ACTIVE methods `gstack.plan-eng-review` and `gstack.qa`
  (registry `elif` ordering: `el if "plan" in flow` / `"qa" in flow`), never onto an autoplan/qa-only
  branch, which do not exist.
- **MAP_ROLE_ABSENT (6)** — `design-consultation`, `investigate`, `benchmark`, `document-*`, `canary`, `codex`.
  The map and the TSV declare all of them (dispositions MAP_TO_EXISTING_OWNER, `canary` local-paper,
  `codex` tracked-writer, `fallback: sealed-codex-lane`), and the map prints
  `missing_disposition_count: 0` — meaning no declared role is missing a disposition — but the live
  router has **no GSTACK branch for any of their flows**:
  - `investigate research`, `benchmark perf`, `document writing`, `canary rollout`, `coding delegation` →
    `route=NATIVE, provider=None` (they ride the native HGK surface with no named-method receipt at all)
  - `design consultation` → also `route=NATIVE` (the `plan-eng-review`/`review` branches trigger on
    "plan"/"review" substrings, which "design consultation" does not carry).
- **MAP_TO_EXISTING_OWNER shared dispatch (4, by the map's own declared intent — not a gap)** —
  `plan-ceo-review`, `plan-design-review`, `plan-devex-review`, `devex-review`. All four are
  MO_RExistingOwner rows and their flows land on the ACTIVE `gstack.plan-eng-review` /
  `gstack.review` methods. Consequence stated plainly: these four roles have no role-keyed
  route(flow) evidence of their own; their verification depends on the shared flow branch only.
- **SELECTED_NOT_IN_MAP: 0** — every `gstack.*` method that is ACTIVE_SELECTED has a map counterpart.

Snapshot cross-check: the TSV's `stage2_disposition` column matches the map's `disposition` for all
19 rows; both agree on hosts, worker modes, and `NO_ADOPT_CONTROL_PLANE` in `authority_ceiling`.
`hard_deny` surfaces were neg-probed 0-breaches, and `authority_ceiling=NO_ADOPT_CONTROL_PLANE`
aligns with `architecture.ADOPT_FULL_GSTACK_CONTROL_PLANE=false`.

## What the LIVE registry routes (per role's host/category — with the map's role-to-lane reference)

The registry has **no gstack role names**; none of `office-hours|plan-ceo-review|autoplan|cso|benchmark|canary|hgk-*`
appears in `lane-routing-registry.yaml` (verified by grep). Per-role lane attribution below is
**our inferred role-to-lane reference** (role-category adopted to lane_group per AGENTS.md §Files &&
`map_role_to_lane`), not a registry key.

| map role(s) | registry lane_group | live registry route (top-level route_for_lane) |
|---|---|---|
| `cso`, `review`, `qa*` | VERIFY_SECURITY | `hermes` / `openai-codex / gpt-6.1-sol` (medium), `selected_arm A`, identity `gpt-6.1-sol`, fallbacks `opencode-go / glm-5.3-flash` → `opencode-go / deepseek-v4.1-flash`, `admission_status: UNPROVEN` |
| `review`, `qa*`, `devex-review` | VERIFY lane shapes | same row (lanes ACCEPTANCE / SECURITY REVIEW / VERIFY) |
| `plan-ceo-review`, `plan-eng-review`, `autoplan` | PLAN | `hermes` / `opencode-go / glm-5.3-flash` (medium), fallbacks `deepseek-v4.1-flash` → `gpt-6.1-sol`, `admission_status: UNPROVEN` |
| `plan-design-review`, `plan-devex-review`, `design-consultation` | PLAN-shaped | same row |
| `investigate` | PLAN/RESEARCH | same row |
| `codex` | EXECUTE | `codex-cli` / `opencode-go / deepseek-v4.1-flash`, fallbacks `gpt-6-luna (openai-codex)` → `nvidia/deepseek-ai/deepseek-v4.1-flash`, `admission_status: UNPROVEN` |
| `ship`, `canary`, `retro`, `benchmark`, `document-*`, `office-hours` | no registry lane | no per-role lane route; the map itself is the authority (ship/retro/office-hours advisory; canary local-paper; benchmark perf; document-* docs) |

`check_sod` returns, all three pairs OK: PLAN≠VERIFY (`glm-5.3-flash != gpt-6.1-sol`),
EXECUTE≠VERIFY (`deepseek-v4.1-flash != gpt-6.1-sol`), PLAN≠EXECUTE (`glm-5.3-flash != deepseek-v4.1-flash`).
`assignment_cross_check`: the registry's `source_of_routes` pin matches the live bytes of
`config/model-lane-assignment.json` (sha256 `6af264…08753`), revision 19 == source-of-routes
revision 19 == registry epoch 19 == assignment `registry_epoch` — all hash-bound in the JSON.

`check_drift(registry=…)`, 90 sites: **1 DRIFT_VALUE (severity error)**, at
`config/hermes-codex-lane.json::/codex_sha256` — expected `D13914CE…DAEC`, actual
`e98c516f…c495b99e`. This is not a lane route finding; it is the known AGENTS.md
"Lane-chain contract… KNOWN STALE POINTER pending owner approval" residual, recorded as such in
AGENTS.md (epoch 18 note) and not repaired here (repair = owner-ordered registry work, not a subagent write).

One in-artifact contradiction worth stating: the **epoch-18 lane-chain contract block in
AGENTS.md (lines 51–55)** still declares PLAN default `openai-codex/gpt-6.1-sol` while the live
registry epoch 19 routes PLAN to
`opencode-go/glm-5.3-flash`. The live registry is the newer authority (epoch-19
header names the 2026-10-15 owner PLAN rebind, order line "PLAN & Orchestrator 模型改成使用
GLM-5.3-Flash(OPENCODE GO), 因為GPT 配額耗盡", assignment `declared_by` field) — the AGENTS.md +
README epoch-18 lines are the stale side. We report this; we do not edit AGENTS.md. Two corollaries
are recorded in the JSON as `registry_sod_pairs_staleness` and `assignment_internal_contradiction`:
(a) `sod_invariants.pairs[PLAN, VERIFY_SECURITY].note` still describes the epoch-18 state
("owner re-points BOTH lanes to openai-codex/gpt-6.1-sol"), so its conclusion —
`distinct_required: false` — predates the epoch-19 rebind it summarizes; (b) inside
`config/model-lane-assignment.json` itself, `/sod/verify_security_lane` (plus
`verify_security_arm_A` / `verify_security_default_arm`) declares **arm A = opencode-go/glm-5.3-flash**
while `/assignment[2]/supply_selector.unspecified_default` + `arms[0]` declare
**arm A = openai-codex/gpt-6.1-sol**. `check_drift` passes both blocks because each is compared to
its own recorded expectation — the gate proves expectation-matching, not internal coherence of the
file it reads. In this round we report the contradiction; we do not smooth it over.

## SoD consequence for the current session (court-recorded owner data, plainly stated)

- **What the registry declares**: `sod_invariants.declared_conflicts` carries `SOD006-C2
  (OPEN_OWNER_ORDERED)` and `SOD-APPLY-01 (OPEN)`; `assignment.sod_conflicts` adds
  `SOD006-C3 (OPEN_OWNER_ORDERED, ruled_by: owner order 2026-10-15 (PLAN rebind, this session))`;
  `sod_invariants.pairs[PLAN, VERIFY_SECURITY] = distinct_required: false`. Caveat stated above:
  that pair-policy note describes the epoch-18 state it summarizes and is one epoch behind its own
  routes.

- **What is actually running (measured, session store)**: orchestrator session `20261015_125956_d5f877`
  (PLAN & Orchestrator role) = `deepseek-v4.1-flash` / `opencode-go`; **this** delegation
  (`deleg_68ec5414`, and the three child sessions `20261015_235535_*`) = `glm-5.3-flash` / `opencode-go`.
  Note the session model predates the epoch-19 rebind and kept its start-time pin; live
  `config.yaml model.default` is already `glm-5.3-flash`.

- **The collision**: the delegation (subagent) plane runs `glm-5.3-flash`, which is also
  VERIFY_SECURITY's **fallback1 arm B** identity — the assignment's own
  `verify_vs_plan_model_separation` records exactly this residual as `SOD006-C3`
  ("…that arm served the R6 checker turn"). Conversely the session PLAN plane (deepseek) remains
  model-distinct from VERIFY's default gpt-6.1-sol.

- **Plain answer**: is this a **court-recorded owner deviation?** Yes in kind — SOD006-C2/-C3
  are explicitly declared owner-ordered, recorded-not-enforced residuals (ruled_by fields name the
  owner order of 2026-10-15), not agent-decided, not hidden. But the current epoch-19 epoch-shift
  means **no `declared_conflicts` entry names the pair that actually collides TODAY by model token**
  on the delegation-vs-VERIFY-arm-B edge beyond SOD006-C3's note text: the conflicts records
  corroborate awareness, while the operative collision on this round's R7 child turns is served at
  the fallback plane. This is a recorded-bounded residual, not a session-level cover-up; but the
  formal conflict list is not itself refreshed to the new epoch (it remains epoch-aware only via
  cross-reference), which is the residual the next lane round must adjudicate.
- **What independence therefore does NOT exist**:
  1. **No model-axis independence on the delegation/checker edge** when VERIFY falls back to arm B —
    delegation children (glm-5.3-flash) and checker fallback (glm-5.3-flash) are the same token.
  2. **No provider-axis independence**: provider_axis_required=false;
    PLAN/EXECUTE/VERIFY-armA all sit on `opencode-go`.
  3. **No role-mandate enforcement on this surface**: `runtime_role_binding_assert.py` is not
    invoked by any runtime caller; the role mandate chain[] gate is a **declared** contract, not a
    runtime-enforced gate at this layer.
- **What independence DOES still exist** (also stated, not smoothed over): EXECUTE vs VERIFY ARM A
  are distinct (`deepseek-v4.1-flash != gpt-6.1-sol`), enforced by `check_sod` on the canonical identity;
  dispatcher refuses same-arm self-acceptance concurrently; and the registry declares arm A
  `openai-codex/gpt-6.1-sol` as the model the checker chain PROMISES when it is usable again
  (`usable_now: QUOTA_429_2026-10-15`), so the collision is a recorded-bounded residual, not a redesign.

Note transparently: **this very subagent is served by `glm-5.3-flash` on `opencode-go`** — the same
identity as VERIFY ARM B. That is the concrete measured instance of SOD006-C3 in the R7 round, not a
theoretical remark; it is the same residual the registry already records, and we do not
hide it here.

## Disagreements with the map (3, stated with the residual consequence)

1. **Only 7 of the 19 declared roles are live-routable as first-class GSTACK methods.** The map
   prints `missing_disposition_count: 0` and `ADOPT_FULL_GSTACK_ROLE_ARCHITECTURE: true`, and the
   snapshot TSV's `stage2_disposition` column agrees everywhere — but the 4 MAP_TO_EXISTING_OWNER
   plan-* rows + `devex-review` dispatch onto the shared `gstack.plan-eng-review` / `gstack.review`
   methods and carry no route(flow) evidence of their own. The map's `missing_disposition_count`
   counts *dispositions*, not *dispatchability*; the 4 shared rows are routeable only by decoration.
   The map's declared `hgk_native_*` fallbacks for all 12 non-role-keyed roles likewise exist
   nowhere in the router. Not a silent smoothing, but not a clean "full architecture adopted" either.
2. **ADOPT ≠ routable for `autoplan` and `investigate`.** `autoplan` is ADOPTed but
   `route("autoplan")` rides the shared `gstack.plan-eng-review` via the "plan"-substring rule — the
   map's own first-class route never exists. `investigate` (ADOPT, host `specialist-research-worker`)
   is the strongest single disagreement in the whole readback: it has **no GSTACK branch at all**
   (`route("investigate research")` → route=NATIVE, provider=None); it rides the native surface
   with no named-method receipt of any kind. Same class for `benchmark`, `document-*`, `canary`,
   `design-consultation`, `codex` (all `route=NATIVE` — no branch).
3. **`codex` (MAP_TO_EXISTING_OWNER, `sealed-codex-lane`) is present in the map but invisible to
   the named-method router.** `route("coding")` → NATIVE; the sealed lane is reached only through
   `assignment[EXECUTE].executor = "CODEX CLI (sealed HGK lane)"` and
   `effective_wiring.default_execute_route=CODEX_CLI_SEALED_LANE`, not the GSTACK surface. Two
   declaration-level handlers for the same role; recorded, not repaired here.

## What this round could NOT verify

- **Model-liveness / quota-availability for any arm — NOT MEASURED.** No probe turn was issued
  against `opencode-go/glm-5.3-flash`, `opencode-go/deepseek-v4.1-flash`, `openai-codex/gpt-6.1-sol`,
  or `openai-codex/gpt-6-luna`. The `registry_lane_route_readback` values are the **registry's own
  declarations replayed through the repo's loader**, not a runtime route. The registry's own
  `admission_status: UNPROVEN` on all three lanes is honored; `usable_now: QUOTA_429_2026-10-15`
  on the PLAN GPT arm is quoted but not re-measured.
- **The MAP-side role-host / `worker_mode` contract is not cross-checked against a worker pool**:
  the registry has no worker-pool projection these hosts (`hgk-orchestrator`, `hgk-qa`, `hgk-security`,
  `hgk-coding-factory`, …) resolve to in this round; the map's host binding is a declaration, not a
  runtime spine row, and the round did not probe worker liveness (ghost-worker check) at all.
- **The GSTACK lifecycle evidence files** (`HG-KSEOS_GSTACK_*.json`, 5 files) exist and produce
  all-zero `activation_invariants`, but their **content** (timestamps, verdicts, subject bindings)
  was NOT opened, parsed, or digested; the all-zero result is therefore a registry-internal
  consistency claim, not fresh independent acceptance. The five `evidence_refs` per method
  likewise unopened.
- `_handover` side receipt files are accepted as INPUTS, not re-derived. No cross-session
  replay of a GSTACK advisory turn was performed (route(flow) probe = pure code path, not the
  advisory method itself); route(flow) here shows the named-method *router's* deterministic
  dispatch, which is not the same gate as an accepted advisory-method turn for a worked flow,
  and the round does not claim it as one.
- **The per-turn mandate gate (`scripts/runtime_role_binding_assert.py`) was NOT executed here.**
  It exists only as an UNTRACKED file (`git status` → `??`), wired solely into the prior round's
  evidence runner (`evidence/FAR-LANE-ROUTE-REBIND-20261015/run_e2e.py`); no `src/**` or live
  dispatcher path imports it, so no mandate-file exists for this R7 subagent round and the
  fail-closed path could not be exercised with a real mandate. (Field `runtime_role_binding_assert_caller_graph`
  in the JSON carries the quoted grep/`git ls-files` evidence.)
- **Round-scope non-goals, not addressed:** `config/hermes-codex-lane.json` /codex_sha256 drift
  repair (owner-gated registry work), AGENTS.md/README epoch-18→19 text refresh, and the
  assignment-internal arm-A contradiction adjudication. Whoever runs the next lane repair round
  must not confuse this receipt with a live per-role dispatch receipt.

## Inputs' hashes (for binding; not self-referential)

| file | sha256 |
|---|---|
| `HGK/HGK_GSTACK_ROLE_MAP.yaml` | `f8b8b967b1acab723e290fa5c7c45ec1e376a7348bfd886b4049e7b1cc9f0627` |
| `HGK/HGK_GSTACK_UPSTREAM_CAPABILITY_SNAPSHOT.tsv` | `a4c427a6e0a96f981209bed437102643f52fd1a0ce6768d8ee445c31554960dc` |
| `config/lane-routing-registry.yaml` | `06a8d10aed3785a9fb015d76291c32ef26cc3d4b36c00eb8ec9f7860d6f550d2` |
| `config/model-lane-assignment.json` | `6af264c9ffdb57113be769842ac1a8503eb472a3c55f1941ee42667078808753` |

Registry epoch 19; assignment revision 19; `assignment.registry_epoch == registry.epoch == 19`.

## Claim ceiling

**DECLARATION-LEVEL READBACK, NOT A RUNTIME ATTESTATION.** This is a structural comparison of the
GSTACK role map against the LIVE lane-routing registry (epoch 19) and the repo's own named-method
registry, plus a live probe and gate-function execution. No GSTACK advisory turn was executed
on any model; no per-role worker was dispatched; no lane/config/map file was mutated (the two
R7 output files alone are written, and no credential material was read or printed); no
model-liveness or quota-support was measured. The machinery's own limits: route(flow) is the router's
deterministic decision path; `evaluate_activation_invariants()` zeroes are the named-method
registry's own bookkeeping, not fresh acceptance. Read the per-role `active_selected_evidence_keys`
in the JSON as the map's own declare-vs-live delta; every gap is named, none smoothed over.
