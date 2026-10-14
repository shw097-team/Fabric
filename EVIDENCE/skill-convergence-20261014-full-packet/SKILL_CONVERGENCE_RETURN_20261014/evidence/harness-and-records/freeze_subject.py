"""Build an immutable verification subject manifest for this round.

Deterministic: same inputs -> same manifest bytes. Volatile coordination/log paths are
excluded by an explicit, printed rule so a reader can see exactly what is in and out of
the freeze, instead of assuming.
"""
import pathlib,json,hashlib,sys,datetime
R=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS');RUN=R/'var/SKILL-CONVERGENCE-20261014';E=RUN/'evidence'
OUT=E/'subject_manifest.json'
EXCLUDE_PARTS={'__pycache__','_pytest_tmp','pytest-tmp','.pytest_cache','_lintcheck','_lintcheck2','_scratch','tests/_work','trace','raw','scratch','sandbox','_work_p2','_work_dbg','_blobdbg','.avr_p2_probe','.avr_p2_snap','rollback_drill'}
EXCLUDE_NAMES={'driver.json','dispatch.json','security2_adjudication.json'}
EXCLUDE_GLOB=set()
INCLUDE_ROOTS=[RUN/'candidates',RUN/'baseline',RUN/'qualification',RUN/'verification/round-harness']
INCLUDE_FILES=[E/'verification_contract.json',E/'qualification_receipt.json',E/'execution_bindings.json',
               E/'gstack_route_receipt.json',E/'continuation_turn_record.py',
               E/'convergence_check.py',E/'check_topic_batch.py',E/'rollback_drill.py',E/'status_check.py',
               E/'global_baseline.json',E/'subject_binding.json',E/'timeout_class_remediation.json']
def rel(p):
 try:return p.relative_to(RUN).as_posix()
 except ValueError:return str(p)
def excluded(p):
 parts=set(p.parts)
 if parts & EXCLUDE_PARTS:return 'excluded_dir_or_fixture_work'
 if any(x in rel(p) for x in ('tests/_work/','_scratch/','_lintcheck2/')):return 'excluded_dir_or_fixture_work'
 if p.name in EXCLUDE_NAMES:return 'excluded_volatile_coordination_file'
 for g in EXCLUDE_GLOB:
  if p.match(g):return 'excluded_post_freeze_harness_receipt'
 if p.suffix in {'.pyc','.log'}:return 'excluded_volatile_log_or_bytecode'
 return None
rows=[];skipped=[]
for root in INCLUDE_ROOTS:
 if not root.exists():continue
 for p in sorted(root.rglob('*')):
  if not p.is_file():continue
  r=excluded(p)
  if r:skipped.append({'path':rel(p),'reason':r});continue
  rows.append({'path':rel(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
for p in INCLUDE_FILES:
 if p.exists():
  rows.append({'path':rel(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
rows.sort(key=lambda x:x['path'])
manifest={'kind':'SKILL-CONVERGENCE-20261014 verification subject manifest',
 'generated_from':'frozen candidate/baseline/qualification trees plus named control evidence files',
 'inclusion_rule':'every regular file under candidates/, baseline/ and qualification/, plus the named control evidence files listed in INCLUDE_FILES',
 'exclusion_rule':'directory parts __pycache__/_pytest_tmp/pytest-tmp/.pytest_cache/_lintcheck*/_scratch/scratch/sandbox/_work_p2/_work_dbg/_blobdbg/.avr_p2_probe/.avr_p2_snap and paths tests/_work/, trace/, raw/, rollback_drill/, files named driver.json or dispatch.json, and .pyc/.log files — excluded because they are volatile coordination, log, sandbox-copy or fixture-work artefacts rather than subject bytes',
 'excluded_count':len(skipped),'excluded':skipped,
 'file_count':len(rows),'files':rows,
 'tree_digest':hashlib.sha256('\n'.join(f"{r['sha256']} {r['path']}" for r in rows).encode()).hexdigest(),
 'digest_method':"tree_digest = sha256( '\\n'.join( f\"{row.sha256} {row.path}\" for row in files ) ) — a hash over the newline-joined 'digest path' lines of the row list, NOT a concatenation of file bytes. A checker must use this composition; hashing concatenated file bytes will not reproduce it.",
 'semantic_freeze':False,
 'honesty_note':'this is a byte-level manifest of the executed files; it is not a semantic freeze and does not assert that every included file is correct, only that its bytes are fixed for the checker'}
payload=json.dumps(manifest,ensure_ascii=False,indent=2,sort_keys=False)
OUT.write_text(payload,encoding='utf-8',newline='\n')
print(json.dumps({'manifest':str(OUT),'file_count':len(rows),'excluded_count':len(skipped),'tree_digest':manifest['tree_digest']},indent=2))
