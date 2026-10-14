"""Generalised independent batch check used by the round harness.

Same method that confirmed the AVR batch: rebuild the lossless claim from raw bytes and
compare against the untouched baseline copy of each absorbed reference. Usage:
  python check_topic_batch.py <role> <batch_json_name>
"""
import pathlib,json,hashlib,re,sys
RUN=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014')
BASE={'avr':'adversarial-verification-rounds','hgk':'hgk-governed-execution'}
role=sys.argv[1];batch_name=sys.argv[2] if len(sys.argv)>2 else 'topic_batch_1.json'
C=RUN/'candidates'/role;B=RUN/'baseline'/BASE[role]
def h(b):return hashlib.sha256(b).hexdigest()
def base_bytes(rel):
 for cand in [B/rel, B/rel.replace('skill/','',1), B/('skill/'+rel)]:
  if cand.exists():return cand.read_bytes(),cand
 return None,None
batch=json.loads((C/batch_name).read_text(encoding='utf-8'))
tfb=batch.get('topic_file');tfd=tfb.get('path') if isinstance(tfb,dict) else tfb
rows=[];ok=True
for e in batch['absorbed']:
 tf=C/(e.get('topic_file') or tfd);raw=tf.read_bytes() if tf.exists() else b''
 seg=raw[e['byte_offset']:e['payload_byte_end']]
 bb,bp=base_bytes(e['absorbed_path'])
 stub=C/('skill/'+e['stub_path'].replace('skill/','',1))
 st=stub.read_text(encoding='utf-8',errors='replace') if stub.exists() else ''
 r={'path':e['absorbed_path'],'claim_bytes':e['bytes'],'segment_bytes':len(seg),
    'segment_matches_claim':h(seg)==e['sha256'],
    'baseline_bytes':len(bb) if bb is not None else None,
    'baseline_equals_segment':(bb==seg) if bb is not None else None,
    'stub_exists':stub.exists(),'stub_bytes':len(st.encode('utf-8')),
    'stub_points_at_topic':tf.name in st,
    'stub_points_at_offset':str(e['byte_offset']) in st}
 if not (r['segment_matches_claim'] and r['baseline_equals_segment'] and r['stub_exists']):ok=False
 rows.append(r)
PAT=re.compile(r'references/[A-Za-z0-9._\-]+\.(md|py|json)')
md=(C/'skill/SKILL.md').read_text(encoding='utf-8',errors='replace')
bmd=(B/'SKILL.md').read_text(encoding='utf-8',errors='replace')
named=sorted(set(PAT.findall(md)));bnamed=sorted(set(PAT.findall(bmd)))
resolve={n:(C/'skill'/n).exists() for n in named if n.endswith('.md')}
ct={p.relative_to(C/'skill').as_posix() for p in (C/'skill').rglob('*') if p.is_file() and '__pycache__' not in p.parts}
bt={p.relative_to(B).as_posix() for p in B.rglob('*') if p.is_file()}
rem=(C/'skill/references/topic-source-remainder.md')
remtxt=rem.read_text(encoding='utf-8',errors='replace') if rem.exists() else ''
unnamed=[n for n in bnamed if n not in named and n.endswith('.md')]
out={'schema':'SKCV-INDEP-HARNESS-BATCH-CHECK/1','role':role,'batch':batch_name,
 'batch_scope':batch.get('batch_scope'),'absorbed_entries':len(rows),'all_absorbed_lossless':ok,'rows':rows,
 'named_paths_in_main_doc':len(named),'named_md_paths_all_resolve':all(resolve.values()),
 'unresolved_named_md_paths':[k for k,v in resolve.items() if not v],
 'baseline_named_md_no_longer_named':unnamed,
 'unnamed_baseline_refs_present_in_topic_source_remainder':{n:(n in remtxt) for n in unnamed},
 'files_deleted_vs_baseline':sorted(bt-ct),'files_added_vs_baseline':sorted(ct-bt),
 'underscore_prefixed_files':sorted(p for p in ct if any(x.startswith('_') for x in p.split('/'))),
 'physical_counts':{'baseline':len(bt),'candidate':len(ct)},
 'claim_ceiling':'byte-level losslessness and structure for this batch only, recomputed by the round harness; it is not independent-checker authority and grants no acceptance'}
print(json.dumps(out,ensure_ascii=False,indent=1))
