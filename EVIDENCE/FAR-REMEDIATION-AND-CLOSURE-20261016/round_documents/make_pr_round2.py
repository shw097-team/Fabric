"""Open the pull request for THIS round's publication branch.

Reads the token from the key file; NEVER prints it. Prints only status + PR identity.
Fail-closed: exits non-zero and prints the API message if the PR cannot be created.
Opens a PR — it does NOT merge. Merging to main is the owner's decision, not this round's.
"""
import json
import pathlib
import re
import sys
import urllib.error
import urllib.request

KEY = pathlib.Path('C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt')
REPO = 'shw097-team/Fabric'
HEAD = 'pub/far-remediation-and-closure-20261016'
BASE = 'main'

tok = re.search(r'github_pat_[A-Za-z0-9_]+', KEY.read_text(encoding='utf-8', errors='replace'))
if not tok:
    print('NO_TOKEN_FOUND_IN_KEY_FILE')
    sys.exit(2)

BODY = """Round `FAR-REMEDIATION-AND-CLOSURE-20261016` — the FAR study of this session's residuals, the
ruling it produced, and the execution of that ruling.

Owner order: under the current Fabric governance contract, HG-KSEOS is the sole control plane and canonical
Hermes is its governed Runtime/Orchestration plane; run FAR over every residual / gap / owner-decision /
closure / publication item, rule the best low-friction option, execute it, then close and publish.

## Headline: the canonical gate that was RED is now green

F1 — `routes[].PLAN` declaring `opencode-go/glm-5.3-flash` while the pool, the registry SoD block, the
conformance test and the owner order all said `openai-codex/gpt-6.1-sol` — is **closed**. The row was
rebound under the owner order of 2026-10-16, its stated premise (a 429 on the OpenAI OAuth arm) having been
measured false the day before. Registry `epoch` 20 → 21.

**Regression isolation, run on both states rather than asserted:** the pre-change config pair was restored
from its backups and the whole tree was run, then the post-change pair was restored and the same command
re-run. Pre: 527 tests, 8 failures + 2 errors, including the conformance case. Post: 527 tests, 7 failures +
2 errors. **Diff: exactly one name removed, none added.** The remaining failures are unrelated by module
ownership and unchanged by this round.

## Also delivered

- **Promotion of the verified candidate** — four product files, each byte-identical to the frozen
  candidate's digest, with the orchestrator re-running the oracle itself (6 + 16 tests OK).
- **SoD reclassification** — `SOD006-C2` moved from "open, awaiting a decision" to "ordered and in force",
  with the surviving independence (process / lane / evidence-path / no-self-acceptance) written down beside it.
- **R7, a defect class named and detected** — the site file simultaneously declared VERIFY_SECURITY's
  default arm as `gpt-6.1-sol` (lane chain) and `glm-5.3-flash` (three prose fields) **with `check_drift`
  at zero fatal findings**. A detector was written and demonstrated on both states: 3 contradictions
  before, 0 after.
- **E11 reclassified by measurement** — "5 E11 cases" is 4 E11 guard cases plus 1 C2 case; on this host the
  unmodified module passes 136/136; and two **genuine product defects** were found: uncaught `OSError` on
  relay/usage metadata probes at `scripts/hgk-lane-dispatch.py:862-873` and `:1134-1135`, where the
  promised refusal receipt is replaced by a crash.

## Not delivered — stated plainly

**The `--turn-shape edit_only` flag is NOT implemented.** Two bounded-writer attempts wedged, with two
*different* diagnosed causes: the first, this round's own ambiguous output path under the sandbox cwd (the
writer spent its window probing directory names for a writable location); the second, the **turn scope** —
four edits plus a new test file on a 2275-line file in one turn. Both terminations are on measurement, not
timeout, and both carry a `TERMINATION.json`.

## Self-reported defects (this round's own)

Four, in `FINDINGS_SELF_CORRECTIONS.md`: an incomplete first application that the existing lane-guard suite
caught; an applied-then-rolled-back attempt whose spine rows survived the rollback; a promotion that ran
before its WorkOrder existed; and a detector whose first parser returned a false negative on the very line
it exists to catch — a claim made from that run was withdrawn.

## Claim ceiling

**CANDIDATE_ONLY.** Every measurement was taken on this host by this session. Applying a ruling is not
accepting it. `hgk_canonical_acceptance: NOT_PERFORMED`. The checker verdict inside the packet is advisory.
This PR is not merged by the round that opened it.

## Where to look

`EVIDENCE/FAR-REMEDIATION-AND-CLOSURE-20261016/README.md` indexes everything; `FAR_RULING.md` is the
ruling; `ROUND_CLOSURE.json` is the machine-readable closure; `implementation/` carries before/after files
**and** unified diffs; `RETROSPECTIVE.md` + `SELF_EVOLUTION.md` are the priced proposals for the next
upgrade (the two highest-value ones are a cross-field declaration sweep and a coupled-pin sweep, both in
`lane_policy`).
"""

req = urllib.request.Request(
    'https://api.github.com/repos/%s/pulls' % REPO,
    data=json.dumps({'title': 'FAR-REMEDIATION-AND-CLOSURE-20261016: F1 closed, candidate promoted, '
                              'R7 class named (candidate only)',
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
