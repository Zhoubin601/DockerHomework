set -eux
date -Iseconds
docker inspect garden6085 --format '{{.Id}}' | tee /lab/before-container.txt
curl -fsS 'http://127.0.0.1:18085/api/leaderboard?difficulty=easy' | tee /lab/before-leaderboard.json
echo
grep -q '"nickname"' /lab/before-leaderboard.json
docker tag memory-game6085:1.0.2-v7 localhost:5000/memory-game6085:1.0.2-v7
docker push localhost:5000/memory-game6085:1.0.2-v7 >/lab/09-push-full.log 2>&1
tail -12 /lab/09-push-full.log
curl -fsS http://localhost:5000/v2/memory-game6085/tags/list
echo
