"""Preserve the security lane's own verdict as a small durable artifact.

The verdict existed only inside a 325 KB transcript, and transcripts are excluded from the return packet by
size, so the packet carried the adjudication of the verdict but not the verdict itself. A reviewer would have had
to take the adjudication on trust, which is the one thing the packet exists to avoid. These two files are
extracted from the lane's own stdout by the round harness; they are labelled as such and are not claimed to be
files the lane wrote.
"""
import json,pathlib
X=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014')
LANE=X/'evidence/lanes/security/5'
TRACE=LANE/'trace/observed-1.stdout.jsonl'
msgs=[]
for line in TRACE.read_text(encoding='utf-8',errors='replace').splitlines():
    line=line.strip()
    if not line:continue
    try:it=json.loads(line)
    except Exception:continue
    if it.get('type')=='item.completed' and it.get('item',{}).get('type')=='agent_message':
        msgs.append(it['item']['text'])
final=msgs[-1] if msgs else ''
( LANE/'last_message.txt' ).write_text(
    'EXTRACTED BY THE ROUND HARNESS from evidence/lanes/security/5/trace/observed-1.stdout.jsonl\n'
    'This is the lane\'s final message verbatim; the lane did not write this file.\n'
    '----\n'+final, encoding='utf-8',newline='\n')
obj=None;start=final.find('{');end=final.rfind('}')
if start>=0 and end>start:
    try:obj=json.loads(final[start:end+1])
    except Exception:obj=None
out={'extraction_note':'harness extraction from the lane transcript; not authored by the lane',
     'source':'evidence/lanes/security/5/trace/observed-1.stdout.jsonl','agent_messages_in_transcript':len(msgs),
     'verdict_object':obj}
( LANE/'verdict.json' ).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
print(json.dumps({'messages':len(msgs),'final_message_bytes':len(final),'verdict_parsed':obj is not None,
  'verdict':(obj or {}).get('verdict'),'case_count':len((obj or {}).get('cases',[])) if isinstance((obj or {}).get('cases'),list) else None},indent=1))
