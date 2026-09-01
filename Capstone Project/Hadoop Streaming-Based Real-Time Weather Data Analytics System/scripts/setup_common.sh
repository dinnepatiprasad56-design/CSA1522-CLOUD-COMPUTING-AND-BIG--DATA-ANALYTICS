#!/usr/bin/env bash
# ==============================================================================
# Common Ubuntu VM Provisioning Script for Hadoop 3.x Node
# Runs on Master and all Worker Nodes
# ==============================================================================

set -e

echo "=========================================================="
echo " Starting Common Hadoop Node Provisioning (Ubuntu Linux)  "
echo "=========================================================="

# 1. Update Package Repositories
echo "[1/6] Updating APT repositories..."
sudo apt-get update -y
sudo apt-get install -y openjdk-8-jdk wget curl pdsh ssh rsync net-tools python3 python3-pip python3-venv

# 2. Configure Java Environment
export JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64"
if ! grep -q "JAVA_HOME" /etc/environment; then
    echo "JAVA_HOME=\"/usr/lib/jvm/java-8-openjdk-amd64\"" | sudo tee -a /etc/environment
fi

# 3. Setup Hadoop Target Directories
HADOOP_VERSION="3.3.6"
HADOOP_INSTALL_DIR="/usr/local/hadoop"

if [ ! -d "$HADOOP_INSTALL_DIR" ]; then
    echo "[2/6] Downloading Apache Hadoop ${HADOOP_VERSION}..."
    wget -q --show-progress "https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz" -O /tmp/hadoop.tar.gz

    echo "[3/6] Extracting Hadoop to ${HADOOP_INSTALL_DIR}..."
    sudo tar -xzf /tmp/hadoop.tar.gz -C /usr/local/
    sudo mv "/usr/local/hadoop-${HADOOP_VERSION}" "$HADOOP_INSTALL_DIR"
    sudo chown -R "$USER":"$USER" "$HADOOP_INSTALL_DIR"
    rm -f /tmp/hadoop.tar.gz
else
    echo "[2/6] Hadoop already installed at ${HADOOP_INSTALL_DIR}. Skipping download."
fi

# 4. Create HDFS Data and Log Directories
echo "[4/6] Creating HDFS storage directories..."
mkdir -p "${HADOOP_INSTALL_DIR}/data/hdfs/namenode"
mkdir -p "${HADOOP_INSTALL_DIR}/data/hdfs/datanode"
mkdir -p "${HADOOP_INSTALL_DIR}/data/hdfs/namesecondary"
mkdir -p "${HADOOP_INSTALL_DIR}/data/tmp"
mkdir -p "${HADOOP_INSTALL_DIR}/logs"
chmod -R 755 "${HADOOP_INSTALL_DIR}/data"

# 5. Export Environment Variables for User Session
echo "[5/6] Exporting Hadoop & Java environment variables..."
ENV_FILE="$HOME/.hadoop_env"
cat << 'EOF' > "$ENV_FILE"
# Hadoop & Java Runtime Environment
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export HADOOP_HOME=/usr/local/hadoop
export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native"
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$JAVA_HOME/bin
EOF

if ! grep -q ".hadoop_env" "$HOME/.bashrc"; then
    echo "source $ENV_FILE" >> "$HOME/.bashrc"
fi
source "$ENV_FILE"

# 6. Configure Passwordless SSH Localhost Access
echo "[6/6] Configuring SSH daemon..."
sudo systemctl enable ssh
sudo systemctl start ssh

echo "=========================================================="
echo " Common Hadoop Node Provisioning Completed Successfully!  "
echo "=========================================================="
