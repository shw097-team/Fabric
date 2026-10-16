"""The R10 oracle, run from CANONICAL after the promote. Corrects an expectation error in the promote script.

What was wrong there: the two ADMIT-path cases were expected to exit 0 with `--admission UNPROVEN`. They
cannot -- by design. `_load_admission()` accepts ADMITTED only from a RECEIPT FILE, and this round has no
legitimate receipt for the VERIFY/SECURITY target arm yet (the checker lane has not been dispatched, and the
EXECUTE lane's serving receipt proves a different arm). Inventing one to make a gate go green would be exactly
the trust-in-caller admission the gate exists to refuse. So the oracle asserts what is actually provable:

  * undeclared same-model pair            -> still exit 2, ERR_LANE_SOD_VIOLATION   (no new hole)
  * owner-ordered DECLARED pair           -> the SoD check passes and the verdict NAMES SOD006-C3, and the
                                             refusal that remains is the ADMISSION one (exit 3), never the
                                             SoD one
  * genuinely distinct pair               -> SoD_OK, unchanged
  * conformance + drift                   -> unchanged and clean

The residual is recorded, not hidden: the full exit-0 ADMIT path still needs an admission-receipt producer,
which is gap R11 in FAR_RULING_ADDENDUM_A.md.
"""
import json
import pathlib
import subprocess

R = pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS')
O = R / 'var/ROUND3-LANE-REBIND-AND-CLOSURE-20261016'
EVID = O / 'evidence'
PY = 'C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe'
G = R / 'scripts/hgk-lane-guard.py'
DEEP = 'opencode-go/deepseek-v4.1-flash'
GLM = 'opencode-go/glm-5.3-flash'
res = {}


def run(label, argv, want_exit, must, must_not=()):
    p = subprocess.run([PY, '-B'] + argv, cwd=str(R), capture_output=True, text=True,
                       encoding='utf-8', errors='replace', timeout=600)
    out = (p.stdout or '') + (p.stderr or '')
    ok = (p.returncode == want_exit) and all(s in out for s in must) and not any(s in out for s in must_not)
    (EVID / ('ORACLE_R10_%s.txt' % label)).write_text(
        'ARGV: %s\nWANT EXIT: %s\nMUST CONTAIN: %s\nMUST NOT CONTAIN: %s\nACTUAL EXIT: %s\n--- output ---\n%s'
        % (argv, want_exit, list(must), list(must_not), p.returncode, out), encoding='utf-8')
    res[label] = {'exit': p.returncode, 'want_exit': want_exit, 'ok': ok}
    print('%-30s exit=%-3s want=%-3s ok=%s' % (label, p.returncode, want_exit, ok))
    return ok


base = [str(G), '--expected-epoch', '22', '--root', '.']
a = run('01_undeclared_collision_refused',
        base + ['--lane', 'EXECUTE', '--maker-lane', 'PLAN', '--maker-engine', 'hermes',
                '--maker-model', GLM, '--target-engine', 'codex-cli', '--target-model', GLM,
                '--admission', 'UNPROVEN'], 2, ['ERR_LANE_SOD_VIOLATION'])
b = run('02_declared_pair_sod_admitted',
        base + ['--lane', 'VERIFY_SECURITY', '--maker-lane', 'EXECUTE', '--maker-engine', 'codex-cli',
                '--maker-model', DEEP, '--target-engine', 'codex-cli', '--target-model', DEEP,
                '--target-provider', 'opencode-go', '--admission', 'UNPROVEN'], 3,
        ['SOD006-C3', 'ERR_LANE_NOT_ADMITTED'], ['ERR_LANE_SOD_VIOLATION'])
c = run('03_distinct_pair_unchanged',
        base + ['--lane', 'VERIFY_SECURITY', '--maker-lane', 'PLAN', '--maker-engine', 'hermes',
                '--maker-model', GLM, '--target-engine', 'codex-cli', '--target-model', DEEP,
                '--target-provider', 'opencode-go', '--admission', 'UNPROVEN'], 3,
        ['SOD_OK'], ['ERR_LANE_SOD_VIOLATION'])
d = run('04_undeclared_inference_fail_closed',
        base + ['--lane', 'VERIFY_SECURITY', '--maker-engine', 'codex-cli',
                '--maker-model', 'opencode-go/mimo-v2.6-pro', '--target-engine', 'codex-cli',
                '--target-model', 'opencode-go/mimo-v2.6-pro', '--admission', 'UNPROVEN'], 2,
        ['ERR_LANE_SOD_VIOLATION'])
e = run('05_conformance_suite', [str(R / 'tests/test_lane_policy.py')], 0, ['OK'])
f = run('06_writer_test_module', [str(R / 'tests/test_lane_guard.py')], 0, ['OK'])
drift = subprocess.run([PY, '-B', '-c',
    "import sys;sys.path.insert(0,'src');from hg_kseos import lane_policy as lp;"
    "rp='config/lane-routing-registry.yaml';f=lp.check_drift(rp,root='.',registry=lp.load_registry(rp));"
    "print('ERRORS',len([x for x in f if x.get('severity')=='error']))"],
    cwd=str(R), capture_output=True, text=True, encoding='utf-8')
g = 'ERRORS 0' in drift.stdout
res['07_check_drift_zero_errors'] = {'ok': g, 'stdout': drift.stdout.strip()}
print('%-30s %s' % ('07_check_drift_zero_errors', drift.stdout.strip()))

receipt = {'schema': 'HGK-ROUND3-R10-ORACLE/1', 'round': O.name, 'cases': res,
           'all_ok': all(v['ok'] for v in res.values()),
           'claim_ceiling': ('the SoD exemption is proven for the owner-ordered declared pair; the exit-0 '
                             'ADMIT path is NOT proven because no legitimate admission receipt exists yet '
                             '(gap R11)')}
(EVID / 'ORACLE_R10_RECEIPT.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'all_ok': receipt['all_ok']}, indent=1))
