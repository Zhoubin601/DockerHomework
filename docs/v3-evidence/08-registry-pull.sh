source /workspace/DockerHomework/docs/v3-evidence/common.sh
printf 'Linux v3 - pull the published version after local image removal\n'
run date -u +%Y-%m-%dT%H:%M:%SZ
run docker pull localhost:15085/memory-game6085:1.0.1-v3
run docker image inspect localhost:15085/memory-game6085:1.0.1-v3 --format 'ImageID={{.Id}} RepoDigests={{json .RepoDigests}}'
