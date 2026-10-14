"""Pre-flight the publication target: repo identity, tree convention, and a reversible write probe.

The token is read from the owner-supplied file and is never printed, never placed in argv, and never written
into a logged command. Only its length and a boolean are reported.

Why a probe instead of reading the token's scope metadata: GitHub's `permissions` object on the repo
endpoint mirrors the USER's role, so a read-only fine-grained token still reports push:true. The only proof of
write capability is a reversible write: create a branch ref at a commit the remote already has, report the
status, then delete it. A denied probe creates nothing.
"""
import json,urllib.request,urllib.error,base64,pathlib
TOK=pathlib.Path('C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt').read_text(encoding='utf-8').strip()
OWNER,REPO='shw097-team','PIPD-LS-SP'
API=f'https://api.github.com/repos/{OWNER}/{REPO}'
def call(url,method='GET',body=None,token=True):
    req=urllib.request.Request(url,method=method)
    req.add_header('User-Agent','hgk-skill-convergence-round')
    req.add_header('Accept','application/vnd.github+json')
    if token:req.add_header('Authorization',f'Bearer {TOK}')
    data=json.dumps(body).encode() if body is not None else None
    try:
        with urllib.request.urlopen(req,data,timeout=45) as r:
            return r.status,r.headers,json.loads(r.read().decode('utf-8') or '{}')
    except urllib.error.HTTPError as e:
        raw=e.read().decode('utf-8','replace')
        try:j=json.loads(raw)
        except:j={'raw':raw[:300]}
        return e.code,e.headers,j
print('token_length',len(TOK))
st,h,repo=call(API)
print('repo_read_status',st,'| private',repo.get('private'),'| default_branch',repo.get('default_branch'))
print('accepted_permissions',h.get('x-accepted-github-permissions'))
st2,h2,tree=call(f'{API}/git/trees/{repo.get("default_branch","main")}?recursive=1')
top=sorted({e['path'].split('/')[0] for e in tree.get('tree',[])}) if st2==200 else f'ERR {st2}'
print('tree_status',st2,'| top_level',top)
returns=[p for p in top if p.endswith('_RETURN') or 'RETURN' in p]
print('return_dirs_at_root',returns)
# reversible write probe: create then delete a branch ref at a commit the remote already has
main_sha=repo.get('default_branch') and next((b['commit']['sha'] for b in [] ),None)
st3,h3,ref=call(f'{API}/git/ref/heads/main')
sha=ref.get('object',{}).get('sha')
print('main_sha',str(sha)[:12])
st4,h4,res=call(f'{API}/git/refs','POST',{'ref':'refs/heads/__hgk_perm_probe__','sha':sha})
print('write_probe_status',st4,'| detail',str(res.get('message'))[:120])
if st4 in (200,201):
    st5,_,_=call(f'{API}/git/refs/heads/__hgk_perm_probe__','DELETE')
    st6,_,_=call(f'{API}/git/ref/heads/__hgk_perm_probe__')
    print('probe_cleanup_delete_status',st5,'| readback_after_delete',st6,'(404 expected)')
elif st4==403:
    print('probe_cleanup_not_needed (a denied probe creates nothing)')
print(json.dumps({'token_length':len(TOK),'repo':f'{OWNER}/{REPO}','public':not repo.get('private'),
 'default_branch':repo.get('default_branch'),'write_probe_status':st4,'top_level':top},ensure_ascii=False))
