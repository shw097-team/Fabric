# Model-lane routing + the Codex-EXECUTE route (ROUTE-LANE-001, verified 2026-10-06)

Durable mechanics learned wiring a PLAN/EXECUTE/VERIFY SoD scheme onto the canonical Hermes runtime
and the sealed HGK Codex lane. Load this when the order says "change the Hermes default EXECUTE route to
Codex CLI", "adopt a model SoD scheme", or "NVIDIA/GLM primary with OPENCODE GO fallback".

## Hermes machine-truth keys (there are only three, and one is not a config key)

| Goal | Surface | Value |
|---|---|---|
| Hermes delegates its agent loop to Codex | `model.openai_runtime` (`hermes config set`) | `codex_app_server` — **provider-gated, see below** |
| Every codex spawn uses the pinned binary | `model.codex_bin` (`hermes config set`) | the pinned `codex.exe` path |
| Codex must load the isolated lane config | **no config key exists** | `CODEX_HOME` in the launching process env |

- `hermes_cli/codex_runtime_switch.py` owns both keys; `get_current_runtime()` reads
  `model.openai_runtime` and `get_configured_codex_binary()` reads `model.codex_bin`.
- **`codex_home` has NO config key.** `agent/codex_runtime.py:_ensure_codex_session` builds
  `CodexAppServerSession(codex_bin=..., model=..., model_provider=...)` and passes no `codex_home`, so
  `agent/transports/codex_app_server.py` only sets `CODEX_HOME` when it is given one. With none, codex
  falls back to `%USERPROFILE%\\.codex`. ⇒ "EXECUTE runs on Codex" is only true when Hermes is launched
  through the sanctioned lane launcher (`scripts/start-hgk-hermes.ps1 -Action Hermes`), which is also the
  only thing allowed to set `CODEX_HOME` (a user/machine-level `CODEX_HOME` makes it throw
  `ERR_GLOBAL_CODEX_HOME_FORBIDDEN`). Record it as a PRECONDITION, never as a config value.
- **Which model codex will use is decided by the lane's `CODEX_HOME/config.toml`**, not by the Hermes
  provider: `model = "deepseek-v4.1-flash"` + `openai_base_url = "http://127.0.0.1:10101/v1"` (the relay).
  Hermes only forwards `model`/`modelProvider` when the Hermes provider is exactly `custom` — for every
  other provider it sends `model=None, model_provider=None` and codex resolves its own config. So
  "Codex must run model M" is proven by reading the lane `config.toml`, not the Hermes config.

## The relay is the single point of failure — and its credential scope is the usual cause

Every EXECUTE request goes `codex.exe → http://127.0.0.1:10101/v1 → opencode-go`. The relay config
(`%LOCALAPPDATA%\\HG-KSEOS\\opencodex-hermes\\config.json`) declares `"apiKey": "$OPENCODE_GO_API_KEY"`,
**expanded from the relay process's own env**. Symptom when it is missing:

```
400 {"error":{"message":"openai-chat requires a non-empty credential (authMode: key)"}}
```

in ~20 ms, i.e. before any upstream call. Diagnose it in three probes, all against the relay, never the
provider: (1) `curl http://127.0.0.1:10101/healthz`, (2) a direct `POST /v1/chat/completions` on the relay,
(3) `Get-CimInstance Win32_Process -Filter 'ProcessId=<listener pid>'` and read the **CommandLine** — a
listener started from the npm-GLOBAL `opencodex` (`AppData\\Roaming\\npm\\node_modules\\@bitkyc08\\opencodex`)
rather than the pinned runtime (`%LOCALAPPDATA%\\HG-KSEOS\\runtime\\opencodex-2.11.0`) was started outside
the launcher and therefore holds no credential. `runtime-port.json` / `ocx.pid` can name a DIFFERENT pid
than the real listener; trust `netstat -ano | grep :10101`.

Fix = do not edit the relay config; re-start the relay from the pinned runtime through the launcher, which
imports the credential from the canonical Hermes `.env` into the process env
(`Import-ProcessCredentialFromEnvFile`), then re-run `-Action Probe` for a provider receipt
(`provider_route_confirmed`, `provider_status: 200`, `provider_request_id`).
- `-Action Probe` starts its OWN relay and stops it in `finally` ⇒ after a probe the lane may be DOWN again.
  For a durable lane run `-Action StartOpenCodex` (background) and verify `/healthz`.
- The launcher refuses to run if the HUMAN `~/.codex/config.toml` still carries
  `openai_base_url = http://127.0.0.1:1010x/v1` or an `opencodex` catalogue (`ERR_SHARED_MUTABLE_CODEX_CONFIG_STILL_ACTIVE`).
- codex tries `ws://127.0.0.1:10101/v1/responses` first (426 Upgrade Required when `websockets:false`, or
  os error 10061 when the relay is down) and then falls back to HTTP. The ws noise is not the fault.

## `-Action Write` (the tracked-writer path) escapes its mandated model

`Write` walks a model chain (`binding.model` then `binding.model_fallbacks`) and advances on ANY non-zero
exit. With `deepseek-v4.1-flash, gpt-5.6-luna, glm-5.2` it will happily finish the work on `glm-5.2`.
When an order pins Codex to ONE model, the chain must be a single element (pass `-ModelChain <model>`) or
the launcher must be changed — otherwise the receipt's `write_model_used` proves the violation.

## Admission/kanban mechanics that cost a round each

- **A lease is required for every `transition_requirement`.** Without `acquire_lease(resource_id, holder,
  token, ttl)` first, it fails closed with `ERR_LEASE_REQUIRED:<id>`; the `token` you pass to the lease is
  the token the transition must carry.
- **One WorkOrder per TaskSpec.** `create_workorder` performs the taskspec `DRAFT→ADMITTED` admission, so a
  second `create_workorder` on the same taskspec dies with `ERR_WORKORDER_REQUIRES_DRAFT_TASKSPEC`. Give
  each writer/checker pair its own taskspec. `transition_requirement` also refuses a taskspec id
  (`ERR_REQUIREMENT_UNKNOWN`) — taskspecs have no standalone transition API here.
- **`hermes kanban --board <slug>` is a TOP-LEVEL option**, before the subcommand. `kanban ls --board x`
  is an argparse error, and a card silently never gets created if you put it after `create`.
- **Drive the board in topological order.** Parent-linked cards stay `todo` (unclaimable) until every
  parent is `done`; a flat claim loop across the DAG leaves the children untouched while reporting success.
- `claim <id> [--ttl]` takes no `--assignee`; assignment is `assign <id> <profile>`. There is **no
  `kanban reopen`** (only `reopen-review`), and `block` refuses a `done` card — to correct an
  over-stated completion, backfill with `kanban edit <id> --result "..."` plus a comment.

## Probe a mandated lane BEFORE wiring it, and triage auth-vs-outage properly

The revised scheme's VERIFY lane was "GLM-5.3, NVIDIA NIM primary". Probing it was decisive:
- NVIDIA's `/v1/models` answers **200 even with a garbage bearer token** ⇒ a 200 catalogue is NOT evidence of
  a working account. Always send a control request with a deliberately invalid credential: a fast `401`
  proves the completion endpoint checks auth (so the credential is fine and the fault is provider-side),
  while a hang on the real key with a fast 401 on the garbage key means **the model side is down and asking
  the user for another key is pointless**.
- Result: `z-ai/glm-5.3`, its sibling, and the streaming path all hung past 90 s on a valid credential
  while `opencode-go` answered `glm-5.3` in 1.4 s. Record the lane as `DEGRADED_PRIMARY`, run it on the
  declared fallback, and write the failover so the **model is preserved and only the provider changes** —
  that keeps PLAN/EXECUTE/VERIFY separation intact instead of collapsing it onto the executor's model.

## Adding fallback arms to a lane (what the platform allows)

- **Hermes has exactly ONE fallback chain, and it lives at the ROOT: `fallback_providers`.** There is no
  per-lane fallback surface (`delegation` accepts only `max_iterations`/`provider`/`model`;
  `auxiliary.<task>` likewise). Set it with `hermes config set fallback_providers '<json-array>'` and read it
  back with `config get fallback_providers`; `config get model.fallback_providers` answers "not set" because
  the key is not under `model`. Per-lane ORDERING therefore only ever exists in the declared assignment
  artifact — say so instead of implying the config carries it.
- **Measure every arm before declaring it, and never infer a provider-wide outage from one model.**
  On the same NVIDIA NIM endpoint and credential, `z-ai/glm-5.3` hung past 75 s while
  `deepseek-ai/deepseek-v4.1-flash` returned 200 in 32.6 s. Probe with a garbage-credential control in the
  same run: a fast 403/401 proves auth is checked (so the credential is fine and the fault is model-side),
  and the provider's own `/v1/models` is the authoritative list of what it will serve.
- **Confirm a model id EXISTS before wiring it** — `models_dev_cache.json` carries `canonical_model_id`
  (e.g. `openai/gpt-6-luna`, `zhipuai/glm-5.3`, `deepseek/deepseek-v4.1-flash`), and an unknown id fails at
  call time, not at config time.
- **Adding a fallback can only ever WEAKEN separation.** Re-check the maker != checker invariant across
  every arm combination (executor arms x verifier arms), not just the primaries, and report the arms where
  the *provider* axis collapses while the model axis still holds.
- **A model-specific provider fault can be cured by a variant on the SAME endpoint — test the variant before
  declaring a lane dead.** `z-ai/glm-5.3` on NVIDIA hung past 75 s while `z-ai/glm-5.3-flash` answered
  HTTP 200 in 1.7 s on the same endpoint and credential. "Provider down" and "lane must run on its fallback"
  are conclusions about a MODEL ROUTE, not about a host.
- **Re-pin the lane's operational surface, not just the declaration.** For Kanban-routed lanes the effective
  pin is the card override (`hermes kanban set-model <id> <model> --provider <p>`; the model is positional,
  `none` clears it), which is separate from the assignment file — change both or the next dispatch keeps the
  old model.
- **Only the namespace the lane relay exposes can be a Codex lane model.** With a single `providers`
  namespace in the lane `config.json`, any cross-provider fallback must run on the Hermes provider client
  instead; keep the lane pinned to its sanctioned model and declare those arms as out-of-lane.

## Pitfalls a full round proves (verified against the running stack)

- **`model.openai_runtime: codex_app_server` is a NO-OP for providers other than `openai` / `openai-codex` /
  a named custom provider.** `hermes_cli/runtime_provider.py` gates the rewrite; with `provider: opencode-go`
  the turn runs on the native loop and the sealed lane records **zero** usage rows. Prove it with an isolated
  `HERMES_HOME` one-shot: exit 0 and the model's marker appear, yet the lane's `usage.jsonl` gains nothing.
  Never set this key to "route a non-OpenAI provider through Codex" — and note it also removes
  `delegate_task`, `memory` and `session_search`, so it would break every SWARM/VERIFY lane built on
  delegation. Hand EXECUTE to Codex at the **orchestration layer** (the lane dispatch) instead.
- **A relay model list is not an admission gate.** Deleting a model from `subagentModels` / `models` /
  `selectedModels` does not stop it being served: a de-listed model still returned `200` with usable content
  on the relay's direct completion path. The only enforcement that holds is the **call site** — pass
  `-ModelChain <single-model>` and assert the receipt: `write_chain` must be exactly one element and
  `write_model_used` must equal it. Label the config-surface pin `UNPROVEN_AS_ENFORCEMENT` and name the
  call-site pin as its compensating control.
- **Backfill a finished card with `hermes kanban edit <id> --result "..."`.** `update --result` does not
  exist and fails with exit 2 — silently, if you redirect stderr. `edit` also accepts `--summary` and
  `--metadata` (JSON dict on the latest completed run). Run it from the parent session: inside a
  `delegate_task` child the CLI refuses with "delegate_task child contexts cannot mutate Kanban tasks or
  boards", so a checker lane must read the board through a read-only SQLite connection.
- **Do not trust the delegation completion banner.** It can report the subagent model as rejected
  ("HTTP 400: not a valid model ID ... every task in this batch failed before doing any work") while both
  children actually ran and returned full results. Confirm the serving model in `logs/agent.log`
  (`agent.turn_context: ... model=... provider=... platform=subagent`) before believing either the banner or
  the absence of results.
- **Budget lane probes above real model latency and persist each result as it lands.** An isolated one-shot
  costs 25 s+ per model call plus tool rounds: a 240 s process budget expired mid-answer while the lane was
  demonstrably working (API call logged, three tool calls executed). Write the receipt incrementally so a
  later budget kill cannot lose the lanes that already finished.
- **Run the CLI as `hermes_cli/main.py` FROM the source root.** Invoking it with a hardcoded interpreter and a
  different cwd fails with `ModuleNotFoundError: No module named 'hermes_cli'` (sys.path[0] becomes the
  `hermes_cli/` package dir). Use the sanctioned launcher/interpreter from inside `hermes-agent/`, or set
  `PYTHONPATH` to the source root.
- **Never watch a tree the maker is still writing to, and attribute a negative containment result before
  reporting it.** A containment digest taken over `config/` + `var/<change>/` returned
  `no_writes_by_lanes: false` purely because the maker was writing its own remediation artifacts into the
  same tree during the lane run. Attribute first: check the lane's own session transcript for write tools
  (`messages.tool_name`/`tool_calls` in the lane's `state.db` — `read_file` + a read-only `terminal` clears
  it) and check the receipt's own `out_of_band_violation` field, then report either a violation or a
  false alarm. Snapshot the watched tree to a copy, or watch only paths the maker has frozen.
- **Hash append-only logs together with their byte length and line count.** A whole-file digest of
  `usage.jsonl` goes stale as the log grows; recording size+lines keeps append-growth distinguishable from
  fabrication when a checker recomputes it later.

## Dispatcher call-site facts that cost a call each (measured)

- **`--lane` takes `PLAN | EXECUTE | VERIFY_SECURITY`** — passing `VERIFY` dies with
  `ERR_SLOT_LANE_UNKNOWN` (exit 2) before any spawn.
- **`--codex-arg` must use the `=` form**: `--codex-arg=-c` works; `--codex-arg -c` makes argparse read
  `-c` as an option and exit 2 with "expected one argument".
- **A read-only role default is not a pin.** `SANDBOX_BY_LANE` fixes only the sandbox; the ARM comes from the
  lane's `ordered_pool` rank 1, so a plain dispatch of the VERIFY lane serves the EXECUTE model and
  `--require-arm` then fails the run closed (`ERR_REQUIRED_ARM_NOT_SERVED`) *after* the turn was served.
  Pin the checker with `--force-rank <rank of its declared arm>` **and** `--require-arm <provider>/<model>`.
- **Never dispatch a lane from `execute_code`**: that cell is capped at 300 s and kills the dispatcher
  mid-attempt (leaves an `attempt.marker.json` with no log). Use `terminal` with a 600 s budget.
- **A repair/retry is refused when the prior attempt has no `EXIT=` log**
  (`ERR_REPAIR_PRIOR_ATTEMPT_NO_LOG`). The `--prior-attempt-*` + `--allow-unverified-prior-gone` triple does
  not help when the prior marker's `log_path` is null; start a **fresh `--attempt N` without the prior flags**
  after confirming no orphan process is alive.
- **Deterministic seam for any argv-level change**: `--codex-executable <recorder.py>` runs a `.py` child under
  the current interpreter, so a stub can assert the exact child argv with no model, no spend, no home touched
  (the stub cannot emit the nonce, so the dispatch itself ends `exit 3 / ERR_LANE_ALL_ROUTES_EXHAUSTED` —
  expected, and the recorded argv is the evidence).
- **To test a proposed dispatcher patch without applying it**, copy the script, edit the copy, `py_compile` it,
  then `importlib` the copy and call `run_candidate(entry, args, codex, lane_home)` with a
  `SimpleNamespace`. `run_candidate` touches exactly these args fields: `lane, sandbox, prompt,
  relay_base, cwd, codex_arg, nonce, timeout, usage` (a missing one raises `AttributeError` inside it, and
  `ROOT` resolves from `__file__`, so pass absolute paths such as `cwd`).

## SoD sanity rule an operator instruction can violate

"PLAN and VERIFY on the same model/provider as EXECUTE" is self-contradictory for a governed stack whose
AGENTS.md forbids maker self-acceptance. When an order contains both clauses, do not pick silently: run the
coherent clause, freeze the conflicting one as superseded in the declared assignment artifact, and surface
it for adjudication. A green probe on such a lane is not a licence to collapse the separation.
