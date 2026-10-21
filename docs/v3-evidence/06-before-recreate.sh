source /workspace/DockerHomework/docs/v3-evidence/common.sh
printf 'Linux v3 - record actual saved score and original container before recreation\n'
run date -u +%Y-%m-%dT%H:%M:%SZ
run curl --fail --silent 'http://127.0.0.1:18086/api/leaderboard?difficulty=easy'
printf '\n'
run docker inspect memory-game6085-v3-app --format 'Container={{.Id}} Image={{.Image}} Volume={{(index .Mounts 0).Name}}'
run docker exec memory-game6085-v3-app sha256sum /app/app.jar
curl --fail --silent 'http://127.0.0.1:18086/api/leaderboard?difficulty=easy' > /workspace/DockerHomework/docs/v3-evidence/before-leaderboard.json
docker inspect memory-game6085-v3-app --format '{{.Id}}' > /workspace/DockerHomework/docs/v3-evidence/before-container.txt
