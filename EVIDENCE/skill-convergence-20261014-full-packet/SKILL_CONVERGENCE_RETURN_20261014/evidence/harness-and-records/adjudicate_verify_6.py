"""Adjudicate the closure-review lane by recomputing its claims from the bits, not by quoting it.

Everything the lane was asked about is recomputed here independently: the packet's own counts, a sample of the
packet's digests, the honesty of its exclusion list, the local repository's commits and working-tree count, the
residual gaps the closure record asserts, and the canonical dispatcher's digest.
"""
import json,hashlib,pathlib,re,subprocess
X=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014')
PACK=pathlib.Path('C:/pkt/SKCV_RETURN_20261014')
FAB='C:/Projects/Agent_Workspace/Fabric'
def sha(b):return hashlib.sha256(b).hexdigest()
verdict={}
vp=X/'evidence/lanes/verify/6/verdict.json'
if vp.exists():
    try:
        raw_v=json.loads(vp.read_text(encoding='utf-8'))
        verdict=raw_v.get('verdict_object') or raw_v
    except Exception as e:verdict={'parse_error':str(e)}
if not verdict.get('verdict'):
    m=re.search(r'"verdict"\s*:\s*"([A-Z_]+)"',(X/'evidence/lanes/verify/6/last_message.txt').read_text(encoding='utf-8',errors='replace'))
    if m:verdict={'verdict':m.group(1),'source':'regex over the lane final message; the object itself did not parse as one JSON document'}
man=json.loads((PACK/'EVIDENCE_MANIFEST.json').read_text(encoding='utf-8'))
subj=json.loads((X/'evidence/subject_manifest.json').read_text(encoding='utf-8'))
files=man['files']
hashes=[l for l in (PACK/'HASHES.sha256').read_text(encoding='utf-8').splitlines() if l.strip()]
bad=[]
for f in files:
    p=PACK/f['packet_path']
    if not p.exists():bad.append({'path':f['packet_path'],'reason':'absent'});continue
    if sha(p.read_bytes())!=f['sha256']:bad.append({'path':f['packet_path'],'reason':'digest differs'})
SEC=[r'github_pat_[A-Za-z0-9_]{20,}',r'gh[pousr]_[A-Za-z0-9]{30,}',r'sk-[A-Za-z0-9]{20,}',r'-----BEGIN [A-Z ]*PRIVATE KEY-----']
hits=[]
for f in files:
    t=(PACK/f['packet_path']).read_text(encoding='utf-8',errors='replace')
    for pat in SEC:
        if re.search(pat,t):hits.append(f['packet_path']);break
refs=[p for p in (X/'candidates/hgk/skill/references').rglob('*.md')]
disp=subprocess.run(['git','-C','C:/Projects/Agent_Workspace/HG-KSEOS','hash-object','scripts/hgk-lane-dispatch.py'],
                    capture_output=True,text=True).stdout.strip()
res={
 'lane_verdict_present':bool(verdict),'lane_verdict':verdict.get('verdict') if isinstance(verdict,dict) else None,
 'packet_manifest_files':len(files),'packet_hashes_lines':len(hashes),
 'manifest_and_hash_list_agree':len(files)==len(hashes),
 'delivered_sample_all_ok':not bad,'delivered_files_recomputed':len(files),'delivered_bad':bad[:5],
 'excluded_entries':len(man['excluded']),
 'excluded_entries_with_hash_or_reason':sum(1 for e in man['excluded'] if e.get('reason')),
 'credential_hits_in_delivered_set':hits[:5],
 'fabric_head':subprocess.run(['git','-C',FAB,'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip(),
 'fabric_working_tree_entries':len([l for l in subprocess.run(['git','-C',FAB,'status','--porcelain'],
    capture_output=True,text=True).stdout.splitlines() if l.strip()]),
 'fabric_commits_present':[c for c in ('8b59155','8bd3685','abb70eb')
    if subprocess.run(['git','-C',FAB,'cat-file','-t',c],capture_output=True,text=True).returncode==0],
 'hgk_reference_markdown_now':len(refs),'linter_cap':60,'still_over_cap_by':max(0,len(refs)-60),
 'canonical_dispatcher_blob_object':disp,
 'gen2_rows':len(subj.get('rows') or subj.get('files') or [])}
res['verdict']=('LANE_CLAIMS_RECOMPUTED_AND_AGREE' if res['delivered_sample_all_ok'] and not hits
                and res['manifest_and_hash_list_agree'] and res['fabric_working_tree_entries']==0
                and len(res['fabric_commits_present'])==3 else 'RECOMPUTATION_DISAGREES')
res['claim_ceiling']='recomputation of the closure packet in support of an advisory review; it grants no acceptance and repairs no earlier failure'
(X/'evidence/postfreeze/verify6_adjudication.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
print(json.dumps({k:v for k,v in res.items() if k!='delivered_bad'},indent=1,ensure_ascii=False)[:1800])
