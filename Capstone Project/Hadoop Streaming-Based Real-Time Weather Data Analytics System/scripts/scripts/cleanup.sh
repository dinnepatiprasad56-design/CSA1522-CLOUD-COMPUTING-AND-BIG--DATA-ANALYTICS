#!/usr/bin/env bash
# ==============================================================================
# HDFS and Local Workspace Cleanup Script
# Safely purges temporary batch data, job output artifacts, and rotated logs.
# ==============================================================================

set -e

HDFS_ROOT=${1:-"/weather"}

echo "=========================================================="
echo " Starting Workspace and HDFS Cleanup                      "
echo " HDFS Root Target: $HDFS_ROOT                             "
echo "=========================================================="

# 1. Clean HDFS Output & Temporary Job Directories
if command -v hdfs >/dev/null 2>&1; then
    echo "[1/3] Removing old HDFS MapReduce output directories..."
    hdfs dfs -rm -r -f "${HDFS_ROOT}/output/*" 2>/dev/null || true
    hdfs dfs -rm -r -f "${HDFS_ROOT}/processed/*" 2>/dev/null || true
    echo "  [OK] HDFS output purged."
else
    echo "[1/3] Hadoop CLI not detected. Purging local mock HDFS..."
    rm -rf data/hdfs_mock/weather/output/* 2>/dev/null || true
    rm -rf data/hdfs_mock/weather/processed/* 2>/dev/null || true
fi

# 2. Clean Local Temporary Batches (Retain sample data)
echo "[2/3] Cleaning local generated CSV batches..."
rm -f data/generated/*.csv 2>/dev/null || true

# 3. Clean Python Cache and Runtime Logs
echo "[3/3] Purging Python __pycache__ and scratch files..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true

echo "=========================================================="
echo " Cleanup Completed Successfully!                          "
echo "=========================================================="
