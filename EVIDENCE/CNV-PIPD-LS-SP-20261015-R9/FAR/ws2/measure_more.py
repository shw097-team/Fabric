import os,sys,json,subprocess
from pathlib import Path
W=Path(__file__).parent
H=Path('C:/Projects/Agent_Workspace/PIPD/worktrees/r8-wt');C=Path('C:/Projects/wt-r8-cleanmain');K=Path('C:/Projects/Agent_Workspace/HG-KSEOS')
PY='C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe'
os.environ.update(PYTHONDONTWRITEBYTECODE='1',PYTHONIOENCODING='utf-8',TMP=str(W),TEMP=str(W),TMPDIR=str(W))
log=[];result={}
def emit(s): print(s,flush=True);log.append(s)
def run(tag,args,cwd):
 p=subprocess.run(args,cwd=cwd,env=os.environ,capture_output=True,text=True,encoding='utf-8',errors='replace')
 d={'argv':args,'cwd':str(cwd),'stdout':p.stdout,'stderr':p.stderr,'exit':p.returncode};result[tag]=d
 emit('\n$ '+subprocess.list2cmdline(args)+'\nCWD='+str(cwd)+'\nSTDOUT:\n'+p.stdout+'\nSTDERR:\n'+p.stderr+'\nEXIT='+str(p.returncode))
def source(p,a,b):
 l=p.read_text(encoding='utf-8').splitlines();emit('\nSOURCE '+str(p)+'\n'+'\n'.join(f'{i}|{l[i-1]}' for i in range(a,min(b,len(l))+1)))
run('drift',[str(K/'.venv/Scripts/python.exe'),'-B','-c',"import sys,json;sys.path.insert(0,'src');from hg_kseos.lane_policy import check_drift,load_registry;print(json.dumps(check_drift(registry=load_registry()),ensure_ascii=False,indent=2))"],K)
fields=['ok','code','required_arm','served_arm','used_rank','used_transport_model','usage_receipt_ok','nonce_present','nonce_absent_arms']
base=Path('C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/lane_runs')
files=sorted(set(base.glob('*receipt*.json'))|set(base.glob('*attempts*.ndjson')))
rows=[]
for p in files:
 docs=[json.loads(x) for x in p.read_text(encoding='utf-8-sig').splitlines() if x.strip()] if p.suffix=='.ndjson' else [json.loads(p.read_text(encoding='utf-8-sig'))]
 for doc in docs:
  row={'path':str(p),'generated_utc':doc.get('generated_utc'),'run_id':doc.get('run_id'),'fields':{k:doc.get(k,'<ABSENT>') for k in fields},'attempts':[]}
  for a in doc.get('attempts',[doc] if p.suffix=='.ndjson' else []):
   row['attempts'].append({k:a.get(k,'<ABSENT>') for k in fields+['rank','provider','model','transport_model','exit','usage_provider','usage_model','usage_status','usage_receipt_reason']})
  rows.append(row);emit('MISSION_RECEIPT '+json.dumps(row,ensure_ascii=False,indent=2))
result['mission_receipts']=rows
for root,tag in [(C,'clean'),(H,'hardened')]:
 code="import sys,json;from pathlib import Path;sys.path.insert(0,'tests');import test_s4ext_trace_closure as t;pi=t._bundle(Path('C:/Projects/wt-r8-cleanmain'));obj=t.LegalTraceStillPassesTests('test_real_trace_link_is_legal_beside_its_endpoints');obj.bundle=pi;obj.test_real_trace_link_is_legal_beside_its_endpoints();print('UNCHANGED TEST METHOD PASS (existing clean repo as read-only fixture; no git init)')"
 run(tag+'_trace_direct',[PY,'-B','-c',code],root)
# Existing mutation source is read-only and only _ensure_src could write; bind SRC to existing fixture inside authorized workspace.
source_path=W/'mutation_source.md'
source_path.write_text('The intake must bind every normative claim to a source locator.\nThe compiler must refuse a normative claim without a source locator.\n',encoding='utf-8')
for mode in ['m04','m06','m16']:
 code="import sys;from pathlib import Path;sys.path.insert(0,'C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8/WS_B/RUNNERS');import probe_mutations as p;p.SRC=Path(r'"+str(source_path)+"');sys.exit(p."+{'m04':'m04_profile_downgrade','m06':'m06_domain_oracle_expected','m16':'m16_trace_digest_mismatch'}[mode]+"())"
 run(mode,[PY,'-B','-c',code],H)
# Exact CLI caller traceback without smoke's 400-char clipping; validate is read-only.
run('cli_validate_crash',[PY,'-B','-c',"import sys;sys.path.insert(0,'src');from pipd_ls_sp.cli import main;sys.argv=['pipd','--root','.','validate','--bundle','.hgk/artifacts/s1/bundle.json'];main()"],H)
for p,a,b in [(H/'src/pipd_ls_sp/validate.py',120,170),(C/'src/pipd_ls_sp/validate.py',110,145),(C/'src/pipd_ls_sp/validate.py',185,206),(C/'src/pipd_ls_sp/validate.py',266,294),(H/'src/pipd_ls_sp/validate.py',215,267),(H/'src/pipd_ls_sp/validate.py',383,446),(H/'src/pipd_ls_sp/cli.py',155,180),(K/'scripts/hgk-lane-dispatch.py',1033,1062),(K/'scripts/hgk-lane-dispatch.py',1263,1276),(K/'scripts/hgk-lane-dispatch.py',2120,2138),(K/'scripts/hgk-lane-dispatch.py',2202,2235)]:source(p,a,b)
for root,tag in [(H,'hard'),(C,'clean')]:run(tag+'_status_after',['git','--no-optional-locks','status','--short'],root)
# Extract registry and assignment safely using repository loader, not any secret-bearing runtime config.
run('declared_routes',[str(K/'.venv/Scripts/python.exe'),'-B','-c',"import sys,json;sys.path.insert(0,'src');from hg_kseos.lane_policy import load_registry;r=load_registry();a=json.load(open('config/model-lane-assignment.json',encoding='utf-8'));print(json.dumps({'registry_routes':r['routes'],'assignment':a['assignment'],'lane_chains':{k:a['lane_chains'][k] for k in ['PLAN','EXECUTE','VERIFY_SECURITY']},'digest_bindings':[{'projection':p['id'],'path':p['path'],**b} for p in r['projections'] for b in p.get('bindings',[]) if any(s in b['pointer'].lower() for s in ['sha','digest'])]},ensure_ascii=False,indent=2))"],K)
(W/'more_raw.log').write_text('\n'.join(log),encoding='utf-8')
(W/'more_results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
