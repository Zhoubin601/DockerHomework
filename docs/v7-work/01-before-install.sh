set -eux
date -Iseconds
cat /etc/os-release | head -6
uname -m
if command -v docker; then exit 1; else echo 'Docker CLI: not installed in this fresh Ubuntu environment'; fi
if command -v dockerd; then exit 1; else echo 'Docker Engine: not installed'; fi
if test -S /var/run/docker.sock; then exit 1; else echo 'No Docker socket; host Docker socket is NOT mounted'; fi
dpkg-query -W docker-ce docker-ce-cli containerd.io 2>/dev/null || true
