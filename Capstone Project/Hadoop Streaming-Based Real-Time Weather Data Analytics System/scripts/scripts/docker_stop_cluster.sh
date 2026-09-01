#!/usr/bin/env bash
# ==============================================================================
# Stop 3-Node Local Docker Hadoop Cluster (Preserves HDFS Data Volumes)
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "=========================================================="
echo " Stopping Local 3-Node Docker Hadoop Cluster              "
echo "=========================================================="

docker compose stop

echo "[OK] Cluster containers stopped safely. Persistent HDFS data volumes preserved."
