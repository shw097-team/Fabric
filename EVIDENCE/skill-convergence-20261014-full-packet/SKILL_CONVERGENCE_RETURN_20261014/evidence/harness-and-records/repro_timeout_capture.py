"""Offline executable reproduction of canonical partial-capture loss.
Extracts the actual existing try block, executes it with TimeoutExpired byte payloads.
This is a bug-reproduction diagnostic, NOT a patched canonical dispatcher or product PASS.
"""
import ast,pathlib,json,hashlib,subprocess,types
from unittest.mock import patch
R=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014')
P=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/scripts/hgk-lane-dispatch.py')
source=P.read_bytes();tree=ast.parse(source)
tries=[n for n in ast.walk(tree) if isinstance(n,ast.Try) and any(isinstance(h.type,ast.Attribute) and h.type.attr=='TimeoutExpired' for h in n.handlers) and 'capture_output=True' in ast.unparse(n)]
assert len(tries)==1
module=ast.Module(body=[tries[0]],type_ignores=[]);ast.fix_missing_locations(module)
cmd=['fixture-codex.exe'];error=subprocess.TimeoutExpired(cmd,0.1,output=b'partial-stdout\r\n',stderr=b'partial-stderr\r\n')
ns={'subprocess':subprocess,'cmd':cmd,'args':types.SimpleNamespace(timeout=0.1),'env':{}}
with patch.object(subprocess,'run',side_effect=error):exec(compile(module,str(P),'exec'),ns)
assert ns['rc']=='TIMEOUT' and ns['out_b']==b'' and ns['err_b']==b''
result={'kind':'PASS_BUG_REPRODUCTION_NOT_PRODUCT_PASS','canonical_source':str(P),'canonical_sha256':hashlib.sha256(source).hexdigest(),'line_start':tries[0].lineno,'line_end':tries[0].end_lineno,'provided_nonempty_partial_output':True,'observed_partial_output_discarded':True,'canonical_source_changed':False,'remediation':'round-only trace observer, ordinary official timeout still FAIL; no acceptance from partial traces'}
(R/'evidence/timeout_capture_reproduction.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result))
