import os, sys, subprocess, json
from pathlib import Path
W=Path(__file__).parent
os.environ.update(PYTHONDONTWRITEBYTECODE='1',PYTHONIOENCODING='utf-8',TMP=str(W),TEMP=str(W),TMPDIR=str(W))
PY='C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe'
H=Path('C:/Projects/Agent_Workspace/PIPD/worktrees/r8-wt')
C=Path('C:/Projects/wt-r8-cleanmain')
K=Path('C:/Projects/Agent_Workspace/HG-KSEOS')
log=[]
def emit(s):
 print(s,flush=True); log.append(s)
def run(args,cwd):
 emit('\n$ '+subprocess.list2cmdline(args)+'\nCWD='+str(cwd))
 p=subprocess.run(args,cwd=cwd,env=os.environ,capture_output=True,text=True,encoding='utf-8',errors='replace')
 emit('STDOUT:\n'+p.stdout+'\nSTDERR:\n'+p.stderr+'\nEXIT='+str(p.returncode))
 return {'argv':args,'cwd':str(cwd),'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
def excerpt(p,start,end):
 emit('\nSOURCE '+str(p))
 lines=p.read_text(encoding='utf-8').splitlines()
 emit('\n'.join(f'{i}|{lines[i-1]}' for i in range(start,min(end,len(lines))+1)))
res={}
for tag,root in [('hardened',H),('clean',C)]:
 res[tag+'_status']=run(['git','--no-optional-locks','status','--short'],root)
 res[tag+'_head']=run(['git','rev-parse','HEAD'],root)
res['diff']=run(['git','diff','--numstat'],H)
res['patch']=run(['git','diff','--','src/pipd_ls_sp/validate.py','src/pipd_ls_sp/pipeline.py','src/pipd_ls_sp/cli.py'],H)
for root in (C,H):
 excerpt(root/'src/pipd_ls_sp/validate.py',1,35)
 excerpt(root/'src/pipd_ls_sp/validate.py',205,460)
 excerpt(root/'src/pipd_ls_sp/pipeline.py',185,245)
 excerpt(root/'src/pipd_ls_sp/cli.py',150,190)
excerpt(H/'tests/test_s4ext_trace_closure.py',80,116)
excerpt(H/'tests/test_tooling_executes.py',59,76)
res['smoke_test']=run([PY,'-B','-m','pytest','-p','no:cacheprovider','--basetemp',str(W/'pytest_temp'),'tests/test_tooling_executes.py::TestToolingExecutes::test_cli_smoke_runs','-vv','--tb=long'],H)
res['crash_repro']=run([PY,'-B','C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8/WS_B/repro_frozen_crash.py'],H)
# No git write command is allowed: invoke unchanged test method with an already initialized read-only repo.
code="import sys; from pathlib import Path; sys.path.insert(0,'tests'); import test_s4ext_trace_closure as t; t._init_git_repo=lambda p: None; t.LegalTraceStillPassesTests.setUpClass=classmethod(lambda cls: (setattr(cls,'repo',Path('C:/Projects/wt-r8-cleanmain')),setattr(cls,'bundle',t._bundle(cls.repo)))); import pytest; raise SystemExit(pytest.main(['-p','no:cacheprovider','--basetemp',r'"+str(W/'pytest_trace_temp')+"','tests/test_s4ext_trace_closure.py::LegalTraceStillPassesTests::test_real_trace_link_is_legal_beside_its_endpoints','-vv','--tb=long']))"
# pytest imports same test module from tests directory, preserving the patched setup; no temp cleanup member is needed.
code=code.replace("import pytest;", "t.LegalTraceStillPassesTests.tearDownClass=classmethod(lambda cls: None); import pytest;")
res['trace_test_fixture_readonly']=run([PY,'-B','-c',code],H)
D=K/'scripts/hgk-lane-dispatch.py'
lines=D.read_text(encoding='utf-8').splitlines()
for a,b in [(1015,1075),(1140,1350),(1350,1470)]: excerpt(D,a,b)
R=Path('C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8')
files=sorted(set(R.rglob('*receipt*.json'))|set(R.rglob('*attempts*.ndjson'))|set((R/'R8_VERIFY').rglob('*.json')))
fields=['ok','code','required_arm','served_arm','used_rank','used_transport_model','usage_receipt_ok','nonce_present','nonce_absent_arms']
receipts=[]
def walk(obj,pointer=''):
 if isinstance(obj,dict):
  if any(k in obj for k in fields):
   yield {'pointer':pointer,'fields':{k:obj[k] if k in obj else '<ABSENT>' for k in fields},'identity_fields':{k:v for k,v in obj.items() if k in ('provider','model','rank','arm','transport_model','canonical_identity','lane','attempt','attempt_id')}}
  for k,v in obj.items(): yield from walk(v,pointer+'/'+str(k))
 elif isinstance(obj,list):
  for i,v in enumerate(obj): yield from walk(v,pointer+'/'+str(i))
for p in files:
 try:
  txt=p.read_text(encoding='utf-8-sig')
  objs=[json.loads(l) for l in txt.splitlines() if l.strip()] if p.suffix=='.ndjson' else [json.loads(txt)]
  rows=list(walk(objs))
  row={'file':str(p),'rows':rows};receipts.append(row)
  emit('\nRECEIPT_ARM_FIELDS '+json.dumps(row,ensure_ascii=False,indent=2))
 except Exception as e: emit('RECEIPT_ERROR '+str(p)+' '+repr(e))
res['receipts']=receipts
for p in (K/'config/lane-routing-registry.yaml', K/'config/model-lane-assignment.json'): excerpt(p,1,10000)
# Read the drift implementation before invoking it, to confirm it only reads.
res['drift_source']=run([PY,'-B','-c',"import sys,inspect;sys.path.insert(0,'src');from hg_kseos.lane_policy import check_drift,load_registry;print(inspect.getsource(load_registry));print(inspect.getsource(check_drift))"],K)
(W/'measure_raw.log').write_text('\n'.join(log),encoding='utf-8')
(W/'measure_results.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8')
