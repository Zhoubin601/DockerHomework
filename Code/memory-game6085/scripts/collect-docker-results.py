from pathlib import Path
import json, re, subprocess
from datetime import datetime, timezone, timedelta
from urllib.request import urlopen

root = Path(__file__).resolve().parents[3]
evidence = root / 'docs/docker-evidence'
queue = root / 'Code/memory-game6085/.qa/terminal-queue'
stages = ['02-build','03b-container-run','04-data-before','05-registry-push','06-remove-local','07-registry-pull','08-run-pulled-image','09-data-after']
for stage in stages:
    data = json.loads((queue / (stage+'-done.json')).read_text(encoding='utf-8-sig'))
    assert data['success'], stage

def docker(*args):
    return subprocess.check_output(['docker', *args], text=True, encoding='utf-8').strip()

before = json.loads((evidence/'before-leaderboard.json').read_text(encoding='utf-8-sig'))
after = json.loads((evidence/'after-leaderboard.json').read_text(encoding='utf-8-sig'))
assert before == after and after['total'] >= 1
before_log = (evidence/'04-data-before.txt').read_text(encoding='utf-8-sig')
old_id = re.search(r'BeforeContainer=([a-f0-9]{64})', before_log).group(1)
container = json.loads(docker('inspect','memory-game6085-pulled'))[0]
assert container['Id'] != old_id and container['State']['Running']
image = json.loads(docker('image','inspect','localhost:5000/memory-game6085:1.0.0'))[0]
push_log = (evidence/'05-registry-push.txt').read_text(encoding='utf-8-sig')
digest = re.search(r'digest: (sha256:[a-f0-9]{64})', push_log).group(1)
assert any(digest in item for item in image['RepoDigests'])
with urlopen('http://127.0.0.1:18085/api/health') as response:
    health = json.load(response)
assert health['status'] == 'UP'
mount = next(item for item in container['Mounts'] if item['Destination']=='/app/data')
assert mount['Name'] == 'memory-game6085-data'
result = {
    'completedAt':datetime.now(timezone(timedelta(hours=8))).isoformat(),
    'imageTag':'localhost:5000/memory-game6085:1.0.0',
    'digest':digest,'imageId':image['Id'],'imageBytes':image['Size'],
    'beforeContainerId':old_id,'afterContainerId':container['Id'],
    'volume':mount['Name'],'dataDestination':mount['Destination'],
    'leaderboardPreserved':before==after,'leaderboard':after,'health':health,
    'dockerVersion':json.loads(docker('version','--format','{{json .}}')),
    'hostPort':18085,'containerPort':8080,'registryPort':5000,
    'stages':stages,
}
(evidence/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:result[k] for k in ['imageTag','digest','beforeContainerId','afterContainerId','leaderboardPreserved']},ensure_ascii=False))
