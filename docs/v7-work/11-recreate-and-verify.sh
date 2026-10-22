set -eux
date -Iseconds
docker run -d --name garden6085-pulled --network memory-game6085-v7-net -p 18085:8080 -e DATA_DIR=/app/data --mount type=volume,source=memory-game6085-v7-data,target=/app/data localhost:5000/memory-game6085:1.0.2-v7
curl --retry 30 --retry-all-errors --retry-delay 1 -fsS http://127.0.0.1:18085/api/health
echo
docker inspect garden6085-pulled --format '{{.Id}}' | tee /lab/after-container.txt
curl -fsS 'http://127.0.0.1:18085/api/leaderboard?difficulty=easy' | tee /lab/after-leaderboard.json
echo
cmp /lab/before-leaderboard.json /lab/after-leaderboard.json
test "$(cat /lab/before-container.txt)" != "$(cat /lab/after-container.txt)"
echo 'NewContainer=True; FullLeaderboardPreserved=True'
docker inspect garden6085-pulled --format '{{range .Mounts}}Volume={{.Name}} Destination={{.Destination}}{{end}}'
docker exec garden6085-pulled id
