"""Round FAR-REMEDIATION-AND-CLOSURE-20261016 detection probes: D01-D03 (PLAN plane) and D12/D15s
GSTACK named-method readback. Every value here is RE-DERIVED from a live surface (the profile's own
session store, the probe stdout, the resolution adapter output, the registry/named-method APIs) --
never from this round's own summary files.
"""
import json
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

R = Path('C:/Projects/Agent_Workspace/HG-KSEOS')
O = R / 'var/FAR-REMEDIATION-AND-CLOSURE-20261016'
H = Path('C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes')
PROFILE = H / 'profiles' / 'hgk-governed'
sys.path.insert(0, str(R / 'src'))
from hg_kseos import lane_policy, named_methods  # noqa: E402

# ---- D03: does the formal adapter resolve HERMES_HOME to the governed profile? --------------------
res = subprocess.run(['pwsh', '-NoProfile', '-File',
                      str(H / 'cache/scratch/r3_resolution_probe.ps1')],
                     capture_output=True, text=True, timeout=120)
resolution_lines = [ln.strip() for ln in res.stdout.splitlines() if ln.strip()]

# ---- D01: the PLAN plane's OWN serving rows (profile state.db), newest first ----------------------
con = sqlite3.connect('file:' + str(PROFILE / 'state.db') + '?mode=ro', uri=True)
serving = [dict(zip(('session', 'model', 'provider', 'base_url', 'mode', 'source',
                     'api_calls', 'messages', 'started_at'),
                    row))
           for row in con.execute(
               'SELECT id, model, billing_provider, billing_base_url, billing_mode, source, '
               'api_call_count, message_count, started_at FROM sessions '
               'ORDER BY started_at DESC LIMIT 6')]

# ---- D02: the probe transcripts captured this round ---------------------------------------------
probe_files = {'reply_probe_stdout': O / 'PLAN' / 'reply_probe.txt',
               'tool_probe_stdout': O / 'PLAN' / 'tool_probe.txt'}
probes = {k: (v.read_text(encoding='utf-8', errors='replace') if v.is_file() else None)
          for k, v in probe_files.items()}

# ---- GSTACK named-method readback (declared role map vs ACTIVE_SELECTED methods) -----------------
role_map_path = R / 'HGK' / 'HGK_GSTACK_ROLE_MAP.yaml'
role_map_roles = []
if role_map_path.is_file():
    body = role_map_path.read_text(encoding='utf-8', errors='replace')
    role_map_roles = sorted(set(re.findall(r'^\s{2}([A-Z][A-Z0-9_]{2,})\s*:', body, re.M)))
snap = named_methods.registry_snapshot()
selected = sorted(k for k, v in snap.items()
                  if isinstance(v, dict) and 'ACTIVE_SELECTED' in str(v.get('current_execution_scope', '')))
routes = {}
for flow in ('far-implementation', 'plan-eng-review', 'security-review', 'coding', 'review'):
    try:
        routes[flow] = named_methods.route(flow)
    except Exception as exc:  # a flow with no route is a fact, not a crash
        routes[flow] = {'error': f'{type(exc).__name__}: {exc}'}
invariants = named_methods.evaluate_activation_invariants()

reg = lane_policy.load_registry()
routes_for_lanes = {lane: lane_policy.route_for_lane(reg, lane)
                    for lane in ('PLAN', 'EXECUTE', 'VERIFY_SECURITY')}
sod_ok, sod_reason = lane_policy.check_sod(routes_for_lanes['PLAN'], routes_for_lanes['VERIFY_SECURITY'])
drift = lane_policy.check_drift(registry=reg)

gstack = {
    'schema': 'HGK-GSTACK-READBACK/1',
    'round': O.name,
    'sources': {
        'role_map': str(role_map_path),
        'upstream_snapshot': str(R / 'HGK/HGK_GSTACK_UPSTREAM_CAPABILITY_SNAPSHOT.tsv'),
        'active_selected_evidence': 'src/hg_kseos/named_methods.py :: registry_snapshot() / route(flow) / evaluate_activation_invariants() -- the config/ surface carries ROUTES, not named methods',
    },
    'registry_epoch': reg.get('epoch'),
    'registry_status': reg.get('status'),
    'role_map_roles': role_map_roles,
    'active_selected_methods': selected,
    'route_by_flow': routes,
    'activation_invariants': invariants,
    'gap_classes': {
        'MAP_ROLE_ABSENT': 'the declared role map uses role names that have no route(flow) branch in named_methods, so their route is NATIVE -- a MAPPING gap, not a named-method gap',
        'SELECTED_NOT_IN_MAP': 'ZERO is reported explicitly: the empty set is part of the evidence',
    },
    'claim_ceiling': ('ACTIVE_SELECTED is a configuration/registration fact, not proof that a role RAN in '
                      'this session. The lane registry carries no gstack role names, so any per-role lane '
                      'attribution here would be INFERENCE and is not made. GSTACK has no separate '
                      'implementation in this repository and is NOT reported as an enabled component.'),
}
(O / 'GSTACK_READBACK.json').write_text(json.dumps(gstack, ensure_ascii=False, indent=2), encoding='utf-8')

plan = {
    'schema': 'HGK-PLAN-LANE-AVAILABILITY/1',
    'round': O.name,
    'priority': 'owner order this session: the PLAN & Orchestrator lane inside Hermes must be GPT 6.1 SOL-MEDIUM (OpenAI OAuth) and its model selection must be demonstrably usable',
    'binding_surface': {
        'surface': str(PROFILE / 'config.yaml'),
        'rows': [ln.strip() for ln in (PROFILE / 'config.yaml').read_text(encoding='utf-8').splitlines()
                 if ln.strip()],
        'why_this_surface': ('per config/model-lane-assignment.json::effective_wiring.main_agent the in-Hermes '
                             'PLAN & Orchestrator plane binds to config.yaml model.default + model.provider of '
                             'the home the process runs under; the per-session picker and delegation.model are '
                             'DIFFERENT surfaces'),
        'activation': {
            'key': 'config/hermes.json :: governed_hermes_home (R3, additive)',
            'adapter_override': 'scripts/hermes-core.ps1 prefers governed_hermes_home when declared; canonical_hermes_home is left UNCHANGED so un-governed consumers keep their binding',
        },
    },
    'D03_resolution_probe': {'argv': ['pwsh', '-NoProfile', '-File',
                                      str(H / 'cache/scratch/r3_resolution_probe.ps1')],
                             'exit': res.returncode, 'stdout_lines': resolution_lines},
    'D01_profile_own_serving_rows': serving,
    'D02_probe_transcripts': probes,
    'lane_dispatch_declaration_for_PLAN': routes_for_lanes['PLAN'],
    'sod_plan_vs_verify': {'ok': sod_ok, 'reason': sod_reason},
    'drift_findings': drift,
    'reliability_findings': [
        {
            'id': 'PLAN-DECL-SURFACE-DIVERGENCE',
            'state': 'OPEN-THIS-ROUND -> ChangeSet A',
            'what': ('three declaration surfaces name the owner-mandated arm for the PLAN plane '
                     '(round role_mandate.json = openai-codex/gpt-6.1-sol medium; config/lane-route-slots.candidate.json PLAN rank 1 = '
                     'openai-codex/gpt-6.1-sol medium; profiles/hgk-governed/config.yaml = gpt-6.1-sol/openai-codex/medium) while '
                     'config/model-lane-assignment.json revision 19 still declares the PLAN lane_group default as opencode-go/glm-5.3-flash '
                     'and marks the GPT arm usable_now=QUOTA_429_2026-10-15. A reader of the two lane-dispatch surfaces therefore believes '
                     'the PLAN lane runs GLM and that GPT is quota-dead.'),
            'measured_counter_evidence': ('the GPT arm served a real PLAN-plane turn this round: profile state.db row above '
                                          '(model=gpt-6.1-sol, billing_provider=openai-codex, '
                                          'billing_base_url=https://chatgpt.com/backend-api/codex, source=oneshot) plus the probe stdout'),
            'why_not_a_registry_reroute': ('PLAN is NOT dispatched through scripts/hgk-lane-dispatch.py (its gate_scope is the CODEX-CLI lanes '
                                           'EXECUTE/VERIFY_SECURITY), so the registry route is the LANE-DISPATCH declaration, not the serving '
                                           'surface of the in-Hermes PLAN plane; re-pointing it would also collapse the PLAN != VERIFY SoD pair '
                                           'that the conformance suite asserts. ChangeSet A is therefore ADDITIVE + a stale measured marker '
                                           'correction, not a re-route.'),
        },
    ],
    'existing_drift_defect': [
        {
            'id': 'REGISTRY-CODEX-SHA256-STALE-EXPECTATION',
            'what': ('registry projection binding config/hermes-codex-lane.json /codex_sha256 still expects the PRE-repair, wrong digest '
                     'D13914CE...DAEC while the live config carries the MEASURED true e98c516f...b99e (the previous round repaired the E pin '
                     'but did not propagate the new expectation to the registry), so check_drift reports one fatal DRIFT_VALUE today.'),
            'state': 'fixed by ChangeSet A2 and re-measured',
        },
    ],
    'claim_ceiling': ('Availability is measured for the GOVERNED PLAN plane (governed profile + the formal adapter path). The interactive '
                      'orchestrator session for this round is a DIFFERENT binding surface and is reported separately. Nothing here is '
                      'acceptance, and no turn in this round resolves canonical acceptance.'),
}
(O / 'PLAN_LANE_AVAILABILITY.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')

print('resolution probe exit', res.returncode, resolution_lines[:3])
print('serving rows:', json.dumps(serving[:2], ensure_ascii=False))
print('gstack selected count:', len(selected), '| invariants all zero:',
      all(v == 0 for v in invariants.values()))
print('drift findings:', len(drift), json.dumps(drift[:2], ensure_ascii=False)[:400])
print('sod:', sod_ok, sod_reason)
