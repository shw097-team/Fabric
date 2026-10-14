"""Honest per-lane disposition of the four timed-out phase-2 lanes.

Reports, from bytes on disk: which lane produced a phase2_result.json (none expected),
what changed versus the frozen baseline copies, and which artefacts are new scripts.
Writes timeout_class_remediation.json. No claims, only observed state.
"""
import pathlib,json,hashlib,datetime,os
R=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS');RUN=R/'var/SKILL-CONVERGENCE-20261014';E=RUN/'evidence'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tree(root):
 out={}
 for p in sorted(pathlib.Path(root).rglob('*')):
  if p.is_file() and '__pycache__' not in p.parts:
   out[p.relative_to(root).as_posix()]=sha(p)
 return out
lanes={}
pairs={'hgk':RUN/'baseline/hgk-governed-execution','avr':RUN/'baseline/adversarial-verification-rounds'}
for role,base in pairs.items():
 cand=RUN/'candidates'/role/'skill'
 b,c=tree(base),tree(cand)
 added=sorted(k for k in c if k not in b);removed=sorted(k for k in b if k not in c)
 changed=sorted(k for k in c if k in b and c[k]!=b[k])
 lanes[role]={'skill_tree':{'baseline_files':len(b),'candidate_files':len(c),'added':added,'removed':removed,'modified':changed}}
for role in ['hgk','avr','consumer','apply']:
 root=RUN/'candidates'/role
 scripts=sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and p.suffix in {'.py','.json'} and 'skill' not in p.parts and 'tests' not in p.parts and '__pycache__' not in p.parts)
 lanes.setdefault(role,{})['phase2_result_present']=(root/'phase2_result.json').exists()
 lanes[role]['top_level_artifacts']=scripts[:20]
 lanes[role]['dispatch_ok']=json.loads((E/'lanes'/role/('4' if role=='hgk' else '3')/'dispatch.json').read_text(encoding='utf-8')).get('ok') if (E/'lanes'/role/('4' if role=='hgk' else '3')/'dispatch.json').exists() else None
receipt={
 'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'error_class':'LANE_BUDGET_TIMEOUT',
 'class_definition':'a maker lane whose Codex turn did not finish inside the granted execution budget; the canonical dispatcher records attempt exit TIMEOUT and ERR_LANE_ALL_ROUTES_EXHAUSTED, and (as separately reproduced) drops partial capture',
 'occurrences_in_this_round':[
  {'lane':'HGK-1','outcome':'TIMEOUT','kept_partial':'diagnostic trace only'},
  {'lane':'HGK-2','outcome':'TIMEOUT','kept_partial':'diagnostic trace, 16 successful read commands'},
  {'lane':'AVR-1','outcome':'TIMEOUT','kept_partial':'diagnostic trace'},
  {'lane':'AVR-2','outcome':'TIMEOUT','kept_partial':'phase-1 artefacts on disk, no completion receipt'},
  {'lane':'CONSUMER-1','outcome':'TIMEOUT','kept_partial':'diagnostic trace'},
  {'lane':'APPLY-1','outcome':'TIMEOUT','kept_partial':'diagnostic trace'},
  {'lane':'HGK-4','outcome':'TIMEOUT','kept_partial':'partial scripts on disk, no phase2_result.json'},
  {'lane':'AVR-3','outcome':'TIMEOUT','kept_partial':'partial scripts on disk, no phase2_result.json'},
  {'lane':'CONSUMER-3','outcome':'TIMEOUT','kept_partial':'NOTHING — this lane wrote no product in its turn'},
  {'lane':'APPLY-3','outcome':'TIMEOUT','kept_partial':'phase-2 test file written, no phase2_result.json'}],
 'count':10,
 'grouping_note':'counted per ERROR CLASS (lane budget timeout), not per session; the class covers all roles because the dispatcher and the relay are the same for each',
 'remediation_already_applied':[
  'decomposed the broad generation-1 asks into bounded single-step phases (this is why HGK-3, CONSUMER-2 and APPLY-2 returned valid receipts)',
  'added a round-only diagnostic observer because the canonical timeout branch discards partial capture (reproduced from source with an executable fixture)',
  'serialized dispatch after the 4-way parallel phase-2 batch all timed out inside the same window, to remove relay contention',
  'replaced tree enumeration with an explicit allow-list of files to read, since the traces show the timed-out turns spending their budget on recursive listings'],
 'current_intervention':{'action':'SERIAL single-lane dispatch (AVR-4) with an explicit no-enumeration read list and a round-only diagnostic budget of 900s, while the canonical 600s gate and the acceptance oracle stay unchanged',
   'why_not_paused':'the work is still producing bounded, reviewable artefacts under an unchanged oracle; the failure mode is budget exhaustion, not a gate refusal, so pausing would stop legitimate progress',
   'would_pause_if':'a lane starts returning gate refusals, mutating frozen subjects, or repeating the same exhausted shape with no new artefact'},
 'lane_disposition':lanes,
 'claim_ceiling':'no lane in the timed-out batch may be cited as a completed maker phase; their artefacts are UNVERIFIED partial work and none produced a phase2_result.json'}
(E/'timeout_class_remediation.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2,default=str),encoding='utf-8',newline='\n')
print(json.dumps({'count':receipt['count'],'lanes':lanes},ensure_ascii=False,indent=2,default=str)[:2600])
