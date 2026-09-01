# ==============================================================================
# Hadoop Environment Configuration (hadoop-env.sh)
# Cloud Production Profile for Ubuntu Linux Cluster
# ==============================================================================

# Java Runtime Environment
export JAVA_HOME=${JAVA_HOME:-/usr/lib/jvm/java-8-openjdk-amd64}

# Hadoop Core Directories
export HADOOP_HOME=${HADOOP_HOME:-/usr/local/hadoop}
export HADOOP_CONF_DIR=${HADOOP_CONF_DIR:-${HADOOP_HOME}/etc/hadoop}
export HADOOP_LOG_DIR=${HADOOP_LOG_DIR:-${HADOOP_HOME}/logs}
export HADOOP_PID_DIR=${HADOOP_PID_DIR:-/tmp/hadoop-pids}

# JVM Memory and Optimization Settings
export HADOOP_HEAPSIZE_MAX=1024m
export HADOOP_HEAPSIZE_MIN=512m
export HADOOP_NAMENODE_OPTS="-Xmx1024m -XX:+UseG1GC -XX:+ExplicitGCInvokesConcurrent"
export HADOOP_DATANODE_OPTS="-Xmx1024m -XX:+UseG1GC"
export HADOOP_SECONDARYNAMENODE_OPTS="-Xmx1024m -XX:+UseG1GC"

# Native Hadoop Libraries
export HADOOP_COMMON_LIB_NATIVE_DIR=${HADOOP_HOME}/lib/native
export HADOOP_OPTS="${HADOOP_OPTS} -Djava.library.path=${HADOOP_HOME}/lib/native"

# Security & User Privilege Defaults
export HADOOP_SECURE_DN_USER=""
export HDFS_NAMENODE_USER=${HDFS_NAMENODE_USER:-$USER}
export HDFS_DATANODE_USER=${HDFS_DATANODE_USER:-$USER}
export HDFS_SECONDARYNAMENODE_USER=${HDFS_SECONDARYNAMENODE_USER:-$USER}
export YARN_RESOURCEMANAGER_USER=${YARN_RESOURCEMANAGER_USER:-$USER}
export YARN_NODEMANAGER_USER=${YARN_NODEMANAGER_USER:-$USER}
