#!/usr/bin/env python3
"""Offline independent-source-anchored PIPD document package checker.
Never treats its own index as trust. Requires a detached SHA received from a different
trusted channel. Does not emit PI_READY, ECP, independent acceptance, or effects.
Can materialize into NEW isolated directory with temp+atomic rename.
"""
import argparse, hashlib, json, os, pathlib, re, shutil, sys, tempfile

SHA=re.compile(r'^[0-9a-f]{64}$')
HERE=pathlib.Path(__file__).resolve()
def h(b): return hashlib.sha256(b).hexdigest()
def compact(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
class Fail(Exception):
    def __init__(self,code,why):self.code=code;self.why=why

def unique(rows, key, expected=None):
    ids=[v[key] for v in rows]
    if len(ids)!=len(set(ids)):raise Fail(20,'DUPLICATE:'+key)
    if expected is not None and set(ids)!=set(expected):raise Fail(20,'ID_SET:'+key)
    return ids

def parse_package(path):
    b=path.read_bytes(); b.decode('utf-8','strict')
    # One namespace: append-only v1 full source is inert and MUST not be parsed as v2 slots.
    cut=b'\n<!-- V1_WHOLE_DOCUMENT_BYTES_BEGIN sha256='
    if b.count(cut)!=1:raise Fail(20,'LEGACY_BOUNDARY_MISSING_OR_DUPLICATE')
    pre,legacy=b.split(cut,1)
    line_end=legacy.find(b' -->\n')
    if line_end<0:raise Fail(20,'LEGACY_HEADER')
    declared=legacy[:line_end].decode('ascii')
    raw_legacy=legacy[line_end+5:]
    end=b'\n<!-- V1_WHOLE_DOCUMENT_BYTES_END -->\n'
    if not raw_legacy.endswith(end):raise Fail(20,'LEGACY_END')
    raw_legacy=raw_legacy[:-len(end)]
    if h(raw_legacy)!=declared:raise Fail(20,'LEGACY_BYTES_TAMPER')
    pat=re.compile(rb'(?m)^```json SLOT:([^\n]+)\n(.*?)^```$',re.S|re.M)
    found=list(pat.finditer(pre));d={};raw={}
    for m in found:
        name=m.group(1).decode('ascii');data=m.group(2)
        if name in d:raise Fail(20,'DUPLICATE_SLOT:'+name)
        try:obj=json.loads(data)
        except Exception as e:raise Fail(20,'BAD_JSON:'+name+':'+str(e))
        d[name]=obj;raw[name]=data
    if len(d)!=27:raise Fail(20,'SLOT_NUMBER')
    expected=[f'{i:02}_' for i in range(1,28)]
    if any(sum(k.startswith(prefix) for k in d)!=1 for prefix in expected):raise Fail(20,'SLOT_SEQUENCE')
    index=d['01_PKG_INDEX.json'];manifest=index['slot_manifest']
    if index['version']!='2.0.0' or index['artifact_slots']!=27 or set(manifest)!=set(d)-{'01_PKG_INDEX.json'}:raise Fail(20,'INDEX_DENOM_OR_VERSION')
    for k in manifest:
        if len(raw[k])!=manifest[k]['bytes'] or h(raw[k])!=manifest[k]['sha256']:raise Fail(20,'SLOT_BYTES:'+k)
    if index['supersedes']['sha256']!=declared:raise Fail(20,'SUPERSEDES_HASH')
    return d,raw,b,raw_legacy

def semantic(d,root):
    # Source bytes for source-locked acceptance MUST be physically readable, not just named in this MD.
    root=root.resolve(strict=True)
    src=d['02_SOURCE_BINDINGS.json']; records=src['physical_sources']
    if not records or len(records)!=d['01_PKG_INDEX.json']['required_source_count']:raise Fail(20,'SOURCE_DENOM')
    unique(records,'filename')
    sources={}
    for r in records:
        name=r['filename'];q=pathlib.PurePosixPath(name)
        if q.is_absolute() or '..' in q.parts or len(q.parts)!=1:raise Fail(20,'SOURCE_ESCAPE')
        f=root/name
        if not f.is_file():raise Fail(30,'SOURCE_PHYSICAL_MISSING:'+name)
        if f.is_symlink() or not f.resolve().is_relative_to(root):raise Fail(20,'SOURCE_LINK_ESCAPE:'+name)
        b=f.read_bytes()
        if h(b)!=r['sha256'] or len(b)!=r['bytes']:raise Fail(20,'SOURCE_SHA_MISMATCH:'+name)
        txt=b.decode('utf-8','strict')
        if len(txt.splitlines())!=r['lines']:raise Fail(20,'SOURCE_LINE_DRIFT:'+name)
        sources[name]=txt
    names=list(sources)
    def source_with(x):
        o=[v for k,v in sources.items() if x in k]
        if len(o)!=1:raise Fail(30,'SOURCE_REQUIRED:'+x)
        return o[0]
    orig=source_with('v1.0.0_DOCUMENT_CANDIDATE_2026-10-15.md')
    bl=source_with('Blueprint_v1.1.0_AUDIT_PATCHED')
    bp=source_with('Global_Engineering_Blueprint_v2.0.0_PATCHED')
    def registries(s):
        return {n:json.loads(body) for n,body in re.findall(r'(?ms)^```json ([A-Z0-9_]+)\n(.*?)^```$',s)}
    r=registries(bl)
    old={n:json.loads(body) for n,body in re.findall(r'(?ms)^```json SLOT:([^\n]+)\n(.*?)^```$',orig)}
    # Namespace-qualified historical source comparison is mandatory; do not trust regenerated manifest alone.
    if d['08_DOMAIN_PARENT_64.json']!=r['RQ_REGISTRY']:raise Fail(20,'SOURCE_PARENT_SEMANTICS')
    if d['09_LEGACY_TESTS_28.json']!=r['T_REGISTRY']:raise Fail(20,'SOURCE_LEGACY_ORACLE_SEMANTICS')
    if d['10_PARENT_TRACE_64.json']!=r['TRACE_REGISTRY']:raise Fail(20,'SOURCE_BRIDGE_SEMANTICS')
    if d['13_TECH_SOURCE_342.json']!=old['13_TECH_LEDGER.json']:raise Fail(20,'SOURCE_TECH_SOURCE_TRUTH')
    if d['11_WP_09.json']!=old['11_WP_EXECUTION_PLAN.json']:raise Fail(20,'SOURCE_WP_APPROVAL_POLICY')
    if d['03_INTENT_PROJECTION.json']['content_hash']!=old['03_INTENT_LOCAL.json']['content_hash'] or d['03_INTENT_PROJECTION.json']['sources']!=old['03_INTENT_LOCAL.json']['sources']:raise Fail(20,'INTENT_ID_OR_SOURCE_DRIFT')
    p=d['04_PROFILE_PROJECTION.json'];ref=old['04_PROFILE_LOCAL.json']
    if p['profile']!='ASSURED' or p['requested_profile']!='ASSURED' or p['artifact_depth']!='L4_FAILURE_RECOVERY' or any(p.get(k)!=ref.get(k) for k in ref):raise Fail(20,'PROFILE_DOWNGRADE_OR_ABI')
    pi=d['05_PI_PROJECTION.json'];fixed=old['05_PI_LOCAL.json']
    if pi['acceptance']!={'mode':'bound','oracle_source':'DOC-03 DOMAIN_ORACLES'} or any(pi.get(k)!=fixed[k] for k in fixed):raise Fail(20,'PI_ORACLE_ABI_OR_IDENTITY')
    if len(d['06_PI_CONTRACTS_18.json'])!=18 or len(d['07_PD_CONTRACTS_10.json'])!=10:raise Fail(20,'PI_PD_DENOM')
    for section,items,key,source_map in [('PI',d['06_PI_CONTRACTS_18.json'],'06_PI_CANONICAL_MAP.json',old['06_PI_CANONICAL_MAP.json']),('PD',d['07_PD_CONTRACTS_10.json'],'07_PD_CANONICAL_MAP.json',old['07_PD_CANONICAL_MAP.json'])]:
        unique(items,'id',[f'{section}-{i:02}' for i in range(1,len(source_map)+1)])
        for x,y in zip(items,source_map):
            if x['id']!=y['id'] or x['title']!=y['title'] or x['normative_anchor']!=y['normative_anchor']:raise Fail(20,section+'_CONTRACT_SOURCE_DRIFT')
            if h(x['prose_body'].encode())!=x['prose_sha256'] or len(x['prose_body'])<150:raise Fail(20,section+'_BODY_MISSING')
            n=int(x['id'].split('-')[-1]);marker=(f'### 6.{n:02}｜' if section=='PI' else f'### 8.{n:02} ')
            if x['prose_body'] not in bl or not x['prose_body'].startswith(marker):raise Fail(20,section+'_SOURCE_BODY_MISMATCH')
    # Exhaustive parent+child source-anchored graph; no orphan/count-only acceptance.
    parents=d['08_DOMAIN_PARENT_64.json'];child=d['16_CHILD_OBLIGATIONS_129.json'];edges=d['17_CHILD_GRAPH_129.json'];testplan=d['19_ORACLE_TESTPLAN_129.json']
    unique(parents,'id',[f'RQ{i:02}' for i in range(1,65)])
    unique(child,'child_id',[cid for row in parents for cid in row['children']]);unique(edges,'child_id',[x['child_id'] for x in child]);unique(testplan,'child_id',[x['child_id'] for x in child])
    pm={x['id']:x for x in parents};em={x['child_id']:x for x in edges};tm={x['child_id']:x for x in testplan}
    bp_lines=bp.splitlines()
    for q in parents:
        if q['source_line']>len(bp_lines) or h(bp_lines[q['source_line']-1].encode())!=q['source_line_sha256']:raise Fail(20,'PARENT_LINE_SOURCE_HASH:'+q['id'])
        if q['id']=='RQ06' and ('T22' in q['verification']['linked_legacy_tests']):raise Fail(20,'RQ06_T22_BAD_ORACLE')
    for x in child:
        if set(x)!={'child_id','parent_id','domain_id','ordinal','source','source_obligation_verbatim','semantic_owner','plugin_axis','spec','acceptance','oracle','fixture_design','evidence_expectation','deliverable','gate','pd_binding','state'}:raise Fail(20,'CHILD_UNDECLARED_FIELDS')
        if x['state']!='DESIGN_READY_NOT_AUTHORIZED' or x['oracle']['current_execution']!='NOT_RUN' or x['evidence_expectation']['type']!='RAW_RECEIPT':raise Fail(20,'CHILD_FAKE_STATUS:'+x['child_id'])
        p=pm[x['parent_id']];id=x['child_id'];i=x['ordinal']-1
        if id not in p['children'] or i<0 or id!=p['children'][i] or x['source_obligation_verbatim']!=p['child_obligations'][i]:raise Fail(20,'CHILD_SEMANTIC_ORPHAN:'+id)
        if x['source']['line_sha256']!=p['source_line_sha256'] or x['source']['parent_registry_sha256']!=h(compact(p)):raise Fail(20,'CHILD_SOURCE_DRIFT:'+id)
        if x['spec']['parent_expected']!=p['acceptance']['expected'] or x['acceptance']['parent_case_expected']!=p['acceptance']['expected'] or x['acceptance']['parent_case_negative']!=p['acceptance']['negative']:raise Fail(20,'CHILD_EXPECTED_DRIFT:'+id)
        if x['spec']['observable_key']!=p['spec']['output']+f'__S{x["ordinal"]:02}' or x['spec']['output_type']!=p['spec']['datatype']:raise Fail(20,'CHILD_OUTPUT_TYPE_OR_KEY:'+id)
        if x['gate']!=p['gate'] or x['plugin_axis']!=p['plugin_req_id']:raise Fail(20,'CHILD_GATE_OR_AXIS:'+id)
        if x['oracle']['runner_sha256'] is not None or x['oracle']['independent_checker_receipt'] is not None or x['pd_binding'] is not None:raise Fail(20,'FAKE_RUNTIME_CHILD_RECEIPT:'+id)
        e=em[id];nodes=e['ordered_nodes']
        names=[v[0] for v in nodes]
        expected_links=[('SRC',f'BP2@{p["source_line"]}'),('INTENT',p['plugin_req_id']),('REQ',p['domain_atom_id']),('SPEC',f'SPEC-{id}'),('ACC',f'ACC-{id}'),('TEST',x['oracle']['test_id']),('ORACLE',x['oracle']['id']),('EE',x['evidence_expectation']['id']),('DEL',x['deliverable']),('GATE',p['gate']),('PD_BINDING','NOT_BOUND')]
        if nodes!=[list(a) for a in expected_links] or e['parent_id']!=p['id'] or e['source_registry_hash']!=h(compact(p)) or e['pd_binding_status']!='NOT_BOUND':raise Fail(20,'CHILD_TRACE_INVALID:'+id)
        tp=tm[id]
        if tp['goal']!=x['source_obligation_verbatim'] or tp['test_id']!=x['oracle']['test_id'] or tp['runner']!='UNBOUND_OWNER_PIN_REQUIRED' or tp['positive_receipt'] is not None or tp['negative_receipt'] is not None or tp['positive_oracle']!=x['acceptance']['positive_predicate'] or tp['negative_oracle']!=x['acceptance']['negative_predicate']:raise Fail(20,'CHILD_ORACLE_TESTPLAN_INVALID:'+id)
    t=d['09_LEGACY_TESTS_28.json'];unique(t,'id',[f'T{i:02}' for i in range(1,29)])
    for x in t:
        if x['fixture_positive']==x['fixture_negative']:raise Fail(20,'TEST_POS_EQ_NEG:'+x['id'])
        if x['source_line']>len(bp_lines) or h(bp_lines[x['source_line']-1].encode())!=x['source_line_sha256']:raise Fail(20,'TEST_SOURCE_HASH:'+x['id'])
    tech=d['13_TECH_SOURCE_342.json'];a=d['18_TECH_ADMISSION_342.json'];unique(a,'key');m={x['key']:x for x in a}
    dims=[('bp2_38','BP2_38',38),('pipd_layer_a_22','PIPD_LAYER_A_22',22),('pipd_doc07_donor_144','PIPD_DOC07_144',144),('pipd_doc03_inventory_130','PIPD_DOC03_130',130),('canonical_workflows_8','PIPD_WORKFLOWS_8',8)]
    if len(a)!=342:raise Fail(20,'TECH_TOTAL')
    for group,ns,n in dims:
        if len(tech[group])!=n:raise Fail(20,'TECH_DENOM:'+group)
        for item in tech[group]:
            key=ns+'/'+item['id'];y=m.get(key)
            if not y:raise Fail(20,'TECH_ID_ORPHAN:'+key)
            name=item.get('name') or item.get('capability') or item['id'];disp=item.get('source_disposition') or item.get('treatment') or 'NOT_BOUND_BY_SOURCE'
            if y['source_name']!=name or y['source_disposition']!=disp or y['owner_approved_terminal_disposition']!='UNBOUND' or y['live_installed'] is not False or y['permission']!='NONE_GRANTABLE_FROM_DOCUMENT':raise Fail(20,'TECH_FALSE_ADMISSION_OR_NAME:'+key)
    gate=d['14_GATES_8.json'];unique(gate,'id',['G-'+a for a in 'ABCDEFGH'])
    if gate!=r['GATE_REGISTRY']:raise Fail(20,'GATE_SOURCE_DRIFT')
    for row in gate:
        if row['pass_claim']!='NOT_EXECUTED' or row['live_runner']!='UNBOUND_OWNER_PIN_REQUIRED':raise Fail(20,'GATE_FAKE_PASS:'+row['id'])
    fw=d['12_CLAIM_CEILING.json'];allowed_claim_keys={'schema','all_canonical_achievements','document_grade','source_authority','pi_ready','predev_ready','execution_admitted','independent_pass','publication_approved','released','production_verified','runtime_qualified','owner_approval','AO_receipt','admission_token','independent_checker_receipt','real_repo_context','release_gate','forbidden_claims_without_authority','legacy_claims'}
    if set(fw)!=allowed_claim_keys or fw['source_authority']!='BLOCKED_A1_A3' or fw['document_grade']!='CANDIDATE_MATERIALIZED' or fw['all_canonical_achievements'] is not None:raise Fail(20,'CLAIM_UNDECLARED_OR_EXTRA_GRANT')
    blocked=['pi_ready','predev_ready','execution_admitted','independent_pass','publication_approved','released','production_verified','runtime_qualified']
    if any(fw.get(k) is not False for k in blocked):raise Fail(20,'CLAIM_FALSE_PROMOTION')
    if fw['release_gate']!='FAIL_CLOSED' or fw['owner_approval'] is not None or fw['AO_receipt'] is not None or fw['independent_checker_receipt'] is not None:raise Fail(20,'CLAIM_EXTRA_GRANT')
    if fw['legacy_claims']!=old['12_CLAIM_FIREWALL.json']:raise Fail(20,'CLAIM_LEGACY_DRIFT')
    repo=src['repo_mirror']
    orig_repo=old['02_SOURCE_INDEX.json']['repo_mirror_snapshot']
    # historical mirror observation; changed = new requalification, not self-authorized update.
    if repo['main_sha']!='266f8d65cf9b21c3b37c1c243946a5c828cf973b' or repo['workflow_files']!=0 or repo['actions_runs']!=0 or repo['approval_list']!='PROPOSAL':raise Fail(20,'FAKE_GITHUB_REPO_SNAPSHOT')
    testcontracts=d['22_FULL_221_TEST_CONTRACTS.json']
    if len(d['20_FULL_AUDIT_FINDINGS_24.json'])!=24 or len(d['21_HOSTILE_MUTATIONS_18.json'])!=18 or len(testcontracts)!=221:raise Fail(20,'AUDIT_TEST_DENOM')
    unique(testcontracts,'id',[x['id'] for x in parents]+[x['child_id'] for x in child]+[x['id'] for x in t])
    cm={x['id']:x for x in testcontracts}
    for q in parents:
        z=cm[q['id']]
        if z['expected']!=q['acceptance']['expected'] or z['negative']!=q['acceptance']['negative'] or z['runner'] is not None:raise Fail(20,'PARENT_TEST_CONTRACT_MISMATCH:'+q['id'])
    for q in child:
        z=cm[q['child_id']]
        if z['expected']!=q['source_obligation_verbatim'] or z['negative']!=q['acceptance']['negative_predicate'] or z['runner'] is not None:raise Fail(20,'CHILD_TEST_CONTRACT_MISMATCH:'+q['child_id'])
    for q in t:
        z=cm[q['id']]
        if z['expected']!=q['fixture_positive'] or z['negative']!=q['fixture_negative'] or z['runner'] is not None:raise Fail(20,'LEGACY_TEST_CONTRACT_MISMATCH:'+q['id'])
    unique(d['20_FULL_AUDIT_FINDINGS_24.json'],'id');unique(d['21_HOSTILE_MUTATIONS_18.json'],'id',[f'M{i:02}' for i in range(1,19)])
    plug=d['23_PLUGIN_TYPED_HANDOFF_8.json']
    expected_skills=['pipd-route-intake','pipd-authority-source','pipd-profile-tailor','pipd-pi-compile','pipd-pd-bind','pipd-execution-contract','pipd-assurance-tqaep','pipd-package-project']
    if [x['skill'] for x in plug]!=expected_skills or any(x['vendor_receipt'] is not None or x['typed_io_status']!='CONTRACT_READ_NOT_VENDOR_EMITTED' for x in plug):raise Fail(20,'PLUGIN_VENDOR_OUTPUT_FORGERY')
    w=d['24_WIRING_AND_LIVE_BLOCKERS.json']
    if w['G1_fresh'] is not False or w['owner_publication_allowlist']!='PROPOSAL' or w['github_workflows']!=0 or w['actual_live_test_runners']!=0 or w['RepoContext'] is not None:raise Fail(20,'PLUGIN_OR_G1_FALSE')
    # Raw whole-body original source provenance protected by detached SHA and exact byte-inclusive appended text.
    return {'sources_rehashed':len(records),'parent_semantic':64,'child_semantic':129,'historic_test_semantic':28,'technology_admissions':342,'runtime_evidence':'MISSING','claim':'AUTHOR_SIDE_OFFLINE_ONLY'}

def materialize(d,raw,dest):
    dest=dest.absolute();parent=dest.parent
    if dest.exists() or dest.is_symlink() or not parent.is_dir():raise Fail(40,'DEST_MUST_NOT_EXIST_PARENT_DIRECTORY_REQUIRED')
    if parent.is_symlink():raise Fail(40,'DEST_PARENT_SYMLINK')
    if any((v/'.git').exists() for v in [parent,*parent.parents]):raise Fail(40,'GIT_TREE_STAGING_FORBIDDEN')
    tmp=None
    try:
        tmp=pathlib.Path(tempfile.mkdtemp(prefix='.pipd-v2-staging-',dir=parent))
        for label,body in raw.items():
            q=tmp/label
            fd=os.open(str(q),os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
            try:
                with os.fdopen(fd,'wb') as f:f.write(body);f.flush();os.fsync(f.fileno())
            except Exception:
                if not os.path.exists(q):os.close(fd)
                raise
            if h(q.read_bytes())!=h(body):raise Fail(40,'STAGING_BYTE_MISMATCH')
        os.rename(tmp,dest)
        tmp=None
        if hasattr(os,'O_DIRECTORY'):
            fd=os.open(str(parent),os.O_DIRECTORY)
            try:os.fsync(fd)
            finally:os.close(fd)
    except Fail:raise
    except Exception as err:raise Fail(40,'STAGING_IO_FAIL:'+str(err))
    finally:
        if tmp and tmp.exists():shutil.rmtree(tmp)
    return len(raw)

def main():
    p=argparse.ArgumentParser();p.add_argument('--doc',required=True);p.add_argument('--source-root');p.add_argument('--trusted-package-sha256');p.add_argument('--check',action='store_true');p.add_argument('--materialize',action='store_true');p.add_argument('--out');a=p.parse_args()
    try:
        if not a.trusted_package_sha256 or not SHA.fullmatch(a.trusted_package_sha256):raise Fail(30,'MISSING_EXTERNAL_OWNER_APPROVED_LOCK')
        db=pathlib.Path(a.doc).read_bytes()
        if h(db)!=a.trusted_package_sha256:raise Fail(20,'TRUSTED_PACKAGE_SHA_MISMATCH')
        d,raw,_,old=parse_package(pathlib.Path(a.doc))
        if not a.source_root:raise Fail(30,'MISSING_PHYSICAL_SOURCE_ROOT')
        report=semantic(d,pathlib.Path(a.source_root))
        if a.materialize:
            if not a.out:raise Fail(40,'MISSING_STAGING_OUT')
            report['extracted']=materialize(d,raw,pathlib.Path(a.out))
        print(json.dumps({'verdict':'AUTHOR_SIDE_OFFLINE_SOURCE_AND_LOCK_CHECK_ONLY','report':report,'official_release':'FAIL_CLOSED'},ensure_ascii=False));return 0
    except Fail as e:
        print(json.dumps({'verdict':'FAIL_CLOSED','reason':e.why,'exit':e.code},ensure_ascii=False));return e.code
    except Exception as e:
        print(json.dumps({'verdict':'FAIL_CLOSED','reason':type(e).__name__+':'+str(e),'exit':40},ensure_ascii=False));return 40
if __name__=='__main__':sys.exit(main())
