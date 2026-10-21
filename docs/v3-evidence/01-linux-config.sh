source /workspace/DockerHomework/docs/v3-evidence/common.sh
printf 'Linux supplementary experiment - existing platform Docker daemon\n'
run date -u +%Y-%m-%dT%H:%M:%SZ
run docker version --format 'Client={{.Client.Version}} Server={{.Server.Version}}'
run docker info --format 'OS={{.OperatingSystem}}; Driver={{.Driver}}; Kernel={{.KernelVersion}}'
run docker compose version
run docker network create --label course=memory-game6085-v3 memory-game6085-v3-net
run docker volume create --label course=memory-game6085-v3 memory-game6085-v3-data
run docker volume create --label course=memory-game6085-v3 memory-game6085-v3-registry-data
run docker network inspect memory-game6085-v3-net --format 'Network={{.Name}} Driver={{.Driver}}'
run docker volume inspect memory-game6085-v3-data --format 'Volume={{.Name}} Driver={{.Driver}}'
printf '\nPlatform Docker reused; isolated v3 network and volumes configured.\n'
