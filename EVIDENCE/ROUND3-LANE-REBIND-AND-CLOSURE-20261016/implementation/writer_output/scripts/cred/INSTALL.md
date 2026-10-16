# scripts/cred — GitHub credential broker (STANDING, NON-ACTIVATED)

This directory is the durable home for the credential broker designed in round
`R9-20261011-s4-gap-closure` (`FAR-PIPD-R9-CREDROT-005.md`). It was moved here
out of ephemeral agent scratch (`…/cache/scratch/r9/cred/`), which is pruned
when idle and therefore cannot serve an unattended run.

**It is installed as a standing, NON-ACTIVATED artefact.** Nothing in
`config/` (lane-routing registry, model-lane assignment, dispatcher, Hermes
binding) references this path. Installing the files does not wire the broker
into any lane; activation is a separate, later, separately-admitted change.

## Contents

| File | Role |
|---|---|
| `cred_preflight.py` | Fail-closed preflight. `--metadata-only` never reads the secret (existence + byte length only). Exit 2 on any required FAIL. |
| `cred_broker.py` | Mints a GitHub App installation token (1 h, RS256 JWT signed via `openssl`; no Python crypto dep) or falls back to a fine-grained PAT; runs git with the secret confined to the child-process environment. |
| `selftest.py` | 5 dummy-credential tests (never touches the real value). T5 needs network. |
| `verify_offline.py` | Network-free verification (T1–T4) for a `network_default: DENY` host; T5 reported INCONCLUSIVE, never PASS. |
| `INSTALL_MANIFEST.json` | Pinned sha256 + target paths + activation flag. |

## Governance route (why this is a control-plane round, not R10's work)

HG-KSEOS is the sole system governance / normative control plane (AGENTS.md).
Editing HG-KSEOS tooling is a **control-plane change**. `FAR-PIPD-R8-DISPATCH-004`
§4 fixed the precedent: such a change "edits HG-KSEOS control-plane tooling …
candidate-only by contract, needs its own admission, and must not ride along
inside a PIPD round." A product round (PIPD R10) therefore records the route and
supplies this candidate; it does not install.

HG-KSEOS **does** have its own lifecycle projects in the shared spine at
`var/shared-spine/hg-kseos.db` (`projects` table: `HGK-P0`, `HGK-CHU-20261009`,
`HGK-PRJ-CLI`, `FAR-LANE-*`, …). The minimal admitted change is one typed
`ProjectLifecycleController.admit_requirement(...)` call adding
`REQ-HGK-CREDBROKER-001` to a control-plane project already in an admissible
state (EXECUTING / PLAN_READY / WORKORDERS_ADMITTED), e.g. `HGK-CHU-20261009`.
The candidate admission script is `admission/hgk_cred_admission.py`.

## Verification (no secret value is read; run from the repo root)

```bash
# 1. install integrity — byte identity against the pinned hashes
python -c "import json,hashlib,pathlib as p;m=json.load(open('scripts/cred/INSTALL_MANIFEST.json'));[print(f['target'], hashlib.sha256((p.Path('.')/f['target']).read_bytes()).hexdigest()==f['sha256']) for f in m['files']]"

# 2. offline security contract (no network, no secret read)
python scripts/cred/verify_offline.py            # -> PASS_OFFLINE_T5_UNPROVEN (exit 0)

# 3. full contract incl. the wire check (needs network; dummy creds only)
python scripts/cred/selftest.py                  # -> 5/5 PASS (exit 0)
env HGK_CRED_FILE=/nonexistent \
  python scripts/cred/cred_preflight.py --metadata-only   # -> FAIL_CLOSED (exit 2)

# 4. NON-ACTIVATION proof — the installed path must appear in NO config file
git grep -n "scripts/cred" -- config/ scripts/ src/ | grep -v '^scripts/cred/' || echo "NON_ACTIVATED_OK"
```

## Security contract (binding — unchanged from R9)

* The secret lives only in the broker process's memory and the git child's
  environment; it never reaches argv, stdout, a log, an evidence file, a prompt,
  a remote URL, or `.git/config`.
* The credential travels as a **URL-scoped** `http.https://github.com/.extraheader`
  set via `GIT_CONFIG_KEY_0`/`GIT_CONFIG_VALUE_0`.
* `GIT_TERMINAL_PROMPT=0`, `GIT_CONFIG_NOSYSTEM=1`, `credential.helper=` reset.
* No command-line `-c <extraheader key>` is ever passed (it would clear the header
  — the prior round's silent unauthenticated-push bug).
* The repository contains **no secret**: the broker reads the credential from an
  external file (`HGK_CRED_FILE`) or mints from an external App key (`HGK_APP_KEY`).

## Configuration (environment only — never argv)

`HGK_CRED_FILE`, `HGK_APP_ID`, `HGK_APP_KEY`, `HGK_APP_INSTALLATION_ID`,
`HGK_CRED_EXPIRY_FILE`, `HGK_REPO_SLUG`.

## Residual human steps

See §4 of `FAR-PIPD-R9-CREDROT-005.md` (App creation, private-key download,
installation, PAT rotation) and §"Residual HUMAN steps" of
`FAR-PIPD-R10-CREDITOOLS-002.md`. None are automatable; GitHub exposes no API
for App registration, private-key download, installation consent, or PAT
rotation/expiry-read.
