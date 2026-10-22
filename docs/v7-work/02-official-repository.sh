set -eux
export DEBIAN_FRONTEND=noninteractive
date -Iseconds
apt-get update >/lab/02-prerequisites-full.log 2>&1
apt-get install -y ca-certificates curl >>/lab/02-prerequisites-full.log 2>&1
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc
cat >/etc/apt/sources.list.d/docker.sources <<'EOF'
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: noble
Components: stable
Architectures: amd64
Signed-By: /etc/apt/keyrings/docker.asc
EOF
cat /etc/apt/sources.list.d/docker.sources
apt-get update >/lab/02-docker-repository-full.log 2>&1
tail -8 /lab/02-docker-repository-full.log
apt-cache policy docker-ce | head -10
