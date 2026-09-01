#!/usr/bin/env bash
# ==============================================================================
# Hadoop Cluster Diagnostics and Health Verification Script
# Checks JPS daemons across all 3 nodes, HDFS capacity, and YARN resource state.
# ==============================================================================

export HADOOP_HOME=/usr/local/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:/usr/lib/jvm/java-8-openjdk-amd64/bin

echo "=========================================================="
echo "      HADOOP CLUSTER HEALTH & STATUS REPORT               "
echo "=========================================================="

# 1. Check Master Node Daemons
echo ""
echo "--- 1. MASTER NODE DAEMONS (hadoop-master) ---"
if command -v jps >/dev/null 2>&1; then
    jps | grep -E "NameNode|ResourceManager|SecondaryNameNode|JobHistoryServer|Jps" || echo "No Hadoop Master daemons running!"
else
    echo "JPS command not found in PATH."
fi

# 2. Check Worker Node Daemons
echo ""
echo "--- 2. WORKER NODE DAEMONS ---"
for worker in hadoop-worker-1 hadoop-worker-2; do
    echo "[$worker]:"
    ssh -o ConnectTimeout=5 -o BatchMode=yes "$worker" "jps | grep -E 'DataNode|NodeManager|Jps'" 2>/dev/null || echo "  Unable to query $worker via SSH"
done

# 3. HDFS Live DataNode and Capacity Report
echo ""
echo "--- 3. HDFS CLUSTER STATUS (dfsadmin) ---"
if command -v hdfs >/dev/null 2>&1; then
    hdfs dfsadmin -report | head -n 25 || echo "HDFS dfsadmin report failed."
else
    echo "HDFS command not available."
fi

# 4. YARN NodeManager State
echo ""
echo "--- 4. YARN ACTIVE NODES (yarn node -list) ---"
if command -v yarn >/dev/null 2>&1; then
    yarn node -list || echo "YARN node list failed."
else
    echo "YARN command not available."
fi

# 5. HDFS Weather Directory Inspection
echo ""
echo "--- 5. HDFS /weather DIRECTORY LISTING ---"
if command -v hdfs >/dev/null 2>&1; then
    hdfs dfs -ls -R /weather || echo "HDFS directory /weather not reachable."
fi

echo ""
echo "=========================================================="
echo " Diagnostics Completed.                                   "
echo "=========================================================="
