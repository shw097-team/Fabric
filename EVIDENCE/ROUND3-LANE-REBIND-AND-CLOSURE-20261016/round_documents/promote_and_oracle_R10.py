"""Promote the EXECUTE lane's bounded change into the canonical tree, then run the oracle itself.

Order of operations is the point of this script (SC-12 taught it): back up BEFORE any write, diff first,
refuse to promote a candidate that changed nothing or changed something outside the write set, and only
then re-run the oracle from the CANONICAL tree -- the writer's own green run is a claim, not acceptance.

Oracle (all four must be produced, verbatim, into evidence/):
  1 the writer's new test module, run from canonical
  2 the lane-policy conformance test, run from canonical
  3 the three MEASURED pre-dispatch guard cases: undeclared same-model -> refuse; declared owner-ordered
    -> ADMIT with the conflict id; distinct pair -> ADMIT unchanged
  4 check_drift == 0 errors over the live registry/site pair

Refuses (exit != 0) rather than half-promoting: a missing candidate file, an empty diff, a diff outside the
write set, a backup that cannot be written, or any oracle step that does not behave as the ruling requires.
"""
import datetime
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys

R = pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS')
O = R / 'var/ROUND3-LANE-REBIND-AND-CLOSURE-20261016'
CAND = O / 'candidate'
EVID = O / 'evidence'
PY = 'C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe'
APPLY = '--apply' in sys.argv
STAMP = 'round3-promote-' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
WRITESET = ['scripts/hgk-lane-guard.py', 'src/hg_kseos/lane_policy.py', 'tests/test_lane_guard.py']
receipt = {'schema': 'HGK-ROUND3-PROMOTION-RECEIPT/1', 'round': O.name, 'apply': APPLY, 'stamp': STAMP,
           'files': [], 'oracle': {}}


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


# ------------------------------------------------------------------ 1. diff the candidate against canonical
for rel in WRITESET:
    c, k = CAND / rel, R / rel
    if not c.is_file():
        raise SystemExit('CANDIDATE FILE MISSING: %s' % rel)
    same = sha(c) == sha(k)
    n = sum(1 for a, b in zip(c.read_text(encoding='utf-8').split('\n'),
                               k.read_text(encoding='utf-8').split('\n')) if a != b)
    receipt['files'].append({'file': rel, 'identical_to_canonical': same,
                             'candidate_sha256': sha(c), 'canonical_sha256_before': sha(k),
                             'changed_lines': n})
    print('%-34s identical=%-5s changed_lines=%d' % (rel, same, n))
if all(f['identical_to_canonical'] for f in receipt['files']):
    raise SystemExit('REFUSING TO PROMOTE: the bounded writer changed none of the write set')
# nothing outside the write set may differ
extra = []
for d in ('scripts', 'src', 'tests', 'config'):
    for p in (CAND / d).rglob('*'):
        if p.is_file():
            rel = str(p.relative_to(CAND)).replace('\\', '/')
            if rel not in WRITESET and sha(p) != sha(R / rel):
                extra.append(rel)
if extra:
    raise SystemExit('REFUSING TO PROMOTE: candidate changed files OUTSIDE the write set: %s' % extra[:10])
receipt['outside_write_set_changes'] = []

# ----------------------------------------------------------------------------------- 2. backup, then write
if APPLY:
    for f in receipt['files']:
        b = R / (f['file'] + '.bak-' + STAMP)
        shutil.copy2(R / f['file'], b)                       # BEFORE the write -- the SC-12 correction
        f['backup'] = b.name
        shutil.copy2(CAND / f['file'], R / f['file'])
        f['canonical_sha256_after'] = sha(R / f['file'])
        print('%-34s promoted, backup=%s' % (f['file'], b.name))

# ------------------------------------------------------------------------------------------ 3. the oracle
def run(label, argv, cwd=R, expect_exit=0, must_contain=()):
    p = subprocess.run([PY, '-B'] + argv, cwd=str(cwd), capture_output=True, text=True,
                       encoding='utf-8', errors='replace', timeout=900)
    out = (p.stdout or '') + (p.stderr or '')
    ok = (p.returncode == expect_exit) and all(s in out for s in must_contain)
    receipt['oracle'][label] = {'argv': argv, 'exit': p.returncode, 'expected_exit': expect_exit,
                                'must_contain': list(must_contain), 'ok': ok}
    (EVID / ('ORACLE_%s.txt' % label)).write_text(
        'ARGV: %s\nEXPECTED EXIT: %s\nMUST CONTAIN: %s\nACTUAL EXIT: %s\n--- output ---\n%s'
        % (argv, expect_exit, list(must_contain), p.returncode, out), encoding='utf-8')
    print('ORACLE %-28s exit=%s expected=%s ok=%s' % (label, p.returncode, expect_exit, ok))
    return ok

EVID.mkdir(parents=True, exist_ok=True)
G = R / 'scripts/hgk-lane-guard.py'
DEEPSEEK = 'opencode-go/deepseek-v4.1-flash'
GLM = 'opencode-go/glm-5.3-flash'
res = {}
res['writer_test_module'] = run('writer_test_module', [str(R / 'tests/test_lane_guard.py')], expect_exit=0)
res['conformance'] = run('conformance', [str(R / 'tests/test_lane_policy.py')], expect_exit=0,
                         must_contain=('OK',))
# case 1: an UNDECLARED same-model pair must still be refused (conformance E1: no new hole)
res['guard_undeclared_collision'] = run(
    'guard_undeclared_collision',
    [str(G), '--lane', 'EXECUTE', '--maker-lane', 'PLAN', '--maker-engine', 'hermes',
     '--maker-model', GLM, '--target-engine', 'codex-cli', '--target-model', GLM,
     '--admission', 'UNPROVEN', '--expected-epoch', '22', '--root', '.'], expect_exit=2,
    must_contain=('ERR_LANE_SOD_VIOLATION',))
# case 2: the owner-ordered declared pair must be ADMITTED, visibly naming the conflict
res['guard_declared_owner_ordered'] = run(
    'guard_declared_owner_ordered',
    [str(G), '--lane', 'VERIFY_SECURITY', '--maker-lane', 'EXECUTE', '--maker-engine', 'codex-cli',
     '--maker-model', DEEPSEEK, '--target-engine', 'codex-cli', '--target-model', DEEPSEEK,
     '--target-provider', 'opencode-go', '--admission', 'UNPROVEN', '--expected-epoch', '22',
     '--root', '.'], expect_exit=0, must_contain=('SOD006-C3',))
# case 3: a genuinely distinct pair is unaffected
res['guard_distinct_pair'] = run(
    'guard_distinct_pair',
    [str(G), '--lane', 'VERIFY_SECURITY', '--maker-lane', 'PLAN', '--maker-engine', 'hermes',
     '--maker-model', GLM, '--target-engine', 'codex-cli', '--target-model', DEEPSEEK,
     '--target-provider', 'opencode-go', '--admission', 'UNPROVEN', '--expected-epoch', '22',
     '--root', '.'], expect_exit=0, must_contain=('SOD_OK',))
# drift must stay clean
_drift = subprocess.run([PY, '-B', '-c',
    "import sys;sys.path.insert(0,'src');from hg_kseos import lane_policy as lp;"
    "rp='config/lane-routing-registry.yaml';f=lp.check_drift(rp,root='.',registry=lp.load_registry(rp));"
    "print('ERRORS',len([x for x in f if x.get('severity')=='error']));print('TOTAL',len(f))"],
    cwd=str(R), capture_output=True, text=True, encoding='utf-8')
res['check_drift'] = ('ERRORS 0' in _drift.stdout)
receipt['oracle']['check_drift'] = {'stdout': _drift.stdout.strip(), 'ok': res['check_drift']}
print('ORACLE check_drift                %s' % _drift.stdout.strip().replace('\n', ' | '))

receipt['all_oracle_ok'] = all(res.values())
if APPLY:
    (O / 'PROMOTION_RECEIPT.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'apply': APPLY, 'oracle': res, 'all_oracle_ok': receipt['all_oracle_ok']}, indent=1))
sys.exit(0 if receipt['all_oracle_ok'] else 5)
