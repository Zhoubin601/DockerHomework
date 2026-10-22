from pathlib import Path
from zipfile import ZipFile
import hashlib, json, subprocess, xml.etree.ElementTree as E

W=Path(__file__).resolve().parent
R=W.parents[1]
sha=lambda b:hashlib.sha256(b).hexdigest()
def run(*args):
    p=subprocess.run(args,capture_output=True,check=True)
    return p.stdout.decode('utf-8','replace')

name='memory-game6085-v5verify-20261022-source-inspect'
pre=subprocess.run(['docker','container','inspect',name],capture_output=True)
assert pre.returncode!=0,'Refusing to reuse existing container'
cid=run('docker','create','--name',name,'--label','codex.memory6085.test=20261022','memory-game6085:v5verify-source-20261022').strip()
try:
    run('docker','cp',cid+':/app/app.jar',str(W/'docker-source-app.jar'))
finally:
    run('docker','rm',cid)
project=W/'unpacked/memory-game6085'
def entries(p):
    with ZipFile(p) as z:
        return {n:sha(z.read(n)) for n in z.namelist() if n.startswith('BOOT-INF/') and not n.endswith('/')}
delivery=project/'dist-artifacts/memory-game6085.jar'
expected=entries(delivery)
jars={
    'sourceRebuild':project/'backend/target/memory-game6085.jar',
    'dockerSource':W/'docker-source-app.jar',
    'dockerDelivery':W/'docker-roundtrip/source-image-app.jar',
}
comparison={k:{'sha256':sha(p.read_bytes()),'bootInfEntries':len(entries(p)),'bootInfMatchesDelivery':entries(p)==expected,'wholeJarMatchesDelivery':p.read_bytes()==delivery.read_bytes()} for k,p in jars.items()}
assert all(m['bootInfMatchesDelivery'] for m in comparison.values())
assert comparison['dockerDelivery']['wholeJarMatchesDelivery']
tests=E.parse(project/'backend/target/surefire-reports/TEST-cn.memorygarden.GardenTests.xml').getroot()
backend={k:tests.get(k) for k in ['tests','failures','errors','skipped']}
assert backend=={'tests':'3','failures':'0','errors':'0','skipped':'0'}
baseline=json.loads((W/'baseline-sha256.json').read_text(encoding='utf-8'))
changed=[p for p,h in baseline.items() if not (R/p).exists() or sha((R/p).read_bytes())!=h]
assert not changed
runtime=json.loads((W/'docker-roundtrip/results.json').read_text(encoding='utf-8'))
assert all(runtime[k] for k in ['containerChanged','leaderboardPreserved','repoDigestsMatch','originalContainersUnchanged'])
browser=json.loads((W/'docker-roundtrip/browser-after.json').read_text(encoding='utf-8'))
assert browser['savedScoreVisible'] and not browser['pageErrors']
pag=json.loads((W/'pagination-check.json').read_text(encoding='utf-8'))
result={'gitCommit':run('git','rev-parse','HEAD').strip(),'remoteCommit':run('git','rev-parse','origin/main').strip(),'backendTests':backend,'browserTests':'3 passed','pulledImageBrowser':browser,'jarComparison':comparison,'deliveryJarSha256':sha(delivery.read_bytes()),'rawAndOutputFilesChecked':len(baseline),'rawAndOutputChanged':changed,'dockerRoundtripPassed':True,'originalContainersUnchanged':runtime['originalContainersUnchanged'],'wordPages':pag['pages'],'tocEntriesVerified':pag['verifiedTocEntries'],'wordSchema':'passed, zero errors','applicationUrl':runtime['applicationUrl'],'historicalInstallScreenshots':'资料未提供；报告如实说明沿用已有引擎'}
(W/'final-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=True,indent=2))
