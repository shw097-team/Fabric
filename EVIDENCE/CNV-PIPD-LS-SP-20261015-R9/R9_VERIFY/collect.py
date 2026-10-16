import csv
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

OUT = Path(__file__).resolve().parent
BASE = Path('C:/Projects/Agent_Workspace')
ROUND = BASE / '_handover/CNV-PIPD-LS-SP-20261015-R9'
PIPD = BASE / 'PIPD/worktrees/r8-wt'
PY = 'C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe'
HERMES = Path('C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes')
LIVE = HERMES / 'skills/software-development/hgk-governed-execution'
TEMP = OUT / 'tmp'
TEMP.mkdir(exist_ok=True)
os.environ.update(PYTHONDONTWRITEBYTECODE='1', TEMP=str(TEMP), TMP=str(TEMP), PYTEST_ADDOPTS='-p no:cacheprovider')
DATA = {}

def save(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')

def run(name, command, cwd=OUT, extra=None):
    env = dict(os.environ)
    env.update(extra or {})
    result = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, encoding='utf-8', errors='replace')
    row = dict(command=command, cwd=str(cwd), exit=result.returncode, stdout=result.stdout, stderr=result.stderr)
    save(name + '.json', row)
    print(name, 'exit=', result.returncode, result.stdout[-1200:], result.stderr[-500:], flush=True)
    return row

DATA['git_names'] = run('git_names', ['git', '-C', str(PIPD), 'diff', '--name-status', 'dba4b19456777d3b597fdf71480f6423dd974243'])
DATA['git_diff'] = run('git_diff', ['git', '-C', str(PIPD), 'diff', 'dba4b19456777d3b597fdf71480f6423dd974243', '--', 'src/pipd_ls_sp/validate.py'])
text = (PIPD / 'src/pipd_ls_sp/validate.py').read_text(encoding='utf-8')
DATA['guard_lines'] = [{'line': number, 'text': line} for number, line in enumerate(text.splitlines(), 1) if 388 <= number <= 424 or 454 <= number <= 470]
DATA['guard_search'] = run('guard_search', ['rg', '-n', 'R9-0|BLK-R8-WS2', str(PIPD / 'src')])
DATA['tests'] = run('named_tests', [PY, '-B', str(OUT / 'safe_tests.py')], PIPD)
runner = BASE / '_handover/CNV-PIPD-LS-SP-20261015-R8/WS_B/RUNNERS/probe_mutations.py'
DATA['mutations'] = run('mutation_probes', [PY, '-B', '-c', "import importlib.util; from pathlib import Path; spec=importlib.util.spec_from_file_location('probe',r'" + str(runner) + "'); module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); module.SRC=Path(r'" + str(OUT / 'probe_source.md') + "'); codes=[module.m04_profile_downgrade(),module.m06_domain_oracle_expected(),module.m16_trace_digest_mismatch()]; raise SystemExit(max(codes))"])
harness = BASE / '_handover/CNV-PIPD-LS-SP-20261015-R8/ws_a_skill_slim_regression.py'
DATA['harness'] = run('harness_run', [PY, '-B', str(harness), '--subject', str(ROUND / 'CANDIDATE_V2'), '--live', str(LIVE), '--out', str(OUT / 'harness_v2_yourrun.json')])
skill = LIVE / 'SKILL.md'
reference = LIVE / 'references/product-branch-write-set-gates.md'
def digest(path):
    body = path.read_bytes()
    return dict(path=str(path), bytes=len(body), sha256=hashlib.sha256(body).hexdigest())
DATA['live'] = dict(skill=digest(skill), references_count=len([path for path in (LIVE / 'references').rglob('*') if path.is_file()]), target_reference=digest(reference) if reference.is_file() else None, candidate_skill=digest(ROUND / 'CANDIDATE_V2/SKILL.md'), candidate_matches_live=(skill.read_bytes() == (ROUND / 'CANDIDATE_V2/SKILL.md').read_bytes()), ws_b2_exists=(ROUND / 'WS_B2').exists())
DATA['live']['ws_b2_receipt_names_only'] = [str(path) for path in (ROUND / 'WS_B2').rglob('*') if path.is_file() and 'receipt' in path.name.lower()] if (ROUND / 'WS_B2').exists() else []
pkg = HERMES / 'attachments/Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md'
pkg_lines = pkg.read_text(encoding='utf-8').splitlines()
DATA['pkg'] = digest(pkg)
DATA['pkg']['approved_matches'] = DATA['pkg']['sha256'] == '96d9d564286743e17550ccef15b9952347901eb77168f930376938893cff9c3f'
DATA['pkg']['size_literals'] = [dict(line=number, text=line) for number, line in enumerate(pkg_lines, 1) if re.search(r'100[,_]?000', line)]
rq_lines = {index for index, line in enumerate(pkg_lines) if 'ACC-RQ06' in line}
indices = sorted({index for match in rq_lines for index in range(max(0, match-2), min(len(pkg_lines), match+8))})
DATA['pkg']['acc_rq06_context'] = [dict(line=index+1, text=pkg_lines[index]) for index in indices]
registry_code = "import json; from hg_kseos import lane_policy; reg=lane_policy.load_registry(); print(json.dumps({'registry_path':str(lane_policy.DEFAULT_REGISTRY),'drift':lane_policy.check_drift(registry=reg),'routes':reg.get('routes'),'route_keys':list(reg)},ensure_ascii=False,indent=2))"
DATA['registry'] = run('registry_drift', [str(BASE / 'HG-KSEOS/.venv/Scripts/python.exe'), '-B', '-c', registry_code], BASE / 'HG-KSEOS', {'PYTHONPATH':'src'})
far_requested = BASE / 'Fabric/FABRIC/fabric-autonomous-research/runs/FAR-20261016-012-r9-residual-closure'
far = BASE / 'Fabric/fabric-autonomous-research/runs/FAR-20261016-012-r9-residual-closure'
DATA['far'] = dict(requested_path=str(far_requested), requested_exists=far_requested.exists(), discovered_path=str(far), discovered_exists=far.exists())
if far.exists():
    DATA['far']['inventory'] = [dict(path=str(path), bytes=path.stat().st_size) for path in sorted(far.rglob('*')) if path.is_file()]
    def table(path):
        with path.open(encoding='utf-8-sig', newline='') as stream:
            reader = csv.DictReader(stream, delimiter='\t')
            return dict(headers=reader.fieldnames, rows=list(reader))
    DATA['far']['claims'] = table(far / 'ClaimLedger.tsv')
    DATA['far']['sources'] = table(far / 'ResearchSourceDenominator.tsv')
    DATA['far']['snapshots'] = table(far / 'SourceSnapshotLedger.tsv')
    DATA['far']['evidence_ref_fields'] = [header for header in DATA['far']['claims']['headers'] if 'evidence_ref' in header]
    sources = {row['source_id'] for row in DATA['far']['sources']['rows']}
    DATA['far']['source_id_resolution'] = [dict(claim=row['claim_id'], source=source.strip(), exists_in_denominator=source.strip() in sources) for row in DATA['far']['claims']['rows'] for field in ('support_source_ids','counter_source_ids') for source in row.get(field,'').split(',') if source.strip()]
lanes = BASE / '_handover/CNV-PIPD-LS-SP-20261015/lane_runs'
DATA['receipts'] = []
for path in sorted(lanes.rglob('*.json')):
    if 'receipt' not in path.name.lower() and path.name != 'attempt.marker.json':
        continue
    receipt = json.loads(path.read_text(encoding='utf-8-sig'))
    DATA['receipts'].append(dict(path=str(path), receipt=receipt))
save('measurements.json', DATA)
print('SAVED', OUT / 'measurements.json', flush=True)
