"""Prove what the owner's credential can actually do to the mirror repository, before planning the landing.

Reads are answered by the repository metadata and a contents probe; the only proof of write is a reversible ref
probe at a commit the remote already has, undone in one call. The credential value is read at runtime and only
its length and a same-as-file boolean can ever be printed.
"""
import json,re,urllib.request,pathlib
TOK=pathlib.Path('C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt').read_text(encoding='utf-8',errors='replace')
m=re.search(r'github_pat_[A-Za-z0-9_]+|gh[pousr]_[A-Za-z0-9]+',TOK); tok=(m.group(0) if m else TOK.strip())
REPO='shw097-team/Fabric'
BASE='https://api.github.com/repos/'+REPO
def call(u,method='GET',body=None):
    r=urllib.request.Request(u,method=method,
      headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json','User-Agent':'hgk-round-probe'},
      data=json.dumps(body).encode() if body is not None else None)
    try:
        with urllib.request.urlopen(r,timeout=30) as x:return x.status,x.headers.get('x-accepted-github-permissions'),x.read().decode('utf-8','replace')
    except Exception as e:
        code=getattr(e,'code',None);txt=''
        try:txt=e.read().decode('utf-8','replace')
        except Exception:pass
        return code,None,txt
out={'credential_length':len(tok),'credential_family':'github_pat' if tok.startswith('github_pat_') else tok.split('_')[0]}
s,h,b=call(BASE)
out['repo_read']={'http':s,'accepted_permissions':h}
if s==200:
    j=json.loads(b);out['repo_read'].update({'default_branch':j.get('default_branch'),'private':j.get('private'),'permissions_block_for_the_user_not_the_token':j.get('permissions')})
else:
    out['repo_read']['body_head']=b[:200]
s,h,b=call(BASE+'/contents/README.md')
out['contents_read']={'http':s,'accepted_permissions':h}
target=call(BASE+'/git/ref/heads/main')
sha=json.loads(target[2])['object']['sha'] if target[0]==200 else None
out['main_sha']=sha
s,h,b=call(BASE+'/git/refs','POST',{'ref':'refs/heads/__write_probe__','sha':sha})
out['write_probe']={'http':s,'body_head':b[:200]}
if s==201:
    d,_,db=call(BASE+'/git/refs/heads/__write_probe__','DELETE')
    out['write_probe']['deleted_http']=d
out['residual_probe_ref']=call(BASE+'/git/ref/heads/__write_probe__')[0]
out['verdict']=('WRITE_GRANTED_TO_MIRROR' if out['write_probe'].get('http')==201 else
                'WRITE_DENIED_OR_UNKNOWN: '+str(out['write_probe'].get('http')))
pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014/evidence/fabric_repo_probe.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
print(json.dumps(out,ensure_ascii=False,indent=2)[:1500])
