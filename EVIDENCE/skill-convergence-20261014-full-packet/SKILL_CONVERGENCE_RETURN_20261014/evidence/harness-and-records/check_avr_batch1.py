"""Independent check of the AVR topic-batch-1 lossless claim.

Does NOT call the maker's topic_check.py. Rebuilds the claim from raw bytes:
for every absorbed entry, the topic-file byte range must hash to the entry digest AND to
the digest of the unchanged baseline copy of that reference; every stub must point at its
original; every link in the candidate SKILL.md must resolve; nothing may have been deleted.
"""
import pathlib,json,hashlib,re,sys
C=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014/candidates/avr')
B=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014/baseline/adversarial-verification-rounds')
def h(b):return hashlib.sha256(b).hexdigest()
batch=json.loads((C/'topic_batch_1.json').read_text(encoding='utf-8'))
rows=[];ok=True
for e in batch['absorbed']:
 tf=C/e['topic_file'];raw=tf.read_bytes()
 seg=raw[e['byte_offset']:e['payload_byte_end']]
 base=B/e['absorbed_path'].replace('references/','references/',1)
 base2=B/(e['absorbed_path'])
 base_bytes=base2.read_bytes() if base2.exists() else None
 stub=C/e['stub_path']
 stub_txt=stub.read_text(encoding='utf-8',errors='replace') if stub.exists() else ''
 r={'path':e['absorbed_path'],'claim_bytes':e['bytes'],
    'segment_bytes':len(seg),'segment_sha':h(seg)[:16],'claim_sha':e['sha256'][:16],
    'segment_matches_claim':h(seg)==e['sha256'],
    'baseline_bytes':len(base_bytes) if base_bytes is not None else None,
    'baseline_matches_segment':(base_bytes==seg) if base_bytes is not None else None,
    'stub_exists':stub.exists(),'stub_mentions_topic':e['topic_file'].split('/')[-1] in stub_txt,
    'stub_bytes':len(stub_txt.encode('utf-8'))}
 if not (r['segment_matches_claim'] and r['baseline_matches_segment'] and r['stub_exists']):ok=False
 rows.append(r)
# link resolution in the candidate main doc
md=(C/'skill/SKILL.md').read_text(encoding='utf-8',errors='replace')
links=re.findall(r'\]\(([^)\s]+)\)',md)
bad=[];ext=[]
for L in links:
 if L.startswith(('http://','https://','#')):ext.append(L);continue
 tgt=(C/'skill'/L) if not L.startswith('skill/') else (C/L.split('skill/',1)[1] if False else C/L)
 cand=[C/'skill'/L, C/L, C/'skill'/L.replace('./','')]
 if not any(p.exists() for p in cand):bad.append(L)
# baseline vs candidate file sets
bt={p.relative_to(B).as_posix() for p in B.rglob('*') if p.is_file()}
ct={p.relative_to(C/'skill').as_posix() for p in (C/'skill').rglob('*') if p.is_file()}
deleted=sorted(bt-ct);added=sorted(ct-bt)
underscore=sorted(p for p in ct if any(part.startswith('_') for part in p.split('/')))
out={'schema':'SKCV-INDEP-TOPIC-BATCH-CHECK/1','checker':'round harness (independent of maker topic_check.py)',
 'batch_scope':batch.get('batch_scope'),'absorbed_entries':len(rows),'all_absorbed_lossless':ok,'rows':rows,
 'links_total':len(links),'links_external_or_anchor':len(ext),'links_unresolved':bad,
 'files_deleted_vs_baseline':deleted,'files_added_vs_baseline':added,
 'underscore_prefixed_files':underscore,
 'claim_ceiling':'checks byte-level losslessness of the absorbed segments and link/stub integrity for THIS batch only; it says nothing about the remaining theme groups, about the deferred entry-only references relative to the live skill, or about any acceptance'}
print(json.dumps(out,ensure_ascii=False,indent=1))
