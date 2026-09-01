#!/usr/bin/env bash
# ==============================================================================
# Hadoop Cluster Shutdown Script
# Safely stops MapReduce JobHistory Server, YARN, and HDFS Daemons.
# ==============================================================================

export HADOOP_HOME=/usr/local/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:/usr/lib/jvm/java-8-openjdk-amd64/bin

echo "=========================================================="
echo " Stopping Hadoop Weather Analytics Cluster                "
echo "=========================================================="

echo "[1/3] Stopping MapReduce JobHistory Server..."
mapred --daemon stop historyserver || true

echo "[2/3] Stopping YARN Daemons..."
$HADOOP_HOME/sbin/stop-yarn.sh || true

echo "[3/3] Stopping HDFS Daemons..."
$HADOOP_HOME/sbin/stop-dfs.sh || true

echo "=========================================================="
echo " Hadoop Cluster Stopped Safely.                           "
echo "=========================================================="
