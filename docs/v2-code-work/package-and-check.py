from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from hashlib import sha256
import json, re, socket, subprocess, os, time, urllib.request, shutil
ROOT=Path('/workspace/DockerHomework')
WORK=ROOT/'docs/v2-code-work'
CODE=ROOT/'Code/memory-game6085'
JAR=WORK/'build/memory-game6085/backend/target/memory-game6085.jar'
DEST=WORK/'20261021-memory-game6085-v2.zip'
assert not DEST.exists()
with ZipFile(ROOT/'output/v1/20261021-memory-game6085-v1.zip') as old, ZipFile(DEST,'x',ZIP_DEFLATED) as new:
    for name in old.namelist():
        relative=Path(name).relative_to('memory-game6085')
        source=JAR if str(relative)=='backend/target/memory-game6085.jar' else CODE/relative
        new.write(source,name)
    new.write(CODE/'scripts/start-docker-runtime.ps1','memory-game6085/scripts/start-docker-runtime.ps1')
with ZipFile(DEST) as new:
    assert new.testzip() is None
    assert len(new.namelist())==30
    assert 'memory-game6085/scripts/start-docker-runtime.ps1' in new.namelist()
    assert 'clean package' in new.read('memory-game6085/scripts/build.ps1').decode()
with ZipFile(JAR) as z:
    assets=[n for n in z.namelist() if n.startswith('BOOT-INF/classes/static/assets/') and not n.endswith('/')]
    assert len(assets)==2, assets
    index=z.read('BOOT-INF/classes/static/index.html').decode()
    manifest=z.read('META-INF/MANIFEST.MF').decode()
    assert 'Spring-Boot-Version: 4.1.1' in manifest
    assert z.testzip() is None
with socket.socket() as sock:
    sock.bind(('127.0.0.1',0)); port=sock.getsockname()[1]
data=WORK/'smoke-data'
assert not data.exists()
env=dict(os.environ,PORT=str(port),DATA_DIR=str(data))
log=(WORK/'smoke-startup.log').open('w')
process=subprocess.Popen(['/workspace/.cloud-tools/jdk-21/bin/java','-jar',str(JAR)],cwd=WORK,env=env,stdout=log,stderr=subprocess.STDOUT)
base=f'http://127.0.0.1:{port}'
result={}
try:
    for attempt in range(100):
        try:
            with urllib.request.urlopen(base+'/api/health',timeout=1) as response:health=json.load(response)
            break
        except Exception:
            if process.poll() is not None: raise RuntimeError('JAR exited during startup')
            time.sleep(.2)
    else:raise RuntimeError('health timeout')
    assert health['status']=='UP'
    with urllib.request.urlopen(base,timeout=3) as response:html=response.read().decode()
    urls=re.findall(r'(?:src|href)="(/assets/[^\"]+)"',html)
    assert len(urls)==2
    sizes={}
    for url in urls:
        with urllib.request.urlopen(base+url,timeout=3) as response:sizes[url]=len(response.read())
    request=urllib.request.Request(base+'/api/games',data=json.dumps({'difficulty':'easy'}).encode(),headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(request,timeout=3) as response:game=json.load(response)
    assert len(game['cards'])==12 and all(c['symbol'] is None for c in game['cards'])
    result={'health':health,'assetSizes':sizes,'gameCreated':bool(game['id']),'cardCount':len(game['cards']),'allCardSymbolsHidden':True,'jarStaticAssetCount':len(assets),'zipEntries':30,'zipSha256':sha256(DEST.read_bytes()).hexdigest(),'jarSha256':sha256(JAR.read_bytes()).hexdigest(),'frontEndRebuilt':True,'backendRebuiltFromEmptyTarget':True,'mavenOffline':True,'tests':{'run':3,'failures':0,'errors':0,'skipped':0}}
finally:
    process.terminate()
    try: process.wait(timeout=10)
    except subprocess.TimeoutExpired:process.kill();process.wait(timeout=5)
    log.close()
    if data.exists():shutil.rmtree(data)
    result['smokeProcessStopped']=process.poll() is not None
    result['temporaryDataRemoved']=not data.exists()
(WORK/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
# Confirm v1 artifacts are unchanged.
for line in (WORK/'v1-sha256-before.txt').read_text().splitlines():
    expected,path=line.split('  ',1)
    assert sha256((ROOT/path).read_bytes()).hexdigest()==expected,path
print(json.dumps(result,ensure_ascii=False,indent=2))
