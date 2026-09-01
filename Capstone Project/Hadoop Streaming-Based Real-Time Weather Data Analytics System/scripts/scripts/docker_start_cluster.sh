#!/usr/bin/env bash
# ==============================================================================
# Start 3-Node Local Docker Hadoop Cluster
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "=========================================================="
echo " Starting Local 3-Node Docker Hadoop Cluster              "
echo " Network: weather-hadoop-network                          "
echo " Master:  hadoop-master                                   "
echo " Workers: hadoop-worker1, hadoop-worker2                  "
echo "=========================================================="

if ! docker info >/dev/null 2>&1; then
    echo "[ERROR] Docker daemon is not running. Please start Docker Desktop and retry."
    exit 1
fi

docker compose up -d --build

echo ""
echo "[OK] Docker containers launched!"
echo "Waiting for cluster services to initialize (15 seconds)..."
sleep 15

docker compose ps

echo ""
echo "=========================================================="
echo " Hadoop Web UIs:"
echo "  - HDFS NameNode      : http://localhost:9870"
echo "  - YARN ResourceMgr   : http://localhost:8088"
echo "  - JobHistory Server  : http://localhost:19888"
echo "  - Weather Dashboard  : http://localhost:8501"
echo "=========================================================="
