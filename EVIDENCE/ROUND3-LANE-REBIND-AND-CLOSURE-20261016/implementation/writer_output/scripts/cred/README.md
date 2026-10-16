# R9 credential broker — local tooling

Fail-closed credential handling for the PIPD-LS-SP **unattended write lane**.
Working files for `REQ-PIPD-R9-CREDROT-005` (design study:
`.hgk/rounds/R9-20261011-s4-gap-closure/far/FAR-PIPD-R9-CREDROT-005.md`).

## Files

| File | Role |
|---|---|
| `cred_preflight.py` | Fail-closed preflight. Verifies credential presence/syntax/validity at minute 0; `--metadata-only` never reads the secret (existence + byte length only). Exit 2 on any required FAIL. |
| `cred_broker.py` | Credential broker. Mints a GitHub App installation token (1 h, RS256 JWT signed via `openssl`, no Python deps) or falls back to the fine-grained PAT; runs git with the secret confined to the child-process environment. `preflight`, `dry-run`, `run -- <git args>`. |
| `selftest.py` | 5 dummy-credential tests (never touches the real value). |

## Security contract (binding)

* The secret lives only in this process's memory and the git child's environment.
* Nothing prints it. git output and free text are redacted of token-shaped strings.
* The credential travels as a **URL-scoped** `http.https://github.com/.extraheader`
  set through `GIT_CONFIG_KEY_0`/`GIT_CONFIG_VALUE_0` — never argv, stdout, a log,
  a remote URL, or `.git/config`.
* `GIT_TERMINAL_PROMPT=0` so a missing credential never hangs a run.
* No command-line `-c <extraheader key>` is ever passed — a CLI value would
  override and clear the header (the prior round's silent unauthenticated-push bug).

## Usage

```bash
python cred_preflight.py --metadata-only     # presence + byte length, no read
python cred_preflight.py                     # + syntax + GET /user probe
python cred_broker.py dry-run                # prove a credential WOULD be supplied
python cred_broker.py run -- push origin main
```

## Configuration (environment; never argv)

* `HGK_CRED_FILE` — path to the PAT file (default: the owner's API-KEY file).
* `HGK_APP_ID`, `HGK_APP_KEY`, `HGK_APP_INSTALLATION_ID` — GitHub App source
  (used in preference to the PAT when all three are set).
* `HGK_CRED_EXPIRY_FILE` — optional owner-recorded expiry date, since GitHub has
  **no API** to read a fine-grained PAT's own expiry.

## Verified (this round)

`selftest.py` → **5/5 PASS**: fail-closed on absent credential; metadata-only
reports size without reading; extraheader is URL-scoped and base64-wrapped with
the raw token absent from the value; redaction strips token-shaped text; the
extraheader is actually transmitted over the wire (dummy-token `ls-remote` differs
from anonymous) with no leak.

App JWT path verified separately: a 3-part RS256 JWT, `iss`=app_id, 600 s TTL,
signature `Verified OK` against the matching public key. The final installation
token exchange (`POST /app/installations/{id}/access_tokens`) is coded but not
exercised — it needs the owner's real App.
