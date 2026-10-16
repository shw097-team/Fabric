import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

WORK = Path(__file__).resolve().parent.parent
ROUND = WORK.parents[3]
ROOT = ROUND.parent.parent
OUT = WORK / 'TEST_RESULTS'
SUB = WORK / 'subject'
REPORT = {}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def save():
    (OUT / 'derived.json').write_text(json.dumps(REPORT, indent=2, default=str), encoding='utf-8')

def run(label, args, cwd=SUB, env=None):
    result = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=600)
    text = result.stdout + result.stderr
    (OUT / (label + '.txt')).write_text(text, encoding='utf-8')
    summary = {'exit': result.returncode, 'names': re.findall(r'^(?:FAIL|ERROR): (.+)$', text, re.M), 'ran': re.findall(r'^Ran .+$', text, re.M), 'status': re.findall(r'^(?:FAILED|OK).*$', text, re.M)}
    REPORT[label] = summary
    save()
    print(label, json.dumps(summary), flush=True)
    return text

declared = read_json(ROUND / 'SUBJECT_TREE_DIGEST.json')
aggregate = hashlib.sha256()
directories = []
for directory in ('scripts', 'src', 'tests', 'config'):
    files = sorted(path for path in (SUB / directory).rglob('*') if path.is_file() and path.suffix != '.pyc' and '__pycache__' not in path.parts)
    current = hashlib.sha256()
    for path in files:
        data = path.read_bytes()
        current.update(data)
        aggregate.update(data)
    directories.append({'dir': directory, 'files': len(files), 'digest': current.hexdigest()})
REPORT['tree'] = {'computed': aggregate.hexdigest(), 'declared': declared['aggregate_sha256'], 'per_dir': directories, 'matches': directories == declared['per_dir'] and aggregate.hexdigest() == declared['aggregate_sha256']}
save()
assert REPORT['tree']['matches'], 'Reference copy does not match declared subject'
manifest = read_json(ROUND / 'FROZEN_MANIFEST.json')
aggregate = hashlib.sha256()
mismatches = []
for item in manifest['items']:
    path = Path(item['path'])
    actual = digest(path) if path.is_file() else None
    size = path.stat().st_size if path.is_file() else None
    if actual != item['sha256'] or size != item['bytes']:
        mismatches.append({'path': str(path), 'label': item['label'], 'expected_sha256': item['sha256'], 'actual_sha256': actual, 'expected_bytes': item['bytes'], 'actual_bytes': size})
    aggregate.update((item['label'] + '|' + item['path'] + '|' + str(actual) + '\n').encode())
REPORT['manifest'] = {'computed': aggregate.hexdigest(), 'declared': manifest['aggregate_sha256'], 'item_count': len(manifest['items']), 'count_matches': len(manifest['items']) == manifest['item_count'], 'mismatches': mismatches}
save()
print('DIGESTS', json.dumps(REPORT), flush=True)
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
os.environ['HGK_LANE_SCRATCH'] = str(OUT / 'scratch')
sys.path.insert(0, str(SUB / 'src'))
from hg_kseos import lane_policy as policy
before = OUT / 'before'
shutil.copytree(SUB / 'config', before / 'config', dirs_exist_ok=True)
for name in ('model-lane-assignment.json', 'lane-routing-registry.yaml'):
    shutil.copy2(ROOT / 'config' / (name + '.bak-far-remediation-20261016'), before / 'config' / name)
REPORT['states'] = {}
for name, base in [('before', before), ('after', SUB)]:
    registry = policy.load_registry(base / 'config/lane-routing-registry.yaml')
    site = read_json(base / 'config/model-lane-assignment.json')
    findings = policy.check_drift(base / 'config/lane-routing-registry.yaml', root=base, registry=registry)
    REPORT['states'][name] = {'epoch': registry['epoch'], 'revision': site['revision'], 'source_of_routes': registry['source_of_routes'], 'site_sha256': digest(base / 'config/model-lane-assignment.json'), 'routes': registry['routes'], 'lane_chains': site.get('lane_chains'), 'sod': site.get('sod'), 'fatal_findings': [finding for finding in findings if finding['severity'] == 'error']}
    environment = dict(os.environ, HGK_LANE_POLICY_SOURCE_ROOT=str(base))
    run('shape_' + name, [sys.executable, '-B', '-m', 'unittest', 'tests.test_lane_policy.TestLanePolicyConformance.test_registry_and_projection_shape', '-v'], env=environment)
    run('declarations_' + name, [sys.executable, '-B', str(ROUND / 'check_declaration_agreement.py'), str(base / 'config/model-lane-assignment.json'), name])
receipt = read_json(ROUND / 'R2_PROMOTION_RECEIPT.json')
candidate = ROOT / 'var/LANE-RELIABILITY-CLOSURE-20261016/candidate'
REPORT['promotion'] = []
for item in receipt['files']:
    relative = item['rel']
    REPORT['promotion'].append({'rel': relative, 'canonical': digest(ROOT / relative), 'candidate': digest(candidate / relative), 'reference_copy': digest(SUB / relative), 'receipt': item['candidate_sha256']})
REPORT['candidate_configs'] = {'epoch': policy.load_registry(candidate / 'config/lane-routing-registry.yaml')['epoch'], 'revision': read_json(candidate / 'config/model-lane-assignment.json')['revision'], 'config_digests': {name: {'canonical': digest(ROOT / 'config' / name), 'candidate': digest(candidate / 'config' / name)} for name in ('model-lane-assignment.json', 'lane-routing-registry.yaml')}}
REPORT['candidate_comparison'] = []
for directory in ('scripts', 'src', 'tests', 'config'):
    for path in sorted((candidate / directory).rglob('*')):
        if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc':
            relative = path.relative_to(candidate)
            canonical = ROOT / relative
            if not canonical.is_file() or digest(path) != digest(canonical):
                REPORT['candidate_comparison'].append(str(relative))
save()
run('lane_guard_after', [sys.executable, '-B', '-m', 'unittest', 'tests.test_lane_guard', '-v'])
run('whole_after', [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-t', '.', '-v'])
pre_tree = OUT / 'pre_tree'
shutil.copytree(SUB, pre_tree, dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', 'var', 'TEST_RESULTS'))
for name in ('model-lane-assignment.json', 'lane-routing-registry.yaml'):
    shutil.copy2(before / 'config' / name, pre_tree / 'config' / name)
run('whole_before', [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-t', '.', '-v'], cwd=pre_tree)
REPORT['recorded_whole'] = {}
for state in ('PRE', 'POST'):
    text = (ROUND / 'evidence' / ('WHOLE_TREE_' + state + '.txt')).read_text(encoding='utf-8-sig')
    REPORT['recorded_whole'][state] = {'names': re.findall(r'^(?:FAIL|ERROR): (.+)$', text, re.M), 'ran': re.findall(r'^Ran .+$', text, re.M), 'status': re.findall(r'^(?:FAILED|OK).*$', text, re.M)}
save()
print('COMPLETE', flush=True)
