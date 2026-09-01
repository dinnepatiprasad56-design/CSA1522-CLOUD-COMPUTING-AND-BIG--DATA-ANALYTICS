#!/usr/bin/env bash
# ==============================================================================
# Hadoop Streaming Atmospheric Pressure Analytics Runner
# Computes Average, Min, and Max Barometric Pressure grouped by City
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

INPUT_PATH=${1:-"/weather/raw"}
OUTPUT_PATH=${2:-"/weather/output/pressure"}
REDUCERS=${3:-2}

bash "$PROJECT_ROOT/scripts/run_streaming.sh" \
    "$PROJECT_ROOT/mapper/pressure_mapper.py" \
    "$PROJECT_ROOT/reducer/pressure_reducer.py" \
    "$INPUT_PATH" \
    "$OUTPUT_PATH" \
    "$REDUCERS"
