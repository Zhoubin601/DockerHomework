set -eux
date -Iseconds
docker run -d --name garden6085 --network memory-game6085-v7-net -p 18085:8080 -e DATA_DIR=/app/data --mount type=volume,source=memory-game6085-v7-data,target=/app/data memory-game6085:1.0.2-v7
curl --retry 30 --retry-connrefused --retry-delay 1 -fsS http://127.0.0.1:18085/api/health
echo
docker ps --filter name=garden6085 --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}'
docker inspect garden6085 --format 'Network={{json .NetworkSettings.Networks}}'
docker inspect garden6085 --format '{{range .Mounts}}Volume={{.Name}} Destination={{.Destination}}{{end}}'
docker exec garden6085 id
curl -fsS 'http://127.0.0.1:18085/api/leaderboard?difficulty=easy'
echo
