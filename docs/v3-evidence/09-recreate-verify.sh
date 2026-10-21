source /workspace/DockerHomework/docs/v3-evidence/common.sh
printf 'Linux v3 - new container from pulled image, same named volume\n'
run date -u +%Y-%m-%dT%H:%M:%SZ
run docker run -d --name memory-game6085-v3-pulled --network memory-game6085-v3-net -p 127.0.0.1:18086:8080 -e DATA_DIR=/app/data --mount type=volume,source=memory-game6085-v3-data,target=/app/data localhost:15085/memory-game6085:1.0.1-v3
for attempt in $(seq 1 40); do curl --fail --silent http://127.0.0.1:18086/api/health >/dev/null && break; sleep 1; done
run curl --fail --silent http://127.0.0.1:18086/api/health
printf '\n'
run docker inspect memory-game6085-v3-pulled --format 'Container={{.Id}} Image={{.Image}} Volume={{(index .Mounts 0).Name}}'
run docker exec memory-game6085-v3-pulled sha256sum /app/app.jar
run curl --fail --silent 'http://127.0.0.1:18086/api/leaderboard?difficulty=easy'
printf '\n'
curl --fail --silent 'http://127.0.0.1:18086/api/leaderboard?difficulty=easy' > /workspace/DockerHomework/docs/v3-evidence/after-leaderboard.json
docker inspect memory-game6085-v3-pulled --format '{{.Id}}' > /workspace/DockerHomework/docs/v3-evidence/after-container.txt
run python /workspace/DockerHomework/docs/v3-evidence/compare-results.py
