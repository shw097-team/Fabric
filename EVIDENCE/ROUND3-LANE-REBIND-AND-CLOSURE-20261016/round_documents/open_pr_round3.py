"""Open the pull request for THIS round's publication branch (round 3) — fresh, round-3 body.

Reads the token from the key file; NEVER prints it. Prints only status + PR identity.
Fail-closed: exits non-zero and prints the API message if the PR cannot be created.
Opens a PR — it does NOT merge. Merging to main is the owner's decision, not this round's.
"""
import json
import pathlib
import re
import subprocess
import urllib.error
import urllib.request

R = pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS')
FAB = pathlib.Path('C:/Projects/Agent_Workspace/Fabric')
KEY = pathlib.Path('C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt')
REPO = 'shw097-team/Fabric'
BRANCH = 'pub/round3-lane-rebind-and-closure-20261016'
BASE = 'main'

BODY = """Round 3 of session `20261016_104922_d455e7`, under HG-KSEOS as the control plane. **Candidate only \
— this PR is not merged by the round that opened it.**

## What the owner order changed, and what that forced

The order re-points the three governed lanes: PLAN -> `opencode-go/glm-5.3-flash`; the EXECUTE bounded writer \
stays `opencode-go/deepseek-v4.1-flash`; the VERIFY/SECURITY checker becomes `opencode-go/deepseek-v4.1-flash` \
— **the same model the writer holds**. That inverts the separation-of-duties axis of the previous epoch: the \
pair that had to be distinct becomes same-model, and the pair carrying a recorded owner-ordered collision \
stops colliding.

So the rebind is one coupled change across five surfaces (the registry route row, arms and fallbacks, the \
assignment site's `lane_chains`, the dispatch-time pool the dispatcher actually reads, and the conformance \
fixture whose invariant IS the current owner order), plus the coupling (epoch, revision, the \
`source_of_routes` digest pin, every projection binding that names a moved value) and the SoD re-declaration.

## What this packet contains

* the rebind, with per-file before/after digests and the 17 re-bound projection expectations;
* the SoD re-declaration: `SOD006-C3` declared `OWNER_ORDERED_IN_FORCE`, `SOD006-C2` superseded and retained;
* **R10** — the pre-dispatch guard now agrees with the registry it serves: an owner-ordered declared \
collision is admitted with the conflict id visible in the verdict, while an undeclared collision is refused \
exactly as before. Authored by the mandated EXECUTE lane, promoted with backups taken first, oracle 7/7 from \
the canonical tree;
* the two lane dispatches verbatim (`required_arm == served_arm` for both) and the independent checker's \
verdict (C1-C7 AGREE), **disclosed as coming from a checker that shares the writer's model**;
* three self-caught defects (backup ordering, an unquoted YAML note, a dropped bound field) and — found by \
the checker, not by us — a cross-artifact inconsistency deliberately NOT edited after the verdict;
* the frozen subject digest, the four recovered preimages, the reviewable patch, and the OpenSpec change.

## Not claimed

* No model diversity between writer and checker: absent by owner order, and declared as such.
* No canonical acceptance: `hgk_canonical_acceptance: NOT_PERFORMED`. Applying a ruling is not accepting it.
* The guard's exit-0 ADMIT path is not reachable in production: nothing in the product produces an admission \
receipt (gap **R11**), so the round submits the lane's own serving evidence instead and says so.
* The checker verdict is advisory; it is not an external review.

## Where to look

`EVIDENCE/ROUND3-LANE-REBIND-AND-CLOSURE-20261016/README.md` indexes everything; `FAR_RULING.md` and \
`FAR_RULING_ADDENDUM_A.md` are the ruling and the defects found while executing it; `ROUND_CLOSURE.json` is \
the machine-readable closure; `implementation/` carries before/after files and unified diffs; \
`RETROSPECTIVE.md` + `SELF_EVOLUTION.md` are the next round's priced proposals.
"""

HEAD = subprocess.check_output(['git', '-C', str(FAB), 'rev-parse', 'HEAD'], text=True).strip()
tok = re.search(r'github_pat_[A-Za-z0-9_]+', KEY.read_text(encoding='utf-8', errors='replace'))
if not tok:
    raise SystemExit('no token found in the key file')

req = urllib.request.Request(
    'https://api.github.com/repos/%s/pulls' % REPO,
    data=json.dumps({'title': 'ROUND3-LANE-REBIND-AND-CLOSURE-20261016: lanes rebound to the owner order, '
                              'guard/registry SoD agreement, candidate-only',
                     'head': BRANCH, 'base': BASE, 'body': BODY}).encode('utf-8'),
    headers={'Authorization': 'Bearer %s' % tok.group(0),
             'Accept': 'application/vnd.github+json',
             'X-GitHub-Api-Version': '2022-11-28',
             'User-Agent': 'hg-kseos-governed-runtime'})
try:
    with urllib.request.urlopen(req, timeout=60) as r:
        doc = json.loads(r.read().decode('utf-8'))
    print(json.dumps({'created': True, 'number': doc.get('number'), 'html_url': doc.get('html_url'),
                      'head': (doc.get('head') or {}).get('ref'),
                      'base': (doc.get('base') or {}).get('ref'),
                      'additions': doc.get('additions'),
                      'changed_files': doc.get('changed_files')}, ensure_ascii=False, indent=1))
except urllib.error.HTTPError as e:
    body = e.read().decode('utf-8', 'replace')[:600]
    print('PR CREATE FAILED', e.code, body)
    raise SystemExit(3)
