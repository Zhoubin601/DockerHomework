source /workspace/DockerHomework/docs/v3-evidence/common.sh
printf 'Linux v3 - remove only v3 application container and both local image tags\n'
run date -u +%Y-%m-%dT%H:%M:%SZ
run docker rm -f memory-game6085-v3-app
run docker image rm localhost:15085/memory-game6085:1.0.1-v3 memory-game6085:1.0.1-v3
run docker image ls --filter 'reference=*memory-game6085*1.0.1-v3' --format '{{.Repository}}:{{.Tag}} {{.ID}}'
printf 'No v3 image rows above. Named data volume is retained:\n'
run docker volume inspect memory-game6085-v3-data --format '{{.Name}} {{.Driver}}'
