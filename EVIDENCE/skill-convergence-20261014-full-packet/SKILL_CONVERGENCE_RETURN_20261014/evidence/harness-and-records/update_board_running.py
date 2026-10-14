import pathlib,subprocess,os,json,sqlite3,datetime,sys
R=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014');E=R/'evidence';H=pathlib.Path(os.environ['HERMES_HOME']);RT=H/'hermes-agent';PY=RT/'venv/Scripts/python.exe';slug='skill-convergence-20261014';env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1';logs=[]
def call(args):
 p=subprocess.run([str(PY),'-m','hermes_cli.main','kanban','--board',slug,*args],cwd=RT,env=env,capture_output=True,text=True,encoding='utf-8');logs.append({'args':args,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr});return p
for role,card,proc in [('HGK','t_ecf1b71c','proc_264cfc7a58ae'),('AVR','t_cc3569a4','proc_07ccbb59acae'),('CONSUMER','t_82b1e625','proc_eb8855b87794')]:
 call(['claim',card]);call(['comment',card,'Manual sanctioned Codex workspace-write bounded run; WO-SKCV-20261014-'+role+'; process='+proc+'; required arm opencode-go/deepseek-v4.1-flash; actual final receipt pending; no native dispatcher spawn claimed.']);call(['heartbeat',card])
call(['comment','t_abd1c49d','Root done is native swarm planning-anchor completion ONLY, not project acceptance. HGK project EXECUTING; four exact Codex maker processes overlap in disjoint roots. PLAN remains current Hermes GPT6.1 SOL medium OAuth. Initial OpenSpec scaffold preceded specific root admission, disclosed; product mutation remains candidate only.'])
(E/'kanban_running_calls.json').write_text(json.dumps(logs,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
with sqlite3.connect((H/'kanban/boards'/slug/'kanban.db').as_uri()+'?mode=ro',uri=True) as c:
 c.row_factory=sqlite3.Row;s=[dict(r) for r in c.execute('select id,title,status,claim_lock,last_heartbeat_at from tasks')]
(E/'kanban_running_readback.json').write_text(json.dumps({'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tasks':s},indent=2),encoding='utf-8',newline='\n');print(json.dumps({'calls':[(x['args'][:2],x['exit']) for x in logs],'tasks':s},indent=2))
