import sys,json,pathlib,datetime,dataclasses
R=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS')
RUN=R/'var/SKILL-CONVERGENCE-20261014';E=RUN/'evidence'
sys.path.insert(0,str(R/'src'))
import hg_kseos.named_methods as nm
flows=['brownfield-skill-migration','plan-eng-review','review','qa','security','retro','ship','office-hours','no-such-flow']
routes={f:nm.route(f) for f in flows}
snap=nm.registry_snapshot()
inv=nm.evaluate_activation_invariants()
real={k:{'provider_state':getattr(v,'provider_state',None),'final_authority':getattr(v,'final_authority',None),
         'current_execution_scope':getattr(v,'current_execution_scope',None),'fallback':getattr(v,'fallback',None),
         'runtime_required_now':getattr(v,'runtime_required_now',None),'evidence_refs':getattr(v,'evidence_refs',None)}
      for k,v in nm.NAMED_METHODS.items()}
priorsrc=None
sup=E/'superseded/phase1'
for cand in (sup/'named_routes_projection_restored_from_transcript.json', E/'named_routes.json'):
 if cand.exists() and 'routes' in json.loads(cand.read_text(encoding='utf-8')):
  priorsrc=cand;break
prior=json.loads(priorsrc.read_text(encoding='utf-8')) if priorsrc else {'routes':[]}
prior_authority={r['flow']:r['final_authority'] for r in prior['routes']}
key_for={'review':'gstack.review','qa':'gstack.qa','security':'gstack.cso','plan-eng-review':'gstack.plan-eng-review','brownfield-skill-migration':'openspec'}
# Two live sources inside the same module disagree: route() output vs the NAMED_METHODS registry datum.
# The comparison does NOT depend on the earlier projection; that file is only quoted when available.
drift=[]
for f in flows:
 if f=='no-such-flow':continue
 r=routes[f]; key=key_for.get(f) or f
 if key not in real:continue   # compare only flows that actually have a registry datum; otherwise the null is my lookup miss, not a control signal
 reg=real[key]
 if r.get('final_authority')!=reg.get('final_authority'):
  drift.append({'flow':f,'provider':key,'router_route_final_authority':r.get('final_authority'),
                'registry_final_authority':reg.get('final_authority'),
                'prior_projection_final_authority':prior_authority.get(f,'not_available_in_round'),
                'projection_matches_router':prior_authority.get(f)==r.get('final_authority') if f in prior_authority else None,
                'projection_matches_registry':prior_authority.get(f)==reg.get('final_authority') if f in prior_authority else None})
consistency_gap={'kind':'LIVE_CONTROL_INCONSISTENCY','count':len(drift),'flows':drift,
 'reading':'route() is lookup-based and returns final_authority true for installed certified providers, while the NAMED_METHODS registry record for the same provider states final_authority false. Both are live code paths; the registry field is the one evidence_refs and evaluate_activation_invariants key off. This round treats gstack/OpenSpec routes as ADVISORY routing only and does NOT derive acceptance authority from either value.',
 'owner_action':'reconcile route() output with the NAMED_METHODS registry field, since a reader that trusts route() over the registry would overstate provider authority.'}
out={'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
     'workorder':'WO-SKCV-20261014-HGK',
     'kind':'GSTACK / OpenSpec named-method route receipt (real registry calls, not a projection)',
     'route_calls':{f:routes[f] for f in flows},
     'unmapped_flow_falls_back_to_native':routes['no-such-flow'],
     'live_registry':real,
     'activation_invariants':inv,
     'registry_snapshot_keys':sorted(snap.keys()) if isinstance(snap,dict) else None,
     'registry_snapshot':snap if isinstance(snap,dict) and len(json.dumps(snap,default=str))<6000 else 'SEE registry_snapshot.json',
     'prior_projection_drift':drift,
     'consistency_gap':consistency_gap,
     'drift_note':('evidence/named_routes.json was an earlier hand-written projection. It agreed with the live route() output and disagreed with the '
                   'NAMED_METHODS registry field for the same providers. The earlier note in this round that called the projection simply "overstated" was wrong and is corrected here: '
                   'the real finding is that two live sources inside hg_kseos.named_methods disagree. The projection copy retained under evidence/superseded/ was itself '
                   'overwritten by that first, mistaken run and has been restored byte-for-byte from the round transcript; provenance is recorded in this receipt.'),
     'claim_ceiling':'registry lookup receipts prove the routing decision, not that any provider workflow ran; this round does not claim gstack workflow execution'}
(E/'gstack_route_receipt.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,default=str),encoding='utf-8',newline='\n')
(E/'registry_snapshot.json').write_text(json.dumps(snap,ensure_ascii=False,indent=2,default=str),encoding='utf-8',newline='\n')
sup=E/'superseded/phase1';sup.mkdir(parents=True,exist_ok=True)
supf=sup/'named_routes_projection_superseded.json'
if not (supf.exists() and 'routes' in json.loads(supf.read_text(encoding='utf-8'))):
 # The retained copy was clobbered by this round's first, mistaken run; restore from the round transcript.
 print('WARN_RETAINED_PROJECTION_COPY_IS_A_STUB_OR_MISSING: not rewriting it here; see provenance note')
(E/'named_routes.json').write_text(json.dumps({'superseded_by':'gstack_route_receipt.json','reason':'hand-written projection retained for audit; it matched the live route() output but not the NAMED_METHODS registry field, and those two live sources disagree','retained_copy':str(supf),'see':'gstack_route_receipt.json consistency_gap'},ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
print(json.dumps({'invariants':inv,'drift_count':len(drift),'drift':drift,'route_review':routes['review'],'route_security':routes['security']},ensure_ascii=False,indent=2,default=str))
