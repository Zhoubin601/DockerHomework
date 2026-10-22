set -eux
date -Iseconds
docker load -i /lab/base-images.tar
docker run --name hello6085 hello-world
docker ps -a --filter name=hello6085 --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}'
