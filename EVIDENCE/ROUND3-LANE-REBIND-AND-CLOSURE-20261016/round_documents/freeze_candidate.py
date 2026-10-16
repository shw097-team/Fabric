"""Freeze the candidate tree: a digest manifest the checker must recompute before any verdict.

Excludes __pycache__, *.pyc and the round's own TEST_RESULTS scratch, so the manifest covers the
subject the checker is judging and not the harness's noise.
"""
import hashlib
import json
import pathlib
from datetime import datetime, timezone

R = pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS')
O = R / 'var/ROUND3-LANE-REBIND-AND-CLOSURE-20261016'
CAND = O / 'candidate'
SKIP = ('__pycache__', '.pytest_cache', 'TEST_RESULTS')
PRODUCT = ['scripts/runtime_role_binding_assert.py',
           'scripts/hgk-governed-runtime-controller.py',
           'tests/test_governed_runtime_controller.py',
           'tests/test_lane_effort_enforcement.py']


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


files = []
for p in sorted(CAND.rglob('*')):
    if not p.is_file():
        continue
    rel = str(p.relative_to(CAND)).replace('\\', '/')
    if any(s in rel.split('/') for s in SKIP) or p.suffix == '.pyc':
        continue
    files.append({'path': rel, 'bytes': p.stat().st_size, 'sha256': sha(p)})

agg = hashlib.sha256()
for f in files:
    agg.update((f['path'] + ':' + f['sha256'] + '\n').encode('utf-8'))

manifest = {
    'schema': 'HGK-FROZEN-CANDIDATE-MANIFEST/1',
    'round': O.name,
    'frozen_utc': datetime.now(timezone.utc).isoformat(),
    'subject_root': str(CAND),
    'file_count': len(files),
    'aggregate_sha256': agg.hexdigest(),
    'changeset_files': {rel: {'sha256': sha(CAND / rel), 'bytes': (CAND / rel).stat().st_size}
                        for rel in PRODUCT if (CAND / rel).is_file()},
    'files': files,
    'claim_ceiling': ('The frozen subject. A checker MUST recompute the aggregate from the tree before any verdict; '
                      'a mismatch means it is judging something else.'),
}
out = O / 'FROZEN_MANIFEST.json'
out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'manifest': str(out), 'file_count': len(files),
                  'aggregate_sha256': agg.hexdigest(),
                  'changeset_files': {k: v['sha256'][:16] for k, v in manifest['changeset_files'].items()}},
                 ensure_ascii=False, indent=1))
