# Hermes cross-provider model routing: config, verification, pitfalls

Durable knowledge from the WO-HGK-PFR-001 provider-failover upgrade (2026-08-23).
Hermes-native runtime mechanism; records how to configure/troubleshoot it safely
on this stack (Windows + HGK governance).

## Native cross-provider fallback (Hermes)
- `fallback_providers` is a **top-level YAML list** in `config.yaml`; each entry is
  `{provider, model}` and may be a DIFFERENT provider → real cross-provider
  failover (a same-provider chain dies together on quota).
- Triggers: 429 (rate / daily-quota), 500/502/503, 401/403, 404, malformed/empty
  responses, connection failures.
- **Reset-aware**: if the primary reports a subscription-window reset not yet
  elapsed (OpenCode/Claude "5-hour blocks", Codex weekly limits), Hermes skips
  doomed retries and STAYS on the fallback until the window passes — so a 5h-window
  hit keeps the session on the free fallback for the rest of the window.

## Why "can't switch provider" — root cause (credential gate)
A provider is usable by Hermes only when a credential is wired in. Only
credentialed providers are materialized at runtime / in the picker;
`switch_model()` (model_switch.py Path-A) does "Resolve credentials" and refuses
to hop onto an unauthed endpoint (classic HTTP 401). So:
- `~/.hermes/.env` must hold the key (e.g. `OPENROUTER_API_KEY`).
- Non-interactive switch: `hermes model <m> --provider <p> --global` (takes effect
  NEXT session) or session-only `/model <m> --provider <p>`; or
  `hermes config set model.provider X` + `hermes config set model.default M`.
- `hermes model` is interactive-only (prompt_toolkit picker) — not drivable headless
  in a desktop/gateway context.

## PITFALL — `hermes config set fallback_providers '<json>'` corrupts the list
`hermes config set` stores a STRING for a list-typed key (quotes the JSON), so
`hermes fallback list` then reports "No fallback providers configured" and the
chain is broken. `hermes fallback add` is the sanctioned add-path BUT its picker
only offers curated models — it cannot type an arbitrary OpenRouter `:free` slug.
**Working route**: backup `config.yaml` → targeted structured edit (string-replace
just the `fallback_providers:` block, leave every other byte untouched) → readback
`hermes fallback list` + `python -c yaml.safe_load` + `hermes config get`, and
confirm integrity keys (`database.journal_mode`, `agent.max_turns`) still present.
Never leave a JSON-string in place of the list.

## Choose a free emergency model by TOOL-CALL probe, not vibes
The emergency-checkpoint path must call tools (write files, persist state) on the
free backend. Before selecting, POST a chat completion asking for a tool call and
assert `finish_reason == "tool_calls"`. Also:
- `:free` models are single-model rate-limited (~20 req/min / per-model contention);
  the "best" model can 429 while a cheaper sibling passes.
  ⇒ configure a CHAIN of ≥2 free lines and design acceptance as "at least one free
  line reachable+tool-calling" = PASS, recording the 429 as a live_finding (not a
  failure). Redundancy, not a single pick.

## MSYS → python path trap (git-bash on Windows)
Passing a `/c/...` path to a Windows `python.exe` resolves to `C:\c\...`
→ exit 2 "can't open file". Use the Windows-style `C:/...` path when invoking
python from git-bash or redirecting output into a receipt.

## Emergency checkpoint location
`~/.hermes/var/checkpoints/<task-slug>.md` with YAML front-matter: task_goal,
current_step, step_index, partial_outputs/artifact_paths, next_actions,
resume_token, detected_at, active_provider, active_model. Hermes auto-persists
sessions (state.db + `sessions/*.jsonl`); resume via the `@session` link or
`/resume <session>`.

## Minimal simulated live-run ("live-smoke") to SEAL an honest ceiling
Proves a fallback scheme ACTUALLY works live (not just from config/docs), without a
real outage, without touching production config or the live session. Validated on
WO-HGK-PFR-SMOKE-001 (2026-08-23). Validated harness at
`HG-KSEOS/var/provider-failover-routing/tests/live_smoke.py`.
1. Build an **isolated ephemeral HERMES_HOME** (temp dir with a minimal config.yaml + .env).
2. Make the primary fail, run a minimal one-shot task
   `HERMES_HOME=<temp> hermes chat -q "<write marker + report provider/model>" -Q`.
   Subprocess env: filter out inherited `HERMES_*` vars (a stale `HERMES_SESSION_*`
   can confuse the isolated run); the temp home gets its own state.db.
3. Assert: exit 0, the free model wrote the marker (`FAILOVER_OK`), and the temp home's
   `state.db` sessions row records `billing_provider=openrouter` + model ending `:free`.
Two proven scenarios:
- **401 auth path:** poison the primary API key to garbage → 401 → cross-provider
  failover → OpenRouter free completes the task.
- **429 + 5-hour-reset path** (faithful to a "5h usage window"): a local `http.server`
  stub returns HTTP 429 + `Retry-After`/`X-RateLimit-Reset` on every call; point a
  `custom` provider at it (`model.provider: custom`, `model.base_url:
  http://127.0.0.1:<port>/v1`) with `fallback_providers` = the openrouter free lines.
  Assert completion on free AND a bounded stub hit count (<= ~8) → proves the
  reset-aware skip (no retry-loop on a doomed primary). Observed: 4 hits.
Security: the real OpenRouter key goes only into the isolated `.env`; never print it
(scrub `sk-or-v1-...` in logs); verify the harness holds no plaintext live key beyond
the redaction-regex literal.