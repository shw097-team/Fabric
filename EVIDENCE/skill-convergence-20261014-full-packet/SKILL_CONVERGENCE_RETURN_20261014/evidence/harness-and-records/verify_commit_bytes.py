"""Prove the committed bytes are the scanned bytes.

The manifest hashed the working tree before the commit. A commit is a write to an external store even when it
lands in a local repository, so the write is read back: every blob named by HEAD is pulled out of the object
store and hashed, and the digests are compared with the manifest. A mismatch would mean git normalised or
altered content on the way in.
"""
import json,hashlib,pathlib,subprocess
R=pathlib.Path('C:/Projects/Agent_Workspace/Fabric')
man=json.loads((R/'HYGIENE_MANIFEST_20261014.json').read_text(encoding='utf-8'))
want={f['path']:f['sha256'] for f in man['files'] if 'sha256' in f}
unreadable=[f for f in man['files'] if 'sha256' not in f]
raw=subprocess.run(['git','-C',str(R),'ls-tree','-r','-z','--name-only','HEAD'],capture_output=True).stdout
tree=[x.decode('utf-8') for x in raw.split(b'\0') if x]
p=subprocess.run(['git','-C',str(R),'cat-file','--batch'],input='\n'.join(f'HEAD:{t}' for t in tree).encode(),
                 capture_output=True)
out=p.stdout;pos=0;bad=[];missing=[];ok=0;seen=set();i=0
while pos<len(out):
    nl=out.index(b'\n',pos);head=out[pos:nl].decode('utf-8','replace');pos=nl+1
    parts=head.split()
    path=tree[i] if i<len(tree) else f'unknown_{i}'
    if head.endswith(' missing') or len(parts)<3:
        missing.append(path);i+=1;continue
    size=int(parts[2]);blob=out[pos:pos+size];pos+=size+1;i+=1
    seen.add(path)
    got=hashlib.sha256(blob).hexdigest()
    if path not in want:continue
    if got==want[path]:ok+=1
    else:bad.append({'path':path,'manifest':want[path],'committed':got})
untracked_in_manifest=sorted(set(want)-seen)
print(json.dumps({'blobs_in_head':len(tree),'manifest_files':len(want),'matched':ok,'mismatched':len(bad),
  'in_manifest_not_in_head':len(untracked_in_manifest),'missing_blobs':len(missing)},indent=1))
print('MISMATCH_SAMPLE',bad[:5])
print('NOT_IN_HEAD_SAMPLE',untracked_in_manifest[:8])
print('HEAD',subprocess.run(['git','-C',str(R),'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip())
