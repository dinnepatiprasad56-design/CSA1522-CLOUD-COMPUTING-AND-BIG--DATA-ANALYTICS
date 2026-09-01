#!/usr/bin/env bash
# ==============================================================================
# Explicit NameNode Re-formatting Script for Local Docker Cluster
# WARNING: Clears HDFS metadata and re-initializes filesystem
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "=========================================================="
echo "      HDFS NAMENODE EXPLICIT FORMATTING SCRIPT            "
echo " WARNING: This will purge and reset all HDFS metadata.    "
echo "=========================================================="

echo "[1/4] Stopping cluster containers..."
docker compose stop

echo "[2/4] Removing HDFS data volumes..."
docker volume rm namenode_data datanode1_data datanode2_data hadoop_logs 2>/dev/null || true

echo "[3/4] Re-launching cluster containers (NameNode format will auto-trigger)..."
docker compose up -d

echo "Waiting 15 seconds for NameNode initialization..."
sleep 15

echo "[4/4] Verifying HDFS initialization..."
docker exec hadoop-master hdfs dfs -ls /weather

echo "=========================================================="
echo " NameNode re-formatting and directory setup complete!     "
echo "=========================================================="
