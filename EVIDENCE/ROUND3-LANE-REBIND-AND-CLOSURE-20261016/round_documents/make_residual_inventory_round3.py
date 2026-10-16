"""Build RESIDUAL_INVENTORY.json for round 3 by MERGING three measured sources (nothing hand-typed):

  1 the previous round's 15 honest residuals, re-derived against the NEW owner order by an independent
    delegated study (evidence/EVIDENCE_RESIDUAL_STATUS_REDERIVED.json);
  2 that study's own new findings (NF-01..NF-05);
  3 this round's own detection list from ROUND_CLOSURE.json (SC-12/13/14, D-R10, D-R11, NF-05, NF-06).

Each entry keeps its disposition and the artifact that carries the evidence. The inventory asserts no
acceptance; an item is CLOSED only where this round measured the closure itself.
"""
import json
import pathlib

R = pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS')
O = R / 'var/ROUND3-LANE-REBIND-AND-CLOSURE-20261016'


def load(p, default=None):
    p = pathlib.Path(p)
    return json.loads(p.read_text(encoding='utf-8')) if p.is_file() else default


prev = load(O / 'evidence/EVIDENCE_RESIDUAL_STATUS_REDERIVED.json', {})
closure = load(O / 'ROUND_CLOSURE.json', {})

items = []
for it in prev.get('items', []):
    rid = it.get('id') or it.get('item') or '?'
    items.append({'id': rid, 'source': 'round-2 honest_residuals, re-derived under the 2026-10-16 order',
                  'disposition': it.get('status') or it.get('disposition') or 'UNKNOWN',
                  'detail': it.get('detail') or it.get('note') or it.get('why'),
                  'artifact': 'evidence/EVIDENCE_RESIDUAL_STATUS_REDERIVED.json'})
for nf in prev.get('new_findings', []):
    items.append({'id': nf.get('id', '?'), 'source': 'delegated study (this round)',
                  'disposition': nf.get('status') or nf.get('disposition') or 'RECORDED',
                  'detail': nf.get('detail') or nf.get('what'), 'artifact': nf.get('artifact') or
                  'evidence/EVIDENCE_RESIDUAL_STATUS_REDERIVED.json'})
for d in closure.get('detection', []):
    items.append({'id': d.get('id'), 'source': 'this round (self-caught or checker-caught)',
                  'disposition': d.get('status') or 'CLOSED_THIS_ROUND' if d.get('corrected_in')
                  else (d.get('status') or 'OPEN'),
                  'detail': d.get('what'), 'artifact': d.get('evidence') or d.get('corrected_in')})
for nc in closure.get('not_closed', []):
    items.append({'id': nc.get('item'), 'source': 'this round, explicitly not closed',
                  'disposition': 'OPEN', 'detail': nc.get('why'), 'artifact': 'ROUND_CLOSURE.json'})

inv = {
    'schema': 'HGK-RESIDUAL-INVENTORY/1',
    'round': O.name,
    'sources': ['var/FAR-REMEDIATION-AND-CLOSURE-20261016/ROUND_CLOSURE.json::honest_residuals',
                'evidence/EVIDENCE_RESIDUAL_STATUS_REDERIVED.json', 'ROUND_CLOSURE.json'],
    'counts': {'total': len(items),
               'closed_this_round': sum(1 for i in items if str(i['disposition']).startswith('CLOSED')),
               'open': sum(1 for i in items if str(i['disposition']).startswith('OPEN'))},
    'items': items,
    'claim_ceiling': ('CANDIDATE_ONLY. This inventory records dispositions; it is not an acceptance, and an '
                      'item recorded as closed was closed by this round\'s own measurement, not by an '
                      'external party.'),
}
(O / 'RESIDUAL_INVENTORY.json').write_text(json.dumps(inv, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'items': inv['counts'], 'ids': [i['id'] for i in items]}, ensure_ascii=False, indent=1)[:1400])
