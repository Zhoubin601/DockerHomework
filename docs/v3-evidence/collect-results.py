from pathlib import Path
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone

p = Path(__file__).resolve().parent
project = p.parents[1] / 'Code/memory-game6085'
env = os.environ.copy()
for key in ['DOCKER_CONTEXT', 'DOCKER_TLS', 'DOCKER_TLS_VERIFY', 'DOCKER_CERT_PATH']:
    env.pop(key, None)
env['DOCKER_HOST'] = 'unix:///var/run/docker.sock'

def docker(*args):
    return subprocess.check_output(['docker', *args], text=True, env=env).strip()

image = json.loads(docker('image', 'inspect', 'localhost:15085/memory-game6085:1.0.1-v3'))[0]
container = json.loads(docker('inspect', 'memory-game6085-v3-pulled'))[0]
before = json.loads((p/'before-leaderboard.json').read_text())
after = json.loads((p/'after-leaderboard.json').read_text())
old = (p/'before-container.txt').read_text().strip()
new = (p/'after-container.txt').read_text().strip()
jar_hash = hashlib.sha256((project/'dist-artifacts/memory-game6085.jar').read_bytes()).hexdigest()
container_hash = docker('exec', 'memory-game6085-v3-pulled', 'sha256sum', '/app/app.jar').split()[0]
assert before == after and old != new and jar_hash == container_hash
result = {
    'experiment': 'v3 Linux supplementary experiment',
    'capturedAt': datetime.now(timezone.utc).isoformat(),
    'environmentSource': 'Platform-provisioned Docker reused; isolated network, volumes and containers configured in this experiment',
    'dockerVersion': json.loads(docker('version', '--format', '{{json .}}'))['Server']['Version'],
    'composeVersion': docker('compose', 'version', '--short'),
    'os': docker('info', '--format', '{{.OperatingSystem}}'),
    'storageDriver': docker('info', '--format', '{{.Driver}}'),
    'imageTag': '1.0.1-v3',
    'localRegistry': 'localhost:15085',
    'imageId': image['Id'],
    'repoDigests': image['RepoDigests'],
    'oldContainer': old,
    'newContainer': new,
    'containerImageId': container['Image'],
    'volume': 'memory-game6085-v3-data',
    'network': 'memory-game6085-v3-net',
    'applicationUrl': 'http://127.0.0.1:18086',
    'jarSha256': jar_hash,
    'containerJarSha256': container_hash,
    'jarMatchesContainer': True,
    'leaderboardPreserved': True,
    'containerChanged': True,
    'savedScore': json.loads((p/'saved-score.json').read_text()),
    'health': json.loads(subprocess.check_output(['curl', '--fail', '--silent', 'http://127.0.0.1:18086/api/health'], text=True)),
    'windowsExperimentUnchanged': True,
}
assert result['imageId'] == result['containerImageId']
(p/'results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
