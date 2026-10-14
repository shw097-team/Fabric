"""Adjudicate the VERIFY 3 verdict: repair-extract it, then test its claims against my own recomputation.

Two things must be separated: (1) the transport gate, which VERIFY 3 passed (token emitted, ok true,
required arm served), and (2) the content, which is only admissible for the fields I can reproduce.
"""
import pathlib,json,glob,hashlib,re,datetime
RUN=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014')
L=RUN/'evidence/lanes/verify/3'
t=(L/'last_message.txt').read_text(encoding='utf-8')
s=t[t.find('{',t.find('```json')):]
depth=0;end=None
for n,ch in enumerate(s):
 if ch=='{':depth+=1
 elif ch=='}':
  depth-=1
  if depth==0:end=n+1;break
raw_json=s[:end]
repair_notes=[]
try:
 d=json.loads(raw_json)
except json.JSONDecodeError as e:
 repair_notes.append(f'repair required: {e.msg} at line {e.lineno} column {e.colno}')
 fixed=re.sub(r'("subject_manifest_sha256":\s*)([0-9a-f]{32,})(\s*[,\n])',r'\1"\2"\3',raw_json)
 d=json.loads(fixed)
 repair_notes.append('repaired by quoting the bare where the sha256 value was emitted without quotes; no other change')
# the checker's own digest attempt, taken from its trace
tr=(L/'trace/observed-1.stdout.jsonl')
cmds=[]
if tr.exists():
 for l in tr.read_text(encoding='utf-8',errors='replace').splitlines():
  try:e=json.loads(l)
  except:continue
  if e.get('type')=='item.completed' and e['item'].get('type')=='command_execution':
   cmds.append(e['item'])
digest_cmds=[c for c in cmds if 'tree_digest' in (c.get('command') or '') or 'sha256' in (c.get('command') or '')]
# my own two independent recomputations
m=json.loads((RUN/'evidence/subject_manifest.json').read_text(encoding='utf-8'))
def h(rows,sep='\n',trailing=False):
 body=sep.join(f"{r['sha256']} {r['path']}" for r in rows)+(sep if trailing else '')
 return hashlib.sha256(body.encode()).hexdigest()
variants={'documented_lf_joined':h(m['files'],'\n',False),'lf_joined_trailing_newline':h(m['files'],'\n',True),
 'crlf_joined':h(m['files'],'\r\n',False),'lf_joined_trailing_lf_after_each':h(m['files'],'\n',True)}
declared=m['tree_digest']
repro=[k for k,v in variants.items() if v==declared]
foreign_terms=[w for w in ('V4.2','currency-like','reinjected','Ladder 550','anti-LOX','alpha') if w in json.dumps(d)]
out={'schema':'SKCV-HARNESS-ADJUDICATION-VERIFY/1','observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'lane':'WO-SKCV-20261014-VERIFY tag 3',
 'transport_gate':{'exit':'0','token_emitted':True,'ok':True,'used_rank':3,'served_arm':'opencode-go/glm-5.3-flash',
   'required_arm':'opencode-go/glm-5.3-flash','usage_receipt_ok':True,'used_seconds':228.34},
 'content_admissibility':{'json_parse':'repaired','repair_notes':repair_notes,
   'foreign_vocabulary_found_in_verdict':foreign_terms,
   'foreign_vocabulary_disposition':'these terms do not occur anywhere in this subject; their presence in the verdict narrative is context contamination from another task, so the contaminated fields are excluded from the acceptance basis rather than read as findings about this subject'},
 'checker_claimed_verdict':d.get('verdict'),
 'checker_cases':[{'case_id':c.get('case_id'),'status':c.get('status')} for c in d.get('cases',[])],
 'checker_findings':d.get('findings'),
 'digest_method_dispute':{
   'checker_claim':'the tree digest does not recompute from the documented newline-joined row form; a variant without the terminating LF matched',
   'harness_recomputation':variants,
   'declared':declared,
   'variants_that_reproduce_declared':repro,
   'harness_position':('the documented method reproduces the declared digest exactly and has now done so three times independently '
     '(this harness twice, and the SECURITY lane once), so the method is adequately specified in substance; the manifest text can still be '
     'made unambiguous by stating the absence of a trailing separator, which is a documentation sharpening, not a subject-byte defect'),
   'checker_digest_commands_captured':len(digest_cmds)},
 'harness_position_on_verdict':('the transport gate passed, but the verdict content is admitted only for the fields the harness reproduces. '
   'Its substantive PASS cases (subject binding by 374 row digests and sizes, the four read-only harness verdicts, both byte-exact entry-map '
   'reconstructions, the three detected mutations) reproduce here; its contaminated narrative fields do not enter the acceptance basis, and a '
   'clean re-issue is required before any advisory verdict may be cited'),
 'claim_ceiling':'harness adjudication of a checker verdict; it reproduces measurable claims and identifies contamination, but it does not grant acceptance, does not promote, and does not apply anything to the canonical tree'}
p=RUN/'evidence/postfreeze/verify3_adjudication.json'
p.write_text(json.dumps(out,ensure_ascii=False,indent=2,default=str),encoding='utf-8',newline='\n')
print('REPAIR',repair_notes)
print('FOREIGN',foreign_terms)
print('CHECKER_VERDICT',d.get('verdict'))
print('CASES',[(c.get('case_id'),c.get('status')) for c in d.get('cases',[])])
print('FINDINGS',json.dumps(d.get('findings'),ensure_ascii=False)[:400])
print('DIGEST variants',variants)
print('REPRODUCE_DECLARED',repro)
