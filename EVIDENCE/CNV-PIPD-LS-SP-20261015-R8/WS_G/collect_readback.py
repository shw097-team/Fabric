"""Read-only subject audit; all authored writes confined to this directory."""
import os, sys, json, subprocess, datetime
from pathlib import Path
OUT = Path(__file__).resolve().parent
ROOT = Path('C:/Projects/Agent_Workspace/HG-KSEOS')
HOME = Path('C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes')
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONIOENCODING='utf-8', GIT_OPTIONAL_LOCKS='0')
LOG = OUT / 'commands.json'
records = json.loads(LOG.read_text(encoding='utf-8')) if LOG.exists() else []
def run(label, argv):
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    p = subprocess.run(argv, cwd='C:/Users/user', env=ENV, capture_output=True, encoding='utf-8', errors='replace', timeout=180)
    rec = dict(id=label, command=subprocess.list2cmdline(argv), argv=argv, cwd='C:/Users/user', started_utc=start, ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), stdout=p.stdout, stderr=p.stderr, exit_code=p.returncode)
    records.append(rec)
    LOG.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
    print(label, 'exit=',p.returncode, '\n'+p.stdout, '\nSTDERR:\n'+p.stderr)
    return rec

def py(label, code): return run(label,[sys.executable,'-B','-c',code])
if __name__ == '__main__':
    py('identity-time', "import os,sys,datetime,getpass; print('utc='+datetime.datetime.now(datetime.timezone.utc).isoformat()); print('local='+datetime.datetime.now().astimezone().isoformat()); print('pid='+str(os.getpid())); print('ppid='+str(os.getppid())); print('user='+getpass.getuser()); print('python='+sys.executable)")
    run('os-identity',['whoami','/user'])
    names = ['probe_gstack_rolemap.py','lane-route-slots.candidate.json','model-lane-assignment.json','lane-routing-registry.yaml','HGK_GSTACK_ROLE_MAP.yaml','HGK_GSTACK_UPSTREAM_CAPABILITY_SNAPSHOT.tsv','named_methods.py','runtime_role_binding_assert.py']
    py('discover-current-non-reparse-tree', "import os,json; from pathlib import Path; root=Path("+repr(str(ROOT))+"); names="+repr(names)+"; hits=[]; excluded=[]\nfor d,ds,fs in os.walk(root):\n keep=[]\n for x in ds:\n  p=Path(d)/x\n  if x in {'.git','node_modules','.venv','var','worktrees','.hgk'} or (getattr(p.stat(follow_symlinks=False),'st_file_attributes',0)&1024): excluded.append(str(p))\n  else: keep.append(x)\n ds[:]=keep\n for n in fs:\n  if n in names: hits.append(str(Path(d)/n))\nprint(json.dumps({'hits':hits,'excluded_noncanonical_or_reparse_roots':excluded},indent=2))")
    run('git-head',['git','-C',str(ROOT),'rev-parse','HEAD'])
    run('git-status-before',['git','-C',str(ROOT),'-c','core.quotepath=false','status','--porcelain','--untracked-files=normal'])
    run('runtime-assert-tracked',['git','-C',str(ROOT),'ls-files','--error-unmatch','scripts/runtime_role_binding_assert.py'])
    run('runtime-assert-status',['git','-C',str(ROOT),'status','--porcelain','--untracked-files=all','--','scripts/runtime_role_binding_assert.py'])
    run('source-role-and-wiring-search',['rg','--no-ignore','--hidden','-n','-g','*.py','-g','*.ps1','-g','*.sh','NAMED_METHODS|gstack\\.|runtime_role_binding_assert|role_binding|require_arm|served_arm|run_as_user|os_identity|whoami',str(ROOT/'src'),str(ROOT/'scripts')])
    rels=['AGENTS.md','control/AGENTS.md','HGK/HGK_GSTACK_ROLE_MAP.yaml','HGK/HGK_GSTACK_UPSTREAM_CAPABILITY_SNAPSHOT.tsv','src/hg_kseos/named_methods.py','src/hg_kseos/lane_policy.py','scripts/runtime_role_binding_assert.py','config/lane-route-slots.candidate.json','config/model-lane-assignment.json','config/lane-routing-registry.yaml']
    for rel in rels:
        py('source:'+rel, "from pathlib import Path; p=Path("+repr(str(ROOT/rel))+"); print('FILE='+str(p)); print(''.join(str(i)+': '+line for i,line in enumerate(p.read_text(encoding='utf-8').splitlines(True),1)))")
    py('hermes-safe-selected-config', "import json,yaml; from pathlib import Path; home=Path("+repr(str(HOME))+")\nfor p in [home/'profiles/hgk-governed/config.yaml',home/'config.yaml']:\n print('FILE='+str(p)); lines=p.read_text(encoding='utf-8').splitlines(); chosen={'model','governed_runtime','delegation'}; active=False\n for i,line in enumerate(lines,1):\n  if line and not line[0].isspace() and not line.lstrip().startswith('#'): active=line.split(':',1)[0] in chosen\n  if active:\n   key=line.strip().split(':',1)[0].lower()\n   if any(x in key for x in ['api_key','password','secret','token']): print(str(i)+': <credential-key line not emitted>')\n   else: print(str(i)+': '+line)\n")
    probe=Path('C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/R6_DELIVERY/RUNNERS/probe_gstack_rolemap.py')
    py('existing-probe-source',"from pathlib import Path; p=Path("+repr(str(probe))+"); print('FILE='+str(p)); print(''.join(str(i)+': '+line for i,line in enumerate(p.read_text(encoding='utf-8').splitlines(True),1)))")
    run('existing-probe-positive',[sys.executable,'-B',str(probe),'positive'])
    run('existing-probe-negative',[sys.executable,'-B',str(probe),'negative'])
    py('runtime-named-method-and-drift-readback', "import sys,json,dataclasses,hashlib; from pathlib import Path; root=Path("+repr(str(ROOT))+"); sys.path.insert(0,str(root/'src')); from hg_kseos import named_methods as nm,lane_policy as lp; reg=lp.load_registry(); print(json.dumps({'named_method_source':nm.__file__,'named_methods':{k:dataclasses.asdict(v) for k,v in nm.NAMED_METHODS.items()},'ACTIVE_SELECTED':sorted(nm.ACTIVE_SELECTED),'route_calls':{f:nm.route(f) for f in ['ambiguity','plan','review','qa','security','release','retro','brownfield']},'role_literal_calls':{r:nm.route(r) for r in json.loads((root/'HGK/HGK_GSTACK_ROLE_MAP.yaml').read_text())['roles']},'lane_policy_source':lp.__file__,'routes':reg['routes'],'drift_receipt':lp.render_receipt(registry=reg,findings=lp.check_drift(),checked_sites=lp.count_checked_sites(reg)),'source_pin':{'expected':reg['source_of_routes'],'observed_sha256':hashlib.sha256((root/'config/model-lane-assignment.json').read_bytes()).hexdigest()},'mandated_plan_verify_sod':lp.check_sod('gpt-6.1-sol','gpt-6.1-sol'),'mandated_execute_verify_sod':lp.check_sod('deepseek-v4.1-flash','gpt-6.1-sol')},ensure_ascii=False,indent=2))")
