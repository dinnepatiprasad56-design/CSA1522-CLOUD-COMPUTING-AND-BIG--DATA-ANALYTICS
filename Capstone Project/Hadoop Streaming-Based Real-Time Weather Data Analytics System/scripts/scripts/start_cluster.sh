#!/usr/bin/env bash
# ==============================================================================
# Hadoop 3-Node Cluster Startup Launcher (Docker & Native Support)
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Trigger Docker Compose start cluster script
bash "$SCRIPT_DIR/docker_start_cluster.sh"
