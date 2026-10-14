"""Find out why two files fetched from the raw host differ from the local copy, before calling it a defect.

Both files are written by the harness with newline='\\n'. The suspicion is a line-ending rewrite somewhere in the
trip, so the bytes are compared by length and by a count of carriage returns, and the committed blob is compared
in the same pass so that blob, local working copy and raw fetch are three separate answers.
"""
import hashlib,pathlib,subprocess,urllib.request
LOCAL=pathlib.Path('C:/pkt/repo/SKILL_CONVERGENCE_RETURN_20261014')
ANON=pathlib.Path('C:/pkt/an/SKILL_CONVERGENCE_RETURN_20261014')
URL='https://raw.githubusercontent.com/shw097-team/PIPD-LS-SP/feat/skill-convergence-return-20261014/SKILL_CONVERGENCE_RETURN_20261014/'
def sha(b):return hashlib.sha256(b).hexdigest()
res={}
for rel in ('EVIDENCE_MANIFEST.json','HASHES.sha256','README.md'):
    loc=(LOCAL/rel).read_bytes();anon=(ANON/rel).read_bytes()
    req=urllib.request.Request(URL+rel,headers={'User-Agent':'hgk-readback'})
    with urllib.request.urlopen(req,timeout=45) as r:raw=r.read()
    blob=subprocess.run(['git','-C','C:/pkt/repo','cat-file','-p','HEAD:SKILL_CONVERGENCE_RETURN_20261014/'+rel],
                        capture_output=True).stdout
    res[rel]={'local':{'bytes':len(loc),'crlf':loc.count(b'\r\n'),'sha':sha(loc)[:16]},
              'anonymous_clone':{'bytes':len(anon),'crlf':anon.count(b'\r\n'),'sha':sha(anon)[:16]},
              'committed_blob':{'bytes':len(blob),'crlf':blob.count(b'\r\n'),'sha':sha(blob)[:16]},
              'raw_fetch':{'bytes':len(raw),'crlf':raw.count(b'\r\n'),'sha':sha(raw)[:16]},
              'raw_equals_blob':raw==blob,'raw_equals_local':raw==loc,'local_equals_blob':loc==blob}
print(res)
