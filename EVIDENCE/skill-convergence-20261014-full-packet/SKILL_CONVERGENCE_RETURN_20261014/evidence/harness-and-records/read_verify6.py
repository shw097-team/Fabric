"""Read the closure-review lane's own transcript and report what it emitted.

Same discipline as the security lane: the transport gate judged a token and a usage receipt, so the transcript is
read item by item -- how many commands ran, what the final message contains, where the token sits, and whether the
case ids named in the brief appear in the verdict object.
"""
import json,pathlib,re
L=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014/evidence/lanes/verify/6')
P=L/'trace/observed-1.stdout.jsonl'
items=[]
for line in P.read_text(encoding='utf-8',errors='replace').splitlines():
    line=line.strip()
    if line:
        try:items.append(json.loads(line))
        except Exception:pass
kinds={}
for it in items:
    t=it.get('type');kinds[t]=kinds.get(t,0)+1
    if t=='item.completed':kinds['item:'+str(it.get('item',{}).get('type'))]=kinds.get('item:'+str(it.get('item',{}).get('type')),0)+1
msgs=[(n,it['item']['text']) for n,it in enumerate(items) if it.get('type')=='item.completed' and it.get('item',{}).get('type')=='agent_message']
TOK='SKCV_VERIFY_6_OK'
tok=[n for n,t in msgs if TOK in t]
obj=None
if msgs:
    final=msgs[-1][1];s=final.find('{');e=final.rfind('}')
    if s>=0 and e>s:
        try:obj=json.loads(final[s:e+1])
        except Exception:obj=None
(L/'last_message.txt').write_text('EXTRACTED BY THE ROUND HARNESS from trace/observed-1.stdout.jsonl\n'
  'This is the lane\'s final message verbatim; the lane did not write this file.\n----\n'+(msgs[-1][1] if msgs else ''),
  encoding='utf-8',newline='\n')
(L/'verdict.json').write_text(json.dumps({'extraction_note':'harness extraction from the lane transcript; not authored by the lane',
  'source':'evidence/lanes/verify/6/trace/observed-1.stdout.jsonl','agent_messages':len(msgs),'verdict_object':obj},
  ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
print(json.dumps({'items':len(items),'kinds':kinds,'messages':len(msgs),'token_positions':tok,
  'token_is_last':bool(msgs and tok and msgs[-1][0] in tok),'verdict_parsed':obj is not None},indent=1))
if obj:
    print('VERDICT',obj.get('verdict'))
    cases=obj.get('cases');print('CASES',[(c.get('case_id'),c.get('status')) for c in cases] if isinstance(cases,list) else cases)
    print('FINDINGS',json.dumps(obj.get('findings'),ensure_ascii=False)[:1200])
    print('COVERAGE',json.dumps(obj.get('coverage'),ensure_ascii=False)[:600])
    print('CEILING',str(obj.get('claim_ceiling'))[:200])
print('TAIL');print(msgs[-1][1][-900:] if msgs else '')
