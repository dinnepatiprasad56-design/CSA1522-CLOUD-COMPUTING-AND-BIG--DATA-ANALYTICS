# System Architecture & Technical Specification

> **Capstone Project**: Hadoop Streaming-Based Real-Time Weather Data Analytics System on Cloud Infrastructure

---

## 1. Executive Summary & Processing Model

The system is architected as a **Near-Real-Time / Continuous Distributed Meteorological Analytics Pipeline**. 

Because Apache Hadoop MapReduce is fundamentally a batch-oriented distributed compute engine designed for high throughput over large datasets rather than millisecond-level event streaming, the architecture uses a **micro-batching continuous processing model**:

1. **Continuous Acquisition Layer**: Weather records are continuously ingested from live REST APIs or high-fidelity meteorological simulators and buffered into partitioned directories.
2. **HDFS Distributed Storage**: Time-series batches are staged into `/weather/raw/YYYY/MM/DD/part-*.csv` partitions with a replication factor of 2.
3. **Periodic Hadoop Streaming MapReduce**: A daemon controller triggers periodic MapReduce jobs across accumulated partitions at configurable intervals, preventing overlapping executions via mutex locks.
4. **Analytical Consolidation**: Reducer outputs are extracted to structured analytics files and historical time-series logs.
5. **Interactive Dashboard**: A Streamlit web dashboard serves interactive visualizations and real-time alerts.

---

## 2. End-to-End Data Pipeline Flow

```
+-------------------------------------------------------------------------------+
|                       METEOROLOGICAL DATA GENERATION                          |
|  - OpenWeatherMap REST API / Real-Time Diurnal Weather Simulator              |
|  - 7 Target Indian Metros: Chennai, Bengaluru, Hyderabad, Mumbai, Delhi,      |
|    Kolkata, Pune                                                              |
+---------------------------------------+---------------------------------------+
                                        | (Continuous stream / micro-batches)
                                        v
+-------------------------------------------------------------------------------+
|                    INGESTION & VALIDATION ENGINE (Python 3)                   |
|  - Schema Verification: timestamp, city, temp, hum, rain, wind, press         |
|  - Physical Bounds Filtering (-50°C to 65°C, 0-100% hum, 0-500mm rain)        |
|  - Malformed Record Isolation & Quarantine Logging                            |
+---------------------------------------+---------------------------------------+
                                        |
                                        v
+-------------------------------------------------------------------------------+
|                  DISTRIBUTED FILE SYSTEM STORAGE (HDFS 3.3.6)                 |
|  - NameNode Metadata Coordinator (Port 9870 / RPC 9000)                       |
|  - Partition Hierarchy: /weather/raw/YYYY/MM/DD/weather_batch_*.csv           |
|  - Dual DataNode Block Distribution (Replication = 2, Block Size = 128MB)     |
+---------------------------------------+---------------------------------------+
                                        | (Periodic YARN Job Submission)
                                        v
+-------------------------------------------------------------------------------+
|                      HADOOP STREAMING MAPREDUCE (YARN)                        |
|  - Mapper (Python): Emits city-partitioned key-value pairs (stdin -> stdout)  |
|  - YARN Shuffle & Sort: Grouping and sorting by city key across worker nodes  |
|  - Reducer (Python): Key-transition statistical aggregation & anomaly tally   |
+---------------------------------------+---------------------------------------+
                                        |
                                        v
+-------------------------------------------------------------------------------+
|                       PROCESSED ANALYTICAL DATASETS                           |
|  - /weather/output/analytics_summary/part-* -> data/processed/analytics.csv   |
|  - Historical Trends Archive: data/processed/historical_analytics.csv        |
|  - Job Performance Audit Log: data/processed/job_history.csv                 |
+---------------------------------------+---------------------------------------+
                                        |
                                        v
+-------------------------------------------------------------------------------+
|                  STREAMLIT LIVE VISUALIZATION DASHBOARD                       |
|  - KPI Metric Badges & Weather Summary Matrix Table                           |
|  - Interactive Plotly Visualizations (Temp, Humidity, Rain, Wind, Pressure)   |
|  - 5-Axis Normalized Spider Radar Comparison                                  |
|  - Multi-tier Anomaly Alert Banners (HEATWAVE, FLOOD, CYCLONE, GALE)          |
+-------------------------------------------------------------------------------+
```

---

## 3. Distributed Cloud Cluster Topology

The system is deployed on Google Cloud Platform (GCP) Compute Engine across 3 dedicated virtual machines in a dedicated private Virtual Private Cloud (VPC):

```
                        +-------------------------------+
                        |         HADOOP MASTER         |
                        |       (hadoop-master)         |
                        |  - NameNode (Metadata)        |
                        |  - SecondaryNameNode          |
                        |  - ResourceManager (YARN)     |
                        |  - JobHistory Server          |
                        |  - Ingestion & Streamlit Host |
                        +---------------+---------------+
                                        |
                   +--------------------+--------------------+
                   |                                         |
                   v                                         v
    +------------------------------+          +------------------------------+
    |       HADOOP WORKER 1        |          |       HADOOP WORKER 2        |
    |      (hadoop-worker-1)       |          |      (hadoop-worker-2)       |
    |  - DataNode (Block Storage)  |          |  - DataNode (Block Storage)  |
    |  - NodeManager (Containers)  |          |  - NodeManager (Containers)  |
    +------------------------------+          +------------------------------+
```

---

## 4. Key Architectural Decisions

1. **Hadoop Streaming via Standard Streams (`sys.stdin` / `sys.stdout`)**:
   - Eliminates complex Java compilation and dependency packaging.
   - Allows the data science pipeline to use native Python mappers and reducers.
   - Highly performant with tab-delimited key-value exchanges.
2. **Dynamic Host Resolution via Environment Variables**:
   - Cluster nodes communicate using logical hostnames (`hadoop-master`, `hadoop-worker-1`, `hadoop-worker-2`).
   - Private IPs are mapped in `/etc/hosts` and `.env`, avoiding cloud-specific IP lock-in.
3. **Decoupled Dashboard Read Model**:
   - The Streamlit web dashboard strictly reads pre-computed Hadoop analytics outputs rather than re-aggregating data in Python memory.
