"""Read the security lane's own transcript and report what it actually emitted.

The transport gate judges the lane on a token and a usage receipt, and an earlier attempt satisfied that gate
with a seven-second turn whose entire content was the token. So the transcript is read item by item: how many
commands ran, which messages the agent emitted, whether the token is present and where it sits relative to the
verdict object, and whether the case ids named in the brief appear.
"""
import json,pathlib,re
P=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014/evidence/lanes/security/5/trace/observed-1.stdout.jsonl')
items=[];bad=0
for line in P.read_text(encoding='utf-8',errors='replace').splitlines():
    line=line.strip()
    if not line:continue
    try:items.append(json.loads(line))
    except Exception:bad+=1
kinds={}
for it in items:
    t=it.get('type','?');kinds[t]=kinds.get(t,0)+1
    if it.get('type')=='item.completed':kinds['item:'+it.get('item',{}).get('type','?')]=kinds.get('item:'+it.get('item',{}).get('type','?'),0)+1
msgs=[(n,it['item']['text']) for n,it in enumerate(items) if it.get('type')=='item.completed' and it.get('item',{}).get('type')=='agent_message']
TOK='SKCV_SECURITY_5_OK'
tok_pos=[n for n,t in msgs if TOK in t]
verdict_obj=None;verdict_msg=None
for n,t in msgs:
    for m in re.finditer(r'\{',t):
        frag=t[m.start():]
        try:
            obj=json.loads(frag[:frag.rindex('}')+1])
        except Exception:
            pass
        else:
            if isinstance(obj,dict) and 'verdict' in obj:
                verdict_obj=obj;verdict_msg=n
print(json.dumps({'lines':len(items),'unparsed':bad,'kinds':kinds,'agent_messages':len(msgs),
  'token_present_in_messages':len(tok_pos),'token_message_index':tok_pos[:3],'last_message_index':msgs[-1][0] if msgs else None,
  'verdict_object_found':verdict_obj is not None,'verdict_in_message':verdict_msg,
  'token_is_last_content':bool(msgs) and tok_pos and tok_pos and msgs[-1][0] in tok_pos},indent=1))
if verdict_obj:
    print('VERDICT',verdict_obj.get('verdict'),'| cases',list(verdict_obj.get('cases',{}).keys()) if isinstance(verdict_obj.get('cases'),dict) else verdict_obj.get('cases'))
    print('CASE_IDS',json.dumps(verdict_obj.get('cases'),ensure_ascii=False)[:900])
    print('FINDINGS',json.dumps(verdict_obj.get('findings'),ensure_ascii=False)[:700])
    print('COVERAGE',json.dumps(verdict_obj.get('coverage'),ensure_ascii=False)[:500])
    print('CEILING',str(verdict_obj.get('claim_ceiling'))[:200])
print('TAIL_MESSAGES')
for n,t in msgs[-2:]:
    print('---',n,len(t));print(t[-1200:])
