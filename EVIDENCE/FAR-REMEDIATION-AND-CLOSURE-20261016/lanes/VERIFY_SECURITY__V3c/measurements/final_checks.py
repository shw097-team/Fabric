import hashlib
import json
from pathlib import Path
import re

WORK = Path(__file__).resolve().parent.parent
ROUND = WORK.parents[3]
ROOT = ROUND.parent.parent
OUT = WORK / 'TEST_RESULTS'
manifest = json.loads((ROUND / 'FROZEN_MANIFEST.json').read_text(encoding='utf-8'))
rows = []
aggregate = hashlib.sha256()
for item in manifest['items']:
    path = Path(item['path'])
    actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
    size = path.stat().st_size if path.is_file() else None
    rows.append({'label': item['label'], 'path': item['path'], 'bytes': size, 'sha256': actual, 'matches': size == item['bytes'] and actual == item['sha256']})
    aggregate.update((item['label'] + '|' + item['path'] + '|' + str(actual) + '\n').encode())
result = {'manifest_aggregate': aggregate.hexdigest(), 'manifest_items': rows, 'frozen_post_comparison': []}
previous = ROOT / 'var/LANE-RELIABILITY-CLOSURE-20261016'
candidate_manifest = json.loads((previous / 'FROZEN_MANIFEST.json').read_text(encoding='utf-8'))
result['candidate_files_checked'] = len(candidate_manifest['files'])
result['candidate_mismatches'] = []
for item in candidate_manifest['files']:
    path = previous / 'candidate' / item['path']
    actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
    if actual != item['sha256'] or not path.is_file() or path.stat().st_size != item['bytes']:
        result['candidate_mismatches'].append({'path': str(path), 'actual_sha256': actual, 'expected_sha256': item['sha256']})
for name in ('lane-routing-registry.yaml', 'model-lane-assignment.json'):
    result['frozen_post_comparison'].append({'file': name, 'hashes': {label: hashlib.sha256(path.read_bytes()).hexdigest() for label, path in [('post_state', ROUND / 'frozen/post_state' / name), ('canonical', ROOT / 'config' / name), ('copy', WORK / 'subject/config' / name)]}})
result['R5_document_search'] = []
for path in sorted(ROUND.rglob('*')):
    relative = path.relative_to(ROUND)
    if not path.is_file() or path.suffix not in ('.json', '.md') or any(part in ('subject', 'candidate', 'TEST_RESULTS', 'work', '.git') for part in relative.parts):
        continue
    if path.stat().st_size > 2000000:
        continue
    for number, line in enumerate(path.read_text(encoding='utf-8-sig', errors='replace').splitlines(), 1):
        if re.search(r'R5.{0,150}(LANDED|DELIVER|CLOSED|landed|delivered|closed)|turn.shape.{0,150}(LANDED|DELIVER|CLOSED|landed|delivered|closed)|NOT LANDED', line):
            result['R5_document_search'].append({'path': str(relative), 'line': number, 'text': line[:1500]})
(OUT / 'final_checks.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps({'manifest_aggregate': result['manifest_aggregate'], 'mismatches': [row for row in rows if not row['matches']], 'frozen_post_comparison': result['frozen_post_comparison'], 'R5_document_search': result['R5_document_search']}, indent=2, ensure_ascii=False))
