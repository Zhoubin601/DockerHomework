source /workspace/DockerHomework/docs/v3-evidence/common.sh
cd /workspace/DockerHomework/Code/memory-game6085
printf 'Linux v3: build runtime image from clean prebuilt Spring Boot JAR\n'
run date -u +%Y-%m-%dT%H:%M:%SZ
run sha256sum dist-artifacts/memory-game6085.jar
run docker build --pull=false -f Dockerfile.prebuilt -t memory-game6085:1.0.1-v3 .
run docker image inspect memory-game6085:1.0.1-v3 --format 'ImageID={{.Id}} User={{.Config.User}} Exposed={{json .Config.ExposedPorts}}'
