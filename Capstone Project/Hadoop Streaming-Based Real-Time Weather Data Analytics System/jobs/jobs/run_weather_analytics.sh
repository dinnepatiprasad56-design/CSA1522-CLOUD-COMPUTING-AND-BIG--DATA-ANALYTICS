#!/usr/bin/env bash
# ==============================================================================
# Master Weather Analytics Pipeline Runner
# End-to-End Workflow:
# Raw Weather Data -> HDFS Raw Directory -> Hadoop Streaming MapReduce ->
# Python Mapper -> YARN Shuffle/Sort -> Python Reducer -> HDFS Output -> Local Export
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Load Configuration & Environment
if [ -f "$PROJECT_ROOT/.env" ]; then
    set -a
    source "$PROJECT_ROOT/.env"
    set +a
fi

# Configurable Parameters with Intelligent Defaults
RAW_INPUT_FILE=${1:-"$PROJECT_ROOT/data/sample/sample_weather_data.csv"}
HDFS_INPUT_DIR=${2:-"/weather/raw"}
HDFS_OUTPUT_DIR=${3:-"/weather/output/analytics_summary"}
NUM_REDUCERS=${4:-2}
LOCAL_EXPORT_PATH=${5:-"$PROJECT_ROOT/data/processed/analytics_summary.csv"}

LOG_FILE="$PROJECT_ROOT/data/pipeline_execution.log"
mkdir -p "$PROJECT_ROOT/data/processed"

echo "=========================================================="
echo "    STARTING COMPLETE HADOOP WEATHER ANALYTICS PIPELINE   "
echo "=========================================================="
echo " Timestamp        : $(date '+%Y-%m-%d %H:%M:%S')"
echo " Raw Source File  : $RAW_INPUT_FILE"
echo " HDFS Input Path  : $HDFS_INPUT_DIR"
echo " HDFS Output Path : $HDFS_OUTPUT_DIR"
echo " Reducers Count   : $NUM_REDUCERS"
echo " Local Export CSV : $LOCAL_EXPORT_PATH"
echo " Log Destination  : $LOG_FILE"
echo "=========================================================="

# ------------------------------------------------------------------------------
# STEP 1: HDFS Directory Initialization
# ------------------------------------------------------------------------------
echo ""
echo "[STEP 1/5] Initializing HDFS Directory Architecture..."
if command -v hdfs >/dev/null 2>&1; then
    hdfs dfs -mkdir -p /weather/raw
    hdfs dfs -mkdir -p /weather/processed
    hdfs dfs -mkdir -p /weather/output
    hdfs dfs -mkdir -p /weather/archive
    hdfs dfs -mkdir -p /weather/logs
    echo "  [OK] HDFS hierarchy verified."
else
    echo "  [INFO] Hadoop CLI not detected in system. Using local simulated HDFS."
    mkdir -p "$PROJECT_ROOT/data/hdfs_mock/weather/raw"
    mkdir -p "$PROJECT_ROOT/data/hdfs_mock/weather/output"
    mkdir -p "$PROJECT_ROOT/data/hdfs_mock/weather/processed"
fi

# ------------------------------------------------------------------------------
# STEP 2: Raw Weather Data Validation & HDFS Upload
# ------------------------------------------------------------------------------
echo ""
echo "[STEP 2/5] Uploading Validated Weather Data to HDFS..."
if [ -f "$RAW_INPUT_FILE" ]; then
    python3 "$PROJECT_ROOT/ingestion/hdfs_uploader.py" --file "$RAW_INPUT_FILE" --hdfs-root "/weather"
    echo "  [OK] Ingested '$RAW_INPUT_FILE' to $HDFS_INPUT_DIR"
else
    echo "  [WARN] Source file '$RAW_INPUT_FILE' not found. Using existing HDFS contents."
fi

# ------------------------------------------------------------------------------
# STEP 3: Clean Previous Output
# ------------------------------------------------------------------------------
echo ""
echo "[STEP 3/5] Purging Previous MapReduce Output ($HDFS_OUTPUT_DIR)..."
if command -v hdfs >/dev/null 2>&1; then
    hdfs dfs -rm -r -f "$HDFS_OUTPUT_DIR" 2>/dev/null || true
else
    rm -rf "$PROJECT_ROOT/data/hdfs_mock${HDFS_OUTPUT_DIR}" 2>/dev/null || true
fi
echo "  [OK] Ready for fresh job output."

# ------------------------------------------------------------------------------
# STEP 4: Submit & Execute Hadoop Streaming MapReduce Job
# ------------------------------------------------------------------------------

echo ""
echo "[STEP 4/5] Executing Hadoop Streaming MapReduce Job..."

MAPPER="$PROJECT_ROOT/mapper/weather_mapper.py"
REDUCER="$PROJECT_ROOT/reducer/weather_reducer.py"

if command -v hadoop >/dev/null 2>&1 && [ -n "$HADOOP_HOME" ]; then

    STREAMING_JAR=${HADOOP_STREAMING_JAR:-$(find "$HADOOP_HOME/share/hadoop/tools/lib/" \
        -name "hadoop-streaming-*.jar" | head -n 1)}

    echo "  Executing on YARN via $STREAMING_JAR..."

    # The uploader stores files using:
    # /weather/raw/YYYY/MM/DD/<filename>
    #
    # Therefore, use today's partition as the MapReduce input directory.
    if [ "$HDFS_INPUT_DIR" = "/weather/raw" ]; then
        TODAY_PARTITION="$(date '+%Y/%m/%d')"
        MAPREDUCE_INPUT="$HDFS_INPUT_DIR/$TODAY_PARTITION"
    else
        MAPREDUCE_INPUT="$HDFS_INPUT_DIR"
    fi

    echo "  MapReduce Input Directory: $MAPREDUCE_INPUT"

    # Verify that the partition exists and contains files.
    if ! hdfs dfs -test -e "$MAPREDUCE_INPUT"; then
        echo "  [ERROR] HDFS input directory does not exist: $MAPREDUCE_INPUT"
        exit 1
    fi

    echo "  Input files:"
    hdfs dfs -ls "$MAPREDUCE_INPUT"

    echo ""
    echo "  Submitting Hadoop Streaming job..."

    set +e

    hadoop jar "$STREAMING_JAR" \
        -D mapreduce.job.name="Master_Weather_Analytics" \
        -D mapreduce.job.reduces="$NUM_REDUCERS" \
        -files "$MAPPER,$REDUCER" \
        -mapper "python3 $(basename "$MAPPER")" \
        -reducer "python3 $(basename "$REDUCER")" \
        -input "$MAPREDUCE_INPUT" \
        -output "$HDFS_OUTPUT_DIR" 2>&1 | tee -a "$LOG_FILE"

    HADOOP_EXIT_CODE=${PIPESTATUS[0]}

    set -e

    if [ "$HADOOP_EXIT_CODE" -ne 0 ]; then
        echo "  [ERROR] Hadoop Streaming job failed with exit code $HADOOP_EXIT_CODE"
        exit "$HADOOP_EXIT_CODE"
    fi

    echo "  [OK] Hadoop Streaming job completed."

    # Retrieve output from HDFS
    echo "  Retrieving results from HDFS..."

    RAW_OUTPUT_TMP="/tmp/weather_raw_analytics.tsv"

    hdfs dfs -cat "$HDFS_OUTPUT_DIR/part-*" > "$RAW_OUTPUT_TMP"

    if [ ! -s "$RAW_OUTPUT_TMP" ]; then
        echo "  [ERROR] Hadoop completed but produced no analytics output."
        exit 1
    fi

else

    echo "  [SIMULATION] Executing streaming MapReduce pipeline locally via UNIX pipes..."

    RAW_OUTPUT_TMP="/tmp/weather_raw_analytics.tsv"

    cat "$RAW_INPUT_FILE" \
        | python3 "$MAPPER" \
        | sort \
        | python3 "$REDUCER" \
        > "$RAW_OUTPUT_TMP"

    echo "  [OK] Local MapReduce execution completed."

fi

# ------------------------------------------------------------------------------
# STEP 5: Format and Export Analytics to CSV
# ------------------------------------------------------------------------------
echo ""
echo "[STEP 5/5] Formatting Processed Analytics for Dashboard Consumption..."

# CSV Header definitions for multi-metric summary
CSV_HEADER="city,record_count,avg_temperature,min_temperature,max_temperature,avg_humidity,min_humidity,max_humidity,total_rainfall,max_rainfall,avg_wind_speed,max_wind_speed,avg_pressure,min_pressure,anomalies_count"

echo "$CSV_HEADER" > "$LOCAL_EXPORT_PATH"
# Convert TAB delimiters to CSV commas
awk -F'\t' '{OFS=","; print $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15}' "$RAW_OUTPUT_TMP" >> "$LOCAL_EXPORT_PATH"

echo "  [OK] Exported clean analytics to $LOCAL_EXPORT_PATH"

# ------------------------------------------------------------------------------
# Final Analytics Summary Inspection
# ------------------------------------------------------------------------------
echo ""
echo "=========================================================="
echo "               FINAL ANALYTICS SUMMARY REPORT             "
echo "=========================================================="
cat "$LOCAL_EXPORT_PATH"
echo "=========================================================="
echo " Pipeline Finished Successfully at $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================================="
