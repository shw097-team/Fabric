"""Round-only trace observer around the existing canonical dispatcher.
No route, sandbox, oracle, nonce, acceptance, or canonical source change.
Canonical timeout handling drops partial capture; separate trace is diagnostic only.
"""
import pathlib,sys,subprocess,runpy,json,hashlib,time,os
DISPATCH=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/scripts/hgk-lane-dispatch.py')
TRACE=pathlib.Path(os.environ['SKCV_TRACE_DIR']);TRACE.mkdir(parents=True,exist_ok=True)
original_run=subprocess.run
counter=0
def observed_run(args,*pos,**kw):
 global counter
 if not isinstance(args,(list,tuple)) or pathlib.Path(str(args[0])).name.lower()!='codex.exe':return original_run(args,*pos,**kw)
 assert kw.get('capture_output') is True and not pos,'Observer only supports the canonical binary capture invocation'
 counter+=1;stem=TRACE/('observed-'+str(counter));out=stem.with_suffix('.stdout.jsonl');err=stem.with_suffix('.stderr.log');meta=stem.with_suffix('.metadata.json');actual=dict(kw);actual.pop('capture_output');timeout=actual.pop('timeout',None)
 assert not any(k in actual for k in ['text','encoding','errors','stdout','stderr']),'Do not silently change byte handling'
 started=time.time();p=None
 with out.open('wb') as stdout,err.open('wb') as stderr:
  p=subprocess.Popen(args,stdout=stdout,stderr=stderr,**actual)
  meta.write_text(json.dumps({'pid':p.pid,'started_epoch':started,'timeout':timeout,'argv_sha256':hashlib.sha256(json.dumps(args,ensure_ascii=False).encode()).hexdigest(),'canonical_dispatch':str(DISPATCH),'authority':'diagnostic trace only; no gate overrides'},indent=2),encoding='utf-8')
  try:rc=p.wait(timeout=timeout)
  except subprocess.TimeoutExpired:
   # Kill only the process this observer created, including its own child tree.
   original_run(['taskkill.exe','/F','/T','/PID',str(p.pid)],capture_output=True,timeout=15)
   p.wait(timeout=15);stdout.flush();stderr.flush()
   raise subprocess.TimeoutExpired(args,timeout,output=out.read_bytes(),stderr=err.read_bytes())
 return subprocess.CompletedProcess(args,rc,out.read_bytes(),err.read_bytes())
if __name__=='__main__':
 subprocess.run=observed_run
 sys.argv=[str(DISPATCH),*sys.argv[1:]]
 runpy.run_path(str(DISPATCH),run_name='__main__')
