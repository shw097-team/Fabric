# Desktop-effect-plane authorization gate (fail-closed)

The desktop-effect plane is guarded by two hooks that live in THIS skill's `references/`:
`fda_guard_hook.py` (pre-tool-call, fail-closed) and `fda_guard_mint.py` (pre-LLM-call, never
blocks). Learn this before touching anything whose command text mentions the plane, because the
gate blocks far more than you expect and the natural reaction (rephrase the command) is forbidden.

## Authorization conditions

An operation is authorized when ONE of these holds:

1. The user's own message explicitly authorized the plane (the mint hook then writes a token).
2. A registered ACTIVE route id is supplied (`--route-id <ID>`; registry
   `references/FDA_ROUTE_REGISTRY.json`).
3. The task requires it → **pause, ask the user, obtain explicit authorization, then proceed**.

If none holds: STOP. Do not run any plane script.

## The token, and the path you must actually check

- Canonical token file: `C:\Users\user\AppData\Local\hermes\var\fda-auth\<session_id>.json`
  (under the Hermes data dir).
- The desktop-automation skill still names an older `~/.hermes/var/...` location. If you check that
  path you will wrongly conclude "no token was ever minted" while a valid token sits at the
  canonical path. Check the canonical path first.
- Shape: `{session_id, turn_id, minted_at_utc, ttl_seconds: 3600, expires_at_utc, matched_text}`.
  The hook's decision is: the token file for THIS session exists, `session_id` matches, and
  `expires_at_utc` is in the future. Nothing else — an authorization that was valid on a previous
  turn does not help once the TTL lapses.

## What re-mints the token

The mint hook fires only when a **user message** contains BOTH:

- an **intent verb** — 用 / 使用 / 操作 / 操控 / 執行 / 開啟 / 啟用 / 允許 / 授權 / 可以 / 批准 /
  approve / use / run / operate / authorize / allow; AND
- a **target token** — the plane's name, `fda_run`, `fda_preflight`, `screen_state_check`,
  `XQLite`, `PAPER`, the product name, or the radar/strategy term.

Consequences to plan around:

- A blanket "全部授權執行，不必再問" contains the verb but NO target token → **no re-mint**. The gate
  keeps blocking and every retry fails the same way.
- A clarify-menu answer that contains both may not arrive as a `user_message` → **no re-mint**.
- The fix is always the same and costs one user turn: ask for a message containing a verb AND the
  plane name (e.g. "授權 FDA" / "authorize FDA"). Frame it as a token refresh, not as re-asking
  for a decision the user already made.

## The gate matches substrings, not intent

The hook scans the tool-call arguments for marker strings: the plane's short name, `XQ`, `var/fda`,
`SysJust`, `fabric-desktop-automation`, `fda_run`, `fda_preflight`, `screen_state_check`,
`XQLite`, `cua-driver`. So while the token is absent or expired:

- a **read-only** `ls`/`find` that merely names a plane path is blocked;
- `write_file` whose **content** merely *describes* the plane is blocked — you cannot even author
  the governance documentation, though writing a doc is not a plane operation.

Mitigations that ARE legitimate: name staging and mirror directories neutrally so later `git`
commands on the staging tree do not trip the gate, and write the plane-specific sections once the
token is live. Mitigations that are NOT legitimate: building a command that avoids the literal
marker to slip past the gate. That is lowering a security control — refuse it and report instead,
even when the underlying intent is benign.

## When the gate blocks you

Report: (a) it is a fail-closed mechanical gate, not a policy refusal; (b) the exact one-line user
message that refreshes the token; (c) what is already done versus what is pending. Do not silently
work around it, and do not claim the gated work is complete.
