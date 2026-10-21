#!/bin/bash
set -euo pipefail
unset DOCKER_CONTEXT DOCKER_TLS DOCKER_TLS_VERIFY DOCKER_CERT_PATH
export DOCKER_HOST=unix:///var/run/docker.sock
run() { set -x; "$@"; { set +x; } 2>/dev/null; }
