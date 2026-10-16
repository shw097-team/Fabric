import hashlib
import importlib.util
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
result = {}
sys.path.insert(0, str(SUB / 'src'))
from hg_kseos import lane_policy as policy

spec = importlib.util.spec_from_file_location('detector', ROUND / 'check_declaration_agreement.py')
detector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(detector)
old = json.loads((OUT / 'before/config/model-lane-assignment.json').read_text(encoding='utf-8'))
result['SC4'] = []
for pointer in detector.SINGLE:
    text = detector.get(old, pointer)
    buggy = next((token for token in detector.MODELS if token in text), None)
    result['SC4'].append({'pointer': pointer, 'text': text, 'old_parser': buggy, 'fixed_parser': detector.claimed_default(text)[0]})

registry = policy.load_registry(SUB / 'config/lane-routing-registry.yaml')
site = json.loads((SUB / 'config/model-lane-assignment.json').read_text(encoding='utf-8'))
result['routes'] = [{'lane': route['lane'], 'provider': route['provider'], 'model': route['model'], 'reasoning_effort': route.get('reasoning_effort'), 'auth': route.get('auth'), 'oauth': route.get('oauth'), 'fallback': route.get('fallback'), 'fallbacks': route.get('fallbacks'), 'arms': route.get('arms')} for route in registry['routes']]
result['site_chains'] = site['lane_chains']
result['site_sod'] = site['sod']
result['pins'] = {'source_of_routes': registry['source_of_routes'], 'site_revision': site['revision'], 'site_registry_epoch': site['registry_epoch'], 'sha256': hashlib.sha256((SUB / 'config/model-lane-assignment.json').read_bytes()).hexdigest()}

intermediate = OUT / 'incomplete_tree'
shutil.copytree(SUB, intermediate, dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', 'var', 'TEST_RESULTS'))
site['revision'] = 20
site['registry_epoch'] = 20
site_path = intermediate / 'config/model-lane-assignment.json'
site_path.write_text(json.dumps(site, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
text = (SUB / 'config/lane-routing-registry.yaml').read_text(encoding='utf-8')
text = re.sub(r'(?m)^source_of_routes:\n(?:  [^\n]*\n)*', 'source_of_routes:\n  path: config/model-lane-assignment.json\n  revision: 20\n  sha256: d41f8f8bff41d4338a4b85dab7a60bd2c9c23b2f5f39c8c008e89bf82587bd36\n', text, count=1)
text = text.replace('{pointer: /registry_epoch, expected: 21}', '{pointer: /registry_epoch, expected: 20}').replace('{pointer: /revision, expected: 21}', '{pointer: /revision, expected: 20}')
text = re.sub(r'    note: canonical policy revision 21[^\n]*', '    note: canonical policy revision 19 (owner PLAN rebind 2026-10-15) — PLAN rank-1 is opencode-go/glm-5.3-flash and the GPT arm is a non-default alternate; additional EXECUTE route is operator-selectable only; VERIFY arm selection is owner-adjudicated.', text)
reg_path = intermediate / 'config/lane-routing-registry.yaml'
reg_path.write_text(text, encoding='utf-8')
result['SC1_reconstructed'] = {'site_sha256': hashlib.sha256(site_path.read_bytes()).hexdigest(), 'registry_sha256': hashlib.sha256(reg_path.read_bytes()).hexdigest()}
receipt = json.loads((ROUND / 'R1_R3_COMPLETION_RECEIPT.json').read_text())
result['SC1_reconstructed']['matches_recorded_before'] = result['SC1_reconstructed']['site_sha256'] == receipt['site_sha_before'] and result['SC1_reconstructed']['registry_sha256'] == receipt['registry_sha_before']
environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', HGK_LANE_SCRATCH=str(OUT / 'scratch_incomplete'))
command = [sys.executable, '-B', '-m', 'unittest', 'tests.test_lane_guard', 'tests.test_lane_policy', '-v']
execution = subprocess.run(command, cwd=intermediate, env=environment, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=300)
raw = execution.stdout + execution.stderr
(OUT / 'SC1_incomplete.txt').write_text(raw, encoding='utf-8')
result['SC1_reconstructed'].update({'exit': execution.returncode, 'names': re.findall(r'^(?:FAIL|ERROR): (.+)$', raw, re.M), 'status': re.findall(r'^(?:Ran |FAILED|OK).*$', raw, re.M)})
result['SC1_reconstructed']['drift'] = policy.check_drift(reg_path, root=intermediate)

result['R5'] = {'canonical_flag': '--turn-shape' in (ROOT / 'scripts/hgk-lane-dispatch.py').read_text(encoding='utf-8'), 'copy_flag': '--turn-shape' in (SUB / 'scripts/hgk-lane-dispatch.py').read_text(encoding='utf-8'), 'mentions': []}
for path in sorted(ROUND.glob('*')):
    if path.is_file() and path.suffix in ('.md', '.json'):
        for number, line in enumerate(path.read_text(encoding='utf-8-sig').splitlines(), 1):
            if re.search('turn.shape|R5.*(LANDED|DELIVER|完成|未|landed)|NOT LANDED', line):
                result['R5']['mentions'].append({'path': path.name, 'line': number, 'text': line[:1500]})
result['promoter_source'] = (ROUND / 'apply_R2_promote.py').read_text(encoding='utf-8')
(OUT / 'details.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps({'SC1_reconstructed': result['SC1_reconstructed'], 'routes': result['routes'], 'site_chains': result['site_chains'], 'site_sod': result['site_sod']}, indent=2, ensure_ascii=False))
