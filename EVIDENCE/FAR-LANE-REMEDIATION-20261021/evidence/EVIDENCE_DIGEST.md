# FAR EVIDENCE DIGEST — HG-KSEOS lane/model-version mix (round FAR-LANE-VERSION-MIX-20261021)

Measured 2026-10-21 (local, UTC+8) against `C:\Projects\Agent_Workspace\HG-KSEOS` @ HEAD `903e47c`.
Every row below is a LIVE readback, not a recalled claim. Round is READ-ONLY + bounded evidence writes
(`var/FAR-LANE-VERSION-MIX-20261021/`). WorkOrder `WO-FAR-LANE-MIX-001` (writer=codex), REQ FROZEN v1.

## S1. Five+ surfaces declare lane models, and they disagree

| # | Surface (path) | PLAN | EXECUTE | VERIFY_SECURITY | engine |
|---|---|---|---|---|---|
| S1a | `config/lane-routing-registry.yaml` `routes[]` (epoch **22**) | **glm-5.3-flash** / opencode-go, effort medium | deepseek-v4.1-flash / opencode-go | **deepseek-v4.1-flash** / opencode-go, effort medium | PLAN=hermes, EXECUTE=codex-cli, **VERIFY=hermes** |
| S1b | `config/model-lane-assignment.json` `lane_chains` | rank1 glm-5.3-flash primary; gpt-6.1-sol = `fallback1_operator_selectable` (note: "Rank-1 default of epochs 19-21") | rank1 deepseek-v4.1-flash | rank1 deepseek-v4.1-flash; gpt-6.1-sol = operator-selectable alternate | — |
| S1c | `config/lane-route-slots.candidate.json` `lanes[].ordered_pool` | rank1 glm (role label **FALLBACK1/備援1**) / rank2 gpt-6.1-sol (role label **DEFAULT/首選**, medium, openai_oauth) / rank3 deepseek (FALLBACK2) / rank4 mimo (OPTIONAL) / rank5-6 nvidia | rank1 deepseek (DEFAULT) / rank2 gpt-6-luna / rank3 nvidia deepseek | rank1 deepseek (role label **FALLBACK2**) / rank2 gpt-6.1-sol (role label **DEFAULT/首選**) / rank3 glm (FALLBACK1) / rank4 nvidia deepseek | — |
| S1d | `AGENTS.md` lines 53-55 (governing doc) | default **openai-codex/gpt-6.1-sol (medium, OAuth)** → glm → deepseek | default deepseek-v4.1-flash → gpt-6-luna → nvidia | default **gpt-6.1-sol (medium)** → glm → deepseek | "Hermes-internal" vs "Codex CLI" |
| S1e | `profiles/hgk-governed/config.yaml` (in-Hermes PLAN & Orchestrator plane) | **model.default = deepseek-v4.1-flash / provider opencode-go** (`_plane:` key says it IS the PLAN plane) | — | — | hermes |
| S1f | `config/model-lane-assignment.json::in_hermes_plan_orchestrator_plane.binding_surface` | DECLARES the same profile file must hold `model.default=gpt-6.1-sol`, `provider=openai-codex`; cites a 2026-10-16 probe (`PLAN_LANE_PROBE_OK`, state.db row gpt-6.1-sol) | — | — | — |
| S1g | `tests/test_lane_policy.py` lines 100-113 (conformance gate) | asserts `("opencode-go","glm-5.3-flash")` rank-1 | deepseek rank-1 | asserts `("opencode-go","deepseek-v4.1-flash")` rank-1 (comment: "same model as the EXECUTE writer BY OWNER ORDER") | — |
| S1h | `<HERMES_HOME>/config.yaml` (session default plane) | `model.default=deepseek-v4.1-flash`, `provider=opencode-go` | — | — | hermes |

**Contradiction set (measured, not inferred):**
- C1: S1a/S1b/S1g (registry+assignment+test) put PLAN rank-1 on **glm-5.3-flash**; S1d (AGENTS.md) and S1f put the PLAN plane on **gpt-6.1-sol**; S1e (live profile bytes) holds **deepseek-v4.1-flash**.
- C2: S1c labels the **rank-2** entry `DEFAULT/首選` while **rank-1** carries `FALLBACK1/備援1` (PLAN) and `FALLBACK2/備援2` (VERIFY) — rank order and role labels disagree inside one file.
- C3: S1a gives VERIFY_SECURITY `engine: hermes`, while S1d/S1c and the dispatcher's gate_scope treat VERIFY as a **Codex-CLI** lane (`scripts/hgk-lane-dispatch.py --lane VERIFY_SECURITY`).
- C4: S1b's own `prior_revision_note` records that gpt-6.1-sol **was** the rank-1 default of epochs 19–21 and was demoted on 2026-10-16; S1f (same file) still declares the gpt binding as current — two declarations inside ONE file contradict each other while `check_drift` reports nothing about it.

## S2. `check_drift` is NOT clean — 2 hard DRIFT_VALUE rows today

`lane_policy.check_drift(registry=reg)` → 2 × `severity: error`:
- `/codex_version` expected `0.162.0-alpha.17.2`, actual `0.163.0-alpha.10.2`
- `/codex_sha256` expected `e98c516f…b99e`, actual `9ecb9df2…a46d`
So the registry's projection pins an OLD Codex build while the lane config declares a NEWER one. `check_sod(PLAN, VERIFY_SECURITY)` returns `(True,'SOD_OK glm-5.3-flash != deepseek-v4.1-flash')` — the SoD gate is satisfied *because* the registry was rebound away from AGENTS.md's declaration; it never sees the gpt-vs-gpt collision the user mandate would create.

## S3. Toolchain pins: three-way version mix, one of them dead

- `config/hermes-codex-lane.json::codex_executable` = `…/OpenAI/Codex/bin/**e78bad9887fa50cf**/codex.exe` → **PATH DOES NOT EXIST** (verified `ls`).
- Same file `codex_version` = `0.163.0-alpha.10.2`, sha `9ecb9df2…`.
- `<HERMES_HOME>/config.yaml::model.codex_bin` = `…/HG-KSEOS/runtime/**codex-0.147.0-alpha.6.5**/codex.exe` → exists (Aug 7 build) — a THIRD, older pin.
- Live installed build: `…/OpenAI/Codex/bin/**896a0166b774037a**/codex.exe` → `codex-cli 0.163.0-alpha.10.2`.
- Consequence: a dispatch that trusts the declared pin fail-closes (`ERR_LANE_TOOLCHAIN_BINARY_MISSING`) **before any model is called**, which reads to an operator like "the model is unavailable".

## S4. Version-control status: the routing surfaces are UNTRACKED

`git status --short` → `?? config/lane-routing-registry.yaml`, `?? config/model-lane-assignment.json`,
`?? config/lane-route-slots.candidate.json`, `?? config/hermes-codex-lane.json`.
`git ls-files config/` → only `config/hermes.json`, `config/project.json`.
`git log -- <routing file>` → **0 commits** each. `.gitignore` also ignores `var/` and `var/shared-spine/*.db`.
So: the registry, the assignment, the pool and the lane binding — plus the spine DB and every evidence root —
have **no commit lineage**. The only history is ad-hoc `.bak-*` files in the same directory.

`.bak` census: `lane-routing-registry.yaml` 8, `model-lane-assignment.json` **13**, `hermes-codex-lane.json` 8,
`lane-route-slots.candidate.json` 6. Newest three all carry `…-round3-lane-rebind-20261016`; others span
`chainrebind-20261015`, `far-remediation-20261016`, `lane-reliability-20261016`, `planrebind-20261015`,
`pre-rebind-20261013`, `pre-rebind-20261012`, `final-route-20261008`. → at least **6 rebind generations in 13 days**
on the SAME three files.

## S5. Session plane vs lane plane (the user's question about "other sessions")

`<HERMES_HOME>/state.db::sessions` model counts (all sessions): deepseek-v4.1-flash 203, gpt-6.1-sol 127,
glm-5.3-flash 84, mimo-v2.6-pro 18. Recent order shows the chat plane flipping between deepseek / gpt / glm / mimo
across consecutive days, e.g. 2026-10-21 10:26→11:20 local: `Fallback activated: deepseek-v4.1-flash → mimo-v2.6-pro (opencode-go)`
after `Rate-limit backoff level 0`; `session_model_usage` records BOTH models in one session while
`model_config` still names deepseek — i.e. the SERVED model changed mid-session.
`<HERMES_HOME>/config.yaml::fallback_providers` HEAD was `opencode-go/mimo-v2.6-pro` (replaced by owner order today
2026-10-21 with `opencode-go/glm-5.3-flash`; receipt `var/config-change-mimo2glm-20261021/RECEIPT.md`).
Session-plane and lane-plane are separate by construction (S1f `not_the_binding`: per-session picker,
`delegation.provider/model`); conflating them is how a "PLAN=gpt-6.1-sol" mandate gets evaluated against the wrong surface.

## S6. Why some sessions CAN get gpt-6.1-sol on PLAN/VERIFY and others cannot (mechanism, enumerated)

CAN (any one path suffices):
1. **Pinned lane dispatch** with `--force-rank 2 --require-arm openai-codex/gpt-6.1-sol` against the pool (rank 2 = gpt, S1c). Proven today: VERIFY probe `ok=true, required_arm==served_arm==openai-codex/gpt-6.1-sol, used_rank 2` (`probes/probe_VERIFY.json`).
2. **In-Hermes PLAN plane** launched with `HERMES_HOME=<profiles/hgk-governed>` **while that profile held the gpt binding** (the 2026-10-16 measured state, S1f). Proven today with an explicit `-m gpt-6.1-sol --provider openai-codex` one-shot on the same profile: `PLAN_GPT_SOL_PROBE_OK`. NOT proven for the profile's CURRENT bytes, which hold deepseek (S1e).
3. **Per-session picker** set to gpt-6.1-sol (127 session rows) — a SESSION-plane fact that authorizes nothing about lanes.
4. Periods when GPT quota was available (owner note 2026-10-20; relay ledger shows 393 gpt-6.1-sol calls in the last 3 days).

CANNOT (any one suffices):
1. **Unpinned dispatch** — dispatcher walks the pool in rank order, so PLAN rank-1 glm / VERIFY rank-1 deepseek serve; `--require-arm` VERIFIES an arm but does not SELECT it (`--force-rank` is the selector).
2. **Registry-default dispatch** (`route_for_lane` top level, S1a) → glm/depseek, never gpt.
3. **Profile re-launch after the later rebind** → deepseek (S1e), while the declaration file still claims gpt (S1f).
4. **Round-level exclusion** `round_model_exclusions` (HGK-ROUND-MODEL-EXCLUSION-1, 2026-10-12 round) fail-closes gpt-* restores with `ERR_MODEL_FAMILY_EXCLUDED_ROUND`.
5. **Stale toolchain pin** (S3) → `ERR_LANE_TOOLCHAIN_BINARY_MISSING` before any model call.
6. **Pool epoch dependence** — the same lane that refused an arm at one registry epoch served it at the next; nothing cache-invalidates a pool verdict.
7. **Quota/upstream 429** on the serving provider → `fallback_providers` chain takes over (S5).

## S7. Governance debt in the control plane itself (closure quality)

`var/shared-spine/hg-kseos.db` workorder states: **CREATED 444**, VERIFIED 112, RESULT_RECORDED 20,
COMPLETED 11, ADMITTED 2, FAILED 1, ROLLED_BACK 1, COMPLETED_WITH_BINDING_DEFECT 1.
Requirement states: CANDIDATE 496, FROZEN 413, ACCEPTED 2, ADMITTED 1, OPEN 2.
→ most admitted work is never carried to a recorded result; "repair round" WOs are opened and left CREATED.

Prior rounds in `var/` matching FAR/lane topics: **44 directories**, including
`far-lane-health-repair-20261011`, `FAR-LANE-REPAIR-20261014`, `FAR-LANE-REUSE-RCA-20261015`,
`FAR-LANE-ENFORCEMENT-RCA-20261015`, `FAR-LANE-ROUTE-REBIND-20261015`, `far-lane-sod-003/004/005`,
`FAR-REMEDIATION-AND-CLOSURE-20261016`, `far-018`, `far-019`.

## S8. Lane-dispatch proofs run THIS round (raw receipts in `probes/`)

| Probe | Receipt | Result |
|---|---|---|
| EXECUTE attempt1 (no nonce requested — brief defect) | `probe_EXECUTE_attempt1_nononce.json` | `ok=false, code=ERR_NO_ARM_EMITTED_NONCE`; the TURN itself completed (`stdout_tail` carries `EXECUTE_DS_LANE_PROBE_OK`, `usage_receipt_ok=true`) — the nonce gate is transport attestation, not evidence of no work |
| EXECUTE attempt2 (nonce requested) | `probe_EXECUTE.json` | `ok=true`, `required_arm==served_arm==opencode-go/deepseek-v4.1-flash`, `used_rank=1`, `usage_receipt_ok=true` |
| VERIFY_SECURITY pinned gpt-6.1-sol | `probe_VERIFY.json` | `ok=true`, `required_arm==served_arm==openai-codex/gpt-6.1-sol`, `used_rank=2`, `usage_receipt_ok=true`, nonce present |
| PLAN in-Hermes plane gpt-6.1-sol medium | one-shot | stdout `PLAN_GPT_SOL_PROBE_OK` (exit 0) |

Mandated scheme therefore **IS usable**: PLAN gpt-6.1-sol (OAuth) / EXECUTE deepseek (Codex CLI) /
VERIFY gpt-6.1-sol (Codex CLI) — each bound by pin, not by default.

## S9. Residuals / claim ceiling for anything built on this digest

- `used_seconds` 3-4 s on both probes proves transport + arm binding, NOT long-run sustainability.
- The mandated scheme puts PLAN and VERIFY on the SAME model (gpt-6.1-sol): model-axis SoD between planner and
  checker is ABSENT by owner mandate; maker(EXECUTE=deepseek)≠checker(gpt) still holds. Process separation only.
- `.bak` mtimes are filesystem metadata, not authorship evidence.
- Session-row model labels are the SERVED model as recorded by Hermes; they are not independent provider attestation.
