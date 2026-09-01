#!/usr/bin/env bash
# ==============================================================================
# Hadoop Streaming Job Runner Utility
# Submits Python Mapper and Reducer jobs to the YARN Cluster.
# ==============================================================================

set -e

# Default Paths & Environment
HADOOP_HOME=${HADOOP_HOME:-/usr/local/hadoop}
STREAMING_JAR=${HADOOP_STREAMING_JAR:-$(find $HADOOP_HOME/share/hadoop/tools/lib/ -name "hadoop-streaming-*.jar" | head -n 1)}

if [ -z "$STREAMING_JAR" ] || [ ! -f "$STREAMING_JAR" ]; then
    echo "[ERROR] Hadoop Streaming JAR not found in $HADOOP_HOME/share/hadoop/tools/lib/"
    echo "Please set HADOOP_STREAMING_JAR environment variable."
    exit 1
fi

MAPPER_SCRIPT=$1
REDUCER_SCRIPT=$2
HDFS_INPUT=$3
HDFS_OUTPUT=$4
NUM_REDUCERS=${5:-2}

if [ -z "$MAPPER_SCRIPT" ] || [ -z "$REDUCER_SCRIPT" ] || [ -z "$HDFS_INPUT" ] || [ -z "$HDFS_OUTPUT" ]; then
    echo "Usage: $0 <mapper_path> <reducer_path> <hdfs_input_dir> <hdfs_output_dir> [num_reducers]"
    echo "Example: $0 mapper/temperature_mapper.py reducer/temperature_reducer.py /weather/raw /weather/output/temperature 2"
    exit 1
fi

echo "=========================================================="
echo " Submitting Hadoop Streaming MapReduce Job                "
echo " Streaming JAR : $STREAMING_JAR                           "
echo " Mapper        : $MAPPER_SCRIPT                           "
echo " Reducer       : $REDUCER_SCRIPT                          "
echo " Input Path    : $HDFS_INPUT                              "
echo " Output Path   : $HDFS_OUTPUT                             "
echo " Num Reducers  : $NUM_REDUCERS                            "
echo "=========================================================="

# Remove existing output path if present (Hadoop MapReduce requirement)
echo "[INFO] Cleaning up existing HDFS output directory $HDFS_OUTPUT..."
hdfs dfs -rm -r -f "$HDFS_OUTPUT" || true

# Execute Hadoop Streaming MapReduce Job
echo "[INFO] Executing MapReduce Job via YARN..."
hadoop jar "$STREAMING_JAR" \
    -D mapreduce.job.name="WeatherAnalytics_$(basename $MAPPER_SCRIPT .py)" \
    -D mapreduce.job.reduces="$NUM_REDUCERS" \
    -files "$MAPPER_SCRIPT,$REDUCER_SCRIPT" \
    -mapper "python3 $(basename $MAPPER_SCRIPT)" \
    -reducer "python3 $(basename $REDUCER_SCRIPT)" \
    -input "$HDFS_INPUT" \
    -output "$HDFS_OUTPUT"

echo ""
echo "=========================================================="
echo " Job Finished. Output Directory Contents:                 "
hdfs dfs -ls "$HDFS_OUTPUT"
echo ""
echo " Sample Analytics Output:                                 "
hdfs dfs -cat "$HDFS_OUTPUT/part-*" | head -n 10
echo "=========================================================="
