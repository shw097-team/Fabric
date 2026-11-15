"""Run only against a NEW scratch native fhs profile. No model inference or live effects."""
import argparse,asyncio,json,os,pathlib,secrets,socket,subprocess,sys,time,urllib.request

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',type=pathlib.Path,required=True)
    parser.add_argument('--home',type=pathlib.Path,required=True)
    args=parser.parse_args();source=args.source.resolve();home=args.home.resolve()
    expected='bf0203a794a07aac3ff764972ab9087baa4e4f4e'
    sha=subprocess.check_output(['git','-C',str(source),'rev-parse','HEAD'],text=True).strip()
    if sha!=expected:raise SystemExit('SOURCE_IDENTITY_MISMATCH')
    if home.name!='fhs' or home.parent.name!='profiles' or not (home/'profile.yaml').is_file():raise SystemExit('NEW_NATIVE_FHS_PROFILE_REQUIRED')
    if (home/'state.db').exists() or (home/'config.yaml').exists():raise SystemExit('PROFILE_ALREADY_USED; choose a fresh scratch root')
    (home/'config.yaml').write_text('model:\n  provider: opencode-go\n  default: deepseek-v4.1-flash\n  api_mode: anthropic_messages\n  base_url: https://opencode.ai/zen/go\n',encoding='utf-8')
    env=dict(os.environ)
    for key in list(env):
        if key.endswith(('_API_KEY','_ACCESS_TOKEN','_REFRESH_TOKEN')) or key in {'HERMES_PROFILE','HERMES_INSTALL_ROOT','PYTHONHOME','VIRTUAL_ENV'}:env.pop(key,None)
    env.update(HERMES_HOME=str(home),HERMES_RUNTIME_DIR=str(home.parent.parent.parent/'tools'),PYTHONPATH=str(source),PYTHONDONTWRITEBYTECODE='1',PYTHONIOENCODING='utf-8')
    token=secrets.token_urlsafe(32);env['HERMES_DASHBOARD_SESSION_TOKEN']=token
    with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
    checks={};identities=[]
    def identity():
        req=urllib.request.Request(f'http://127.0.0.1:{port}/api/host/identity',headers={'X-Hermes-Session-Token':token})
        with urllib.request.urlopen(req,timeout=5) as r:return json.load(r)
    def start():
        log=(home/'logs/backend-smoke.log').open('a',encoding='utf-8')
        process=subprocess.Popen([sys.executable,'-B','-m','hermes_cli.main','serve','--isolated','--host','127.0.0.1','--port',str(port)],cwd=source,env=env,stdout=log,stderr=log,creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
        for _ in range(120):
            if process.poll() is not None:raise RuntimeError('BACKEND_EXIT')
            try:
                identities.append(identity());return process,log
            except Exception:time.sleep(.5)
        stop(process,log);raise RuntimeError('BACKEND_READY_DEADLINE')
    def stop(process,log):
        if process.poll() is None:
            if os.name=='nt':subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            else:process.terminate()
            process.wait(timeout=20)
        log.close()
    async def run(resume=None):
        import websockets
        async with websockets.connect(f'ws://127.0.0.1:{port}/api/ws?token={token}',open_timeout=10) as ws:
            async def rpc(method,params):
                rid=secrets.token_hex(8)
                await ws.send(json.dumps({'jsonrpc':'2.0','id':rid,'method':method,'params':params}))
                while True:
                    result=json.loads(await asyncio.wait_for(ws.recv(),timeout=40))
                    if result.get('id')==rid:return result
            if resume:
                value=await rpc('session.resume',{'session_id':resume,'profile':'fhs'})
                checks['resume_after_restart']='error' not in value
                bad=await rpc('session.resume',{'session_id':'missing-upgrade-smoke-session','profile':'fhs'})
                checks['stale_session_refused']='error' in bad
                return
            params={'profile':'fhs','idempotency_key':'isolated-upgrade-smoke','cwd':str(home/'workspace')}
            first=await rpc('session.create',params);retry=await rpc('session.create',params)
            if 'error' in first:raise RuntimeError('SESSION_CREATE_REFUSED')
            checks['profile_identity']=first['result'].get('info',{}).get('profile_name')=='fhs'
            checks['duplicate_create_same_session']=first['result']['session_id']==retry.get('result',{}).get('session_id')
            bad=await rpc('session.create',{'profile':'fhs','provider':'openai-codex','model':'opencode-go/deepseek-v4.1-flash'})
            checks['wrong_provider_refused']='error' in bad
            return first['result']['stored_session_id']
    process=log=None
    try:
        process,log=start();stored=asyncio.run(run());stop(process,log);process=log=None
        process,log=start();asyncio.run(run(stored))
        checks['fresh_backend_pid']=len(identities)==2 and identities[0]['pid']!=identities[1]['pid']
        result={'source_sha':sha,'checks':checks,'result':'PASS' if all(checks.values()) else 'HOLD','ceiling':'new empty test Session/Backend only; provider, legacy Session, Native E2E and cutover NOT_RUN'}
    except Exception as ex:result={'source_sha':sha,'checks':checks,'result':'HOLD','error_type':type(ex).__name__}
    finally:
        if process is not None:stop(process,log)
    print(json.dumps(result))
    return 0 if result['result']=='PASS' else 1

if __name__=='__main__':raise SystemExit(main())
