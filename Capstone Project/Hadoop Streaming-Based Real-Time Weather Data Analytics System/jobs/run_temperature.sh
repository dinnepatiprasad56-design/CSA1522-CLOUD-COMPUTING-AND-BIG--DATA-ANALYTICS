#!/usr/bin/env bash
# ==============================================================================
# Hadoop Streaming Temperature Analytics Runner
# Computes Average, Min, and Max temperatures grouped by City
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

INPUT_PATH=${1:-"/weather/raw"}
OUTPUT_PATH=${2:-"/weather/output/temperature"}
REDUCERS=${3:-2}

bash "$PROJECT_ROOT/scripts/run_streaming.sh" \
    "$PROJECT_ROOT/mapper/temperature_mapper.py" \
    "$PROJECT_ROOT/reducer/temperature_reducer.py" \
    "$INPUT_PATH" \
    "$OUTPUT_PATH" \
    "$REDUCERS"
