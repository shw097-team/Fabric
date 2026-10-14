import pathlib,subprocess,sys,os,json,datetime
R=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS');RUN=R/'var/SKILL-CONVERGENCE-20261014';E=RUN/'evidence';H=pathlib.Path(os.environ['HERMES_HOME']);RT=H/'hermes-agent';PY=RT/'venv/Scripts/python.exe';ENV=os.environ.copy();ENV['PYTHONDONTWRITEBYTECODE']='1';slug='skill-convergence-20261014'
logs=[]
def cli(args):
 p=subprocess.run([str(PY),'-m','hermes_cli.main','kanban',*args],cwd=RT,env=ENV,capture_output=True,text=True,encoding='utf-8');logs.append({'args':args,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr});assert p.returncode==0,p.stdout+p.stderr;return p.stdout
cli(['boards','create',slug,'--name','HGK Skills Convergence 20261014','--description','HGK typed WorkOrders are truth; manual exact Codex dispatch, no automatic unpinned helpers','--default-workdir',str(RUN)])
x=cli(['--board',slug,'swarm','Two-entry lossless extraction topic references full-lint consumer and independent global regression','--worker','hgk-orchestrator:HGK lossless candidate','--worker','hgk-orchestrator:AVR lossless candidate','--worker','hgk-orchestrator:Existing consumer candidate','--verifier','hgk-orchestrator','--synthesizer','hgk-orchestrator','--created-by','hermes-main-GPT61-SOL-medium','--idempotency-key','SWARM-SKCV-20261014','--json'])
(E/'kanban_setup.json').write_text(json.dumps({'slug':slug,'calls':logs,'swarm_raw':x,'native_auto_dispatch':False,'manual_codex_binding':'Seven admitted roles; native graph coordinates, model pins in exact Codex launcher'},ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
db=H/'kanban/boards'/slug/'kanban.db';import sqlite3
with sqlite3.connect(db.as_uri()+'?mode=ro',uri=True) as c:
 c.row_factory=sqlite3.Row;tasks=[dict(t) for t in c.execute('select * from tasks')]
(E/'kanban_initial_readback.json').write_text(json.dumps(tasks,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n');print(x)
