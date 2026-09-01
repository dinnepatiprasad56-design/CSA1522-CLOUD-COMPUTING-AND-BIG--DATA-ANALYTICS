#!/usr/bin/env bash
# ==============================================================================
# Hadoop Worker Node Automated Deployment Script
# Configures Worker Node (DataNode, NodeManager)
# ==============================================================================

set -e

# Load Environment Variables from .env if present
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
if [ -f "$PROJECT_ROOT/.env" ]; then
    echo "[INFO] Loading cluster environment from $PROJECT_ROOT/.env..."
    set -a
    source "$PROJECT_ROOT/.env"
    set +a
fi

MASTER_IP=${MASTER_PRIVATE_IP:-"127.0.0.1"}
WORKER1_IP=${WORKER1_PRIVATE_IP:-"127.0.0.1"}
WORKER2_IP=${WORKER2_PRIVATE_IP:-"127.0.0.1"}
HADOOP_CONF_DIR="/usr/local/hadoop/etc/hadoop"

echo "=========================================================="
echo " Starting Hadoop WORKER Node Configuration                "
echo " Master Private IP   : $MASTER_IP                         "
echo " Worker 1 Private IP : $WORKER1_IP                         "
echo " Worker 2 Private IP : $WORKER2_IP                         "
echo "=========================================================="

# 1. Run Common Setup if Hadoop is not present
if [ ! -d "/usr/local/hadoop" ]; then
    echo "[1/4] Running common prerequisites installation..."
    bash "$SCRIPT_DIR/setup_common.sh"
fi

# 2. Update /etc/hosts with Cluster Private IPs
echo "[2/4] Configuring /etc/hosts for cluster hostname resolution..."
sudo sed -i '/hadoop-master/d' /etc/hosts
sudo sed -i '/hadoop-worker-1/d' /etc/hosts
sudo sed -i '/hadoop-worker-2/d' /etc/hosts

cat << EOF | sudo tee -a /etc/hosts
$MASTER_IP hadoop-master
$WORKER1_IP hadoop-worker-1
$WORKER2_IP hadoop-worker-2
EOF

# 3. Setup SSH directory and authorize Master Key
echo "[3/4] Ensuring SSH authorized_keys directory is configured..."
mkdir -p "$HOME/.ssh"
chmod 700 "$HOME/.ssh"
touch "$HOME/.ssh/authorized_keys"
chmod 600 "$HOME/.ssh/authorized_keys"

# 4. Deploy XML Configurations to Hadoop Conf Directory
echo "[4/4] Deploying Hadoop XML configurations to $HADOOP_CONF_DIR..."
cp "$PROJECT_ROOT/hadoop/hadoop-env.sh" "$HADOOP_CONF_DIR/"
cp "$PROJECT_ROOT/hadoop/core-site.xml" "$HADOOP_CONF_DIR/"
cp "$PROJECT_ROOT/hadoop/hdfs-site.xml" "$HADOOP_CONF_DIR/"
cp "$PROJECT_ROOT/hadoop/mapred-site.xml" "$HADOOP_CONF_DIR/"
cp "$PROJECT_ROOT/hadoop/yarn-site.xml" "$HADOOP_CONF_DIR/"
cp "$PROJECT_ROOT/hadoop/workers" "$HADOOP_CONF_DIR/"

# Clean and prepare DataNode storage directory
mkdir -p /usr/local/hadoop/data/hdfs/datanode
chmod 755 /usr/local/hadoop/data/hdfs/datanode

echo "=========================================================="
echo " Worker Node Configuration Completed Successfully!        "
echo " Ensure Master's id_rsa.pub is added to ~/.ssh/authorized_keys"
echo "=========================================================="
