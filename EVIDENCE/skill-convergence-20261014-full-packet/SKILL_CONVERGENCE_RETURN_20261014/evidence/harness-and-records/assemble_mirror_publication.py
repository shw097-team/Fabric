"""Assemble this round's projection inside a clone of the mirror, then stop before committing.

Curated, not raw: the mirror excludes raw evidence stores, so this copies the round's closure documents and its
machine receipts into EVIDENCE/<round>/, brings the subject front page up to the local revision, and scans every
byte it is about to publish. Nothing is committed here -- the commit is a separate, reviewed step.
"""
import hashlib,pathlib,re,shutil,subprocess,sys
R=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014')
CLONE=pathlib.Path('C:/pkt/fabpub')
DEST=CLONE/'EVIDENCE'/'SKILL-CONVERGENCE-20261014'
def run(*a,**k): return subprocess.run(a,cwd=str(CLONE),capture_output=True,text=True,**k)
print(run('git','rev-parse','HEAD').stdout.strip(),'<- cloned tip')
print(run('git','checkout','-q','-b','docs/skill-convergence-20261014').stderr.strip() or 'branch created')
DEST.mkdir(parents=True,exist_ok=True)
M=R/'evidence/mirror_publication'
P=R/'evidence/postfreeze'
COPY=[
 (M/'README.md','README.md'),
 (M/'INDEPENDENT-CHECK-VERDICT.md','INDEPENDENT-CHECK-VERDICT.md'),
 (M/'SECURITY-CHECK.md','SECURITY-CHECK.md'),
 (M/'PUBLICATION-RECORD.md','PUBLICATION-RECORD.md'),
 (M/'APPROVAL-LIST.md','APPROVAL-LIST.md'),
 (P/'SESSION_CLOSURE.md','ROUND-CLOSURE.md'),
 (P/'FAR_CLOSURE_REPORT.md','FAR-CLOSURE-REPORT.md'),
 (P/'CLOSURE_MANIFEST.json','closure_manifest.json'),
 (P/'verify6_adjudication.json','verify6_adjudication.json'),
 (P/'security5_adjudication.json','security5_adjudication.json'),
 (P/'verify5_adjudication.json','verify5_adjudication.json'),
 (P/'verify4_adjudication.json','verify4_adjudication.json'),
 (P/'security_workorder_pause.json','security_workorder_pause.json'),
 (P/'board_closure.json','board_closure.json'),
 (P/'publish_readback.json','publish_readback.json'),
 (P/'PUBLICATION_FINAL_v5.json','publication_final_v5.json'),
 (P/'commit_digest_classification.json','commit_digest_classification.json'),
 (P/'far_measurements.json','far_measurements.json'),
 (P/'closing_tally.json','closing_tally.json'),
 (P/'timeout_class_update.json','timeout_class_update.json'),
 (P/'convergence_gen2_before_repair.json','convergence_before_repair.json'),
 (P/'convergence_gen2_after_repair.txt','convergence_after_repair.txt'),
]
missing=[];copied=[]
for src,dst in COPY:
    if not src.exists(): missing.append(str(src)); continue
    shutil.copyfile(src,DEST/dst); copied.append(dst)
shutil.copyfile('C:/Projects/Agent_Workspace/Fabric/README.md',CLONE/'FABRIC'/'README.md')
copied.append('FABRIC/README.md (front page, local revision)')
SEC=[r'github_pat_[A-Za-z0-9_]{20,}',r'gh[pousr]_[A-Za-z0-9]{30,}',r'nvapi-[A-Za-z0-9_\-]{20,}',r'sk-[A-Za-z0-9]{20,}',r'oc_sk_[A-Za-z0-9_]{10,}',r'-----BEGIN [A-Z ]*PRIVATE KEY-----',r'7776004oc_sk']
hits=[]
for p in sorted(DEST.rglob('*')):
    if p.is_file():
        t=p.read_text(encoding='utf-8',errors='replace')
        for pat in SEC:
            if re.search(pat,t): hits.append((p.name,pat)); break
for rel in ('FABRIC/README.md',):
    t=(CLONE/rel).read_text(encoding='utf-8',errors='replace')
    for pat in SEC:
        if re.search(pat,t): hits.append((rel,pat)); break
print('copied',len(copied),'files; missing',missing)
print('scanned set secret hits:',hits if hits else 'NONE')
print('dest listing:',sorted(x.name for x in DEST.iterdir())[:8],'...',len(list(DEST.iterdir())),'entries')
print(run('git','status','--porcelain').stdout.strip()[:1500])
if hits: sys.exit('ABORT: secret-shaped content in the payload')
