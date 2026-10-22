set -eux
export DEBIAN_FRONTEND=noninteractive
date -Iseconds
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin >/lab/03-apt-install-full.log 2>&1
tail -22 /lab/03-apt-install-full.log
dpkg-query -W docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
docker --version
dockerd --version
docker compose version
