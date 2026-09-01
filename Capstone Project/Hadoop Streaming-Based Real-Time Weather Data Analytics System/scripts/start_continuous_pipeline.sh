#!/usr/bin/env bash
# ==============================================================================
# Near-Real-Time Continuous Weather Analytics Daemon Runner
# Runs the dual-loop ingestion & periodic Hadoop Streaming pipeline.
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

INGEST_INTERVAL=${1:-"5"}
PROC_INTERVAL=${2:-"20"}
SOURCE_MODE=${3:-"SIMULATOR"}
ANOMALY_RATIO=${4:-"0.08"}

echo "=========================================================="
echo " Starting Near-Real-Time Weather Analytics Pipeline Daemon "
echo " Ingestion Interval   : ${INGEST_INTERVAL}s              "
echo " MapReduce Processing : ${PROC_INTERVAL}s              "
echo " Source Mode          : ${SOURCE_MODE}                   "
echo " Anomaly Ratio        : ${ANOMALY_RATIO}                 "
echo "=========================================================="

python3 "$PROJECT_ROOT/ingestion/continuous_pipeline.py" \
    --ingest-interval "$INGEST_INTERVAL" \
    --proc-interval "$PROC_INTERVAL" \
    --source "$SOURCE_MODE" \
    --anomaly-ratio "$ANOMALY_RATIO"
