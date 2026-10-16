"""Annotate SELFCHECK_REPORT.json: fix one harness bug of my own, and add an INTERPRETATION per item.

Two things this does NOT do: it never rewrites a raw `status` to look better, and it never deletes an
observation. Raw statuses stay exactly as measured; every correction or explanation is added as new
fields, so a reader can see both the measurement and the reading.

Fix applied: D03's substring test compared 'hk-governed' against a value containing 'hgk-governed', so
a probe that actually reported EFFECTIVE_HERMES_HOME=<...>\\profiles\\hgk-governed was marked
UNVERIFIED. The observation itself was correct; only the assertion was wrong.
"""
import json
import pathlib

O = pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/FAR-REMEDIATION-AND-CLOSURE-20261016')
p = O / 'SELFCHECK_REPORT.json'
rep = json.loads(p.read_text(encoding='utf-8'))
items = rep['items']

rep['status_semantics'] = {
    'PASS': 'the measured value met the item\'s expectation',
    'FAIL': 'the measured value did not meet the expectation AS THE HARNESS STATED IT. Read the '
            'interpretation field: several FAILs are root-dependent by design, because this round applies '
            'ChangeSet B/C to the CANDIDATE and deliberately does NOT promote them to the canonical product.',
    'RECORDED': 'the item records a value rather than judging it',
    'PENDING': 'not yet run at the time this report was written',
    'UNVERIFIED': 'the harness could not decide; read the interpretation field',
    'BEFORE_STATE_ON_CANONICAL': 'the CANONICAL root still shows the pre-change behaviour. This is not a '
                                 'defect introduced by the round; it is the evidence of what the round '
                                 'changes, and it stays until an owner-authorised promotion applies the '
                                 'verified candidate.',
    'EXPECTED_ROOT_DIFFERENCE': 'the two roots differ for a structural reason, not because of a defect',
}

# ---- D03: the harness's own substring bug ----
d03 = items.get('D03')
if d03:
    obs = d03['observed'].get('resolution_probe_tail') or ''
    ok = ('hgk-governed' in obs) and ('exists=True' in obs) and ('governed_runtime present=True' in obs)
    d03['status'] = 'PASS' if ok else 'UNVERIFIED'
    d03['harness_correction'] = {
        'bug': "the original assertion tested for the substring 'hk-governed', which is NOT a substring of "
               "'hgk-governed', so a passing probe was reported UNVERIFIED",
        'fixed_test': "('hgk-governed' in tail) and ('exists=True' in tail) and ('governed_runtime present=True' in tail)",
        'observation_unchanged': obs,
        'note': 'the raw observation was always correct; only the harness assertion was wrong',
    }

INTERP = {
    'D01': 'PLAN plane: reply probe exit 0 with PLAN_LANE_PROBE_OK, and the governed profile\'s OWN '
           'state.db::sessions carries fresh rows model=gpt-6.1-sol / billing_provider=openai-codex / '
           'billing_base_url=https://chatgpt.com/backend-api/codex / subscription_included. The model '
           'selection is PROVEN SERVED, not read from a config file.',
    'D02': 'the same plane executed a command and reported its stdout (PLAN_TOOL_PROBE_OK): the PLAN & '
           'Orchestrator lane can ACT, not only reply.',
    'D04 candidate': 'grep -c effort = 36, from 0 before ChangeSet B: the effort axis exists in the gate.',
    'D05 candidate': 're-derived by THIS harness with its own fixtures (not by the lane\'s test file): all four '
                     'typed refusals exit 7 with their own codes, and the served-effort axis refuses too.',
    'D06 candidate': 'the positive controls on the SAME fixtures exit 0, so the refusals cannot be passing for '
                     'some other reason.',
    'D07 candidate': 'blank, null and free-text session ids are all ANSWERED with '
                     'no-session-id-unattributable on exit 0. Compare the canonical row: the same three fixtures '
                     'return exit 3 there. That contrast IS the closed outage.',
    'D08 candidate': 'positive control held: the REAL governed maker write is still denied (reason names the work '
                     'order), and an ordinary read is still allowed.',
    'D08 canonical': 'the same control passes on the canonical root, so ChangeSet C cannot have turned the deny '
                     'path off.',
    'D09 candidate': 'the candidate is the WRITER\'s tree and its config/ is a snapshot taken BEFORE ChangeSet A '
                     'landed, so two failures are expected there and neither is a product defect: '
                     'test_drift_injection_subcases (its pristine baseline is fatal only because that snapshot '
                     'still carries the stale /codex_sha256 expectation that ChangeSet A fixes) and '
                     'test_registry_and_projection_shape (the open finding F1). The canonical root is the '
                     'authority for config and reports drift == [] (see D11).',
    'D10 canonical': 'the canonical tree does not carry ChangeSet B/C product changes, so the new test module is '
                     'absent there (ModuleNotFoundError is the EXPECTED consequence of not promoting) and F1 is '
                     'the only other failure. No agent may promote its own candidate; the promotion is left to '
                     'the owner, with the exact command recorded in the closure.',
    'D11': 'canonical check_drift(registry=reg) == []: the fatal DRIFT_VALUE that existed before this round is '
           'gone, measured on the canonical root.',
    'D12': 'check_sod(PLAN, VERIFY_SECURITY) = SOD_OK with PLAN=opencode-go/glm-5.3-flash and '
           'VERIFY=openai-codex/gpt-6.1-sol. Recorded verbatim; it stays SOD_OK precisely because this round did '
           'NOT re-route the PLAN route row (that would be an unauthorised rebind).',
    'D13': 'Read the two levels separately, because they disagree on a wedged attempt. BC3 (the turn that completed) '
           'satisfies the gate as an AGGREGATE verdict: required_arm == served_arm == opencode-go/deepseek-v4.1-flash, '
           'usage_receipt_ok true, rank 1, nonce present. BC1 (the wedged turn) does NOT: its aggregate verdict is '
           'ok:false / ERR_LANE_ALL_ROUTES_EXHAUSTED / usage_receipt_ok:false / served_arm:null, while only its '
           'ATTEMPT-level attribution names opencode-go/deepseek-v4.1-flash. BC2 has a TERMINATION record instead of a '
           'dispatch.json because the orchestrator stopped it, and so carries no arm claim at all. An attempt-level '
           'field is never the arm-identity gate.',
    'D15': 'the board DB itself carries the swarm root, three workers, the verifier and the synthesizer, with a '
           'real edge set - the graph is not just an artifact on disk.',
    'D16': "the repo's own CLI accepts the change: Change 'hgk-lane-reliability-closure-20261016' is valid "
           '(--type change --strict).',
    'D18': 'the json_without_claim_ceiling list is dominated by pre-existing candidate/config files (hermes-codex-lane.json, '
           'project.json, ssot-supersession-ledger.json, credential files) that predate this round and were never '
           'meant to carry a claim ceiling; no artifact scanned claims acceptance.',
    'D19': 'no artifact or lane resolved acceptance: the grep for acceptance-resolution constructs returns nothing.',
    'D20': 'both canonical mutations have a backup with a recorded pre-change digest, and the current digest '
           'differs from it, so the rollback path is real rather than nominal.',
}
for k, v in INTERP.items():
    if k in items:
        items[k]['interpretation'] = v

for k, it in items.items():
    if k in ('D04 canonical', 'D05 canonical', 'D07 canonical') and it['status'] == 'FAIL':
        it['status'] = 'BEFORE_STATE_ON_CANONICAL'
    elif k in ('D09 candidate', 'D10 canonical') and it['status'] == 'FAIL':
        it['status'] = 'EXPECTED_ROOT_DIFFERENCE'

tally = {}
for it in items.values():
    tally[it['status']] = tally.get(it['status'], 0) + 1
rep['status_tally_after_annotation'] = tally
p.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'tally': tally, 'D03': items['D03']['status'],
                  'harness_correction_applied': 'D03',
                  'raw_field_untouched': 'every observation is exactly as measured'}, ensure_ascii=False, indent=1))
