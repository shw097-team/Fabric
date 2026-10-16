"""Publish the gated packet to Fabric: branch off origin/main, stage ONLY the packet, commit, push.

Credential handling (Windows, HTTPS remote, fine-grained PAT):
  * the token is read from the key file at runtime and passed to git only through an environment variable
    and a temporary `askPass` WRAPPER .cmd — it is never an argv of git, never written into the repository,
    never printed, and the wrapper is deleted when this script exits;
  * `credential.helper=` (empty) and `credential.interactive=always` are set per-invocation, because on
    this host the Windows credential manager otherwise intercepts and a bare GIT_ASKPASS is ignored.
A wrapper that returns the token for every prompt is sufficient: GitHub accepts any username when the
password is a valid PAT.

Refuses to run if the packet is absent, if the gate report is not GATE_PASS, or if anything outside the
packet path would be staged. Never force-pushes; never merges.
"""
import json
import os
import pathlib
import re
import subprocess
import sys

R = pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS')
O = R / 'var/FAR-REMEDIATION-AND-CLOSURE-20261016'
FAB = pathlib.Path('C:/Projects/Agent_Workspace/Fabric')
KEY = pathlib.Path('C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt')
SCRATCH = pathlib.Path(os.environ.get('TMPDIR', 'C:/Users/user/AppData/Local/Temp'))
BRANCH = 'pub/far-remediation-and-closure-20261016'
PACKET_REL = 'EVIDENCE/FAR-REMEDIATION-AND-CLOSURE-20261016'
MSG = ('FAR-REMEDIATION-AND-CLOSURE-20261016: F1 closed, verified candidate promoted, R7 defect class '
       'named (candidate only)')
out = {'branch': BRANCH, 'steps': []}


def run(args, **kw):
    p = subprocess.run(args, capture_output=True, text=True, cwd=str(FAB), **kw)
    return p.returncode, (p.stdout or '').strip(), (p.stderr or '').strip()


def step(name, args, **kw):
    rc, so, se = run(args, **kw)
    out['steps'].append({'step': name, 'rc': rc, 'stdout': so[-600:], 'stderr': se[-400:]})
    return rc, so, se


# ---- preconditions
UPDATE = '--update' in sys.argv
gate = O / 'GATE_REPORT.json'
if not gate.is_file() or json.loads(gate.read_text(encoding='utf-8')).get('verdict') != 'GATE_PASS':
    print(json.dumps({'REFUSED': 'the gate report is missing or not GATE_PASS', 'verdict':
                      (json.loads(gate.read_text(encoding='utf-8')).get('verdict') if gate.is_file() else None)},
                     indent=1))
    sys.exit(2)
if not (FAB / PACKET_REL).is_dir():
    print(json.dumps({'REFUSED': 'packet directory absent: %s' % PACKET_REL}, indent=1))
    sys.exit(2)

tok = re.search(r'github_pat_[A-Za-z0-9_]+', KEY.read_text(encoding='utf-8', errors='replace'))
if not tok:
    print(json.dumps({'REFUSED': 'no token found in the key file'}, indent=1))
    sys.exit(2)

# ---- branch off the origin tip (never off a divergent local branch, never a force-push)
if UPDATE:
    # ADDITIVE update: the branch already carries this round's base commit on the remote, so a later
    # publication must STACK on it. Re-running the fresh-branch path here would rewrite the branch from
    # origin/main and the push would be rejected as non-fast-forward -- correctly, because it would drop
    # the earlier commit. The previous round used exactly this shape (four commits on one branch).
    rc, cur, _ = step('verify_branch', ['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
    if cur != BRANCH:
        print(json.dumps({'REFUSED': 'update mode requires the checked-out branch to be %s, found %s'
                          % (BRANCH, cur)}, indent=1))
        sys.exit(5)
    step('fetch', ['git', 'fetch', 'origin', '--prune'])
else:
    step('fetch', ['git', 'fetch', 'origin', '--prune'])
    step('checkout', ['git', 'checkout', '-B', BRANCH, 'origin/main'])
rc, porcelain, _ = step('status_before', ['git', 'status', '--porcelain'])
step('add', ['git', 'add', '--', PACKET_REL])
rc, staged, _ = step('staged_list', ['git', 'diff', '--cached', '--name-only'])
staged_files = [l for l in staged.splitlines() if l.strip()]
outside = [f for f in staged_files if not f.startswith(PACKET_REL + '/')]
out['staged_count'] = len(staged_files)
out['staged_outside_packet'] = outside
if outside:
    print(json.dumps({'REFUSED': 'staging leaked outside the packet', 'outside': outside[:10]}, indent=1))
    sys.exit(3)

if UPDATE:
    MSG = MSG + ' [addendum: remote readback, the final closure revision and the re-frozen manifest]'
rc, so, se = step('commit', ['git', 'commit', '-m', MSG])
if rc != 0 and 'nothing to commit' not in (so + se):
    print(json.dumps({'REFUSED': 'commit failed', 'stderr': se[:300]}, indent=1))
    sys.exit(4)

local_head = run(['git', 'rev-parse', 'HEAD'])[1]
out['local_head'] = local_head

# ---- push with the credential wrapper
wrapper = SCRATCH / 'hgk_push_askpass_round2.cmd'
wrapper.write_text('@echo off\r\necho %HGK_PUSH_TOKEN%\r\n', encoding='ascii')
env = dict(os.environ, HGK_PUSH_TOKEN=tok.group(0), GIT_ASKPASS=str(wrapper), GIT_TERMINAL_PROMPT='0')
rc, so, se = step('push', ['git', '-c', 'credential.helper=', '-c', 'credential.interactive=always',
                           '-c', 'core.askPass=' + str(wrapper),
                           'push', 'origin', 'HEAD:refs/heads/%s' % BRANCH], env=env)
try:
    wrapper.unlink()
except OSError:
    pass
# the token must never appear in what we captured
leaked = [s for s in out['steps'] if tok.group(0) in json.dumps(s)]
out['token_leaked_into_captured_output'] = bool(leaked)
if leaked:
    for s in leaked:
        s['stdout'] = s['stderr'] = '[REDACTED BY THE PUBLISHER]'
out['push_ok'] = (rc == 0)
(O / 'PUSH_RECEIPT.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'branch': BRANCH, 'local_head': local_head, 'staged_count': out['staged_count'],
                  'push_ok': out['push_ok'], 'push_rc': rc, 'token_leaked': out['token_leaked_into_captured_output'],
                  'push_stderr_tail': (se[-300:] if rc else '')}, ensure_ascii=False, indent=1))
sys.exit(0 if rc == 0 else 5)
