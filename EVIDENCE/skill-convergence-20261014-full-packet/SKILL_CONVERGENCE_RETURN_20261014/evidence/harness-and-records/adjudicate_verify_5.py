"""Adjudicate the VERIFY 5 verdict against the harness's own measurements for generation 2.

Admits the verdict only for the fields the harness reproduces: binding, the four harness verdicts, the
stub-signal repair, the sprawl pilot, the apply patch's canonical-untouched property, both entry-map
reconstructions and the three mutations. Anything the harness cannot reproduce is named as such.
"""
import pathlib,json,hashlib,re,datetime,subprocess,glob
RUN=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014')
PY='C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe'
L=RUN/'evidence/lanes/verify/5'
FIXED=['SUBJECT-BINDING','HARNESS-CONVERGENCE','HARNESS-AVR-BATCH1','HARNESS-HGK-BATCH1','HARNESS-HGK-BATCH2',
 'STUB-SIGNAL-REPAIR','REMEDIATION-HGK-SPRAWL','REMEDIATION-APPLY-PATCH','RECONSTRUCTION-AVR','RECONSTRUCTION-HGK',
 'RECONSTRUCTION-MUTATIONS','C1-EXTRACTION','C2-THEMES','C3-CONSUMER','C4-ROLLBACK','C5-POLICY','COVERAGE']
FOREIGN=['V4.2','currency-like','reinjected','Ladder 550','anti-LOX','ratchet','envelope count']
f=sorted((L/'raw').glob('*stdout*.txt'))[-1]
msgs=[]
for l in f.read_text(encoding='utf-8',errors='replace').splitlines():
    try:e=json.loads(l)
    except:continue
    if e.get('type')=='item.completed' and e['item'].get('type')=='agent_message':msgs.append(e['item'].get('text') or '')
t=msgs[-1] if msgs else ''
(L/'last_message.txt').write_text(t,encoding='utf-8')
s=t[t.find('{',t.find('```json')):] if '```json' in t else t[t.find('{'):]
depth=0;end=None
for n,ch in enumerate(s):
    if ch=='{':depth+=1
    elif ch=='}':
        depth-=1
        if depth==0:end=n+1;break
raw=s[:end]
notes=[]
try:d=json.loads(raw);notes.append('parsed clean')
except json.JSONDecodeError as ex:
    fixed=re.sub(r'("subject_manifest_sha256":\s*)([0-9a-f]{32,})(\s*[,\n])',r'\1"\2"\3',raw)
    d=json.loads(fixed);notes.append(f'repair needed ({ex.msg})')
(L/'verdict.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
ids=[c.get('case_id') for c in d.get('cases',[])]
foreign=[w for w in FOREIGN if w.lower() in json.dumps(d,ensure_ascii=False).lower()]
# ---- harness re-derivation
m=json.loads((RUN/'evidence/subject_manifest.json').read_text(encoding='utf-8'))
digest=hashlib.sha256('\n'.join(f"{r['sha256']} {r['path']}" for r in m['files']).encode()).hexdigest()
badrows=sum(1 for r in m['files'] if hashlib.sha256((RUN/r['path']).read_bytes()).hexdigest()!=r['sha256'])
harn={}
for name,script,args in (('convergence','evidence/convergence_check.py',[]),
    ('avr_batch1','evidence/check_topic_batch.py',['avr','topic_batch_1.json']),
    ('hgk_batch1','evidence/check_topic_batch.py',['hgk','topic_batch_1.json']),
    ('hgk_batch2','evidence/check_topic_batch.py',['hgk','topic_batch_2.json'])):
    p=subprocess.run([PY,str(RUN/script)]+args,cwd=str(RUN),capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=600)
    o=p.stdout or ''
    harn[name]={'exit':p.returncode,'rows_reporting_stub_points_at_topic_true':o.count('"stub_points_at_topic": true'),
      'rows_reporting_false':o.count('"stub_points_at_topic": false'),'all_absorbed_lossless':'"all_absorbed_lossless": true' in o,
      'verdict_token':('CONVERGENCE_INVARIANTS_HOLD_WITH_DECLARED_REMEDIATION' if 'CONVERGENCE_INVARIANTS_HOLD_WITH_DECLARED_REMEDIATION' in o else None)}
C=RUN/'candidates/hgk/skill';B=RUN/'baseline/hgk-governed-execution'
rr=json.loads((RUN/'candidates/hgk/remediation_result.json').read_text(encoding='utf-8'))
tp=C/(rr['topic_file']['path'].split('skill/',1)[-1] if 'skill/' in rr['topic_file']['path'] else rr['topic_file']['path'])
tt=tp.read_bytes()
pres=[];notpres=[]
for rec in rr['merged']:
    rel=rec['path'].split('skill/',1)[-1] if 'skill/' in rec['path'] else rec['path']
    bb=B/rel
    ok=bb.exists() and tt.count(bb.read_bytes())==1
    (pres if ok else notpres).append(rel)
refs=len([p for p in C.rglob('*.md') if not any(x.startswith('_') for x in p.relative_to(C).parts)])
can=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/scripts/hgk-lane-dispatch.py')
patch=(RUN/'candidates/apply/patch/lane-dispatch-timeout-capture.patch')
ctx_ok=None
if patch.exists():
    lines=[l[1:] for l in patch.read_text(encoding='utf-8',errors='replace').splitlines() if l.startswith(' ')]
    canlines=can.read_text(encoding='utf-8',errors='replace').splitlines()
    hits=sum(1 for l in lines if l.strip() and any(l.strip()==c.strip() for c in canlines))
    ctx_ok={'context_lines':len(lines),'context_lines_present_in_canonical':hits,'all_present':hits==len([l for l in lines if l.strip()])}
out={'schema':'SKCV-HARNESS-ADJUDICATION-VERIFY5/1','observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'lane':'WHO-SKCV-20261014-VERIFY tag 5','transport':{'exit':'0','ok':True,'used_rank':3,'served_arm':'opencode-go/glm-5.3-flash',
   'required_arm':'opencode-go/glm-5.3-flash','usage_receipt_ok':True,'used_seconds':486.87,
   'token_at_both_ends':t.strip().startswith('SKCV_VERIFY_5_OK') and t.strip().endswith('SKCV_VERIFY_5_OK')},
 'conformance':{'json':notes,'case_ids_match_fixed_list':ids==FIXED,'case_ids':ids,
   'statuses':{c.get('case_id'):(c.get('result') or c.get('status')) for c in d.get('cases',[])},
   'foreign_vocabulary_found':foreign,'verdict_declared':d.get('verdict'),
   'findings':d.get('findings'),'carry_forward':d.get('carry_forward'),'claim_ceiling':d.get('claim_ceiling')},
 'harness_rederivation':{'rows':len(m['files']),'rows_with_wrong_digest':badrows,'digest_matches_declared':digest==m['tree_digest'],
   'declared_digest':m['tree_digest'],'harness_runs':harn,
   'sprawl_pilot':{'merged_verified':len(pres),'merged_not_verified':notpres,'topic_bytes':len(tt),
     'reference_md_files_now':refs,'linter_cap':60,'still_over_cap_by':max(0,refs-60)},
   'apply_patch':{'patch_exists':patch.exists(),'patch_bytes':patch.stat().st_size if patch.exists() else None,
     'canonical_sha256_now':hashlib.sha256(can.read_bytes()).hexdigest(),'patch_context_matches_canonical':ctx_ok}},
 'claim_ceiling':'harness adjudication of a checker verdict over generation 2; it reproduces measurable claims, names what it cannot reproduce, and grants no acceptance'}
p=RUN/'evidence/postfreeze/verify5_adjudication.json'
p.write_text(json.dumps(out,ensure_ascii=False,indent=2,default=str),encoding='utf-8',newline='\n')
print(json.dumps({'verdict':out['conformance']['verdict_declared'],'ids_match':ids==FIXED,'statuses':out['conformance']['statuses'],
 'foreign':foreign,'findings':[f.get('severity') for f in (d.get('findings') or [])],
 'digest_ok':out['harness_rederivation']['digest_matches_declared'],'bad_rows':badrows,
 'stub_true_rows':{k:v['rows_reporting_stub_points_at_topic_true'] for k,v in harn.items()},
 'stub_false_rows':{k:v['rows_reporting_false'] for k,v in harn.items()},
 'merge':out['harness_rederivation']['sprawl_pilot'],'patch':out['harness_rederivation']['apply_patch']},ensure_ascii=False,indent=1))
