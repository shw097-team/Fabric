"""Second half of the independent batch-1 check: the skill names its references in backticks,
not markdown links, so link resolution must be tested against that convention.
Verifies every named path resolves, and locates the baseline references that the rewritten
main doc no longer names.
"""
import pathlib,json,re,hashlib
RUN=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014')
C=RUN/'candidates/avr';B=RUN/'baseline/adversarial-verification-rounds'
PAT=re.compile(r'references/[A-Za-z0-9._\-]+\.md')
md=(C/'skill/SKILL.md').read_text(encoding='utf-8',errors='replace')
bmd=(B/'SKILL.md').read_text(encoding='utf-8',errors='replace')
named=sorted(set(PAT.findall(md)));bnamed=sorted(set(PAT.findall(bmd)))
resolve={n:(C/'skill'/n).exists() for n in named}
allsrc=(C/'skill/references'/'topic-source-remainder.md').read_text(encoding='utf-8',errors='replace')
rem=json.loads((C/'evidence_remainder_index.json').read_text(encoding='utf-8')) if (C/'evidence_remainder_index.json').exists() else None
not_named=[n for n in bnamed if n not in named]
covered={n:(n in allsrc) for n in not_named}
phys={p.relative_to(C/'skill').as_posix() for p in (C/'skill/references').rglob('*') if p.is_file()}
out={'schema':'SKCV-INDEP-REFERENCE-CONVENTION-CHECK/1',
 'convention':'references are named in backticks like `references/x.md`; the doc contains no markdown links, so a markdown-link check is vacuous here and is reported as such',
 'named_in_candidate_main_doc':named,'all_named_paths_resolve':all(resolve.values()),'per_path_exists':resolve,
 'named_in_baseline_main_doc':bnamed,
 'baseline_refs_no_longer_named_in_main_doc':not_named,
 'those_present_verbatim_in_topic_source_remainder':covered,
 'physical_reference_files_in_candidate':sorted(phys),
 'counts':{'candidate_named':len(named),'baseline_named':len(bnamed),'candidate_physical':len(phys),
   'baseline_physical':len([p for p in (B/'references').rglob('*') if p.is_file()])},
 'claim_ceiling':'structure and resolvability only for this batch; it does not judge the remaining theme groups and grants no acceptance'}
print(json.dumps(out,ensure_ascii=False,indent=1))
