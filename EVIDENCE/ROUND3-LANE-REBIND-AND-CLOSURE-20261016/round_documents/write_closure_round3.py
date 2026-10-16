"""Build ROUND_CLOSURE.json for ROUND3-LANE-REBIND-AND-CLOSURE-20261016.

The closure is a SELF-REPORT: it records what this round did, what it measured, what it could not close,
and where every decisive claim can be independently re-derived. It asserts no acceptance. Every cited
receipt is read from disk here, so a missing one degrades the closure honestly instead of being hand-typed.
"""
import datetime
import hashlib
import json
import pathlib

R = pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS')
O = R / 'var/ROUND3-LANE-REBIND-AND-CLOSURE-20261016'


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def load(name, default=None):
    p = O / name
    return json.loads(p.read_text(encoding='utf-8')) if p.is_file() else default


apply_r1 = load('R1_R2_R3_APPLY_RECEIPT.json', {})
proj = load('PROJECTION_REPAIR_RECEIPT.json', {})
patch1 = load('PATCH1_RECEIPT.json', {})
promo = load('PROMOTION_RECEIPT.json', {})
subj = load('SUBJECT_DIGEST.json', {})
oracle = load('evidence/ORACLE_R10_RECEIPT.json', {})
ex = load('lanes/EXECUTE/R1/dispatch.json', {})
ver = load('lanes/VERIFY_SECURITY/V4/dispatch.json', {})
verdict = load('lanes/VERIFY_SECURITY/V4/CHECKER_VERDICT.json', {})

closure = {
    'schema': 'HGK-ROUND-CLOSURE/1',
    'round': O.name,
    'session': '20261016_104922_d455e7',
    'order_id': 'owner-order-20261016-lane-rebind-plan-glm-verify-deepseek',
    'generated_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'authority': 'owner order delivered to this session (round 3), then the FAR ruling it authorises',
    'claim_ceiling': ('CANDIDATE_ONLY. This round implements the owner order in the candidate layer and '
                      'publishes its evidence for an external verifier. It performs NO merge, NO branch '
                      'deletion and NO promotion beyond applying its own owner-authorised edits and the '
                      'promotion of the bounded writer\'s change into this working tree.'),
    'canonical_acceptance': 'NOT_PERFORMED',
    'hgk_canonical_acceptance': 'NOT_PERFORMED',

    'canonical_mutations': {
        'R1_R2_R3_lane_rebind': {
            'files': [f['file'] for f in apply_r1.get('files', [])],
            'sha256_before_after': {f['file']: [f.get('sha256_before'), f.get('sha256_after')]
                                    for f in apply_r1.get('files', [])},
            'projection_rebindings': proj.get('rewrites'),
            'patch1_corrections': patch1.get('edits'),
            'new_site_digest': apply_r1.get('new_site_digest'),
        },
        'R10_guard_exemption_promoted_files': [
            {'file': f['file'], 'changed_lines': f['changed_lines'],
             'candidate_sha256': f['candidate_sha256'],
             'canonical_sha256_after': f.get('canonical_sha256_after'),
             'backup': f.get('backup')}
            for f in promo.get('files', [])],
        'R10_oracle': {'cases': oracle.get('cases'), 'all_ok': oracle.get('all_ok')},
        'frozen_subject': subj,
    },

    'lane_evidence': {
        'EXECUTE': {'required_arm': ex.get('required_arm'), 'served_arm': ex.get('served_arm'),
                    'used_rank': ex.get('used_rank'), 'usage_receipt_ok': ex.get('usage_receipt_ok'),
                    'used_seconds': ex.get('used_seconds'), 'ok': ex.get('ok'),
                    'note': 'first measured serving of the mandated EXECUTE arm '
                            '(opencode-go/deepseek-v4.1-flash) in a code-writing turn'},
        'VERIFY_SECURITY': {'required_arm': ver.get('required_arm'), 'served_arm': ver.get('served_arm'),
                            'used_rank': ver.get('used_rank'), 'usage_receipt_ok': ver.get('usage_receipt_ok'),
                            'used_seconds': ver.get('used_seconds'), 'ok': ver.get('ok'),
                            'disclosure': "the checker shares the writer's model BY OWNER ORDER "
                                          '(SOD006-C3); model-axis independence is absent and NOT claimed'},
        'PLAN': {'model': 'opencode-go/glm-5.3-flash', 'surface': 'in-process orchestrator (this session)',
                 'note': "the PLAN plane is this agent; its binding is declared in the assignment site and "
                         "the registry, and the round's own delegation fan-out was served by that model"},
    },

    'verification': {
        'checker': 'VERIFY_SECURITY (CODEX CLI, opencode-go/deepseek-v4.1-flash)',
        'claims': verdict.get('claims'),
        'subject_digest_recomputed': verdict.get('subject_digest_recomputed'),
        'verdict_ceiling': verdict.get('verdict_ceiling'),
        'disclosures': verdict.get('disclosures'),
        'commands': verdict.get('commands'),
        'weight': ('ADVISORY ONLY, and produced by a checker that SHARES the writer\'s model by owner order '
                   '(SOD006-C3). It is not an external review, not an acceptance, and it does not convert '
                   'the round\'s claims into verified fact on its own.'),
        'note': ('the checker recomputed the frozen subject digest and matched it, ran the guard cases itself '
                 '(including a synthetic in-scope admission receipt that reached the exit-0 ADMIT path and an '
                 'adversarial attempt to WIDEN the exemption), and reported the cross-artifact finding below'),
    },

    'detection': [
        {'id': 'SC-12', 'found_by': 'self, while repairing the registry after SC-13',
         'what': 'apply_R1_R2_R3.commit() copied each file to its .bak AFTER writing the edit, so the four '
                 'backups were post-edit copies; and config/ is not tracked by git, so HEAD held no preimage '
                 'either', 'corrected_in': "preimages recovered by digest from the previous round's frozen "
                 'subject tree and installed under preimages/ with provenance; the promote script now backs '
                 'up before writing', 'evidence': 'PATCH1_RECEIPT.json'},
        {'id': 'SC-13', 'found_by': 'the product itself (yaml ScannerError on the live registry)',
         'what': 'the projection note written by the projection-repair pass was an unquoted YAML plain '
                 'scalar containing ": ", which made the whole registry unparseable',
         'corrected_in': 'patch1_R1_R2_R3.py quotes it', 'evidence': 'PATCH1_RECEIPT.json'},
        {'id': 'SC-14', 'found_by': 'check_drift COVERAGE_GAP on '
                                    '/lane_chains/VERIFY_SECURITY/0/reasoning_effort',
         'what': 'the structured rewrite of the VERIFY chain dropped a field the registry binds, so the '
                 'binding resolved to nothing', 'corrected_in': 'the field was RESTORED (with its effort '
                 'declared UNVERIFIED for this model) rather than deleting the binding, which would have '
                 'traded coverage for a green light', 'evidence': 'PATCH1_RECEIPT.json'},
        {'id': 'D-R10', 'found_by': 'measured pre-dispatch guard call during execution',
         'what': 'the guard refuses ANY same-model maker/checker pair (exit 2) and never consults the '
                 "registry's declared_conflicts, so the owner's mandate was undispatchable",
         'corrected_in': 'R10 (additive, fail-closed, visible exemption) via the mandated EXECUTE lane',
         'evidence': 'FAR_RULING_ADDENDUM_A.md A2 + evidence/ORACLE_R10_*.txt'},
        {'id': 'D-R11', 'found_by': 'reading _load_admission()',
         'what': 'ADMITTED is accepted only from a receipt FILE, and nothing in the product produces one '
                 '(only tests do), so the gate can refuse but never admit',
         'status': 'OPEN - recorded, not papered over; the round does NOT invent a producer',
         'evidence': 'FAR_RULING_ADDENDUM_A.md A3'},
        {'id': 'NF-01', 'found_by': "the previous round's enumeration attempt, re-derived here",
         'what': 'the whole-tree enumeration obstruction is a LONG-PATH failure (WinError 3), not '
                 'access-denied as the previous round recorded', 'status': 'correction published',
         'evidence': 'this round hit the same failure class in its own preimage search and handled it with '
                     'an onerror-tolerant walk'},
        {'id': 'NF-06', 'found_by': 'the INDEPENDENT CHECKER (this round\'s own finder did not catch it)',
         'what': "config/model-lane-assignment.json carries its OWN sod_conflicts[] array, which still lists "
                 "SOD006-C2 as OPEN and SOD006-C3 as OPEN_OWNER_ORDERED: the registry's declared_conflicts was "
                 "re-declared but this second declaring surface was not",
         'status': 'OPEN - recorded and NOT edited, deliberately: editing the site now would move its digest, '
                   'invalidate the frozen subject and void the checker verdict on the shipped bytes',
         'remediation': "next round: bind the site's sod_conflicts[] in the registry's projections (or fold "
                        "the array into one declaring surface) so the two can no longer diverge unnoticed; "
                        "then re-freeze and re-check",
         'evidence': 'lanes/VERIFY_SECURITY/V4/CHECKER_VERDICT.json disclosures'},
        {'id': 'NF-05', 'found_by': "this round's pool edit",
         'what': 'the dispatch path reads config/lane-route-slots.candidate.json as its pool while the file '
                 'itself declares status CANDIDATE / not active', 'status': "recorded in the file's "
                 'selection_note; changing its status is a promotion and stays with the owner',
         'evidence': 'FAR_RULING_ADDENDUM_A.md A5'},
    ],

    'not_closed': [
        {'item': 'NF-06 — the assignment site\'s own sod_conflicts[] still disagrees with the registry',
         'why': "found by the independent checker AFTER the subject was frozen; editing it now would void the "
                'verdict on the shipped bytes, so it is recorded with a remediation instead'},
        {'item': 'R11 admission-receipt producer', 'why': 'a new capability, not a repair; needs its own '
         'WorkOrder and acceptance'},
        {'item': 'F-IND-2 detector axis (epoch/revision coupling)', 'why': 'out of scope for the rebind; '
         'the drift pass proved the coupling is enforced at the gate level'},
        {'item': 'F-IND-3 (the previous round\'s canonical writer was not the mandated writer)',
         'why': 'not retroactively curable; recorded as a bounded accepted deviation'},
        {'item': 'the repository merge and branch cleanup', 'why': "the OWNER's decision under the standing "
         'contract; a merge-readiness packet is published instead'},
    ],

    'publication': {'branch': None, 'pr': None, 'note': 'filled after the push'},
}
(O / 'ROUND_CLOSURE.json').write_text(json.dumps(closure, ensure_ascii=False, indent=2), encoding='utf-8')
print('ROUND_CLOSURE.json written; detections:', len(closure['detection']),
      '; not_closed:', len(closure['not_closed']))
print('EXECUTE arm:', ex.get('served_arm'), '| VERIFY arm:', ver.get('served_arm'))
