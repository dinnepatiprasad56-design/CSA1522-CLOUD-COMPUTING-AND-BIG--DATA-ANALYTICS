# Google Cloud Platform (GCP) 3-Node Hadoop Cluster Deployment Guide

This guide provides step-by-step instructions for deploying the **Hadoop Streaming Weather Analytics Cluster** on Google Cloud Platform (GCP) Compute Engine virtual machines running Ubuntu Linux.

---

## 1. Cluster Architecture & Sizing

| Node Role | GCP Hostname | Recommended Machine Type | vCPU / RAM | OS | Disk |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Master Node** | `hadoop-master` | `e2-standard-2` | 2 vCPU, 8 GB RAM | Ubuntu 22.04 LTS | 50 GB SSD/Standard |
| **Worker 1** | `hadoop-worker-1` | `e2-standard-2` / `e2-medium` | 2 vCPU, 4–8 GB RAM | Ubuntu 22.04 LTS | 50 GB Standard |
| **Worker 2** | `hadoop-worker-2` | `e2-standard-2` / `e2-medium` | 2 vCPU, 4–8 GB RAM | Ubuntu 22.04 LTS | 50 GB Standard |

---

## 2. GCP VPC Firewall Rules & Port Matrix

Configure the following ingress firewall rules in the Google Cloud Console (`VPC network > Firewall > Create Firewall Rule` or via `gcloud` CLI):

### Internal Cluster Communications (Within VPC Subnet, e.g., `10.128.0.0/20`)
- **Protocol**: `tcp:0-65535,udp:0-65535,icmp`
- **Source Filter**: Subnet CIDR (e.g., `10.128.0.0/20`) or Target Tag `hadoop-cluster`

### External Web Monitoring Endpoints (Restricted to Authorized Admin IPs)

| Port | Protocol | Service | Description |
| :---: | :---: | :--- | :--- |
| **22** | TCP | SSH | Remote management and deployment |
| **9870** | TCP | HDFS NameNode Web UI | HDFS filesystem explorer and live datanode status |
| **8088** | TCP | YARN ResourceManager UI | YARN cluster applications, memory, and vcores tracker |
| **19888** | TCP | JobHistory Server Web UI | Historical MapReduce execution analytics |
| **8501** | TCP | Streamlit Dashboard | Weather analytics, charts, and real-time alert web interface |
| **9864** | TCP | HDFS DataNode Web UI | DataNode HTTP block viewer |

```bash
# GCP gcloud CLI command to open monitoring ports:
gcloud compute firewall-rules create allow-hadoop-web-monitoring \
    --network=default \
    --allow=tcp:22,tcp:9870,tcp:8088,tcp:19888,tcp:8501 \
    --source-ranges=0.0.0.0/0 \
    --target-tags=hadoop-master
```

---

## 3. Step-by-Step Deployment Instructions

### Step 1: Provision Compute Engine VMs
Create 3 Ubuntu 22.04 LTS VMs in the same GCP region and zone (e.g. `us-central1-a`):
```bash
# Master VM
gcloud compute instances create hadoop-master \
    --zone=us-central1-a \
    --machine-type=e2-standard-2 \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=50GB \
    --tags=hadoop-cluster,hadoop-master

# Worker 1 VM
gcloud compute instances create hadoop-worker-1 \
    --zone=us-central1-a \
    --machine-type=e2-standard-2 \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=50GB \
    --tags=hadoop-cluster

# Worker 2 VM
gcloud compute instances create hadoop-worker-2 \
    --zone=us-central1-a \
    --machine-type=e2-standard-2 \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=50GB \
    --tags=hadoop-cluster
```

---

### Step 2: Note Down VM Private and Public IPs
Run `gcloud compute instances list` to record:
- `hadoop-master`: Internal IP (e.g., `10.128.0.2`), External IP
- `hadoop-worker-1`: Internal IP (e.g., `10.128.0.3`)
- `hadoop-worker-2`: Internal IP (e.g., `10.128.0.4`)

---

### Step 3: Configure Environment Variables
On **all 3 nodes**, clone the repository and configure `.env`:
```bash
git clone <repository_url> weather-hadoop-capstone
cd weather-hadoop-capstone
cp .env.example .env
nano .env
```
Populate `.env` with the recorded private IPs:
```ini
MASTER_PRIVATE_IP=10.128.0.2
WORKER1_PRIVATE_IP=10.128.0.3
WORKER2_PRIVATE_IP=10.128.0.4
```

---

### Step 4: Run Automated Master Setup (On `hadoop-master`)
```bash
chmod +x scripts/*.sh
./scripts/setup_master.sh
```
*This script will:*
1. Install Java 8 OpenJDK, wget, curl, pdsh, python3.
2. Download and install Apache Hadoop 3.3.6 in `/usr/local/hadoop`.
3. Configure `/etc/hosts` with cluster private IP mappings.
4. Generate passwordless SSH keys (`~/.ssh/id_rsa`).
5. Deploy `core-site.xml`, `hdfs-site.xml`, `mapred-site.xml`, `yarn-site.xml`, and `workers`.
6. Format the HDFS NameNode metadata.
7. Print the Master's Public SSH key.

---

### Step 5: Run Automated Worker Setup (On `hadoop-worker-1` and `hadoop-worker-2`)
On **Worker 1**:
```bash
chmod +x scripts/*.sh
./scripts/setup_worker.sh
```
On **Worker 2**:
```bash
chmod +x scripts/*.sh
./scripts/setup_worker.sh
```

---

### Step 6: Authorize Master SSH Key on Workers
Copy the Master's public key (printed at the end of `setup_master.sh`) and append it to `~/.ssh/authorized_keys` on both Worker 1 and Worker 2:
```bash
# On hadoop-worker-1 and hadoop-worker-2:
echo "<PASTE_MASTER_ID_RSA_PUB_KEY_HERE>" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

From **`hadoop-master`**, test passwordless SSH connectivity:
```bash
ssh hadoop-worker-1 "echo '[OK] Connected to Worker 1'"
ssh hadoop-worker-2 "echo '[OK] Connected to Worker 2'"
```

---

### Step 7: Start the Hadoop Cluster (On `hadoop-master`)
```bash
./scripts/start_cluster.sh
```
*This script starts:*
- HDFS NameNode, SecondaryNameNode, and remote DataNodes
- YARN ResourceManager and remote NodeManagers
- MapReduce JobHistory Server
- Prepares `/weather/raw`, `/weather/processed`, `/weather/output` directories in HDFS

---

### Step 8: Verify Cluster Health & Active Nodes
```bash
./scripts/monitor_cluster.sh
```
**Expected Verification Checklist:**
1. **Master JPS**: `NameNode`, `ResourceManager`, `SecondaryNameNode`, `JobHistoryServer`.
2. **Worker 1 JPS**: `DataNode`, `NodeManager`.
3. **Worker 2 JPS**: `DataNode`, `NodeManager`.
4. **HDFS dfsadmin report**: `Live datanodes (2)`.
5. **YARN node list**: `Total Nodes:2`.

---

### Step 9: Stop the Cluster
```bash
./scripts/stop_cluster.sh
```
