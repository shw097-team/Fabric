"""Check the packet's own claim inside the clone: committed blob bytes and checked-out bytes against the manifest.

The manifest is the packet's statement about itself. Two consumers hash two different things — a reviewer who
reads the working copy, and one who reads the committed blob — so both are compared, and a normalisation that
rewrites one of them is caught here rather than by the reviewer.
"""
import json,hashlib,pathlib,subprocess
CLONE='C:/pkt/repo';PK='SKILL_CONVERGENCE_RETURN_20261014'
man=json.loads(pathlib.Path(CLONE,PK,'EVIDENCE_MANIFEST.json').read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
paths=[f['packet_path'] for f in man['files']]
want={f['packet_path']:f['sha256'] for f in man['files']}
out=subprocess.run(['git','-C',CLONE,'cat-file','--batch'],input=b'\n'.join(b'HEAD:'+(PK+'/'+p).encode() for p in paths),
                   capture_output=True).stdout
pos=0;i=0;blob_bad=[];blob_ok=0
while pos<len(out):
    nl=out.index(b'\n',pos);head=out[pos:nl].decode('utf-8','replace');pos=nl+1
    parts=head.split();p=paths[i] if i<len(paths) else f'unknown_{i}'
    if len(parts)<3:
        blob_bad.append({'path':p,'reason':'blob unreadable: '+head[:80]});i+=1;continue
    size=int(parts[2]);blob=out[pos:pos+size];pos+=size+1;i+=1
    if sha(blob)==want[p]:blob_ok+=1
    else:blob_bad.append({'path':p,'manifest':want[p],'blob':sha(blob)})
work_bad=[]
for p in paths:
    f=pathlib.Path(CLONE,PK,p)
    if not f.exists():work_bad.append({'path':p,'reason':'absent in the working copy'});continue
    if sha(f.read_bytes())!=want[p]:work_bad.append({'path':p,'manifest':want[p],'worktree':sha(f.read_bytes())})
res={'manifest_files':len(paths),'committed_blob_match':blob_ok,'committed_blob_mismatch':len(blob_bad),
     'worktree_match':len(paths)-len(work_bad),'worktree_mismatch':len(work_bad),
     'blob_mismatch_sample':blob_bad[:5],'worktree_mismatch_sample':work_bad[:5],
     'verdict':'PACKET_BYTES_REPRODUCIBLE_FROM_THE_CLONE' if not blob_bad and not work_bad else 'PACKET_BYTES_NOT_REPRODUCIBLE',
     'head':subprocess.run(['git','-C',CLONE,'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()}
pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014/evidence/postfreeze/packet_readback.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
print(json.dumps({k:v for k,v in res.items() if not k.endswith('_sample')},indent=1))
print('BLOB_BAD',blob_bad[:3]);print('WORK_BAD',work_bad[:3])
