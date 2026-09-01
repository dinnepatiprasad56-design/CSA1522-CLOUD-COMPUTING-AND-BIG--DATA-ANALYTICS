#!/usr/bin/env bash
# ==============================================================================
# Hadoop Streaming Rainfall Analytics Runner
# Computes Total Rainfall, Max Rainfall Event, and Rain Frequency grouped by City
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

INPUT_PATH=${1:-"/weather/raw"}
OUTPUT_PATH=${2:-"/weather/output/rainfall"}
REDUCERS=${3:-2}

bash "$PROJECT_ROOT/scripts/run_streaming.sh" \
    "$PROJECT_ROOT/mapper/rainfall_mapper.py" \
    "$PROJECT_ROOT/reducer/rainfall_reducer.py" \
    "$INPUT_PATH" \
    "$OUTPUT_PATH" \
    "$REDUCERS"
