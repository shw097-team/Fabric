# FINDINGS F1 — `routes[].PLAN` is the one surface that disagrees with every other PLAN declaration

Round `LANE-RELIABILITY-CLOSURE-20261016` · measured 2026-10-16 · **recorded, NOT repaired** (out of this
round's authorised scope, which explicitly excludes a registry `routes[]` re-route)

Claim ceiling: this is a measured deviation report against the named governing documents below. It
asserts nothing about acceptance, and it does not authorise a repair. Any repair is a lane-chain
REBIND and needs an owner order of its own.

---

## 1. The measurand

The question this round set out to answer was: *is the PLAN lane's model selection usable and
reliable?* Answering it required establishing, per lane, WHICH surface actually selects the model.
For PLAN that produced a five-way comparison, and four of the five agree:

| # | surface (file) | who consumes it | PLAN declaration |
|---|---|---|---|
| 1 | `config/lane-route-slots.candidate.json` → `lanes[PLAN].ordered_pool[rank 1]` | **the dispatch path** (`hgk-lane-dispatch.py --pool`, resolved live in this round's probe) | `openai-codex` / `gpt-6.1-sol` / `reasoning_effort: medium` / `auth: openai_oauth` |
| 2 | `config/lane-routing-registry.yaml` → `sod_invariants.pairs[PLAN vs VERIFY_SECURITY]` + `declared_conflicts[SOD006-C2]` | SoD / constraint checks | PLAN == VERIFY == `openai-codex/gpt-6.1-sol` (`distinct_required: false`, conflict `OPEN_OWNER_ORDERED`) |
| 3 | `tests/test_lane_policy.py` → `owner_chain` table (the repo's own conformance gate) | CI / pre-commit | PLAN rank-1 = `("openai-codex", "gpt-6.1-sol")` |
| 4 | `var/LANE-RELIABILITY-CLOSURE-20261016/role_mandate.json` → `roles.PLAN` (this round's owner mandate) | the per-round pre-dispatch gate `runtime_role_binding_assert.py` | `openai-codex` / `gpt-6.1-sol` / `medium` |
| 5 | **`config/lane-routing-registry.yaml` → `routes[].PLAN`** | `lane_policy.route_for_lane` (status / drift / Sod consumers) | **`opencode-go` / `glm-5.3-flash`** ← the outlier |

Surface 1's declared provenance is itself `declared_by: "FAR-LANE-REPAIR-20261014 apply
(owner-ordered)"`, and the registry's own epoch-19 header says the PLAN rebind was driven by an
OpenAI-OAuth `status=429` measurement taken **2026-10-15**, i.e. *before* the model-catalog repair.

## 2. The deviation, stated against the named governing documents

- **Against `tests/test_lane_policy.py` (the repo's own conformance gate).** The gate is RED on the
  canonical tree, before and after this round:

  ```
  AssertionError: Tuples differ: ('opencode-go', 'glm-5.3-flash') != ('openai-codex', 'gpt-6.1-sol')
  ('opencode-go', 'glm-5.3-flash')
  + ('openai-codex', 'gpt-6.1-sol') : PLAN rank-1 default must be owner-declared
  ```

- **Against `sod_invariants` in the same file.** One file asserts, in two places, two different
  things about the same lane. The SoD block already describes the post-rebind world; `routes[].PLAN`
  still describes the pre-rebind world. Whichever way the owner rules, one of them must move.

- **Against the owner mandate for this session.** The mandate names `gpt-6.1-sol` medium for PLAN.

## 3. Blast radius — measured, not asserted

- The **dispatch path is NOT affected**: this round's own probe resolved the EXECUTE pool live and
  the PLAN pool independently; the pool (surface 1) is correct, and `--require-arm` /
  `--force-rank` bind from the pool. So no lane has been silently dispatched at the wrong model
  through this defect.
- What IS affected: any consumer of `lane_policy.route_for_lane(reg, 'PLAN')` — status views, drift
  sweeps, SoD views, and the conformance gate above. Those report GLM for a lane the rest of the
  tree says is GPT, which is exactly the class of defect that makes a later session reconcile by
  archaeology instead of by reading.
- The identical misreading is already recorded in-repo as a **pre-existing** condition: the registry
  binding `/codex_sha256` pointed at a pre-repair digest (repaired this round under
  `WO-LANE-RELIABILITY-20261016-CHANGESET-A`). Two stale expectations in one file is a pattern, not
  an accident.

## 4. Low-friction remediation options (for the owner to order)

**R1 — re-point the route row onto the owner chain (RECOMMENDED; ~1 edit + the documented loop).**
Change `routes[].PLAN` to `openai-codex` / `gpt-6.1-sol` / `medium` / `auth: openai_oauth` /
`oauth: true` with `arms` = A(primary GPT) + B(fallback1 GLM) + fallback2 DeepSeek; bump `epoch`
20 → 21; then run `lane_policy.check_drift(registry=reg)` and rewrite each `projections[].bindings[]`
pointer it reports until fatal == 0; refresh `source_of_routes` LAST; append a `history:` entry at the
REAL top-level `history:` key. Expected outcome: `tests/test_lane_policy.py` 3/3 green, and
`check_sod(PLAN, VERIFY)` flips from `SOD_OK` to a **declared collision** — already recorded as
`SOD006-C2 OPEN_OWNER_ORDERED`, so no new SoD record is needed. Cost: one apply script (the
ChangeSet A machinery in this round is reusable); risk: config-data only, fully reversible via
`.bak`, and the drift loop proves it before any consumer sees it.

**R2 — re-point the mandate instead (not recommended).** Keep `routes[].PLAN` on GLM and change the
conformance chain + the mandate to GLM. This contradicts the owner's 2026-10-16 order and the pool's
owner-ordered rank-1, and it would put the lane's *dispatch* default on GLM while the SoD block stays
declaring GPT — moving the contradiction rather than closing it.

**R3 — waive it in writing (lowest effort, keeps a permanent RED).** Record an explicit, authority-named
waiver and accept that `tests/test_lane_policy.py::test_registry_and_projection_shape` fails on every
full-suite run until R1 lands. Cheapest, but it normalises a RED gate, which is the failure mode the
skill's own rule warns about ("never weaken the sweep to unconditional ok").

**Not an option:** patching the conformance test to assert GLM. The skill's rule for a DEMOTED pair is
to assert that the collision is REAL and that an OPEN declared conflict EXISTS — not to relax the
assertion for the pair that is not demoted. PLAN vs VERIFY is declared demoted (SOD006-C2); the
outlier here is the route row, not the gate.

## 5. Why this round did NOT repair it

This round's PLAN (§2) lists `no registry routes[] re-route` among the things it is **not**
authorised to do, and the prior session's own playbook
(`hgk-kanban-and-lane-routing/references/lane-chain-rebind.md`) classifies a lane-chain rebind as a
canonical config mutation that is owner-ordered and WorkOrder-gated, "never performed inside a
candidate maker round". An agent that both detects the deviation and silently re-routes the lane it
is being asked to certify would be grading its own homework. It is recorded here instead, with the
remediation priced.

## 6. Reproduce

```
# canonical root
python -B -m unittest tests.test_lane_policy -v          # 1 failure: test_registry_and_projection_shape
python -c "import sys;sys.path.insert(0,'src');from hg_kseos import lane_policy as lp;\
reg=lp.load_registry('config/lane-routing-registry.yaml');\
print(lp.route_for_lane(reg,'PLAN')['provider'], lp.route_for_lane(reg,'PLAN')['model'])"
# -> opencode-go glm-5.3-flash      (vs pool rank-1 openai-codex/gpt-6.1-sol)
```
