import datetime
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
NONCE = 'R9V-CHECKER-NONCE-5c1d84'
DATA = json.loads((OUT / 'measurements.json').read_text(encoding='utf-8'))
EXTRA = json.loads((OUT / 'supplement.json').read_text(encoding='utf-8'))
HARNESS = json.loads((OUT / 'harness_v2_yourrun.json').read_text(encoding='utf-8'))
REGISTRY = json.loads(DATA['registry']['stdout'])
ROUTES = [route for route in REGISTRY['routes'] if route.get('lane') in ('PLAN', 'VERIFY_SECURITY')]
LIVE = DATA['live']['skill']['path'].rsplit('\\', 1)[0]
CEILING = 'LOCAL / candidate-only; not AO acceptance, not a Gate PASS, not a release decision'

def disagreement(code, evidence, interpretation):
    return dict(code=code, raw_evidence=evidence, interpretation=interpretation)

def evidence(command, raw_output, **extras):
    return dict(command=command, essential_raw_output=raw_output, **extras)

def numbered(rows):
    return '\n'.join(str(row['line']) + ': ' + row['text'] for row in rows)

claims = []
claims.append(dict(
    claim_id='1', verdict='UNVERIFIABLE', requested_status='UNVERIFIABLE',
    conclusion='Both R9 guard blocks occur only in validate.py. The three required mutation refusals were reproduced. CLI smoke passed unchanged. The original legal-link test fixture requires forbidden Git write commands, so an unmodified two-test pass was not established. A separately disclosed filesystem-fixture adaptation ran both original named test methods and both passed; this is supporting evidence, not substitution for the missing original-fixture result.',
    how_you_derived_it=[
        evidence(DATA['git_names']['command'], DATA['git_names']['stdout'], note='HEAD was independently read as dba4b19456777d3b597fdf71480f6423dd974243. Other modified files exist; only the two R9 guard locations are claimed to be confined to validate.py.'),
        evidence(DATA['guard_search']['command'], DATA['guard_search']['stdout']),
        evidence('Read src/pipd_ls_sp/validate.py with 1-based line numbers; full git diff retained in git_diff.json', numbered(DATA['guard_lines'])),
        evidence(EXTRA['named_tests_confined']['command'], EXTRA['named_tests_confined']['stderr'], exit=EXTRA['named_tests_confined']['exit']),
        evidence(EXTRA['adapted_fixture_tests']['command'], EXTRA['adapted_fixture_tests']['stderr'], exit=EXTRA['adapted_fixture_tests']['exit'], fixture_change='Only module._init_git_repo is replaced in memory by mkdir + README seed; the two named methods and their assertions remain unchanged. The repository probe then takes its disclosed filesystem-degraded path. No git init/add/commit command executes.'),
        evidence(DATA['mutations']['command'], DATA['mutations']['stdout'], exit=DATA['mutations']['exit'], runner_change='Import the original runner without editing it; redirect only module.SRC to R9_VERIFY/probe_source.md. Run m04_profile_downgrade, m06_domain_oracle_expected and m16_trace_digest_mismatch. raw_receipt values printed by the runner are labels, not files written by this check; mutation_probes.json is the actual raw output.')
    ],
    disagreement=[
        disagreement('ORIGINAL_TEST_FIXTURE_REQUIRES_FORBIDDEN_GIT_WRITE', "RuntimeError: R9V_FORBIDDEN_GIT_WRITE: ['git', '-C', '.../R9_VERIFY/tmp/tmpso_m_3qp/repo', 'init', '-q']; Ran 1 test; FAILED (errors=1). Adapted fixture: Ran 2 tests; OK.", 'Do not report an unmodified two-test PASS. This is a verifier constraint, not a demonstrated validator regression.'),
        disagreement('BASELINE_DIFF_NOT_SINGLE_FILE', DATA['git_names']['stdout'], 'The base-to-current delta includes cli.py and pipeline.py as well as validate.py. The two specific R9 guards are in validate.py, but the whole worktree is not a one-file patch.')
    ]))

claims.append(dict(
    claim_id='2', verdict='CONFIRMED', requested_status='PASS',
    conclusion='The requested harness process exited 0; all six checks report PASS against the explicitly passed HGK live tree. This is the harness result only. The subject_live metadata is wrong because it is captured before check() updates the global LIVE.',
    how_you_derived_it=[
        evidence(DATA['harness']['command'], HARNESS, exit=DATA['harness']['exit']),
        evidence('Read ws_a_skill_slim_regression.py lines 64-66 and 217-219', '64: global LIVE\n66: LIVE = Path(live)\n217: "subject_candidate": str(root), "subject_live": str(LIVE),\n219: "checks": check(root, a.live)')
    ],
    disagreement=[
        disagreement('HARNESS_SUBJECT_LIVE_SERIALIZATION_DEFECT', dict(passed_live=LIVE, recorded_subject_live=HARNESS['subject_live']), 'A harness metadata defect, not evidence that the checks used AVR. Dict values are evaluated in insertion order; check(root, a.live) subsequently sets LIVE and uses the supplied HGK tree. Treating the recorded field as the effective comparison tree would also be a reading error.'),
        disagreement('STALE_C6_DENOMINATOR', dict(recorded_claim='ClaimLedger.tsv CL-06: 113 live references accounted and none lost', measured=HARNESS['checks']['C6_reference_coverage']), 'The current result is 117 live non-pycache files, 103 identical, 14 absorbed verbatim, 0 lost. The live tree has changed; the historical 113 is not the current denominator.'),
        disagreement('HARNESS_CAP_NOT_PKG_AUTHORITY', 'ws_a_skill_slim_regression.py:33 MAIN_CAP_BYTES = 100_000; PKG literal matches for 100000, 100,000, 100_000 = 0', 'C1 measures a harness-defined cap. Its PASS cannot establish that the PKG imposes that cap.')
    ]))

apply = EXTRA['apply_receipt_comparison']
claims.append(dict(
    claim_id='3', verdict='CONFIRMED', requested_status='PASS',
    conclusion='The LIVE tree contains the applied slim main file and restored reference. All 111 candidate files have byte-identical counterparts in LIVE; LIVE intentionally contains additional retained files. Historical agency is not inferred from hashes alone; the independently read preimage and per-path receipt comparison corroborate the applied state. There is no WS_B2 directory; the accessible JSON apply receipt is in WS_B.',
    how_you_derived_it=[
        evidence('python -B collect.py: Path.read_bytes/stat, hashlib.sha256 and references.rglob; python -B supplement.py: compare every candidate file and every apply-receipt path', dict(live=DATA['live'], reference_counts=EXTRA['reference_counts'], candidate_file_count=EXTRA['candidate_file_count'], candidate_files_different_or_missing_in_live=EXTRA['tree_comparison'], preimage=EXTRA['preimage'], apply_receipt_comparison=apply))
    ],
    disagreement=[
        disagreement('APPLY_RECEIPT_LOCATION_MISMATCH', dict(ws_b2_exists=False, observed_receipt=apply['path'], applied=apply['applied']), 'No WS_B2 apply receipt can be compared because WS_B2 is absent. The WS_B JSON receipt is checked against live bytes instead; no *_RECEIPT.md was opened.'),
        disagreement('APPLY_RECEIPT_TOTAL_STALE', dict(recorded_dst_files_total=apply['recorded_dst_files_total'], measured_dst_files_total=apply['actual_dst_files_total'], per_path_digest_mismatches=[row for row in apply['rows'] if row['match'] is False]), 'The receipt total is 127, the current tree total is 131; all 35 recorded after-digests still match. This count difference alone does not disprove the historical apply.'),
        disagreement('REFERENCE_COUNT_DEFINITION', EXTRA['reference_counts'], 'The requested all-files count is 123. The harness excludes 6 pycache files and counts 117. Markdown-only references number 110. These denominators must not be conflated.')
    ]))

claims.append(dict(
    claim_id='4', verdict='CONFIRMED', requested_status='PASS',
    conclusion='PKG sha256 equals the approved owner digest. Its own bytes contain no literal 100000/100,000/100_000 cap and associate ACC-RQ06 with AVR/10-piece and HGK/6-piece byte reconstruction. This confirms the requested correction, not the harness hard-cap authority.',
    how_you_derived_it=[evidence('python -B collect.py: hash PKG.read_bytes(); regex r"100[,_]?000" over all lines; read ACC-RQ06 contexts; supplement.py expanded contexts', dict(path=DATA['pkg']['path'], bytes=DATA['pkg']['bytes'], sha256=DATA['pkg']['sha256'], approved_matches=DATA['pkg']['approved_matches'], size_literal_matches=DATA['pkg']['size_literals'], quotes=numbered(EXTRA['rq06_quote'])))],
    disagreement=[disagreement('PKG_RECORDED_BYTE_COUNT_WRONG', dict(recorded='SourceSnapshotLedger.tsv SRC-01 byte_count=2580690; ResearchSourceDenominator.tsv SRC-01 reason includes 2580690 bytes', measured_bytes=DATA['pkg']['bytes'], measured_sha256=DATA['pkg']['sha256']), 'The observed file is 2,689,181 bytes, not 2,580,690. The approved digest nonetheless matches exactly. No package modification is inferred.')]))

claims.append(dict(
    claim_id='5', verdict='CONFIRMED', requested_status='PASS',
    conclusion='The canonical repo drift check returns []. Both current top-level PLAN and VERIFY_SECURITY select openai-codex/gpt-6.1-sol, medium reasoning, OpenAI OAuth, in agreement with the 2026-10-16 mandate. Drift cleanliness is projection conformance, not execution attestation. VERIFY_SECURITY admission_status remains UNPROVEN; that separate status is not upgraded here.',
    how_you_derived_it=[evidence(DATA['registry']['command'], dict(registry_path=REGISTRY['registry_path'], drift=REGISTRY['drift'], routes=ROUTES), cwd=DATA['registry']['cwd'], environment={'PYTHONPATH':'src','PYTHONDONTWRITEBYTECODE':'1'}, exit=DATA['registry']['exit'])],
    disagreement=[disagreement('STALE_FAR_PLAN_ROUTE_CLAIM', dict(recorded_claim='ClaimLedger.tsv CL-05: routes[].PLAN (opencode-go/glm-5.3-flash) disagrees with the pool and the 2026-10-16 mandate', current_top_level_routes=[{key:route.get(key) for key in ('lane','provider','model','reasoning_effort','auth','oauth','admission_status')} for route in ROUTES], drift=REGISTRY['drift']), 'The measured current PLAN route is corrected and agrees with the mandate. CL-05 is stale for the live tree; do not repeat it as a current result.')]))

source13 = next(row for row in EXTRA['source_locator_checks'] if row['source_id'] == 'SRC-13')
claims.append(dict(
    claim_id='6', verdict='UNVERIFIABLE', requested_status='UNVERIFIABLE',
    conclusion='The requested Fabric/FABRIC/.../runs path does not exist. A matching run exists under Fabric/fabric-autonomous-research/runs and contains 21 files, inventoried by name and size only. ClaimLedger.tsv has no evidence_ref field. All 11 support-source usages resolve to source records in ResearchSourceDenominator.tsv, but this does not prove the missing evidence_ref relation. One upstream locator contains a literal ellipsis and one prior-run shorthand has the wrong date. No vacuous evidence-ref PASS is issued.',
    how_you_derived_it=[evidence('python -B collect.py: requested_path.exists(); find matching run; stat inventory only; csv.DictReader on ClaimLedger.tsv and source ledgers. python -B supplement.py: exists()/glob on source locators, without opening reports or syntheses', dict(requested_path=DATA['far']['requested_path'], requested_exists=DATA['far']['requested_exists'], discovered_path=DATA['far']['discovered_path'], inventory=DATA['far']['inventory'], claim_ledger_headers=DATA['far']['claims']['headers'], evidence_ref_fields=DATA['far']['evidence_ref_fields'], source_id_resolution=DATA['far']['source_id_resolution'], source_locator_checks=EXTRA['source_locator_checks']))],
    disagreement=[
        disagreement('FAR_REQUESTED_PATH_ABSENT', dict(requested=DATA['far']['requested_path'], exists=False, discovered=DATA['far']['discovered_path'], artifacts=len(DATA['far']['inventory'])), 'The physical run is outside the requested FABRIC subdirectory. The discovered directory was not silently substituted.'),
        disagreement('FAR_EVIDENCE_REF_COLUMN_ABSENT', DATA['far']['claims']['headers'], 'No evidence_ref column or named evidence_ref values exist in ClaimLedger.tsv. Source-ID linkage was separately checked, not conflated with the requested relation.'),
        disagreement('UNADDRESSABLE_UPSTREAM_LOCATOR', source13, 'SRC-13 is a present source record, but _handover/...-R8/ws_a_skill_slim_regression.py is not an addressable file. The actual harness is known from the user brief, not from that locator. There are no dangling support_source_ids; this is a dangling/ambiguous external locator.'),
        disagreement('FAR_PRIOR_RUN_DATE_SHORTHAND_WRONG', dict(recorded='SRC-11: Fabric/fabric-autonomous-research/runs/FAR-20261015-010,-011', measured_010='FAR-20261015-010-r6r7-closure-and-r7-slice', measured_011='FAR-20261016-011-r5r3-preview4-live-subject', match_for_20261015_011=False), 'The -011 run is dated October 16, 2026, not October 15. The shorthand does not directly resolve both runs.')
    ]))

claims.append(dict(
    claim_id='7', verdict='UNVERIFIABLE', requested_status='UNVERIFIABLE',
    conclusion='All 14 historical attempt-log rows identify serving arms: EXECUTE used rank 1 opencode-go/deepseek-v4.1-flash; VERIFY_SECURITY used rank 2 opencode-go/glm-5.3-flash. Those rows agree with the old dispatcher pin, not the R9 checker pin. None proves a silent fallback from a rank-1 checker pin on the same turn. The current R9 checker has only an open attempt marker, no finalized serving receipt; it cannot be attributed to the pinned OpenAI arm from these artifacts yet. The root final receipt names are reused across runs and are not a complete per-run history.',
    how_you_derived_it=[
        evidence('python -B supplement.py: parse lane_runs/*dispatch_receipt*.json and *.attempts.ndjson; correlate code only by exact stdout_path; read R9 attempt.marker.json and old/current dispatcher pin lines', dict(current_receipts=EXTRA['receipt_summary'], historical_attempts=EXTRA['attempt_history'], dispatch_pin_lines=EXTRA['dispatch_pin_lines'], r9_open_attempts=EXTRA['r9_markers']))
    ],
    disagreement=[
        disagreement('HISTORICAL_CHECKER_ARM_DIFFERS_FROM_R9_PIN', dict(served_historical_checker={'rank':2,'provider':'opencode-go','model':'glm-5.3-flash'}, old_dispatcher_pin={'rank':2,'arm':'opencode-go/glm-5.3-flash'}, r9_dispatcher_pin={'rank':1,'arm':'openai-codex/gpt-6.1-sol'}), 'Historical turns served the arm the old dispatcher explicitly pinned. They were not evidence of a runtime fallback or of current R9 arm nonconformance.'),
        disagreement('R9_FINAL_SERVING_RECEIPT_NOT_YET_PRESENT', EXTRA['r9_markers'], 'The open R9 marker contains no served rank/provider/model, exit, seconds, nonce_present or final code. A marker and dispatcher configuration do not prove which arm served this ongoing checker.'),
        disagreement('HISTORICAL_FINAL_RECEIPTS_OVERWRITTEN', dict(history_rows=len(EXTRA['attempt_history']), root_receipt_files=len(EXTRA['receipt_summary']), rows_without_correlated_final_code=sum(row['code'] is None for row in EXTRA['attempt_history'])), 'Some historical ndjson rows have no code field and their original final receipt is no longer available. code=null is reported rather than copying a later turn code.'),
        disagreement('NO_COMPLETED_NONCE_ACCEPTED_RECEIPT', dict(nonce_present_values=sorted(set(row['nonce_present'] for row in EXTRA['attempt_history'])), final_receipt_codes=[row['code'] for row in EXTRA['receipt_summary']]), 'All historical nonce_present values are false. VERIFY attempt5 was refused before serving, with ERR_LANE_REMOTE_WRITE_NOT_AUTHORIZED. Exit 0 for other attempts does not mean dispatch acceptance.')
    ]))

report = dict(schema='R9-INDEPENDENT-VERDICT/1', mission='CNV-PIPD-LS-SP-20261015', changeset='R9-0-FAR-RESIDUAL-CLOSURE', nonce=NONCE, generated_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), claims=claims, overall='UNVERIFIABLE', overall_reason='Claims 1, 6 and the current-turn part of 7 cannot be fully re-derived. Confirmed local measurements must not be promoted to acceptance. Separately, the first test invocation breached the temporary write boundary, so this checker run is procedurally nonconformant.', claim_ceiling=CEILING, procedural_compliance=dict(verdict='REFUTED', incident=EXTRA['boundary_incident'], no_git_write_command_executed=True, no_network_used=True, forbidden_report_contents_used_as_evidence=False, scope_note='No forbidden report/synthesis or *_RECEIPT.md was used to derive verdicts. The FAR ResearchSynthesis.md was inventoried by stat only; no content read. Existing report paths used as source locators were checked for existence only. JSON dispatch/apply receipts were examined as explicitly requested.'), raw_artifacts=['measurements.json','supplement.json','git_names.json','git_diff.json','guard_search.json','named_tests.json','named_tests_confined.json','adapted_fixture_tests.json','mutation_probes.json','harness_run.json','harness_v2_yourrun.json','registry_drift.json'])
(OUT / 'R9_VERDICT.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

markdown = [NONCE, '# R9 independent local verdict', '', '**Overall: UNVERIFIABLE.** ' + CEILING + '.', '', report['overall_reason'], '', '## Procedural incident', '', EXTRA['boundary_incident']['explanation'], '', 'Raw: `named_tests.json` records `C:/Users/user/AppData/Local/Temp/tmp3eedulc6/repo` before the git-init call was blocked. That temporary root no longer exists on readback. The first CLI smoke invocation also used the default TEMP. The confined rerun uses only `R9_VERIFY/tmp`. This is disclosed as `CHECKER_TEMP_WRITE_BOUNDARY_BREACH`, not excused as compliance.', '', '## Verdict summary', '', '| Claim | Verdict | Requested status |', '|---|---|---|']
for claim in claims:
    markdown.append('| ' + claim['claim_id'] + ' | ' + claim['verdict'] + ' | ' + claim['requested_status'] + ' |')
for claim in claims:
    markdown.extend(['', '## Claim ' + claim['claim_id'] + ' — ' + claim['verdict'], '', claim['conclusion'], '', '### Derivation and raw evidence'])
    for item in claim['how_you_derived_it']:
        command = item['command']
        markdown.extend(['', '**Command / method:**', '', '```text', json.dumps(command, ensure_ascii=False) if isinstance(command,list) else command, '```', '', '**Essential raw output:**', '', '```text', item['essential_raw_output'] if isinstance(item['essential_raw_output'],str) else json.dumps(item['essential_raw_output'], ensure_ascii=False, indent=2), '```'])
        for key,value in item.items():
            if key not in ('command','essential_raw_output'):
                markdown.append('- ' + key + ': ' + (value if isinstance(value,str) else json.dumps(value, ensure_ascii=False)))
    markdown.extend(['', '### Disagreements / limitations'])
    for item in claim['disagreement']:
        markdown.extend(['', '**' + item['code'] + '** — ' + item['interpretation'], '', '```text', item['raw_evidence'] if isinstance(item['raw_evidence'],str) else json.dumps(item['raw_evidence'], ensure_ascii=False, indent=2), '```'])
markdown.extend(['', '## Attribution table — current root final receipts', '', '| Receipt | Rank | Provider | Model | Exit | Seconds | nonce_present | Code |', '|---|---:|---|---|---|---:|---|---|'])
for item in EXTRA['receipt_summary']:
    name = Path(item['path']).name
    for attempt in item['attempts'] or [dict()]:
        markdown.append('| ' + name + ' | ' + ' | '.join(str(attempt.get(key,'N/A')) for key in ('rank','provider','model','exit','seconds','nonce_present')) + ' | ' + str(item['code']) + ' |')
markdown.extend(['', '## Attribution table — complete append-only attempt history', '', 'A null final code means no same-turn final receipt is available; no code is inferred from a newer receipt.', '', '| Run ID | Lane | Rank | Provider | Model | Exit | Seconds | nonce_present | Same-turn final code |', '|---|---|---:|---|---|---|---:|---|---|'])
for row in EXTRA['attempt_history']:
    markdown.append('| ' + ' | '.join(str(row.get(key)) for key in ('run_id','lane','rank','provider','model','exit','seconds','nonce_present','code')) + ' |')
markdown.extend(['', '## Limits', '', 'No AO acceptance, Gate PASS, release approval, or current serving-arm proof is issued. Original-fixture legal-link test execution remains blocked by the no-Git-write rule; the adapted-fixture pass is explicitly separate. FAR missing evidence_ref fields are not treated as a vacuous pass. Candidate post-apply coverage does not by itself prove losslessness against the pre-apply corpus. No files outside R9_VERIFY were intentionally edited; the automatic temporary-write incident above is an exception and prevents a procedural-compliance claim.', '', NONCE])
(OUT / 'R9_VERDICT.md').write_text('\n'.join(markdown) + '\n', encoding='utf-8')
(OUT / 'R9V_DONE').write_text(NONCE, encoding='utf-8')
print(json.dumps({'claims':[{key:claim[key] for key in ('claim_id','verdict','requested_status')} for claim in claims], 'overall':report['overall'], 'procedural_compliance':report['procedural_compliance']['verdict'], 'outputs':['R9_VERDICT.json','R9_VERDICT.md','R9V_DONE']}, indent=2))
