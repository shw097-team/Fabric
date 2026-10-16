"""Round FAR-REMEDIATION-AND-CLOSURE-20261016 lane runner (reused proven shape).

    python -B run_lane.py <ROLE> <TAG> <PROMPT_MD_REL> [GUARD_SUBJECT_REL]

ROLE   : EXECUTE | VERIFY_SECURITY
TAG    : attempt tag; the output subtree lanes/<ROLE>/<TAG>/ is created fresh (never overwritten)
PROMPT : brief, relative to the round root
GUARD  : VERIFY_SECURITY only -- the frozen subject the checker's window is judged against,
         relative to the round root (default: candidate)

Every attempt gets its OWN immutable output subtree. The dispatcher is the only surface that turns
the mandated arm into worker argv, so the receipt's required_arm/served_arm is the arm evidence.
"""
import datetime
import json
import os
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

R = Path('C:/Projects/Agent_Workspace/HG-KSEOS')
O = R / 'var/FAR-REMEDIATION-AND-CLOSURE-20261016'

role, tag, promptfile = sys.argv[1:4]
lane = 'VERIFY_SECURITY' if role == 'VERIFY_SECURITY' else 'EXECUTE'
guard_rel = sys.argv[4] if len(sys.argv) > 4 else 'candidate'
guard = (O / guard_rel).resolve()

root = O / 'candidate' if lane == 'EXECUTE' else O / 'checker'
out = O / 'lanes' / role / tag
assert not out.exists(), f'REFUSING_TO_OVERWRITE_AN_EXISTING_ATTEMPT: {out}'
out.mkdir(parents=True)

# --- admission readback: the discipline is enforced from the SPINE, not from a local file ---------
db = R / 'var/shared-spine/hg-kseos.db'
with sqlite3.connect(db.as_uri() + '?mode=ro', uri=True) as c:
    row = c.execute(
        'SELECT r.state, t.state, w.state, t.writable_root FROM requirements r '
        'JOIN taskspecs t ON t.requirement_id = r.requirement_id '
        'JOIN workorders w ON w.taskspec_id = t.taskspec_id WHERE w.workorder_id = ?',
        ('WO-FAR-REMEDIATION-AND-CLOSURE-20261016-' + role,)).fetchone()
assert row and row[:3] == ('FROZEN', 'ADMITTED', 'CREATED'), f'INCOMPLETE_ADMISSION: {row}'
assert Path(row[3]) == root, f'WRITABLE_ROOT_MISMATCH: {row[3]} != {root}'

mandate = json.loads((O / 'role_mandate.json').read_text(encoding='utf-8'))
declared = mandate['roles'][lane]
arm = f"{declared['provider']}/{declared['model']}"
rank = str(declared.get('rank', 1))
nonce = 'LANE_RELIABILITY_' + role + '_' + tag + '_DONE'

exe = json.loads((R / 'config/hermes-codex-lane.json').read_text(encoding='utf-8'))['codex_executable']
assert Path(exe).is_file(), f'CODEX_EXECUTABLE_MISSING: {exe}'

prompt = (O / promptfile).read_text(encoding='utf-8') + (
    '\nWINDOWS COMMAND CONSTRAINT: no PowerShell scriptblocks, ForEach-Object, shell loops, '
    'multi-statement commands or heredocs. Use native apply_patch for edits. For bounded source reads '
    'use one simple command. Tests: write a driver .py under TEST_RESULTS via apply_patch, then run it '
    'in one simple interpreter invocation. Test-first RED must be against actual production behaviour, '
    'never a post-hoc stub. No broad repeated source survey. '
    'Your final answer MUST end with this standalone exact transport token (it is NOT a verdict): '
    + nonce)

if lane == 'VERIFY_SECURITY':
    assert guard.is_dir() and guard.resolve().is_relative_to(O.resolve()), f'BAD_GUARD_SUBJECT: {guard}'
    assert (guard / 'scripts/runtime_role_binding_assert.py').is_file(), 'GUARD_SUBJECT_NOT_THE_CANDIDATE'
    work = out / 'work'
    work.mkdir(parents=True)
    copy = work / 'subject'
    shutil.copytree(guard, copy, ignore=shutil.ignore_patterns('.git', '__pycache__', '*.pyc',
                                                               '.pytest_cache', 'TEST_RESULTS'))
    # The suite scratch precondition differs by root: <ROOT.parent>/TEST_RESULTS must exist, else the
    # controller/guard suites error before asserting.
    (work / 'TEST_RESULTS').mkdir(parents=True, exist_ok=True)
    for p in ('scripts', 'src', 'tests', 'config'):
        assert (copy / p).is_dir(), 'INCOMPLETE_SUBJECT_COPY:' + p
    prompt += ('\nWRITABLE WORKSPACE: your cwd is ' + str(work) + ' (writable). The FROZEN subject '
               '(the digest reference; NEVER write there) is ' + str(guard) + '. A byte-identical COPY '
               'is at ' + str(copy) + ' -- run the suites IN THE COPY. Recompute the frozen subject '
               'digest over the copy and assert it equals the declared value BEFORE reporting any '
               'verdict. Write your verdict JSON in your cwd, NOT in the subject. Return your verdict '
               'as your ONLY final agent message, one compact JSON object on a single line, ending '
               'with the transport token line.')
    sandbox, cwd_v = 'workspace-write', str(work)
    allow_esc = True   # DISCLOSED: cwd is a scratch OUTSIDE the guarded subject; --guard-subject still judges it
else:
    sandbox, cwd_v, allow_esc = 'workspace-write', str(root), False
    prompt += ('\nWRITABLE ROOT: ' + str(root) + ' (your cwd). Write ONLY the files named in the '
               'WRITE SET section, plus your own scratch under TEST_RESULTS/.')

seconds = int(os.environ.get('LANE_TIMEOUT_S', '900'))
argv = [sys.executable, str(R / 'scripts/hgk-lane-dispatch.py'), '--lane', lane,
        '--require-arm', arm, '--force-rank', rank, '--max-candidates', '1',
        '--sandbox', sandbox, '--cwd', cwd_v, '--codex-executable', exe,
        '--prompt', prompt, '--nonce', nonce, '--timeout', str(seconds),
        '--json-out', str(out / 'dispatch.json'), '--attempt-log-dir', str(out / 'raw')]
if lane == 'VERIFY_SECURITY':
    argv += ['--guard-subject', str(guard)]
    if allow_esc:
        argv += ['--allow-sandbox-escalation']

(out / 'invocation.json').write_text(json.dumps({
    'start': datetime.datetime.now().astimezone().isoformat(),
    'argv': argv,
    'workorder': 'WO-FAR-REMEDIATION-AND-CLOSURE-20261016-' + role,
    'mandate_ref': str(O / 'role_mandate.json'),
    'declared_arm': arm, 'forced_rank': rank, 'nonce': nonce,
    'guard_subject': str(guard) if lane == 'VERIFY_SECURITY' else None,
    'claim_ceiling': 'the receiver of this receipt is the orchestrator; a lane verdict is advisory',
}, ensure_ascii=False, indent=2), encoding='utf-8')

try:
    p = subprocess.run(argv, cwd=R, capture_output=True, text=True, encoding='utf-8',
                       errors='replace', timeout=seconds + 120)
    code, stdout, stderr = p.returncode, p.stdout, p.stderr
except subprocess.TimeoutExpired as e:
    code = 124
    stdout = e.stdout or ''
    stderr = e.stderr or ''
    if isinstance(stdout, bytes):
        stdout = stdout.decode('utf-8', 'replace')
    if isinstance(stderr, bytes):
        stderr = stderr.decode('utf-8', 'replace')

(out / 'stdout.txt').write_text(stdout, encoding='utf-8')
(out / 'stderr.txt').write_text(stderr, encoding='utf-8')
(out / 'exit.json').write_text(json.dumps(
    {'exit': code, 'end': datetime.datetime.now().astimezone().isoformat()}), encoding='utf-8')
print('RESULT', role, tag, 'exit=' + str(code))
print('--- stdout tail ---')
print(stdout[-6000:])
print('--- stderr tail ---')
print(stderr[-2000:])
sys.exit(code)
