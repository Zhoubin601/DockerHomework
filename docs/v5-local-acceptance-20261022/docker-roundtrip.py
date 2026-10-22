from pathlib import Path
import datetime, hashlib, json, subprocess, sys, time, urllib.request

work=Path(__file__).resolve().parent
evidence=work/'docker-roundtrip'
evidence.mkdir(exist_ok=True)
prefix='memory-game6085-v5verify-20261022'
app=prefix+'-app'
pulled=prefix+'-pulled'
registry=prefix+'-registry'
network=prefix+'-net'
data=prefix+'-data'
registrydata=prefix+'-registry-data'
tag='memory-game6085:v5verify-20261022'
remote='localhost:15087/memory-game6085:v5verify-20261022'
base='http://127.0.0.1:18088'
label='codex.memory6085.test=20261022'

def command(name,*args,allow_fail=False):
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    proc=subprocess.run(['docker',*args],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,encoding='utf-8',errors='replace',timeout=240)
    (evidence/(name+'.txt')).write_text(f'{start}\n> docker '+subprocess.list2cmdline(args)+'\n'+proc.stdout+f'\nExitCode={proc.returncode}\n',encoding='utf-8')
    print(name,proc.returncode,proc.stdout[-1000:],flush=True)
    if proc.returncode and not allow_fail: raise RuntimeError(name+' failed')
    return proc

def get(path):
    return json.load(urllib.request.urlopen(base+path,timeout=4))

def registry_digests(items):
    repository=remote.rsplit(':',1)[0]
    return sorted(item for item in items if item.split('@')[0]==repository)

def ready():
    deadline=time.monotonic()+45
    while time.monotonic()<deadline:
        try:
            state=get('/api/health')
            if state['status']=='UP': return state
        except Exception: pass
        time.sleep(.5)
    raise RuntimeError('Application not ready')

def run_app(name,image):
    result=command('run-'+name,'run','-d','--name',name,'--label',label,'--network',network,'-p','127.0.0.1:18088:8080','-e','DATA_DIR=/app/data','--mount',f'type=volume,source={data},target=/app/data',image)
    ready()
    return result.stdout.strip()

if sys.argv[1]=='prepare':
    before=command('original-containers','ps','-a','--format','{{json .}}')
    (evidence/'original-containers.json').write_text(json.dumps([json.loads(line) for line in before.stdout.splitlines() if line.strip()],ensure_ascii=False,indent=2),encoding='utf-8')
    for kind,names in [('container',[app,pulled,registry]),('volume',[data,registrydata]),('network',[network])]:
        for name in names:
            p=command('preflight-'+name,kind,'inspect',name,allow_fail=True)
            if p.returncode==0: raise RuntimeError('Refusing to reuse existing resource '+name)
    command('network-create','network','create','--label',label,network)
    command('data-create','volume','create','--label',label,data)
    command('registry-data-create','volume','create','--label',label,registrydata)
    command('registry-run','run','-d','--name',registry,'--label',label,'--network',network,'-p','127.0.0.1:15087:5000','-e','OTEL_TRACES_EXPORTER=none','--mount',f'type=volume,source={registrydata},target=/var/lib/registry','registry:3')
    cid=run_app(app,tag)
    command('source-image','image','inspect',tag,'--format','{{json .}}')
    command('container-user','exec',app,'id')
    command('container-jar','exec',app,'sha256sum','/app/app.jar')
    command('copy-container-jar','cp',app+':/app/app.jar',str(evidence/'source-image-app.jar'))
    (evidence/'before-container.txt').write_text(cid,encoding='utf-8')
    (evidence/'initial-health.json').write_text(json.dumps(get('/api/health'),ensure_ascii=False,indent=2),encoding='utf-8')
    print('READY FOR BROWSER TESTS',flush=True)
elif sys.argv[1]=='roundtrip':
    before=get('/api/leaderboard?difficulty=easy')
    assert before['total']>0,'Browser must save a real score first'
    (evidence/'before-leaderboard.json').write_text(json.dumps(before,ensure_ascii=False,indent=2),encoding='utf-8')
    command('tag','tag',tag,remote)
    command('push','push',remote)
    tags=json.load(urllib.request.urlopen('http://127.0.0.1:15087/v2/memory-game6085/tags/list',timeout=5))
    (evidence/'registry-tags.json').write_text(json.dumps(tags,indent=2),encoding='utf-8')
    pushed=json.loads(command('image-after-push','image','inspect',remote,'--format','{{json .RepoDigests}}').stdout)
    own=json.loads(command('validate-owned-app','container','inspect',app,'--format','{{json .Config.Labels}}').stdout)
    assert own.get('codex.memory6085.test')=='20261022'
    command('app-stop','stop',app)
    command('app-remove','rm',app)
    command('image-remove','image','rm',remote,tag)
    for name in [remote,tag]:
        p=command('check-image-absent-'+('remote' if name==remote else 'source'),'image','inspect',name,allow_fail=True)
        assert p.returncode!=0
    command('volume-retained','volume','inspect',data)
    command('pull','pull',remote)
    downloaded=json.loads(command('image-after-pull','image','inspect',remote,'--format','{{json .RepoDigests}}').stdout)
    cid=run_app(pulled,remote)
    after=get('/api/leaderboard?difficulty=easy')
    (evidence/'after-leaderboard.json').write_text(json.dumps(after,ensure_ascii=False,indent=2),encoding='utf-8')
    (evidence/'after-container.txt').write_text(cid,encoding='utf-8')
    command('pulled-container-jar','exec',pulled,'sha256sum','/app/app.jar')
    command('pulled-container-mounts','inspect',pulled,'--format','{{json .Mounts}}')
    original=json.loads((evidence/'original-containers.json').read_text(encoding='utf-8'))
    nowproc=command('final-containers','ps','-a','--format','{{json .}}')
    now={c['Names']:c for c in (json.loads(line) for line in nowproc.stdout.splitlines() if line.strip())}
    original_unchanged=all(c['Names'] in now and c['ID']==now[c['Names']]['ID'] and c['State']==now[c['Names']]['State'] for c in original)
    result={'completedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sourceBuild':'Dockerfile.prebuilt, exact v5 deliverable JAR','oldContainer':(evidence/'before-container.txt').read_text(),'newContainer':cid,'containerChanged':cid!=(evidence/'before-container.txt').read_text(),'leaderboardPreserved':before==after,'beforeLeaderboard':before,'afterLeaderboard':after,'pushRepoDigests':pushed,'pullRepoDigests':downloaded,'repoDigestsMatch':bool(registry_digests(pushed)) and registry_digests(pushed)==registry_digests(downloaded),'localTagsAbsentBeforePull':True,'originalContainersUnchanged':original_unchanged,'applicationUrl':base,'registry':'localhost:15087','dataVolume':data,'health':get('/api/health')}
    (evidence/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    assert all(result[k] for k in ['containerChanged','leaderboardPreserved','repoDigestsMatch','originalContainersUnchanged'])
    print(json.dumps(result,ensure_ascii=False,indent=2),flush=True)
elif sys.argv[1]=='recheck':
    result=json.loads((evidence/'results.json').read_text(encoding='utf-8'))
    backup=evidence/'results-before-repository-normalization.json'
    if not backup.exists():backup.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    result['repoDigestsMatch']=bool(registry_digests(result['pushRepoDigests'])) and registry_digests(result['pushRepoDigests'])==registry_digests(result['pullRepoDigests'])
    result['digestComparisonNote']='Compare digests for localhost:15087/memory-game6085 only; pre-pull inspect also included a source-repository alias. Raw push/pull logs retained.'
    assert get('/api/leaderboard?difficulty=easy')==result['beforeLeaderboard']
    assert all(result[k] for k in ['containerChanged','leaderboardPreserved','repoDigestsMatch','originalContainersUnchanged'])
    (evidence/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2),flush=True)
else:
    raise RuntimeError('Use prepare, roundtrip, or recheck')
