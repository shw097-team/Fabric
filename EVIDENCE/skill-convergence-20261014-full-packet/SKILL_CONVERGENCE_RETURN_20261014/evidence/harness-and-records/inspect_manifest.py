import json,pathlib,collections
RUN=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014')
d=json.loads((RUN/'evidence/subject_manifest.json').read_text(encoding='utf-8'))
print('keys',list(d.keys()))
print('meta',json.dumps({k:v for k,v in d.items() if k!='files'},ensure_ascii=False)[:1400])
c=collections.Counter()
for f in d['files']:
 p=f['path'].replace(chr(92),'/')
 c['/'.join(p.split('/')[-4:])[:0] or '/'.join(p.split('/')[:4])]+=1
print('included_groups_top4')
for k,v in c.most_common(16):print('  ',k,v)
print('sample_included')
for f in d['files'][:8]:print('   ',f['path'].split('SKILL-CONVERGENCE-20261014')[-1])
ex=d.get('excluded') or d.get('excluded_globs') or []
print('excluded_type',type(ex).__name__,'n',len(ex) if hasattr(ex,'__len__') else '?')
for x in list(ex)[:14]:print('   ',str(x).split('SKILL-CONVERGENCE-20261014')[-1])
