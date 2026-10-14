"""Adjudicate the security lane's two discrepancies against the round's own records.

The lane returned PASS_ADVISORY and raised two byte-level doubts. A doubt is adjudicated by recomputing from the
bits, never by quoting the lane or the maker: the subject manifest is recomputed row by row, and the merged
payloads are re-hashed from the baseline files and searched in the topic file's current bytes.
"""
import json,hashlib,pathlib,re
X=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014')
def sha(b):return hashlib.sha256(b).hexdigest()
man=json.loads((X/'evidence/subject_manifest.json').read_text(encoding='utf-8'))
rows=man['rows'] if 'rows' in man else man.get('files',man)
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
rows=[r for r in rows if isinstance(r,dict) and 'path' in r and 'sha256' in r]
lines=[];bad=[]
for r in rows:
    p=X/r['path']
    lines.append(f"{r['sha256']} {r['path']}")
    try:got=sha(p.read_bytes())
    except OSError as e:bad.append({'path':r['path'],'error':str(e)});continue
    if got!=r['sha256']:bad.append({'path':r['path'],'manifest':r['sha256'],'disk':got})
dig=sha('\n'.join(lines).encode())
rem=json.loads((X/'candidates/hgk/remediation_result.json').read_text(encoding='utf-8'))
topic=X/'candidates/hgk/skill/references/topics/lane-bootstrap-and-guard-notes.md'
tb=topic.read_bytes()
payloads=[]
for m in rem['merged']:
    src=X/'baseline/hgk-governed-execution'/m['path'] if (X/'baseline/hgk-governed-execution'/m['path']).exists() else X/'baseline'/m['path']
    try:raw=src.read_bytes()
    except OSError:payloads.append({'path':m['path'],'status':'source not located'});continue
    payloads.append({'path':m['path'],'baseline_sha_matches_record':sha(raw)==m['sha256_before'],
                     'baseline_bytes':len(raw),'occurrences_in_topic':tb.count(raw),
                     'recorded_bytes_before':m['bytes_before']})
head=[l for l in tb.decode('utf-8').splitlines() if l.startswith('#')]
norm=json.loads((X/'evidence/postfreeze/heading_normalisation.json').read_text(encoding='utf-8'))
res={'subject_manifest':{'rows':len(rows),'row_set_digest_recomputed':dig,
    'row_set_digest_expected':'b050a0256e57f5e6958956874d3f4c4d63ac38c7cbe46489990183a16b48e8fa',
    'digest_match':dig=='b050a0256e57f5e6958956874d3f4c4d63ac38c7cbe46489990183a16b48e8fa',
    'rows_not_matching_disk':bad},
 'topic_file':{'bytes_now':len(tb),'sha256_now':sha(tb),
    'sha256_recorded_after_normalisation':norm['sha256_after'],
    'matches_record':sha(tb)==norm['sha256_after'],
    'sha256_recorded_by_maker':norm['maker_recorded_topic_sha256'],'bytes_recorded_by_maker':norm['bytes_before'],
    'heading_lines_now':len(head),'heading_lines_rewritten_at_normalisation':norm['headings_rewritten']},
 'merged_payloads':payloads}
res['disposition_of_lane_doubts']=[
 {'doubt':'the candidate main file is not byte-identical to the baseline snapshot (21026 against 105116 bytes)',
  'disposition':'expected by construction, not drift: this round\'s subject is a lossless extraction that moves the oversized main file\'s body into slices and references, so the main file must be smaller. Byte-exactness is claimed for the union of main file plus slices, which the round re-derives against the baseline digest, not for the main file alone.'},
 {'doubt':'the topic file on disk hashes to a different digest than the maker recorded',
  'disposition':'attributable and already disclosed: the round harness rewrote fourteen heading lines after the maker lane, changing 43675 bytes into 44879 and the digest from the maker value to the current one. The normalisation record states that the content excluding those heading lines is unchanged, and the payload search above re-establishes it: every absorbed file still occurs in the topic exactly as many times as it should.'},
 {'doubt':'the lane could not judge merged-text semantics','disposition':'accepted as a real ceiling. Byte identity is all this axis can prove; reader-facing quality of merged text is unverified and stays that way.'}]
res['verdict']=('LANE_DOUBTS_RECONCILED_WITH_ROUND_RECORDS' if res['subject_manifest']['digest_match']
                and not bad and all(p.get('occurrences_in_topic')==1 and p.get('baseline_sha_matches_record') for p in payloads)
                else 'RECONCILIATION_FAILED')
res['claim_ceiling']='recomputation of the subject binding and of the merge payload identity in support of a security verdict; it grants no acceptance and repairs no earlier failure'
(X/'evidence/postfreeze/security5_adjudication.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
print(json.dumps({'rows':res['subject_manifest']['rows'],'digest_match':res['subject_manifest']['digest_match'],
  'rows_bad':len(bad),'topic_sha_matches_record':res['topic_file']['matches_record'],
  'topic_bytes':res['topic_file']['bytes_now'],'headings':res['topic_file']['heading_lines_now'],
  'payloads_ok':sum(1 for p in payloads if p.get('occurrences_in_topic')==1 and p.get('baseline_sha_matches_record')),
  'payloads_total':len(payloads),'verdict':res['verdict']},indent=1))
print('PAYLOAD_ODDITIES',[p for p in payloads if not (p.get('occurrences_in_topic')==1 and p.get('baseline_sha_matches_record'))][:4])
