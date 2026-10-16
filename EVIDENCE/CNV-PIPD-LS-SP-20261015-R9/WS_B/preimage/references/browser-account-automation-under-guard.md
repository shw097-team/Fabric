# Browser/account automation under the desktop-effect guard

Procedures for doing real GitHub-account work with a browser while `fda_guard_hook.py` is armed, and the
findings that only appeared by executing rather than reading.

## 1. Establish the authorisation condition, do not assume it

Two independent conditions authorise a gated call: (1) a live token for THIS session at
`C:\Users\user\AppData\Local\hermes\var\fda-auth\<session_id>.json`, or (2) a payload naming an ACTIVE
route id. A live token is minted only from a **user message** containing both an intent verb and the
plane's name (`授權 FDA` is enough); a blanket "全部授權" contains no target token and re-mints nothing.

Cheap test of condition 1: run a `terminal` call whose text contains `var/fda`. If it returns output, the
token is live; if it is blocked, it is not. Do not infer the answer from the last turn - the TTL is 1 hour.

**Check the route registry too.** Read `FDA_ROUTE_REGISTRY.json` before claiming a route authorises your
work. If every ACTIVE route is scoped to another application (as all four are: XQ / guard verification),
then **no route covers your task** and you are running on a per-turn human grant. Say so in the evidence,
because it means the work is not repeatable without a new route plus a WorkOrder admitted to the spine
(`mutation_authority: ADMITTED_HGK_WORKORDER_ONLY`). **Do not create that route yourself** - self-issuing
an automation authority is precisely what `MAY NOT SELF-PROMOTE` forbids. Propose it.

## 2. The browser tool may simply not start - fix the runtime path, do not give up on it

Symptom: `browser_exec` exits 103 with
`No Python at '...\AppData\Local\hermes\hermes-agent\.hermes-runtime\python\...\python.exe'`.
Two Hermes trees are live on this host; the interpreter exists only under the MSIX tree
(`...\Packages\OpenAI.Codex_*\LocalCache\Local\hermes\hermes-agent\.hermes-runtime\...`).

Fix: a reversible directory junction (not a copy), which alters no security control:

```bash
MSYS2_ARG_CONV_EXCL='*' cmd.exe /c mklink /J "<LOCALAPPDATA>\hermes\hermes-agent\.hermes-runtime" \
  "<MSIX>\hermes\hermes-agent\.hermes-runtime"
```

`MSYS2_ARG_CONV_EXCL='*'` is required - MSYS rewrites `mklink` switches otherwise. **Disclose this as a
host-side mutation outside the governance framework**; it is a path alias, not a gate bypass, so it is
allowed, but it is still a change to the machine.

## 3. Sign-in without ever seeing a credential

The agent's browser starts with no session, and the vault may be empty. Never type a password and never
ask for one in chat. The sanctioned path:

1. `browser_vault_save_login(label=...)` on the login page. The owner types the secret into a **masked UI
   prompt**; you receive only a handle and the **identifier**.
2. `fill_input('#login_field', '<identifier>')` - the identifier is not a secret; you may type it.
3. Submit. The password is already filled server-side.
4. On the 2FA page, `browser_vault_enter_code(handle=...)`; the code is entered by the owner and never
   enters the conversation.
5. Re-logins afterwards use `browser_vault_fill(handle=...)` (identifier typed by you, password filled) +
   `browser_vault_enter_code`.

Expect to sign in more than once: GitHub logs this browser out mid-flow. Do not build long click-chains
that assume one session survives.

## 4. GitHub App setup: the App must be owned by the RESOURCE OWNER's organisation

A personal-account App **cannot** reach an organisation's repositories when the org's third-party access
policy is **"Access restricted"** (org settings -> Third-party Access). The policy page states the rule:
*Applications owned by the organisation always have access.* Evidence that a personal App will fail:
its install page offers only the personal account; the org-targeted install URL returns *Page not found*.

Correct entry point: `https://github.com/organizations/<org>/settings/apps/new`. Only then does the
install flow offer "Install on your organization ...".

**Webhook defaults to ACTIVE - switch it off before creating** if the App is only a push credential.

**Repository permissions are not a `<select>`.** Each permission row is a custom menu: the real state
lives in a hidden `integration[default_permissions][<name>]` input (starts `none`), and the visible
choices are `button[role=menuitemradio]` with labels `No access` / `Read-only` / `Read and write`.
Click the right one, then assert the hidden input's value - not the UI's colour.

**The repo picker is a `<details>`** whose list loads lazily. Force `details.open = true` and wait; the
authoritative proof of selection is a hidden `repository_ids[]` field appearing in the form. Clicking the
item and seeing no visual change means nothing; the hidden field is the evidence.

Key generation: the **Credentials -> Key pairs -> `New key`** button downloads the `.pem`. Find it by
`find <Downloads> -iname '*.pem' -newermt '-15 minutes'`, move it **outside every repo**, `chmod 600`,
confirm it parses (`openssl rsa -in <key> -noout -check` -> `RSA key ok`), and delete the download copy.
A private key is download-once; losing it means deleting and regenerating the key pair.

## 5. A declared-but-never-executed path is a claim, not code

A credential broker shipped an App-token branch that had been called **implemented** across four rounds,
on the strength of an offline verifier reporting `PASS_OFFLINE_T5_UNPROVEN` and a selftest whose network
test was never run with a real App. The first real execution raised `UnboundLocalError` on `urllib`:
an `import urllib.error` **inside** the function body made `urllib` a local name, so an earlier line
referencing `urllib.request` read an unbound local. One line, invisible to every offline check.

Rule: an offline "unproven" verdict is not coverage of the unproven branch. When a documented source
(e.g. "App first, PAT as fallback") names a preferred path, **exercise the preferred path early** - the
first execution of it is where the real defects are. And when you fix such a file, **recompute its pinned
hash in the same change**; a stale pin is worse than no pin.

## 6. Readback must not use the thing it attests

After proving the broker writes, verify with a **plain** `git ls-remote` that does not go through the
broker - otherwise the broker certifies itself. Same principle as `ls-remote` after any push: `exit 0` on
a push is not evidence the remote advanced.

A working capability that nothing calls is **not** a delivered capability. If `config/` references the
tool zero times, the tool is installed, not activated - say that, and let activation be its own admitted
change.

## 7. Stopping

When the remainder splits into "needs the owner's interactive step" and "needs its own admission", that
is a reason to stop THOSE items - **not** to stop the line. Re-read your own open list first: a proof
sitting in it that needs nobody but was skipped is a self-inflicted gap, and the mid-session correction
costs less than shipping the claim without it.
