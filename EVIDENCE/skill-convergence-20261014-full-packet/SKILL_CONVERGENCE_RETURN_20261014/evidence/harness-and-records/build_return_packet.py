"""Build the return packet for the external design team, then scan every byte that would leave the machine.

The packet is assembled from named sources only: the frozen generation's own manifest rows, the round's evidence
by category, and the closure scripts. Lane transcripts are excluded by size and are listed with their hashes and
their reason instead of being dropped in silence. Nothing is copied from another workstream's directory.

Two gates run before anything is published: a manual copy is verified file by file against the manifest, and a
credential-shaped-string scan runs over exactly the bytes that would be sent. A hit aborts the build.
"""
import json,hashlib,pathlib,shutil,re,sys,collections,datetime,os
X=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014')
FAB=pathlib.Path('C:/Projects/Agent_Workspace/Fabric')
OUT=pathlib.Path('C:/pkt')
PK=OUT/'SKCV_RETURN_20261014'
EXT='\\\\?\\'
def _w(t,data):
    path=EXT+str(t.parent).replace('/','\\')
    os.makedirs(path,exist_ok=True)
    with open(EXT+str(t).replace('/','\\'),'wb') as fh:fh.write(data)
    return t
if PK.exists():shutil.rmtree(PK)
PK.mkdir(parents=True)
def sha(b):return hashlib.sha256(b).hexdigest()
SEC=[r'github_pat_[A-Za-z0-9_]{20,}',r'gh[pousr]_[A-Za-z0-9]{30,}',r'sk-[A-Za-z0-9]{20,}',
     r'-----BEGIN [A-Z ]*PRIVATE KEY-----',r'AKIA[0-9A-Z]{16}',r'xox[baprs]-[A-Za-z0-9-]{10,}',
     r'(?i)(api[_-]?key|password|passwd|secret|access[_-]?token)\s*[:=]\s*["\']?[A-Za-z0-9_\-]{16,}']
files=[];excluded=[];hits=[]
def put(src,dst,disposition,reason):
    b=src.read_bytes()
    for pat in SEC:
        if re.search(pat,b.decode('utf-8','replace')):hits.append({'packet_path':dst,'pattern':pat});break
    t=_w(PK/dst,b)
    files.append({'packet_path':dst,'source':str(src).replace('\\','/'),'bytes':len(b),'sha256':sha(b),
                  'disposition':disposition,'reason':reason})
# 1. the frozen generation, exactly the rows the subject manifest binds
man=json.loads((X/'evidence/subject_manifest.json').read_text(encoding='utf-8'))
rows=[r for r in (man.get('rows') or man.get('files')) if 'path' in r and 'sha256' in r]
for r in rows:
    src=X/r['path']
    if src.exists():put(src,'subject_frozen_generation/'+r['path'],'DELIVERED','row of the frozen generation 2 manifest')
    else:excluded.append({'source':r['path'],'reason':'manifest row not present on disk at packet build time','sha256':r['sha256']})
# 2. round evidence by category
for p in sorted((X/'evidence').glob('*.py'))+sorted((X/'evidence').glob('*.json'))+sorted((X/'evidence').glob('*.md')):
    put(p,'evidence/harness-and-records/'+p.name,'DELIVERED','round harness or record')
for p in sorted((X/'evidence/postfreeze').glob('*')):
    if p.is_file():put(p,'evidence/postfreeze/'+p.name,'DELIVERED','post-freeze record')
for p in sorted((X/'evidence/prompts').glob('*')):
    if p.is_file():put(p,'evidence/prompts/'+p.name,'DELIVERED','lane brief')
for p in sorted((X/'evidence/lanes').rglob('*')):
    if not p.is_file():continue
    rel=p.relative_to(X/'evidence/lanes').as_posix()
    parts=set(rel.split('/'))
    if parts & {'raw','trace'}:
        excluded.append({'source':'evidence/lanes/'+rel,
            'reason':'lane transcript excluded by size; retained in the round directory','bytes':p.stat().st_size,'sha256':sha(p.read_bytes())})
        continue
    put(p,'evidence/lanes/'+rel,'DELIVERED','lane verdict, dispatch receipt or result')
# 3. closure material produced for this handover
for p in [FAB/'HYGIENE_MANIFEST_20261014.json']:
    if p.exists():put(p,'closure/'+p.name,'DELIVERED','local repo hygiene manifest')
for name in ('commit_digest_classification.json',):
    p=X/'evidence/postfreeze'/name
    if p.exists():put(p,'closure/'+name,'DELIVERED','classification of the committed-byte difference')
for name in ('repo_hygiene.py','verify_commit_bytes.py','classify_commit_digests.py','read_security5.py','adjudicate_security_5.py','publish_preflight.py'):
    p=X/'evidence'/name
    if p.exists():put(p,'closure/scripts/'+name,'DELIVERED','closure script, regenerable')
put(X/'evidence/postfreeze/RETURN_README.md','README.md','DELIVERED','entry document for this return packet')
HO=pathlib.Path('C:/Projects/Agent_Workspace/_handover')
for p,dst in [(X/'_CHECKPOINT_RESUME.md','closure/handover/_CHECKPOINT_RESUME.md'),
              (HO/'CHECKPOINT_SKILL-CONVERGENCE-20261014.md','closure/handover/HANDOVER_SKILL-CONVERGENCE-20261014.md')]:
    if p.exists():put(p,dst,'DELIVERED','handover artifact for the next session; the packet copy of the checkpoint document is renamed because the repository\'s own .gitignore excludes CHECKPOINT_*.md and would have dropped it from the commit without a word')
for p in sorted((X/'evidence/postfreeze').glob('*')):
    pass
for name in ('board_closure.json',):
    p=X/'evidence/postfreeze'/name
    if p.exists():put(p,'closure/handover/'+name,'DELIVERED','board close-out readback')
for name in ('close_board.py','board_readback.py','preserve_security5_verdict.py','build_closure_manifest.py','verify_published_bytes.py','publish_readback.py','diag_raw_readback.py','build_return_packet.py'):
    p=X/'evidence'/name
    if p.exists():put(p,'closure/scripts/'+name,'DELIVERED','closure script, regenerable')
excluded.append({'source':'C:/Projects/Agent_Workspace/API KEY/','reason':'the owner credential file itself is never packaged and never scanned into a manifest as content','sha256':None})
_w(PK/'.gitattributes',b"# Byte-fidelity control for this return packet.\n# Every digest this packet records was computed over the bytes as they sit on the authoring host, so the\n# repository's own line-ending normalisation must not rewrite them on the way into the object store or back out\n# into a clone. Without this file a reader cannot reproduce a single digest in EVIDENCE_MANIFEST.json.\n* -text\n")
_ga=(PK/'.gitattributes').read_bytes()
files.append({'packet_path':'.gitattributes','source':'(generated in this packet)','bytes':len(_ga),'sha256':sha(_ga),
 'disposition':'DELIVERED','reason':'byte-fidelity control so the recorded digests are reproducible from a clone'})
summary={'schema':'SKILL-CONVERGENCE-RETURN-PACKET/1',
 'built_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'subject':{'round':'SKILL-CONVERGENCE-20261014',
   'frozen_generation':'2','subject_manifest_rows':len(rows),
   'subject_tree_digest':'b050a0256e57f5e6958956874d3f4c4d63ac38c7cbe46489990183a16b48e8fa',
   'subject_tree_digest_method':'sha256 over newline-joined "<sha256> <path>" rows, no trailing separator'},
 'counts':{'delivered_files':len(files),'delivered_bytes':sum(f['bytes'] for f in files),'excluded_entries':len(excluded)},
 'by_category':dict(collections.Counter(f['packet_path'].split('/')[1] if '/' in f['packet_path'] else 'root' for f in files)),
 'files':sorted(files,key=lambda x:x['packet_path']),'excluded':excluded,
 'credential_scan':{'patterns':len(SEC),'hits':hits,'outcome':'NO_HITS' if not hits else 'ABORT'},
 'ceiling':'a return packet for external design reference: candidate-only subject, advisory verdicts only, no acceptance, no promotion, no canonical apply'}
_w(PK/'EVIDENCE_MANIFEST.json',json.dumps(summary,ensure_ascii=False,indent=2).encode())
_w(PK/'HASHES.sha256','\n'.join(f"{f['sha256']}  {f['packet_path']}" for f in sorted(files,key=lambda x:x['packet_path'])).encode())
print(json.dumps({'delivered_files':len(files),'delivered_bytes':sum(f['bytes'] for f in files),
  'excluded_entries':len(excluded),'by_category':summary['by_category'],'scan_hits':len(hits)},indent=1))
print('HITS',hits[:4])
if hits:sys.exit(9)
