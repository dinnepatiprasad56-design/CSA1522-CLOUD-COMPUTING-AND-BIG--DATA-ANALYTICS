#!/usr/bin/env bash

set -e

echo "[ENTRYPOINT] Starting SSH Daemon..."
service ssh start || /usr/sbin/sshd

echo "[ENTRYPOINT] Deploying Hadoop XML configurations from /app/docker/config..."
if [ -d "/app/docker/config" ]; then
    cp -f /app/docker/config/* /usr/local/hadoop/etc/hadoop/ 2>/dev/null || true
fi

export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export HADOOP_HOME=/usr/local/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$JAVA_HOME/bin

ROLE=${ROLE:-master}

echo "[ENTRYPOINT] Container initialized with ROLE=${ROLE}"

if [ "$ROLE" = "master" ]; then

    # ------------------------------------------------------------
    # NameNode metadata
    # ------------------------------------------------------------
    if [ ! -d "/hadoop/dfs/name/current" ] && \
       [ ! -f "/hadoop/dfs/name/formatted.marker" ]; then

        echo "[ENTRYPOINT] Formatting NameNode metadata..."
        hdfs namenode -format -force -nonInteractive
        touch /hadoop/dfs/name/formatted.marker

    else
        echo "[ENTRYPOINT] Existing HDFS NameNode metadata detected."
    fi

    # ------------------------------------------------------------
    # Start NameNode directly
    # ------------------------------------------------------------
    echo "[ENTRYPOINT] Starting NameNode..."
    hdfs --daemon start namenode

    # ------------------------------------------------------------
    # Start ResourceManager directly
    # ------------------------------------------------------------
    echo "[ENTRYPOINT] Starting ResourceManager..."
    yarn --daemon start resourcemanager

    # ------------------------------------------------------------
    # Start JobHistory Server
    # ------------------------------------------------------------
    echo "[ENTRYPOINT] Starting JobHistory Server..."
    mapred --daemon start historyserver || true

    # ------------------------------------------------------------
    # Wait for NameNode RPC
    # ------------------------------------------------------------
    echo "[ENTRYPOINT] Waiting for NameNode..."

    for i in {1..30}; do
        if hdfs dfs -ls / >/dev/null 2>&1; then
            echo "[ENTRYPOINT] NameNode is ready."
            break
        fi

        echo "[ENTRYPOINT] Waiting for NameNode... ($i/30)"
        sleep 2
    done

    # ------------------------------------------------------------
    # Initialize HDFS directories
    # ------------------------------------------------------------
    echo "[ENTRYPOINT] Initializing HDFS /weather structure..."

    hdfs dfs -mkdir -p /weather
    hdfs dfs -mkdir -p /weather/raw
    hdfs dfs -mkdir -p /weather/processed
    hdfs dfs -mkdir -p /weather/output
    hdfs dfs -mkdir -p /weather/archive
    hdfs dfs -mkdir -p /weather/logs

    hdfs dfs -chmod -R 777 /weather 2>/dev/null || true

    echo "[ENTRYPOINT] HDFS /weather directories ready."
    echo "[ENTRYPOINT] Master node initialization complete."

    # Keep container alive
    tail -f /dev/null

elif [ "$ROLE" = "worker" ]; then

    # ------------------------------------------------------------
    # Start DataNode directly
    # ------------------------------------------------------------
    echo "[ENTRYPOINT] Starting DataNode..."
    hdfs --daemon start datanode

    # ------------------------------------------------------------
    # Start NodeManager directly
    # ------------------------------------------------------------
    echo "[ENTRYPOINT] Starting NodeManager..."
    yarn --daemon start nodemanager

    echo "[ENTRYPOINT] Worker Hadoop services started."

    # Keep container alive
    tail -f /dev/null

else
    exec "$@"
fi
