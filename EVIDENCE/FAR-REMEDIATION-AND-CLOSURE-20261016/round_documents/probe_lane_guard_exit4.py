"""Why did R1/R3 turn 4 lane_guard cases from exit 3 into exit 4? Ask the guard directly."""
import importlib.util
import json
import pathlib
import tempfile

ROOT = pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS')


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


guard = load('hgk_lane_guard', ROOT / 'scripts' / 'hgk-lane-guard.py')
lp = load('lane_policy_mod', ROOT / 'src' / 'hg_kseos' / 'lane_policy.py')

tmp = pathlib.Path(tempfile.mkdtemp())
ver = tmp / 'verify.json'
ver.write_text(json.dumps({
    'schema': 'CONTROL-FIXTURE-NOT-A-REAL-ADMISSION', 'status': 'ADMITTED',
    'arm': {'engine': 'hermes', 'model': 'glm-5.3-flash', 'provider': 'opencode-go'},
    'served': {'engine': 'hermes', 'model': 'glm-5.3-flash', 'provider': 'opencode-go'}}), encoding='utf-8')

argv = ['--lane', 'VERIFY_SECURITY', '--maker-engine', 'opencode-go', '--maker-model',
        'deepseek-v4.1-flash', '--target-engine', 'hermes', '--target-model', 'glm-5.3-flash',
        '--target-provider', 'opencode-go', '--admission', str(ver)]
v = guard.evaluate(guard.build_parser().parse_args(argv))
print('exit_code =', v['exit_code'], '| status =', v.get('status'))
print('errors    =', json.dumps(v.get('errors'), ensure_ascii=False))
for c in v.get('checks', []):
    print('  check %-28s ok=%-5s %s' % (c.get('id'), c.get('ok'), str(c.get('detail'))[:150]))
print()
reg = lp.load_registry()
sor = reg.get('source_of_routes', {})
print('source_of_routes =', json.dumps(sor, ensure_ascii=False)[:400])
p = sor.get('path')
if p:
    live = (ROOT / p) if not pathlib.Path(p).is_absolute() else pathlib.Path(p)
    print('live source exists =', live.is_file(), '| live digest =', lp._sha256_file(live) if live.is_file() else None)
print('registry epoch =', reg.get('epoch'))
site = lp.load_site(ROOT / 'config' / 'model-lane-assignment.json')
print('site revision =', site.get('revision'), '| registry_epoch field =', site.get('registry_epoch'))
