"""Close this round's board cards, in dependency order, with the round's evidence as the result text.

The board graph was created at round start and its worker cards were never driven by the native dispatcher: the
round ran its lanes through the manual exact dispatcher instead. That is a real divergence between the board and
what happened, and the correct close is to say so on each card rather than to leave cards reading "running" or to
mark them done without a word.
"""
import os,subprocess,json,pathlib,datetime
HERMES=r'C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes'
VENV=HERMES+'/hermes-agent/venv/Scripts/python.exe'
SRC=HERMES+'/hermes-agent'
BOARD='skill-convergence-20261014'
X=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014')
env=os.environ.copy();env['HERMES_HOME']=HERMES;env['PYTHONDONTWRITEBYTECODE']='1'
def kc(*args):
    p=subprocess.run([VENV,'-B','-m','hermes_cli.main','kanban','--board',BOARD,*args],cwd=SRC,env=env,
                     capture_output=True,text=True,encoding='utf-8',errors='replace')
    return p.returncode,(p.stdout or '').strip(),(p.stderr or '').strip()
rc,out,err=kc('tasks','--json')
print('READBACK_BEFORE rc',rc,'bytes',len(out));print(out[:600] or err[:400])
before=None
try:before=json.loads(out)
except Exception:pass
NOTE=('本回合以既有可複用的手動 exact 派遣車道執行，未由 native dispatcher 驅動此卡；'
      '證據見 var/SKILL-CONVERGENCE-20261014/evidence/postfreeze/SESSION_CLOSURE.md 與同目錄 CLOSURE_MANIFEST.json。')
RESULT=('結案：候選成果已交付；兩軸獨立查核皆 PASS_ADVISORY（VERIFY 與 SECURITY，gen2）；'
        '對外發佈 feat/skill-convergence-return-20261014；殘留缺口與失敗紀錄見 SESSION_CLOSURE.md。'
        '本卡狀態為結案紀錄，不構成 acceptance 或 promotion。')
plan=[('t_ecf1b71c','HGK lossless candidate'),('t_cc3569a4','AVR lossless candidate'),
      ('t_82b1e625','Existing consumer candidate'),('t_187f9c1d','Verify swarm outputs'),
      ('t_0706f07e','Synthesize swarm outputs')]
log=[]
for cid,title in plan:
    rc1,o1,e1=kc('comment',cid,NOTE)
    rc2,o2,e2=kc('comment',cid,RESULT)
    rc3,o3,e3=kc('complete',cid,'--result',RESULT)
    log.append({'id':cid,'title':title,'comment_rc':rc1,'comment2_rc':rc2,'complete_rc':rc3,
                'complete_out':(o3 or e3)[:200]})
    print(cid,title,'comment',rc1,rc2,'complete',rc3,(o3 or e3)[:120])
rc,out,err=kc('tasks','--json')
after=None
try:after=json.loads(out)
except Exception:pass
res={'schema':'SKILL-CONVERGENCE-BOARD-CLOSURE/1','observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'board':BOARD,'board_db':HERMES+'/kanban/boards/'+BOARD+'/kanban.db',
 'readback_before':before,'readback_after':after,'calls':log,
 'note':NOTE,'result_text':RESULT,
 'claim_ceiling':'a board close-out; card status is mutable state and grants no acceptance'}
(X/'evidence/postfreeze/board_closure.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
print('STATUSES_AFTER',[(t.get('id'),t.get('status')) for t in (after or [])] if isinstance(after,list) else after)
