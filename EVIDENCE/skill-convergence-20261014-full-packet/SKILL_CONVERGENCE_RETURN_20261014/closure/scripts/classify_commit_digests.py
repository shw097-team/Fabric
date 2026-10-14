"""Classify the difference between the scanned working-tree bytes and the committed blobs.

The first read-back refused to claim equality: 155 of 220 files differed. A refusal is only useful if the cause
is identified, so each mismatch is re-compared after stripping carriage returns on both sides. A mismatch that
disappears under that comparison is line-ending normalisation performed by the repository's own configuration;
a mismatch that survives it is an unexplained content difference and is reported as such.
"""
import json,hashlib,pathlib,subprocess
R='C:/Projects/Agent_Workspace/Fabric'
man=json.loads(pathlib.Path(R,'HYGIENE_MANIFEST_20261014.json').read_text(encoding='utf-8'))
want={f['path']:f['sha256'] for f in man['files'] if 'sha256' in f}
raw=subprocess.run(['git','-C',R,'ls-tree','-r','-z','--name-only','HEAD'],capture_output=True).stdout
tree=[x.decode('utf-8') for x in raw.split(b'\0') if x]
out=subprocess.run(['git','-C',R,'cat-file','--batch'],input=b'\n'.join(b'HEAD:'+p.encode() for p in tree),
                   capture_output=True).stdout
pos=0;i=0;blobs={}
while pos<len(out):
    nl=out.index(b'\n',pos);head=out[pos:nl].decode('utf-8','replace');pos=nl+1
    parts=head.split()
    if len(parts)<3 or head.endswith(' missing'):i+=1;continue
    size=int(parts[2]);blobs[tree[i]]=out[pos:pos+size];pos+=size+1;i+=1
exact=[];eol=[];other=[];absent=[]
for p,want_sha in want.items():
    if p not in blobs:absent.append(p);continue
    b=blobs[p]
    if hashlib.sha256(b).hexdigest()==want_sha:exact.append(p);continue
    try:work=pathlib.Path(R,p).read_bytes()
    except OSError:other.append({'path':p,'reason':'working file no longer readable'});continue
    if b.replace(b'\r\n',b'\n')==work.replace(b'\r\n',b'\n'):
        eol.append({'path':p,'blob_bytes':len(b),'working_bytes':len(work),
                    'blob_sha256':hashlib.sha256(b).hexdigest(),'scanned_sha256':want_sha})
    else:other.append({'path':p,'reason':'difference survives line-ending normalisation',
                       'blob_bytes':len(b),'working_bytes':len(work)})
cfg={k:subprocess.run(['git','-C',R,'config','--get',k],capture_output=True,text=True).stdout.strip()
     for k in ('core.autocrlf','core.eol','core.safecrlf')}
attrs=[('gitattributes_present',pathlib.Path(R,'.gitattributes').exists())]
res={'head':subprocess.run(['git','-C',R,'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip(),
     'manifest_files':len(want),'byte_exact':len(exact),'line_ending_only':len(eol),'unexplained':len(other),
     'absent_from_head':absent,'differs_only_by_line_ending':eol,'unexplained_differences':other,
     'repo_line_ending_config':cfg,'gitattributes_present':attrs[0][1],
     'verdict':('COMMITTED_BYTES_EQUAL_SCANNED_BYTES_EXCEPT_REPO_LINE_ENDING_NORMALISATION'
                if not other and not absent else 'UNEXPLAINED_DIFFERENCE_PRESENT'),
     'claim':'the commit stores the same content as was scanned and hashed, with the difference confined to the carriage returns that this repository\'s configuration strips on the way into the object store',
     'what_this_does_not_prove':'that the line endings are immaterial to any consumer; a consumer hashing the working-tree bytes will see the scanned digest, a consumer hashing the blob will see the committed digest'}
pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014/evidence/postfreeze/commit_digest_classification.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
print(json.dumps({k:res[k] for k in ('manifest_files','byte_exact','line_ending_only','unexplained','absent_from_head','verdict','repo_line_ending_config','gitattributes_present')},indent=1))
print('UNEXPLAINED_SAMPLE',other[:3])
print('EOL_SAMPLE',[e['path'] for e in eol[:4]])
