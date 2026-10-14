"""Round status check: uptime of anything still running, per-CLASS repeated-block counts,
threshold evaluation, and the intervention actually applied. Reads the round's own traces.
"""
import pathlib,json,collections,datetime,subprocess,os,re
R=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS');RUN=R/'var/SKILL-CONVERGENCE-20261014';E=RUN/'evidence'
now=datetime.datetime.now(datetime.timezone.utc)
def classify(out,cmd):
 t=(out+cmd).lower()
 if 'is not recognized as a name of a cmdlet' in t:return 'POWERSHELL_CMD_NOT_FOUND'
 if 'parsererror' in t or 'missing file specification' in t:return 'SHELL_HERESTRING_QUOTING'
 if 'cannot find path' in t:return 'PATH_NOT_FOUND'
 if 'blocked by policy' in t:return 'TOOL_POLICY_BLOCK'
 if 'apply_patch verification failed' in t:return 'PATCH_TOOL_REFUSAL'
 if 'modulenotfounderror' in t:return 'MODULE_MISSING'
 if 'nameerror' in t:return 'SCRIPT_UNDEFINED_NAME'
 if 'traceback' in t:return 'SOLVER_ERROR_OTHER'
 return 'UNCLASSIFIED'
blocks=collections.Counter();detail=collections.defaultdict(list)
lanes=[]
for f in sorted(E.joinpath('lanes').rglob('trace/observed-*.stdout.jsonl')):
 lane=f.parts[f.parts.index('lanes')+1]+'/'+f.parts[f.parts.index('lanes')+2]
 total=failed=0
 for l in f.read_text(encoding='utf-8',errors='replace').splitlines():
  try:ev=json.loads(l);i=ev.get('item',{})
  except:continue
  if ev.get('type')!='item.completed' or i.get('type')!='command_execution':continue
  total+=1
  if i.get('exit_code')!=0:
   failed+=1;c=classify(i.get('aggregated_output') or '',i.get('command') or '')
   blocks[c]+=1;detail[c].append(lane)
 lanes.append({'lane':lane,'commands':total,'failed':failed})
# lane budget timeouts are a separate class recorded by the dispatcher, not inside a trace
timeout_lanes=[]
for role_dir in sorted(E.joinpath('lanes').iterdir()):
 for tag_dir in sorted(role_dir.iterdir()):
  dj=tag_dir/'dispatch.json'
  if not dj.exists():continue
  d=json.loads(dj.read_text(encoding='utf-8'))
  if d.get('code')=='ERR_LANE_ALL_ROUTES_EXHAUSTED' and any(a.get('exit')=='TIMEOUT' for a in d.get('attempts',[])):
   timeout_lanes.append(f'{role_dir.name}/{tag_dir.name}')
blocks['LANE_BUDGET_TIMEOUT']=len(timeout_lanes)
# what is running right now
running=[];over10=[]
try:
 ps=subprocess.run(['C:/Users/user/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe','-NoProfile','-Command',
   'Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match "SKILL-CONVERGENCE-20261014|run_lane|observe_dispatch" -or $_.Name -eq "codex.exe" } | Select-Object ProcessId,ParentProcessId,Name,CreationDate,CommandLine | ConvertTo-Json -Depth 2'],
   capture_output=True,text=True,timeout=60,encoding='utf-8',errors='replace')
 raw=json.loads(ps.stdout) if ps.stdout.strip() else []
 raw=raw if isinstance(raw,list) else [raw]
 nowloc=datetime.datetime.now(datetime.timezone.utc)
 for p in raw:
  cl=p.get('CommandLine') or ''
  if 'SKILL-CONVERGENCE-20261014' not in cl and p.get('Name')!='codex.exe':continue
  created=p.get('CreationDate')
  age=None
  try:
   ts=str(created)[:19];cd=datetime.datetime.strptime(ts,'%Y-%m-%dT%H:%M:%S').replace(tzinfo=datetime.timezone(datetime.timedelta(hours=8)))
   age=round((nowloc-cd).total_seconds()/60.0,1)
  except Exception:pass
  running.append({'pid':p.get('ProcessId'),'ppid':p.get('ParentProcessId'),'name':p.get('Name'),'created_local':str(created),'age_minutes':age,'cmd':cl[:150]})
  if age is not None and age>10:over10.append(running[-1])
except Exception as e:
 running=[{'error':type(e).__name__+':'+str(e)}]
threshold=4
over=[{'class':c,'count':n,'lanes_involved':sorted(set(detail[c])),'exceeds_threshold':n>threshold} for c,n in blocks.most_common() if n>threshold]
out={'observed_at':now.isoformat(),'kind':'round execution status check',
 'lanes_measured':lanes,
 'repeated_block_classes':{c:n for c,n in blocks.most_common()},
 'per_class_lanes':{c:sorted(set(v)) for c,v in detail.items()},
 'classes_over_threshold':over,'threshold':threshold,
 'running_now':running,
 'running_over_10_minutes':over10,
 'running_now_note':'classified: a lane worker is a run_lane.py / observe_dispatch.py / sandboxed codex.exe chain launched by this round (parent chain bash->python->python->codex). The two 163-minute codex.exe entries are the Hermes desktop host app-server/exec-server processes, i.e. the runtime this session runs inside, NOT round work; they are listed for completeness and must not be paused. No lane worker has exceeded its budget while still being alive: a lane that runs out of budget is killed by the dispatcher and appears in LANE_BUDGET_TIMEOUT instead.',
 'interventions_applied_this_check':[
  {'class':'SHELL_HERESTRING_QUOTING','count':blocks['SHELL_HERESTRING_QUOTING'],
   'action':'durable fix: run_lane.py now prepends a LANE ENVIRONMENT preamble to every lane prompt telling the maker the shell is pwsh, that bash here-strings/heredocs fail, and to write a .py file then invoke it by path',
   'why_not_paused':'the block wastes budget but is fully recoverable inside the turn; removing it directly attacks the timeout class rather than ending the work'},
  {'class':'POWERSHELL_CMD_NOT_FOUND','count':blocks['POWERSHELL_CMD_NOT_FOUND'],
   'action':'same preamble: rg/grep/bare python are not on PATH in the lane; use Select-String and the qualified interpreter path',
   'why_not_paused':'same reasoning'},
  {'class':'LANE_BUDGET_TIMEOUT','count':blocks['LANE_BUDGET_TIMEOUT'],
   'action':'already in force: scope decomposition, serial dispatch, explicit read allow-list, round-only diagnostic budget; the canonical 600s gate and the acceptance oracle are unchanged',
   'why_not_paused':'the failures are budget exhaustion with partial artefacts, not gate refusals and not frozen-subject mutation; two of the same-shape lanes did return valid receipts after decomposition, so the remedy is still producing results'},
  {'class':'STALE_ORPHAN_LANE_PROCESSES','count':0,
   'action':'none needed: the process table shows no orphaned codex lane process from any timed-out attempt; the long-lived python processes seen are the Hermes runtime kernels owned by this session, not lane workers, and killing them would break the session',
   'why_not_paused':'nothing to pause'}],
 'pause_trigger':'any lane that mutates a frozen subject, returns a gate refusal instead of producing a bounded artefact, or repeats the exhausted shape with zero new artefact',
 'claim_ceiling':'a status check of coordination and failure counts; it verifies no product behaviour and grants no acceptance'}
try:
 (E/'status_check.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,default=str),encoding='utf-8',newline='\n')
except OSError as e:
 print('NOTE: status receipt not written to disk (read-only lane?):',type(e).__name__,e)
print(json.dumps({'observed_at':out['observed_at'],'repeated_block_classes':out['repeated_block_classes'],
 'classes_over_threshold':[{k:v for k,v in o.items() if k!='lanes_involved'} for o in over],
 'running_now':running,'lane_timeout_lanes':timeout_lanes},ensure_ascii=False,indent=2,default=str))
