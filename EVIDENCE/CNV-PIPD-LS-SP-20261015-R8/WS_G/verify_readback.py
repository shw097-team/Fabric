import json,hashlib,datetime,subprocess,os,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
path=OUT/'GSTACK_R8_ROLEMAP.json'
doc=json.loads(path.read_text(encoding='utf-8'))
records=json.loads((OUT/'commands.json').read_text(encoding='utf-8'))
by={r['id']:r for r in records}
roles=doc['roles']
assert len(roles)==19 and len({r['role'] for r in roles})==19
assert sum(r['status']=='ROLE_KEYED' for r in roles)==7
assert sum(r['status']=='MAP_ROLE_ABSENT' for r in roles)==12
assert all(r['route_slot']['provider'] is None and r['route_slot']['model'] is None for r in roles)
assert all(r['named_method']['line'] and r['named_method']['source_quote'] for r in roles if r['named_method']['exists'])
assert by['existing-probe-positive']['exit_code']==0
assert by['existing-probe-negative']['exit_code']==0
assert by['probe-in-memory-negative-control']['exit_code']==1
assert by['probe-positive-assertion-boundary']['exit_code']==0
assert doc['sod']['model_axis_PLAN_VERIFY']['independent'] is False
assert not doc['runtime_assert']['tracked']
assert doc['subject_git_status_unchanged']
assert len(doc['registry_drift_receipt']['findings'])==1
assert doc['registry_drift_receipt']['findings'][0]['pointer']=='/codex_sha256'
checks=[]
for item in doc['input_fingerprints']:
    p=Path(item['path'])
    h=hashlib.sha256(p.read_bytes()).hexdigest()
    checks.append({'path':str(p),'same_sha256':h==item['sha256'],'observed_sha256':h})
assert all(c['same_sha256'] for c in checks), 'input changed during readback'
# Exact preserved source text readback against the still-current tree (line numbers were added by the collector).
source_checks=[]
for r in records:
    if r['id'].startswith('source:'):
        p=Path(doc['repo'])/r['id'][7:]
        captured=r['stdout'].splitlines()[1:]
        current=p.read_text(encoding='utf-8').splitlines()
        # print() contributes a final terminator; only a source that already
        # ended in newline leaves an extra empty frame line in splitlines().
        if captured and captured[-1] == '':
            captured = captured[:-1]
        for i, line in enumerate(captured, 1):
            assert line.startswith(str(i)+': '), 'invalid numbered capture frame'
        assert [line.split(': ',1)[1] for line in captured]==current
        source_checks.append(str(p))
receipt=(OUT/'GSTACK_R8_RECEIPT.md').read_text(encoding='utf-8')
assert all('### '+r['id'] in receipt and r['stdout'] in receipt and (not r['stderr'] or r['stderr'] in receipt) for r in records)
# Read-only git verification, no lock writes.
cmd=['git','-C',doc['repo'],'-c','core.quotepath=false','status','--porcelain','--untracked-files=normal']
p=subprocess.run(cmd,capture_output=True,encoding='utf-8',env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
assert p.returncode==0 and p.stdout==by['git-status-before']['stdout']
result={'schema':'GSTACK-R8-READBACK-VERIFICATION/1','claim_ceiling':'LOCAL_CANDIDATE_READBACK_INTEGRITY_ONLY_NOT_ACCEPTANCE','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks_completed':True,'roles':len(roles),'counts':doc['counts'],'all_recorded_stdout_stderr_present_in_receipt':True,'input_fingerprints_unchanged':checks,'source_line_readbacks_match_current_files':source_checks,'json_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'json_size':path.stat().st_size,'git_status_command':subprocess.list2cmdline(cmd),'git_status_stdout':p.stdout,'git_status_stderr':p.stderr,'git_status_exit_code':p.returncode,'git_status_unchanged':True,'verification_command':'python -B '+str(Path(__file__).resolve()),'expected_verification_exit_code':0}
render=json.dumps(result,ensure_ascii=False,indent=2)
(OUT/'verification.json').write_text(render+'\n',encoding='utf-8')
with (OUT/'GSTACK_R8_RECEIPT.md').open('a',encoding='utf-8') as f:
    f.write('\n## Post-build readback verification\n\nCommand: `'+result['verification_command']+'` (CWD C:/Users/user). stdout follows; stderr empty; successful completion exits 0. Assertions concern evidence integrity only, not subject acceptance.\n\n```json\n'+render+'\n```\n')
print(render)
