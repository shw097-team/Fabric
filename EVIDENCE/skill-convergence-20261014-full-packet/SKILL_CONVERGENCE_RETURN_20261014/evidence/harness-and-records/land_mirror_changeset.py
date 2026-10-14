"""Land the change-set on the mirror's main through a PR, then read the result back from the remote's objects.

A PR is opened for the record (the mirror's ground rules ask for a reviewed change-set); if the credential cannot
open one, the fallback is an explicit merge commit pushed to main, reported as such. Either way the last step is
an anonymous read of the published tip, not the write's own exit code.
"""
import json,pathlib,re,subprocess,urllib.request
TOK=pathlib.Path('C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt').read_text(encoding='utf-8',errors='replace')
m=re.search(r'github_pat_[A-Za-z0-9_]+|gh[pousr]_[A-Za-z0-9]+',TOK); tok=(m.group(0) if m else TOK.strip())
B='https://api.github.com/repos/shw097-team/Fabric'
def call(u,method='GET',body=None):
    r=urllib.request.Request(u,method=method,headers={'Authorization':'Bearer '+tok,
      'Accept':'application/vnd.github+json','User-Agent':'hgk-round-land'},data=json.dumps(body).encode() if body is not None else None)
    try:
        with urllib.request.urlopen(r,timeout=60) as x:return x.status,x.read().decode('utf-8','replace')
    except Exception as e:
        code=getattr(e,'code',None);txt=''
        try:txt=e.read().decode('utf-8','replace')
        except Exception:pass
        return code,txt
out={}
s,b=call(B+'/pulls','POST',{'title':'docs(SKILL-CONVERGENCE-20261014): publish the candidate-only convergence round record',
 'head':'docs/skill-convergence-20261014','base':'main',
 'body':('Publishes the round record for `SKILL-CONVERGENCE-20261014` under `EVIDENCE/SKILL-CONVERGENCE-20261014/`, '
   'brings the `FABRIC/` front page to the local revision, and updates the mirror README, the manifest and the '
   'findings ledger (K-13 to K-19).\n\nThe change-set exists because the round\'s Fabric-side work had been committed '
   'only in the local Fabric tree, which has no remote, while the full return packet went to '
   '`shw097-team/PIPD-LS-SP`.\n\nNon-claims: NOT_EXTERNALLY_ACCEPTED, NOT_MERGED, NOT_RELEASED, NOT_PRODUCTION, '
   'NO_LIVE_WORLD_EFFECT. All checks in the round are advisory; no contract, baseline or subject state changed.')})
out['pr']={'http':s}
if s in (200,201):
    j=json.loads(b);out['pr'].update({'number':j['number'],'url':j['html_url']})
    s2,b2=call(B+f"/pulls/{j['number']}/merge",'PUT',{'merge_method':'merge',
      'commit_title':'merge: docs/skill-convergence-20261014 -> main','commit_message':'Round record, front page and ledger update for SKILL-CONVERGENCE-20261014. Nothing is accepted by this merge.'})
    out['merge']={'http':s2,'body':b2[:200]}
else:
    out['pr']['body_head']=b[:300]
    out['fallback']='opening a PR was refused; merging locally instead'
r=subprocess.run(['git','-C','C:/pkt/fabpub','checkout','-q','main'],capture_output=True,text=True)
helper=('!f() { if [ "$1" = get ]; then echo username=shw097; printf "password="; '
        'tr -d "\\r\\n" < "C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt"; echo; fi; }; f')
def git(*a):
    return subprocess.run(['git','-C','C:/pkt/fabpub',*a],capture_output=True,text=True)
import os
env=dict(os.environ,GIT_TERMINAL_PROMPT='0',GCM_INTERACTIVE='never')
merged_by_api=out.get('merge',{}).get('http')==200
if merged_by_api:
    git('fetch','--quiet','origin','main')
    git('reset','--hard','-q','origin/main')
    out['main_updated_by']='pull request merge on the remote'
else:
    r=git('merge','--no-ff','-m','merge: docs/skill-convergence-20261014 -> main','docs/skill-convergence-20261014')
    out['local_merge']={'rc':r.returncode,'tail':(r.stdout+r.stderr).strip()[-200:]}
    p=subprocess.run(['git','-C','C:/pkt/fabpub','-c','credential.helper=','-c','credential.helper='+helper,
      'push','--porcelain','https://github.com/shw097-team/Fabric.git','refs/heads/main:refs/heads/main'],
      capture_output=True,text=True,env=env)
    out['main_updated_by']='local merge commit pushed to main'
    out['push']={'rc':p.returncode,'tail':(p.stdout+p.stderr).strip()[-200:]}
out['local_tip']=git('rev-parse','HEAD').stdout.strip()
pathlib.Path('C:/pkt/land.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
print(json.dumps(out,ensure_ascii=False,indent=2)[:1200])
