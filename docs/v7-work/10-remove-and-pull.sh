set -eux
date -Iseconds
docker rm -f garden6085 jarcheck6085
docker image rm memory-game6085:1.0.2-v7 localhost:5000/memory-game6085:1.0.2-v7
if docker image inspect memory-game6085:1.0.2-v7 >/dev/null 2>&1; then exit 1; fi
if docker image inspect localhost:5000/memory-game6085:1.0.2-v7 >/dev/null 2>&1; then exit 1; fi
echo 'Both local application image tags are absent before pull'
docker image ls --filter reference='*memory-game6085*'
docker pull localhost:5000/memory-game6085:1.0.2-v7 >/lab/10-pull-full.log 2>&1
tail -15 /lab/10-pull-full.log
docker image inspect localhost:5000/memory-game6085:1.0.2-v7 --format '{{json .RepoDigests}}'
