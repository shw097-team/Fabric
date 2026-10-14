"""Harness verification of the HGK sprawl pilot, from bytes on disk.

Independent of the maker's self-report: the merged originals are located in the topic file and compared
against their baseline copies where those exist, so byte identity is checked two ways - against the
baseline file content and against the digest the lane recorded before deleting.
"""
import pathlib,json,hashlib,re,datetime
RUN=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014')
C=RUN/'candidates/hgk/skill'; B=RUN/'baseline/hgk-governed-execution'
res=json.loads((RUN/'candidates/hgk/remediation_result.json').read_text(encoding='utf-8'))
def md(d):return {p.relative_to(d).as_posix():p for p in d.rglob('*.md') if not any(x.startswith('_') for x in p.relative_to(d).parts)}
now=md(C)
topic=res.get('topic_file',{}).get('path') or 'references/topics/lane-bootstrap-and-guard-notes.md'
rel_topic=topic.split('skill/',1)[-1] if 'skill/' in topic else topic.lstrip('/')
tp=C/rel_topic
print('topic_used',rel_topic,'exists',tp.exists())
ttext=tp.read_bytes()
rows=[];bad=[]
for mrec in res.get('merged',[]):
    p=mrec.get('path');rel=p[4:] if p.startswith('skill/') else p
    bb=(B/rel)
    base_bytes=bb.read_bytes() if bb.exists() else None
    in_topic=ttext.count(base_bytes)==1 if base_bytes is not None else None
    digest_hit=False
    if base_bytes is not None:
        digest_hit=hashlib.sha256(base_bytes).hexdigest()==mrec.get('sha256_before')
    rows.append({'path':rel,'bytes_claimed':mrec.get('bytes_before'),'baseline_copy_exists':base_bytes is not None,
      'baseline_bytes':len(base_bytes) if base_bytes is not None else None,
      'baseline_shares_recorded_digest':digest_hit,'content_appears_once_in_topic':in_topic,
      'original_gone_as_file':not (C/rel).exists()})
    if base_bytes is not None and (not in_topic or not digest_hit):bad.append(rel)
main_now=(C/'SKILL.md').read_bytes()
refs_now=len(now)
out={'schema':'SKCV-HARNESS-ADJUDICATION-HGK7/1','observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'lane':'WO-SCV... HGK tag 7','transport':{'exit':'0','ok':True,'used_rank':1,'served_arm':'opencode-go/deepseek-v4.1-flash',
   'required_arm':'opencode-go/deepseek-v4.1-flash','usage_receipt_ok':True,'used_seconds':341.2},
 'merges_verified':len(rows),'merges_with_byte_problems':bad,'rows':rows,
 'topic_file':{'path':topic,'bytes':len(ttext),'sha256':hashlib.sha256(ttext).hexdigest()[:16],
   'headings':re.findall(r'^## (references/[^\n]+)$',ttext.decode('utf-8',errors='replace'),re.M)[:20]},
 'counts':{'references_md_now':refs_now,'claimed_before':res.get('counts',{}).get('references_md_before'),
   'claimed_after':res.get('counts',{}).get('references_md_after'),
   'linter_cap':60,'still_over_cap':refs_now>60,'over_by':max(0,refs_now-60)},
 'main_doc_unchanged':{'recorded_before':res.get('sha256_of_skill_md_before'),'recorded_after':res.get('sha256_of_skill_md_after'),
   'actual_now':hashlib.sha256(main_now).hexdigest(),'equal':res.get('sha256_of_skill_md_before')==hashlib.sha256(main_now).hexdigest()},
 'stubs_created_claimed':res.get('stubs_created'),'deleted_claimed':len(res.get('deleted',[]) or []),
 'claim_ceiling':'harness verification of a bounded candidate edit; it checks byte identity and count, not semantic quality, and grants no acceptance'}
(RUN/'evidence/postfreeze/hgk7_adjudication.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,default=str),encoding='utf-8',newline='\n')
print(json.dumps({'merges':len(rows),'problems':bad,'refs_now':refs_now,'over_cap_by':out['counts']['over_by'],
 'main_unchanged':out['main_doc_unchanged']['equal'],'topic_bytes':len(ttext),
 'headings':len(out['topic_file']['headings']),'deleted_claimed':out['deleted_claimed'],'stubs':out['stubs_created_claimed']},ensure_ascii=False,indent=1))
