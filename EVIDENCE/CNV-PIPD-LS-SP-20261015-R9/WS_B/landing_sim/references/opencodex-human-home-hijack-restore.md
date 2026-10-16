# opencodex human-home hijack: diagnosis, restore, and HGK-lane route re-verification

Verified 2026-08-15 on WO-HGK-GPTWORK-CODEX-RESTORE-001 (桌面APP版 GPT WORK / CODEX 恢復 OpenAI 原廠供應).
Consolidated 2026-08-15 from three parallel drafts (opencodex-codex-home-hijack.md +
opencodex-human-home-hijack-restore.md + gptwork-codex-desktop-restore.md) — this is the
single canonical recipe.

## What happened

The OpenAI ChatGPT desktop app's Work/Codex modes run on the HUMAN Codex home
(`C:\Users\user\.codex`). A third-party tool **opencodex (`ocx`)** — "Universal
provider proxy for Codex", npm `@bitkyc08/opencodex` — had hijacked that home:

- `~/.codex/config.toml` got injected: `openai_base_url = "http://127.0.0.1:10101/v1"` +
  `model_catalog_json = ~/.codex/opencodex-catalog.json` (24 `opencode-go/*` models) +
  comment `# Auto-injected by opencodex`
- `~/.opencodex/config.json`: `defaultProvider=opencode-go`, native `openai` provider
  `disabled: true`, `codexAutoStart: true`, `codexShimAutoRestore: true`, `port=10100`
- `~/.codex/models_cache.json` polluted with opencode-go model entries
- `~/.codex/auth.json` UNTOUCHED native ChatGPT login (`auth_mode=chatgpt`, tokens
  id/access/refresh/account_id) → restore needs NO re-login
- Backups `config.toml.backup-20260812` / `.pre-opencodex-removal-20260812.bak` were ALSO
  already injected (port 10100) — **never assume a `.bak` is pristine**; hijack predates
  the backup
- Proxy was NOT running (10100/10101 no listener) → desktop App requests to
  `127.0.0.1:10101` all failed → App "cannot use"

Diagnosis markers: `ocx doctor` / `ocx status` show the hijack; grep the injection
markers in `~/.codex/config.toml`; `~/.codex/auth.json` still has `auth_mode: chatgpt`
+ 4 token keys (native login survives → restore needs NO re-login).

## Diagnosis route (validated 2026-08-15)

1. `ocx status` → proxy health, port (10100), Config path, default provider, autostart, shim/service state, restart safety.
2. `ocx doctor` → CODEX_HOME / OPENCODEX_HOME paths, "Codex app home targeting", runtime selection, proxy env presence.
3. `ocx system status` / `ocx codex-shim status` → service/shim installed? (both absent on this host).
4. Read `~/.codex/config.toml` for `Auto-injected by opencodex` + `openai_base_url` + `model_catalog_json`.
5. Read `~/.opencodex/config.json` (providers disabled flags, defaultProvider, codexAutoStart, port).
6. Check `~/.codex/auth.json` auth_mode (chatgpt = native login intact) — never print token VALUES.
7. `netstat -ano | grep :1010[01]` — empty = proxy down = the "unusable" trigger.
8. Env-layer check: user/machine `CODEX_HOME`/`OPENCODEX_HOME`/`OPENAI_BASE_URL`/`OPENAI_API_KEY` — all unset here (no env binding; hijack is config-file-only).

## ocx CLI surface (restore-relevant)

- `ocx restore` — restore native Codex config WITHOUT stopping the proxy; `ocx restore back` re-points codex at the running proxy (undo).
- `ocx uninstall` / `ocx remove` — remove service/shim/config and restore native Codex (legacy/shared dirs left in place).
- `ocx stop` — stop proxy AND restore native Codex ("plain codex works again").
- `ocx start [--port N]` — start proxy; AUTO-SYNCS models into codex config (= RE-INJECTS).
- `ocx ensure` / `ocx sync` / `ocx sync-cache` — other re-injection paths; `ocx system settings` needs the proxy running.
- `ocx codex-shim install|status|uninstall` — auto-start-proxy-on-codex-launch shim (not installed here).

## Minimal restore (方案A, HITL-approved)

1. Backup: `~/.codex/restore-backup-<ts>/` — copy config.toml, models_cache.json,
   opencodex.config.toml, `~/.opencodex/config.json`.
2. `~/.codex/config.toml`: strip the 3 injection lines (`model_catalog_json` /
   `# Auto-injected by opencodex` / `openai_base_url`). Keep `model = "gpt-5.6-sol"`,
   `model_reasoning_effort`, `service_tier`. **CRLF trap:** naive Python
   `io.open(..., newline='\r\n')` + `'\r\n'.join()` DOUBLE-encodes to `\r\r\n` — read
   with `newline=''`, normalize, write CRLF explicitly, assert no `\r\r` and no lone `\n`.
3. `~/.opencodex/config.json`: `codexAutoStart: false` + `codexShimAutoRestore: false`
   (prevents re-injection on next `ocx start`).
4. `~/.codex/models_cache.json`: reset to
   `{"fetched_at":"2000-01-01T00:00:00Z","client_version":"0.0.0","models":[]}`.
   **`fetched_at: null` is NOT a valid RFC3339** → codex logs
   `failed to load models cache: invalid type: null` (non-fatal fallback, but noisy;
   canary 2 re-populated it with genuine OpenAI slugs: gpt-5.6-sol, gpt-5.5, gpt-5.4,
   codex-auto-review…).
5. Canary with the HUMAN runtime
   (`%LOCALAPPDATA%\OpenAI\Codex\bin\<hash>\codex.exe`, 0.148.0-alpha.9):
   `exec --skip-git-repo-check --ephemeral --json "Reply with exactly: NATIVE_OPENAI_OK"`.
   Success = `cached_input_tokens > 0` in NDJSON (hits real OpenAI backend).

## HGK-lane isolation (never touch the governed lane)

The HGK lane is a SEPARATE home: `%LOCALAPPDATA%\HG-KSEOS\codex-hermes` (CODEX_HOME) +
`opencodex-hermes` (OPENCODEX_HOME, port 10101) + pinned runtime
`codex-0.147.0-alpha.6.5\codex.exe`. Restore MUST NOT run `ocx restore/uninstall`
against it. Zero-touch proof = mtime of lane config files < task start + config still
`deepseek-v4-flash` + `openai_base_url 127.0.0.1:10101` + `codex --version` matches.

## Route re-verification (K6 recheck — the daemon-stop trap)

The launcher `scripts/start-hgk-hermes.ps1 -Action Probe` STOPS the opencodex daemon
in its `finally` block (`if ($proxy -and -not $proxy.HasExited) { Stop-Process ... }`).
So after a Probe run the lane is dead (healthz 000) even though the probe itself
succeeded. A later "is the route still working?" recheck must:

1. Start the daemon resident: `powershell -NoProfile -ExecutionPolicy Bypass -File
   scripts\start-hgk-hermes.ps1 -Action StartOpenCodex` in background; poll
   `curl http://127.0.0.1:10101/healthz` until 200 (body `{"status":"ok",
   "service":"opencodex","version":"2.11.0"}`).
2. Run the canonical canary with **splatting**, NOT Start-Process:
   `& $codexExe @codexArgs *> log` with
   `--model deepseek-v4-flash --sandbox read-only -c approval_policy=never --cd $root
   exec --skip-git-repo-check --ephemeral --json "ReplyExactly:<NONCE>"`.
   (Note: `-c approval_policy=never` replaces the removed `--ask-for-approval never`.)
3. **`ERR_CODEX_ROUTE_EXIT_` from the launcher's Probe action is a FALSE alarm** — the
   launcher reads `$codexProcess.ExitCode` from a Start-Process with redirection, which
   is always null (known PS 5.1 pitfall). When the codex log shows the nonce +
   `turn.completed` + usage, the route SUCCEEDED. Recheck via splatting gives real exit=0.
4. Provider receipt: tail `%LOCALAPPDATA%\HG-KSEOS\opencodex-hermes\usage.jsonl` →
   `provider: opencode-go`, `model: deepseek-v4-flash`, `status: 200`, requestId.
5. Benign warning: `Model metadata for deepseek-v4-flash not found. Defaulting to
   fallback metadata` — the catalog slug is namespaced `opencode-go/deepseek-v4-flash`
   while `--model deepseek-v4-flash` is un-namespaced; metadata lookup misses but
   routing works. NOT a defect. (Mirrored in the `codex` skill's Pitfalls section.)

## daemon 常駐 vs on-demand（FAR 治理判定 2026-08-15）

- 上游藍圖判定：**「需要時啟動」是正常設計，非缺陷**。證據鏈：
  - 知識庫《HG-KSEOS_多智能體協作系統_本地部屬藍圖_r2.md》§5.2（ChatGPT Desktop 三泳道：GPT Work 規劃 / Codex Local 執行 / Human 批准）、§8.2 `standalone_daemon: forbidden`、L1488（P0 manual startup；Task Scheduler only after G4 durability + service account + HITL）、§30（Codex CLI→OpenCodex→OpenCode Go→DeepSeek V4 Flash 是已完整驗收路線，勿換）。
  - 《HG-KSEOS使用說明文檔.md》L168-171：啟動序列 = `-Action StartOpenCodex`（啟動 transport）→ `-Action Hermes`（healthz gate，fail closed 不 fallback OpenAI）。
  - 8/12 驗收 `HGK_CODEX_PROVIDER_LANE_ISOLATION_RAW.json` restart_persistence：`post_probe_listener_count: 0`（Probe 測試後 proxy 停止 = 設計）；`config/hermes-codex-lane.json` `scope: launcher-process-tree-only`。
- 「daemon 常駐進開機流程」= 偏離藍圖保守原則（需 G4 + HITL review）→ 不建議；若用戶仍要 launcher auto-ensure（Hermes action 在 healthz 失敗時自動重啟），屬產品碼變更需另立 WO + Gate 2。

## Evidence shape

- Construction receipt JSON (pre/post sha256 of every touched file) → EVD.
- AO_PREDICATE_CORRECTION record when a challenge lane fails on letter-of-spec while
  intent is met (e.g. models_cache repopulated with 8 genuine OpenAI models instead of
  an empty array = STRONGER proof of native restore).
- Single evidence MD, fully-embedded raw (config heads, NDJSON lines, usage receipts,
  swarm CHECK lines), mirrored byte-identical to HGK|SQS|Fabric `evidence\review\` +
  team `var\a3\` primary; EVDs registered in SharedSpine; WO VERIFIED.
- User UI confirmation (HumanGate) closed the round as a separate
  USER_CONFIRMATION.md bound to the WO.
