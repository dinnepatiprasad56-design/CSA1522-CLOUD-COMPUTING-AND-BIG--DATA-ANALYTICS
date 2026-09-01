# Hadoop Streaming-Based Real-Time Weather Data Analytics System on Cloud Infrastructure

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Hadoop 3.3.6](https://img.shields.io/badge/hadoop-3.3.6-orange.svg)](https://hadoop.apache.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Final-Year Capstone Project in Cloud Computing & Big Data Analytics**

A production-grade, distributed meteorological analytics pipeline leveraging **Hadoop Streaming MapReduce**, **HDFS**, and **YARN** deployed across a 3-node cloud VM cluster (1 Master + 2 Workers). The system continuously ingests meteorological time-series records, stores massive datasets in HDFS, executes distributed statistical aggregation and anomaly detection jobs using Python Mappers and Reducers, and serves live interactive insights via a modern Streamlit analytics dashboard.

---

## 1. System Architecture

```
                  +----------------------------------------------+
                  |  Weather API / Real-Time Weather Generator   |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------------------------------+
                  |           Python Ingestion & Validator       |
                  |  - Schema & Range Validation                 |
                  |  - Malformed Record Quarantine               |
                  |  - Buffered Micro-batching                   |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------------------------------+
                  |               HDFS Storage Root              |
                  |   /weather/raw/YYYY/MM/DD/part-*.csv         |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------------------------------+
                  |          Hadoop Streaming Execution          |
                  |   - Python Mappers (City Partitioning)       |
                  |   - YARN Shuffle & Sort Engine               |
                  |   - Python Reducers (Statistical Analytics)  |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------------------------------+
                  |          Processed Analytics Output          |
                  |   /weather/output/analytics_summary.csv      |
                  |   /weather/output/anomalies.csv              |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------------------------------+
                  |        Streamlit Interactive Dashboard       |
                  |   - Geospatial & City Comparisons            |
                  |   - Diurnal Trends & Anomaly Alerts          |
                  |   - Dynamic Refresh Engine                   |
                  +----------------------------------------------+
```

---

## 2. Cloud Cluster Topology

```
                       +-------------------------------+
                       |         HADOOP MASTER         |
                       |  - NameNode (HDFS Metadata)   |
                       |  - ResourceManager (YARN)     |
                       |  - JobHistory Server          |
                       |  - Ingestion / Dashboard Host |
                       +---------------+---------------+
                                       |
                   +-------------------+-------------------+
                   |                                       |
                   v                                       v
    +-----------------------------+         +-----------------------------+
    |       HADOOP WORKER 1       |         |       HADOOP WORKER 2       |
    |  - DataNode (Blocks)        |         |  - DataNode (Blocks)        |
    |  - NodeManager (Containers) |         |  - NodeManager (Containers) |
    +-----------------------------+         +-----------------------------+
```

---

## 3. Monitored Meteorological Parameters & Anomaly Thresholds

| Parameter | Unit | Normal Range | Critical Thresholds |
| :--- | :---: | :---: | :--- |
| **Temperature** | °C | 15.0 – 38.0 | $\ge 42.0$ (Heatwave) / $\le 5.0$ (Coldwave) |
| **Relative Humidity** | % | 30.0 – 80.0 | $\ge 90.0$ (Saturation) / $\le 15.0$ (Aridity) |
| **Precipitation / Rainfall** | mm | 0.0 – 15.0 | $\ge 65.0$ (Torrential / Flood Risk) |
| **Wind Speed** | km/h | 5.0 – 25.0 | $\ge 60.0$ (Gale / Storm Warning) |
| **Atmospheric Pressure** | hPa | 950.0 – 1015.0 | $\le 970.0$ (Cyclonic Depression) |

---

## 4. Repository Structure

```
weather-hadoop-capstone/
│
├── README.md                 # Master Project Documentation
├── requirements.txt          # Python dependencies
├── .gitignore                # Git exclusions (credentials, caches, logs)
├── .env.example              # Environment variables template for cloud deployment
│
├── config/
│   ├── config.yaml           # Master pipeline, HDFS paths, and cluster configuration
│   └── thresholds.yaml       # Anomaly detection & meteorology alert thresholds
│
├── data/
│   ├── sample/               # Baseline sample weather datasets (CSV)
│   └── generated/            # Dynamic simulation batch storage
│
├── ingestion/                # Data acquisition, API fetcher, validator & HDFS uploader
├── mapper/                   # Hadoop Streaming Python Mappers
├── reducer/                  # Hadoop Streaming Python Reducers
├── hadoop/                   # Core Hadoop XML configs (core-site, hdfs-site, yarn-site)
├── scripts/                  # Cluster automation, setup, and maintenance bash scripts
├── jobs/                     # Hadoop Streaming execution scripts for each metric
├── dashboard/                # Streamlit live monitoring web dashboard
├── tests/                    # Unit and integration test suites
└── docs/                     # Technical architecture and performance evaluation guides
```

---

## 5. Development Phases

| Phase | Description | Status |
| :--- | :--- | :---: |
| **Phase 1** | Project Structure, Configuration & Sample Dataset | **Completed** |
| **Phase 2** | Data Ingestion, Simulation & Robust Validation Engine | **Completed** |
| **Phase 3** | Python MapReduce Mappers & Reducers Implementation | **Completed** |
| **Phase 4** | Cloud Cluster Architecture & Configuration Management | **Completed** |
| **Phase 5** | Production Hadoop 3.x XML Deployment Templates | **Completed** |
| **Phase 6** | Automated Cloud VM Setup Scripts (Master & Workers) | **Completed** |
| **Phase 7** | Cloud Cluster Verification & HDFS Diagnostics | **Completed** |
| **Phase 8** | Distributed Hadoop Streaming Analytics Pipeline | **Completed** |
| **Phase 9** | Continuous / Near-Real-Time Ingestion Pipeline | **Completed** |
| **Phase 10** | Streamlit Real-Time Analytics Dashboard | **Completed** |
| **Phase 11** | Anomaly Detection & Cloud Alert Engine | **Completed** |
| **Phase 12** | Multi-Worker & Large Dataset Scalability Benchmark | **Completed** |
| **Phase 13** | Complete Documentation & Capstone Presentation Guide | **Completed** |

---

## 6. Phase 1 Verification & Testing

### 1. Verify Sample Dataset
The sample weather dataset `data/sample/sample_weather_data.csv` contains 1,176 hourly records for 7 major Indian metropolitan regions (*Chennai, Bengaluru, Hyderabad, Mumbai, Delhi, Kolkata, Pune*) with diurnal solar variation and injected meteorologic anomalies.

To regenerate or verify the dataset:
```bash
python scripts/generate_sample_data.py
```

### 2. Inspect Dataset Structure
```bash
head -n 10 data/sample/sample_weather_data.csv
```
Sample record:
```csv
timestamp,city,temperature,humidity,rainfall,wind_speed,pressure
2026-08-11T00:00:00,Chennai,27.2,85.0,0.0,10.0,1010.2
```
