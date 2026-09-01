#!/usr/bin/env bash
# ==============================================================================
# Hadoop Streaming Wind Speed Analytics Runner
# Computes Average and Maximum Wind Velocities grouped by City
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

INPUT_PATH=${1:-"/weather/raw"}
OUTPUT_PATH=${2:-"/weather/output/wind"}
REDUCERS=${3:-2}

bash "$PROJECT_ROOT/scripts/run_streaming.sh" \
    "$PROJECT_ROOT/mapper/wind_mapper.py" \
    "$PROJECT_ROOT/reducer/wind_reducer.py" \
    "$INPUT_PATH" \
    "$OUTPUT_PATH" \
    "$REDUCERS"
