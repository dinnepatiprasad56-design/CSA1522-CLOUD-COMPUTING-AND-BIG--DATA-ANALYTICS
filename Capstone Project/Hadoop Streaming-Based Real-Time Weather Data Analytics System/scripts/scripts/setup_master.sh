#!/usr/bin/env bash
# ==============================================================================
# Hadoop Master Node Automated Deployment Script
# Configures Master Node (NameNode, ResourceManager, JobHistoryServer)
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
echo " Starting Hadoop MASTER Node Configuration                "
echo " Master Private IP   : $MASTER_IP                         "
echo " Worker 1 Private IP : $WORKER1_IP                         "
echo " Worker 2 Private IP : $WORKER2_IP                         "
echo "=========================================================="

# 1. Run Common Setup if Hadoop is not present
if [ ! -d "/usr/local/hadoop" ]; then
    echo "[1/6] Running common prerequisites installation..."
    bash "$SCRIPT_DIR/setup_common.sh"
fi

# Load Hadoop Environment
export HADOOP_HOME=/usr/local/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:/usr/lib/jvm/java-8-openjdk-amd64/bin

# 2. Update /etc/hosts with Cluster Private IPs
echo "[2/6] Configuring /etc/hosts for cluster hostname resolution..."
sudo sed -i '/hadoop-master/d' /etc/hosts
sudo sed -i '/hadoop-worker-1/d' /etc/hosts
sudo sed -i '/hadoop-worker-2/d' /etc/hosts

cat << EOF | sudo tee -a /etc/hosts
$MASTER_IP hadoop-master
$WORKER1_IP hadoop-worker-1
$WORKER2_IP hadoop-worker-2
EOF

# 3. Setup Passwordless SSH Keys
echo "[3/6] Setting up Master SSH keys..."
mkdir -p "$HOME/.ssh"
chmod 700 "$HOME/.ssh"
if [ ! -f "$HOME/.ssh/id_rsa" ]; then
    ssh-keygen -t rsa -P "" -f "$HOME/.ssh/id_rsa"
fi
cat "$HOME/.ssh/id_rsa.pub" >> "$HOME/.ssh/authorized_keys"
chmod 600 "$HOME/.ssh/authorized_keys"

# Configure SSH Client for non-interactive host key checking
cat << 'EOF' > "$HOME/.ssh/config"
Host hadoop-master hadoop-worker-1 hadoop-worker-2 localhost 127.0.0.1
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
    LogLevel ERROR
EOF
chmod 600 "$HOME/.ssh/config"

# 4. Deploy XML Configurations to Hadoop Conf Directory
echo "[4/6] Deploying Hadoop XML configurations to $HADOOP_CONF_DIR..."
cp "$PROJECT_ROOT/hadoop/hadoop-env.sh" "$HADOOP_CONF_DIR/"
cp "$PROJECT_ROOT/hadoop/core-site.xml" "$HADOOP_CONF_DIR/"
cp "$PROJECT_ROOT/hadoop/hdfs-site.xml" "$HADOOP_CONF_DIR/"
cp "$PROJECT_ROOT/hadoop/mapred-site.xml" "$HADOOP_CONF_DIR/"
cp "$PROJECT_ROOT/hadoop/yarn-site.xml" "$HADOOP_CONF_DIR/"
cp "$PROJECT_ROOT/hadoop/workers" "$HADOOP_CONF_DIR/"

# 5. Format HDFS NameNode
echo "[5/6] Formatting HDFS NameNode metadata..."
hdfs namenode -format -force -nonInteractive

echo "=========================================================="
echo " Master Node Setup Completed Successfully!                "
echo " Next step: Run setup_worker.sh on Worker 1 and Worker 2. "
echo " Public SSH Key for Workers:"
echo "----------------------------------------------------------"
cat "$HOME/.ssh/id_rsa.pub"
echo "----------------------------------------------------------"
echo "=========================================================="
