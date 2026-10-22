set -eux
date -Iseconds
mkdir -p /etc/docker
cat >/etc/docker/daemon.json <<'EOF'
{
  "data-root": "/var/lib/docker-lab6085",
  "storage-driver": "vfs",
  "log-driver": "json-file",
  "log-opts": {"max-size": "10m", "max-file": "3"}
}
EOF
cat /etc/docker/daemon.json
dockerd --validate --config-file=/etc/docker/daemon.json
nohup dockerd --config-file=/etc/docker/daemon.json >/lab/04-dockerd-full.log 2>&1 &
for n in $(seq 1 60); do
  if docker info >/lab/04-docker-info-full.log 2>&1; then break; fi
  sleep 1
done
docker version --format 'Client={{.Client.Version}} Server={{.Server.Version}}'
docker info --format 'Name={{.Name}} Driver={{.Driver}} Root={{.DockerRootDir}} Cgroup={{.CgroupVersion}}'
docker compose version
docker info --format '{{json .LoggingDriver}}'
