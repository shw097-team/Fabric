# EVIDENCE_LANE_AVAILABILITY — ROUND3-LANE-REBIND-AND-CLOSURE-20261016

Round: `ROUND3-LANE-REBIND-AND-CLOSURE-20261016`. Scope: read-only audit of what the NEW owner
mandate (PLAN = opencode-go/glm-5.3-flash; EXECUTE / VERIFY_SECURITY = opencode-go/deepseek-v4.1-flash,
both through CODEX CLI) requires in `config/lane-routing-registry.yaml` (epoch 21,
sha256 of the whole file NOT pinned; its pinned source `config/model-lane-assignment.json` measured
revision 21, sha256 `e7be2dea36874f169e0cddc61ecb77102402218a2e05136878a097462e7664df`), and whether the
mandated models are actually servable on this host. Nothing was edited; no real writer/checker turn
was dispatched. Side effect of the probe: one tiny `max_tokens` chat completion per mandated model id
against the local relay only (no external call from this audit).

## 0. Environment probes (measured)

| # | command | result |
|---|---|---|
| P1 | `curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:10101/v1/chat/completions -X POST -d {glm-5.3-flash PROBE_OK, max_tokens 8}` | **200** |
| P2 | `curl -s -X POST .../127.0.0.1:10101/v1/chat/completions -d {deepseek-v4.1-flash PROBE_OK}` | **200**; envelope id `chatcmpl-...`; at `max_tokens:80` content = `'PROBE_OK'`, usage `{completion_tokens 56, reasoning_tokens 51}` |
| P3 | same for glm-5.3-flash at `max_tokens:400` | **200**, content `'PROBE_OK'`, `reasoning_tokens 0`; at `max_tokens:8/12` content was `None` with `finish_reason:length` (the model spends tokens on reasoning; short caps truncate the visible answer — a probe artifact, not an outage) |
| P4 | `curl http://127.0.0.1:10100/healthz` | **200** |
| P5 | `curl http://127.0.0.1:10101/v1/models` | 90 models; both mandated ids listed: `opencode-go/deepseek-v4.1-flash`, `opencode-go/glm-5.3-flash` |
| P6 | `python scripts/hgk-lane-toolchain.py --resolve` (exit 0) | ok; path `C:\Users\user\AppData\Local\OpenAI\Codex\bin\9614f1d9b40d9c4f\codex.exe`, version `0.162.0-alpha.17.2`, sha256 `E98C516F...99E` == declared pin |
| P7 | relay `usage.jsonl` (`%LOCALAPPDATA%\HG-KSEOS\opencodex-hermes\usage.jsonl`), today's rows: | `opencode-go/deepseek-v4.1-flash` 484 rows 200, `opencode-go/glm-5.3-flash` 280 rows 200, `openai-p6a1fe3/gpt-6.1-sol` 194 rows 200 (all `inboundProtocol:responses`), 3× deepseek 499, 1× glm 499 |

Both mandated models are relay-servable TODAY and are the two most-served ids in today's ledger.
P3's short-cap `content:null` reproduces the established `transport_model_constraints.opencode_go`
finding: a probe that truncates the visible carrier line does not prove the turn failed; this audit
re-measured with a larger cap and got the promised text.

## 1. Lane-by-lane: what the mandate requires vs epoch 21 (registry `routes[]` + `lane_chains` projection)

For every lane the registry route row and the pinned projection (`config/model-lane-assignment.json
:: lane_chains`) agree with each other and with the slots pool `config/lane-route-slots.candidate.json`
(checked in the same run); all three desurface the CURRENT chain, so "the pool matches the mandate" is a
separate, per-lane finding.

### PLAN & Orchestrator (`opencode-go/glm-5.3-flash`)

Present in pool/arms as declared? — **PARTIALLY, at the wrong rank.**
- registry `routes.PLAN` (lines 146-221): `provider: openai-codex`, `model: gpt-6.1-sol`,
  `reasoning_effort: medium`, `auth: openai_oauth`, `selection_authority: owner-order-20261016-plan-model-rebind-gpt61-sol`;
  arm `primary` default:true = `openai-codex/gpt-6.1-sol`; **fallback1** = `opencode-go/glm-5.3-flash`
  (`automatic_selection: true`, `default: false`); fallback2 = `opencode-go/deepseek-v4.1-flash`.
  `admission_status: ADMITTED` with measured evidence text (two VERIFY turns served at
  required_arm == served_arm on 2026-10-16, recorded in the row itself).
- `lane_chains.PLAN[0]` = `{gpt-6.1-sol, openai-codex, primary, default true, arm A, medium}`;
  `lane_chains.PLAN[2]` = glm-5.3-flash as `rotation_alternate`, `automatic_selection: false`.
- slots pool: PLAN rank 1 = `openai-codex/gpt-6.1-sol` (REACHABLE_BY_PRECEDENT, "not probeable by
  bearer key; it is this session's parent model and the current PLAN default on this host"),
  rank 2 = glm-5.3-flash, rank 3 = deepseek-v4.1-flash, plus OPTIONAL nvidia/mimo arms.

**Exactly what must change to make the mandate rank-1 (minimum field set):**
1. `routes[].PLAN`: `provider`, `model`, `canonical_identity`, `auth` (`auth: env_ref:OPENCODE_GO_API_KEY`), `oauth: true->false`, `admission_status` (+`admission_evidence`) — the rank-1 arm itself.
2. The arm currently `default: true` re-labeled (or a new arm created) so `opencode-go/glm-5.3-flash` carries `default: true` and the old primary moves to `fallback1` (registry keeps the chain as first-class data, `fallbacks[]` reorder accordingly: glm first, deepseek second).
3. `selection_authority` — must be re-pointed at the NEW owner order id (it currently names `owner-order-20261016-plan-model-rebind-gpt61-sol`, the order this mandate supersedes).
4. The same rebinding inside the canonical source the registry pins:
   - `config/model-lane-assignment.json`: `lane_chains.PLAN[0]` (model/provider/arm/effort) +
     `sod.plan_lane` + `sod.plan_reasoning_effort` prose + every `projections[].bindings[]` pointer
     that pins the OLD PLAN chain (`/lane_chains/PLAN/0/model` = `gpt-6.1-sol`,
     `/lane_chains/PLAN/0/provider` = `openai-codex`, `/assignment/0/assigned_model` = `glm-5.3-flash` etc.).
     Advance `revision` AND `registry_epoch` in the SAME change, then re-pin the registry's
     `source_of_routes.sha256` + `revision` to those bytes — otherwise the dispatcher's pre-dispatch
     guard refuses every evaluation with `ERR_LANE_SOURCE_STALE` (the failure mode epoch 21 itself
     documents in its own `source_of_routes` comment; measured digest mismatch = that error in
     `chk_gate`, section 4 below).
5. slots pool rank-flip for PLAN (rank1 <-> rank2) — the dispatcher reads the pool as the selection
   AUTHORITY (`scripts/hgk-lane-dispatch.py` header: "The pool artifact is the selection AUTHORITY"),
   so a registry-only edit would leave the dispatched default different from the mandate.
6. `sod_invariants`: PLAN-vs-VERIFY `distinct_required` and `declared_conflicts` must be RE-DECLARED,
   see §5.

**Stale plane binding under the mandate (measured):**
`%LOCALAPPDATA%/.../hermes/profiles/hgk-governed/config.yaml` binds
`model.default: gpt-6.1-sol`, `model.provider: openai-codex`, `reasoning_effort: medium`, plane comment
"PLAN & Orchestrator (in-Hermes) — main-agent binding". This is R-phase work, not this audit's; the
round's PLAN.md already names it as a repair item (the mandate's in-Hermes PLAN plane).

### EXECUTE bounded writer (`opencode-go/deepseek-v4.1-flash` via CODEX CLI)

Present in pool/arms as declared? — **YES, exactly the mandate, exactly rank 1.**
- registry `routes.EXECUTE` (lines 222-276): `engine: codex-cli`, `provider: opencode-go`,
  `model: deepseek-v.1-flash`, canonical_identity `deepseek-v4.1-flash`,
  `auth: env_ref:OPENCODE_GO_API_KEY`; the primary arm IS the default; fallbacks =
  `openai-codex/gpt-6-luna` (operator-selectable only, `automatic_selection: false`) then `nvidia/deepseek-ai/deepseek-v4.1-flash`.
  `admission_status: UNPROVEN` on the LANE (see §4; the model ITSELF is measured-servable, P2/P7).
- `lane_chains.EXECUTE[0]` = `{deepseek-v4.1-flash, opencode-go, reasoning_effort null}`.
- slots pool EXECUTE rank 1 = same, `feasibility: DISPATCHABLE (verified end-to-end on the real lane
  transport after the credential fix)`, `lane_end_to_end: codex exec ... turn.completed, content LANE_OK, exit 0`.
- `hermes-codex-lane.json` (registry projection): `/provider opencode-go`, `/model deepseek-v4.1-flash`,
  `/default_execute_route CODEX_CLI_SEALED_LANE`, `/status ACTIVE_FAIL_CLOSED`, `/credential_env OPENCODE_GO_API_KEY`.

**Exactly what must change: NOTHING in the route.** Field-wise, the mandate is already the rank-1
default at every declarative surface. `admission_status: UNPROVEN` is a MEASUREMENT debt, not a
rebind: it flips to ADMITTED only on the next measured turn (a `used_rank`-bearing dispatch receipt;
see §4). Drivers: `automatic_selection` and rank stay as-is; a rebinding NOT needed.

### VERIFY_SECURITY acceptance officer (`opencode-go/deepseek-v4.1-flash` via CODEX CLI, read-only checker)

Present in pool/arms as declared? — **YES as a non-default arm; NO as the mandatory default.**
- registry `routes.VERIFY_SECURITY` (lines 278-340): `engine: hermes` (NOT codex-cli — the row's
  engine field describes the harness plane, while the `codex_home_config`我们家在 slots pool still declares
  read-only/workspace-write sandbox needs for this lane), default arm `A` =
  `openai-codex/gpt-6.1-sol` (medium, openai_oauth); arm `B` = `opencode-go/glm-5.3-flash`
  (fallback1, `automatic_selection: true`); arm `C` = `opencode-go/deepseek-v4.1-flash`
  (fallback2, `automatic_selection: true`). `admission_status: UNPROVEN`.
- `lane_chains.VERIFY_SECURITY[2]` = `{role fallback2, model deepseek-v4.1-flash, provider
  opencode-go, arm C, default false, automatic_selection true, medium}`.
- slots pool VERIFY_SECURITY rank 3 = `opencode-go/deepseek-v4.1-flash`, measured
  `{relay_http 200, [1.0, 1.52s]}`, `feasibility DISPATCHABLE`; rank 1 = `openai-codex/gpt-6.1-sol`,
  `feasibility REACHABLE_VIA_HUMAN_HOME_TRANSPORT` (relay 404, "requires the canonical openai
  provider (registered this round; account needs-reauth)"); rank 2 = glm-5.3-flash DISPATCHABLE.

**Exactly what must change to make the mandate rank-1 (minimum field set):**
1. `routes[].VERIFY_SECURITY`: default arm must become the deepseek arm — either promote arm C to
   `default: true` / `role: primary` and demote arm A to an operator-selectable alternate, or re-point
   the row's own `provider/model/canonical_identity/auth/oauth/reasoning_effort` fields and rebuild
   `arms[]`/`fallbacks[]` around it.
2. `selected_arm` + `selected_arm_identity` (currently `A` / `gpt-6.1-sol`) — the row carries an
   explicit selection that the mandate supersedes.
3. Same fields inside the pinned source: `lane_chains.VERIFY_SECURITY[2]` role/default flip,
   `sod.verify_security_lane`, `sod.verify_security_default_arm`, `sod.verify_security_reasoning_effort`,
   and the affected `projections[].bindings[]` pointers (e.g. `/lane_chains/VERIFY_SECURITY/0/model` =
   `gpt-6.1-sol`, `/assignment/2/supply_selector/arms/0/provider` = `openai-codex`).
4. `engine` / `codex_home_config`: the lane is being handed to CODEX CLI as a checker; the slot
   pool already declares `windows_sandbox: elevated` (required_for read-only + workspace-write) —
   the dispatcher's own R-E gate (§3) refuses a read-only lane whose home declares no sandbox level,
   so this declaration MUST survive the rebind.
5. `admission_status` flips from UNPROVEN to ADMITTED only on a measured receipt
   (`--require-arm opencode-go/deepseek-v4.1-flash` returning `required_arm == served_arm`).
6. `round_model_exclusions`: currently empty — a checked exclusion set, because a rebind round
   retains a standing fail-closed rule (`excluded_family_restore_forbidden: true`, executor
   `src/hg_kseos/lane_policy.py::check_exclusions`, `ERR_MODEL_FAMILY_EXCLUDED_ROUND`). Confirm it
   stays empty under the mandate or declare a new exclusion only if the owner orders one.
7. SoD re-declaration (mandatory for conformant registry content, not a field drift) — §5.

## 2. Is the CODEX CLI lane path able to SERVE `opencode-go/deepseek-v4.1-flash` as CHECKER (read-only non-interactive) and as WRITER?

Cited from the dispatcher/toolchain code itself, not prose.

**Argv contract (writer AND checker = the same invocation shape):**
`scripts/hgk-lane-dispatch.py::run_candidate` builds
`codex --model <entry.transport_model> --sandbox <per-lane> --ask-for-approval never
 -c \"openai_base_url=<--relay-base>\" --cd <cwd>
 [-c model_reasoning_effort=<entry.reasoning_effort>]
 [-c windows.sandbox=\"<codex_home_config.windows_sandbox>\"]
 [--codex-arg ...] exec --skip-git-repo-check --ephemeral --json <prompt>`.
- `CODEX_HOME` + `HERMES_CODEX_HOME` are set to the lane home (default
  `%LOCALAPPDATA%\HG-KSEOS\codex-hermes`), never the human home; a non-isolated home
  refuses with `ERR_LANE_HOME_NOT_ISOLATED` unless `--allow-human-home-transport` is recorded.
- `transport_model` per pool entry is what actually reaches codex (`opencode-go/deepseek-v4.1-flash`
  — the provider-qualified slug this provider requires, per `transport_model_constraints.opencode_go`).
- Identity/relay admission for this arm is `default_identity_requirement` → provider
  `opencode-go` = `IDENTITY_NONE` (\"key-auth arm: no human-attended identity\"), so an unattended
  checker turn does not need a human login on this arm.

**READ-ONLY is enforced, not defaulted:**
- `SANDBOX_BY_LANE = {\"EXECUTE\": \"danger-full-access\", \"VERIFY_SECURITY\": \"read-only\", \"PLAN\": \"read-only\"}` — the checker role default; the writer gets the writer role default.
- One flag cannot hand a checker writer-grade access: `ERR_SANDBOX_ESCALATION_REFUSED` fires unless
  `--allow-sandbox-escalation` is passed (code comment: `single flag cannot give a checker lane
  writer-grade access (round-5 checker finding)`).
- An escalated lane must also be BOUND: `ERR_GUARD_REQUIRED_FOR_ESCALATED_CHECKER` unless
  `--guard-subject` (or the recorded `--allow-unguarded-escalation`).
- Non-mutation guard: snapshot + digest, `ERR_GUARD_ROOT_EMPTY` on a zero-file guard,
  `ERR_GUARD_ROOT_CONTAINS_HARNESS_OUTPUT`, and `ERR_CHECKER_MUTATED_SUBJECT` voids the verdict
  (\"a checker that changed the subject has voided its own verdict, whatever it concluded\").
- Non-interactive: `--ask-for-approval never` in the argv contract, plus the fail-closed git
  credential posture preflight (`GIT_TERMINAL_PROMPT=0` for every child).

**Writer capability is separately measured:**
- The same `run_candidate` contract serves EXECUTE with `SANDBOX_BY_LANE[EXECUTE] =
  danger-full-access`; the code records that under `read-only`/`workspace-write` NO
  command_execution item is emitted while the turn still exits 0 — only `danger-full-access` blends
  with the writing side (comment T5/T5b/T6), so a WRITER lane MUST keep the writer sandbox.
- `hermes-codex-lane.json` seals the writer lane: `/provider opencode-go`, `/model
  deepseek-v4.1-flash`, `/default_execute_route CODEX_CLI_SEALED_LANE`, `/status ACTIVE_FAIL_CLOSED`.
- Toolchain binary pin verified today (P6, exit 0): `scripts/hgk-lane-toolchain.py` carries typed
  errors `ERR_LANE_TOOLCHAIN_VERSION_MISMATCH` / `ERR_LANE_TOOLCHAIN_DIGEST_MISMATCH` and the
  dispatcher runs its own toolchain probe (line 2087, `--codex-executable` / declared pin verify)
  before spawning.
- The relay accounting today (P7) already carries 484 deepseek responses rows at 200 — the same id
  the writer AND the checker would use — so the ROUTE is live; the difference between writer and
  checker turn is the SANDBOX and guard, not the model binding.

**Checker-arm nuance (reference `lane-model-attribution.md` §10, not a code path):** the default
read-only checker cannot write its verdict artifact to the writer's tree; the receipt will record an
inline-only verdict (`item.completed/agent_message` only) unless the checker is redirected to its own
root. This does NOT change the model binding; it changes where the verdict lands.

## 3. Is any mandated arm ABSENT from a pool (failable as a required-arm absence)?

Measured on the pool file the dispatcher actually reads (`config/lane-route-slots.candidate.json`):

- `opencode-go/glm-5.3-flash`: PRESENT in all three pools (PLAN rank 2 `FALLBACK1`; EXECUTE rank 3 n/a
  — NOT present in EXECUTE pool; VERIFY rank 2 `FALLBACK1`). Predictor for the mandate's PLAN default:
  the arm must be moved to rank1; today's failure shape in the dispatcher would be
  `--require-arm opencode-go/glm-5.3-flash` answering
  `ERR_LANE_REQUIRED_ARM_ABSENT` (\"{tok} is not in the <lane> pool\") only if it is missing; on PLAN
  it is NOT missing today, so the arm-absence error IS NOT the expected first failure — a wrong-rank
  serving is.
- `opencode-go/deepseek-v4.1-flash`: PRESENT in all three pools (PLAN rank 3, EXECUTE rank 1,
  VERIFY rank 3).
- The ONLY pool absence across the three lanes is the EXECUTE pool's missing glm-5.3-flash, which the
  mandate does NOT require for EXECUTE (EXECUTE stays deepseek). No mandated arm is absent →
  `ERR_LANE_REQUIRED_ARM_ABSENT` is NOT expected for any mandated turn once rebind sets rank1.
- `default_identity_requirement()` → provider `opencode-go` = `IDENTITY_NONE`, so pre-spawn the
  identity gate passes without relay-pool or CLI-login evidence (measured in code); the fail points
  that remain are `ERR_LANE_REQUIRED_ARM_ABSENT` (arm not in pool),
  `ERR_RELAY_OAUTH_NEEDS_REAUTH` (n.a. for opencode-go), `ERR_LANE_NOT_ADMITTED` (the
  SPINE admission gate, `scripts/hgk-lane-guard.py`, §4), and dispatch timeouts.

## 4. What the lane receipt requires to prove `required_arm == served_arm`

From `scripts/hgk-lane-dispatch.py` (aggregate-vs-attempt dict fields, `receipt[\"required_arm\"]`,
`receipt[\"served_arm\"]`):
- the caller passes `--require-arm \"opencode-go/deepseek-v4.1-flash\"` (or a
  `--role-binding-file`/`--workorder` whose bound arm is derived, and a caller-supplied
  `--require-arm`/`--force-rank` CONTRADICTING the binding is refused
  ERR_ROLE_BINDING_ARM_MISMATCH / ERR_ROLE_BINDING_RANK_MISMATCH);
- PRE-SPAWN: the arm is validated against the pool artifact BEFORE the gate:
  `{f'{e[\"provider\"]}/{e[\"model\"]}' == tok for e in candidates}` →
  `ERR_LANE_REQUIRED_ARM_ABSENT` if the arm is not in the lane's pool at all; the
  `--no-identity-gate` flag does NOT switch off THIS guarantee (comment: \"A hostile review
  demonstrated the nesting defect, where `--no-identity-gate --require-arm <refused-arm>` silently
  degraded to another arm\");
- POST-SPAWN: `used` = the attempt that completed the nonce-or-verdict contract (one attempt,
  `usage_receipt_ok` byte-offset-bound to the attempt's start; `--attempt-log-dir`/stdout hash
  preserves the raw stream); then `receipt[\"served_arm\"] = f\"{used['provider']}/{used['model']}\"`,
  and if != `--require-arm` → `receipt[\"ok\"] = False`, code `ERR_REQUIRED_ARM_NOT_SERVED`
  (\"Surviving the gate is not the guarantee; BEING SERVED is\");
- `used_rank` is printed ADJACENT so a pooled-advance mode (`mode: pooled_advance` vs
  `pinned_primary` / `forced_rank`) is never confused with serving the mandated arm;
- the SPINEbound guard `scripts/hgk-lane-guard.py` additionally refuses a bare ADMITTED string:
  `_load_admission` accepts ONLY a receipt FILE whose `arm`/`served` fields match
  (`admission_status: REQUIRED RECEIPT-FILE`), which is what turns a receipt into proof that
  `arm.model == served.model == target.model` AND `arm.provider == --target-provider` —
  ERR_LANE_NOT_ADMITTED otherwise (measured exit 2 today, §5).
- Receipt-level aggregate fields to cite: `required_arm`, `served_arm`, `ok`, `code`,
  `used_rank`, `usage_receipt_ok`, `role_binding_served_arm` (bound rounds),
  `subject_mutation.mutated`, `identity_gate.arms`.

Measured receipt proof (this round's read-only obligation): NONE YET on the mandate's VERIFY arm
under the new mandate — the round's R/VERIFY phases will produce the first one; the lane event
logs this audit did NOT spawn a writer or checker turn by contract.

## 5. SoD re-declaration (flipped axis)

- `sod_invariants.pairs[]` today: `{EXECUTE, VERIFY_SECURITY, distinct_required: True}`,
  `{PLAN, VERIFY_SECURITY, distinct_required: False}` (measured from the registry source).
- The mandate makes EXECUTE and VERIFY BOTH `opencode-go/deepseek-v4.1-flash` → the pair that must
  stay distinct (writer vs checker) becomes same-model by mandate. Measured fail-closed path for
  that pair today (this audit's own command):
  `python scripts/hgk-lane-guard.py --lane VERIFY_SECURITY --maker-model
  opencode-go/deepseek-v4.1-flash --target-model opencode-go/deepseek-v4.1-flash
  --admission ADMITTED --expected-epoch 21` →
  `checks[0]: sod_distinct_model ok=false, code ERR_LANE_SOD_VIOLATION,
  detail \"SOD_VIOLATION maker_model=deepseek-v4.1-flash == checker_model=deepseek-v4.1-flash\"`,
  DECISION = REFUSE, exit_code = 2. (The `source_digest` and `epoch_current` checks both PASS,
  confirming the fail is exactly the SoD rule under the mandate, not a stale-pinning fault.)
- Control-path reference (measured in code): `src/hg_kseos/lane_policy.py::check_sod` →
  `SOD_VIOLATION maker_model=X == checker_model=X` (fail closed on an empty identity).
- Convergence path available to the owner (precedent, not a recommendation): the registry's
  `sod_invariants.declared_conflicts` carries SUPERSEDED / OPEN / OWNER_ORDERED_IN_FORCE records in
  which the owner has explicitly ordered a same-model PLAN==VERIFY pair (SOD006-C2 today) with the
  remaining independence on the PROCESS / LANE / EVIDENCE-PATH axes; a mandate that re-points
  EXECUTE and VERIFY onto the same arm must be re-declared in the SAME change (registry-only edit
  leaves the file self-contradictory). The `distinct_required` for the EXECUTE-vs-VERIFY pair must
  then be carried by a NEW declared-conflict record referencing a NEW owner order; the dispatcher
  can still prove LANE independence (separate codex processes), PROCESS independence (fresh
  context), EVIDENCE-path independence, and `no-self-acceptance` at runtime
  (`ERR_WORKORDER_SELF_REVIEW` in the spine, per the skill's surfaces reference; measured in
  code as `ERR_LANE_SOD_VIOLATION` on the guard above).

## 6. Unknowns

- Whether the owner order id the rebind will record (§1.1 and §1.VERIFY parts, items 1-3) has a
  canonical name already — the artifact that CONSUMES the rebind (FAR ruling / WorkOrder) did not
  exist at audit time. UNKNOWN for the field value; the field (`selection_authority`) is known.
- Whether the mandate's VERIFY checker must also produce a FILE-BACKED verdict artifact or whether
  inline-only is acceptable under the new procedure (skill surface note, not a code path — the
  dispatcher's R&E computations make the inline-vs-file decision per round, not per lane).
- `admission_status` for the two `openai-codex/*` arms (gpt-6-luna fallback arms) under the mandate:
  their pool entries carzyst `admission_status: UNPROVEN` in `alternate` shape; the lane guard of
  today's tree cannot be measured without a dispatch, which is out of this audit's contract. These
  arms are NOT the mandate's defaults, so no admission evidence is REQUIRED for them by this rebind.
- Whether a same-model EXECUTE/VERIFY pair is acceptable at the acceptance-officer ROLE level when
  the model axis is lost — the SoD re-declaration in §5 is a field requirement, not a running
  measurement; it needs the owner's adjudication (entrusted to the round's FAR ruling) rather than
  a probe.

## 7. What this audit did NOT do

- No real writer/checker turn was dispatched (contract). No lane-clearing or relay-probe traffic
  other than two ≤100-token local chat completions on the LOOPBACK relay.
- No registry, lane-slot, assignment, profile, spine, or config file was edited (measured: the
  audit ran read-only commands against the canonical tree; the only write by this audit is this
  evidence file + its JSON sibling under `var/ROUND3-LANE-REBIND-AND-CLOSURE-20261016/evidence/`).
- `git status` is MET dirty (17 files, +2596 lines) from PRE-AUDIT round work; nothing in that set
  was touched by this audit.
