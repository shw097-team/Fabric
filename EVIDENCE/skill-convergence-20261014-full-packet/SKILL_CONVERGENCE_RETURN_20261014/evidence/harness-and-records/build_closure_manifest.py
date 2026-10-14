"""Generate the closure manifest: every artifact this session's close-out rests on, with its digest.

Hand-written close-out notes are claims. This file turns them into references a later reader can re-derive:
each entry names a path, a size and a sha256, and the set is grouped by what it is for. Regenerable — re-run it
and compare.
"""
import json,hashlib,pathlib,datetime,collections
X=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014')
FAB=pathlib.Path('C:/Projects/Agent_Workspace/Fabric')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
groups={}
def add(group,label,path):
    if not path.exists():groups.setdefault(group,[]).append({'label':label,'path':str(path).replace('\\','/'),'status':'ABSENT'});return
    groups.setdefault(group,[]).append({'label':label,'path':str(path).replace('\\','/'),
        'bytes':path.stat().st_size,'sha256':sha(path)})
add('decision','closure FAR ruling',X/'evidence/postfreeze/FAR_CLOSURE_REPORT.md')
add('decision','prior FAR remediation ruling',X/'evidence/postfreeze/FAR_REMEDIATION_REPORT.md')
add('decision','closing tally',X/'evidence/postfreeze/closing_tally.json')
add('decision','timeout class update',X/'evidence/postfreeze/timeout_class_update.json')
add('decision','security work-order pause receipt',X/'evidence/postfreeze/security_workorder_pause.json')
add('verdicts','VERIFY 5 verdict (gen2)',X/'evidence/lanes/verify/5/verdict.json')
add('verdicts','SECURITY 5 verdict (gen2), harness-extracted from the lane transcript',X/'evidence/lanes/security/5/verdict.json')
add('verdicts','SECURITY 5 last message verbatim',X/'evidence/lanes/security/5/last_message.txt')
add('verdicts','VERIFY 4 verdict (gen1)',X/'evidence/lanes/verify/4/verdict.json')
add('verdicts','SECURITY 2 last message (gen1)',X/'evidence/lanes/security/2/last_message.txt')
add('adjudications','security 5 adjudication',X/'evidence/postfreeze/security5_adjudication.json')
add('adjudications','security 2 adjudication',X/'evidence/adjudicate_security_2.py')
add('adjudications','verify 5 adjudication script',X/'evidence/adjudicate_verify_5.py')
add('binding','subject manifest (generation 2)',X/'evidence/subject_manifest.json')
add('binding','generation record',X/'evidence/postfreeze/generations.json')
add('binding','heading normalisation record',X/'evidence/postfreeze/heading_normalisation.json')
add('convergence','convergence invariants harness',X/'evidence/convergence_check.py')
add('convergence','rollback drill harness',X/'evidence/rollback_drill.py')
add('closure','session closure record',X/'evidence/postfreeze/SESSION_CLOSURE.md')
add('closure','return packet entry document',X/'evidence/postfreeze/RETURN_README.md')
add('closure','packet readback (committed and checked-out bytes)',X/'evidence/postfreeze/packet_readback.json')
add('closure','publication readback',X/'evidence/postfreeze/publish_readback.json')
add('closure','publication preflight (repo identity and write probe)',X/'evidence/publish_preflight.py')
add('closure','reviewer brief',X/'evidence/prompts/verify-6.md')
add('closure','board close-out readback (direct sqlite read)',X/'evidence/postfreeze/board_closure.json')
add('closure','resume checkpoint',X/'_CHECKPOINT_RESUME.md')
add('closure','handover checkpoint',pathlib.Path('C:/Projects/Agent_Workspace/_handover/CHECKPOINT_SKILL-CONVERGENCE-20261014.md'))
add('closure','local-repo','') if False else None
add('local-repo','hygiene manifest',FAB/'HYGIENE_MANIFEST_20261014.json')
add('local-repo','committed byte classification',X/'evidence/postfreeze/commit_digest_classification.json')
add('local-repo','hygiene pass script',X/'evidence/repo_hygiene.py')
add('local-repo','commit byte read-back script',X/'evidence/verify_commit_bytes.py')
add('packet','return packet staging (delivered set)',pathlib.Path('C:/pkt/SKCV_RETURN_20261014/EVIDENCE_MANIFEST.json'))
res={'schema':'SKILL-CONVERGENCE-CLOSURE-MANIFEST/1','built_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'purpose':'the artifacts this close-out rests on, each with a digest so a later reader re-derives rather than trusts',
 'groups':groups,'counts':{k:len(v) for k,v in groups.items()},
 'absent':[e for g in groups.values() for e in g if e.get('status')=='ABSENT'],
 'claim_ceiling':'a manifest of close-out artifacts; it grants no acceptance and repairs no earlier failure'}
(X/'evidence/postfreeze/CLOSURE_MANIFEST.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
print(json.dumps(res['counts'],indent=1));print('ABSENT',res['absent'])
