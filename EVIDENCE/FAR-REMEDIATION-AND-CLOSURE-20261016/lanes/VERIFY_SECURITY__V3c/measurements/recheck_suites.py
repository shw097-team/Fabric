import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

WORK = Path(__file__).resolve().parent.parent
OUT = WORK / 'TEST_RESULTS'
result = {}
pre = WORK / 'pre'
shutil.copytree(WORK / 'subject', pre, dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', 'var', 'TEST_RESULTS'))
for name in ('model-lane-assignment.json', 'lane-routing-registry.yaml'):
    shutil.copy2(OUT / 'before/config' / name, pre / 'config' / name)
for label, base in [('after', WORK / 'subject'), ('before', pre)]:
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONPATH=os.pathsep.join([str(base / 'src'), str(base / 'scripts')]), HGK_LANE_SCRATCH=str(OUT / ('scratch_' + label)))
    command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-t', '.', '-v']
    execution = subprocess.run(command, cwd=base, env=environment, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=600)
    raw = execution.stdout + execution.stderr
    (OUT / ('whole_with_path_' + label + '.txt')).write_text(raw, encoding='utf-8')
    result[label] = {'command': command, 'cwd': str(base), 'PYTHONPATH': environment['PYTHONPATH'], 'exit': execution.returncode, 'names': re.findall(r'^(?:FAIL|ERROR): (.+)$', raw, re.M), 'status': re.findall(r'^(?:Ran |FAILED|OK).*$', raw, re.M)}
    (OUT / 'whole_with_path.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(label, json.dumps(result[label]), flush=True)
