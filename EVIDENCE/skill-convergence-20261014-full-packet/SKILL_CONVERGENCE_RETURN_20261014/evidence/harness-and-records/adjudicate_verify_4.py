"""Corrected VERIFY 4 adjudication.

Corrections over the first attempt, both of them my own bugs and both disclosed:
 - the harness invocations converted the role and batch arguments into absolute paths, so the
   three batch checks were run with wrong arguments and their exit 1 was mine, not the harness's;
 - the AVR entry map keys its slice source as src_start / src_end, not source.start / source.end,
   so the first AVR reconstruction silently hashed the whole file ten times (1,014,880 bytes).
The reconstruction below handles both map shapes and reports the mutation behaviour directly.
"""
import pathlib,json,hashlib,re,datetime,subprocess
RUN=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014')
PY='C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe'
L=RUN/'evidence/lanes/verify/4'
FIXED=['SUBJECT-BINDING','HARNESS-CONVERGENCE','HARNESS-AVR-BATCH1','HARNESS-HGK-BATCH1','HARNESS-HGK-BATCH2',
 'RECONSTRUCTION-AVR','RECONSTRUCTION-HGK','RECONSTRUCTION-MUTATIONS','C1-EXTRACTION','C2-THEMES','C3-CONSUMER',
 'C4-ROLLBACK','C5-POLICY','COVERAGE']
FOREIGN=['V4.2','currency-like','reinjected','Ladder 550','anti-LOX','ratchet']
t=(L/'last_message.txt').read_text(encoding='utf-8')
raw=t[t.find('{',t.find('```json')):]
depth=0;end=None
for n,ch in enumerate(raw):
    if ch=='{':depth+=1
    elif ch=='}':
        depth-=1
        if depth==0:end=n+1;break
d=json.loads(raw[:end])
ids=[c.get('case_id') for c in d['cases']]
statuses={c.get('case_id'):(c.get('result') or c.get('status')) for c in d['cases']}
foreign=[w for w in FOREIGN if w.lower() in json.dumps(d,ensure_ascii=False).lower()]
def slices(role):
    em=json.loads((RUN/f'candidates/{role}/entry_map.json').read_text(encoding='utf-8'))
    out=[]
    for s in em['slices']:
        if 'src_start' in s: out.append((s['src_start'],s['src_end'],s['id']))
        else: out.append((s['source']['start'],s['source']['end'],s.get('slice_id')))
    return out
def recon(role,mutate=None):
    base=(RUN/f'baseline/{"adversarial-verification-rounds" if role=="avr" else "hgk-governed-execution"}/SKILL.md').read_bytes()
    sl=slices(role)
    parts=[]
    for idx,(a,z,sid) in enumerate(sl):
        seg=base[a:z]
        if mutate=='flip' and idx==0 and seg: seg=bytes([seg[0]^0x01])+seg[1:]
        parts.append((idx,sid,seg))
    if mutate=='drop': parts=parts[:-1]
    if mutate=='swap' and len(parts)>=2: parts[0],parts[1]=parts[1],parts[0]
    cat=b''.join(p[2] for p in parts)
    return {'slices':len(sl),'bytes':len(cat),'sha16':hashlib.sha256(cat).hexdigest()[:16],'equals_baseline':cat==base,
            'baseline_bytes':len(base),'baseline_sha16':hashlib.sha256(base).hexdigest()[:16]}
m=json.loads((RUN/'evidence/subject_manifest.json').read_text(encoding='utf-8'))
digest=hashlib.sha256('\n'.join(f"{r['sha256']} {r['path']}" for r in m['files']).encode()).hexdigest()
bad=sum(1 for r in m['files'] if hashlib.sha256((RUN/r['path']).read_bytes()).hexdigest()!=r['sha256'])
harn={}
for name,script,args in (('convergence','evidence/convergence_check.py',[]),
    ('avr_batch1','evidence/check_topic_batch.py',['avr','topic_batch_1.json']),
    ('hgk_batch1','evidence/check_topic_batch.py',['hgk','topic_batch_1.json']),
    ('hgk_batch2','evidence/check_topic_batch.py',['hgk','topic_batch_2.json'])):
    p=subprocess.run([PY,str(RUN/script)]+args,cwd=str(RUN),capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=600)
    o=p.stdout or ''
    harn[name]={'exit':p.returncode,'all_absorbed_lossless':'"all_absorbed_lossless": true' in o,
      'verdict_token':('CONVERGENCE_INVARIANTS_HOLD' if 'CONVERGENCE_INVARIANTS_HOLD' in o else None)}
res={'avr':recon('avr'),'hgk':recon('hgk')}
mut={'drop':{r:recon(r,'drop')['equals_baseline'] for r in ('avr','hgk')},
     'swap':{r:recon(r,'swap')['equals_baseline'] for r in ('avr','hgk')},
     'flip':{r:recon(r,'flip')['equals_baseline'] for r in ('avr','hgk')}}
out={'schema':'SKCV-HARNESS-ADJUDICATION-VERIFY4/2','observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'lane':'WO-SKCV-20261014-VERIFY tag 4',
 'transport':{'exit':'0','ok':True,'used_rank':3,'served_arm':'opencode-go/glm-5.3-flash','required_arm':'opencode-go/glm-5.3-flash',
   'usage_receipt_ok':True,'used_seconds':451.69},
 'conformance':{'json_parsed':'clean, no repair needed','case_ids_match_fixed_list':ids==FIXED,'case_statuses':statuses,
   'foreign_vocabulary_found':foreign,'findings':d.get('findings'),'verdict_declared':d.get('verdict'),
   'coverage_status':statuses.get('COVERAGE'),
   'carry_forward':d.get('carry_forward'),'claim_ceiling':d.get('claim_ceiling')},
 'harness_rederivation':{'rows':len(m['files']),'rows_with_wrong_digest':bad,'digest_matches_declared':digest==m['tree_digest'],
   'reconstruction_clean':res,'mutation_detection_equals_baseline':mut,
   'mutations_all_detected':all(not v for r in mut.values() for v in r.values()),
   'harness_runs':harn},
 'harness_defects_observed_this_round':[
   {'id':'H1','where':'evidence/check_topic_batch.py line 31','symptom':'stub_points_at_topic reports false for every row',
    'diagnosis':"str(pathlib.Path) renders with backslashes on Windows, so str(tfd).split('/')[-1] returns the whole path and never matches the stub text",
    'effect_on_verdict':'none: the ok computation uses segment_matches_claim, baseline_equals_segment and stub_exists only; the headline all_absorbed_lossless is unaffected',
    'independent_confirmation':"reading the stub directly shows the topic path it names, and stub_points_at_offset is true",
    'status':'not repaired in place; the file is inside the frozen row set, so editing it now would invalidate the digest every running checker binds'}],
 'my_own_errors_corrected':['the first adjudication passed absolute paths as the role and batch arguments, so the three batch harnesses were invoked wrongly and their exit 1 was mine; with correct arguments all four harnesses exit 0',
   "the first AVR reconstruction used the HGK map shape, so it hashed the whole file ten times and reported 1,014,880 bytes; with the AVR keys (src_start, src_end) the reconstruction is byte-exact"],
 'claim_ceiling':'harness adjudication of a checker verdict over a frozen generation; it reproduces measurable claims and grants no acceptance, no promotion and no apply'}
(RUN/'evidence/postfreeze/verify4_adjudication.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,default=str),encoding='utf-8',newline='\n')
print(json.dumps({'verdict':out['conformance']['verdict_declared'],'case_ids_match':out['conformance']['case_ids_match_fixed_list'],
 'statuses':statuses,'foreign':foreign,'findings_severity':[f.get('severity') for f in d.get('findings',[])],
 'recon':res,'mutations':mut,'mutations_all_detected':out['harness_rederivation']['mutations_all_detected'],
 'harness':harn,'digest_ok':out['harness_rederivation']['digest_matches_declared'],'bad_rows':bad},ensure_ascii=False,indent=1))
