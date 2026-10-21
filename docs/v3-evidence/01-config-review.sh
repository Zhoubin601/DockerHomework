source /workspace/DockerHomework/docs/v3-evidence/common.sh
printf 'Linux v3 supplementary experiment - platform Docker reused\n'
run date -u +%Y-%m-%dT%H:%M:%SZ
run docker version --format 'Client={{.Client.Version}} Server={{.Server.Version}}'
run docker info --format 'OS={{.OperatingSystem}}; Driver={{.Driver}}'
run docker compose version
printf '\nIsolated resources created in 01-linux-config.txt; configuration verification:\n'
run docker network inspect memory-game6085-v3-net --format 'Network={{.Name}} Driver={{.Driver}}'
run docker volume inspect memory-game6085-v3-data --format 'Volume={{.Name}} Driver={{.Driver}}'
run docker volume inspect memory-game6085-v3-registry-data --format 'Volume={{.Name}} Driver={{.Driver}}'
printf '\nOriginal Windows installation history is separate from this Linux experiment.\n'
