import pathlib,subprocess,sys,json
ROOT=pathlib.Path(__file__).resolve().parent
HOME=pathlib.Path('C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes')
rows=[]
def attempt(label,path):
 try:path.write_bytes(b'SKCV_ESCAPE_SHOULD_NOT_LAND');rows.append({'probe':label,'refused':False,'path':str(path)});return False
 except PermissionError as e:rows.append({'probe':label,'refused':True,'error':type(e).__name__,'path':str(path)});return True
 except Exception as e:rows.append({'probe':label,'refused':None,'error':repr(e),'path':str(path)});return False
pos=ROOT/'admitted-marker.txt';pos.write_bytes(b'SKCV_ADMITTED_WRITE');positive=pos.read_bytes()==b'SKCV_ADMITTED_WRITE'
out=HOME/'cache/scratch/SKCV-owned-escape-root/outside-direct.txt';direct=attempt('outside_direct',out)
code="from pathlib import Path;Path("+repr(str(out.parent/'outside-subprocess.txt'))+").write_bytes(b'SKCV_ESCAPE_SHOULD_NOT_LAND')"
p=subprocess.run([sys.executable,'-c',code],capture_output=True,text=True);sub_denied=p.returncode!=0 and 'PermissionError' in p.stderr;rows.append({'probe':'subprocess','refused':sub_denied,'child_exit':p.returncode,'stderr':p.stderr})
link=ROOT/'probe-junction';junction_exists=link.exists();traversal=attempt('preexisting_junction_traversal',link/'junction-escape.txt') if junction_exists else False
sibling=attempt('outside_cwd_sibling',ROOT.parent/'evidence/SKCV-SIBLING-ESCAPE.txt')
result={'positive':positive,'admitted_marker':str(pos),'junction_fixture_exists':junction_exists,'rows':rows,'all_negative_seams_refused':direct and sub_denied and traversal and sibling,'interpreter':sys.executable,'claim_ceiling':'raw scoped qualification observations, not acceptance'}
print(json.dumps(result,indent=2));sys.exit(0 if positive and result['all_negative_seams_refused'] else 3)
