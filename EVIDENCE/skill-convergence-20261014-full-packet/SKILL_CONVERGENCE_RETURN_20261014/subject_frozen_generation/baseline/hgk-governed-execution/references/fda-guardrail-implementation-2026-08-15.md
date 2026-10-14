# FDA Guardrail implementation knowledge (WO-HGK-FDA-GUARD-IMPL-001, 2026-08-15)

Verified engineering facts from building the FDA auto-invoke guardrail (方案 D: pre_llm_call
mint + pre_tool_call guard + preflight auth + route registry + approvals.deny). Reuse these
when extending the guardrail, writing Hermes shell hooks, or repairing config.

## 1. Hermes shell-hook wire format (verified against agent/shell_hooks.py)

- `_serialize_payload` (L673-689) builds the stdin JSON the hook script receives:
  `{hook_event_name, tool_name, tool_input, session_id, cwd, extra}`.
- **`tool_input`** = the `args` kwarg **renamed** (only when args is a dict). The hook script
  must NOT read `args` — it is absent from the wire payload.
- **`extra`** = every kwarg not in `_TOP_LEVEL_PAYLOAD_KEYS = {tool_name, args, session_id,
  parent_session_id}` (L492). For `pre_llm_call`, `user_message`, `conversation_history`,
  and `turn_id` all arrive inside `extra`. For `pre_tool_call`, `task_id`/`tool_call_id`/
  `turn_id`/`api_request_id` arrive in `extra`.
- The module docstring wire-protocol example (which shows `tool_input`) is CORRECT. The
  synthetic payloads in `hermes_cli/hooks.py` (`_DEFAULT_PAYLOADS`) use `args`, but
  `_serialize_payload` renames before the script sees it — a fresh-context challenge lane
  that concluded "actual key is `args`, docstring outdated" was WRONG. Verify against
  `_serialize_payload`, never the synthetic payloads.
- Normalize at the top of every hook script's main():

```python
extra = data.get("extra")
if isinstance(extra, dict):
    for k, v in extra.items():
        data.setdefault(k, v)
if data.get("tool_input") is not None and data.get("args") is None:
    data["args"] = data["tool_input"]
```

- Real-pipeline testing without an agent run: `hermes hooks test <event> --payload-file
  <json>` (payload merged into the synthetic payload; block output shown as Hermes wire
  shape). E2E cold-start canary: `hermes chat -q "<prompt>"` spawns a fresh process that
  re-reads config and registers hooks — the canary session transcript lives in
  `C:\Users\user\AppData\Local\hermes\state.db` (sessions/messages tables).
- Hooks registered at process start only: config changes do NOT affect the currently
  running session; new sessions/processes pick them up. Verify registration with
  `hermes hooks doctor` (checks script, allowlist, fires once).
- `fail_closed: true` is per-entry and honored only for `pre_tool_call` (default is
  fail-open). Allowlist file: `~/.hermes/shell-hooks-allowlist.json` = `{"approvals":
  [{"event": ..., "command": ...}]}`; seed it + `hooks_auto_accept: true` or non-TTY
  gateway/cron registration silently skips. Hook commands must use FORWARD slashes —
  `shlex.split` with posix=True mangles `C:\...` backslashes.

## 2. `hermes config set` list-value trap (approvals.deny / hooks)

- `hermes config set approvals.deny '["a","b"]'` stores the JSON array as a SINGLE-QUOTED
  YAML STRING, not a list. `_match_user_deny_rule` iterates the string → each CHARACTER
  becomes a glob → the `*` char blocks EVERY terminal command ("matches the user-defined
  deny rule '*'"), and user-deny has NO circuit breaker (denial_breaker_threshold applies
  only to smart-approval verdicts). The terminal is hard-locked, including the fix command.
- `patch`/`write_file` refuse `config.yaml` ("Agent cannot modify security-sensitive
  configuration"); execute_code that edits config.yaml raises an approval prompt which can
  time out silently. Repair path: get explicit user authorization → execute_code python
  edit writing a REAL YAML list (`deny:\n  - "pattern"`) → verify with yaml.safe_load that
  the value is a list, then `hermes config get approvals` + a harmless command.
- Same trap hits `hooks.<event>` values: stored as strings → `hermes hooks list` reports
  "No shell hooks configured". Fix: rewrite the hooks block as a proper YAML list of dicts.
- Guardrail C-layer pattern selection: do NOT add `*python*var/fda/*` — it also matches the
  LEGITIMATE `python .../var/fda/fda_run.py` registered-route execution (condition 2) and
  blocks it unconditionally. Deny only always-wrong vectors: `*quarantined_violations*`,
  `*cua-driver*foreground*`, `*cua-driver*bring_to_front*`. Conditional gating (token/route)
  belongs to the pre_tool_call hook (it can express conditions; deny cannot).

## 3. Output-redaction ghost: verify with hashes, not displayed output

- Hermes secret redaction masks secret-looking strings in TOOL OUTPUT display as `***`.
  A correct file line `no_authorization:{authz['reason']}` DISPLAYS as
  `no_authorization:***` — indistinguishable from a corrupted f-string literal.
- Consequence chain observed: patch attempts "succeeded" but were silent no-ops on an
  already-correct file; a byte-level "repair" reported "0 replacements" (search pattern
  genuinely absent because content was fine); grep for literal `***` found nothing; a Codex
  spawn that claimed "defect already absent" was doubted but was actually RIGHT.
- Rule: when displayed content looks corrupted, verify against RAW BYTES first — hex-dump
  the bytes at the position (`[hex(b) for b in ln[i:i+8]]`), compare sha256 of
  expected-vs-actual strings. Never "repair" or re-patch based on redacted display.

## 4. Codex + Chinese literals in Python: \uXXXX escape technique

- CODEX_MOJIBAKE_DEFECT: the sealed lane corrupts raw Chinese UTF-8 on write. Workaround
  that keeps Codex as the writer: precompute `\uXXXX` escapes for EVERY non-ASCII literal
  (regex alternation members, block messages) and require the prompt to copy them verbatim.
  Source stays ASCII-only; runtime strings decode correctly.
- Verify after any such write: `grep -c $'\uFFFD'` == 0, CJK char count in source == 0,
  py_compile, then functional tests feeding real inputs (regex must match Chinese text).
- Codex self-reports are unreliable (spawn3 claimed "defect already absent" without making
  the change). Always fresh-readback + hash verify; a tiny 1-line fix is faster as a direct
  patch with compensating controls than a second Codex round.

## 5. Kanban: children of a running parent

- Cards created with `--parent` of a claimed/running card stay `todo` and are promoted only
  after the parent completes — `kanban complete <child>` fails "unknown id or terminal
  state" mid-run. Complete the parent first (with the full result summary), then the
  children promote to `ready` and complete cleanly. For sub-task granularity that must be
  completed independently, create cards WITHOUT the parent link.
