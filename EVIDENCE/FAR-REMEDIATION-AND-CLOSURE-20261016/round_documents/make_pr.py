"""Open a pull request for the round's publication branch, so the external acceptance officer has a
review surface. Reads the token from the key file; NEVER prints it. Prints only status + PR identity.

Fail-closed: exits non-zero and prints the API message if the PR cannot be created.
"""
import json
import pathlib
import re
import sys
import urllib.error
import urllib.request

KEY = pathlib.Path('C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt')
REPO = 'shw097-team/Fabric'
HEAD = 'pub/lane-reliability-closure-20261016'
BASE = 'main'

tok = re.search(r'github_pat_[A-Za-z0-9_]+', KEY.read_text(encoding='utf-8', errors='replace'))
if not tok:
    print('NO_TOKEN_FOUND_IN_KEY_FILE')
    sys.exit(2)

BODY = """Round `LANE-RELIABILITY-CLOSURE-20261016` — HG-KSEOS three-lane usability and reliability.

Owner order: under the current Fabric governance contract, HG-KSEOS is the sole control plane and canonical
Hermes is its governed Runtime/Orchestration plane; the three lanes **and their model selection** must be
usable and reliable.

## Proven by measurement, not by configuration

| lane | arm | how it was proven |
|---|---|---|
| PLAN & Orchestrator (in Hermes) | `gpt-6.1-sol` / `openai-codex` (OAuth), medium | reply probe + tool-executing probe + the governed profile's own `state.db::sessions` serving rows |
| EXECUTE (CODEX CLI) | `opencode-go/deepseek-v4.1-flash` | `required_arm == served_arm`, `usage_receipt_ok`, `used_rank 1`, nonce present, exit 0 |
| VERIFY/SECURITY (CODEX CLI) | `openai-codex/gpt-6.1-sol`, medium | same, plus a CLEAN subject-mutation verdict over the frozen subject |

## What is in the packet

`EVIDENCE/LANE-RELIABILITY-CLOSURE-20261016/` (71 files, digests in `PACKET_MANIFEST.json`):

- `README.md`, `ROUND_CLOSURE.json` — the round, the detection list, the residuals, the claim ceiling
- `implementation/` — the changed product files, their baselines, three unified diffs
- `lanes/` — every lane attempt verbatim: `dispatch.json`, `exit.json`, the raw codex event stream,
  the extracted `CHECKER_VERDICT.json`, and the `TERMINATION.json` for the attempt that was stopped
- `SELFCHECK_REPORT.json` — the detection list re-derived orchestrator-side, with an interpretation field
  per item; raw statuses are left exactly as measured
- `FINDINGS_*.md` — the PLAN route outlier (recorded, **not** repaired) and the defect in my own V1
  checker brief, published unedited
- `_handover` checkpoint, the OPENSPEC change, the KANBAN/SWARM graph, the admission and role mandate

## Claim ceiling

**CANDIDATE_ONLY.** Changes B (the missing effort axis) and C (the absent-session-id outage) live in the
candidate and were **not** promoted; no agent promoted its own work. Nothing here is accepted or merged.
`hgk_canonical_acceptance: NOT_PERFORMED`. Checker verdicts are **advisory**.

## What changed, and why it was worth changing

- **B** `scripts/runtime_role_binding_assert.py` — `grep -c effort` was **0**: a lane served at a
  different reasoning effort than its mandate declares was refused by *nothing*. Now gated, exit 7,
  four typed codes. The checker independently reproduced all six cases and noted the honest limit:
  these are **declaration** checks, not proof of the backend's actual effort.
- **C** `scripts/hgk-governed-runtime-controller.py` — a blank or absent session id mapped to exit 3,
  which refused **every** mutating call for an agent with no session id. Now answered
  `{"action":"allow","reason":"no-session-id-unattributable"}`. Before/after is visible in the packet:
  the same three fixtures return exit 3 on the canonical root and exit 0 on the candidate.
- **A** canonical `config/…` only — PLAN declaration coherence; registry `epoch` 19 → 20; stale
  `/codex_sha256` projection expectation corrected. Canonical drift now measures empty.

## Honest residuals (not smoothed — full list in `ROUND_CLOSURE.json`)

- **F1** `routes[].PLAN` is `opencode-go/glm-5.3-flash` while the pool, the registry SoD block, the
  conformance test and the owner mandate all say `openai-codex/gpt-6.1-sol`. Recorded, not repaired: a
  rebind is outside this round's authorisation. `test_registry_and_projection_shape` is therefore RED on
  the canonical tree.
- PLAN and VERIFY are the **same model**; model independence between them is absent (`SOD006-C2`
  OPEN_OWNER_ORDERED) — only process/lane/evidence-path independence remains.
- Two of three EXECUTE turns **wedged** before an edit-only turn succeeded in 74 s. The remedies and the
  measurement that justifies them are in the packet.

Recompute the manifest, re-run the named suite, and judge F1 yourself.
"""

req = urllib.request.Request(
    'https://api.github.com/repos/%s/pulls' % REPO,
    data=json.dumps({'title': 'LANE-RELIABILITY-CLOSURE-20261016: three-lane usability and reliability '
                              '(candidate only)',
                     'head': HEAD, 'base': BASE, 'body': BODY}).encode('utf-8'),
    headers={'Authorization': 'Bearer %s' % tok.group(0),
             'Accept': 'application/vnd.github+json',
             'X-GitHub-Api-Version': '2022-11-28',
             'User-Agent': 'hg-kseos-governed-runtime'},
    method='POST')
try:
    with urllib.request.urlopen(req, timeout=60) as r:
        doc = json.loads(r.read().decode('utf-8'))
    print(json.dumps({'http': r.status, 'number': doc.get('number'), 'state': doc.get('state'),
                      'html_url': doc.get('html_url'), 'head': (doc.get('head') or {}).get('ref'),
                      'base': (doc.get('base') or {}).get('ref')}, ensure_ascii=False, indent=1))
except urllib.error.HTTPError as e:
    payload = e.read().decode('utf-8', errors='replace')[:400]
    print(json.dumps({'http': e.code, 'error': payload}, ensure_ascii=False, indent=1))
    sys.exit(1)
