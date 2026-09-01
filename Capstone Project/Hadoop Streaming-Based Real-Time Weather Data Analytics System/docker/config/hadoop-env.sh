# ==============================================================================
# Hadoop Environment Configuration (hadoop-env.sh) for Docker Containers
# ==============================================================================

export JAVA_HOME=${JAVA_HOME:-/usr/lib/jvm/java-8-openjdk-amd64}
export HADOOP_HOME=${HADOOP_HOME:-/usr/local/hadoop}
export HADOOP_CONF_DIR=${HADOOP_CONF_DIR:-${HADOOP_HOME}/etc/hadoop}
export HADOOP_LOG_DIR=${HADOOP_LOG_DIR:-${HADOOP_HOME}/logs}
export HADOOP_PID_DIR=${HADOOP_PID_DIR:-/tmp/hadoop-pids}

# JVM Memory Settings optimized for Containers
export HADOOP_HEAPSIZE_MAX=512m
export HADOOP_HEAPSIZE_MIN=256m
export HADOOP_NAMENODE_OPTS="-Xmx512m -XX:+UseG1GC"
export HADOOP_DATANODE_OPTS="-Xmx512m -XX:+UseG1GC"
export HADOOP_SECONDARYNAMENODE_OPTS="-Xmx512m -XX:+UseG1GC"

# Daemon Privileges
export HDFS_NAMENODE_USER=root
export HDFS_DATANODE_USER=root
export HDFS_SECONDARYNAMENODE_USER=root
export YARN_RESOURCEMANAGER_USER=root
export YARN_NODEMANAGER_USER=root
