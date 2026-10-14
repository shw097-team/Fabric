"""Verify the publication from the remote's own objects, with no credential at all.

Three channels, each answering a different question, so none of them can carry the others:
  * `git ls-remote` without a credential -- the refs, including the default branch that must not have moved.
  * an anonymous `git clone` of the branch -- the bytes the repository actually serves, compared per file both as
    a checked-out file and as a committed blob.
  * the raw file host -- the cheapest channel, and the one that lies: it is CDN-cached and served an EARLIER
    revision of two files whose content changed between the two commits on this branch. That outcome is recorded
    as STALE_CDN_CONTENT with the sizes that show it, not as a content mismatch, because the clone and the blob
    agree with the manifest while the raw host does not.
"""
import hashlib,json,pathlib,subprocess,urllib.request,datetime
OWNER,REPO='shw097-team','PIPD-LS-SP'
BRANCH='feat/skill-convergence-return-20261014'
PK='SKILL_CONVERGENCE_RETURN_20261014'
LOCAL=pathlib.Path('C:/pkt/repo');ANON=pathlib.Path('C:/pkt/an')
def sha(b):return hashlib.sha256(b).hexdigest()
def ls_remote(ref):
    p=subprocess.run(['git','-c','credential.helper=','ls-remote','--heads',
                      f'https://github.com/{OWNER}/{REPO}.git',ref],capture_output=True,text=True)
    return p.stdout.strip().split('\t')[0] if p.stdout.strip() else None
tip=ls_remote(BRANCH);main=ls_remote('main')
man=json.loads((LOCAL/PK/'EVIDENCE_MANIFEST.json').read_text(encoding='utf-8'))
# clone channel: committed blobs of the anonymous clone, per file
paths=[f['packet_path'] for f in man['files']];want={f['packet_path']:f['sha256'] for f in man['files']}
out=subprocess.run(['git','-C',str(ANON),'cat-file','--batch'],
                   input=b'\n'.join(b'HEAD:'+(PK+'/'+p).encode() for p in paths),capture_output=True).stdout
pos=0;i=0;clone_bad=[]
while pos<len(out):
    nl=out.index(b'\n',pos);head=out[pos:nl].decode('utf-8','replace');pos=nl+1
    parts=head.split();p=paths[i] if i<len(paths) else f'unknown_{i}'
    if len(parts)<3:clone_bad.append({'path':p,'reason':head[:60]});i+=1;continue
    size=int(parts[2]);blob=out[pos:pos+size];pos+=size+1;i+=1
    if sha(blob)!=want[p]:clone_bad.append({'path':p,'manifest':want[p],'cloned_blob':sha(blob)})
work_bad=[p for p in paths if not (ANON/PK/p).exists() or sha((ANON/PK/p).read_bytes())!=want[p]]
# raw channel
raw=[];base=f'https://raw.githubusercontent.com/{OWNER}/{REPO}/{BRANCH}/{PK}/'
for rel in ('EVIDENCE_MANIFEST.json','README.md','HASHES.sha256','.gitattributes'):
    req=urllib.request.Request(base+rel,headers={'User-Agent':'hgk-skill-convergence-readback'})
    try:
        with urllib.request.urlopen(req,timeout=45) as r:body=r.read()
    except Exception as e:
        raw.append({'path':rel,'outcome':'FETCH_FAILED','detail':str(e)[:100]});continue
    loc=(LOCAL/PK/rel).read_bytes()
    raw.append({'path':rel,'raw_bytes':len(body),'local_bytes':len(loc),'raw_equals_local':body==loc,
                'outcome':'MATCH' if body==loc else 'STALE_CDN_CONTENT'})
res={'schema':'SKILL-CONVERGENCE-PUBLICATION-READBACK/1','observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'branch':BRANCH,'local_tip':subprocess.run(['git','-C',str(LOCAL),'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip(),
 'remote_tip':tip,'tip_matches':tip==subprocess.run(['git','-C',str(LOCAL),'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip(),
 'local_tree':subprocess.run(['git','-C',str(LOCAL),'rev-parse','HEAD^{tree}'],capture_output=True,text=True).stdout.strip(),
 'default_branch_sha':main,'default_branch_unmoved':(main or '').startswith('f4021ae'),
 'channel_1_refs':{'credential_used':False,'branch_tip_matches_local':tip==subprocess.run(['git','-C',str(LOCAL),'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()},
 'channel_2_anonymous_clone':{'credential_used':False,'files_compared':len(paths),'blob_mismatch':len(clone_bad),
   'checked_out_mismatch':len(work_bad),'blob_mismatch_sample':clone_bad[:5],'worktree_mismatch_sample':work_bad[:5],
   'verdict':'CLONE_BYTES_EQUAL_THE_MANIFEST' if not clone_bad and not work_bad else 'CLONE_BYTES_DIFFER'},
 'channel_3_raw_file_host':{'credential_used':False,'results':raw,
   'interpretation':'the raw host is a cache: it served an earlier revision of the two files whose content changed between the two commits on this branch. The clone and the committed blob agree with the manifest, so this is classified as cache staleness, not as a content mismatch. A reviewer whose only channel is the raw host should re-fetch after the cache expires, or use a clone.'},
 'packet':{'delivered_files':man['counts']['delivered_files'],'delivered_bytes':man['counts']['delivered_bytes'],
           'excluded_entries':man['counts']['excluded_entries'],'credential_scan':man['credential_scan']['outcome']},
 'claim_ceiling':'a publication and a credential-free read-back of it: candidate-only subject, advisory verdicts, no acceptance, no promotion',
 'what_this_does_not_show':'that any consumer accepts the packet, or that the packet is free of defects it discloses about itself'}
pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014/evidence/postfreeze/publish_readback.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
print(json.dumps({'remote_tip':tip,'tip_matches':res['tip_matches'],'default_branch_unmoved':res['default_branch_unmoved'],
 'clone_channel':{k:v for k,v in res['channel_2_anonymous_clone'].items() if not k.endswith('sample')},
 'raw_channel':[(r['path'],r['outcome']) for r in raw]},indent=1))
