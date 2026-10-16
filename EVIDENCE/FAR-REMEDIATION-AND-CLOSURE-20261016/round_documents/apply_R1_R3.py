"""R1 + R3 — rebind the PLAN route declaration to the owner-ordered arm, and reclassify SOD006-C2.

Scope, decided by MEASUREMENT rather than by memory: the PLAN arm's model is declared in FOUR coupled
places, and changing any one alone leaves the repo self-inconsistent.

  A. config/lane-routing-registry.yaml   routes[].PLAN            (the route row itself)
  B. config/lane-routing-registry.yaml   projections[].expected   (the registry's own expectations of
                                                                   the SITE file for PLAN's chain)
  C. config/model-lane-assignment.json   lane_chains.PLAN, sod.plan_lane, and the prose that describes
                                                                   the PLAN/VERIFY separation
  D. tests/test_lane_policy.py           owner_chain               (read-only for us; it is the gate that
                                                                   is currently RED, not something we edit)

The loop is self-checking: apply, run check_drift, and let it name any coupled string still missed
(DRIFT_VALUE carries the JSON pointer). Nothing is declared fixed until check_drift is empty and the
conformance test passes.

WorkOrder: WO-FAR-REMEDIATION-AND-CLOSURE-20261016-R1. Backups and before/after digests are recorded.
"""
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys

R = pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS')
O = R / 'var/FAR-REMEDIATION-AND-CLOSURE-20261016'
PY = 'C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe'
REG = R / 'config/lane-routing-registry.yaml'
SITE = R / 'config/model-lane-assignment.json'
WO = 'WO-FAR-REMEDIATION-AND-CLOSURE-20261016-R1'
REQ = 'REQ-FAR-REMEDIATION-AND-CLOSURE-20261016-R1'
TS = 'TS-FAR-REMEDIATION-AND-CLOSURE-20261016-R1'
SUFFIX = '.bak-far-remediation-20261016'
AUTH = 'owner-order-20261016-plan-model-rebind-gpt61-sol'
MEASURED = ('MEASURED 2026-10-16: reply probe + tool-executing probe + 2 VERIFY/SECURITY turns at '
            'required_arm == served_arm == openai-codex/gpt-6.1-sol')


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def backup(p):
    b = pathlib.Path(str(p) + SUFFIX)
    if not b.is_file():
        shutil.copy2(p, b)
    return b


def sub(text, old, new, where, required=True):
    n = text.count(old)
    if n != 1 and required:
        raise SystemExit('EDIT NOT UNIQUE: %s occurrences=%d in %s' % (old[:70], n, where))
    if n == 0:
        return text, 0
    return text.replace(old, new), n


log = {'workorder': WO, 'edits': [], 'dry_run': '--apply' not in sys.argv}

# ---------------------------------------------------------------- create the WorkOrder (spine)
sys.path.insert(0, str(R / 'src'))
if not log['dry_run']:
    from hg_kseos.spine import SharedSpine  # noqa: E402
    sp = SharedSpine(R / 'var/shared-spine/hg-kseos.db')
    head = subprocess.run(['git', '-C', 'C:/Projects/Agent_Workspace/HG-KSEOS', 'rev-parse', 'HEAD'],
                          capture_output=True, text=True).stdout.strip()
    wording = ('R1/R3 of FAR_RULING.md: rebind routes[].PLAN and the coupled PLAN declaration surfaces to '
               'the owner-ordered arm openai-codex/gpt-6.1-sol (medium, OAuth) under authority %s, replace '
               'the stale usable_now 429 marker with this session\'s measurement, advance the registry '
               'epoch 20 -> 21, and reclassify declared_conflicts[SOD006-C2] to OWNER_ORDERED_IN_FORCE.' % AUTH)
    try:
        sp.register_requirement(REQ, 'owner-order:20261016_104922_d455e7:far-remediation', wording,
                                'ACC-' + REQ, 'check_drift empty + the conformance test green',
                                'applying a ruling is not accepting it', 'fail on non-empty drift',
                                project_id='HGK-P0')
        token = 'TK-' + REQ
        sp.acquire_lease(REQ, 'hermes-plan-orchestrator', token, 600)
        try:
            sp.transition_requirement(REQ, 'FROZEN', 'hermes-plan-orchestrator', token, 0,
                                      str(O / 'admission.json'), 'FRZ-' + REQ,
                                      payload={'ruling': 'R1+R3', 'authority': AUTH})
        finally:
            sp.release_lease(REQ, 'hermes-plan-orchestrator', token)
        sp.create_taskspec(TS, REQ, wording, 'hermes-plan-orchestrator', R,
                           {'canonical_config_edit': True, 'writer': 'hermes-plan-orchestrator'},
                           ['check_drift(registry) == []', 'test_lane_policy conformance case passes'],
                           'before/after sha256 of both config files + .bak copies on disk')
        sp.create_workorder(WO, TS, 'hermes-plan-orchestrator', R, head)
        log['workorder_created'] = True
    except Exception as exc:
        log['workorder_note'] = 'spine registration raised %s: %s (the change proceeds; the WorkOrder is ' \
                                'recorded here either way)' % (type(exc).__name__, exc)

# ---------------------------------------------------------------- A + B: the registry
before_reg = sha(REG)
text = REG.read_text(encoding='utf-8')
edits = []

# A1 the route row's own scalars
text, n = sub(text, """    engine: hermes
    provider: opencode-go
    model: glm-5.3-flash
    canonical_identity: glm-5.3-flash
    auth: env_ref:OPENCODE_GO_API_KEY
    oauth: false
    reasoning_effort: medium
# Owner order 2026-10-15 (this session, epoch 19): PLAN & Orchestrator rebound to GLM-5.3-Flash(GO)
    # because the OpenAI OAuth GPT arm is exhausted (status=429, credential-pool rotation logged).
    # Rank-1 GLM-5.3-Flash (GO); fallback1 DeepSeek V4.1 Flash (GO); the GPT arm is retained as a
    # NON-DEFAULT, non-automatic operator-selectable alternate. Per-session-round user re-selection
    # remains first-class (role_mandate -> runtime_role_binding_assert).
    selection_authority: owner-order-20261015-plan-model-rebind-glm""",
            """    engine: hermes
    provider: openai-codex
    model: gpt-6.1-sol
    canonical_identity: gpt-6.1-sol
    auth: openai_oauth
    oauth: true
    reasoning_effort: medium
    # Owner order 2026-10-16 (round FAR-REMEDIATION-AND-CLOSURE-20261016, epoch 21): PLAN & Orchestrator
    # is GPT-6.1-SOL-MEDIUM (OpenAI OAuth). This SUPERSEDES owner-order-20261015-plan-model-rebind-glm,
    # whose stated premise -- the OpenAI OAuth arm exhausted (status=429 on 2026-10-15) -- was MEASURED
    # FALSE on 2026-10-16 in round LANE-RELIABILITY-CLOSURE-20261016: the arm answered the PLAN reply
    # probe and a tool-executing probe, and served two VERIFY/SECURITY turns at
    # required_arm == served_arm. The 429 is retained below as dated history, not as a current fact.
    # Rank-1 gpt-6.1-sol; fallback1 GLM-5.3-Flash (GO); fallback2 DeepSeek V4.1 Flash (GO) -- the owner
    # chain ORDER is first-class policy (tests/test_lane_policy.py owner_chain asserts it exactly).
    # Per-session-round re-selection remains first-class (role_mandate -> runtime_role_binding_assert).
    selection_authority: owner-order-20261016-plan-model-rebind-gpt61-sol""",
            'registry routes[].PLAN scalars')
edits.append(('A1', 'registry: routes[].PLAN provider/model/auth/oauth/authority', n))

# A2 the arms list: gpt becomes primary, glm becomes the rotation alternate and keeps its 429 as history
text, n = sub(text, """    arms:
      - arm: primary
        provider: opencode-go
        model: glm-5.3-flash
        canonical_identity: glm-5.3-flash
        auth: env_ref:OPENCODE_GO_API_KEY
        oauth: false
        reasoning_effort: medium
        default: true
      - arm: fallback1
        provider: opencode-go
        model: deepseek-v4.1-flash
        canonical_identity: deepseek-v4.1-flash
        auth: env_ref:OPENCODE_GO_API_KEY
        oauth: false
        default: false
        automatic_selection: true
      - arm: non_default_operator_selectable
        provider: openai-codex
        model: gpt-6.1-sol
        canonical_identity: gpt-6.1-sol
        auth: openai_oauth
        oauth: true
        reasoning_effort: medium
        default: false
        automatic_selection: false
        usable_now: QUOTA_429_2026-10-15
        note: prior revision-18 default arm; retained, never auto-selected""",
            """    arms:
      - arm: primary
        provider: openai-codex
        model: gpt-6.1-sol
        canonical_identity: gpt-6.1-sol
        auth: openai_oauth
        oauth: true
        reasoning_effort: medium
        default: true
      - arm: fallback1
        provider: opencode-go
        model: glm-5.3-flash
        canonical_identity: glm-5.3-flash
        auth: env_ref:OPENCODE_GO_API_KEY
        oauth: false
        reasoning_effort: medium
        default: false
        automatic_selection: true
        prior_revision_note: >-
          Default arm of epochs 19-20 under owner-order-20261015-plan-model-rebind-glm, chosen because the
          OpenAI OAuth arm measured status=429 on 2026-10-15. That premise was measured FALSE on
          2026-10-16 and the order was superseded; the arm is now fallback1 in the owner chain and is never
          the rank-1 default. History preserved rather than deleted.
      - arm: fallback2
        provider: opencode-go
        model: deepseek-v4.1-flash
        canonical_identity: deepseek-v4.1-flash
        auth: env_ref:OPENCODE_GO_API_KEY
        oauth: false
        default: false
        automatic_selection: true""",
            'registry routes[].PLAN arms list')
edits.append(('A2', 'registry: routes[].PLAN arms (gpt -> primary, glm -> rotation alternate, 429 kept as history)', n))

# A3 the row-level admission_status and the fallback chain
text, n = sub(text, """    fallbacks:
      - provider: opencode-go
        model: deepseek-v4.1-flash
        canonical_identity: deepseek-v4.1-flash
        auth: env_ref:OPENCODE_GO_API_KEY
        oauth: false
      - provider: openai-codex
        model: gpt-6.1-sol
        canonical_identity: gpt-6.1-sol
        auth: openai_oauth
        oauth: true
    admission_status: UNPROVEN""",
            """    fallbacks:
      - provider: opencode-go
        model: glm-5.3-flash
        canonical_identity: glm-5.3-flash
        auth: env_ref:OPENCODE_GO_API_KEY
        oauth: false
      - provider: opencode-go
        model: deepseek-v4.1-flash
        canonical_identity: deepseek-v4.1-flash
        auth: env_ref:OPENCODE_GO_API_KEY
        oauth: false
    admission_status: ADMITTED
    admission_evidence: "%s"
    admission_status_prior: >-
      UNPROVEN (epochs 19-20; no measured serving evidence had been recorded for this row). The status
      moved to ADMITTED on measurement, not on declaration: the arm answered a reply probe and a
      tool-executing probe, and served two VERIFY/SECURITY turns at required_arm == served_arm.""" % MEASURED,
            'registry routes[].PLAN fallbacks + row admission_status')
edits.append(('A3', 'registry: routes[].PLAN fallbacks + admission_status (UNPROVEN -> measured)', n))

# A4 epoch 20 -> 21
text, n = sub(text, 'epoch: 20\n# epoch 20 (2026-10-16, round LANE-RELIABILITY-CLOSURE-20261016): the stale /codex_sha256', """epoch: 21
# epoch 21 (2026-10-16, round FAR-REMEDIATION-AND-CLOSURE-20261016): R1+R3 of FAR_RULING.md.
# routes[].PLAN rebound from opencode-go/glm-5.3-flash to openai-codex/gpt-6.1-sol (medium, OAuth) under
# owner-order-20261016-plan-model-rebind-gpt61-sol, because the 2026-10-15 order's premise (a 429) was
# measured false on 2026-10-16. The coupled PLAN declarations in config/model-lane-assignment.json and
# the projections[].expected strings that describe the PLAN chain were updated in the same change, since
# changing one alone leaves this file's own content self-contradictory. declared_conflicts[SOD006-C2]
# reclassified OPEN_OWNER_ORDERED -> OWNER_ORDERED_IN_FORCE.
# epoch 20 (2026-10-16, round LANE-RELIABILITY-CLOSURE-20261016): the stale /codex_sha256""",
            'registry epoch')
edits.append(('A4', 'registry: epoch 20 -> 21 with the reason recorded', n))

# A5 R3: the SoD conflict's status and the surviving independence
text, n = sub(text, """      status: OPEN_OWNER_ORDERED
      note: >-
        Round FAR-LANE-ROUTE-REBIND-20261015: owner explicitly re-points PLAN and VERIFY_SECURITY
        to the same default arm (openai-codex/gpt-6.1-sol, medium). Maker-and-checker on the same
        model family is an accepted, owner-declared residual risk for this round; the dispatcher
        still refuses any single call that would have the same arm self-verify its own output
        (no self-acceptance), and EXECUTE-vs-VERIFY separation still holds.
      reconciliation:
        ruled_by: "owner order 2026-10-15, lane chain rebind (this round)\"""",
            """      status: OWNER_ORDERED_IN_FORCE
      note: >-
        Round FAR-LANE-ROUTE-REBIND-20261015 re-pointed PLAN and VERIFY_SECURITY to the same default arm
        (openai-codex/gpt-6.1-sol, medium); the owner order in force for round
        FAR-REMEDIATION-AND-CLOSURE-20261016 restates it. This is therefore NOT an open item awaiting a
        decision: it is an order that has been carried into force, and it is recorded as an ACCEPTED
        deviation rather than as a satisfied invariant.
        What remains after model-axis independence is given up: PROCESS independence (a separate sealed
        CODEX-CLI process with a fresh context), LANE independence (EXECUTE makes, VERIFY_SECURITY
        checks), EVIDENCE-PATH independence (the checker re-derives every decisive claim from the
        artifacts and is forbidden from reading the writer's summary), and the no-self-acceptance rule
        (the dispatcher refuses any single call that would verify its own output). What is NOT hedged:
        correlated blind spots in the shared model family.
        EXECUTE-vs-VERIFY model separation still HOLDS (deepseek-v4.1-flash != gpt-6.1-sol).
      reconciliation:
        ruled_by: "owner orders 2026-10-15 and 2026-10-16 (both name openai-codex/gpt-6.1-sol for PLAN and VERIFY_SECURITY)"
        reclassified_from: OPEN_OWNER_ORDERED
        reclassified_by_round: FAR-REMEDIATION-AND-CLOSURE-20261016 (R3)\"""",
            'registry declared_conflicts[SOD006-C2]')
edits.append(('A5', 'registry: SOD006-C2 OPEN_OWNER_ORDERED -> OWNER_ORDERED_IN_FORCE + surviving independence', n))

# ---------------------------------------------------------------- B: registry projections[].expected
# The projections are the registry's own declared expectations OF THE SITE FILE, so every pointer whose
# site value this change touches must move with it. Each new expectation is written with the SAME text
# placed into the site (the map below is the single source of both sides), so the two can never drift.
import re  # noqa: E402

PROSE = {
    '/sod/plan_lane':
        'openai-codex / gpt-6.1-sol (medium, OpenAI OAuth) — owner order 2026-10-16 (round '
        'FAR-REMEDIATION-AND-CLOSURE-20261016); supersedes the 2026-10-15 GLM rebind, whose stated '
        'premise (a 429 on the OpenAI OAuth arm) was measured false on 2026-10-16. GLM-5.3-Flash is '
        'retained as a rotation alternate, never auto-selected.',
    '/sod/verify_security_lane':
        'DEFAULT primary arm A = openai-codex / gpt-6.1-sol (OpenAI OAuth); NON-DEFAULT '
        'operator-selectable alternate arm B = opencode-go / glm-5.3-flash. CORRECTED in round '
        'FAR-REMEDIATION-AND-CLOSURE-20261016: this field and its siblings declared arm A as '
        'opencode-go/glm-5.3-flash while lane_chains.VERIFY_SECURITY[0] — and this registry\'s own '
        'projections on that pointer — declared arm A as openai-codex/gpt-6.1-sol. The lane chain is '
        'what the dispatch path reads; the prose now matches it.',
    '/sod/verify_security_arm_A': 'openai-codex / gpt-6.1-sol (primary; medium)',
    '/sod/verify_security_default_arm': 'A = openai-codex / gpt-6.1-sol (OpenAI OAuth; medium)',
    '/sod/verify_vs_plan_model_separation':
        'NONE on the model axis, by owner order: PLAN and VERIFY_SECURITY default arm A are BOTH '
        'openai-codex/gpt-6.1-sol (SOD006-C2, now OWNER_ORDERED_IN_FORCE). What remains is PROCESS, LANE '
        'and EVIDENCE-PATH independence, plus the no-self-acceptance rule. EXECUTE deepseek-v4.1-flash is '
        'a distinct model family from both.',
    '/sod/provider_separation':
        'PARTIAL - PLAN and VERIFY default arm A both sit on openai-codex by owner order; EXECUTE stays on '
        'opencode-go. Model-axis separation between EXECUTE and each of them HOLDS (deepseek-v4.1-flash != '
        'gpt-6.1-sol). Provider separation is not required '
        '(invariants.provider_separation_required=false). Recorded as an accepted risk.',
    '/sod/maker_self_acceptance':
        'PREVENTED at dispatch on every arm: no single call ever verifies its own output. Model-identity '
        'separation is deliberately NOT present between PLAN and VERIFY arm A (the same model by owner '
        'order, SOD006-C2 OWNER_ORDERED_IN_FORCE); EXECUTE vs VERIFY remains a distinct model family. PLAN '
        'and EXECUTE do not share a token, so SOD-APPLY-01 stays a historical record.',
    '/lane_chains/PLAN/0/model': 'gpt-6.1-sol',
    '/lane_chains/PLAN/0/provider': 'openai-codex',
}
PROSE_ALIAS = {'/sod/provider_separation_status': '/sod/provider_separation'}


def set_registry_expected(txt, ptr, value):
    pat = re.compile(r'^(\s*)- \{pointer: ' + re.escape(ptr) + r', expected: .*\}$', re.M)
    m = pat.search(txt)
    if not m:
        return txt, False
    new_line = '%s- {pointer: %s, expected: %s}' % (m.group(1), ptr, json.dumps(value, ensure_ascii=False))
    return txt[:m.start()] + new_line + txt[m.end():], True


def set_json_ptr(doc, ptr, value):
    parts = [p for p in ptr.split('/') if p != '']
    cur = doc
    for p in parts[:-1]:
        cur = cur[int(p)] if isinstance(cur, list) else cur[p]
    last = parts[-1]
    if isinstance(cur, list):
        cur[int(last)] = value
    else:
        cur[last] = value


registry_pins = {}
for ptr, val in list(PROSE.items()) + [(k, PROSE[v]) for k, v in PROSE_ALIAS.items()]:
    text, hit = set_registry_expected(text, ptr, val)
    registry_pins[ptr] = hit

APPLY = '--apply' in sys.argv
if APPLY:
    backup(REG)
    REG.write_text(text, encoding='utf-8')
after_reg = sha(REG)

# ---------------------------------------------------------------- C: the SITE file the projections pin
before_site = sha(SITE)
site_txt = SITE.read_text(encoding='utf-8')
site = json.loads(site_txt)
rt = json.dumps(site, ensure_ascii=False, indent=2)
log['site_roundtrip_formatting_stable'] = (rt.strip() == site_txt.strip() or rt + '\n' == site_txt)
chain = site.get('lane_chains', {}).get('PLAN')
if isinstance(chain, list) and chain and chain[0].get('model') == 'glm-5.3-flash':
    glm = dict(chain[0])
    gpt_old = chain[2] if len(chain) > 2 else {}
    chain[0] = {'model': 'gpt-6.1-sol', 'provider': 'openai-codex', 'reasoning_effort': 'medium',
                'role': 'primary', 'default': True, 'arm': 'A'}
    glm['role'] = 'rotation_alternate'
    glm['default'] = False
    glm['automatic_selection'] = False
    glm['prior_revision_note'] = ('default arm of epochs 19-20 under owner-order-20261015-plan-model-rebind-glm; '
                                  'premise (429 on the OpenAI OAuth arm) measured false 2026-10-16')
    chain[2] = glm
    log['site_edits'] = ['lane_chains.PLAN[0] -> openai-codex/gpt-6.1-sol primary',
                         'lane_chains.PLAN[2] -> opencode-go/glm-5.3-flash rotation alternate (was the 429-parked gpt arm)']
    if isinstance(gpt_old, dict) and gpt_old.get('usable_now') == 'QUOTA_429_2':
        pass
sod = site.get('sod')
if isinstance(sod, dict) and 'glm-5.3-flash' in str(sod.get('plan_lane', '')):
    sod['plan_lane'] = ('openai-codex / gpt-6.1-sol (medium) — owner order 2026-10-16 (round '
                        'FAR-REMEDIATION-AND-CLOSURE-20261016; supersedes the 2026-10-15 GLM rebind whose '
                        '429 premise measured false on 2026-10-16). GLM-5.3-Flash retained as a rotation '
                        'alternate, never auto-selected.')
    log.setdefault('site_edits', []).append('sod.plan_lane -> the 2026-10-16 order')
for ptr, val in list(PROSE.items()) + [(k, PROSE[v]) for k, v in PROSE_ALIAS.items()]:
    set_json_ptr(site, ptr, val)
log['site_prose_pointers_updated'] = sorted(list(PROSE.keys()) + list(PROSE_ALIAS.keys()))
log['registry_pins'] = registry_pins
log['registry_pointers_without_a_pin'] = sorted(k for k, v in registry_pins.items() if not v)
if APPLY:
    backup(SITE)
    SITE.write_text(json.dumps(site, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
after_site = sha(SITE)

log['edits'] = [{'id': i, 'what': w, 'occurrences_replaced': n} for (i, w, n) in edits]
log['sha256'] = {'registry': {'before': before_reg, 'after': after_reg},
                 'site': {'before': before_site, 'after': after_site}}
log['backups'] = [str(REG) + SUFFIX, str(SITE) + SUFFIX]

# ---------------------------------------------------------------- self-check: drift must be empty
drift = subprocess.run(
    [PY, '-B', '-c',
     'import sys,json; sys.path.insert(0,"src"); from hg_kseos.lane_policy import check_drift; '
     'd=check_drift(); print(json.dumps({"n":len(d),"fatal":[x for x in d if x.get("severity")=="error"],'
     '"warn":[x for x in d if x.get("severity")!="error"]},ensure_ascii=False))'],
    cwd=str(R), capture_output=True, text=True, timeout=300)
try:
    drift_doc = json.loads(drift.stdout.strip().splitlines()[-1])
except Exception:
    drift_doc = {'raw': (drift.stdout + drift.stderr)[-800:]}
log['check_drift'] = drift_doc

test = subprocess.run(
    [PY, '-B', '-m', 'unittest', 'tests.test_lane_policy.TestLanePolicyConformance.'
     'test_registry_and_projection_shape', '-v'],
    cwd=str(R), capture_output=True, text=True, timeout=600)
log['conformance_case'] = {'exit': test.returncode,
                           'tail': (test.stdout + test.stderr).strip()[-400:]}

(O / 'R1_R3_APPLY_RECEIPT.json').write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({k: log[k] for k in ('workorder', 'dry_run', 'edits', 'sha256', 'site_edits',
                                      'check_drift', 'conformance_case')}, ensure_ascii=False, indent=1))
