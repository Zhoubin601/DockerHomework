source /workspace/DockerHomework/docs/v3-evidence/common.sh
printf 'Linux v3 - isolated local Registry and actual image publication\n'
run date -u +%Y-%m-%dT%H:%M:%SZ
run docker run -d --name memory-game6085-v3-registry --network memory-game6085-v3-net -p 127.0.0.1:15085:5000 -e OTEL_TRACES_EXPORTER=none --mount type=volume,source=memory-game6085-v3-registry-data,target=/var/lib/registry registry:3
for attempt in $(seq 1 40); do curl --fail --silent http://127.0.0.1:15085/v2/ >/dev/null && break; sleep 1; done
run docker tag memory-game6085:1.0.1-v3 localhost:15085/memory-game6085:1.0.1-v3
run docker push localhost:15085/memory-game6085:1.0.1-v3
run curl --fail --silent http://127.0.0.1:15085/v2/memory-game6085/tags/list
printf '\n'
run docker image inspect localhost:15085/memory-game6085:1.0.1-v3 --format 'RepoDigests={{json .RepoDigests}}'
