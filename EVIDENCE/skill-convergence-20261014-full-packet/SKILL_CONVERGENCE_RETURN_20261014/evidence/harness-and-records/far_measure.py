"""FAR measurement pass for the remediation ruling.

Measures, per role: how far the entry body shrank, how the reference population is shaped
(count, size bands), and how much of it is actually reachable — named by the main document or
by another reference. Reachability is what separates "topical depth" from the per-session-log
shape the linter warns about, so it is the number the ruling must rest on.
"""
import pathlib,json,re,datetime,collections
RUN=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014')
PAT=re.compile(r'references/[A-Za-z0-9._\-]+\.(?:md|py|json)')
LINTER_CAP_REFS=60; SOFT_BODY=24000; HARD=100000
out={'schema':'SKCV-FAR-MEASUREMENTS/1','observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'thresholds':{'body_soft_budget_chars':SOFT_BODY,'max_skill_content_chars':HARD,'references_warning_cap':LINTER_CAP_REFS,
   'source':'live tools/skill_linter.py lines 51,56,192: the 60-file rule is a warning named references-sprawl'},
 'roles':{},'claim_ceiling':'measurement of a frozen candidate generation; it supports an engineering ruling and grants no acceptance'}
for role,base in (('avr','adversarial-verification-rounds'),('hgk','hgk-governed-execution')):
    bdir=RUN/'baseline'/base; cdir=RUN/'candidates'/role/'skill'
    bmain=(bdir/'SKILL.md').read_text(encoding='utf-8'); cmain=(cdir/'SKILL.md').read_text(encoding='utf-8')
    def refs(d):
        return {p.relative_to(d).as_posix():p for p in d.rglob('*.md') if not any(x.startswith('_') for x in p.relative_to(d).parts)}
    br,cr=refs(bdir),refs(cdir)
    # reachability in the candidate: named by the main doc, else by some other reference, else unreachable
    named_main=set(PAT.findall(cmain))
    reach=collections.Counter(); unreachable=[]
    alltext={k:(v.read_text(encoding='utf-8',errors='replace') if v.stat().st_size<400_000 else '') for k,v in cr.items()}
    for k,v in cr.items():
        n='references/'+k.replace('references/','') if not k.startswith('references/') else k
        if n.replace('references/','references/') in {x for x in named_main}:
            reach['named_by_main_doc']+=1; continue
        if any((n in t or k in t) for kk,t in alltext.items() if kk!=k):
            reach['named_by_another_reference']+=1; continue
        reach['unreachable']+=1; unreachable.append((k,v.stat().st_size))
    bands=collections.Counter()
    for k,v in cr.items():
        s=v.stat().st_size
        bands['<400B' if s<400 else '400B-4KB' if s<4096 else '4KB-20KB' if s<20480 else '>20KB']+=1
    out['roles'][role]={'main_doc':{'baseline_chars':len(bmain),'candidate_chars':len(cmain),
        'delta_chars':len(cmain)-len(bmain),'pct_of_hard_cap':round(100*len(cmain)/HARD,1),
        'over_body_soft_budget':len(cmain)>SOFT_BODY},
      'references':{'baseline_files':len(br),'candidate_files':len(cr),
        'over_linter_cap':len(cr)>LINTER_CAP_REFS,'over_by':max(0,len(cr)-LINTER_CAP_REFS),
        'size_bands':dict(bands),'reachability':dict(reach),
        'unreachable_sample':sorted(unreachable,key=lambda x:-x[1])[:12],
        'unreachable_bytes':sum(s for _,s in unreachable)},
      'named_by_main_doc':sorted(named_main)}
(RUN/'evidence/postfreeze/far_measurements.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,default=str),encoding='utf-8',newline='\n')
for r,v in out['roles'].items():
    print(r,'main',v['main_doc']['candidate_chars'],'chars (',v['main_doc']['pct_of_hard_cap'],'% of hard cap )','| refs',v['references']['baseline_files'],'->',v['references']['candidate_files'],
          '| over cap by',v['references']['over_by'],'| bands',v['references']['size_bands'])
    print('   reach',v['references']['reachability'],'unreachable bytes',v['references']['unreachable_bytes'])
    print('   named in main doc:',len(v['named_by_main_doc']),v['named_by_main_doc'][:8])
