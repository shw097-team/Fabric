import pathlib,json,os,hashlib,sys,shutil,datetime,sqlite3
R=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS');RUN=R/'var/SKILL-CONVERGENCE-20261014';E=RUN/'evidence';H=pathlib.Path(os.environ['HERMES_HOME']);RT=H/'hermes-agent';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
D=json.loads((E/'lanes/probe/2/dispatch.json').read_text());assert D['ok'] is True and D['usage_receipt_ok'] is True and D['required_arm']==D['served_arm']=='opencode-go/deepseek-v4.1-flash'
completed=[]
for a in D['attempts']:
 for line in pathlib.Path(a['stdout_path']).read_text(encoding='utf-8').splitlines():
  try:it=json.loads(line).get('item',{})
  except:continue
  if it.get('type')=='command_execution' and it.get('status')=='completed' and it.get('exit_code')==0 and 'qualify_native.py' in it.get('command','') and '"all_negative_seams_refused"' in it.get('aggregated_output',''):completed.append(it)
assert len(completed)==1
raw=completed[0]['aggregated_output'];q=json.JSONDecoder().raw_decode(raw[raw.index('{'):])[0];assert q['positive'] is True and q['all_negative_seams_refused'] is True and q['junction_fixture_exists'] is True and len(q['rows'])==4 and all(x['refused'] is True for x in q['rows'])
pos=RUN/'qualification/admitted-marker.txt';assert pos.read_bytes()==b'SKCV_ADMITTED_WRITE';outside=H/'cache/scratch/SKCV-owned-escape-root';neg=[outside/'outside-direct.txt',outside/'outside-subprocess.txt',outside/'junction-escape.txt',E/'SKCV-SIBLING-ESCAPE.txt'];assert all(not p.exists() for p in neg)
qr={'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'writer_scope_qualified':True,'mechanism':'Codex native Windows elevated workspace-write sandbox; qualified admitted cwd and outside-cwd direct/subprocess/preexisting-junction/sibling write seams','sandbox_bypass':False,'raw_dispatch':str(E/'lanes/probe/2/dispatch.json'),'actual_command':completed[0]['command'],'command_exit':completed[0]['exit_code'],'raw_observations':q,'host_readback':{'positive_path':str(pos),'positive_sha256':sha(pos),'outside_absent':[str(p) for p in neg]},'prior_probe_1':'INCOMPLETE marker mismatch and traversal not tested; superseded not deleted','claim_ceiling':'scoped fixture qualification; not universal sandbox security, endpoint-only egress or independent product acceptance'}
(E/'qualification_receipt.json').write_text(json.dumps(qr,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
subjects=json.loads((E/'subject_binding.json').read_text())
for it in subjects:
 source=pathlib.Path(it['source']);base=pathlib.Path(it['baseline']);assert sha(source/'SKILL.md')==it['skill_sha256'];out=RUN/'candidates'/it['role'].lower()/'skill';shutil.copytree(base,out);assert all(sha(p)==sha(out/p.relative_to(base)) for p in base.rglob('*') if p.is_file())
rels=['tools/skill_manager_tool.py','tools/skill_manager_batch.py','tools/skill_linter.py','tools/skill_manager_guards.py','tests/tools/test_skill_manager_tool.py','tests/tools/test_skill_manage_batch.py','tests/tools/test_skill_linter.py']
inputs=[]
for rel in rels:
 p=RT/rel
 if not p.exists():continue
 b=RUN/'baseline/runtime'/rel;b.parent.mkdir(parents=True,exist_ok=True);b.write_bytes(p.read_bytes());out=RUN/'candidates/consumer'/rel;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(p.read_bytes());inputs.append({'source':str(p),'baseline':str(b),'candidate':str(out),'sha256':sha(p),'rel':rel})
(E/'consumer_sources.json').write_text(json.dumps(inputs,indent=2),encoding='utf-8',newline='\n')
adm=json.loads((E/'admission.json').read_text());bindings=[]
for it in adm['items']:
 role=it['role'];bindings.append({'workorder_id':it['binding']['workorder_id'],'taskspec_id':it['binding']['taskspec_id'],'base_head':it['binding']['base_head'],'cwd':it['binding']['writable_root'],'writer_scope_qualification_receipt':str(E/'qualification_receipt.json'),'writer_scope_qualification_digest':sha(E/'qualification_receipt.json'),'subject':next((x for x in subjects if x['role']==role),inputs if role=='CONSUMER' else 'frozen admitted candidates'),'writer':'Codex CLI opencode-go/deepseek-v4.1-flash','checker':'Codex CLI opencode-go/glm-5.3-flash','actual_binding_consumer':str(E/'run_lane.py'),'binding_ceiling':'existing typed TS/WO + per-round invocation binding, no canonical schema or acceptance token invented'})
(E/'execution_bindings.json').write_text(json.dumps(bindings,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
sys.path.insert(0,str(R/'src'));from hg_kseos.spine import SharedSpine;from hg_kseos.lifecycle import ProjectLifecycleController
lc=ProjectLifecycleController(SharedSpine(R/'var/shared-spine/hg-kseos.db'));state=lc.status(RUN.name)['state'];assert state=='WORKORDERS_ADMITTED';lc.transition(RUN.name,'EXECUTING',trigger='QUALIFIED_NATIVE_SCOPE_EXACT_SUBJECT_BOUND',workorder_refs=[x['workorder_id'] for x in bindings],evidence_refs=[str(E/'qualification_receipt.json'),str(E/'execution_bindings.json')]);print(json.dumps({'qualification':True,'candidate_inputs_prepared':True,'roles':[x['role'] for x in subjects],'runtime_source_files':len(inputs),'state':lc.status(RUN.name)['state']},indent=2))
