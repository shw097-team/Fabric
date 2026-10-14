"""Read the board's own database to prove the close-out landed, since the CLI has no `tasks` verb.

The CLI accepted the comments and the completions (exit 0 each), but a CLI's exit code is a claim. The board is a
SQLite file, so the statuses and the comment rows are read directly and written into the closure artifact.
"""
import sqlite3,json,pathlib,datetime
DB=r'C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/kanban/boards/skill-convergence-20261014/kanban.db'
X=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014/evidence/postfreeze/board_closure.json')
con=sqlite3.connect(f'file:{DB}?mode=ro',uri=True);cur=con.cursor()
tabs=[r[0] for r in cur.execute("select name from sqlite_master where type='table'")]
tasks=[{'id':r[0],'title':r[1],'status':r[2],'assignee':r[3] if len(r)>3 else None}
       for r in cur.execute('select id,title,status from tasks')]
comments={}
if 'task_comments' in tabs:
    for tid,n in cur.execute('select task_id,count(*) from task_comments group by task_id'):
        comments[tid]=n
con.close()
res=json.loads(X.read_text(encoding='utf-8'))
res['readback_source']='direct sqlite read of the board database; the kanban CLI on this host has no `tasks` verb, so a CLI readback was impossible and the exit codes alone would have been a claim'
res['readback_after']=tasks;res['comments_per_task']=comments
res['tables']=tabs
res['statuses']={t['id']:t['status'] for t in tasks}
res['all_round_cards_done']=all(t['status']=='done' for t in tasks)
X.write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
print(json.dumps({'tables':tabs,'statuses':res['statuses'],'comments':comments,'all_done':res['all_round_cards_done']},indent=1))
