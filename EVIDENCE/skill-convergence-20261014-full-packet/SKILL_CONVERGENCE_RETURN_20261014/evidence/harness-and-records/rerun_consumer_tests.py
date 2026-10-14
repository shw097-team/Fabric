"""Corrects and completes the harness re-run of the consumer phase-3 tests.

The first harness attempt ran pytest with the qualified interpreter but without the user
site-packages on PYTHONPATH, so pytest was not importable and the run failed for a harness
reason, not a product reason. That stale result is recorded here as superseded, together
with the corrected run and the full-suite regression comparison against the unpatched live
runtime.
"""
import pathlib,json,subprocess,datetime
RUN=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014')
C=RUN/'candidates/consumer'
LIVE=pathlib.Path('C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/hermes-agent')
PY='C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/hermes-agent/venv/Scripts/python.exe'
SITE='C:/Users/user/AppData/Roaming/Python/Python311/site-packages'
def run(cwd,args,env_extra=None):
 import os
 env=dict(os.environ);env['PYTHONPATH']=SITE;env['PYTHONDONTWRITEBYTECODE']='1'
 if env_extra:env.update(env_extra)
 p=subprocess.run([PY,'-m','pytest','-q','--no-header','-p','no:cacheprovider',*args],cwd=cwd,env=env,
   capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=900)
 return {'cwd':str(cwd),'args':args,'exit':p.returncode,'summary':[l for l in (p.stdout or '').strip().splitlines() if 'passed' in l or 'failed' in l or 'error' in l][-2:]}
out={'schema':'SKCV-CONSUMER-PHASE3-TESTS-RERUN/2',
 'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'superseded_first_attempt':{'what_it_said':'both test targets exited 1','real_reason':'the harness invoked pytest without the user site-packages on PYTHONPATH, so the qualified interpreter reported "No module named pytest". This was a harness fault, not a product failure, and it is kept here rather than deleted.'},
 'environment':{'pytest':'9.1.1 from '+SITE,'interpreter':PY,
   'known_environment_limit':'symlink creation is refused on this host (WinError 1314, no SeCreateSymbolicLinkPrivilege), so symlink-dependent tests cannot run here'},
 'corrected_runs':{
   'reader_test':run(C,['tests/tools/test_lint_reader_edit.py']),
   'lint_full_current':run(C,['tests/tools/test_lint_full_current.py']),
   'whole_tools_suite_candidate':run(C,['tests/tools/']),
   'same_failing_test_on_unpatched_live_runtime':run(LIVE,['tests/tools/test_skill_manager_tool.py::TestDeleteSkillRmtreeGuard::test_symlinked_skill_dir_refused'])},
 'claim_ceiling':'these are runs of the maker-authored tests by the round harness; a green suite proves those tests pass in this environment and that no test the patch touches regressed, not that the change is correct or accepted'}
p=RUN/'verification/round-harness/consumer_phase3_tests_rerun.json'
p.write_text(json.dumps(out,ensure_ascii=False,indent=2,default=str),encoding='utf-8',newline='\n')
print(json.dumps(out['corrected_runs'],ensure_ascii=False,indent=1))
