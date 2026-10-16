"""R1/R3 completion — the coupled pins the lane guard caught.

As first applied, R1/R3 was INCOMPLETE: tests/test_lane_guard.py went from 0 failures to 4, all of the
form 'exit_code 3 != 4'. The guard refused EARLIER than the tests exercise, with ERR_LANE_SOURCE_STALE
and epoch_current=false, because two declarations are coupled to the site file but are not covered by
check_drift or by the conformance test:

  * registry source_of_routes{path: config/model-lane-assignment.json, revision, sha256} pins the SITE's
    revision AND its byte digest -- editing the site without re-pinning makes every guard evaluation
    report a stale source;
  * the registry's epoch and the site's own `revision` (== live_epoch) must advance together.

This is the same class as the R7 finding: a change to one declaration surface silently invalidates
another, and the surface that would have caught it (check_drift) does not look at it. The existing test
did catch it, which is why this is a completion and not a rollback.

Edits, in this order (the digest is computed AFTER the site is final):
  S1  site revision 20 -> 21
  S2  site registry_epoch 20 -> 21
  R1  registry source_of_routes.revision 20 -> 21
  R2  registry source_of_routes.sha256 -> the site's post-edit digest
  R3  registry projections /registry_epoch and /revision expected 20 -> 21
  R4  registry projection-group note (prose that still described revision 19 / PLAN=GLM)
"""
import hashlib
import json
import pathlib
import subprocess
import sys

R = pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS')
O = R / 'var/FAR-REMEDIATION-AND-CLOSURE-20261016'
PY = 'C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe'
REG = R / 'config/lane-routing-registry.yaml'
SITE = R / 'config/model-lane-assignment.json'
APPLY = '--apply' in sys.argv
OLD_SITE_SHA = 'd41f8f8bff41d4338a4b85dab7a60bd2c9c23b2f5f39c8c008e89bf82587bd36'
log = {'apply': APPLY, 'edits': []}


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def sub(text, old, new, where):
    n = text.count(old)
    if n != 1:
        raise SystemExit('EDIT NOT UNIQUE (%d) in %s: %s' % (n, where, old[:80]))
    log['edits'].append({'where': where, 'old_head': old[:60]})
    return text.replace(old, new)


# ---- S1/S2 (site must be final BEFORE the digest is taken)
log['site_sha_before'] = sha(SITE)
site = json.loads(SITE.read_text(encoding='utf-8'))
if site.get('revision') != 21:
    site['revision'] = 21
    site['registry_epoch'] = 21
    if APPLY:
        SITE.write_text(json.dumps(site, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
new_site_sha = sha(SITE)
log['site_sha_after'] = new_site_sha

# ---- R1/R2
text = REG.read_text(encoding='utf-8')
log['registry_sha_before'] = sha(REG)
text = sub(text, 'source_of_routes:\n  path: config/model-lane-assignment.json\n  revision: 20\n  sha256: ' + OLD_SITE_SHA,
           'source_of_routes:\n  # Re-pinned in round FAR-REMEDIATION-AND-CLOSURE-20261016 (R1/R3 completion): the site file was\n'
           '  # edited (PLAN rebind, the corrected VERIFY-arm prose, revision 20 -> 21), so the recorded digest\n'
           '  # and revision had to move with it. Without this the pre-dispatch lane guard refuses every\n'
           '  # evaluation with ERR_LANE_SOURCE_STALE. Its sibling epoch coupling is below.\n'
           '  path: config/model-lane-assignment.json\n  revision: 21\n  sha256: ' + new_site_sha,
           'registry source_of_routes revision+sha256')

# ---- R3
text = sub(text, '      - {pointer: /registry_epoch, expected: 20}\n      - {pointer: /revision, expected: 20}',
           '      - {pointer: /registry_epoch, expected: 21}\n      - {pointer: /revision, expected: 21}',
           'registry projections /registry_epoch + /revision')

# ---- R4
text = sub(text,
           '    note: canonical policy revision 19 (owner PLAN rebind 2026-10-15) — PLAN rank-1 is '
           'opencode-go/glm-5.3-flash and the GPT arm is a non-default alternate; additional EXECUTE route is '
           'operator-selectable only; VERIFY arm selection is owner-adjudicated.',
           '    note: canonical policy revision 21 (owner order 2026-10-16, round '
           'FAR-REMEDIATION-AND-CLOSURE-20261016). PLAN rank-1 is openai-codex/gpt-6.1-sol (medium, OAuth) '
           'with the owner-chain fallbacks GLM-5.3-Flash then DeepSeek V4.1 Flash; the additional EXECUTE '
           'route is operator-selectable only; VERIFY_SECURITY arm A is openai-codex/gpt-6.1-sol and arm B is '
           'opencode-go/glm-5.3-flash. Supersedes the 2026-10-15 GLM rebind, whose 429 premise was measured '
           'false on 2026-10-16.',
           'registry projection-group note')

if APPLY:
    REG.write_text(text, encoding='utf-8')
log['registry_sha_after'] = sha(REG)

# ---- verification: the guard, the suites, the drift gate
if APPLY:
    log['lane_guard_suite'] = subprocess.run(
        [PY, '-B', '-m', 'unittest', 'tests.test_lane_guard', 'tests.test_lane_policy'],
        cwd=str(R), capture_output=True, text=True, timeout=900)
    tail = (log['lane_guard_suite'].stdout + log['lane_guard_suite'].stderr).strip().splitlines()
    log['lane_guard_suite'] = {'exit': log['lane_guard_suite'].returncode,
                               'ran': next((l for l in tail if l.startswith('Ran ')), ''),
                               'verdict': tail[-1] if tail else '',
                               'failed': [l for l in tail if l.startswith(('FAIL:', 'ERROR:'))]}
    pr = subprocess.run([PY, '-B', 'var/FAR-REMEDIATION-AND-CLOSURE-20261016/probe_lane_guard_exit4.py'],
                        cwd=str(R), capture_output=True, text=True, timeout=300)
    log['guard_probe'] = pr.stdout.strip().splitlines()[:1]
    dr = subprocess.run([PY, '-B', '-c',
                         'import sys,json;sys.path.insert(0,"src");from hg_kseos.lane_policy import check_drift;'
                         'd=check_drift();print(json.dumps({"n":len(d),"fatal":[x for x in d if x.get("severity")=="error"]},ensure_ascii=False))'],
                        cwd=str(R), capture_output=True, text=True, timeout=300)
    log['check_drift'] = dr.stdout.strip()[-400:]

(O / 'R1_R3_COMPLETION_RECEIPT.json').write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(log, ensure_ascii=False, indent=1)[:2200])
