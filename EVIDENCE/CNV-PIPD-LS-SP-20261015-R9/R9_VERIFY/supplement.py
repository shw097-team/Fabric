import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

OUT = Path(__file__).resolve().parent
BASE = Path('C:/Projects/Agent_Workspace')
ROUND = OUT.parent
PY = 'C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe'
HERMES = Path('C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes')
LIVE = HERMES / 'skills/software-development/hgk-governed-execution'
tempfile.tempdir = str(OUT / 'tmp')
os.environ.update(TEMP=tempfile.tempdir, TMP=tempfile.tempdir, TMPDIR=tempfile.tempdir, PYTHONDONTWRITEBYTECODE='1')
DATA = {}

def run(name, command, cwd=OUT):
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    record = dict(command=command, cwd=str(cwd), exit=result.returncode, stdout=result.stdout, stderr=result.stderr)
    (OUT / (name + '.json')).write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    DATA[name] = record
    print(name, result.returncode, result.stdout[-900:], result.stderr[-1800:], flush=True)

run('named_tests_confined', [PY, '-B', str(OUT / 'safe_tests.py')], BASE / 'PIPD/worktrees/r8-wt')
run('adapted_fixture_tests', [PY, '-B', '-c', "import runpy; source=open(r'" + str(OUT / 'safe_tests.py') + "',encoding='utf-8').read(); source=source.replace('suite = unittest.TestSuite([',\"def filesystem_fixture(path):\\n    path.mkdir(parents=True, exist_ok=True)\\n    (path / 'README.md').write_text('seed\\\\n', encoding='utf-8')\\nmodules[0]._init_git_repo = filesystem_fixture\\nsuite = unittest.TestSuite([\"); exec(compile(source,r'" + str(OUT / 'safe_tests.py') + "','exec'),{'__file__':r'" + str(OUT / 'safe_tests.py') + "','__name__':'__main__'})"], BASE / 'PIPD/worktrees/r8-wt')
receipt_path = ROUND / 'WS_B/APPLY_RECEIPT.json'
receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
rows = []
for entry in receipt['paths']:
    path = LIVE / entry['path']
    actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
    expected = entry.get('after_sha256')
    rows.append(dict(path=entry['path'], actual=actual, recorded_after=expected, match=(actual == expected) if expected else None))
DATA['apply_receipt_comparison'] = dict(path=str(receipt_path), applied=receipt['applied'], src=receipt['src'], recorded_dst_files_total=receipt['dst_files_total'], actual_dst_files_total=len([path for path in LIVE.rglob('*') if path.is_file()]), rows=rows)
preimage = ROUND / 'WS_B/preimage/SKILL.md'
DATA['preimage'] = dict(path=str(preimage), exists=preimage.exists(), bytes=preimage.stat().st_size if preimage.exists() else None, sha256=hashlib.sha256(preimage.read_bytes()).hexdigest() if preimage.exists() else None)
refs = [path for path in (LIVE / 'references').rglob('*') if path.is_file()]
DATA['reference_counts'] = dict(all_files=len(refs), excluding_pycache=len([path for path in refs if '__pycache__' not in str(path)]), markdown=len([path for path in refs if path.suffix == '.md']), excluded_pycache=[str(path.relative_to(LIVE)) for path in refs if '__pycache__' in str(path)])
DATA['tree_comparison'] = []
candidate = ROUND / 'CANDIDATE_V2'
for path in sorted(candidate.rglob('*')):
    if path.is_file():
        relative = path.relative_to(candidate)
        counterpart = LIVE / relative
        if not counterpart.is_file() or counterpart.read_bytes() != path.read_bytes():
            DATA['tree_comparison'].append(dict(relative=str(relative), live_exists=counterpart.is_file()))
DATA['candidate_file_count'] = len([path for path in candidate.rglob('*') if path.is_file()])
pkg = HERMES / 'attachments/Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md'
lines = pkg.read_text(encoding='utf-8').splitlines()
DATA['rq06_quote'] = [dict(line=index+1, text=line) for index, line in enumerate(lines) if 1585 <= index+1 <= 1600 or 55875 <= index+1 <= 55890]
lanes = BASE / '_handover/CNV-PIPD-LS-SP-20261015/lane_runs'
DATA['receipt_summary'] = []
code_by_stdout = {}
for path in sorted(lanes.glob('*dispatch_receipt*.json')):
    receipt = json.loads(path.read_text(encoding='utf-8-sig'))
    attempts = receipt.get('attempts', [])
    for attempt in attempts:
        code_by_stdout[attempt.get('stdout_path')] = receipt.get('code')
    DATA['receipt_summary'].append(dict(path=str(path), code=receipt.get('code'), attempts=[{field:attempt.get(field) for field in ('rank','provider','model','exit','seconds','nonce_present','attempt_log_dir','usage_provider','usage_model','usage_receipt_ok')} for attempt in attempts]))
DATA['attempt_history'] = []
for path in sorted(lanes.glob('*.ndjson')):
    for line_number, line in enumerate(path.read_text(encoding='utf-8-sig').splitlines(), 1):
        row = json.loads(line)
        record = {field:row.get(field) for field in ('at_utc','run_id','lane','rank','provider','model','exit','seconds','nonce_present','attempt_log_dir','usage_provider','usage_model','usage_receipt_ok')}
        record.update(path=str(path), line=line_number, code=code_by_stdout.get(row.get('stdout_path')))
        record['code_status'] = 'CURRENT_FINAL_RECEIPT_MATCH' if record['code'] else 'FINAL_RECEIPT_NOT_AVAILABLE_FOR_HISTORICAL_RUN'
        DATA['attempt_history'].append(record)
DATA['dispatch_pin_lines'] = {}
for path in [ROUND / 'dispatch_r9.py', BASE / '_handover/CNV-PIPD-LS-SP-20261015/dispatch_r6.py']:
    DATA['dispatch_pin_lines'][str(path)] = [dict(line=number, text=line) for number,line in enumerate(path.read_text(encoding='utf-8').splitlines(),1) if '--force-rank' in line or '--require-arm' in line or 'round_name =' in line]
DATA['r9_markers'] = [dict(path=str(path), record=json.loads(path.read_text(encoding='utf-8-sig'))) for path in lanes.glob('CNV-PIPD-LS-SP-20261015-R9/**/attempt.marker.json')]
far = BASE / 'Fabric/fabric-autonomous-research/runs/FAR-20261016-012-r9-residual-closure'
with (far / 'ResearchSourceDenominator.tsv').open(encoding='utf-8-sig', newline='') as stream:
    source_rows = list(csv.DictReader(stream, delimiter='\t'))
DATA['source_locator_checks'] = []
for row in source_rows:
    locator = row['identity_locator']
    if locator.startswith('attachments/'):
        paths = [HERMES / locator]
    elif row['source_id'] == 'SRC-08':
        paths = list(lanes.glob('*dispatch_receipt*.json'))
    elif row['source_id'] == 'SRC-09':
        paths = [BASE / 'PIPD/worktrees/r8-wt', Path('C:/Projects/wt-r8-cleanmain')]
    elif row['source_id'] == 'SRC-10':
        paths = [BASE / 'HG-KSEOS/config' / name for name in ['lane-routing-registry.yaml','lane-route-slots.candidate.json','model-lane-assignment.json']]
    elif row['source_id'] == 'SRC-11':
        paths = list((BASE / 'Fabric/fabric-autonomous-research/runs').glob('FAR-20261015-01[01]*'))
    elif row['source_id'] == 'SRC-12':
        paths = [BASE / 'Fabric/FABRIC/fabric-autonomous-research' / name for name in ['governance','research-product']]
    elif row['source_id'] == 'SRC-13':
        paths = [BASE / 'HG-KSEOS/var/SKILL-CONVERGENCE-20261014/candidates/hgk/skill', BASE / '_handover/...-R8/ws_a_skill_slim_regression.py']
    else:
        paths = [BASE / locator]
    DATA['source_locator_checks'].append(dict(source_id=row['source_id'], recorded_locator=locator, resolved_paths=[dict(path=str(path), exists=path.exists()) for path in paths], empty_resolution=not paths))
DATA['boundary_incident'] = dict(code='CHECKER_TEMP_WRITE_BOUNDARY_BREACH', observed_from='named_tests.json stderr', known_external_fixture='C:/Users/user/AppData/Local/Temp/tmp3eedulc6/repo', currently_exists=Path('C:/Users/user/AppData/Local/Temp/tmp3eedulc6').exists(), explanation='First named-test run initialized its fixtures under the interpreter default TEMP rather than R9_VERIFY/tmp. The trace fixture created its repo directory before the git-init call was blocked; the CLI smoke test also used the default temporary root. Those automatic temporary writes breached the requested write boundary. No Git write command was executed. Subsequent safe_tests.py forces tempfile.tempdir to R9_VERIFY/tmp. This verifier cannot claim full procedural compliance.')
(OUT / 'supplement.json').write_text(json.dumps(DATA, ensure_ascii=False, indent=2), encoding='utf-8')
print('SAVED supplement.json', flush=True)
