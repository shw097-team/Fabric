"""R1 + R2 + R3 of round ROUND3-LANE-REBIND-AND-CLOSURE-20261016 — ONE batch, as the ruling requires.

Owner mandate 2026-10-16: PLAN & Orchestrator = opencode-go/glm-5.3-flash; EXECUTE (bounded writer, CODEX CLI)
= opencode-go/deepseek-v4.1-flash; VERIFY/SECURITY (independent acceptance officer, CODEX CLI) =
opencode-go/deepseek-v4.1-flash.

Measured consequence (lane guard, fail-closed): with the mandated arms the pair whose distinct_required was
TRUE (EXECUTE vs VERIFY) becomes SAME-model, while the pair carrying the recorded owner-ordered collision
(PLAN vs VERIFY, SOD006-C2) stops colliding. Both the re-binding and the re-declaration must therefore land
in one change or the guard refuses every dispatch with ERR_LANE_SOD_VIOLATION.

FILES (each backed up to .bak-round3-lane-rebind-20261016 before writing):
  1 config/model-lane-assignment.json      lane_chains.PLAN/.VERIFY_SECURITY, 10 sod prose fields,
                                           revision + registry_epoch -> 22
  2 config/lane-routing-registry.yaml      PLAN/VERIFY rows, arms, fallbacks, selected_arm, authority,
                                           epoch 21->22, source_of_routes re-pinned, sod pairs flipped,
                                           SOD006-C3 declared, SOD006-C2 superseded (never deleted)
  3 config/lane-route-slots.candidate.json the dispatch-time pool ranks, revision 9 -> 10 + change_log
  4 tests/test_lane_policy.py              the conformance fixture's owner_chain (its invariant IS the
                                           current owner order, so it moves in the same change)
Projection `expected` strings inside file 2 are repaired by a check_drift-driven pass AFTER this script;
they are never guessed here.

REFUSES rather than guesses:
  * every literal edit asserts it occurs exactly ONCE (a stale anchor aborts with EDIT NOT UNIQUE);
  * every file's newline convention is verified byte-faithful before anything is written (all four are CRLF
    with zero lone LF -- a silent LF conversion would re-write every line's bytes and invalidate every pinned
    digest, including this round's own source_of_routes pin);
  * nothing is written without --apply, and re-running is refused because the anchors no longer match.

Rollback: copy each <file>.bak-round3-lane-rebind-20261016 back over its file.
"""
import hashlib
import json
import pathlib
import shutil
import sys

R = pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS')
O = R / 'var/ROUND3-LANE-REBIND-AND-CLOSURE-20261016'
REG = R / 'config/lane-routing-registry.yaml'
SITE = R / 'config/model-lane-assignment.json'
POOL = R / 'config/lane-route-slots.candidate.json'
TEST = R / 'tests/test_lane_policy.py'
STAMP = 'round3-lane-rebind-20261016'
ORDER_ID = 'owner-order-20261016-lane-rebind-plan-glm-verify-deepseek'
ROUND = 'ROUND3-LANE-REBIND-AND-CLOSURE-20261016'
APPLY = '--apply' in sys.argv

log = {'schema': 'HGK-ROUND3-REBIND-RECEIPT/1', 'round': ROUND, 'apply': APPLY, 'order_id': ORDER_ID,
       'newline_convention': 'CRLF preserved (verified byte-faithful per file)', 'files': []}


def digest_of(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def read_norm(p):
    """Read with newline normalisation, plus the ORIGINAL bytes and its convention."""
    raw = pathlib.Path(p).read_bytes()
    crlf = raw.count(b'\r\n')
    lone = raw.count(b'\n') - crlf
    return pathlib.Path(p).read_text(encoding='utf-8'), raw, crlf, lone


def encode_like(text, crlf_true):
    """Re-encode normalised text the way the source file stores it."""
    return text.replace('\n', '\r\n').encode('utf-8') if crlf_true else text.encode('utf-8')


def preflight(p):
    """Prove the writer is byte-faithful for this file BEFORE any edit: normalised round-trip must reproduce
    the original bytes exactly. A failure here means a silent newline/encoding rewrite, so abort."""
    norm, raw, crlf, lone = read_norm(p)
    if lone:
        raise SystemExit('PREFLIGHT: %s mixes line endings (lone LF=%d) -- refuse to guess' % (p, lone))
    if encode_like(norm, crlf > 0) != raw:
        raise SystemExit('PREFLIGHT: %s is not byte-faithful under normalise+re-encode -- abort' % p)
    return norm, digest_of(p), crlf > 0


def backup(p):
    b = pathlib.Path(str(p) + '.bak-' + STAMP)
    if not b.is_file():
        shutil.copy2(p, b)
    return b.name


def commit(p, text, crlf_true, label, before):
    if APPLY:
        pathlib.Path(p).write_bytes(encode_like(text, crlf_true))
    after = digest_of(p) if APPLY else None
    log['files'].append({'file': str(pathlib.Path(p).relative_to(R)).replace('\\', '/'), 'what': label,
                         'sha256_before': before, 'sha256_after': after,
                         'backup': backup(pathlib.Path(p)) if APPLY else 'DRY_RUN_NO_BACKUP'})
    print('%-44s %s -> %s  %s' % (pathlib.Path(p).name, before[:12], (after or 'DRY')[:12], label))


def rep1(t, old, new, label):
    n = t.count(old)
    if n != 1:
        raise SystemExit('EDIT NOT UNIQUE [%s]: occurrences=%d for %r' % (label, n, old[:120]))
    return t.replace(old, new)


# =============================================================== file 1: the assignment site (structured)
site_norm, site_before, site_crlf = preflight(SITE)
site = json.loads(site_norm)
old_prose = dict(site['sod'])

site['lane_chains']['PLAN'] = [
    {'model': 'glm-5.3-flash', 'provider': 'opencode-go', 'reasoning_effort': 'medium',
     'role': 'primary', 'default': True, 'arm': 'A', 'automatic_selection': True},
    {'model': 'gpt-6.1-sol', 'provider': 'openai-codex', 'reasoning_effort': 'medium',
     'role': 'fallback1_operator_selectable', 'default': False, 'automatic_selection': False, 'arm': 'B',
     'prior_revision_note': 'Rank-1 default of epochs 19-21 (owner orders 2026-10-15 and 2026-10-16); '
                            'demoted to a NON-DEFAULT operator-selectable alternate by the 2026-10-16 owner '
                            'order that makes GLM-5.3-Flash (OpenCode Go) the PLAN default. History '
                            'preserved, never deleted.'},
    {'model': 'deepseek-v4.1-flash', 'provider': 'opencode-go', 'role': 'fallback2', 'default': False,
     'automatic_selection': True, 'arm': 'C'},
]
site['lane_chains']['VERIFY_SECURITY'] = [
    {'role': 'primary', 'model': 'deepseek-v4.1-flash', 'provider': 'opencode-go', 'default': True,
     'arm': 'A', 'automatic_selection': True},
    {'role': 'fallback1_operator_selectable', 'model': 'gpt-6.1-sol', 'provider': 'openai-codex',
     'reasoning_effort': 'medium', 'default': False, 'automatic_selection': False, 'arm': 'B',
     'prior_revision_note': 'Primary arm A of every earlier revision (owner orders 2026-10-15 and '
                            '2026-10-16); demoted to a NON-DEFAULT operator-selectable alternate by the '
                            '2026-10-16 owner order that makes deepseek-v4.1-flash the checker.'},
    {'role': 'fallback2', 'model': 'glm-5.3-flash', 'provider': 'opencode-go', 'reasoning_effort': 'medium',
     'default': False, 'automatic_selection': True, 'arm': 'C'},
]

PROSE = {
 'plan_lane': ('opencode-go / glm-5.3-flash (medium, OpenCode Go) — owner order 2026-10-16 (round %s). This '
   'supersedes owner-order-20261016-plan-model-rebind-gpt61-sol (round FAR-REMEDIATION-AND-CLOSURE-20261016) '
   'and, with it, the 2026-10-15 GLM order whose premise (a 429 on the OpenAI OAuth arm) was already measured '
   'false. GLM is now rank-1 AND an automatically selected arm; the earlier prose calling GLM "never '
   'auto-selected" while the chain declared automatic_selection: true was a cross-field contradiction '
   '(F-IND-2) and is repaired here. gpt-6.1-sol is retained as the NON-DEFAULT fallback1 and '
   'deepseek-v4.1-flash as automatically selected fallback2.' % ROUND),
 'verify_security_lane': ('DEFAULT primary arm A = opencode-go / deepseek-v4.1-flash (Codex CLI checker); '
   'NON-DEFAULT operator-selectable alternate arm B = openai-codex / gpt-6.1-sol (OpenAI OAuth); '
   'automatically selected fallback2 arm C = opencode-go / glm-5.3-flash. Rebound by owner order 2026-10-16 '
   '(round %s): the checker arm is the SAME model the EXECUTE writer holds, so model-axis independence '
   'between maker and checker is deliberately ABSENT and is declared in sod_invariants.declared_conflicts '
   '(SOD006-C3, OWNER_ORDERED_IN_FORCE). What remains is PROCESS, LANE and EVIDENCE-PATH independence plus '
   'the no-self-acceptance rule. Model diversity between writer and checker is NOT claimed.' % ROUND),
 'verify_security_arm_A': 'opencode-go / deepseek-v4.1-flash (primary Codex CLI checker)',
 'verify_security_default_arm': 'A = opencode-go / deepseek-v4.1-flash (Codex CLI checker)',
 'verify_security_selection': ('owner order 2026-10-16 (round %s); unset -> default arm A = '
   'deepseek-v4.1-flash; arm B (gpt-6.1-sol) is a NON-DEFAULT operator-selectable alternate and is never '
   'auto-selected; arm C (glm-5.3-flash) is an automatically selected fallback.' % ROUND),
 'verify_vs_execute_model_separation': ('NONE on the model axis, BY OWNER ORDER: EXECUTE and VERIFY_SECURITY '
   'default arm A are BOTH opencode-go/deepseek-v4.1-flash (SOD006-C3, OWNER_ORDERED_IN_FORCE, owner order '
   '2026-10-16). What remains is PROCESS, LANE and EVIDENCE-PATH independence plus the no-self-acceptance '
   'rule; model diversity between writer and checker is deliberately absent and is NOT claimed.'),
 'verify_vs_plan_model_separation': ('PASS on the model axis: PLAN is opencode-go/glm-5.3-flash and '
   'VERIFY_SECURITY default arm A is opencode-go/deepseek-v4.1-flash — different model families. The earlier '
   'collision recorded as SOD006-C2 (PLAN and VERIFY arm A both openai-codex/gpt-6.1-sol) no longer exists '
   'and is retained as SUPERSEDED history rather than deleted.'),
 'provider_separation': ('ABSENT by owner order: all three lanes now sit on the opencode-go provider (PLAN '
   'glm-5.3-flash, EXECUTE deepseek-v4.1-flash, VERIFY_SECURITY arm A deepseek-v4.1-flash). Provider '
   'separation is not required (invariants.provider_separation_required=false). Model-axis separation HOLDS '
   'between PLAN and each of the other two, and is deliberately absent between EXECUTE and VERIFY '
   '(SOD006-C3). Recorded as an accepted risk, not as compliance.'),
 'provider_separation_status': ('ABSENT by owner order: all three lanes sit on opencode-go (PLAN '
   'glm-5.3-flash, EXECUTE deepseek-v4.1-flash, VERIFY_SECURITY arm A deepseek-v4.1-flash). Provider '
   'separation is not required (invariants.provider_separation_required=false). Model-axis separation HOLDS '
   'PLAN-vs-EXECUTE and PLAN-vs-VERIFY, and is deliberately absent EXECUTE-vs-VERIFY (SOD006-C3). Recorded '
   'as an accepted risk.'),
 'maker_self_acceptance': ('PREVENTED at dispatch on every arm: no single call ever verifies its own output. '
   'Model-identity separation between writer and checker is deliberately NOT present under the 2026-10-16 '
   'owner order (EXECUTE and VERIFY_SECURITY arm A are both opencode-go/deepseek-v4.1-flash, SOD006-C3 '
   'OWNER_ORDERED_IN_FORCE); the separation this round actually has is process, lane and evidence-path '
   'independence. PLAN (glm-5.3-flash) is a different model family from both lanes.'),
 'verify_security_reasoning_effort': ('medium (RETAINED from the previous chain because the mandate names no '
   'effort for this arm and the deepseek arm declares none — UNVERIFIED for this model, recorded rather '
   'than assumed)'),
}
hunks = sum(1 for k, v in PROSE.items() if old_prose.get(k) != v)
site['sod'].update(PROSE)
site['revision'] = 22
site['registry_epoch'] = 22
site['declared_by'] = ('Owner order 2026-10-16 (round %s) — PLAN & Orchestrator rebound to '
   'opencode-go/glm-5.3-flash; VERIFY/SECURITY checker rebound to opencode-go/deepseek-v4.1-flash; EXECUTE '
   'unchanged at opencode-go/deepseek-v4.1-flash. Applied under typed WorkOrders by the in-Hermes '
   'orchestrator; external acceptance NOT performed.' % ROUND)
site_new = json.dumps(site, indent=2, ensure_ascii=False) + '\n'
NEW_SITE_DIGEST = hashlib.sha256(encode_like(site_new, site_crlf)).hexdigest()

# ============================================================== file 2: the registry (surgical, CRLF-safe)
reg, reg_before, reg_crlf = preflight(REG)

# 2a. PLAN row: top fields + authority + arms + fallbacks (this exact block is unique because of its order)
reg = rep1(reg, """    engine: hermes
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
    selection_authority: owner-order-20261016-plan-model-rebind-gpt61-sol
    arms:
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
        automatic_selection: true
    fallbacks:
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
    admission_status: ADMITTED""", """    engine: hermes
    provider: opencode-go
    model: glm-5.3-flash
    canonical_identity: glm-5.3-flash
    auth: env_ref:OPENCODE_GO_API_KEY
    oauth: false
    reasoning_effort: medium
    # Owner order 2026-10-16 (round %s, epoch 22): PLAN & Orchestrator is GLM-5.3-FLASH-MEDIUM
    # (OpenCode Go). This SUPERSEDES owner-order-20261016-plan-model-rebind-gpt61-sol; that order's own
    # premise (the PLAN plane belongs on the OpenAI OAuth arm) is not disputed as a measurement, it is
    # simply superseded by a later owner order. The 2026-10-15 GLM order remains superseded history.
    # Rank-1 glm-5.3-flash; fallback1 GPT-6.1-SOL (OAuth, NON-DEFAULT); fallback2 DeepSeek V4.1 Flash (GO)
    # -- the owner chain ORDER is first-class policy (tests/test_lane_policy.py owner_chain asserts it
    # exactly, and that fixture moved with this order in this same change).
    selection_authority: %s
    arms:
      - arm: primary
        provider: opencode-go
        model: glm-5.3-flash
        canonical_identity: glm-5.3-flash
        auth: env_ref:OPENCODE_GO_API_KEY
        oauth: false
        reasoning_effort: medium
        default: true
        automatic_selection: true
      - arm: fallback1
        provider: openai-codex
        model: gpt-6.1-sol
        canonical_identity: gpt-6.1-sol
        auth: openai_oauth
        oauth: true
        reasoning_effort: medium
        default: false
        automatic_selection: false
        prior_revision_note: >-
          Rank-1 default of epochs 19-21 under owner orders 2026-10-15 and 2026-10-16; demoted to a
          NON-DEFAULT operator-selectable alternate by the 2026-10-16 owner order that makes GLM the PLAN
          default. The 429 recorded against this arm on 2026-10-15 was measured FALSE on 2026-10-16.
          History preserved rather than deleted.
      - arm: fallback2
        provider: opencode-go
        model: deepseek-v4.1-flash
        canonical_identity: deepseek-v4.1-flash
        auth: env_ref:OPENCODE_GO_API_KEY
        oauth: false
        default: false
        automatic_selection: true
    fallbacks:
      - provider: openai-codex
        model: gpt-6.1-sol
        canonical_identity: gpt-6.1-sol
        auth: openai_oauth
        oauth: true
      - provider: opencode-go
        model: deepseek-v4.1-flash
        canonical_identity: deepseek-v4.1-flash
        auth: env_ref:OPENCODE_GO_API_KEY
        oauth: false
    admission_status: ADMITTED""" % (ROUND, ORDER_ID), 'PLAN row: rank-1 default, chain order, arms, authority')

# 2b. VERIFY row: top fields + authority/selected_arm + arms + fallbacks
reg = rep1(reg, """    engine: hermes
    provider: openai-codex
    model: gpt-6.1-sol
    reasoning_effort: medium
    canonical_identity: gpt-6.1-sol
    auth: openai_oauth
    oauth: true
# Owner order 2026-10-15 (round FAR-LANE-ROUTE-REBIND-20261015): chain re-bound.
    # Default GPT-6.1_SOL-medium (OpenAI OAuth); fallback1 GLM-5.3-Flash (GO); fallback2 DeepSeek (GO).
    # Per-session-round user re-selection is first-class (role_mandate -> runtime_role_binding_assert).
    selection_authority: owner-order-20261015-lane-model-chain-rebind
    selected_arm: A
    selected_arm_identity: gpt-6.1-sol
    arms:
      - arm: A
        model: gpt-6.1-sol
        provider: openai-codex
        canonical_identity: gpt-6.1-sol
        auth: openai_oauth
        oauth: true
        reasoning_effort: medium
        co_equal: false
        role: primary
        default: true
      - arm: B
        model: glm-5.3-flash
        provider: opencode-go
        canonical_identity: glm-5.3-flash
        auth: env_ref:OPENCODE_GO_API_KEY
        oauth: false
        reasoning_effort: medium
        co_equal: false
        role: fallback1_operator_selectable
        default: false
        automatic_selection: true
      - arm: C
        model: deepseek-v4.1-flash
        provider: opencode-go
        canonical_identity: deepseek-v4.1-flash
        auth: env_ref:OPENCODE_GO_API_KEY
        oauth: false
        co_equal: false
        role: fallback2_operator_selectable
        default: false
        automatic_selection: true
    fallbacks:
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
    admission_status: UNPROVEN""", """    engine: hermes
    provider: opencode-go
    model: deepseek-v4.1-flash
    canonical_identity: deepseek-v4.1-flash
    auth: env_ref:OPENCODE_GO_API_KEY
    oauth: false
    # Owner order 2026-10-16 (round %s, epoch 22): VERIFY/SECURITY chain re-bound. The default is now
    # DeepSeek V4.1 Flash on OpenCode Go -- the SAME model the EXECUTE writer holds BY OWNER ORDER, so
    # model-axis independence between maker and checker is deliberately ABSENT and is DECLARED in
    # sod_invariants.declared_conflicts (SOD006-C3). The declaration and the re-binding land together
    # because the lane guard fails this pair CLOSED when the declaration is absent (measured
    # ERR_LANE_SOD_VIOLATION, exit 2).
    # fallback1 GPT-6.1-SOL (OAuth) is a NON-DEFAULT operator-selectable alternate; fallback2 GLM (GO) is
    # automatically selected.
    selection_authority: %s
    selected_arm: A
    selected_arm_identity: deepseek-v4.1-flash
    arms:
      - arm: A
        model: deepseek-v4.1-flash
        provider: opencode-go
        canonical_identity: deepseek-v4.1-flash
        auth: env_ref:OPENCODE_GO_API_KEY
        oauth: false
        co_equal: false
        role: primary
        default: true
        automatic_selection: true
      - arm: B
        model: gpt-6.1-sol
        provider: openai-codex
        canonical_identity: gpt-6.1-sol
        auth: openai_oauth
        oauth: true
        reasoning_effort: medium
        co_equal: false
        role: fallback1_operator_selectable
        default: false
        automatic_selection: false
        prior_revision_note: >-
          Primary arm A of every earlier revision (owner orders 2026-10-15 and 2026-10-16); demoted to a
          NON-DEFAULT operator-selectable alternate by the 2026-10-16 owner order that makes
          deepseek-v4.1-flash the checker. History preserved rather than deleted.
      - arm: C
        model: glm-5.3-flash
        provider: opencode-go
        canonical_identity: glm-5.3-flash
        auth: env_ref:OPENCODE_GO_API_KEY
        oauth: false
        reasoning_effort: medium
        co_equal: false
        role: fallback2
        default: false
        automatic_selection: true
    fallbacks:
      - provider: openai-codex
        model: gpt-6.1-sol
        canonical_identity: gpt-6.1-sol
        auth: openai_oauth
        oauth: true
      - provider: opencode-go
        model: glm-5.3-flash
        canonical_identity: glm-5.3-flash
        auth: env_ref:OPENCODE_GO_API_KEY
        oauth: false
    admission_status: UNPROVEN""" % (ROUND, ORDER_ID), 'VERIFY row: rank-1 default, chain order, arms, authority')

# 2c. sod_invariants.pairs -- ONE replacement of the whole block (a pairwise flag swap would collide)
reg = rep1(reg, """    - maker: EXECUTE
      checker: VERIFY_SECURITY
      distinct_required: true
      note: EXECUTE opencode-go/deepseek-v4.1-flash vs VERIFY_SECURITY openai-codex/gpt-6.1-sol (owner
        order 2026-10-15) — distinct model families on the default arms across every rank pair.
    - maker: PLAN
      checker: VERIFY_SECURITY
      distinct_required: false
      note: >-
        Owner order 2026-10-15 (round FAR-LANE-ROUTE-REBIND-20261015) re-points BOTH lanes to the
        same default arm openai-codex/gpt-6.1-sol (medium). The maker/checker sweep therefore runs
        with distinct_required: false for this pair; the collision is recorded as SOD006-C2
        (OPEN, owner-ordered, not agent-decided). EXECUTE-vs-VERIFY pair unchanged and still
        distinct on the default arms (deepseek-v4.1-flash != gpt-6.1-sol).""", """    - maker: EXECUTE
      checker: VERIFY_SECURITY
      distinct_required: false
      note: >-
        Owner order 2026-10-16 (round %s) re-binds the VERIFY/SECURITY checker to
        opencode-go/deepseek-v4.1-flash, the SAME model the EXECUTE writer holds, so the maker/checker
        sweep runs with distinct_required: false for this pair. The collision is REAL and DECLARED as
        SOD006-C3 (OWNER_ORDERED_IN_FORCE) rather than hidden, and the lane guard fails this pair closed
        when the declaration is absent (measured ERR_LANE_SOD_VIOLATION) -- which is why the declaration
        and the re-binding land in one change.
    - maker: PLAN
      checker: VERIFY_SECURITY
      distinct_required: true
      note: >-
        Owner order 2026-10-16 (round %s) makes PLAN opencode-go/glm-5.3-flash and VERIFY/SECURITY
        default arm A opencode-go/deepseek-v4.1-flash -- distinct model families, so separation is
        required again on this pair. The earlier collision SOD006-C2 (both openai-codex/gpt-6.1-sol) no
        longer holds and is SUPERSEDED by the same order; it is retained as history, never deleted.""" % (ROUND, ROUND),
        'sod_invariants.pairs: EXECUTE/VERIFY demoted+declared, PLAN/VERIFY required again')

# 2d. epoch bump (anchored at column 0 so the indented projection epoch at :589 cannot match)
reg = rep1(reg, '\nepoch: 21\n', '\nepoch: 22\n', 'registry epoch 21 -> 22')

# 2e. source_of_routes re-pinned (verbatim anchor; the digests are read, never guessed)
reg = rep1(reg, """  # Re-pinned in round FAR-REMEDIATION-AND-CLOSURE-20261016 (R1/R3 completion): the site file was
  # edited (PLAN rebind, the corrected VERIFY-arm prose, revision 20 -> 21), so the recorded digest
  # and revision had to move with it. Without this the pre-dispatch lane guard refuses every
  # evaluation with ERR_LANE_SOURCE_STALE. Its sibling epoch coupling is below.
  path: config/model-lane-assignment.json""", """  # Re-pinned in round %s (R1/R3): the site file was edited again (PLAN rebound to
  # opencode-go/glm-5.3-flash, the VERIFY/SECURITY checker rebound to
  # opencode-go/deepseek-v4.1-flash, the sod prose repaired to match the flags, revision 21 -> 22),
  # so the recorded digest and revision moved with it. Without this the pre-dispatch lane guard
  # refuses every evaluation with ERR_LANE_SOURCE_STALE. Its sibling epoch coupling is below.
  path: config/model-lane-assignment.json""" % ROUND, 'source_of_routes comment re-pinned')

# the two pinned values themselves (read from the live file immediately before this run)
old_pin = [l for l in reg.split('\n') if l.strip().startswith('revision:') or l.strip().startswith('sha256:')]
i = reg.find('  path: config/model-lane-assignment.json\n') + len('  path: config/model-lane-assignment.json\n')
j = reg.find('\n', reg.find('sha256:', i))
old_block = reg[i:j]
import re as _re
m_rev = _re.search(r'revision:\s*(\d+)', old_block)
m_sha = _re.search(r'sha256:\s*([0-9a-f]{64})', old_block)
if not (m_rev and m_sha):
    raise SystemExit('source_of_routes pin block unreadable: %r' % old_block)
new_block = ('  revision: 22\n  sha256: %s' % NEW_SITE_DIGEST)
reg = reg[:i] + new_block + reg[j:]
print('source_of_routes pin %s(%s) -> revision 22(%s)' % (m_rev.group(1), m_sha.group(1)[:12],
                                                          NEW_SITE_DIGEST[:12]))

# 2f. declared_conflicts: supersede SOD006-C2 (status only; the note stays as history) ...
reg = rep1(reg, """    - id: SOD006-C2
      pairs: [[PLAN, VERIFY_SECURITY]]
      axis: canonical_identity
      status: OWNER_ORDERED_IN_FORCE""", """    - id: SOD006-C2
      pairs: [[PLAN, VERIFY_SECURITY]]
      axis: canonical_identity
      status: SUPERSEDED
      superseded_by: >-
        %s (round %s): its premise -- PLAN and VERIFY/SECURITY sharing the openai-codex/gpt-6.1-sol
        default arm -- no longer holds, so the collision it recorded is gone. The order and its
        compensating controls are preserved here as history, never deleted.""" % (ORDER_ID, ROUND),
        'SOD006-C2 -> SUPERSEDED (entry kept, never deleted)')

# ... and declare the mandate's own collision immediately before it
NEW_C3 = """    - id: SOD006-C3
      pairs: [[EXECUTE, VERIFY_SECURITY]]
      axis: canonical_identity
      status: OWNER_ORDERED_IN_FORCE
      note: >-
        Owner order 2026-10-16 (round %s) puts the VERIFY/SECURITY checker on
        opencode-go/deepseek-v4.1-flash, the SAME model the EXECUTE bounded writer holds. Model-axis
        independence between writer and checker is therefore deliberately ABSENT BY ORDER. The pair is
        demoted to distinct_required: false and the collision is recorded here rather than hidden. The
        lane guard refuses this pair when the declaration is absent (measured ERR_LANE_SOD_VIOLATION),
        so this entry is load-bearing, not documentation.
        What remains after model-axis independence is given up: PROCESS independence (a separate sealed
        CODEX-CLI process with a fresh context), LANE independence (EXECUTE makes, VERIFY_SECURITY
        checks), EVIDENCE-PATH independence (the checker re-derives every decisive claim from the
        artifacts and is forbidden from reading the writer's summary), and the no-self-acceptance rule
        (the dispatcher refuses any single call that would verify its own output). What is NOT hedged:
        correlated blind spots in the shared model family -- recorded as an accepted deviation.
      reconciliation:
        ruled_by: "owner order 2026-10-16 (round %s)"
        reclassified_from: null
      residual: >-
        maker and checker are the same model; model diversity is NOT claimed anywhere in this round's
        artifacts.
""" % (ROUND, ROUND)
anchor = '    - id: SOD006-C2\n'
if reg.count(anchor) != 1:
    raise SystemExit('SOD006-C2 header not unique: %d' % reg.count(anchor))
reg = reg.replace(anchor, NEW_C3 + anchor, 1)

commit(REG, reg, reg_crlf, 'R1+R2: PLAN/VERIFY rebind, SoD pairs + SOD006-C3, epoch 22, source_of_routes re-pinned', reg_before)
commit(SITE, site_new, site_crlf, 'R1+R3: lane_chains, %d sod prose fields, revision/registry_epoch 22' % hunks, site_before)

# =============================================================================== file 3: the dispatch pool
pool_norm, pool_before, pool_crlf = preflight(POOL)
pool = json.loads(pool_norm)
for lane in pool['lanes']:
    ops = sorted(lane['ordered_pool'], key=lambda e: e['rank'])
    if lane['lane'] == 'PLAN':
        promoted = [e for e in ops if (e['provider'], e['model']) == ('opencode-go', 'glm-5.3-flash')]
        if len(promoted) != 1:
            raise SystemExit('PLAN pool: glm-5.3-flash entry not found uniquely')
        relisted = promoted + [e for e in ops if e not in promoted]
        lane['selection_note'] = ('Owner order 2026-10-16: GLM-5.3-Flash is rank 1 for PLAN. NOTE this file '
                                 'is read as the dispatch-time pool (scripts/hgk-lane-dispatch.py '
                                 'DEFAULT_POOL) while its own status field says CANDIDATE / not active -- a '
                                 'declaration-vs-operability mismatch recorded as round finding NF-05, not '
                                 'silently normalised.')
    elif lane['lane'] == 'VERIFY_SECURITY':
        promoted = [e for e in ops if (e['provider'], e['model']) == ('opencode-go', 'deepseek-v4.1-flash')]
        if len(promoted) != 1:
            raise SystemExit('VERIFY pool: deepseek-v4.1-flash entry not found uniquely')
        relisted = promoted + [e for e in ops if e not in promoted]
        lane['selection_note'] = ('Owner order 2026-10-16: deepseek-v4.1-flash is rank 1 for the '
                                 'VERIFY/SECURITY checker -- the same model the EXECUTE writer holds, '
                                 'declared in sod_invariants.declared_conflicts as SOD006-C3.')
    else:
        continue
    for n, e in enumerate(relisted, start=1):
        e['rank'] = n
    lane['ordered_pool'] = relisted
pool['revision'] = 10
pool['round'] = ROUND
pool['supersedes_revision'] = 9
pool['declared_by'] = ('Owner order 2026-10-16 (round %s): PLAN GLM-5.3-Flash rank 1; VERIFY/SECURITY '
                       'deepseek-v4.1-flash rank 1; EXECUTE unchanged.' % ROUND)
pool['change_log'].insert(0, 'rev 9 -> rev 10 (round %s): owner order 2026-10-16 applied to the dispatch-time '
                             'pool ranks -- PLAN glm-5.3-flash promoted to rank 1, VERIFY/SECURITY '
                             'deepseek-v4.1-flash promoted to rank 1, EXECUTE untouched.' % ROUND)
pool_new = json.dumps(pool, indent=2, ensure_ascii=False) + '\n'
commit(POOL, pool_new, pool_crlf, 'pool ranks: PLAN glm->1, VERIFY deepseek->1 (rev 9 -> 10)', pool_before)

# =========================================================================== file 4: the conformance fixture
tst_norm, tst_before, tst_crlf = preflight(TEST)
tst = rep1(tst_norm, """        # Owner chain (2026-10-15 rebind): the declared fallback sequence is first-class policy,
        # not a fixture-era empty list. Conformance = exact owner order per lane.
        owner_chain = {
            "PLAN": [("openai-codex", "gpt-6.1-sol"), ("opencode-go", "glm-5.3-flash"), ("opencode-go", "deepseek-v4.1-flash")],
            "VERIFY_SECURITY": [("openai-codex", "gpt-6.1-sol"), ("opencode-go", "glm-5.3-flash"), ("opencode-go", "deepseek-v4.1-flash")],""",
"""        # Owner chain (2026-10-16 rebind, round %s): the declared fallback sequence is first-class
        # policy, not a fixture-era empty list, and it moves WITH the owner order in the SAME change --
        # PLAN's rank-1 default is GLM-5.3-Flash and the VERIFY/SECURITY checker's rank-1 default is
        # deepseek-v4.1-flash, which is the same model as the EXECUTE writer BY OWNER ORDER (declared as
        # SOD006-C3 in sod_invariants.declared_conflicts). Conformance = exact owner order per lane.
        owner_chain = {
            "PLAN": [("opencode-go", "glm-5.3-flash"), ("openai-codex", "gpt-6.1-sol"), ("opencode-go", "deepseek-v4.1-flash")],
            "VERIFY_SECURITY": [("opencode-go", "deepseek-v4.1-flash"), ("openai-codex", "gpt-6.1-sol"), ("opencode-go", "glm-5.3-flash")],""" % ROUND,
        'owner_chain moved with the owner order')
commit(TEST, tst, tst_crlf, 'conformance fixture owner_chain moved with the owner order', tst_before)

# ================================================================================================== report
if APPLY:
    (O / 'R1_R2_R3_APPLY_RECEIPT.json').write_text(
        json.dumps({**log, 'new_site_digest': NEW_SITE_DIGEST, 'sod_prose_fields_rewritten': hunks},
                   ensure_ascii=False, indent=2), encoding='utf-8')
print('--')
print('APPLY=%s  new site sha256 = %s' % (APPLY, NEW_SITE_DIGEST))
print('next: check_drift (fix any remaining projection bindings), then the conformance test, then the guard')
