"""Owner-authorized FDA source-document preflight, not product execution.
Writes only new noncanonical evidence below this script's directory.
No credentials, external requests, canonical store writes or model dispatch.
"""
from pathlib import Path
import copy
import datetime
import hashlib
import json
import os
import re
import subprocess

ROOT = Path(__file__).resolve().parent
PYTHON = Path('C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe')
COMPILER = Path('C:/Projects/Agent_Workspace/知識庫/實作相關DOC/HG-KSEOS/construction-acceptance-prompt-compiler/construction-acceptance-prompt-compiler')

def digest(b):
    return hashlib.sha256(b).hexdigest()

def output(name, value):
    target = ROOT / name
    if not target.resolve().is_relative_to(ROOT.resolve()):
        raise RuntimeError('OUTPUT_SCOPE_ESCAPE')
    target.parent.mkdir(parents=True, exist_ok=True)
    data = value if isinstance(value, bytes) else (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    with target.open('xb') as stream:
        stream.write(data)
    if target.read_bytes() != data:
        raise RuntimeError('OUTPUT_READBACK_MISMATCH')
    return {'path': str(target), 'bytes': len(data), 'sha256': digest(data)}

def run_case(name, command):
    env = os.environ.copy()
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    result = subprocess.run(command, capture_output=True, timeout=90, env=env)
    stdout = output(name + '.stdout.txt', result.stdout)
    stderr = output(name + '.stderr.txt', result.stderr)
    receipt = {'kind': 'LOCAL_PREFLIGHT_EXECUTION_NOT_ACCEPTANCE', 'observed_at': started,
               'command': command, 'exit_code': result.returncode, 'stdout': stdout, 'stderr': stderr}
    output(name + '.receipt.json', receipt)
    return receipt

lock = json.loads((ROOT / 'OWNER_TRUST_LOCK.json').read_text(encoding='utf-8'))
assert (ROOT / 'FDA_SCOPE_AUTHORIZATION.json').is_file()
pkg = Path(lock['package']['path'])
raw = pkg.read_bytes()
assert digest(raw) == lock['package']['sha256']
verifier = ROOT / 'pipd_pkg_v2_check.py'
assert digest(verifier.read_bytes()) == lock['verifier']['sha256']
text = raw.decode('utf-8', 'strict')
slots = {m.group(1): json.loads(m.group(2)) for m in list(re.finditer(r'(?ms)^```json SLOT:([^\n]+)\n(.*?)^```', text))[:27]}
records = slots['02_SOURCE_BINDINGS.json']['physical_sources']
discovery = json.loads((ROOT / 'PHYSICAL_SOURCE_DISCOVERY_EXPANDED.json').read_text(encoding='utf-8'))
lookup = {r['expected']['filename']: r['matching_physical_paths'] for r in discovery['rows']}
cut = b'\n<!-- V1_WHOLE_DOCUMENT_BYTES_BEGIN sha256='
assert raw.count(cut) == 1
_, legacy = raw.split(cut, 1)
end_header = legacy.index(b' -->\n')
legacy_digest = legacy[:end_header].decode('ascii')
legacy = legacy[end_header + 5:]
end = b'\n<!-- V1_WHOLE_DOCUMENT_BYTES_END -->\n'
assert legacy.endswith(end)
legacy = legacy[:-len(end)]
assert digest(legacy) == legacy_digest
source_rows = []
missing = []
for r in records:
    paths = lookup[r['filename']]
    if paths:
        data = Path(paths[0]).read_bytes()
        origin = paths[0]
        kind = 'EXISTING_PHYSICAL_SOURCE_BYTE_COPY'
    elif r['sha256'] == legacy_digest:
        data = legacy
        origin = str(pkg) + '#V1_WHOLE_DOCUMENT_BYTES_BEGIN'
        kind = 'EXACT_BYTES_RECOVERED_FROM_OWNER_PINNED_APPENDIX_NOT_INDEPENDENT_ORIGINAL'
    else:
        missing.append(r)
        continue
    assert len(data) == r['bytes'] and digest(data) == r['sha256']
    artifact = output('physical_source_readback/' + r['filename'], data)
    source_rows.append(dict(artifact, origin=origin, origin_kind=kind))
output('PHYSICAL_SOURCE_READBACK_MANIFEST.json', {
    'claim': 'byte copies plus explicit exact-byte appendix recovery; not canonical source freeze',
    'expected': len(records), 'materialized': len(source_rows), 'rows': source_rows, 'missing': missing})
package_receipt = run_case('PACKAGE_CHECK_FLAT', [str(PYTHON), '-B', str(verifier), '--doc', str(pkg),
    '--check', '--source-root', str(ROOT / 'physical_source_readback'),
    '--trusted-package-sha256', lock['package']['sha256']])
plan = json.loads((ROOT / 'MISSION_PLAN_SPEC_CHECKLIST.json').read_text(encoding='utf-8'))
prompt_path = Path(plan['source_locator'])
contract = json.loads((COMPILER / 'tests/fixtures/baseline.json').read_text(encoding='utf-8'))
contract['task_id'] = plan['mission_id']
source_defs = [
    ('owner', 'SRC-OWNER', ROOT / 'OWNER_TRUST_LOCK.json', 'NORMATIVE', 'A0'),
    ('prompt', 'SRC-PROMPT', prompt_path, 'NORMATIVE', 'A4'),
    ('package', 'SRC-PKG', pkg, 'NORMATIVE', 'A3'),
    ('HGK', 'SRC-HGK', Path('C:/Projects/Agent_Workspace/HG-KSEOS/AGENTS.md'), 'NORMATIVE', 'A1'),
    ('Fabric', 'SRC-FABRIC', Path('C:/Projects/Agent_Workspace/Fabric/AGENTS.md'), 'SUPPORT', 'A6'),
    ('compiler', 'SRC-COMPILER', COMPILER / 'construction-acceptance-prompt-compiler_SKILL.md', 'NORMATIVE', 'A5')]
for authority in discovery['recovered_authority_files']:
    source_defs.append((authority['id'], 'SRC-' + authority['id'], Path(authority['path']), 'NORMATIVE', 'A2-' + authority['id']))
reviewed = []
authority_sources = []
for family, sid, path, role, rank in source_defs:
    sha = digest(path.read_bytes())
    reviewed.append({'source_family': family, 'source_id': sid, 'locator': str(path), 'sha256': sha, 'role': role, 'critical': True})
    authority_sources.append({'id': sid, 'rank': rank, 'path': str(path), 'sha256': sha, 'locator': str(path), 'role': role, 'governs': role == 'NORMATIVE'})
required = [r['source_family'] for r in reviewed]
missing_sources = []
for i, r in enumerate(records, 1):
    family = 'physical-' + str(i).zfill(2)
    required.append(family)
    if r in missing:
        missing_sources.append(family + ':' + r['filename'])
    else:
        reviewed.append({'source_family': family, 'source_id': 'SRC-' + family,
            'locator': str(ROOT / 'physical_source_readback' / r['filename']), 'sha256': r['sha256'],
            'role': 'STATE_EVIDENCE', 'critical': True})
for family in ['knowledge-00-19-review', 'eight-plugin-typed-bundle-review', 'current-Fabric-policy-consumption-review']:
    required.append(family)
    missing_sources.append(family + ':NOT_YET_REVIEWED')
contract['source_scan'] = {'required_source_families': required, 'reviewed': reviewed,
    'missing': missing_sources, 'normative_claims': [{'claim_id': 'MO-CNV-001', 'text': plan['core_goal'],
        'source_ids': ['SRC-PROMPT', 'SRC-PKG', 'SRC-HGK'], 'locators': [str(prompt_path) + ':1,2,6', str(pkg) + ':Slot22']}]}
contract['intent'] = {
    'goal': plan['core_goal'],
    'user_expected_outcome': 'Same-subject actual evidence for all 221 distinct planning cases, 18 hostile cases, 24 AUD findings and eight gates; only an approved nonsecret Draft PR.',
    'user_expected_experience': 'HGK routes goal/source_paths/target_root through Hermes and existing bounded Codex lanes, without silent fallback or invented completion.',
    'explicit_constraints': ['HG-KSEOS sole normative control plane', 'PLAN Hermes openai-codex/gpt-6.1-sol medium; EXECUTE Codex opencode-go/deepseek-v4.1-flash; VERIFY_SECURITY Codex opencode-go/glm-5.3-flash', 'required_arm equals served_arm', 'No product mutation before source/compiler/admission gates', 'Compiler/runtime/admission/acceptance/publication remain separate'],
    'non_goals': ['second governor or task database', 'Stage-3 or SQP1', 'production/live/trade', 'secret export', 'direct main push or force push'],
    'authorized_mutations': ['noncanonical preflight and compiler evidence under ' + str(ROOT), 'product writes conditional on compiled contract and typed admission', 'Draft PR conditional on approved exact paths and publication gate'],
    'forbidden_mutations': ['source corpus', 'unadmitted product/canonical writes', 'raw SQL state mutation', 'secret export', 'unapproved external publication'],
    'expected_autonomy': 'HIGH', 'allowed_hitl': ['source trust', 'oracle conflict', 'Fresh G1', 'effect expansion', 'technology admission', 'exact publication set', 'AO/release'],
    'requested_delivery': ['SUBJECT_AND_SOURCE.json', 'AUTHORITY_LOCK_STATUS.json', 'COMPILER_RECEIPTS/', 'REQ_TRACE_221.json', 'AUDIT_24_CLOSURE.json', 'K_LEDGER_CROSSWALK.json', 'RUNNER_AND_TEST_MATRIX.json', 'MUTATIONS_18.json', 'EFFECTS_5.json', 'GATES_A_TO_H.json', 'MAKER_CHECKER_SEPARATION.json', 'TT_CR_REGISTER.json', 'CHECKPOINT_AND_ROLLBACK.json', 'PUBLICATION_RECEIPT.json', 'EXTERNAL_ACCEPTANCE_HANDOFF.md', 'NON_CLAIMS.md'],
    'active_requirement_ids': [r['id'] for r in slots['22_FULL_221_TEST_CONTRACTS.json']] + [r['id'] for r in plan['task_specs']], 'claim_ceiling': 'LOCAL'}
contract['authority'] = {'sources': authority_sources, 'conflicts': [{'conflict_id': 'TT-PIPD-03', 'sources': ['SRC-PKG'], 'equal_rank': False, 'decision': 'OPEN', 'tt_id': 'TT-PIPD-03'}], 'missing_sources': missing_sources, 'native_control_plane_ids': ['HG-KSEOS'], 'current_control_plane_id': 'HG-KSEOS'}
contract['changeset'] = {'class': 'CONTINUATION', 'baseline_required': True, 'baseline_verified': False, 'reuse_prior_pass': False, 'affected_domains': ['Fabric-HGK-PIPD admitted affected edges'], 'affected_files': [str(ROOT)], 'must_not_reopen': ['sealed RP002 Stage-2', 'Stage-3/SQP1', 'unrelated dirty changes', 'source corpus', 'global model settings'], 'scope_expansion_requires_hitl': True, 'tracked_mutation': False, 'product_mutation_allowed': False}
caps = ['native-prompt-compiler', 'approved-document-verifier', 'HGK-typed-spine-and-lifecycle', 'Hermes-canonical-runtime', 'Codex-EXECUTE-DeepSeek', 'Codex-VERIFY-GLM', 'Hermes-Kanban', 'Hermes-Swarm', 'gstack-advisory', 'OpenSpec-brownfield', 'AVR-HGK-Skill-loader', 'FAR-SQLite-FTS5', 'bounded-FS-API-Desktop', 'approval-gated-GitHub'] + [r['skill'] for r in slots['23_PLUGIN_TYPED_HANDOFF_8.json']]
contract['execution_scope'] = []
contract['runtime_readiness'] = []
contract['acceptance'] = []
stages = ['identify', 'pin', 'install_materialize', 'configure', 'discover', 'bind', 'route', 'effective_load', 'doctor_health', 'positive_pilot', 'negative_security', 'fallback', 'rollback_uninstall', 'independent_qualification', 'certify', 'enable']

def acceptance(subject, kind, positive, negative, recovery, locator):
    contract['acceptance'].append({'acceptance_id': 'ACC-' + subject, 'subject_id': subject, 'subject_type': kind,
        'source_locators': [locator], 'runtime_required': True, 'required_depth': 'L4_FAILURE_RECOVERY',
        'positive_fixture': str(positive), 'negative_fixture': str(negative), 'recovery_fixture': str(recovery),
        'raw_evidence_required': True, 'independent_checker_required': True,
        'terminal_states': ['INDEPENDENT_CASE_PASS', 'INDEPENDENT_CASE_FAIL', 'BLOCKED_HITL', 'BLOCKED_EXTERNAL']})

for cap in caps:
    locator = str(prompt_path) + ':4,6'
    contract['execution_scope'].append({'capability': cap, 'source_disposition': 'REQUIRED_BY_MISSION', 'current_execution_disposition': 'ACTIVE_REQUIRED', 'current_profile_selected': True, 'canonical_flow_referenced': True, 'automatic_route_target': False, 'user_experience_required': True, 'runtime_required_now': True, 'action': 'QUALIFY', 'source_locators': [locator], 'external_method': cap in ['gstack-advisory', 'OpenSpec-brownfield'], 'control_authority': cap == 'HGK-typed-spine-and-lifecycle'})
    contract['runtime_readiness'].append({'capability': cap, 'required_now': True, 'lifecycle': {k: 'OPEN' for k in stages}, 'current_verdict': 'NOT_READY', 'work_required': ['Complete source/compiler gates', 'Reuse actual bound entrypoint for ' + cap, 'Run same-subject positive/negative/fallback/rollback and independent qualification after typed admission'], 'acceptance_ids': ['ACC-' + cap]})
    acceptance(cap, 'CAPABILITY', 'Actual bound ' + cap + ' entrypoint with raw result', 'Wrong/missing scope, stale binding, injection or unavailable route must fail closed', 'Rollback/residue readback and independent recheck', locator)
for row in slots['22_FULL_221_TEST_CONTRACTS.json']:
    acceptance(row['id'], 'REQUIREMENT', json.dumps(row['expected'], ensure_ascii=False), json.dumps(row['negative'], ensure_ascii=False), 'Actual first-fail ' + str(row['failure']) + '; bounded fixture/effect restoration', str(pkg) + ':Slot22/' + row['id'])
for row in plan['task_specs']:
    acceptance(row['id'], 'REQUIREMENT', row['minimum_deliverable'], 'Reject missing/stale/foreign/self-attested evidence', 'Smallest admitted affected repair; no scope expansion', str(prompt_path) + ':' + row['id'])
for name in contract['intent']['requested_delivery']:
    acceptance(name, 'DELIVERABLE', 'Exact current-subject artifact with authentic raw backing', 'Reject missing evidence, false PASS, secret content or stale binding', 'Keep failed generation; repair only affected evidence', str(prompt_path) + ':8,9')
contract['journeys'] = [{'journey_id': 'CNV-USER-JOURNEY', 'required': True, 'user_goal': 'Governed convergence from goal/source_paths/target_root', 'expected_visible_result': 'Actual evidence, open blockers and only authorized candidate Draft PR', 'expected_automatic_behavior': ['deterministic HGK route', 'reuse existing lanes', 'carry every obligation'], 'expected_manual_behavior': ['Owner acts only at actual authority boundaries'], 'allowed_hitl': contract['intent']['allowed_hitl'], 'required_capabilities': caps, 'negative_behavior': ['no false receipt', 'no Maker acceptance', 'no unapproved push'], 'failure_recovery': ['affected-only fresh recheck', 'preserve raw failures and admitted checkpoint'], 'source_expectation_ids': ['MO-CNV-001'], 'source_locators': [str(prompt_path) + ':3,7,9']}]
acceptance('CNV-USER-JOURNEY', 'JOURNEY', 'Actual user-visible governed result', 'Reject unadmitted dispatch or unsupported completion', 'Checkpoint and currentness-checked affected-only resume', str(prompt_path) + ':3,7,9')
contract['evidence'] = []
for gate in slots['14_GATES_8.json']:
    contract['evidence'].append({'gate_id': gate['id'], 'predicate': 'Current Slot14 registered oracle, positive/negative/recovery and independent same-subject raw evidence', 'expected': 'INDEPENDENT_CASE_PASS', 'command_or_probe': 'UNBOUND; discover actual runner after source/compiler/admission prerequisites', 'raw_receipt_required': True, 'producer': 'Codex CLI opencode-go/deepseek-v4.1-flash; Hermes preflight separately attributed', 'independent_checker': 'fresh read-only Codex CLI opencode-go/glm-5.3-flash and canonical AO', 'candidate_binding': {'head': 'NOT_CREATED', 'package_sha256': lock['package']['sha256'], 'source_hashes': [r['sha256'] for r in reviewed]}, 'tracked_subject': False, 'rerun_rule': 'affected-only', 'invalidation': ['source digest', 'candidate HEAD/tree', 'scope/token', 'runtime version', 'served arm', 'oracle'], 'terminal_verdict': 'BLOCKED_EXTERNAL', 'runtime_pass_allowed': False, 'claim_level': 'LOCAL'})
contract['termination'] = {'terminal_states': ['CANDIDATE_READY_FOR_INDEPENDENT_REVIEW', 'INDEPENDENTLY_ACCEPTED', 'TEMP_CLOSED', 'FAIL'], 'non_terminal_pause': ['ITERATION_BUDGET_PAUSE', 'SESSION_BOUNDARY', 'HITL_AUTHORITY_EDGE'], 'checkpoint_required': True, 'checkpoint_fields': ['task_id', 'source_hashes', 'current_candidate', 'completed_gates', 'open_gates', 'next_work_order', 'rollback_pointer', 'typed_admission_ids', 'open_tt_cr', 'raw_evidence_refs', 'resume_condition'], 'retry_budget': 0, 'rollback_pointer_required': True}
contract['render_policy'] = {'control_corpus_restatement': False, 'embedded_control_bodies': [], 'max_prompt_chars': 30000, 'output_language': 'zh-TW'}
output('C0_C9_CONTRACT.json', contract)
compiler_script = COMPILER / 'scripts/prompt_contract_compiler.py'
assert digest(compiler_script.read_bytes()) == '2c282ad6539a465c3b1d751868cab98437a8f35e9728be686117e364a70857d9'
compiler_results = []
for stage in ['lint', 'activation', 'acceptance', 'compile']:
    command = [str(PYTHON), '-B', str(compiler_script), stage, str(ROOT / 'C0_C9_CONTRACT.json')]
    if stage == 'compile':
        command += ['--out-dir', str(ROOT / 'compiler_native_output')]
    compiler_results.append(run_case('COMPILER_' + stage, command))
summary = {'kind': 'NONCANONICAL_PREFLIGHT_SUMMARY', 'mission_id': plan['mission_id'],
    'physical_sources': {'expected': len(records), 'materialized': len(source_rows), 'missing': len(missing)},
    'package_check_exit': package_receipt['exit_code'],
    'compiler_exits': {r['command'][3]: r['exit_code'] for r in compiler_results},
    'contract_acceptance_edges': len(contract['acceptance']), 'active_capabilities': len(caps),
    'canonical_mutation': False, 'product_writes': False, 'model_dispatches': 0, 'credential_access': False,
    'publication': 'NOT_RUN', 'claim_ceiling': 'local preflight only; no acceptance or release'}
output('PREFLIGHT_SUMMARY.json', summary)
print(json.dumps(summary, ensure_ascii=False))
