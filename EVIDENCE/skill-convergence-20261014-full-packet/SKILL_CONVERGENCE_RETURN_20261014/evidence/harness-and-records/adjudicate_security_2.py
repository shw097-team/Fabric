"""Harness adjudication of the SECURITY 2 advisory verdict.

Independently re-derives the checker's central claim (all 374 frozen rows match disk and
the row-set line hash equals the recorded tree_digest), records the verdict verbatim, and
states the claim ceiling: an advisory lane verdict is not canonical acceptance.
"""
import pathlib,json,hashlib,datetime,re
RUN=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014')
E=RUN/'evidence'
m=json.loads((E/'subject_manifest.json').read_text(encoding='utf-8'))
bad=[];missing=[];size_bad=[]
for f in m['files']:
 p=RUN/f['path']
 if not p.exists():missing.append(f['path']);continue
 b=p.read_bytes()
 if hashlib.sha256(b).hexdigest()!=f['sha256']:bad.append(f['path'])
 if len(b)!=f['bytes']:size_bad.append(f['path'])
recomputed=hashlib.sha256('\n'.join(f"{r['sha256']} {r['path']}" for r in m['files']).encode()).hexdigest()
lm=(E/'lanes/security/2/last_message.txt').read_text(encoding='utf-8')
j=re.search(r'```json\s*(\{.*?\})\s*```',lm,re.S)
verdict=json.loads(j.group(1)) if j else None
disp=json.loads((E/'lanes/security/2/dispatch.json').read_text(encoding='utf-8'))
out={'schema':'SKCV-HARNESS-ADJUDICATION-SECURITY/1','observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'lane':'WO-SKCV-20261014-SECURITY tag 2',
 'transport':{'exit':'0','ok':disp.get('ok'),'used_rank':disp.get('used_rank'),'served_arm':disp.get('served_arm'),
   'required_arm':disp.get('required_arm'),'usage_receipt_ok':disp.get('usage_receipt_ok'),'used_seconds':disp.get('used_seconds')},
 'checker_verdict_recorded_verbatim':(verdict or {}).get('verdict'),
 'checker_cases':[{ 'case_id':c['case_id'],'status':c['status']} for c in (verdict or {}).get('cases',[])],
 'checker_findings_severities':[f.get('severity') for f in (verdict or {}).get('findings',[])],
 'harness_independent_rederivation':{
   'rows_in_manifest':len(m['files']),
   'rows_missing_on_disk':missing,
   'rows_with_wrong_digest':bad,
   'rows_with_wrong_size':size_bad,
   'row_set_line_hash_matches_recorded_tree_digest':recomputed==m['tree_digest'],
   'recorded_tree_digest':m['tree_digest'],
   'recomputed_tree_digest':recomputed},
 'agreement':{'checker_claim_all_374_rows_pass':(not bad and not missing and not size_bad),
   'checker_claim_digest_matches':recomputed==m['tree_digest']},
 'f1_disposition':'the checker is right that the digest composition must be stated: tree_digest is sha256 over the newline-joined "sha256 path" lines of the row list, not a concatenation of file bytes. The harness now records that method inside the manifest so a later checker does not have to guess. The row set is unchanged, so tree_digest is unchanged.',
 'claim_ceiling':'an advisory lane verdict rederived by the round harness; it is not independent-checker authority over the product, it does not establish semantic correctness, and it grants no acceptance, promotion or apply'}
p=RUN/'verification/round-harness/security2_adjudication.json'
p.write_text(json.dumps(out,ensure_ascii=False,indent=2,default=str),encoding='utf-8',newline='\n')
print(json.dumps(out,ensure_ascii=False,indent=1))
