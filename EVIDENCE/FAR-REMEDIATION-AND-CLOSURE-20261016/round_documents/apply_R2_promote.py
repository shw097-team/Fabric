"""R2 — promote the verified candidate product files to the canonical tree.

The PROMOTE set is taken from the MEASURED enumeration (var/.../evidence/EVIDENCE_PROMOTION_SCOPE.json,
produced by a read-only walk over both trees), never from memory. Four files, and nothing else:

  scripts/runtime_role_binding_assert.py        (the M03 effort axis)
  scripts/hgk-governed-runtime-controller.py    (the absent-session-id outage)
  tests/test_governed_runtime_controller.py     (its typed tests)
  tests/test_lane_effort_enforcement.py         (its typed tests; NEW file)

Two candidate config files were also modified relative to canonical but are STALE (revision 19 vs the
canonical 20, now 21) — retaining canonical there is the measured decision, recorded rather than acted on.

This is an APPLY under the owner's authorisation to execute the ruling. It is NOT an acceptance: the
oracle (the two test modules) is re-run by the orchestrator, and external acceptance stays NOT_PERFORMED.

WorkOrder: WO-FAR-REMEDIATION-AND-CLOSURE-20261016-R2.
"""
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys

R = pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS')
O = R / 'var/FAR-REMEDIATION-AND-CLOSURE-20261016'
CAND = R / 'var/LANE-RELIABILITY-CLOSURE-20261016/candidate'
PY = 'C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe'
SUFFIX = '.bak-far-remediation-20261016'
APPLY = '--apply' in sys.argv
BIG = O / 'evidence/EVIDENCE_PROMOTION_SCOPE.json'

REL = ['scripts/runtime_role_binding_assert.py',
       'scripts/hgk-governed-runtime-controller.py',
       'tests/test_governed_runtime_controller.py',
       'tests/test_lane_effort_enforcement.py']


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


log = {'workorder': 'WO-FAR-REMEDIATION-AND-CLOSURE-20261016-R2', 'apply': APPLY, 'files': []}

# ---------------------------------------------------------------- shrink the 114 MB enumeration
if BIG.is_file() and BIG.stat().st_size > 8_000_000:
    big = json.loads(BIG.read_text(encoding='utf-8'))
    summary = {'schema': big.get('schema'), 'generated_for_round': big.get('generated_for_round'),
               'counts': big.get('notes', {}).get('counts'),
               'promote': big.get('promote'),
               'needs_owner_decision_count': len(big.get('needs_owner_decision', [])),
               'do_not_promote_count': len(big.get('do_not_promote', [])),
               'completeness': big.get('notes', {}).get('completeness'),
               'exactness_claim': big.get('notes', {}).get('exactness_claim')}
    (O / 'evidence/EVIDENCE_PROMOTION_SCOPE.summary.json').write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    log['enumeration_compacted'] = {'original_bytes': BIG.stat().st_size,
                                    'kept': 'EVIDENCE_PROMOTION_SCOPE.md + .summary.json',
                                    'dropped_because': 'a 114 MB per-file listing cannot be published; every '
                                                       'classification count and the PROMOTE set are retained'}
    del big
    BIG.unlink()

# ---------------------------------------------------------------- promote
for rel in REL:
    src = CAND / rel
    dst = R / rel
    rec = {'rel': rel, 'candidate_exists': src.is_file(), 'canonical_existed': dst.is_file()}
    if not src.is_file():
        rec['action'] = 'SKIPPED: candidate file missing'
        log['files'].append(rec)
        continue
    rec['candidate_sha256'] = sha(src)
    rec['canonical_sha256_before'] = sha(dst) if dst.is_file() else None
    if rec['canonical_sha256_before'] == rec['candidate_sha256']:
        rec['action'] = 'ALREADY_IDENTICAL (no write)'
        log['files'].append(rec)
        continue
    if APPLY:
        if dst.is_file():
            b = pathlib.Path(str(dst) + SUFFIX)
            if not b.is_file():
                shutil.copy2(dst, b)
            rec['backup'] = str(b)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    rec['canonical_sha256_after'] = sha(dst) if dst.is_file() else None
    rec['action'] = 'PROMOTED' if APPLY else 'WOULD_PROMOTE (dry run)'
    rec['byte_identical_to_candidate'] = rec['canonical_sha256_after'] == rec['candidate_sha256']
    log['files'].append(rec)

# ---------------------------------------------------------------- the oracle, re-derived here
if APPLY:
    sys.path.insert(0, str(R / 'src'))
    try:
        from hg_kseos.spine import SharedSpine  # noqa: E402
        sp = SharedSpine(R / 'var/shared-spine/hg-kseos.db')
        head = subprocess.run(['git', '-C', 'C:/Projects/Agent_Workspace/HG-KSEOS', 'rev-parse', 'HEAD'],
                              capture_output=True, text=True).stdout.strip()
        sp.create_workorder('WO-FAR-REMEDIATION-AND-CLOSURE-20261016-R2',
                            'TS-FAR-REMEDIATION-AND-CLOSURE-20261016-R2', 'hermes-plan-orchestrator', R, head)
        log['workorder_created'] = True
    except Exception as exc:
        log['workorder_note'] = '%s: %s' % (type(exc).__name__, exc)

    for mod in ('tests.test_lane_effort_enforcement', 'tests.test_governed_runtime_controller'):
        pr = subprocess.run([PY, '-B', '-m', 'unittest', mod, '-v'], cwd=str(R),
                            capture_output=True, text=True, timeout=900)
        tail = (pr.stdout + pr.stderr).strip().splitlines()
        log.setdefault('oracle', {})[mod] = {
            'exit': pr.returncode,
            'ran': next((l for l in tail if l.startswith('Ran ')), ''),
            'verdict': tail[-1] if tail else '',
            'failed_lines': [l for l in tail if l.startswith('FAIL:') or l.startswith('ERROR:')]}
    # did anything else in the tree move?
    log['post_promotion_changed_vs_baseline'] = subprocess.run(
        ['git', '-C', 'C:/Projects/Agent_Workspace/HG-KSEOS', 'status', '--porcelain'],
        capture_output=True, text=True).stdout.strip().splitlines()

(O / 'R2_PROMOTION_RECEIPT.json').write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(log, ensure_ascii=False, indent=1))
