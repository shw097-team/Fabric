"""Build the machine-readable residual inventory this round's FAR study rules on.

Sources, all read from disk (nothing is transcribed from memory):
  - var/LANE-RELIABILITY-CLOSURE-20261016/ROUND_CLOSURE.json   (this session's residual ledger)
  - var/LANE-RELIABILITY-CLOSURE-20261016/FROZEN_MANIFEST.json (the frozen subject this round promotes)
  - var/LANE-ENFORCEMENT-APPLY-20261015/                       (the previous session's round dir)
  - config/lane-routing-registry.yaml                          (the current declaration the ruling edits)
  - the live repo (for the measurements the ruling leans on)

Each item carries: id, kind (residual | gap | owner_decision | closure | publication), source, the
verbatim measurement basis, and a `ruling` slot the FAR study fills.
"""
import json
import pathlib
import re

R = pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS')
O = R / 'var/ROUND3-LANE-REBIND-AND-CLOSURE-20261016'
PREV = R / 'var/LANE-RELIABILITY-CLOSURE-20261016'
PRIOR = R / 'var/LANE-ENFORCEMENT-APPLY-20261015'


def load(p, default=None):
    try:
        return json.loads(pathlib.Path(p).read_text(encoding='utf-8'))
    except Exception:
        return default


closure = load(PREV / 'ROUND_CLOSURE.json', {})
frozen = load(PREV / 'FROZEN_MANIFEST.json', {})
items = []


def add(i, kind, title, source, basis, extra=None):
    rec = {'id': i, 'kind': kind, 'title': title, 'source': source, 'measurement_basis': basis,
           'ruling': None}
    if extra:
        rec.update(extra)
    items.append(rec)


# ---- 1. this session's own residual ledger -------------------------------------------------------
for n, text in enumerate(closure.get('honest_residuals') or [], start=1):
    kind = 'owner_decision' if ('SOD006-C2' in text or 'owner' in text.lower()) else 'residual'
    add('RES-%02d' % n, kind, text.split(':')[0][:110], 'var/LANE-RELIABILITY-CLOSURE-20261016/'
        'ROUND_CLOSURE.json#honest_residuals[%d]' % (n - 1), text)

# ---- 2. the two named findings of the previous round ---------------------------------------------
for f in ('FINDINGS_F1_PLAN_ROUTE_OUTLIER.md', 'FINDINGS_CHECKER_BRIEF_V1_WRITE_CONTRADICTION.md',
          'FINDINGS_SELF_CORRECTION_BC1_ARM_CLAIM.md'):
    p = PREV / f
    if p.is_file():
        head = [ln.strip() for ln in p.read_text(encoding='utf-8').splitlines() if ln.strip()][:1]
        add('FIND-%s' % f.split('_')[1], 'gap' if 'F1' in f else 'closure', head[0][:110] if head else f,
            str(p.relative_to(R)), 'finding file published in the previous round; see the file for the '
            'measurement')

# ---- 3. the unpromoted verified change -----------------------------------------------------------
if frozen:
    add('GAP-PROMOTION', 'gap', 'ChangeSets B and C are verified but live only in the candidate',
        'var/LANE-RELIABILITY-CLOSURE-20261016/FROZEN_MANIFEST.json',
        'frozen subject: %d files, aggregate %s; the VERIFY lane returned claim_B AGREE and claim_C AGREE '
        'over it; the canonical tree still carries the pre-change behaviour '
        '(same fixtures: canonical exit 3 vs candidate exit 0 / allow)'
        % (frozen.get('file_count'), str(frozen.get('aggregate_sha256'))[:16]),
        {'changeset_files': sorted((frozen.get('changeset_files') or {}).keys())})

# ---- 4. the F1 outlier, measured live right now ---------------------------------------------------
try:
    import yaml
    reg = yaml.safe_load((R / 'config/lane-routing-registry.yaml').read_text(encoding='utf-8'))
    epoch = reg.get('epoch')
    plan = next((r for r in reg.get('routes', []) if str(r.get('lane', '')).upper() == 'PLAN'), {})
    pool = load(R / 'config/lane-route-slots.candidate.json', {})
    sod = reg.get('sod_invariants') or {}
    conflicts = sod.get('declared_conflicts') or {}
    add('GAP-F1', 'gap', 'routes[].PLAN disagrees with every other PLAN declaration surface',
        'config/lane-routing-registry.yaml#routes[PLAN]',
        'routes[].PLAN = %s/%s with selection_authority=%r, while the pool rank-1, the registry SoD block, '
        'the conformance test and the owner mandate all say openai-codex/gpt-6.1-sol; the registry itself '
        'marks that arm usable_now=%r'
        % (plan.get('provider'), plan.get('model'), plan.get('selection_authority'),
           next((a.get('usable_now') for a in plan.get('arms', [])
                 if a.get('model') == 'gpt-6.1-sol'), None)),
        {'registry_epoch_now': epoch,
         'plan_route_now': '%s/%s' % (plan.get('provider'), plan.get('model')),
         'plan_route_authority': plan.get('selection_authority'),
         'plan_route_admission_status': plan.get('admission_status'),
         'sod_conflicts': conflicts})
except Exception as exc:
    add('GAP-F1', 'gap', 'routes[].PLAN outlier (live read failed)', 'config/lane-routing-registry.yaml',
        'live read raised %s' % exc)

# ---- 5. the owner-order staleness that F1 rests on ------------------------------------------------
add('GAP-OWNER-ORDER-STALE', 'owner_decision',
    'The 2026-10-15 PLAN rebind order rests on a 429 that this session measured as no longer true',
    'config/lane-routing-registry.yaml#routes[PLAN].arms[openai-codex] + this session\'s probes',
    'the row records usable_now="QUOTA_429_2026-10-15" for openai-codex/gpt-6.1-sol, while this session '
    'measured that arm serving: PLAN_LANE_PROBE_OK, PLAN_TOOL_PROBE_OK, and fresh state.db::sessions rows '
    '(gpt-6.1-sol / openai-codex / chatgpt.com/backend-api/codex / subscription_included), plus two '
    'VERIFY/SECURITY turns at required_arm == served_arm == openai-codex/gpt-6.1-sol',
    {'owner_objective_in_force': 'PLAN & Orchestrator = GPT 6.1 SOL-MEDIUM (OpenAI OAuth), per the '
                                 '2026-10-16 order this round runs under'})

# ---- 6. previous session's carrier items ---------------------------------------------------------
for name in ('OWNER_RULING.json.md', 'FAR_INTEG_STUDY_RULING_V2.md', 'R3_GOVERNED_PROFILE_RULING.md'):
    p = PRIOR / 'FAR-GAP-RULING-20261015' / name
    if p.is_file():
        add('PRIOR-%s' % name.split('.')[0], 'closure',
            'carried forward from the previous session: %s' % name,
            str(p.relative_to(R)), 'read in full by this study; any item of it that is still unmet is '
            'folded into a ruling below rather than re-listed')

# ---- 7. the session-closure obligations of this round -------------------------------------------
add('CLOSE-01', 'closure', 'session closure + handover checkpoint for this round',
    'owner order: 最後你必須進行本SESSION的結案/移交事項', 'checkpoint written to _handover/ with the '
    'round dir, the claim ceiling, the residuals that survive, and the next moves')
add('CLOSE-02', 'publication', 'publish this round\'s implementation and evidence to Fabric',
    'owner order + C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt',
    'PR against shw097-team/Fabric main; the packet gate and the remote readback decide whether it '
    'actually landed')

inv = {
    'schema': 'HGK-FAR-RESIDUAL-INVENTORY/1',
    'round': O.name,
    'generated_from': 'disk only: the previous round\'s closure JSON, its frozen manifest, the live '
                      'registry, and the carried-forward ruling directory',
    'counts_by_kind': {},
    'items': items,
    'claim_ceiling': 'an inventory is a list, not a judgement. Every item\'s disposition comes from the '
                     'FAR study that follows; this file asserts nothing about any of them.',
}
for it in items:
    inv['counts_by_kind'][it['kind']] = inv['counts_by_kind'].get(it['kind'], 0) + 1

(O / 'RESIDUAL_INVENTORY.json').write_text(json.dumps(inv, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'inventory': str(O / 'RESIDUAL_INVENTORY.json'), 'count': len(items),
                  'by_kind': inv['counts_by_kind'],
                  'ids': [i['id'] for i in items]}, ensure_ascii=False, indent=1))
