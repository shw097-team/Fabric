import json,subprocess,os
from pathlib import Path
W=Path(__file__).parent
A=json.loads((W/'measure_results.json').read_text(encoding='utf-8'))
B=json.loads((W/'more_results.json').read_text(encoding='utf-8'))
H=Path('C:/Projects/Agent_Workspace/PIPD/worktrees/r8-wt');C=Path('C:/Projects/wt-r8-cleanmain');K=Path('C:/Projects/Agent_Workspace/HG-KSEOS')
def quote(p,a,b):
 l=p.read_text(encoding='utf-8').splitlines();return {'path':str(p),'start':a,'end':min(b,len(l)),'quote':'\n'.join(f'{i}|{l[i-1]}' for i in range(a,min(b,len(l))+1))}
patch=subprocess.run(['git','diff','--','src/pipd_ls_sp/validate.py','src/pipd_ls_sp/pipeline.py','src/pipd_ls_sp/cli.py'],cwd=H,capture_output=True,text=True,encoding='utf-8')
numstat=A['diff']['stdout'].splitlines();added=sum(int(x.split()[0]) for x in numstat);removed=sum(int(x.split()[1]) for x in numstat)
r8=Path('C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8')
search={'receipt_json_matches':[str(p) for p in sorted(r8.rglob('*receipt*.json'))],'attempts_ndjson_matches':[str(p) for p in sorted(r8.rglob('*attempts*.ndjson'))],'R8_VERIFY_files':[str(p) for p in sorted((r8/'R8_VERIFY').rglob('*')) if p.is_file()], 'finding':'No dispatcher invocation receipt or attempts trail is stored in R8 itself. Recent R8 lane runs reused the ORIGINAL mission lane_runs location; append-only trail holds older and R8 runs under distinct run_id. The final attempt1 JSON files have October 16 timestamps and overwrite earlier same-name receipt files.'}
registry=json.loads(B['declared_routes']['stdout'])
recent=[]
for row in B['mission_receipts']:
 if row['generated_utc'] and row['generated_utc'].startswith('2026-10-16'):recent.append(row)
F={
 'schema':'CNV-R9-FAR-WS2-TECH-FACTS/1','claim_ceiling':'LOCAL/candidate-only research; not acceptance; no fix implemented',
 'A':{
  'baseline':{'hardened':str(H),'clean':str(C),'commit':A['hardened_head']['stdout'].strip(),'modified_files':numstat,'added':added,'removed':removed,'hunks':sum(x.startswith('@@ ') for x in A['patch']['stdout'].splitlines())},
  'trace_failure':{
   'cause_one_sentence':'The legal test supplies a PI-PKG and its real TraceLink but no frozen_context, and hardened validate_bundle forwards None rather than deriving the available PI endpoint map, so semantic_invariants emits UNBOUND_FROZEN_CONTEXT for both hashes even though closure resolves both endpoints.',
   'test':quote(H/'tests/test_s4ext_trace_closure.py',108,116),
   'clean_trace_rule':quote(C/'src/pipd_ls_sp/validate.py',190,195),
   'clean_bundle':quote(C/'src/pipd_ls_sp/validate.py',266,294),
   'hardened_trace_rule':quote(H/'src/pipd_ls_sp/validate.py',215,242),
   'hardened_bundle':quote(H/'src/pipd_ls_sp/validate.py',383,409),
   'positive_control':B['clean_trace_direct'],'reproduction':B['hardened_trace_direct'],
   'fixture_scope':'Direct invocation runs the unchanged test method using a freshly compiled bundle bound to the existing clean repo; it omits git-initializing fixture setup. A prior pytest reproduction also ran (see issues).'},
  'crash':{
   'cause_one_sentence':'CLI run passes the PI-PKG dictionary as source, but the checked-in s1 bundle contains a nonempty string at source[stable_semantic_contract][atoms][0][risk_guard], and derive_frozen_context line 434 invokes .get(oracle) on that string because or {} only guards falsy values, not non-dict values.',
   'exact_argument':'The positional source argument is a dict, NOT a str; the nested atom["risk_guard"] value becomes the receiver of .get("oracle") and is str where a mapping is required.',
   'caller':quote(H/'src/pipd_ls_sp/cli.py',164,177),
   'function_complete':quote(H/'src/pipd_ls_sp/validate.py',412,446),
   'other_callers':quote(H/'src/pipd_ls_sp/pipeline.py',207,240),
   'smoke_fixture_and_caller':quote(H/'tools/cli_smoke.py',31,54),
   'schema_legacy_shape':quote(H/'schemas/RequirementAtom.schema.json',15,35),
   'crash_raw':B['cli_validate_crash'],'isolated_repro':A['crash_repro'],'smoke_test_raw':A['smoke_test']},
  'minimal_fix_surface':{
   'file':'src/pipd_ls_sp/validate.py','functions':['validate_bundle','derive_frozen_context'],
   'change_1':{'location':'validate_bundle, between current lines 391 and 392 (before per-record semantic checks)','smallest_change':'If frozen_context is None AND bundle.get("PI-PKG") is a dict, set frozen_context = derive_frozen_context(bundle["PI-PKG"]). Do not replace any caller-supplied context, including explicit {}. Leave semantic_invariants fail-closed and closure_findings unchanged. No PI means no auto-binding; a lone TraceLink must still fail closed.'},
   'change_2':{'location':'derive_frozen_context, current line 434, before subsequent oracle.get calls at 435-436','smallest_change':'Replace the unsafe chain with rg = atom.get("risk_guard"); oracle = rg.get("oracle") if isinstance(rg, dict) else None; oracle = oracle if isinstance(oracle, dict) else {}. Keep endpoint collection at 432-433, the req_id/expected guard at 435-436, and explicit frozen map precedence (setdefault). A legacy string has no derivable oracle map entry; do not invent an expectation or discard endpoint bindings.'},
   'no_change_needed':['src/pipd_ls_sp/pipeline.py','src/pipd_ls_sp/cli.py','semantic_invariants','DIGEST_BOUND','POLARITY_EXPECTED','ProfileBinding assurance checks','closure_findings'],
   'hardening_preservation':'M04 and M06 still hit unchanged self-body digest checks plus unchanged assurance/polarity checks; M16 still hits unchanged self-body digest and endpoint mismatch/closure checks. The observed M16 runner validates a lone edge and thus additionally remains unbound. Never copy an edge from_hash/to_hash into the endpoint map to satisfy itself.',
   'verification_limit':'This is the minimal inferred repair specification, not a post-fix pass claim: implementation and testing a changed implementation were explicitly prohibited. Both existing failures were reproduced, clean trace positive control passed, and unchanged hardened M04/M06/M16 were re-run and REJECTED.'},
  'mutation_measurements':{x:B[x] for x in ['m04','m06','m16']},
  'product_diff_unchanged':patch.returncode==0 and patch.stdout==A['patch']['stdout'],
  'clean_status_after':B['clean_status_after'],'hardened_status_after':B['hard_status_after']
 },
 'B':{
  'requested_root_discovery':search,
  'actual_lane_receipt_root':'C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/lane_runs',
  'all_discovered_receipt_and_trail_rows':B['mission_receipts'],
  'raw_final_receipt_files':sum(1 for r in B['mission_receipts'] if r['generated_utc']),
  'raw_trail_rows':sum(1 for r in B['mission_receipts'] if r['generated_utc'] is None),
  'recent_R8_final_receipts':recent,
  'recent_R8_trail_run_ids':['4640-1792119447','2480-1792119780','2900-1792121826'],
  'error_condition_source':quote(K/'scripts/hgk-lane-dispatch.py',1033,1062),
  'where_error_is_surfaced':quote(K/'scripts/hgk-lane-dispatch.py',2226,2235),
  'attempt_identity_fields_source':quote(K/'scripts/hgk-lane-dispatch.py',1263,1276),
  'trail_and_usable_turn_gate':quote(K/'scripts/hgk-lane-dispatch.py',2123,2138),
  'top_level_receipt_fields':quote(K/'scripts/hgk-lane-dispatch.py',2202,2235),
  'answer':'YES: answered-arm attribution is recoverable from attempts[].provider/model/transport_model, backed by attempts[].usage_provider/usage_model/usage_status=200 and usage_receipt_ok=true, and from nonce_absent_arms. Recent EXECUTE runs answered on opencode-go/deepseek-v4.1-flash rank 1; recent VERIFY answered on opencode-go/glm-5.3-flash rank 2. The missing nonce means the completion/nonce attestation failed, NOT that model identity fields are absent. Top-level served_arm is genuinely absent and used_rank/used_transport_model null because used is assigned only after exit==0 AND nonce_present AND usage_receipt_ok (and any completion gate). Never upgrade these runs to successful/accepted turns. This is relay-usage attribution, not independent provider-internals model attestation.',
  'error_semantics':'ERR_NO_ARM_EMITTED_NONCE is returned (not raised as an exception) at 1057 by failure_disposition when at least one attempt has exit 0 and truthy usage_receipt_ok, and none of those answered attempts has nonce_present. The returned fields merge into receipt at 2230; failure receipt is written at 2269. Timeouts alone do not meet answered.'
 },
 'C':{
  'declared_values_complete':registry,'drift_raw':B['drift'],
  'drift_verdict':'[] (exit 0): no projection mismatch reported by the repository check_drift at measurement time.',
  'digest_expected':'e98c516f1c8935789aabe9122ee7e05ec4c3efd1ba6acf179242e031c495b99e',
  'projection':'hermes-codex-lane / config/hermes-codex-lane.json /codex_sha256',
  'declaration_disagreement_not_covered_by_empty_drift':'Assignment VERIFY_SECURITY top-level assigned_provider/model is opencode-go/glm-5.3-flash while registry route, assignment supply_selector default A, and lane_chains VERIFY rank 1 name openai-codex/gpt-6.1-sol. Registry projection expectations explicitly pin both inconsistent surfaces, so empty check_drift does not prove internal semantic consistency or conformity to an external mandate. PLAN route remains opencode-go/glm-5.3-flash; EXECUTE reasoning_effort absent in route and assignment, null in lane_chains.'
 },
 'issues':[
  'No dispatcher receipt/trail was in the requested R8 subtree; expanded read-only discovery found reused original mission lane_runs paths, with append-only rows distinguishing runs.',
  'The first pytest trace attempt intended to replace fixture setup but imported top-level test_s4ext_trace_closure while pytest collected tests.test_s4ext_trace_closure; therefore its fixture substitution did not take effect and the original helper performed git init/add/commit only in a disposable directory under ws2. This inadvertently violated the no-git-write-command constraint; no product/control-plane file was changed. Subsequent direct method clean/hardened reproductions omitted the git-initializing helper entirely.',
  'A broad pathlib discovery of older handover trees hit WinError 1920 on a historical lib64 link; bounded search_files discovery succeeded instead.',
  'No network used. No remediation implemented. No credential values printed. All authored files and test temporaries are under ws2. Interpreter actually reports Python 3.11.9 in pytest output, despite runtime generic toolchain description.'
 ],
 'raw_logs':['measure_raw.log','more_raw.log','raw_command_outputs.log'],
 'raw_measurements':{'first':{k:v for k,v in A.items() if k!='receipts'},'second':B}
}
(W/'tech_facts.json').write_text(json.dumps(F,ensure_ascii=False,indent=2),encoding='utf-8')
raw=(W/'measure_raw.log').read_text(encoding='utf-8')+'\n'+(W/'more_raw.log').read_text(encoding='utf-8')
raw+='\nFINAL DIFF VERIFICATION\n$ git diff -- src/pipd_ls_sp/validate.py src/pipd_ls_sp/pipeline.py src/pipd_ls_sp/cli.py\nSTDOUT:\n'+patch.stdout+'\nSTDERR:\n'+patch.stderr+'\nEXIT='+str(patch.returncode)+'\nDIFF_UNCHANGED='+str(F['A']['product_diff_unchanged'])
(W/'raw_command_outputs.log').write_text(raw,encoding='utf-8')
check=json.loads((W/'tech_facts.json').read_text(encoding='utf-8'))
print(json.dumps({'tech_facts_json_valid':True,'diff_unchanged':check['A']['product_diff_unchanged'],'added':added,'removed':removed,'hunks':check['A']['baseline']['hunks'],'receipt_files':check['B']['raw_final_receipt_files'],'trail_rows':check['B']['raw_trail_rows'],'drift_stdout':check['C']['drift_raw']['stdout'],'output_paths':[str(W/'tech_facts.json'),str(W/'raw_command_outputs.log')]},indent=2))
