"""Complete noncanonical preflight evidence; no product/admission/publication writes.
FDA-related content remains inside the explicitly authorized evidence root.
Preserve first-attempt failures and emit a separate corrected compiler contract.
"""
from pathlib import Path
import datetime
import hashlib
import json
import os
import re
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parent
PYTHON = 'C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe'
COMPILER_ROOT = Path('C:/Projects/Agent_Workspace/知識庫/實作相關DOC/HG-KSEOS/construction-acceptance-prompt-compiler/construction-acceptance-prompt-compiler')
COMPILER = COMPILER_ROOT / 'scripts/prompt_contract_compiler.py'
ENV = os.environ.copy()
ENV['PYTHONDONTWRITEBYTECODE'] = '1'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def emit(name, obj):
    path = ROOT / name
    assert path.resolve().is_relative_to(ROOT.resolve())
    data = obj if isinstance(obj, bytes) else (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(data)
    assert path.read_bytes() == data
    return {'path': str(path), 'sha256': sha(data), 'bytes': len(data)}

def record_run(name, command):
    result = subprocess.run(command, capture_output=True, timeout=90, env=ENV)
    receipt = {'command': command, 'exit_code': result.returncode,
        'observed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'stdout': emit(name + '.stdout.txt', result.stdout),
        'stderr': emit(name + '.stderr.txt', result.stderr),
        'claim_ceiling': 'local deterministic compiler/preflight only'}
    emit(name + '.receipt.json', receipt)
    return receipt

def inventory(path):
    data = path.read_bytes()
    text = data.decode('utf-8', 'strict')
    return {'path': str(path), 'sha256': sha(data), 'bytes': len(data), 'lines': len(text.splitlines())}

lock = json.loads((ROOT / 'OWNER_TRUST_LOCK.json').read_text(encoding='utf-8'))
pkg = Path(lock['package']['path'])
raw = pkg.read_bytes()
assert sha(raw) == lock['package']['sha256']
slots = {m.group(1): json.loads(m.group(2)) for m in list(re.finditer(r'(?ms)^```json SLOT:([^\n]+)\n(.*?)^```', raw.decode('utf-8')))[:27]}
knowledge_root = Path('C:/Projects/Agent_Workspace/知識庫/工程基座/GPTs_GENIEMAKER_開發實作+驗收指揮官_KP_Builder_ReleasePack_v2026.06.03-r2/KnowledgePack')
knowledge_files = sorted(knowledge_root.glob('*.md'))
assert len(knowledge_files) == 20
knowledge = []
for path in knowledge_files:
    text = path.read_text(encoding='utf-8')
    row = inventory(path)
    row['R04_rows'] = [line for line in text.splitlines() if re.match(r'^\| GPTB-KP\d+-R04 \|', line)]
    row['authority_disposition'] = 'SUPPORT_ONLY; R04 polarity not promoted; higher mission/HGK evidence rules prevail'
    knowledge.append(row)
plugin_root = Path('C:/Projects/Agent_Workspace/PIPD/skills')
plugin_rows = []
for item in slots['23_PLUGIN_TYPED_HANDOFF_8.json']:
    name = item['skill']
    files = [inventory(plugin_root / name / rel) for rel in ['SKILL.md', 'schemas/input.schema.json', 'schemas/output.schema.json', 'references/contract.md', 'references/examples.md', 'tests/cases.yaml']]
    plugin_rows.append({'skill': name, 'files': files, 'execution': 'NOT_RUN', 'vendor_receipt': None,
        'claim': 'physical typed contract bundle read; not compiled project package or loader qualification'})
fabric_paths = [Path('C:/Projects/Agent_Workspace/Fabric/fabric/consumers/hgk_policy_consumer.py'), Path('C:/Projects/Agent_Workspace/Fabric/stage/RP002-STAGE-HGK/F0/F0_POLICY_CONSUMER_TRACE.json')]
review = {'kind': 'STATIC_SOURCE_REVIEW_NOT_RUNTIME_QUALIFICATION',
    'knowledge': knowledge, 'plugins': plugin_rows, 'Fabric_consumer_sources': [inventory(p) for p in fabric_paths],
    'Fabric_claim': 'consumer source and historical F0 trace read; no current Convergence consumption invocation',
    'oracle_mapping': 'TT-PIPD-03 quarantined; DOC03 DOMAIN_ORACLES is not silently equated to DOC07 project oracle'}
review_artifact = emit('SOURCE_REVIEW_INVENTORY.json', review)
original_path = ROOT / 'C0_C9_CONTRACT.json'
contract = json.loads(original_path.read_text(encoding='utf-8'))
# Repair maker-authored schema errors; never relax the native compiler.
conflict = contract['authority']['conflicts'][0]
conflict['decision'] = 'QUARANTINE'
conflict['sources'] = ['SRC-DOC03', 'SRC-DOC07']
conflict['equal_rank'] = True
for docid, pattern in [('03', 'PIPD_LS_DOC-03*'), ('07', 'PIPD_LS_DOC-07*')]:
    paths = list((ROOT / 'physical_source_readback').glob(pattern))
    assert len(paths) == 1
    path = paths[0]
    contract['authority']['sources'].append({'id': 'SRC-DOC' + docid, 'rank': 'A2_SINGLE_WRITER',
        'path': str(path), 'sha256': sha(path.read_bytes()), 'locator': str(path), 'role': 'NORMATIVE', 'governs': True})
review_families = ['knowledge-00-19-review', 'eight-plugin-typed-bundle-review', 'current-Fabric-policy-consumption-review']
for i, family in enumerate(review_families):
    contract['source_scan']['reviewed'].append({'source_family': family, 'source_id': 'SRC-STATIC-REVIEW-' + str(i),
        'locator': str(ROOT / 'SOURCE_REVIEW_INVENTORY.json') + '#' + family,
        'sha256': review_artifact['sha256'], 'role': 'SUPPORT', 'critical': True})
contract['source_scan']['missing'] = [v for v in contract['source_scan']['missing'] if not any(v.startswith(f + ':') for f in review_families)]
contract['authority']['missing_sources'] = list(contract['source_scan']['missing'])
contract['render_policy']['output_language'] = 'zh-TW'
contract_artifact = emit('C0_C9_CONTRACT_R2.json', contract)
assert sha(COMPILER.read_bytes()) == '2c282ad6539a465c3b1d751868cab98437a8f35e9728be686117e364a70857d9'
compiler_runs = {}
for stage in ['lint', 'activation', 'acceptance', 'compile']:
    command = [PYTHON, '-B', str(COMPILER), stage, str(ROOT / 'C0_C9_CONTRACT_R2.json')]
    if stage == 'compile':
        command.extend(['--out-dir', str(ROOT / 'compiler_native_output_R2')])
    compiler_runs[stage] = record_run('COMPILER_R2_' + stage, command)
errors = json.loads((ROOT / 'COMPILER_R2_lint.stdout.txt').read_text(encoding='utf-8'))
assert all(e['code'] != 'PL-SCHEMA' for e in errors['errors']), errors
source_manifest = json.loads((ROOT / 'PHYSICAL_SOURCE_READBACK_MANIFEST.json').read_text(encoding='utf-8'))
# Fresh anonymous read only; no credential helper, token file or Git config involved.
def public_get(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'HGK-authorized-readonly-preflight'})
    return urllib.request.urlopen(request, timeout=30).read()
remote_ref = json.loads(public_get('https://api.github.com/repos/shw097-team/Fabric/git/ref/heads/main'))
remote_sha = remote_ref['object']['sha']
remote_docs = []
for name in ['KNOWN-FINDINGS.md', 'SOURCE-PROJECTION.md', 'NON-CLAIMS.md', 'APPROVAL-LIST-PROPOSAL.md', 'VALIDATION-AND-ROLLBACK.md', 'MANIFEST.json']:
    data = public_get('https://raw.githubusercontent.com/shw097-team/Fabric/' + remote_sha + '/INTEGRATION/' + name)
    remote_docs.append(emit('REMOTE_PUBLIC_READBACK/' + name, data))
known = (ROOT / 'REMOTE_PUBLIC_READBACK/KNOWN-FINDINGS.md').read_text(encoding='utf-8')
k_rows = []
for line in known.splitlines():
    if re.match(r'^\| K-\d+ \|', line):
        fields = [f.strip() for f in line.strip('|').split('|')]
        k_rows.append({'id': fields[0], 'finding': fields[1], 'remote_status': fields[2], 'evidence_or_gap': fields[3],
            'local_convergence_reverification': 'NOT_RUN', 'closure_claim': 'NOT_MADE'})
assert len(k_rows) == 20
emit('K_LEDGER_CROSSWALK_PREFLIGHT.json', {'remote_main': remote_sha, 'rows': k_rows, 'claim': 'current public ledger carry-forward only'})
repos = {}
for name in ['HG-KSEOS', 'Fabric']:
    path = 'C:/Projects/Agent_Workspace/' + name
    head = subprocess.run(['git', '-C', path, 'rev-parse', 'HEAD'], capture_output=True, check=True).stdout.decode().strip()
    status = subprocess.run(['git', '-C', path, 'status', '--porcelain=v1', '-z'], capture_output=True, check=True).stdout
    artifact = emit('REPO_READBACK/' + name + '.porcelain.bin', status)
    repos[name] = {'root': path, 'head': head, 'dirty': bool(status), 'porcelain': artifact}
case_rows = []
for row in slots['22_FULL_221_TEST_CONTRACTS.json']:
    case_rows.append({'id': row['id'], 'test_id': row['test_id'], 'kind': row['kind'],
        'source_locator': str(pkg) + '#Slot22/' + row['id'], 'state': 'BLOCKED_NOT_RUN',
        'runner_sha256': None, 'actual': None, 'raw_receipt': None, 'independent_receipt': None,
        'blockers': ['SOURCE_PHYSICAL_MISSING', 'PROMPT_COMPILE_BLOCKED', 'EXECUTION_ADMISSION_NOT_RUN']})
assert len(case_rows) == len({r['id'] for r in case_rows}) == 221
emit('RUNNER_AND_TEST_MATRIX_PREFLIGHT.json', {'planned': 221, 'actually_run': 0, 'rows': case_rows})
audit_rows = []
for row in slots['20_FULL_AUDIT_FINDINGS_24.json']:
    audit_rows.append(dict(row, convergence_status='BLOCKED_NOT_VERIFIED', actual_test=None,
        independent_receipt=None, source_locator=str(pkg) + '#Slot20/' + row['id']))
assert len(audit_rows) == len({r['id'] for r in audit_rows}) == 24
emit('AUDIT_24_CLOSURE_PREFLIGHT.json', {'closed': 0, 'open': 24, 'rows': audit_rows})
emit('MUTATIONS_18_PREFLIGHT.json', {'claim': 'plans only; zero mutation runs',
    'rows': [dict(r, actual_execution='BLOCKED_NOT_RUN', raw_receipt=None, independent_receipt=None)
             for r in slots['21_HOSTILE_MUTATIONS_18.json']]})
blockers = [
    {'code': 'SOURCE_PHYSICAL_MISSING', 'owner': 'source corpus custodian', 'details': source_manifest['missing'], 'unlock': 'provide the six exact original files matching recorded SHA/bytes; do not fabricate or weaken source denominator'},
    {'code': 'ORACLE_OWNER_CONFLICT', 'reference': 'TT-PIPD-03', 'owner': 'DOC03/DOC07 authority owner', 'unlock': 'explicit authorized oracle mapping; never implicit equivalence'},
    {'code': 'G1_UNCERTIFIED', 'owner': 'Human Policy Owner', 'unlock': 'Fresh G1 for actual canonical runtime and affected gates'},
    {'code': 'EXECUTION_ADMISSION_MISSING', 'owner': 'HGK typed admission authority', 'unlock': 'compiled contract, real RepoContext, exact TaskSpec/WorkOrder/ExecutionBinding before dispatch'},
    {'code': 'PUBLICATION_ALLOWLIST_PROPOSAL', 'owner': 'publication owner', 'unlock': 'approve exact changed paths, branch, reviewer, exclusions and revert plan; G-G before credential access'}]
emit('BLOCKERS_AND_RESUME.json', {'kind': 'NONCANONICAL_HANDOFF_NOT_SPINE_CHECKPOINT', 'blockers': blockers,
    'canonical_checkpoint': None, 'workorder': None, 'execution_binding': None,
    'resume': 'Supply exact missing sources; inspect SOURCE_REVIEW_INVENTORY and quarantined TT-PIPD-03; derive a new non-overwriting compiler revision and rerun native four stages. No model/product dispatch until admitted.',
    'rollback': 'No product or canonical mutation; retain this evidence directory. No automatic delete or reset.',
    'guard_refusals': {'nested_source_copy_calls': 2, 'nested_contract_write_calls': 1,
        'primary_tool_authorized_write': 'succeeded under explicit Owner FDA grant',
        'handling': 'No hook/token-store modifications. First refusal attempts preserved in session; subsequently used direct authorized tools and an explicitly bounded evidence generator.'}})
return_pack = {'mission_id': 'CNV-PIPD-LS-SP-20261015', 'changeset': 'CONTINUATION',
    'compiler_verdict': errors['verdict'], 'authority_and_owner_lock': 'PARTIAL_OWNER_PINS_VERIFIED_OTHER_AUTHORITY_GATES_OPEN',
    'candidate_subject_sha': None, 'local_hgk_head': repos['HG-KSEOS']['head'], 'local_fabric_head': repos['Fabric']['head'],
    'hermes_g1': 'UNVERIFIED', 'execution_admission': 'NOT_RUN',
    'audit_24': {'closed': 0, 'open': 24, 'unknown': 0},
    'requirement_cases': {'planned': 221, 'actually_run': 0, 'passed': 0, 'failed': 0, 'blocked': 221},
    'hostile_cases': {'planned': 18, 'passed': 0, 'failed': 0, 'blocked': 18},
    'gates': {'G-' + c: 'NOT_RUN' for c in 'ABCDEFGH'}, 'candidate_sha': None,
    'evidence_manifest_sha': None, 'independent_checker_receipt': None,
    'github': {'repository': 'shw097-team/Fabric', 'observed_main_sha': remote_sha, 'branch': None, 'commit_sha': None,
        'draft_pr': None, 'token_value': 'NEVER_EXPORT', 'credential_access': False},
    'blocking_tt_cr': ['TT-PIPD-03: source reference quarantined; no canonical disposition made'],
    'first_fail_code': 'SOURCE_PHYSICAL_MISSING', 'smallest_next_repair': 'supply six exact source files and authoritative oracle mapping',
    'rollback_pointer': 'BLOCKERS_AND_RESUME.json#rollback', 'canonical_checkpoint': None, 'verdict': 'TEMP_CLOSED'}
emit('CONVERGENCE_RETURN_PACK.json', return_pack)
summary = {'kind': 'NONCANONICAL_PREFLIGHT_R2_SUMMARY', 'physical_sources': {'standalone_originals_found': 14,
    'exact_appendix_recovery': 1, 'available_for_checker': 15, 'required': 21, 'missing': 6},
    'A1_A3': 'DOC00 source digest matches verified', 'knowledge_files_read': 20, 'typed_plugin_bundles_read': 8,
    'compiler_exits': {k: v['exit_code'] for k, v in compiler_runs.items()},
    'compiler_error_codes': sorted({e['code'] for e in errors['errors']}),
    'contract': contract_artifact, 'contract_acceptance_edges': len(contract['acceptance']),
    'planning_test_identities': 221, 'runtime_cases_executed': 0, 'canonical_mutations': 0, 'product_mutations': 0,
    'model_dispatches': 0, 'credential_access': False, 'remote_mutations': 0, 'repos': repos,
    'remote_main': remote_sha, 'verdict': 'TEMP_CLOSED'}
emit('PREFLIGHT_SUMMARY_R2.json', summary)
handoff = '''# Convergence 本輪 preflight 交接（非 canonical checkpoint）

## 裁決
TEMP_CLOSED。Owner 已明確核定完整 PKG SHA 與 standalone verifier SHA；尚未取得本案 source freeze、Compiler PASS、HGK admission、Fresh G1、獨立驗收或發布資格。

## 已實際完成
- 保存 Owner trust 與 FDA 文件範圍授權；未修改任何 hook。
- A1/A3 原件 SHA 與 DOC00 來源表一致。
- 21 份來源：14 份現有原件 + 1 份已核定附件內的原始 legacy bytes 無損回復；仍缺 6 份。
- 已讀 Knowledge 00..19 與八個實體 PIPD typed plugin bundles；僅靜態來源審查，不是 vendor pipeline 或 host loader 執行。
- 保存核心目標、SPEC、CNV-01..19、CK-01..20；C0-C9 R2 含 279 acceptance edges，與 221 規劃測試身份不同分母。
- 文件 checker 真實 exit30；正式 compiler 四階兩輪皆有 raw stdout/stderr/exit；R2 無 PL-SCHEMA，仍因來源缺件及 TT-PIPD-03 quarantine 阻擋。
- fresh 匿名讀回 GitHub main 與六份 INTEGRATION 文件；K-01..20 原 ID 逐項保留。

## 未執行
無產品修改、無 canonical admission/TT/checkpoint 寫入、無本案 Codex model dispatch、無 221/18 runtime 測試、無 Token 存取、無 GitHub branch/push/PR、無 acceptance/release。

## 證據索引
- MISSION_PLAN_SPEC_CHECKLIST.json
- OWNER_TRUST_LOCK.json / FDA_SCOPE_AUTHORIZATION.json
- PHYSICAL_SOURCE_DISCOVERY_EXPANDED.json / PHYSICAL_SOURCE_READBACK_MANIFEST.json
- SOURCE_REVIEW_INVENTORY.json
- PACKAGE_CHECK_FLAT.receipt.json + raw stdout/stderr
- C0_C9_CONTRACT.json（首次 schema 失敗原件保留）
- C0_C9_CONTRACT_R2.json / COMPILER_R2_*.receipt.json / compiler_native_output_R2/compiler-report.json
- RUNNER_AND_TEST_MATRIX_PREFLIGHT.json / AUDIT_24_CLOSURE_PREFLIGHT.json / MUTATIONS_18_PREFLIGHT.json
- K_LEDGER_CROSSWALK_PREFLIGHT.json / REMOTE_PUBLIC_READBACK/
- BLOCKERS_AND_RESUME.json / CONVERGENCE_RETURN_PACK.json / PREFLIGHT_SUMMARY_R2.json

## 最小續作
PHYSICAL_SOURCE_READBACK_MANIFEST.json 的 missing[] 列出六份原件的 exact filename/bytes/SHA。補齊原件並取得 DOC03/DOC07 oracle mapping 後，重新驗證 currentness，建立新編號 contract/output，不覆寫既存失敗紀錄；待 native compiler PASS 才進 HGK typed admission。不能以全面授權取代來源 bytes 或獨立驗收。

## 副作用與回滾
僅本證據根的新增檔案、明確標示 provenance 的來源副本、read-only subprocess 及匿名 GET。三次 nested helper write 被 hook 拒絕（兩次 source copy，一次 contract）；direct authorized write 成功後，改用直接工具與受限 evidence generator，沒有修改安全 hook 或授權存放區。無產品改動可回滾；保留證據，不自動刪除或 reset。
'''
emit('PREFLIGHT_HANDOFF.md', handoff.encode('utf-8'))
# Manifest is constructed after all producers stop; exclude itself by construction.
manifest_rows = []
for path in sorted(ROOT.rglob('*')):
    if path.is_file() and '__pycache__' not in path.parts:
        data = path.read_bytes()
        manifest_rows.append({'path': path.relative_to(ROOT).as_posix(), 'bytes': len(data), 'sha256': sha(data)})
emit('PREFLIGHT_EVIDENCE_MANIFEST.json', {'kind': 'NONCANONICAL_LOCAL_EVIDENCE_MANIFEST',
    'self_excluded_by_construction': True, 'file_count': len(manifest_rows), 'files': manifest_rows,
    'not_approved_for_publication': True, 'claim': 'byte inventory only; no independent acceptance'})
print(json.dumps(summary, ensure_ascii=False))
