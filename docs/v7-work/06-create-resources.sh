set -eux
date -Iseconds
docker network create memory-game6085-v7-net
docker volume create memory-game6085-v7-data
docker volume create memory-game6085-v7-registry
docker run -d --name registry6085 --network memory-game6085-v7-net -p 127.0.0.1:5000:5000 -e OTEL_TRACES_EXPORTER=none --mount type=volume,source=memory-game6085-v7-registry,target=/var/lib/registry registry:3
docker network inspect memory-game6085-v7-net --format 'Network={{.Name}} Driver={{.Driver}} Subnet={{(index .IPAM.Config 0).Subnet}}'
docker volume inspect memory-game6085-v7-data memory-game6085-v7-registry --format 'Volume={{.Name}} Driver={{.Driver}}'
docker ps --filter name=registry6085 --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}'
curl --retry 10 --retry-connrefused --retry-delay 1 -fsS http://127.0.0.1:5000/v2/
echo
