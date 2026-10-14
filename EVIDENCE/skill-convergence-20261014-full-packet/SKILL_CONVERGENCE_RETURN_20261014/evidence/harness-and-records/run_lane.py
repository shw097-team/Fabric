import pathlib,subprocess,sys,os,json,datetime,sqlite3
R=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS');RUN=R/'var/SKILL-CONVERGENCE-20261014';E=RUN/'evidence';role=sys.argv[1].upper();tag=sys.argv[2] if len(sys.argv)>2 else '1';verify=role in ['VERIFY','SECURITY'];probe=role=='PROBE';folder=RUN/('qualification' if probe else 'verification/'+role.lower() if verify else 'candidates/'+role.lower());out=E/'lanes'/role.lower()/tag;out.mkdir(parents=True,exist_ok=False)
wo='WO-SKCV-20261014-'+role
with sqlite3.connect((R/'var/shared-spine/hg-kseos.db').as_uri()+'?mode=ro',uri=True) as c:
 c.row_factory=sqlite3.Row;b=dict(c.execute('select r.state requirement_state,t.state taskspec_state,t.writable_root,t.permissions_json,w.workorder_id,w.worktree from requirements r join taskspecs t on r.requirement_id=t.requirement_id join workorders w on t.taskspec_id=w.taskspec_id where w.workorder_id=?',(wo,)).fetchone())
assert b['requirement_state']=='FROZEN' and b['taskspec_state']=='ADMITTED';assert pathlib.Path(b['writable_root']).resolve()==folder.resolve()
if not probe and not verify:
 q=json.loads((E/'qualification_receipt.json').read_text());assert q['writer_scope_qualified'] is True,'Writer enforcement prerequisite not proven'
 bindings=json.loads((E/'execution_bindings.json').read_text());bind=next(x for x in bindings if x['workorder_id']==wo);assert pathlib.Path(bind['cwd']).resolve()==folder.resolve()
 import hashlib
 assert hashlib.sha256((E/'qualification_receipt.json').read_bytes()).hexdigest()==bind['writer_scope_qualification_digest']
 if role in ['HGK','AVR']:
  subject=bind['subject'];assert hashlib.sha256((pathlib.Path(subject['source'])/'SKILL.md').read_bytes()).hexdigest()==subject['skill_sha256'],'Canonical source changed before writer dispatch'
 if role=='CONSUMER':
  assert all(hashlib.sha256(pathlib.Path(x['source']).read_bytes()).hexdigest()==x['sha256'] for x in bind['subject']),'Runtime consumer source changed before writer dispatch'
LANE_ENV_PREAMBLE=(
 "\n\n--- LANE ENVIRONMENT (mandatory; added by the round runner after repeated shell failures) ---\n"
 "Your shell is PowerShell (pwsh) on Windows, NOT bash. Rules learned from this round's failed commands:\n"
 "1. NEVER use bash here-strings or heredocs: `<<'PY'`, `python - <<EOF`, `cmd <<'X'` all fail with ParserError / 'Missing file specification after redirection operator'. "
 "To run a Python script: write it to a .py file inside your own work directory first (Set-Content with a single-quoted here-string @'...'@ , or [IO.File]::WriteAllText with a UTF8Encoding($false)), then invoke it by path.\n"
 "2. `rg`, `grep`, bare `python` and bare `python3` are NOT on PATH in this lane. Use Select-String for searching, and always call Python by its full qualified path given in your brief. If you must discover a path, do it once and reuse it.\n"
 "3. Do NOT run recursive listings or whole-tree searches: no Get-ChildItem -Recurse, no `rg` over the tree, no scanning skill/references to 'see what is there'. Read only the files named in your brief.\n"
 "4. Prefer one written script you can re-run over a long inline -Command string; quoting inside nested PowerShell is where turns are lost.\n"
 "5. If a command fails twice for the same reason, stop and write the failure into your result file instead of retrying variations.\n"
 "--- END LANE ENVIRONMENT ---\n")
prompt=(E/'prompts'/(role.lower()+'-'+tag+'.md')).read_text(encoding='utf-8')+LANE_ENV_PREAMBLE;nonce='SKCV_'+role+'_'+tag+'_OK';prompt+='\nFinal literal transport token (not an acceptance): '+nonce+'\n'
args=[sys.executable,str(R/'scripts/hgk-lane-dispatch.py'),'--lane','VERIFY_SECURITY' if verify else 'EXECUTE','--prompt',prompt,'--nonce',nonce,'--force-rank','3' if verify else '1','--max-candidates','1','--require-arm','opencode-go/glm-5.3-flash' if verify else 'opencode-go/deepseek-v4.1-flash','--sandbox','read-only' if verify else 'workspace-write','--cwd',str(folder),'--timeout','600' if not probe else '150','--json-out',str(out/'dispatch.json'),'--attempt-log-dir',str(out/'raw')]
if os.environ.get('SKCV_DIAGNOSTIC_TRACE')=='1':
 args[1]=str(E/'observe_dispatch.py');os.environ['SKCV_TRACE_DIR']=str(out/'trace')
 budget=int(os.environ.get('SKCV_DIAGNOSTIC_BUDGET','150'));assert 1<=budget<=1500,'diagnostic budget is a round-only execution budget, not the acceptance oracle';args[args.index('--timeout')+1]=str(budget)
if verify:args+=['--guard-subject',str(RUN/'baseline'),'--guard-subject',str(RUN/'candidates')]
start=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run(args,capture_output=True,text=True,encoding='utf-8',timeout=1100 if not probe else 220);end=datetime.datetime.now(datetime.timezone.utc).isoformat();data={'role':role,'tag':tag,'workorder':wo,'cwd':str(folder),'start':start,'end':end,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'scope':'native sandbox qualification required; no danger-full-access or fallback','brief_remote_detection':'not invoked; no publication permission claimed'};(out/'driver.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n');print('EXIT',p.returncode,p.stdout[-11000:],p.stderr[-1500:]);sys.exit(p.returncode)
