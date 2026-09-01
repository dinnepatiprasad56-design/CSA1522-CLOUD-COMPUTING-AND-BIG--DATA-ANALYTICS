#!/usr/bin/env bash
# ==============================================================================
# Docker Hadoop Cluster Status and Diagnostics Script
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "=========================================================="
echo "      DOCKER HADOOP CLUSTER DIAGNOSTICS REPORT            "
echo "=========================================================="

echo ""
echo "--- 1. CONTAINER STATUS ---"
docker compose ps

echo ""
echo "--- 2. MASTER NODE DAEMONS (hadoop-master) ---"
docker exec hadoop-master jps || echo "Unable to execute jps on hadoop-master"

echo ""
echo "--- 3. WORKER 1 DAEMONS (hadoop-worker1) ---"
docker exec hadoop-worker1 jps || echo "Unable to execute jps on hadoop-worker1"

echo ""
echo "--- 4. WORKER 2 DAEMONS (hadoop-worker2) ---"
docker exec hadoop-worker2 jps || echo "Unable to execute jps on hadoop-worker2"

echo ""
echo "--- 5. HDFS DFSADMIN REPORT ---"
docker exec hadoop-master hdfs dfsadmin -report || echo "HDFS dfsadmin report failed"

echo ""
echo "--- 6. YARN ACTIVE NODE LIST ---"
docker exec hadoop-master yarn node -list || echo "YARN node list failed"

echo ""
echo "--- 7. HDFS /weather DIRECTORY LISTING ---"
docker exec hadoop-master hdfs dfs -ls -R /weather || echo "HDFS listing failed"

echo ""
echo "=========================================================="
echo " Diagnostics Report Completed.                            "
echo "=========================================================="
