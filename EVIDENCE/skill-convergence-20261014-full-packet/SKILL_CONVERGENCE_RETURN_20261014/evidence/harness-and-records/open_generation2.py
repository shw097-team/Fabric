"""Close generation 1 and open generation 2.

Runs after the remediation lanes have written their candidate edits: re-freezes the subject so the
manifest describes the new bytes, then stamps the new digest into the two checker briefs in place of the
placeholder, so the checker lanes bind the generation they are actually reading.

It refuses to stamp a brief whose placeholder is already gone unless --force, so a stale digest cannot be
quietly reused.
"""
import pathlib,json,subprocess,sys
RUN=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014')
PY='C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe'
FORCE='--force' in sys.argv
freeze=subprocess.run([PY,str(RUN/'evidence/freeze_subject.py')],cwd=str(RUN),capture_output=True,text=True,encoding='utf-8',errors='replace')
print(freeze.stdout.strip() or freeze.stderr.strip()[-400:])
m=json.loads((RUN/'evidence/subject_manifest.json').read_text(encoding='utf-8'))
digest=m['tree_digest'];count=m['file_count']
stamped=[]
for name in ('verify-5.md','security-3.md'):
    p=RUN/'evidence/prompts'/name
    t=p.read_text(encoding='utf-8')
    if '__GEN2_DIGEST__' in t:
        p.write_text(t.replace('__GEN2_DIGEST__',digest),encoding='utf-8',newline='\n');stamped.append(name)
    elif not FORCE:
        raise SystemExit(f'{name} has no placeholder: refusing to stamp a possibly stale digest into it (use --force if intended)')
gen=json.loads((RUN/'evidence/postfreeze/generations.json').read_text(encoding='utf-8')) if (RUN/'evidence/postfreeze/generations.json').exists() else {'schema':'SKCV-GENERATIONS/1','generations':[]}
gen['generations'].append({'generation':2,'file_count':count,'tree_digest':digest,
  'why':'generation 2 carries three bounded remediations: the HGK reference-sprawl pilot merge, the candidates/apply timeout-capture candidate patch, and the repair of the false stub signal in evidence/check_topic_batch.py',
  'generation_1':{'file_count':374,'tree_digest':'9b68418bcbfd230d43d6525752a09d156b37fb31fb214eacaf3b5c77b616936cb',
    'status':'reported on by two GLM checker lanes; superseded as a binding, not deleted'}})
(RUN/'evidence/postfreeze/generations.json').write_text(json.dumps(gen,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
print(json.dumps({'generation':2,'file_count':count,'tree_digest':digest,'briefs_stamped':stamped},indent=1))
