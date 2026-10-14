"""Independent check of the CONSUMER phase-3 claims (round harness side).

Does not trust phase3_result.json: it re-hashes the claimed files, re-runs the tests with
the qualified interpreter, checks the reader is actually reached from the edit path rather
than merely defined, and confirms no cap/threshold/policy constant moved relative to the
live runtime copy.
"""
import pathlib,json,hashlib,re,subprocess,sys
RUN=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014')
C=RUN/'candidates/consumer'
LIVE=pathlib.Path('C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/hermes-agent')
PY='C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/hermes-agent/venv/Scripts/python.exe'
if not pathlib.Path(PY).exists():PY='C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe'
h=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
res=json.loads((C/'phase3_result.json').read_text(encoding='utf-8'))
digest_ok={}
for fc in res['files_changed']:
 p=C/fc['path']
 digest_ok[fc['path']]={'exists':p.exists(),
   'claimed_after_matches_disk':(h(p)==fc['after_sha256']) if p.exists() else None,
   'is_new_file':fc['before_sha256'] is None}
# reader reached from the edit path?
t=(C/'tools/skill_manager_tool.py').read_text(encoding='utf-8',errors='replace')
defs=len(re.findall(r'def _consult_skill_lint',t))
calls=len(re.findall(r'_consult_skill_lint\(',t))-defs
edit_body=None
m=re.search(r'def _edit_skill\(.*?(?=\ndef |\Z)',t,re.S)
if m:edit_body=m.group(0)
bt=(C/'tools/skill_manager_batch.py').read_text(encoding='utf-8',errors='replace')
# policy constants unchanged vs the live runtime copy
CONST=re.compile(r'^(MAX_SKILL_CONTENT_CHARS|_BODY_SOFT_BUDGET_CHARS|MAX_REFERENCE_FILES|_MAX_REFERENCE_FILES)\s*[:=]\s*(.+)$',re.M)
def consts(txt):return {k:v.strip() for k,v in CONST.findall(txt)}
cand_consts=consts(t) if False else None
cand_lint=(C/'tools/skill_linter.py').read_text(encoding='utf-8',errors='replace')
live_lint=(LIVE/'tools/skill_linter.py')
live_lint_txt=live_lint.read_text(encoding='utf-8',errors='replace') if live_lint.exists() else ''
const_cmp={'candidate':consts(cand_lint),'live':consts(live_lint_txt),
  'identical':consts(cand_lint)==consts(live_lint_txt)}
# re-run the tests
def runpytest(targets):
 cmd=[PY,'-m','pytest','-q','--no-header','-p','no:cacheprovider',*targets]
 p=subprocess.run(cmd,cwd=str(C),capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=900)
 tail=(p.stdout or '').strip().splitlines()[-6:]
 return {'cmd':' '.join(cmd),'exit':p.returncode,'tail':tail,'stderr_tail':(p.stderr or '').strip().splitlines()[-3:]}
tests={'reader_test':runpytest(['tests/tools/test_lint_reader_edit.py']),
       'lint_full_current':runpytest(['tests/tools/test_lint_full_current.py'])}
out={'schema':'SKCV-INDEP-CONSUMER-PHASE3-CHECK/1','digest_check':digest_ok,
 'reader_reached_from_edit_path':{'definitions':defs,'call_sites_outside_definition':calls,
   'called_inside_edit_skill':bool(edit_body and '_consult_skill_lint(' in edit_body)},
 'batch_advisor_keys':{k:(k in bt) for k in ['lint_evaluation_status','full_current_lint_findings']},
 'policy_constants':const_cmp,'tests_rerun_by_harness':tests,
 'claim_ceiling':'it re-runs the maker tests and re-hashes its files; it is not an independent checker verdict, it does not prove the reader changes behaviour under a real governed edit, and it grants no acceptance'}
print(json.dumps(out,ensure_ascii=False,indent=1))
