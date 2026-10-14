import json,pathlib,sqlite3,subprocess,os,datetime,hashlib
R=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS');RUN=R/'var/SKILL-CONVERGENCE-20261014';E=RUN/'evidence'
H=pathlib.Path(os.environ['HERMES_HOME']);RT=H/'hermes-agent';PY=RT/'venv/Scripts/python.exe'
def run(args,cwd,e=None):
 if isinstance(args,str):
  p=subprocess.run(args,cwd=cwd,env=e,capture_output=True,text=True,encoding='utf-8',shell=True)
 else:
  p=subprocess.run(args,cwd=cwd,env=e,capture_output=True,text=True,encoding='utf-8')
 return {'args':args if isinstance(args,str) else ' '.join(args),'exit':p.returncode,'stdout':(p.stdout or '').strip()[:2500],'stderr':(p.stderr or '').strip()[:1200]}
osr=run('openspec validate hgk-skill-convergence-20261014 --strict',R)
ost=run('openspec status --change hgk-skill-convergence-20261014 --json',R)
try:ostatus=json.loads(ost['stdout'])
except Exception:ostatus={'raw':ost['stdout'][:1500]}
board=H/'kanban/boards/skill-convergence-20261014/kanban.db'
tasks=[]
if board.exists():
 with sqlite3.connect(board.as_uri()+'?mode=ro',uri=True) as c:
  c.row_factory=sqlite3.Row
  cols=[r[1] for r in c.execute('pragma table_info(tasks)')]
  keep=[k for k in ('id','title','status','assignee','owner','role','updated_at','created_at') if k in cols]
  tasks=[{k:r[k] for k in keep} for r in c.execute('select * from tasks')]
lanes={}
for role,tag in [('hgk','4'),('avr','3'),('consumer','3'),('apply','3')]:
 d=RUN/'evidence/lanes'/role/tag
 disp=d/'dispatch.json';drv=d/'driver.json'
 lanes[f'{role}-{tag}']={'dispatch_json_exists':disp.exists(),'driver_exists':drv.exists(),
                        'prompt':'|'.join((E/'prompts'/f'{role}-{tag}.md').read_text(encoding='utf-8').split('\n')[:1])}
receipt={
 'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'kind':'continuation turn record — owner route change + tooling activation + lane launches',
 'owner_route_revision':{
   'plan_orchestrator_model_mandated':'GLM-5.3-Flash (OPENCODE GO)',
   'execute_writer_mandated':'Codex CLI opencode-go/deepseek-v4.1-flash',
   'checker_mandated':'Codex CLI opencode-go/glm-5.3-flash',
   'reason_given':'GPT quota exhausted',
   'plan_document':str(H/'cache/scratch/SKILL-CONVERGENCE-20261014-preflight/PLAN-REV4-OWNER-ROUTE.md'),
   'observed_deviation':{
     'session_active_model_reported':'deepseek-v4.1-flash via opencode-go (runtime metadata for this chat)',
     'config_model_default_reported':'deepseek-v4-flash / provider opencode-go / api_mode chat_completions',
     'consequence':'the mandated PLAN model is NOT what served this PLAN session; the deviation is recorded, not hidden, and the global model setting was NOT changed by this agent',
     'sod_residual':'mandated PLAN and mandated checker are the same model (GLM-5.3-Flash); independence is at entry-point/lane/evidence-path level only, NOT model level; no model-level SoD is claimed',
     'owner_action_available':'switch the chat model in the UI, or explicitly authorise a config change; either would remove this deviation'}},
 'openspec':{'validate':osr,'status_exit':ost['exit'],'status':ostatus if isinstance(ostatus,dict) else {'raw':str(ostatus)[:1500]}},
 'gstack_route_receipt':{'path':str(E/'gstack_route_receipt.json'),'sha256':hashlib.sha256((E/'gstack_route_receipt.json').read_bytes()).hexdigest(),
   'consistency_gap_count':json.loads((E/'gstack_route_receipt.json').read_text(encoding='utf-8'))['consistency_gap']['count'],
   'activation_invariants_all_zero':all(v==0 for v in json.loads((E/'gstack_route_receipt.json').read_text(encoding='utf-8'))['activation_invariants'].values())},
 'kanban':{'board_db':str(board),'board_exists':board.exists(),'task_count':len(tasks),'tasks':tasks,
   'honesty_note':'the swarm parent task reads status=done while its worker tasks read running; kanban board status is coordination state, NOT evidence that any work finished or passed. The parent done value is not used as a completion claim in this round.'},
 'lanes_launched_this_turn':lanes,
 'verification_route':{'planned':'fresh Codex CLI opencode-go/glm-5.3-flash read-only VERIFY and SECURITY over an immutable frozen subject manifest, dispatched only after the maker phases close',
   'not_yet_run':True,'not_an_acceptance_yet':True},
 'claim_ceiling':'tooling activation and route receipts only; no product acceptance, no canonical apply, no gstack workflow execution claimed'}
(E/'continuation_turn_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2,default=str),encoding='utf-8',newline='\n')
print(json.dumps({'openspec_validate_exit':osr['exit'],'openspec_validate':osr['stdout'][:60],'openspec_status_exit':ost['exit'],
 'planning_complete':ostatus.get('isPlanningComplete') if isinstance(ostatus,dict) else None,
 'kanban_tasks':len(tasks),'kanban_sample':tasks[:3]},ensure_ascii=False,indent=2,default=str))
