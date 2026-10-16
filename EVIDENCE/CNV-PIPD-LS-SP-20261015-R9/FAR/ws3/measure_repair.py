from pathlib import Path
import hashlib, json, shutil, subprocess, sys, os
S = Path('C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R9/FAR/ws3')
R = Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014')
OLD = Path('C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8')
C = R/'candidates/hgk/skill'
L = Path('C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/skills/software-development/hgk-governed-execution')
P = S/'repaired_candidate'
def h(b): return hashlib.sha256(b).hexdigest()
def inventory(root):
    return {p.relative_to(root).as_posix(): {'bytes':p.stat().st_size,'sha256':h(p.read_bytes())} for p in sorted(root.rglob('*')) if p.is_file()}
def put(name,obj): (S/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
S.mkdir(parents=True,exist_ok=True)
assert not P.exists(), 'Refusing to overwrite an existing experiment'
source_harness=OLD/'ws_a_skill_slim_regression.py'
H=S/source_harness.name
shutil.copyfile(source_harness,H)
assert H.read_bytes()==source_harness.read_bytes()
help_run=subprocess.run([sys.executable,'-B',str(H),'--help'],capture_output=True,text=True)
(S/'harness_help.txt').write_text(help_run.stdout+help_run.stderr,encoding='utf-8')
assert help_run.returncode==0
lm,cm=inventory(L),inventory(C)
def run(root,name):
    args=[sys.executable,'-B',str(H),'--subject',str(root),'--live',str(L),'--out',str(S/name)]
    r=subprocess.run(args,capture_output=True,text=True)
    (S/(name+'.stdout.txt')).write_text(r.stdout,encoding='utf-8')
    (S/(name+'.stderr.txt')).write_text(r.stderr,encoding='utf-8')
    assert r.returncode in (0,1),r.stderr
    data=json.loads((S/name).read_text(encoding='utf-8'))
    return data,{'args':args,'returncode':r.returncode}
before,bexec=run(C,'harness_before.json')
# Independent full-byte membership measurement, separately from harness.
corpus_files=[q for q in C.rglob('*.md') if q.is_file()]
corpus=[(q,q.read_bytes()) for q in corpus_files]
diffs=[]
for rel in sorted(set(lm)|set(cm)):
    if lm.get(rel)!=cm.get(rel):
        b=(L/rel).read_bytes() if rel in lm else None
        placements=[] if b is None else [{'path':str(q),'offset':data.find(b)} for q,data in corpus if b in data]
        diffs.append({'path':rel,'live':lm.get(rel),'candidate':cm.get(rel),'state':'candidate-only' if rel not in lm else 'absent' if rel not in cm else 'changed','live_bytes_verbatim_in_candidate_markdown':placements,'cache_artifact':'__pycache__' in rel.split('/')})
missing=[x for x in diffs if x['live'] and x['path'].startswith('references/') and not x['cache_artifact'] and not x['live_bytes_verbatim_in_candidate_markdown']]
# Scan the specified archival roots; report ALL whole-file or embedded exact-byte copies.
needles={x['path']:(L/x['path']).read_bytes() for x in missing}
locations={rel:[{'path':str(L/rel),'match':'whole-file','offset':0,'container_bytes':len(b),'container_sha256':h(b)}] for rel,b in needles.items()}
scan_roots=[R,OLD/'WS_A']
scanned=0
errors=[]
for root in scan_roots:
    if not root.exists():
        errors.append({'path':str(root),'error':'missing scan root'})
        continue
    paths=[]
    for directory, dirs, files in os.walk(root, followlinks=False, onerror=lambda e: errors.append({'path':str(e.filename),'error':str(e)})):
        paths.extend(Path(directory)/name for name in files)
    for q in sorted(paths):
        if not q.is_file(): continue
        try:
            size=q.stat().st_size
            if size<min(map(len,needles.values())): continue
            data=q.read_bytes(); scanned+=1
            for rel,b in needles.items():
                off=data.find(b)
                if off>=0:
                    locations[rel].append({'path':str(q),'match':'whole-file' if data==b else 'embedded-verbatim','offset':off,'container_bytes':len(data),'container_sha256':h(data)})
        except OSError as e: errors.append({'path':str(q),'error':str(e)})
shutil.copytree(C,P)
repairs=[]
for x in missing:
    rel=x['path']; src=L/rel; dest=P/rel
    dest.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(src,dest)
    repairs.append({'path':rel,'source':str(src),'before':cm.get(rel),'after':{'bytes':dest.stat().st_size,'sha256':h(dest.read_bytes())},'original_byte_locations':locations[rel]})
pm=inventory(P)
actual_changed=[r for r in sorted(set(cm)|set(pm)) if cm.get(r)!=pm.get(r)]
assert actual_changed==sorted(x['path'] for x in repairs)
assert inventory(L)==lm,'Live drift detected'
assert inventory(C)==cm,'Candidate drift detected'
after,aexec=run(P,'harness_after.json')
assert inventory(P)==pm,'Harness mutated repaired tree'
assert inventory(L)==lm and inventory(C)==cm,'Source drift detected'
main=pm['SKILL.md']['bytes']
result={'claim_ceiling':'LOCAL / candidate-only; not acceptance','live':str(L),'candidate':str(C),'repaired':str(P),'harness':{'path':str(H),'sha256':h(H.read_bytes()),'copied_verbatim':True,'before_execution':bexec,'after_execution':aexec,'metadata_bug':'Raw subject_live field is evaluated before check() applies --live, so it incorrectly names AVR. The explicit --live arguments and HGK identity/live byte count demonstrate effective HGK binding. Instrument unchanged.'},'before_verdicts':{k:v['verdict'] for k,v in before['checks'].items() if k.startswith('C')},'after_verdicts':{k:v['verdict'] for k,v in after['checks'].items() if k.startswith('C')},'before_overall':before['verdict'],'after_overall':after['verdict'],'live_manifest':lm,'candidate_manifest':cm,'repaired_manifest':pm,'file_by_file_differences':diffs,'non_surviving_live_reference_files':missing,'minimal_repair_set':repairs,'actual_candidate_to_repaired_changed_paths':actual_changed,'archive_scan':{'roots':[str(x) for x in scan_roots],'files_read':scanned,'errors':errors},'source_trees_unchanged':True,'slim_benefits':{'live_main_bytes':lm['SKILL.md']['bytes'],'repaired_main_bytes':main,'main_unchanged_from_candidate':pm['SKILL.md']==cm['SKILL.md'],'main_under_100000':main<100000,'main_reduction_bytes':lm['SKILL.md']['bytes']-main,'main_reduction_percent':100*(lm['SKILL.md']['bytes']-main)/lm['SKILL.md']['bytes'],'repair_added_bytes':sum(x['after']['bytes']-(x['before']['bytes'] if x['before'] else 0) for x in repairs)},'scope_note':'All files inventoried; cache artifacts shown but excluded from instructional-loss classification as in C6. No deletion/cleanup in repair. Full main-file raw-byte survival is not asserted: C4 checks lines >40 bytes, C6 checks full reference bytes.'}
put('repair_measurements.json',result)
lines=['# R9-0 FAR EXPERIMENT: minimal scratch repair','', '**Claim ceiling: LOCAL / candidate-only; not acceptance.**','','## Outcome',f"- Before: {before['verdict']}; after: {after['verdict']}.",'- Exact per-check verdicts (verbatim strings from raw harness JSON):','','| Check | Before | After |','|---|---|---|']
for k in sorted(result['before_verdicts']): lines.append(f"| {k} | {result['before_verdicts'][k]} | {result['after_verdicts'][k]} |")
lines+=['','## Minimal repair set','']
for x in repairs:
    lines += [f"- `{x['path']}`: source `{x['source']}`; {x['after']['bytes']} bytes; SHA256 `{x['after']['sha256']}`.",f"  Original bytes recovered at {len(x['original_byte_locations'])} exact whole-file/embedded locations (full list in measurements JSON)."]
lines+=['','## Measurements and interpretation',f"- Main file: {lm['SKILL.md']['bytes']} live bytes -> {main} candidate/repaired bytes; unchanged by repair; below 100,000.",f"- Repair adds {result['slim_benefits']['repair_added_bytes']} net bytes; only the listed two paths change.",f"- C6 before: {json.dumps(before['checks']['C6_reference_coverage'],ensure_ascii=False)}",f"- C6 after: {json.dumps(after['checks']['C6_reference_coverage'],ensure_ascii=False)}",'- No C1-C6 failures remain if overall above is PASS. Reference soft-cap warning remains; not a hard gate.', '- Losslessness: all live instructional reference files now survive byte-identical or fully embedded; C4 also finds no lost main-file lines >40 bytes. These are the harness-defined properties, not a stronger whole-main-byte reconstruction proof.', '- Full path/size/SHA256 manifests and all file differences (including caches) are in repair_measurements.json.', '- Original byte availability is confirmed from live and the specified archival roots. Exact matching was measured rather than inferred from names.', '- Source candidate and live manifests were rehashed and unchanged after experiment.', '- Raw harness_before.json and harness_after.json are retained, with invocation/stdout/stderr evidence.', '', '## Instrument caveat', result['harness']['metadata_bug'], '', '## Guarded apply assessment', '- The repaired candidate clears the reproduced C6 blocker and passes all six local checks; it is justified as the candidate for a separately authorized guarded-apply procedure, not as permission to apply now.', '- Before any actual apply: rebind/re-hash live inputs, preserve a pre-image, exclude bytecode caches from publication, exercise rollback, and rerun the gate on the landed tree. Independent acceptance remains separate.', '', '## NON-CLAIMS', '- No canonical/live tree was modified, and no apply, promotion, release or acceptance occurred.', '- This worker performs a local scratch experiment, not an independent acceptance lane.', '- No network or git write command was used. Explicit task writes are confined to ws3; tool-runtime bookkeeping is outside this experiment\'s control.', '- Existing harness C5 implementation is limited: some controls test primitive predicates rather than full end-to-end negative fixtures. A C5 PASS is reported as the instrument returned it, not as broader adversarial validation.', '- No claim that reference count is below its soft cap; no claim that cache cleanup was performed.', '- Archival byte search is bounded to the supplied roots; whole-file or embedded exact matches are listed, not an exhaustive whole-disk search.']
(S/'repair_report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({'before':result['before_verdicts'],'after':result['after_verdicts'],'repairs':[{k:v for k,v in x.items() if k!='original_byte_locations'} for x in repairs],'locations':{k:len(v) for k,v in locations.items()},'scan_errors':errors,'main_bytes':main,'actual_changed':actual_changed,'files_created':[str(x) for x in S.iterdir()]},indent=2))
