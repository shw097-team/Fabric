"""Round FAR-REMEDIATION-AND-CLOSURE-20261016 HGK typed admission.

Registers, for each CLI lane this round authorises, the canonical four-row chain the gates read:
Requirement CANDIDATE -> FROZEN, TaskSpec DRAFT -> ADMITTED, WorkOrder CREATED. The runner asserts
that readback FROM THE SPINE (not from this file) before it dispatches anything.

Authority: the owner order delivered to session 20261016_104922_d455e7. Mutation authority for the
round's config edits is the same WorkOrder chain. This script writes ONLY spine rows + the round's
own admission.json.
"""
import datetime
import hashlib
import json
import subprocess
import sys
from pathlib import Path

R = Path('C:/Projects/Agent_Workspace/HG-KSEOS')
O = R / 'var/FAR-REMEDIATION-AND-CLOSURE-20261016'
sys.path.insert(0, str(R / 'src'))
from hg_kseos import role_binding  # noqa: E402
from hg_kseos.spine import SharedSpine  # noqa: E402

HEAD = subprocess.check_output(['git', '-C', str(R), 'rev-parse', 'HEAD'], text=True).strip()
MANDATE = O / 'role_mandate.json'
MANDATE_DOC = json.loads(MANDATE.read_text(encoding='utf-8'))
MANDATE_DIGEST = 'sha256:' + hashlib.sha256(MANDATE.read_bytes()).hexdigest()

ROLE_ROOT = {'EXECUTE': O / 'candidate', 'VERIFY_SECURITY': O / 'checker'}
WRITER = {'EXECUTE': 'codex', 'VERIFY_SECURITY': 'codex-cli-independent-gpt'}

WRITESET = {
    'EXECUTE': ['scripts/runtime_role_binding_assert.py',
                'scripts/hgk-governed-runtime-controller.py',
                'tests/test_governed_runtime_controller.py',
                'tests/test_lane_effort_enforcement.py'],
    'VERIFY_SECURITY': ['checker/work/** (verdict JSON only; the frozen candidate is read-only)'],
}


def permissions(role: str, root: Path) -> dict:
    return {
        'round': O.name,
        'session': MANDATE_DOC['session'],
        'write_root': str(root),
        'writeset': WRITESET[role],
        'sandbox': ('workspace-write with the native Windows sandbox; the writer edits ONLY the four '
                    'files named in writeset, plus its own TEST_RESULTS scratch'),
        'forbidden': ['credentials', 'network except the existing local model transport',
                      'any git write command', 'sending anything to an outside host',
                      'merge', 'release', 'RP002 Stage3', 'service restart',
                      'resolving acceptance', 'promotion'],
        'phase_gate': ('the orchestrator re-derives the named acceptance command itself; a writer green '
                       'run and a checker verdict are both CLAIMS and neither is acceptance'),
        'claim_ceiling': ('CANDIDATE_ONLY. These permissions authorise a bounded writer turn and an '
                          'independent read-only checker turn; they assert no acceptance and no '
                          'promotion'),
    }


def binding(role: str, workorder: str, root: Path) -> dict:
    roles = {}
    for lane, decl in MANDATE_DOC['roles'].items():
        roles[lane] = {
            'provider': decl['provider'],
            'model': decl['model'],
            'surface': decl['surface'].split(' ')[0],
            'rank': int(decl.get('rank', 1)),
        }
        if decl.get('reasoning_effort'):
            roles[lane]['reasoning_effort'] = decl['reasoning_effort']
    return {
        'schema': role_binding.ROLE_BINDING_SCHEMA,
        'round': O.name,
        'session': MANDATE_DOC['session'],
        'workorder': workorder,
        'base_head': HEAD,
        'subject': 'HG-KSEOS lane-enforcement controls',
        'scope': [WRITESET[role][0], 'HG-KSEOS'] if role == 'EXECUTE' else ['HG-KSEOS'],
        'expiry': MANDATE_DOC['expires_utc'],
        'mandate_digest': MANDATE_DIGEST,
        'roles': roles,
    }


sp = SharedSpine(R / 'var/shared-spine/hg-kseos.db')
rows = []
for role, root in ROLE_ROOT.items():
    root.mkdir(parents=True, exist_ok=True)
    req = 'REQ-FAR-REMEDIATION-AND-CLOSURE-20261016-' + role
    ts = 'TS-FAR-REMEDIATION-AND-CLOSURE-20261016-' + role
    wo = 'WO-FAR-REMEDIATION-AND-CLOSURE-20261016-' + role
    wording = ('Owner order 2026-10-16 (round 2): study every residual with FAR and then EXECUTE the '
               'ruling. ' + (
                   'Bounded writer, EDIT-ONLY turn: implement R5 of FAR_RULING.md in '
                   'scripts/hgk-lane-dispatch.py - add an OPTIONAL --turn-shape {normal,edit_only} whose '
                   'edit_only value prepends a fixed HARD RULES block to the lane prompt (no process '
                   'enumeration, nothing interactive, writes first, no test suite runs) and records the '
                   'shape actually used in dispatch.json. ADDITIVE ONLY: no existing flag may change '
                   'meaning, and the default must behave exactly as before. Add a typed RED-first test '
                   'module for it. Do not run any suite; the orchestrator owns the oracle. '
                   'No other change.' if role == 'EXECUTE' else
                   'Independent VERIFY_ONLY challenge of this round\'s frozen subject: re-derive the '
                   'registry rebind (R1), the promoted product files (R2) and the dispatcher turn-shape '
                   'change (R5) from the artifacts themselves, and report typed DISAGREEMENT or '
                   'UNCERTAINTY where it cannot. No repair, no acceptance authority.'))
    perms = permissions(role, root)
    perms[role_binding.ROLE_BINDING_KEY] = binding(role, wo, root)
    sp.register_requirement(req, 'owner-order:20261016_104922_d455e7:far-remediation',
                            wording, 'ACC-' + req,
                            'Every decisive claim re-derived from the artifact by the checker; '
                            'required_arm == served_arm in the receipt',
                            'A writer green run is not verification; a checker verdict is advisory',
                            'Fail an arm claim when the receipt shows a different rank served it',
                            project_id='HGK-P0')
    token = 'TK-' + req
    sp.acquire_lease(req, 'hermes-plan-orchestrator', token, 600)
    try:
        sp.transition_requirement(req, 'FROZEN', 'hermes-plan-orchestrator', token, 0,
                                  str(O / 'admission.json'), 'FRZ-' + req,
                                  payload={'roles': MANDATE_DOC['roles'], 'permissions': perms})
    finally:
        sp.release_lease(req, 'hermes-plan-orchestrator', token)
    sp.create_taskspec(ts, req, wording, 'hermes-plan-orchestrator', root, perms,
                       ['the lane\'s own named acceptance command, re-run by the orchestrator',
                        'typed refusal codes quoted verbatim',
                        'subject digest recomputation before and after the turn'],
                       'raw lane stdout + dispatch receipt + the frozen candidate digest manifest; '
                       'rollback = no canonical write happened during the lane turn')
    sp.create_workorder(wo, ts, WRITER[role], root, HEAD)
    with sp.connect() as c:
        row = dict(c.execute(
            'SELECT r.state AS requirement_state, t.state AS taskspec_state, t.writable_root, w.* '
            'FROM requirements r JOIN taskspecs t ON t.requirement_id = r.requirement_id '
            'JOIN workorders w ON w.taskspec_id = t.taskspec_id WHERE w.workorder_id = ?', (wo,)).fetchone())
    assert row['requirement_state'] == 'FROZEN' and row['taskspec_state'] == 'ADMITTED'
    assert row['state'] == 'CREATED' and Path(row['writable_root']) == root
    rows.append(row)

result = {
    'round': O.name,
    'at': datetime.datetime.now().astimezone().isoformat(),
    'base_head': HEAD,
    'session': MANDATE_DOC['session'],
    'mandate_digest': MANDATE_DIGEST,
    'roles': MANDATE_DOC['roles'],
    'readback': rows,
    'canonical_acceptance': 'NOT_PERFORMED',
    'claim_ceiling': ('Admission is a PRE-DISPATCH eligibility record. It proves no role executed and '
                      'no model was served; those come from the lane receipts.'),
}
(O / 'admission.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'workorders': [r['workorder_id'] for r in rows],
                  'writable_roots': [r['writable_root'] for r in rows],
                  'mandate_digest': MANDATE_DIGEST}, ensure_ascii=False, indent=2))
