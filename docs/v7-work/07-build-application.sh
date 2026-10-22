set -eux
date -Iseconds
cd /lab
sha256sum dist-artifacts/memory-game6085.jar
docker build --pull=false --network=none -f Dockerfile.prebuilt -t memory-game6085:1.0.2-v7 . >/lab/07-image-build-full.log 2>&1
tail -20 /lab/07-image-build-full.log
docker image inspect memory-game6085:1.0.2-v7 --format 'Image={{.Id}} User={{.Config.User}}'
docker create --name jarcheck6085 memory-game6085:1.0.2-v7
docker cp jarcheck6085:/app/app.jar /lab/container-app.jar
sha256sum /lab/container-app.jar /lab/dist-artifacts/memory-game6085.jar
cmp /lab/container-app.jar /lab/dist-artifacts/memory-game6085.jar
echo 'Container JAR matches the submitted JAR byte-for-byte'
