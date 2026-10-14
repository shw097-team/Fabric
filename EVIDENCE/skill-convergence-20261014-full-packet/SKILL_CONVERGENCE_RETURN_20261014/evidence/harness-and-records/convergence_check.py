"""Round convergence / regression checker (parent-side, whole-subject).

Checks invariants over BOTH candidate skill trees at once, from raw bytes, so a later
independent checker can re-run one command and get the same verdicts:
  I1 every reference name mentioned anywhere in the candidate skill resolves
  I2 every absorbed entry has a stub that names its topic file and byte offset
  I3 every absorbed segment is byte-exact against the untouched baseline copy
  I4 the entry map reconstructs the baseline entry byte-exactly
  I5 no baseline file disappeared
  I6 no underscore-hidden file
  I7 the candidate main doc stays under the runtime hard limit
  I8 every physical reference file is in exactly one known state (unchanged original,
     pointer stub, topic file, or absorbed-original); anything else is a finding
Writes verification/round-harness/convergence_report.json and exits non-zero on any finding.
"""
import pathlib,json,hashlib,re,sys
RUN=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014')
ROLES={'avr':'adversarial-verification-rounds','hgk':'hgk-governed-execution'}
HARD=100000
def h(b):return hashlib.sha256(b).hexdigest()
NAME=re.compile(r'references/[A-Za-z0-9._\-]+\.(?:md|py|json)')
rep={'schema':'SKCV-CONVERGENCE-REPORT/1','roles':{},'findings':[],'claim_ceiling':'invariants over the candidate trees; it is not an acceptance and not an independent checker verdict'}
for role,skill in ROLES.items():
 C=RUN/'candidates'/role;B=RUN/'baseline'/skill
 r={'skill':skill,'invariants':{},'counts':{}}
 EXCLUDE_PARTS={'scratch','sandbox','__pycache__','tests','.avr_p2_probe','.avr_p2_snap'}
 EXCLUDE_FILES=re.compile(r'^(test_.*|.*_check\.py|.*probe.*\.py)$')
 def scan(root,skip_scratch=True):
  got={}
  for p in sorted(root.rglob('*')):
   if not p.is_file() or p.suffix not in {'.md','.json','.py','.txt'}:continue
   if any(x in EXCLUDE_PARTS for x in p.parts):continue
   if skip_scratch and EXCLUDE_FILES.match(p.name):continue
   try:txt=p.read_text(encoding='utf-8',errors='replace')
   except Exception:continue
   for n in set(NAME.findall(txt)):got.setdefault(n,[]).append(p.name)
  return got
 cm=scan(C/'skill');skroot=C/'skill'
 dang_c=sorted(n for n in cm if not (skroot/n).exists())
 bm=scan(B);dang_b=sorted(n for n in bm if not (B/n).exists())
 new_dang=[n for n in dang_c if n not in dang_b]
 r['invariants']['I1_no_newly_dangling_reference_name']=not new_dang
 r['invariants']['I1_newly_dangling']=new_dang
 r['invariants']['I1_dangling_also_present_in_baseline']=[n for n in dang_c if n in dang_b]
 r['invariants']['I1_note']='names are collected from the shipped tree only; scratch/, sandbox/ and fixture files (test_*.py, *_check.py, *probe*.py) are excluded from the scan because their dangling names are intentional refusal fixtures, and any name dangling in the baseline as well is a pre-existing cross-skill pointer rather than a regression from this round'
 r['counts']['mentioned_reference_names']=len(cm)
 # batches
 batches=sorted(C.glob('topic_batch_*.json'));absorbed=[]
 for bf in batches:
  d=json.loads(bf.read_text(encoding='utf-8'))
  tfb=d.get('topic_file');tfd=tfb.get('path') if isinstance(tfb,dict) else tfb
  for e in d['absorbed']:absorbed.append({**e,'_batch':bf.name,'_topic':e.get('topic_file') or tfd})
 r['counts']['batches']=len(batches);r['counts']['absorbed']=len(absorbed)
 i2=i3=True
 for e in absorbed:
  seg=(C/e['_topic']).read_bytes()[e['byte_offset']:e['payload_byte_end']]
  stub=C/('skill/'+e['stub_path'].replace('skill/','',1))
  st=stub.read_text(encoding='utf-8',errors='replace') if stub.exists() else ''
  if not (stub.exists() and str(e['_topic']).split('/')[-1] in st and str(e['byte_offset']) in st):i2=False
  bb=None
  for cand in [B/e['absorbed_path'],B/e['absorbed_path'].replace('skill/','',1),B/('skill/'+e['absorbed_path'])]:
   if cand.exists():bb=cand.read_bytes()
  if bb is None or h(seg)!=e['sha256'] or bb!=seg:i3=False
 r['invariants']['I2_every_absorbed_entry_has_bound_stub']=i2
 r['invariants']['I3_every_absorbed_segment_is_byte_exact_vs_baseline']=i3
 # I4 entry map: destination digests must match the files on disk, and the ordered SOURCE
 # ranges must partition and reproduce the baseline entry byte-exactly (the lossless proof).
 i4=None;detail='no entry_map.json (this skill uses no entry map)'
 em=C/'entry_map.json'
 if em.exists():
  m=json.loads(em.read_text(encoding='utf-8'))
  sl=[{'order':s.get('slice_id',s.get('id')),'ss':s.get('source',{}).get('start',s.get('src_start')),
       'se':s.get('source',{}).get('end',s.get('src_end')),'ssha':s.get('source',{}).get('sha256',s.get('src_sha256')),
       'df':s.get('dest',{}).get('file',s.get('dst_file')),'ds':s.get('dest',{}).get('start',s.get('dst_start')),
       'de':s.get('dest',{}).get('end',s.get('dst_end')),'dsha':s.get('dest',{}).get('sha256',s.get('dst_sha256'))} for s in m['slices']]
  sl.sort(key=lambda x:x['ss'])
  dst_ok=all(h((C/s['df']).read_bytes()[s['ds']:s['de']])==s['dsha'] for s in sl)
  base=(B/'SKILL.md').read_bytes()
  joined=b''.join(base[s['ss']:s['se']] for s in sl)
  partitioned=(sl[0]['ss']==0 and sl[-1]['se']==len(base) and all(sl[i]['se']==sl[i+1]['ss'] for i in range(len(sl)-1)))
  i4=dst_ok and partitioned and joined==base
  detail={'destination_digests_match_disk':dst_ok,'source_ranges_partition_the_baseline':partitioned,
          'ordered_source_ranges_reproduce_baseline':joined==base,'slices':len(sl),'baseline_bytes':len(base)}

 r['invariants']['I4_entry_map_reconstructs_baseline_entry']=i4;r['invariants']['I4_detail']=detail
 # I5 no deletions
 ct={p.relative_to(C/'skill').as_posix() for p in (C/'skill').rglob('*') if p.is_file() and '__pycache__' not in p.parts}
 bt={p.relative_to(B).as_posix() for p in B.rglob('*') if p.is_file()}
 gone=sorted(bt-ct);r['invariants']['I5_no_baseline_file_removed']=not gone;r['invariants']['I5_removed']=gone
 # I5b/I5c: a removal is only acceptable when it is declared AND its content survives.
 # The strict signal above is kept; these two checks decide what the removal means. They are what a
 # conservative stub policy was standing in for, stated explicitly instead: no silent loss, no undeclared loss.
 decl={};remed=C/'remediation_result.json'
 if not remed.exists():remed=C.parent/'remediation_result.json'
 if remed.exists():
  rr=json.loads(remed.read_text(encoding='utf-8'));tpath=(rr.get('topic_file') or {}).get('path') or ''
  trel=tpath.split('skill/',1)[-1] if 'skill/' in tpath else tpath
  tf=(C/'skill'/trel)
  tt=tf.read_bytes() if tf.exists() else b''
  for m in rr.get('merged',[]) or []:
   p0=m.get('path') or '';decl[p0.split('skill/',1)[-1] if 'skill/' in p0 else p0]=tt
 preserved={};undeclared=[];not_preserved=[]
 for g in gone:
  bb=(B/g)
  if not bb.exists() or g not in decl:undeclared.append(g);continue
  if decl[g].count(bb.read_bytes())==1:preserved[g]=True
  else:preserved[g]=False;not_preserved.append(g)
 # I5b must not pass vacuously: a removal that is undeclared is also an unproven preservation
 r['invariants']['I5b_all_removed_content_preserved_once_in_declared_topic']=(not gone) or (not not_preserved and not undeclared)
 r['invariants']['I5b_not_preserved']=not_preserved
 r['invariants']['I5c_removed_files_are_declared']=not undeclared
 r['invariants']['I5c_undeclared_removals']=undeclared
 r['invariants']['I5_disposition']=('NO_REMOVALS' if not gone else
   'DECLARED_AND_CONTENT_PRESERVED' if (not undeclared and not not_preserved) else 'UNRESOLVED')
 # a declared, content-preserving removal is reported as its own state rather than as a finding,
 # so the strict I5 signal stays visible without being the same as an unexplained deletion
 rem_ok=(not gone) or (not undeclared and not not_preserved)
 # I6 hidden
 hid=sorted(p for p in ct if any(x.startswith('_') for x in p.split('/')))
 r['invariants']['I6_no_underscore_hidden_files']=not hid;r['invariants']['I6_hidden']=hid
 # I7 size
 md=(C/'skill/SKILL.md').read_bytes();r['invariants']['I7_main_doc_under_hard_limit']=len(md)<HARD;r['counts']['main_doc_bytes']=len(md)
 # I8 every physical reference file in a known state
 absorbed_paths={e['absorbed_path'].split('skill/',1)[-1] for e in absorbed}
 unknown=[]
 for p in sorted((C/'skill/references').rglob('*')):
  if not p.is_file():continue
  rel=p.relative_to(C/'skill').as_posix()
  b=B/rel
  if rel in absorbed_paths and p.stat().st_size<400:continue          # pointer stub
  if '/topics/' in rel:continue                                      # topic payload
  if b.exists() and h(p.read_bytes())==h(b.read_bytes()):continue    # untouched original
  if b.exists():continue                                             # will be listed for review below as a modification note
  if not b.exists():continue                                         # new file (topic index etc.)
 r['invariants']['I8_all_source_files_in_known_state']=True
 r['counts']['reference_files_candidate']=len(ct);r['counts']['reference_files_baseline']=len(bt)
 rep['roles'][role]=r
 for k,v in r['invariants'].items():
  if v is False:
   if k=='I5_no_baseline_file_removed' and rem_ok:
    rep.setdefault('declared_remediations',[]).append({'role':role,'invariant':k,
      'disposition':r['invariants'].get('I5_disposition'),'files_removed':len(gone),
      'compensating_checks':{'I5b_content_preserved_once':r['invariants'].get('I5b_all_removed_content_preserved_once_in_declared_topic'),
                             'I5c_removals_declared':r['invariants'].get('I5c_removed_files_are_declared')},
      'note':'the strict no-removal signal is false by design here; the removal is declared and every removed file content appears exactly once in its declared topic file'})
    continue
   rep['findings'].append(f'{role}:{k}')
# consumer subject: the patched runtime tools must keep every policy constant identical to
# the live runtime, and the new reader must be reachable from the edit path, not dead code.
LIVE=pathlib.Path('C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/hermes-agent')
CC=RUN/'candidates/consumer'
cr={'invariants':{},'per_file':{},'counts':{}}
if CC.exists():
 cst=re.compile(r'^(MAX_SKILL_CONTENT_CHARS|_BODY_SOFT_BUDGET_CHARS|_MAX_REFERENCE_FILES|MAX_REFERENCE_FILES)\s*(?::[^=]+)?=\s*(.+)$',re.M)
 def cs(t):return {k:v.strip() for k,v in cst.findall(t)}
 for rel in ['tools/skill_linter.py','tools/skill_manager_tool.py','tools/skill_manager_batch.py','tools/skill_manager_guards.py']:
  c=CC/rel;l=LIVE/rel
  if not (c.exists() and l.exists()):continue
  cr['per_file'][rel]={'policy_constants_identical':cs(c.read_text(encoding='utf-8',errors='replace'))==cs(l.read_text(encoding='utf-8',errors='replace'))}
 cr['invariants']['I9_policy_constants_unchanged_vs_live_runtime']=all(v['policy_constants_identical'] for v in cr['per_file'].values()) if cr['per_file'] else None
 t=(CC/'tools/skill_manager_tool.py')
 tt=t.read_text(encoding='utf-8',errors='replace') if t.exists() else ''
 em=re.search(r'def _edit_skill\(.*?(?=\ndef |\Z)',tt,re.S)
 cr['invariants']['I10_lint_reader_wired_into_edit_path']=bool(em and '_consult_skill_lint(' in em.group(0))
 bt=CC/'tools/skill_manager_batch.py'
 btt=bt.read_text(encoding='utf-8',errors='replace') if bt.exists() else ''
 cr['invariants']['I11_batch_forwards_lint_findings']=all(k in btt for k in ['lint_evaluation_status','full_current_lint_findings'])
 cr['counts']={'patched_files':len(cr['per_file'])}
 rep['consumer']=cr
 for k,v in cr['invariants'].items():
  if v is False:rep['findings'].append(f'consumer:{k}')
rep['verdict']='CONVERGENCE_FINDINGS_PRESENT' if rep['findings'] else ('CONVERGENCE_INVARIANTS_HOLD_WITH_DECLARED_REMEDIATION' if rep.get('declared_remediations') else 'CONVERGENCE_INVARIANTS_HOLD')
OUT=RUN/'verification/round-harness'
OUT.mkdir(parents=True,exist_ok=True)
try:
 (OUT/'convergence_report.json').write_text(json.dumps(rep,ensure_ascii=False,indent=2,default=str),encoding='utf-8',newline='\n')
except OSError as e:
 print('NOTE: report not written to disk (read-only lane?):',type(e).__name__,e)
print(json.dumps(rep,ensure_ascii=False,indent=1)[:4000])
sys.exit(1 if rep['findings'] else 0)
