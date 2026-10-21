source /workspace/DockerHomework/docs/v3-evidence/common.sh
cd /workspace/DockerHomework/Code/memory-game6085
printf 'Linux v3 - repeatable image build from the exact deliverable JAR\n'
run date -u +%Y-%m-%dT%H:%M:%SZ
run sha256sum -c dist-artifacts/SHA256SUMS
run docker build --progress=plain --pull=false -f Dockerfile.prebuilt -t memory-game6085:1.0.1-v3 .
run docker image inspect memory-game6085:1.0.1-v3 --format 'ImageID={{.Id}} User={{.Config.User}}'
