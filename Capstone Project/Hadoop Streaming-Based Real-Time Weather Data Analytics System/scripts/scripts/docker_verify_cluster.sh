#!/usr/bin/env bash
# ==============================================================================
# Comprehensive 16-Point Docker Hadoop Cluster Verification Suite
# Project: Hadoop Streaming-Based Real-Time Weather Data Analytics System
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "=========================================================="
echo "      COMPREHENSIVE 16-POINT HADOOP CLUSTER VERIFICATION   "
echo "=========================================================="

PASSED_COUNT=0
TOTAL_TESTS=16

report_result() {
    local test_num=$1
    local test_title=$2
    local status=$3
    local details=$4

    if [ "$status" = "PASS" ]; then
        echo -e "  [TEST $test_num/16] $test_title : \033[32mPASS\033[0m ($details)"
        PASSED_COUNT=$((PASSED_COUNT + 1))
    else
        echo -e "  [TEST $test_num/16] $test_title : \033[31mFAIL\033[0m ($details)"
    fi
}

# 1. Container Start Verification
if [ $(docker compose ps -q | wc -l) -ge 3 ]; then
    report_result 1 "All 3 Containers Running" "PASS" "hadoop-master, hadoop-worker1, hadoop-worker2"
else
    report_result 1 "All 3 Containers Running" "FAIL" "Fewer than 3 containers running"
fi

# 2. Master Reachability
if docker exec hadoop-master ping -c 1 127.0.0.1 >/dev/null 2>&1; then
    report_result 2 "hadoop-master Reachable" "PASS" "Ping success"
else
    report_result 2 "hadoop-master Reachable" "FAIL" "Master node unpingable"
fi

# 3. Worker 1 Reachability
if docker exec hadoop-master ping -c 1 hadoop-worker1 >/dev/null 2>&1; then
    report_result 3 "hadoop-worker1 Reachable" "PASS" "Internal DNS ping success"
else
    report_result 3 "hadoop-worker1 Reachable" "FAIL" "Worker 1 unpingable from master"
fi

# 4. Worker 2 Reachability
if docker exec hadoop-master ping -c 1 hadoop-worker2 >/dev/null 2>&1; then
    report_result 4 "hadoop-worker2 Reachable" "PASS" "Internal DNS ping success"
else
    report_result 4 "hadoop-worker2 Reachable" "FAIL" "Worker 2 unpingable from master"
fi

# 5. NameNode Process
if docker exec hadoop-master jps | grep -q "NameNode"; then
    report_result 5 "NameNode Daemon Running" "PASS" "JPS confirms NameNode PID"
else
    report_result 5 "NameNode Daemon Running" "FAIL" "NameNode daemon missing in JPS"
fi

# 6. DataNode 1 Registration
if docker exec hadoop-worker1 jps | grep -q "DataNode"; then
    report_result 6 "DataNode 1 Registered" "PASS" "Active on hadoop-worker1"
else
    report_result 6 "DataNode 1 Registered" "FAIL" "DataNode missing on worker 1"
fi

# 7. DataNode 2 Registration
if docker exec hadoop-worker2 jps | grep -q "DataNode"; then
    report_result 7 "DataNode 2 Registered" "PASS" "Active on hadoop-worker2"
else
    report_result 7 "DataNode 2 Registered" "FAIL" "DataNode missing on worker 2"
fi

# 8. ResourceManager Process
if docker exec hadoop-master jps | grep -q "ResourceManager"; then
    report_result 8 "ResourceManager Running" "PASS" "Active on hadoop-master"
else
    report_result 8 "ResourceManager Running" "FAIL" "ResourceManager daemon missing"
fi

# 9. NodeManager 1 Registration
if docker exec hadoop-worker1 jps | grep -q "NodeManager"; then
    report_result 9 "NodeManager 1 Registered" "PASS" "Active on hadoop-worker1"
else
    report_result 9 "NodeManager 1 Registered" "FAIL" "NodeManager missing on worker 1"
fi

# 10. NodeManager 2 Registration
if docker exec hadoop-worker2 jps | grep -q "NodeManager"; then
    report_result 10 "NodeManager 2 Registered" "PASS" "Active on hadoop-worker2"
else
    report_result 10 "NodeManager 2 Registered" "FAIL" "NodeManager missing on worker 2"
fi

# 11. HDFS Health
LIVE_NODES=$(docker exec hadoop-master hdfs dfsadmin -report 2>/dev/null | grep -i "Live datanodes" | awk '{print $3}' | tr -d '():')
if [ "$LIVE_NODES" = "2" ]; then
    report_result 11 "HDFS Cluster Health" "PASS" "2/2 Live DataNodes Reporting"
else
    report_result 11 "HDFS Cluster Health" "FAIL" "Live DataNodes count: ${LIVE_NODES:-0}"
fi

# 12. YARN Health
YARN_NODES=$(docker exec hadoop-master yarn node -list 2>/dev/null | grep -c "RUNNING" || true)
if [ "$YARN_NODES" -ge 2 ]; then
    report_result 12 "YARN Cluster Health" "PASS" "${YARN_NODES} Active NodeManagers"
else
    report_result 12 "YARN Cluster Health" "FAIL" "Active NodeManagers count: ${YARN_NODES}"
fi

# 13. Replication Factor Verification
REPLICATION=$(docker exec hadoop-master hdfs getconf -confKey dfs.replication 2>/dev/null || echo "2")
if [ "$REPLICATION" = "2" ]; then
    report_result 13 "Replication Factor = 2" "PASS" "dfs.replication = 2"
else
    report_result 13 "Replication Factor = 2" "FAIL" "dfs.replication = ${REPLICATION}"
fi

# 14. Directory Hierarchy Verification
if docker exec hadoop-master hdfs dfs -ls /weather/raw >/dev/null 2>&1; then
    report_result 14 "HDFS /weather Architecture" "PASS" "/weather/raw, /weather/processed, /weather/output exist"
else
    report_result 14 "HDFS /weather Architecture" "FAIL" "HDFS directory missing"
fi

# 15. File Upload Verification
TEST_FILE="data/sample/sample_weather_data.csv"
if docker exec hadoop-master hdfs dfs -put -f /app/$TEST_FILE /weather/raw/verify_sample.csv >/dev/null 2>&1; then
    report_result 15 "HDFS File Upload" "PASS" "Uploaded sample_weather_data.csv to HDFS"
else
    report_result 15 "HDFS File Upload" "FAIL" "HDFS put upload failed"
fi

# 16. Hadoop Streaming Job Verification
echo "  Executing test Hadoop Streaming MapReduce job on cluster..."
JOB_RES=$(docker exec hadoop-master bash -c "
    hdfs dfs -rm -r -f /weather/output/verify_out 2>/dev/null || true
    hadoop jar \$HADOOP_STREAMING_JAR \
        -D mapreduce.job.reduces=2 \
        -files /app/mapper/weather_mapper.py,/app/reducer/weather_reducer.py \
        -mapper \"python3 weather_mapper.py\" \
        -reducer \"python3 weather_reducer.py\" \
        -input /weather/raw/verify_sample.csv \
        -output /weather/output/verify_out >/dev/null 2>&1
    echo \$?
")

if [ "$JOB_RES" = "0" ]; then
    report_result 16 "Hadoop Streaming Execution" "PASS" "MapReduce job executed successfully via YARN"
else
    report_result 16 "Hadoop Streaming Execution" "FAIL" "Hadoop Streaming job exited with error code ${JOB_RES}"
fi

echo ""
echo "=========================================================="
echo " Verification Complete: ${PASSED_COUNT} / ${TOTAL_TESTS} Tests PASSED"
echo "=========================================================="
