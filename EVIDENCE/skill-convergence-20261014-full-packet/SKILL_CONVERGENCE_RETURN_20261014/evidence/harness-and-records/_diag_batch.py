import subprocess,pathlib
R='C:/Projects/Agent_Workspace/Fabric'
tree=[t for t in subprocess.run(['git','-C',R,'ls-tree','-r','--name-only','HEAD'],capture_output=True,text=True,encoding='utf-8').stdout.split('\n') if t]
print('tree_entries',len(tree))
print('quoted_paths',[t for t in tree if t.startswith('"')][:3])
p=subprocess.run(['git','-C',R,'cat-file','--batch'],input='\n'.join('HEAD:'+t for t in tree).encode(),capture_output=True)
out=p.stdout
heads=[]
pos=0;n=0
while pos<len(out) and n<6:
    nl=out.index(b'\n',pos);h=out[pos:nl].decode('utf-8','replace');heads.append(h)
    parts=h.split()
    if len(parts)>=3 and parts[2].isdigit():pos=nl+1+int(parts[2])+1
    else:pos=nl+1
    n+=1
print('first_headers',heads)
print('stderr',p.stderr.decode('utf-8','replace')[:200])
