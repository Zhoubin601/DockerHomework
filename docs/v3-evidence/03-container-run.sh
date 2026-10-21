source /workspace/DockerHomework/docs/v3-evidence/common.sh
printf 'Linux v3 - run the new image with isolated network and data volume\n'
run date -u +%Y-%m-%dT%H:%M:%SZ
run docker run -d --name memory-game6085-v3-app --network memory-game6085-v3-net -p 127.0.0.1:18086:8080 -e DATA_DIR=/app/data --mount type=volume,source=memory-game6085-v3-data,target=/app/data memory-game6085:1.0.1-v3
for attempt in $(seq 1 40); do curl --fail --silent http://127.0.0.1:18086/api/health >/dev/null && break; sleep 1; done
run docker ps --filter name=memory-game6085-v3-app --format 'Name={{.Names}} Ports={{.Ports}}'
run curl --fail --silent http://127.0.0.1:18086/api/health
printf '\n'
run docker exec memory-game6085-v3-app id
run sha256sum /workspace/DockerHomework/Code/memory-game6085/dist-artifacts/memory-game6085.jar
run docker exec memory-game6085-v3-app sha256sum /app/app.jar
run docker inspect memory-game6085-v3-app --format 'Container={{.Id}} Volume={{(index .Mounts 0).Name}}'
