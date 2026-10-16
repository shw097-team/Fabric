"""Record the digest of the checker's reference tree, and why it is NOT in the packet.

`subject/` is a byte-identical copy of the canonical `scripts/ src/ tests/ config/` trees, built so the
VERIFY/SECURITY lane has a complete read-only reference to run the suites against. It is an ~8 MB
duplicate of content that already lives in the repository, so it is EXCLUDED from the published packet --
and this file is what makes that exclusion auditable rather than silent: the digest lets a reader confirm
the copy the checker used was the canonical tree, without carrying the bytes.
"""
import hashlib
import json
import sys
from pathlib import Path

O = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
SUB = O / 'subject'
rows = []
agg = hashlib.sha256()
for d in ('scripts', 'src', 'tests', 'config'):
    files = sorted(p for p in (SUB / d).rglob('*') if p.is_file()
                   and p.suffix not in ('.pyc',) and '__pycache__' not in p.parts)
    h = hashlib.sha256()
    for p in files:
        h.update(p.read_bytes())
        agg.update(p.read_bytes())
    rows.append({'dir': d, 'files': len(files), 'digest': h.hexdigest()})

doc = {
    'schema': 'HGK-CHECKER-REFERENCE-TREE-DIGEST/1',
    'round': O.name,
    'tree': 'subject/',
    'purpose': ('read-only reference tree handed to the VERIFY/SECURITY lane; the lane runs the suites '
                'against a writable COPY the runner makes under its own lane directory'),
    'in_packet': False,
    'reason_excluded': 'byte-identical duplicate of content that already lives in the repository (~8 MB)',
    'per_dir': rows,
    'aggregate_sha256': agg.hexdigest(),
}
(O / 'SUBJECT_TREE_DIGEST.json').write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding='utf-8')
print('SUBJECT_TREE_DIGEST', doc['aggregate_sha256'][:16], sum(r['files'] for r in rows), 'files')
