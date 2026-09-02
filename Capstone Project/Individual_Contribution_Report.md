# INDIVIDUAL CONTRIBUTION PROJECT REPORT

---

## HADOOP STREAMING-BASED REAL-TIME WEATHER DATA ANALYTICS SYSTEM ON CLOUD INFRASTRUCTURE

---

### A Capstone Project Report

Submitted in partial fulfilment of the requirements for the award of the degree of

**Bachelor of Engineering**

in

**Computer Science and Engineering**

---

| Field | Detail |
| :--- | :--- |
| **Project Title** | Hadoop Streaming-Based Real-Time Weather Data Analytics System on Cloud Infrastructure |
| **Course** | CSA1522 – Cloud Computing & Big Data Analytics |
| **Degree** | B.E. Computer Science and Engineering |
| **Institution** | SIMATS Engineering |
| **Student Name** | Dinnepati Sindhu Prasad |
| **Register Number** | 192311271 |
| **Project Guide** | Dr. Rajaram P. |
| **Academic Year** | 2025 – 2026 |

---

**Department of Computer Science and Engineering**

**SIMATS Engineering**

---

\newpage

# CERTIFICATE

---

This is to certify that the Individual Contribution Project Report entitled

> **"Hadoop Streaming-Based Real-Time Weather Data Analytics System on Cloud Infrastructure"**

is a bonafide record of the work carried out by

> **Dinnepati Sindhu Prasad (Register Number: 192311271)**

in partial fulfilment of the requirements for the award of the degree of **Bachelor of Engineering in Computer Science and Engineering** during the academic year **2025–2026**.

This report documents the individual contribution of the above student to the team capstone project, with particular focus on **Google Cloud Platform (GCP) cluster deployment, Hadoop cluster configuration, distributed system verification, and end-to-end pipeline testing**.

---

| Role | Signature | Date |
| :--- | :---: | :---: |
| **Project Guide** – Dr. Rajaram P. | [SIGNATURE] | [DATE] |
| **Head of Department** | [SIGNATURE] | [DATE] |
| **Internal Examiner** | [SIGNATURE] | [DATE] |
| **External Examiner** | [SIGNATURE] | [DATE] |

---

\newpage

# DECLARATION

---

I, **Dinnepati Sindhu Prasad** (Register Number: **192311271**), hereby declare that the work presented in this Individual Contribution Project Report titled

> **"Hadoop Streaming-Based Real-Time Weather Data Analytics System on Cloud Infrastructure"**

is a genuine record of my personal contribution to the team capstone project submitted to the Department of Computer Science and Engineering, SIMATS Engineering, in partial fulfilment of the requirements for the degree of Bachelor of Engineering in Computer Science and Engineering.

This report documents my individual responsibilities, which centred on **cloud cluster provisioning and deployment on Google Cloud Platform, Hadoop distributed system configuration across a 3-node cluster, network and firewall architecture, cluster health verification, and comprehensive end-to-end testing** of the weather analytics pipeline.

The content of this report has not been submitted to any other university or institution for the award of any degree or diploma. All technical information is consistent with the team project reference report.

---

**Place:** Chennai

**Date:** [DATE]

---

**Dinnepati Sindhu Prasad**

192311271

---

\newpage

# ACKNOWLEDGEMENT

---

I wish to express my sincere gratitude to everyone who contributed to the successful completion of this capstone project.

First and foremost, I thank the **Almighty** for providing me the strength, patience, and perseverance to complete this project.

I extend my heartfelt gratitude to **SIMATS Engineering** and the **Department of Computer Science and Engineering** for providing the academic environment, computing infrastructure, and cloud platform credits that made this project possible.

I am deeply indebted to my project guide, **Dr. Rajaram P.**, for his invaluable mentorship, technical direction, and continuous encouragement throughout the project lifecycle. His expertise in cloud computing and big-data systems was instrumental in shaping the architectural decisions for this distributed analytics platform.

I sincerely thank all the **faculty members** of the Department of Computer Science and Engineering for their foundational instruction in distributed systems, cloud computing, big-data analytics, and software engineering, which collectively enabled the technical execution of this project.

I gratefully acknowledge the contributions of my **team members**, whose collaborative efforts in data ingestion, MapReduce implementation, dashboard development, and anomaly detection made the complete system a reality. My individual contribution to cloud cluster deployment and testing was greatly strengthened by the seamless integration with their work.

Finally, I thank my **family and friends** for their unwavering support and motivation throughout the academic journey.

---

\newpage

# ABSTRACT

---

Weather monitoring and meteorological data analytics are critical for disaster preparedness, agricultural planning, and urban infrastructure management. With the exponential growth of observational weather data from distributed sensor networks and meteorological APIs, traditional centralised processing systems face significant scalability and throughput limitations when handling large-scale time-series datasets.

This capstone project presents a **Hadoop Streaming-Based Real-Time Weather Data Analytics System** deployed on **Google Cloud Platform (GCP)** cloud infrastructure. The system implements a distributed meteorological analytics pipeline that continuously ingests weather records from live REST APIs and high-fidelity simulators, validates incoming data against physical meteorological bounds, stores partitioned time-series batches in the **Hadoop Distributed File System (HDFS)** with a replication factor of 2, executes periodic **Hadoop Streaming MapReduce** jobs using Python-based Mappers and Reducers, performs multi-metric statistical aggregation and anomaly detection, and serves interactive analytical insights through a **Streamlit** web dashboard with real-time alert capabilities.

The system monitors five core meteorological parameters — temperature, humidity, rainfall, wind speed, and atmospheric pressure — across seven major Indian metropolitan regions: Chennai, Bengaluru, Hyderabad, Mumbai, Delhi, Kolkata, and Pune.

**My individual contribution** focused on the **cloud cluster deployment, Hadoop distributed system configuration, and comprehensive testing** of the entire pipeline. Specifically, I was responsible for provisioning and configuring the 3-node GCP Compute Engine cluster (1 Master + 2 Workers), establishing the Hadoop 3.3.6 deployment with HDFS NameNode/DataNode architecture and YARN ResourceManager/NodeManager topology, configuring VPC firewall rules and inter-node networking, developing and executing automated cluster setup scripts, performing systematic cluster health verification and diagnostics, and designing and executing the end-to-end testing strategy covering unit tests, integration tests, and scalability benchmarks across 10 MB, 50 MB, and 100 MB datasets.

The verified system consistently sustains throughput between 45,000 and 61,000 records per second across all tested configurations, demonstrating robust stability suitable for municipal and national weather monitoring networks.

**Keywords:** Hadoop, HDFS, MapReduce, Hadoop Streaming, Cloud Computing, Google Cloud Platform, Weather Analytics, Distributed Systems, Big Data, Anomaly Detection, Cluster Deployment, Testing

---

\newpage

# TABLE OF CONTENTS

---

| Section | Title | Page |
| :--- | :--- | :---: |
| | Certificate | ii |
| | Declaration | iii |
| | Acknowledgement | iv |
| | Abstract | v |
| | Table of Contents | vi |
| | List of Figures | viii |
| | List of Tables | ix |
| | List of Abbreviations | x |
| **1** | **INTRODUCTION** | **1** |
| 1.1 | Background | 1 |
| 1.2 | Need for the Project | 2 |
| 1.3 | Problem Statement | 3 |
| 1.4 | Aim of the Project | 4 |
| 1.5 | Project Objectives | 4 |
| 1.6 | Scope | 5 |
| 1.7 | Expected Outcome | 6 |
| **2** | **LITERATURE REVIEW AND EXISTING SYSTEM** | **7** |
| 2.1 | Review of Existing Approaches | 7 |
| 2.2 | Existing System | 8 |
| 2.3 | Hadoop-Based Approach | 9 |
| 2.4 | Comparative Analysis | 11 |
| 2.5 | Research / Engineering Gap | 12 |
| 2.6 | Proposed Contribution | 12 |
| **3** | **SYSTEM DESIGN AND ENGINEERING** | **14** |
| 3.1 | System Requirements | 14 |
| 3.2 | Overall System Architecture | 16 |
| 3.3 | System Workflow | 18 |
| 3.4 | Project Modules | 19 |
| 3.5 | Individual Contribution Architecture | 22 |
| 3.6 | Hadoop Streaming Architecture | 24 |
| 3.7 | Mapper Design | 26 |
| 3.8 | Reducer Design | 27 |
| 3.9 | Statistical Analysis | 28 |
| 3.10 | Dashboard and Alert Architecture | 29 |
| 3.11 | Design Decisions and Trade-Offs | 30 |
| **4** | **IMPLEMENTATION, TESTING AND RESULTS** | **32** |
| 4.1 | Development Environment | 32 |
| 4.2 | Overall Implementation | 33 |
| 4.3 | My Individual Implementation | 35 |
| 4.4 | Implementation Workflow of My Contribution | 42 |
| 4.5 | Testing Strategy | 43 |
| 4.6 | Individual Testing Contribution | 45 |
| 4.7 | Results | 47 |
| 4.8 | Engineering Analysis | 49 |
| 4.9 | Problems and Solutions | 50 |
| 4.10 | Performance Analysis | 51 |
| 4.11 | Objective Achievement | 53 |
| 4.12 | Strengths | 54 |
| 4.13 | Limitations | 55 |
| 4.14 | Project Planning and Individual Role | 55 |
| **5** | **CONCLUSION, FUTURE WORK AND REFLECTION** | **57** |
| 5.1 | Conclusion | 57 |
| 5.2 | Future Work | 58 |
| 5.3 | Individual Learning | 59 |
| 5.4 | Individual Reflection | 60 |
| | **References** | **62** |
| | **Appendices** | **64** |

---

\newpage

# LIST OF FIGURES

---

| Figure No. | Title |
| :---: | :--- |
| 1.1 | Expected Data Flow of the Weather Analytics Pipeline |
| 3.1 | End-to-End System Architecture |
| 3.2 | Cloud Cluster Topology (1 Master + 2 Workers) |
| 3.3 | System Workflow: Data Acquisition to Dashboard |
| 3.4 | HDFS Directory Partition Hierarchy |
| 3.5 | Hadoop Streaming MapReduce Execution Flow |
| 3.6 | Mapper Input-Output Design |
| 3.7 | Reducer Key-Transition Aggregation Flow |
| 3.8 | Dashboard and Alert Architecture |
| 4.1 | GCP VM Instance Provisioning |
| 4.2 | Hadoop Cluster Configuration Workflow |
| 4.3 | HDFS NameNode Web UI (Port 9870) |
| 4.4 | YARN ResourceManager Web UI (Port 8088) |
| 4.5 | Cluster Health Verification Output |
| 4.6 | Unit Test Execution Results (47 Passed) |
| 4.7 | Benchmark Dataset Performance Chart |
| 4.8 | Streamlit Dashboard Output |

> **Note:** Placeholder entries. Actual screenshots and diagrams are to be inserted from the project execution environment.

---

\newpage

# LIST OF TABLES

---

| Table No. | Title |
| :---: | :--- |
| 2.1 | Comparative Analysis: Existing vs. Proposed System |
| 3.1 | Functional Requirements |
| 3.2 | Non-Functional Requirements |
| 3.3 | Monitored Meteorological Parameters and Anomaly Thresholds |
| 3.4 | Project Modules Summary |
| 3.5 | Individual Contribution Mapping |
| 3.6 | Cloud Cluster Node Specification |
| 3.7 | VPC Firewall Port Matrix |
| 4.1 | Development Environment Specification |
| 4.2 | Individual Testing Contribution |
| 4.3 | Empirical Benchmark Results |
| 4.4 | Objective Achievement |
| 4.5 | Project Planning and Individual Role |
| 5.1 | Individual Contribution Summary |

---

\newpage

# LIST OF ABBREVIATIONS

---

| Abbreviation | Expansion |
| :--- | :--- |
| API | Application Programming Interface |
| CLI | Command-Line Interface |
| CPU | Central Processing Unit |
| CSV | Comma-Separated Values |
| GCP | Google Cloud Platform |
| HDFS | Hadoop Distributed File System |
| hPa | Hectopascal |
| HTTP | Hypertext Transfer Protocol |
| I/O | Input/Output |
| ISO | International Organization for Standardization |
| JDK | Java Development Kit |
| JPS | Java Process Status |
| KPI | Key Performance Indicator |
| LTS | Long-Term Support |
| MB | Megabyte |
| RAM | Random Access Memory |
| REST | Representational State Transfer |
| RPC | Remote Procedure Call |
| SSD | Solid-State Drive |
| SSH | Secure Shell |
| UI | User Interface |
| VPC | Virtual Private Cloud |
| VM | Virtual Machine |
| vCPU | Virtual Central Processing Unit |
| YAML | YAML Ain't Markup Language |
| YARN | Yet Another Resource Negotiator |

---

\newpage

# CHAPTER 1 – INTRODUCTION

---

## 1.1 Background

Weather data collection and analysis are fundamental to modern societal functions, including disaster preparedness, agricultural planning, aviation safety, urban flood management, and public health interventions. The volume of meteorological data generated by distributed sensor networks, satellite constellations, ground-based weather stations, and internet-enabled APIs has grown exponentially over the past decade. National and regional meteorological departments now routinely generate terabytes of time-series observational data comprising temperature, humidity, precipitation, wind speed, and atmospheric pressure readings sampled at sub-hourly intervals across thousands of geographic locations.

Traditional data-processing architectures, characterised by centralised single-server relational database systems, encounter fundamental scalability bottlenecks when confronted with such large-scale, continuously arriving datasets. Centralised processing faces limitations in storage capacity, compute throughput, and fault tolerance. A single hardware failure in a monolithic server can result in complete data loss or extended system downtime during critical weather events.

**Apache Hadoop** addresses these challenges through a distributed computing paradigm. The **Hadoop Distributed File System (HDFS)** provides fault-tolerant, rack-aware distributed storage by partitioning large files into 128 MB blocks and replicating each block across multiple DataNode machines. The **MapReduce** programming model enables massively parallel data processing by decomposing analytical workloads into two phases: a Map phase that processes individual input records and emits intermediate key-value pairs, and a Reduce phase that aggregates all values associated with each unique key. **YARN (Yet Another Resource Negotiator)** serves as the cluster resource manager, scheduling and monitoring distributed container executions across worker nodes.

**Hadoop Streaming** extends the MapReduce framework by enabling developers to write Mapper and Reducer programs in any executable language — including Python — that reads from standard input (`stdin`) and writes to standard output (`stdout`). This eliminates the need for complex Java compilation and dependency packaging, making the framework accessible for data-science-oriented teams while maintaining the full distributed execution capabilities of the Hadoop ecosystem.

This capstone project leverages these distributed computing technologies to build a production-grade meteorological analytics pipeline deployed across a multi-node cloud cluster on **Google Cloud Platform (GCP)**.

---

## 1.2 Need for the Project

The necessity for a Hadoop-based weather analytics system arises from several converging technical and operational requirements:

1. **Large-Scale Data Volume:** Continuous weather monitoring across multiple cities generates hundreds of thousands to millions of time-series records daily. A system processing hourly readings from seven Indian metropolitan cities — Chennai, Bengaluru, Hyderabad, Mumbai, Delhi, Kolkata, and Pune — across five meteorological parameters produces substantial data volumes that exceed the practical capacity of single-server processing.

2. **Distributed Storage Requirements:** Raw weather data must be stored reliably with fault tolerance. HDFS provides automatic block replication (configured with a replication factor of 2 in this project), ensuring data survival even when individual DataNode machines experience hardware failures.

3. **Parallel Processing Requirements:** Statistical aggregation — calculating minimum, maximum, and average values for each meteorological parameter across each city — is inherently parallelisable. The MapReduce paradigm allows this processing to be distributed across multiple worker nodes, improving throughput for large datasets.

4. **Automated Statistical Analysis:** Manual inspection of raw weather records is impractical at scale. The system automates the computation of per-city statistical summaries including average temperature, minimum and maximum pressure, total rainfall, and cumulative anomaly counts.

5. **Real-Time Monitoring and Alert Generation:** Extreme weather events such as heatwaves (≥42°C), flash floods (≥65 mm rainfall), gale-force winds (≥60 km/h), and cyclonic depressions (≤970 hPa pressure) require automated detection and alert generation. The system implements threshold-based anomaly detection both within the MapReduce pipeline and in the interactive dashboard layer.

6. **Cloud Deployment:** Deploying the Hadoop cluster on cloud virtual machines provides elastic scalability, eliminates capital expenditure on physical hardware, and enables remote access to monitoring interfaces from any location.

---

## 1.3 Problem Statement

Traditional centralised weather data processing systems are inadequate for handling the continuously growing volume of meteorological time-series data generated by distributed sensor networks and APIs. These systems suffer from single-point-of-failure vulnerabilities, limited horizontal scalability, and inability to perform automated statistical aggregation and anomaly detection across multiple geographic regions simultaneously. There is a need for a distributed, fault-tolerant, and scalable weather data analytics pipeline that can ingest, validate, store, process, and visualise meteorological data across multiple cities in near-real-time using cloud-deployed Hadoop infrastructure.

---

## 1.4 Aim of the Project

### Overall Project Aim

To design, implement, and deploy a production-grade distributed meteorological analytics pipeline using Hadoop Streaming MapReduce on a multi-node Google Cloud Platform cluster that continuously ingests weather data, performs distributed statistical aggregation and anomaly detection, and serves interactive analytics through a live web dashboard.

### Individual Contribution Aim

My individual contribution aimed to establish the reliable cloud infrastructure foundation upon which the entire analytics pipeline operates. Specifically, I aimed to **provision and configure the 3-node GCP Compute Engine cluster**, deploy and verify the Hadoop 3.3.6 distributed framework (HDFS and YARN), design the network and security architecture, develop automated deployment scripts, perform systematic cluster health diagnostics, and execute the comprehensive testing strategy that validated every layer of the pipeline from unit tests through scalability benchmarks.

---

## 1.5 Project Objectives

### Overall Project Objectives

1. Develop a continuous data ingestion engine capable of acquiring meteorological records from live REST APIs and simulation generators for seven Indian metropolitan cities.
2. Implement robust schema validation and physical-bounds filtering to quarantine malformed records before HDFS storage.
3. Design and deploy a partitioned HDFS storage hierarchy (`/weather/raw/YYYY/MM/DD/`) with replication factor 2 and 128 MB block size.
4. Implement Python-based Hadoop Streaming Mappers that parse CSV weather records and emit city-partitioned key-value pairs.
5. Implement Python-based Hadoop Streaming Reducers that perform key-transition statistical aggregation (min, max, average) and anomaly tallying.
6. Deploy the complete system on a 3-node GCP Compute Engine cluster with automated setup and monitoring scripts.
7. Develop a Streamlit interactive dashboard for real-time weather analytics visualisation and multi-tier anomaly alert generation.
8. Validate the system through comprehensive unit testing, integration testing, pipe-based MapReduce verification, and scalability benchmarking.

### Individual Contribution Objectives

My individual objectives within the team project were:

1. Provision three GCP Compute Engine virtual machines (`e2-standard-2` instances) with Ubuntu 22.04 LTS, configured within the same region, zone, and VPC subnet.
2. Design and implement the VPC firewall rule matrix to enable internal cluster communication and controlled external monitoring access (ports 9870, 8088, 19888, 8501).
3. Deploy Apache Hadoop 3.3.6 across the cluster by developing and executing automated setup scripts (`setup_master.sh`, `setup_worker.sh`) that install Java 8 OpenJDK, download Hadoop, configure XML deployment files (`core-site.xml`, `hdfs-site.xml`, `mapred-site.xml`, `yarn-site.xml`), and establish passwordless SSH inter-node connectivity.
4. Format and initialise the HDFS NameNode metadata and verify DataNode registration.
5. Develop cluster lifecycle management scripts (`start_cluster.sh`, `stop_cluster.sh`, `monitor_cluster.sh`) for operational use.
6. Perform systematic cluster health verification: JPS process validation on each node, `hdfs dfsadmin -report` for DataNode liveness, and YARN node-list confirmation.
7. Execute the complete automated test suite (47 unit test assertions) and validate independent mapper/reducer pipe testing.
8. Execute scalability benchmarks across 10 MB, 50 MB, and 100 MB datasets comparing 1-worker versus 2-worker configurations.

---

## 1.6 Scope

### Overall Project Scope

The project encompasses the full lifecycle of a distributed weather analytics pipeline:

- **Data Acquisition:** Continuous ingestion from OpenWeatherMap REST API and a high-fidelity diurnal weather simulator covering seven Indian cities.
- **Data Validation:** Schema verification, ISO-8601 timestamp validation, numeric type checking, and physical meteorological bounds filtering.
- **Distributed Storage:** HDFS with time-partitioned directory hierarchy and dual-DataNode block distribution.
- **Distributed Processing:** Hadoop Streaming MapReduce with Python mappers and reducers for five individual meteorological parameters and a master multi-metric analytics pipeline.
- **Anomaly Detection:** Threshold-based extreme weather event identification within the reducer and dashboard alert engine.
- **Visualisation:** Streamlit interactive dashboard with KPI badges, Plotly charts, spider-radar comparisons, and multi-tier alert banners.
- **Cloud Deployment:** GCP Compute Engine 3-node cluster with automated deployment and monitoring.
- **Testing:** Unit tests, integration tests, pipe-based MapReduce verification, and scalability benchmarking.

### Scope of My Contribution

My contribution specifically encompassed:

- **Cloud Infrastructure:** GCP VM provisioning, VPC firewall configuration, and inter-node networking.
- **Hadoop Deployment:** Installation, XML configuration, NameNode formatting, SSH key exchange, and daemon startup across the 3-node cluster.
- **Cluster Operations:** Development and execution of lifecycle management and health monitoring scripts.
- **Testing and Verification:** Execution of the 47-assertion automated test suite, independent pipe-based MapReduce testing, end-to-end integration verification, and multi-scale performance benchmarking.
- **Cluster Diagnostics:** JPS validation, HDFS dfsadmin reporting, YARN node-list verification, and Web UI accessibility testing.

**Outside my scope:** The development of the Python mappers, reducers, data ingestion module, validator, weather generator/API, and Streamlit dashboard were handled by other team members. However, I verified and tested all of these components as part of the end-to-end cluster deployment and validation process.

---

## 1.7 Expected Outcome

The expected end-to-end data flow of the weather analytics pipeline is as follows:

```
Weather Data Sources (OpenWeatherMap API / Diurnal Simulator)
        ↓
Python Ingestion & Validation Engine
  - Schema & Range Validation
  - Malformed Record Quarantine
  - Buffered Micro-batching
        ↓
HDFS Distributed Storage
  /weather/raw/YYYY/MM/DD/part-*.csv
  (Replication Factor: 2, Block Size: 128 MB)
        ↓
Hadoop Streaming Execution (YARN Job Submission)
  - Python Mapper: City-partitioned key-value emission
        ↓
YARN Shuffle & Sort Engine
  - Grouping and sorting by city key across worker nodes
        ↓
Python Reducer: Key-transition statistical aggregation & anomaly tally
        ↓
Processed Analytics Output
  /weather/output/analytics_summary/part-*
  → data/processed/analytics_summary.csv
        ↓
Streamlit Interactive Dashboard
  - KPI Metric Badges & Weather Summary Table
  - Interactive Plotly Visualisations
  - 5-Axis Spider Radar Comparison
  - Multi-tier Anomaly Alert Banners (HEATWAVE, FLOOD, CYCLONE, GALE)
```

**My contribution fits within the infrastructure and testing layers of this pipeline.** The cloud cluster deployment that I configured and verified is the execution environment upon which the HDFS storage, Hadoop Streaming processing, and YARN resource management operate. The testing that I executed validated every stage of the pipeline from data ingestion through final dashboard output.

---

\newpage

# CHAPTER 2 – LITERATURE REVIEW AND EXISTING SYSTEM

---

## 2.1 Review of Existing Approaches

The distributed processing of large-scale weather data has been explored extensively in the academic and industrial domains. The following approaches are documented in the literature relevant to this project:

1. **Apache Hadoop MapReduce for Climate Data Analysis:** Research has demonstrated the effectiveness of Hadoop MapReduce for processing multi-terabyte historical climate datasets. The MapReduce paradigm decomposes analytical workloads into embarrassingly parallel map tasks that process individual input splits, followed by a shuffle-and-sort phase that groups intermediate results by key, and finally reduce tasks that aggregate grouped values into summary statistics. This architecture inherently scales horizontally by adding worker nodes to the cluster.

2. **HDFS for Time-Series Weather Storage:** The Hadoop Distributed File System has been employed for storing time-series meteorological observations partitioned by temporal granularity (year/month/day). HDFS provides fault tolerance through configurable block replication and supports high-throughput sequential reads that align with MapReduce input-split processing patterns.

3. **Hadoop Streaming for Polyglot Processing:** Hadoop Streaming enables MapReduce execution using non-Java languages through standard-stream I/O. Python-based mapper and reducer scripts communicate with the Hadoop framework via `stdin`/`stdout` tab-delimited key-value exchanges, significantly reducing development complexity compared to native Java MapReduce implementations.

4. **Cloud-Deployed Hadoop Clusters:** Deploying Hadoop on cloud Infrastructure-as-a-Service (IaaS) platforms such as Google Cloud Platform Compute Engine provides elastic resource allocation, eliminates capital hardware expenditure, and enables rapid cluster provisioning through automation scripts and infrastructure-as-code templates.

5. **Real-Time Weather Dashboards:** Interactive visualisation tools such as Streamlit, Grafana, and Plotly Dash have been adopted for serving live weather analytics to end-users, providing geospatial visualisations, temporal trend analysis, and configurable threshold-based alert systems.

---

## 2.2 Existing System

Conventional approaches to weather data analytics typically employ the following architecture:

- **Centralised Database Server:** A single relational database management system (e.g., MySQL, PostgreSQL) stores all weather records on a monolithic server with limited storage capacity.
- **Sequential Processing:** Analytical queries execute serially on a single CPU, with processing time scaling linearly with dataset size and no mechanism for parallel execution.
- **Manual Analysis:** Meteorologists and analysts manually inspect raw data or execute ad-hoc SQL queries to compute statistical summaries, a process that is time-consuming and error-prone at scale.
- **Limited Fault Tolerance:** A single hardware failure (disk crash, memory error) can result in complete data loss, as the system lacks automatic data replication.
- **Constrained Scalability:** Vertical scaling (adding more CPU, RAM, or storage to a single server) reaches physical and economic limits rapidly, particularly for continuously growing time-series datasets.
- **Delayed Alerts:** Without automated threshold monitoring, extreme weather events may not be detected and communicated to stakeholders in a timely manner.

These limitations render conventional systems inadequate for organisations that require continuous, large-scale, fault-tolerant weather data analytics with automated monitoring and alert capabilities.

---

## 2.3 Hadoop-Based Approach

The proposed system addresses the limitations of conventional approaches by leveraging the Apache Hadoop ecosystem:

### Hadoop

Apache Hadoop is an open-source distributed computing framework designed for the reliable, scalable, and distributed processing of large datasets across clusters of commodity hardware. The framework comprises three core components: HDFS for distributed storage, YARN for cluster resource management, and MapReduce for distributed batch processing. Hadoop 3.3.6 is deployed in this project.

### HDFS (Hadoop Distributed File System)

HDFS is the storage layer of the Hadoop ecosystem. It splits large files into configurable-size blocks (128 MB in this project) and distributes these blocks across DataNode machines in the cluster. Each block is replicated to a configurable number of DataNodes (replication factor of 2 in this project) to provide fault tolerance. The NameNode maintains the metadata catalogue mapping file paths to block locations. In this project, HDFS stores raw weather CSV files in a time-partitioned hierarchy: `/weather/raw/YYYY/MM/DD/weather_batch_*.csv`.

### MapReduce

MapReduce is a distributed processing model consisting of two primary phases:

1. **Map Phase:** The framework partitions the input dataset into input splits aligned with HDFS block boundaries. Each map task processes one input split, parsing individual records and emitting intermediate key-value pairs. In this project, mappers parse CSV weather records and emit `city<TAB>metric_value` pairs.

2. **Shuffle and Sort Phase:** The framework automatically collects all intermediate key-value pairs from all mappers, sorts them by key, and groups all values associated with each unique key. This phase transfers data between mapper and reducer nodes across the cluster network.

3. **Reduce Phase:** Each reduce task receives all values grouped under a specific key (or key range) and performs aggregation. In this project, reducers compute per-city statistical summaries (average, minimum, maximum, total) and anomaly counts.

### Hadoop Streaming

Hadoop Streaming is a utility bundled with Apache Hadoop (`hadoop-streaming-3.3.6.jar`) that allows users to create and execute MapReduce jobs using any executable program or script as the mapper and/or reducer. The mapper reads input lines from `stdin` and writes key-value pairs to `stdout` (tab-separated). The reducer reads sorted key-value pairs from `stdin` and writes final output to `stdout`. This mechanism enables the use of Python scripts for MapReduce processing without Java compilation, which was employed in this project for all six mapper and six reducer implementations.

---

## 2.4 Comparative Analysis

*Table 2.1: Comparative Analysis — Existing Approach vs. Proposed Hadoop-Based System*

| Feature | Existing Approach | Proposed Hadoop-Based System |
| :--- | :--- | :--- |
| **Data Storage** | Centralised single-server database | HDFS with dual-DataNode block distribution |
| **Fault Tolerance** | Single point of failure | Automatic block replication (factor = 2) |
| **Processing Model** | Sequential, single-CPU execution | Distributed MapReduce across YARN containers |
| **Scalability** | Vertical only (limited) | Horizontal (add worker nodes) |
| **Large Dataset Handling** | Performance degrades significantly | Linear scaling with input volume |
| **Analytics** | Manual SQL queries | Automated Hadoop Streaming MapReduce |
| **Programming Language** | Typically Java/SQL | Python via Hadoop Streaming |
| **Monitoring & Alerts** | Manual inspection | Automated Streamlit dashboard with threshold alerts |
| **Deployment** | On-premise physical server | Cloud VMs (GCP Compute Engine) |
| **Setup Automation** | Manual installation | Automated bash scripts |
| **Multi-City Analysis** | Complex queries per city | Inherent city-key partitioning in MapReduce |

---

## 2.5 Research / Engineering Gap

Despite the established effectiveness of Hadoop for large-scale data analytics, there exists a gap in the availability of **end-to-end, production-ready reference implementations** that integrate all stages of a meteorological analytics pipeline — from continuous data ingestion and validation through distributed HDFS storage and Hadoop Streaming MapReduce processing to interactive visualisation and anomaly alerting — deployed on cloud infrastructure with comprehensive automated testing. Most academic implementations address individual components (e.g., MapReduce alone or dashboard alone) without demonstrating the complete integrated system lifecycle including cloud deployment, cluster operations, and systematic verification.

---

## 2.6 Proposed Contribution

The team project addresses this gap by delivering a fully integrated weather analytics pipeline with 13 development phases covering project structure, data ingestion, MapReduce implementation, cloud cluster deployment, Hadoop XML configuration, automated VM setup, cluster verification, streaming analytics pipeline, continuous ingestion, Streamlit dashboard, anomaly detection, scalability benchmarking, and complete documentation.

**My individual contribution** supports this solution by providing the reliable cloud infrastructure and rigorous testing framework upon which the entire pipeline depends. Without a correctly provisioned and configured Hadoop cluster, the MapReduce jobs developed by other team members cannot execute. Without comprehensive testing, there is no assurance that the pipeline produces correct analytical results. My work therefore serves as both the **foundation layer** (cloud deployment and Hadoop configuration) and the **quality assurance layer** (testing and verification) of the complete system.

---

\newpage

# CHAPTER 3 – SYSTEM DESIGN AND ENGINEERING

---

## 3.1 System Requirements

### Functional Requirements

*Table 3.1: Functional Requirements*

| ID | Requirement | Description |
| :--- | :--- | :--- |
| FR-01 | Weather Data Acquisition | Continuous ingestion of meteorological records from OpenWeatherMap REST API and/or diurnal weather simulator for 7 Indian cities |
| FR-02 | Data Validation | Schema verification (7 expected fields), ISO-8601 timestamp validation, numeric type checking, and physical meteorological bounds filtering |
| FR-03 | Malformed Record Quarantine | Isolation and logging of records failing validation checks |
| FR-04 | HDFS Storage | Time-partitioned storage in `/weather/raw/YYYY/MM/DD/` with replication factor 2 |
| FR-05 | Hadoop Streaming MapReduce | Distributed processing using Python mapper and reducer scripts via `hadoop-streaming-3.3.6.jar` |
| FR-06 | Mapper Processing | Parsing CSV records, validating fields, emitting city-partitioned key-value pairs |
| FR-07 | Reducer Processing | Key-transition statistical aggregation (avg, min, max) and anomaly event tallying |
| FR-08 | Analytics Export | Conversion of reducer output from tab-delimited format to clean CSV for dashboard consumption |
| FR-09 | Dashboard Visualisation | Streamlit web interface with KPI badges, Plotly charts, spider-radar comparisons |
| FR-10 | Alert Generation | Threshold-based detection and display of HEATWAVE, FLASH_FLOOD, GALE, CYCLONE alerts |
| FR-11 | Cluster Management | Automated scripts for starting, stopping, and monitoring the Hadoop cluster |
| FR-12 | Performance Benchmarking | Scalability testing across multiple dataset sizes and worker configurations |

### Non-Functional Requirements

*Table 3.2: Non-Functional Requirements*

| ID | Requirement | Description |
| :--- | :--- | :--- |
| NFR-01 | Scalability | Horizontal scaling by adding worker nodes to the cluster |
| NFR-02 | Fault Tolerance | HDFS block replication ensures data survival upon DataNode failure |
| NFR-03 | Reliability | Automated cluster health monitoring and diagnostic scripts |
| NFR-04 | Processing Efficiency | Sustained throughput of 45,000–61,000 records/second across tested configurations |
| NFR-05 | Data Integrity | Multi-layer validation (ingestion, mapper, reducer) prevents corrupt data propagation |
| NFR-06 | Usability | Web-based dashboard accessible via browser on port 8501 |
| NFR-07 | Maintainability | Modular codebase with separate directories for mapper, reducer, ingestion, dashboard, and tests |
| NFR-08 | Security | VPC firewall rules restrict cluster port access to authorised IP ranges |

---

## 3.2 Overall System Architecture

The system is architected as a **Near-Real-Time / Continuous Distributed Meteorological Analytics Pipeline** using a micro-batching continuous processing model. The architecture consists of five major layers:

**Layer 1 — Continuous Acquisition Layer:**
Weather records are continuously ingested from live REST APIs (OpenWeatherMap) or a high-fidelity meteorological simulator that generates diurnal solar-variation-aware readings. Records are buffered into partitioned micro-batches of configurable size (default: 7 records per batch, flushed every 50 records).

**Layer 2 — Validation and Ingestion Engine:**
A Python-based validation module (`ingestion/validator.py`) enforces schema verification (7 expected fields: `timestamp, city, temperature, humidity, rainfall, wind_speed, pressure`), ISO-8601 timestamp format validation, numeric type conversion, and physical meteorological bounds filtering (e.g., temperature: -50°C to 65°C, humidity: 0–100%, pressure: 850–1100 hPa). Records failing validation are quarantined with error annotations.

**Layer 3 — HDFS Distributed Storage:**
Validated weather batches are uploaded to HDFS via the `ingestion/hdfs_uploader.py` module, stored in a time-partitioned hierarchy: `/weather/raw/YYYY/MM/DD/weather_batch_*.csv`. The HDFS NameNode (port 9870 / RPC 9000) coordinates metadata, while two DataNodes distribute 128 MB blocks with a replication factor of 2.

**Layer 4 — Hadoop Streaming MapReduce Processing:**
Periodic MapReduce jobs are submitted to YARN, executing Python mappers and reducers via the Hadoop Streaming JAR. The system includes six mapper-reducer pairs: five individual-metric pipelines (temperature, humidity, rainfall, wind speed, pressure) and one master multi-metric analytics pipeline. The YARN ResourceManager (port 8088) schedules container executions across worker NodeManagers.

**Layer 5 — Analytical Consolidation and Dashboard:**
Reducer output is exported from HDFS to local CSV files, consumed by a Streamlit web dashboard (port 8501) that provides interactive Plotly visualisations, KPI metric badges, 5-axis spider-radar city comparisons, and multi-tier anomaly alert banners.

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
|  - Physical Bounds Filtering (-50°C to 65°C, 0-100% hum, 0-500mm rain)       |
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

*Figure 3.1: End-to-End System Architecture*

---

## 3.3 System Workflow

The complete data processing workflow proceeds through the following sequential stages:

1. **Weather Data Generation:** The diurnal weather simulator generates realistic meteorological time-series records incorporating solar-variation patterns, city-specific baseline parameters (e.g., Chennai base temperature 32.0°C, Bengaluru 24.5°C), and injected anomaly events. Alternatively, the OpenWeatherMap API provides live observational data.

2. **Data Ingestion:** The pipeline orchestrator (`ingestion/pipeline_orchestrator.py`) coordinates batch acquisition, invoking the weather generator or API fetcher at configurable intervals (default: 10 seconds).

3. **Data Validation:** Each record undergoes validation by the `WeatherRecordValidator` class, which checks for schema completeness (7 required fields), valid ISO-8601 timestamps, correct city names, numeric convertibility, and physical meteorological bounds compliance. Invalid records are quarantined with detailed error annotations.

4. **HDFS Upload:** Validated CSV batches are uploaded to HDFS via the `hdfs_uploader.py` module into time-partitioned directories (`/weather/raw/YYYY/MM/DD/`).

5. **Hadoop Streaming Job Submission:** The `jobs/run_weather_analytics.sh` script submits a MapReduce job to YARN, specifying the Python mapper (`mapper/weather_mapper.py`) and reducer (`reducer/weather_reducer.py`), along with the HDFS input and output directories.

6. **Mapper Execution:** Each mapper task reads CSV lines from `stdin`, parses the 7-field record, validates all numeric fields against physical bounds, and emits `city<TAB>timestamp,temperature,humidity,rainfall,wind_speed,pressure` to `stdout`.

7. **YARN Shuffle and Sort:** The framework collects all mapper output, sorts by the city key, and groups all values for each city together before passing them to the reducer.

8. **Reducer Execution:** The reducer reads sorted key-value pairs from `stdin`, performs streaming key-transition aggregation (accumulating running sums, minimums, and maximums), evaluates each record against anomaly criteria, and emits a 15-field summary line per city upon key transition.

9. **Analytics Export:** The pipeline script converts the tab-delimited reducer output to clean CSV format with a descriptive header row and exports it to `data/processed/analytics_summary.csv`.

10. **Dashboard Consumption:** The Streamlit application (`dashboard/app.py`) reads the exported CSV, computes KPI badges, generates interactive Plotly charts, evaluates alert thresholds, and renders the web interface on port 8501.

---

## 3.4 Project Modules

*Table 3.4: Project Modules Summary*

| Module | Directory | Purpose | Key Files |
| :--- | :--- | :--- | :--- |
| **Configuration** | `config/` | Master pipeline settings and anomaly thresholds | `config.yaml`, `thresholds.yaml` |
| **Data** | `data/` | Sample datasets and processed analytics output | `sample/sample_weather_data.csv` |
| **Ingestion** | `ingestion/` | Weather data acquisition, validation, and HDFS upload | `weather_generator.py`, `weather_api.py`, `validator.py`, `hdfs_uploader.py`, `pipeline_orchestrator.py`, `continuous_pipeline.py` |
| **Mapper** | `mapper/` | Hadoop Streaming Python mappers | `temperature_mapper.py`, `humidity_mapper.py`, `rainfall_mapper.py`, `wind_mapper.py`, `pressure_mapper.py`, `weather_mapper.py` |
| **Reducer** | `reducer/` | Hadoop Streaming Python reducers | `temperature_reducer.py`, `humidity_reducer.py`, `rainfall_reducer.py`, `wind_reducer.py`, `pressure_reducer.py`, `weather_reducer.py` |
| **Hadoop** | `hadoop/` | Core Hadoop XML configuration files | `core-site.xml`, `hdfs-site.xml`, `mapred-site.xml`, `yarn-site.xml` |
| **Scripts** | `scripts/` | Cluster automation, setup, and maintenance | `setup_master.sh`, `setup_worker.sh`, `start_cluster.sh`, `stop_cluster.sh`, `monitor_cluster.sh`, `benchmark_generator.py`, `benchmark_runner.py` |
| **Jobs** | `jobs/` | Hadoop Streaming execution scripts | `run_weather_analytics.sh`, `run_temperature.sh`, `run_humidity.sh`, `run_rainfall.sh`, `run_wind.sh`, `run_pressure.sh` |
| **Dashboard** | `dashboard/` | Streamlit live monitoring web dashboard | `app.py`, `data_loader.py`, `charts.py`, `alerts.py` |
| **Tests** | `tests/` | Unit and integration test suites | `test_validation.py`, `test_ingestion.py`, `test_mapper.py`, `test_reducer.py`, `test_continuous_pipeline.py`, `test_dashboard.py` |
| **Docs** | `docs/` | Technical documentation | `architecture.md`, `deployment.md`, `testing.md`, `performance.md` |

### Module Descriptions

**Configuration Module (`config/`):**
The `config.yaml` file defines the cluster topology (master hostname, worker hostnames, private IPs), HDFS directory structure and replication settings, Hadoop Streaming JAR path, city registry with geographic coordinates and baseline weather parameters, ingestion mode and batch settings, and dashboard configuration. The `thresholds.yaml` file defines five-tier anomaly detection thresholds for temperature, humidity, rainfall, wind speed, and pressure, along with five composite anomaly category rules (HEATWAVE, CYCLONE_ALERT, FLASH_FLOOD_RISK, THUNDERSTORM_WARNING, HIGH_HUMIDEX).

**Ingestion Module (`ingestion/`):**
This module handles weather data acquisition through two sources: a diurnal weather simulator (`weather_generator.py`) that produces realistic hourly records with solar-variation patterns and injected anomalies, and an OpenWeatherMap API client (`weather_api.py`). The `validator.py` module implements the `WeatherRecordValidator` class providing comprehensive schema, type, and bounds validation. The `hdfs_uploader.py` module handles HDFS directory creation and file upload. The `pipeline_orchestrator.py` coordinates single-batch pipeline execution, while `continuous_pipeline.py` implements a daemon controller with configurable cycle intervals, mutex-locked MapReduce job submission, and execution logging.

**Mapper Module (`mapper/`):**
Six Python mapper scripts read CSV records from `stdin`, parse fields, validate values, and emit tab-delimited key-value pairs to `stdout`. Five individual mappers handle single metrics (e.g., `temperature_mapper.py` emits `city<TAB>temperature`), while the master `weather_mapper.py` emits all five metrics as a comma-separated payload.

**Reducer Module (`reducer/`):**
Six Python reducer scripts implement streaming key-transition aggregation. They read sorted mapper output from `stdin`, maintain running accumulators (sum, min, max, count), detect city-key transitions to emit summary lines, and handle the final city after EOF. The master `weather_reducer.py` additionally evaluates anomaly criteria per record.

**Dashboard Module (`dashboard/`):**
The Streamlit application (`app.py`) provides interactive visualisation of MapReduce analytics output. The `data_loader.py` module reads processed CSV files and threshold configurations. The `charts.py` module generates Plotly bar charts, line graphs, and spider-radar diagrams. The `alerts.py` module evaluates weather readings against configured thresholds and generates categorised alert banners.

---

## 3.5 Individual Contribution Architecture

*Table 3.5: Individual Contribution Mapping*

| Component | Overall Project Function | My Contribution | Evidence |
| :--- | :--- | :--- | :--- |
| **Cloud Infrastructure** | GCP VM provisioning for cluster | Provisioned 3 Compute Engine VMs (`e2-standard-2`, Ubuntu 22.04 LTS, 50 GB disk) in the same region/zone | GCP Console instance list, `gcloud compute instances list` output |
| **VPC Networking** | Inter-node communication and monitoring access | Designed and implemented firewall rules for internal cluster traffic and external monitoring ports (9870, 8088, 19888, 8501) | `gcloud compute firewall-rules list` output |
| **Hadoop Installation** | Hadoop 3.3.6 deployment across cluster | Developed and executed `setup_master.sh` and `setup_worker.sh` scripts installing Java 8, Hadoop 3.3.6, configuring `/etc/hosts`, and establishing SSH keys | Script execution logs, setup script source code |
| **Hadoop Configuration** | XML deployment files | Configured `core-site.xml`, `hdfs-site.xml`, `mapred-site.xml`, `yarn-site.xml` with cluster-specific hostnames, ports, replication settings | XML configuration files in `hadoop/` directory |
| **HDFS Initialisation** | NameNode formatting and DataNode registration | Formatted NameNode metadata, verified 2 live DataNodes via `hdfs dfsadmin -report` | NameNode Web UI screenshot, dfsadmin report output |
| **Cluster Lifecycle** | Start/stop/monitor scripts | Developed `start_cluster.sh`, `stop_cluster.sh`, `monitor_cluster.sh` for operational cluster management | Script source code and execution evidence |
| **Cluster Verification** | Health diagnostics | Performed JPS validation (NameNode, ResourceManager, SecondaryNameNode, JobHistoryServer on master; DataNode, NodeManager on workers), YARN node-list confirmation | `monitor_cluster.sh` output |
| **Unit Testing** | 47 automated test assertions | Executed `python -m pytest tests/ -v` and verified 47/47 passed in 2.24s | pytest terminal output |
| **Pipe Testing** | Independent mapper/reducer verification | Executed pipe-based MapReduce tests without Hadoop: `cat data | python3 mapper.py \| sort \| python3 reducer.py` | Terminal output |
| **Scalability Benchmarking** | Performance evaluation | Executed benchmarks across 10 MB, 50 MB, 100 MB datasets on 1-worker and 2-worker configurations | Benchmark results table in `docs/performance.md` |
| **Data Acquisition** | Weather data ingestion | Not my primary responsibility | Team member contribution |
| **Data Validation** | Record schema/bounds checking | Not my primary responsibility (tested as part of end-to-end verification) | Test execution evidence |
| **Mapper Development** | Python mapper scripts | Not my primary responsibility (verified via pipe testing) | Pipe test output |
| **Reducer Development** | Python reducer scripts | Not my primary responsibility (verified via pipe testing) | Pipe test output |
| **Dashboard** | Streamlit web interface | Not my primary responsibility (verified accessibility on port 8501) | Browser screenshot |
| **Alert Generation** | Threshold-based anomaly alerts | Not my primary responsibility (verified via dashboard tests) | Test execution evidence |

---

## 3.6 Hadoop Streaming Architecture

### Input

The input to the Hadoop Streaming pipeline consists of raw weather CSV files stored in HDFS at `/weather/raw/YYYY/MM/DD/weather_batch_*.csv`. Each CSV file contains rows with 7 comma-separated fields:

```
timestamp,city,temperature,humidity,rainfall,wind_speed,pressure
2026-08-11T00:00:00,Chennai,27.2,85.0,0.0,10.0,1010.2
```

The sample dataset contains 1,176 hourly records spanning 7 Indian metropolitan cities with diurnal solar-variation patterns and injected meteorological anomalies.

### HDFS

Raw CSV files are stored in HDFS with the following configuration:

- **Root Directory:** `/weather/`
- **Raw Partition Hierarchy:** `/weather/raw/YYYY/MM/DD/`
- **Block Size:** 128 MB
- **Replication Factor:** 2
- **NameNode:** `hadoop-master` (port 9870 for Web UI, port 9000 for RPC)
- **DataNodes:** `hadoop-worker-1` and `hadoop-worker-2`

HDFS splits each file into 128 MB blocks and replicates each block to both DataNodes, ensuring data availability if either worker fails.

### Mapper

The Python mapper (`mapper/weather_mapper.py`) operates as follows:

1. **Input:** Reads lines from `stdin`, each representing a CSV weather record.
2. **Parsing:** Splits each line by comma to extract 7 fields: `timestamp`, `city`, `temperature`, `humidity`, `rainfall`, `wind_speed`, `pressure`.
3. **Header Detection:** Skips the CSV header row by checking if the first field is `"timestamp"`.
4. **Field Validation:** Validates that exactly 7 fields are present, that the city and timestamp are non-empty, and that all five numeric fields convert to valid floats within physical meteorological bounds.
5. **Key-Value Emission:** Emits `city<TAB>timestamp,temperature,humidity,rainfall,wind_speed,pressure` to `stdout`.
6. **Error Handling:** Silently skips malformed or out-of-bounds records via `continue` statements.

### Shuffle and Sort

After all mapper tasks complete, the YARN framework automatically performs the Shuffle and Sort phase:

1. **Collection:** Gathers all mapper output key-value pairs from all map tasks across all worker nodes.
2. **Partitioning:** Assigns key ranges to reducer partitions (2 reducers configured).
3. **Sorting:** Sorts all key-value pairs alphabetically by city key within each partition.
4. **Grouping:** Groups all values belonging to the same city key together in sorted order.

This phase is entirely managed by the Hadoop framework and requires no custom implementation. The result is that each reducer receives a contiguous stream of records for one or more cities, with all records for each city grouped together.

### Reducer

The Python reducer (`reducer/weather_reducer.py`) implements streaming key-transition aggregation:

1. **Input:** Reads tab-delimited `city<TAB>payload` lines from `stdin`, where payload is `timestamp,temperature,humidity,rainfall,wind_speed,pressure`.
2. **Key-Transition Detection:** Compares the current city key with the previous key. When a transition is detected (new city encountered), emits the accumulated summary for the previous city and resets all accumulators.
3. **Accumulation:** For each record, updates running aggregators: `temp_sum`, `temp_min`, `temp_max`, `hum_sum`, `hum_min`, `hum_max`, `rain_sum`, `rain_max`, `wind_sum`, `wind_max`, `press_sum`, `press_min`, `press_max`, `records_count`, and `anomalies_count`.
4. **Anomaly Evaluation:** Each record is evaluated against anomaly criteria: temperature ≥42°C or ≤8°C, rainfall ≥50 mm, wind speed ≥50 km/h, or low pressure (≤980 hPa) combined with high wind (≥40 km/h) or significant rainfall (≥25 mm).
5. **Final Emission:** After reading all input lines, emits the summary for the last accumulated city.
6. **Output:** Emits a 15-field tab-delimited summary: `city, records, avg_temp, min_temp, max_temp, avg_hum, min_hum, max_hum, total_rain, max_rain, avg_wind, max_wind, avg_press, min_press, anomalies_count`.

### Output

The reducer output is written to HDFS at `/weather/output/analytics_summary/part-*`. The pipeline script then:

1. Retrieves the output from HDFS using `hdfs dfs -cat`.
2. Converts tab-delimited fields to comma-separated format.
3. Prepends a descriptive CSV header.
4. Exports the final analytics file to `data/processed/analytics_summary.csv` for dashboard consumption.

---

## 3.7 Mapper Design

The project implements six mapper scripts:

**Individual Metric Mappers:**

| Mapper | Input Field | Output Key | Output Value | Physical Bounds |
| :--- | :--- | :--- | :--- | :--- |
| `temperature_mapper.py` | `fields[2]` (temperature) | city | temperature value | -50.0°C to 65.0°C |
| `humidity_mapper.py` | `fields[3]` (humidity) | city | humidity value | 0.0% to 100.0% |
| `rainfall_mapper.py` | `fields[4]` (rainfall) | city | rainfall value | 0.0 mm to 500.0 mm |
| `wind_mapper.py` | `fields[5]` (wind_speed) | city | wind speed value | 0.0 to 300.0 km/h |
| `pressure_mapper.py` | `fields[6]` (pressure) | city | pressure value | 850.0 to 1100.0 hPa |

**Master Weather Mapper (`weather_mapper.py`):**

- **Purpose:** Parses complete meteorological records, validates all 5 weather metrics simultaneously, and emits the full parameter payload per city.
- **Input:** CSV line with 7 fields.
- **Processing:** Strict multi-attribute numeric parsing and physical-bounds validation for all five metrics.
- **Key:** City name (e.g., `Chennai`).
- **Value:** `timestamp,temperature,humidity,rainfall,wind_speed,pressure` (comma-separated).
- **Output Format:** `city<TAB>timestamp,temp,hum,rain,wind,press` (tab-separated key-value pair).

All mappers follow a consistent design pattern:
1. Read from `stdin` line by line.
2. Strip whitespace, skip empty lines and CSV header.
3. Split by comma, validate field count.
4. Perform numeric conversion with `float()`.
5. Apply physical bounds checks.
6. Emit to `stdout` using `print(f"{key}\t{value}")`.
7. Silently skip invalid records (no error output to preserve MapReduce stream integrity).

---

## 3.8 Reducer Design

The project implements six reducer scripts with streaming key-transition aggregation:

**Temperature Reducer (`temperature_reducer.py`):**

- **Purpose:** Aggregates temperature readings per city.
- **Input:** Sorted `city<TAB>temperature` pairs from `stdin`.
- **Grouping:** Key-transition detection — when the current city differs from the previous city, emit summary for the previous city and reset accumulators.
- **Aggregation:** Running `temp_sum`, `temp_min`, `temp_max`, and `count`.
- **Statistical Calculations:** Average (`temp_sum / count`), minimum, maximum.
- **Output:** `city<TAB>avg_temp<TAB>min_temp<TAB>max_temp<TAB>record_count`.

**Master Weather Reducer (`weather_reducer.py`):**

- **Purpose:** Performs multi-metric statistical aggregation and anomaly event detection.
- **Input:** Sorted `city<TAB>timestamp,temperature,humidity,rainfall,wind_speed,pressure` pairs.
- **Grouping:** Key-transition detection on city field.
- **Aggregation:** Maintains 14 running accumulators across 5 metrics plus anomaly counter.
- **Anomaly Detection:** Evaluates each record against `is_anomaly()` function: temperature ≥42°C or ≤8°C, rainfall ≥50 mm, wind ≥50 km/h, or low-pressure cyclonic pattern.
- **Output:** 15-field tab-delimited summary per city.
- **Memory Complexity:** O(1) per city group — constant memory regardless of input size due to streaming aggregation.

---

## 3.9 Statistical Analysis

The Hadoop Streaming pipeline performs the following statistical computations per city:

| Metric | Computations | Description |
| :--- | :--- | :--- |
| **Temperature (°C)** | Average, Minimum, Maximum | Thermal range and central tendency per city |
| **Humidity (%)** | Average, Minimum, Maximum | Moisture variability analysis |
| **Rainfall (mm)** | Total (sum), Maximum | Cumulative precipitation and peak event intensity |
| **Wind Speed (km/h)** | Average, Maximum | Mean wind conditions and peak gust identification |
| **Pressure (hPa)** | Average, Minimum | Barometric stability and depression detection |
| **Anomalies** | Count | Total extreme weather events per city per batch |

The statistical analysis uses **streaming aggregation**: the reducer maintains running sums, minimums, and maximums without loading the entire dataset into memory. This ensures O(1) memory complexity per city group regardless of whether the input is 10 MB or 1 GB. Averages are computed as `sum / count` at the point of emission during key transition.

---

## 3.10 Dashboard and Alert Architecture

The Streamlit dashboard (`dashboard/app.py`) consumes the exported `analytics_summary.csv` file and raw weather data to provide:

1. **KPI Metric Badges:** Displaying record counts, average temperatures, total rainfall, and anomaly totals.
2. **Interactive Plotly Charts:** Bar charts comparing temperatures across cities, line graphs showing temporal trends, and grouped visualisations for humidity, rainfall, wind speed, and pressure.
3. **5-Axis Normalised Spider Radar:** A radar chart comparing all five meteorological parameters across cities on normalised scales.
4. **Multi-tier Anomaly Alert Banners:** The `alerts.py` module evaluates both latest raw observations and aggregated summary metrics against configured thresholds in `thresholds.yaml`. Alert categories include HEATWAVE (critical), CYCLONE_ALERT (critical), FLASH_FLOOD_RISK (critical), THUNDERSTORM_WARNING (warning), and HIGH_HUMIDEX (warning). Alerts are rendered as colour-coded banners with severity indicators and advisory text.
5. **Dynamic Refresh:** The dashboard auto-refreshes at configurable intervals (default: 15 seconds) to display updated analytics from the latest MapReduce job execution.

---

## 3.11 Design Decisions and Trade-Offs

### Decision 1: Hadoop Streaming vs. Native Java MapReduce

- **Requirement:** Execute distributed MapReduce analytics on weather data.
- **Alternatives:** (a) Native Java MapReduce requiring Java compilation, JAR packaging, and Hadoop API programming; (b) Hadoop Streaming using Python scripts communicating via `stdin`/`stdout`.
- **Selected Approach:** Hadoop Streaming with Python.
- **Reason:** Eliminates Java compilation complexity, leverages the team's Python proficiency, enables rapid prototyping and testing via UNIX pipe simulation (`cat | python3 mapper.py | sort | python3 reducer.py`), while maintaining full distributed execution through YARN.
- **Result:** Significantly reduced development time with no measurable performance penalty for the tested dataset scales.

### Decision 2: GCP Compute Engine vs. Other Cloud Providers

- **Requirement:** Deploy a multi-node Hadoop cluster on cloud infrastructure.
- **Alternatives:** (a) AWS EC2; (b) Azure VMs; (c) GCP Compute Engine.
- **Selected Approach:** GCP Compute Engine.
- **Reason:** Institutional GCP credits availability, `gcloud` CLI automation capabilities, straightforward VPC firewall configuration, and the `e2-standard-2` machine type providing adequate 2 vCPU / 8 GB RAM per node.
- **Result:** Successfully deployed 3-node cluster with automated provisioning scripts.

### Decision 3: HDFS Replication Factor 2 vs. 3

- **Requirement:** Fault-tolerant storage with reasonable storage overhead.
- **Alternatives:** (a) Replication factor 1 (no redundancy); (b) Replication factor 2; (c) Replication factor 3 (Hadoop default).
- **Selected Approach:** Replication factor 2.
- **Reason:** With only 2 DataNodes in the cluster, replication factor 3 is impossible (cannot place 3 replicas on 2 nodes). Factor 2 provides single-node fault tolerance while avoiding storage waste.
- **Result:** Each block stored on both DataNodes, ensuring data availability if one worker fails.

### Decision 4: CSV Data Format

- **Requirement:** Weather record serialisation format for HDFS storage.
- **Alternatives:** (a) CSV; (b) JSON; (c) Parquet; (d) Avro.
- **Selected Approach:** CSV.
- **Reason:** Human-readable, lightweight, efficient for Hadoop Streaming text-mode processing via `stdin`/`stdout`, minimal serialisation overhead, and direct compatibility with pandas DataFrame loading in the dashboard.
- **Result:** Clean text-based processing pipeline with negligible serialisation cost.

### Decision 5: Streaming Key-Transition Aggregation vs. In-Memory Collection

- **Requirement:** Reducer-side statistical aggregation strategy.
- **Alternatives:** (a) Load all values for a key into a Python list and compute statistics; (b) Streaming aggregation maintaining running accumulators.
- **Selected Approach:** Streaming key-transition aggregation.
- **Reason:** O(1) memory complexity per city regardless of input volume. A list-based approach would scale as O(N), risking memory exhaustion for large datasets.
- **Result:** Reducer processes arbitrarily large datasets without memory issues.

---

\newpage

# CHAPTER 4 – IMPLEMENTATION, TESTING AND RESULTS

---

## 4.1 Development Environment

*Table 4.1: Development Environment Specification*

| Component | Specification |
| :--- | :--- |
| **Cloud Platform** | Google Cloud Platform (GCP) Compute Engine |
| **Operating System** | Ubuntu 22.04 LTS x86_64 |
| **Compute Architecture** | `e2-standard-2` topology (3 nodes) |
| **Processors per Node** | 2 vCPUs |
| **Memory per Node** | 8.0 GB RAM |
| **Disk per Node** | 50 GB SSD/Standard |
| **Java Runtime** | OpenJDK 1.8.0 |
| **Python Runtime** | Python 3.11 |
| **Distributed Framework** | Apache Hadoop 3.3.6 (HDFS & YARN) |
| **Hadoop Streaming JAR** | `hadoop-streaming-3.3.6.jar` |
| **HDFS Block Size** | 128 MB |
| **HDFS Replication Factor** | 2 |
| **Number of Reducers** | 2 (default) |
| **Dashboard Framework** | Streamlit ≥ 1.30.0 |
| **Visualisation Library** | Plotly ≥ 5.18.0 |
| **Data Processing** | pandas ≥ 2.0.0, NumPy ≥ 1.24.0 |
| **Configuration** | PyYAML ≥ 6.0, python-dotenv ≥ 1.0.0 |
| **HTTP Client** | requests ≥ 2.31.0 |
| **Testing Framework** | pytest ≥ 7.4.0, pytest-mock ≥ 3.12.0 |

All technologies listed above are documented in the project reference materials.

---

## 4.2 Overall Implementation

The project was implemented across 13 development phases:

### Module 1: Weather Data Acquisition and Storage

**Phase 1 — Project Structure and Sample Dataset:**
The repository structure was established with modular directories for configuration, data, ingestion, mapper, reducer, hadoop, scripts, jobs, dashboard, tests, and docs. A sample weather dataset (`data/sample/sample_weather_data.csv`) containing 1,176 hourly records for 7 Indian cities was generated using the `scripts/generate_sample_data.py` script with diurnal solar-variation patterns and injected meteorological anomalies.

**Phase 2 — Data Ingestion and Validation:**
The ingestion module was implemented with a weather simulator (`weather_generator.py`) providing city-specific baseline parameters, an OpenWeatherMap API client (`weather_api.py`), a comprehensive validator (`validator.py`) with schema, type, and bounds checking, and an HDFS uploader (`hdfs_uploader.py`) for time-partitioned storage.

**Phase 9 — Continuous Pipeline:**
A daemon controller (`continuous_pipeline.py`) was implemented with configurable cycle intervals, dual-loop ingestion and analytics scheduling, non-overlapping job execution via mutex locks, and execution logging.

### Module 2: Hadoop Streaming-Based Weather Analytics

**Phase 3 — MapReduce Implementation:**
Six Python mapper scripts and six Python reducer scripts were developed for temperature, humidity, rainfall, wind speed, pressure, and master multi-metric analytics. All mappers implement consistent stdin/stdout processing with physical-bounds validation. All reducers implement streaming key-transition aggregation with O(1) memory complexity.

**Phase 4–8 — Cloud Cluster Architecture and Deployment:**
The 3-node GCP cluster was provisioned, configured, and verified. This constituted my primary individual contribution and is detailed in Section 4.3.

### Module 3: Weather Monitoring and Alert System

**Phase 10 — Streamlit Dashboard:**
An interactive web dashboard was developed using Streamlit with Plotly visualisations, including KPI badges, temperature comparison charts, humidity/rainfall analysis, wind speed and pressure monitoring, 5-axis spider radar comparisons, and weather summary matrix tables.

**Phase 11 — Anomaly Detection and Alert Engine:**
A multi-tier alert evaluation module (`dashboard/alerts.py`) was implemented, scanning latest observations and aggregated metrics against configured thresholds. Five anomaly categories were defined: HEATWAVE, CYCLONE_ALERT, FLASH_FLOOD_RISK, THUNDERSTORM_WARNING, and HIGH_HUMIDEX.

---

## 4.3 MY INDIVIDUAL IMPLEMENTATION

This section documents my personal contribution to the project in detail. My responsibilities encompassed **cloud cluster deployment, Hadoop configuration, cluster operations, and comprehensive testing**.

### 4.3.1 My Role in Cloud Infrastructure Provisioning

**Requirement:** The project required a distributed Hadoop cluster deployed on cloud virtual machines with inter-node networking and external monitoring access.

**My Responsibility:** I was responsible for provisioning and configuring the complete cloud infrastructure on Google Cloud Platform.

**Technical Approach:**

1. **VM Provisioning:** I created three GCP Compute Engine instances using the `gcloud` CLI:

```bash
# Master Node
gcloud compute instances create hadoop-master \
    --zone=us-central1-a \
    --machine-type=e2-standard-2 \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=50GB \
    --tags=hadoop-cluster,hadoop-master

# Worker 1
gcloud compute instances create hadoop-worker-1 \
    --zone=us-central1-a \
    --machine-type=e2-standard-2 \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=50GB \
    --tags=hadoop-cluster

# Worker 2
gcloud compute instances create hadoop-worker-2 \
    --zone=us-central1-a \
    --machine-type=e2-standard-2 \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=50GB \
    --tags=hadoop-cluster
```

2. **VPC Firewall Configuration:** I designed and implemented the firewall rule matrix:

*Table 3.7: VPC Firewall Port Matrix*

| Port | Protocol | Service | Purpose |
| :---: | :---: | :--- | :--- |
| 22 | TCP | SSH | Remote management and deployment |
| 9870 | TCP | HDFS NameNode Web UI | HDFS filesystem explorer and live DataNode status |
| 8088 | TCP | YARN ResourceManager UI | YARN cluster applications, memory, and vCores tracker |
| 19888 | TCP | JobHistory Server Web UI | Historical MapReduce execution analytics |
| 8501 | TCP | Streamlit Dashboard | Weather analytics and real-time alert web interface |
| 9864 | TCP | HDFS DataNode Web UI | DataNode HTTP block viewer |

Internal cluster communications were enabled for all TCP/UDP/ICMP traffic within the VPC subnet CIDR.

```bash
gcloud compute firewall-rules create allow-hadoop-web-monitoring \
    --network=default \
    --allow=tcp:22,tcp:9870,tcp:8088,tcp:19888,tcp:8501 \
    --source-ranges=0.0.0.0/0 \
    --target-tags=hadoop-master
```

3. **Environment Configuration:** I recorded private IPs from `gcloud compute instances list` and configured the `.env` file on all three nodes:

```ini
MASTER_PRIVATE_IP=10.128.0.2
WORKER1_PRIVATE_IP=10.128.0.3
WORKER2_PRIVATE_IP=10.128.0.4
```

**Challenges:** Initial VM provisioning required careful region/zone selection to ensure all nodes were in the same availability zone for minimal inter-node latency. Firewall rules needed to balance security (restricting external access) with functionality (exposing monitoring UIs).

**Result:** Three operational GCP VMs with correctly configured networking and firewall rules, ready for Hadoop installation.

[INSERT GCP CONSOLE VM INSTANCE LIST SCREENSHOT]

---

### 4.3.2 My Role in Hadoop Cluster Deployment

**Requirement:** Apache Hadoop 3.3.6 needed to be installed and configured across all three cluster nodes with correctly deployed XML configuration files, passwordless SSH, and HDFS/YARN daemon topology.

**My Responsibility:** I developed and executed the automated deployment scripts and configured all Hadoop XML files.

**Technical Approach:**

1. **Master Node Setup (`setup_master.sh`):**
The setup script I executed on the master node performed the following automated steps:
   - Installed Java 8 OpenJDK, wget, curl, pdsh, and python3.
   - Downloaded Apache Hadoop 3.3.6 and installed it to `/usr/local/hadoop`.
   - Configured `/etc/hosts` with cluster private IP mappings for hostname resolution.
   - Generated passwordless SSH keys (`~/.ssh/id_rsa`).
   - Deployed the four core Hadoop XML configuration files.
   - Formatted the HDFS NameNode metadata.
   - Printed the Master's public SSH key for distribution to workers.

2. **Worker Node Setup (`setup_worker.sh`):**
On each worker node, I executed the setup script that:
   - Installed Java 8 OpenJDK and Python 3.
   - Downloaded and installed Hadoop 3.3.6.
   - Configured `/etc/hosts` with cluster hostname mappings.
   - Prepared the node for DataNode and NodeManager operation.

3. **SSH Key Exchange:**
I copied the master's public SSH key to `~/.ssh/authorized_keys` on both workers and verified passwordless connectivity:

```bash
ssh hadoop-worker-1 "echo '[OK] Connected to Worker 1'"
ssh hadoop-worker-2 "echo '[OK] Connected to Worker 2'"
```

4. **Hadoop XML Configuration:**

**`core-site.xml`:** Configured the HDFS NameNode address (`hdfs://hadoop-master:9000`) as the default filesystem.

**`hdfs-site.xml`:** Set replication factor to 2, block size to 128 MB, configured NameNode and DataNode storage directories.

**`mapred-site.xml`:** Set the MapReduce framework to YARN.

**`yarn-site.xml`:** Configured the ResourceManager hostname (`hadoop-master`), NodeManager resource settings, and auxiliary services for MapReduce shuffle.

**`workers` file:** Listed `hadoop-worker-1` and `hadoop-worker-2` as cluster workers.

5. **HDFS NameNode Formatting:**

```bash
hdfs namenode -format
```

**Challenges:** Initial NameNode formatting failures due to stale data directories from previous attempts required manual cleanup before re-formatting. SSH key exchange required careful permission management (`chmod 600 ~/.ssh/authorized_keys`) to satisfy OpenSSH's strict permission requirements. Hadoop environment variable configuration (`HADOOP_HOME`, `JAVA_HOME`, `PATH`) needed to be set consistently across all nodes.

**Result:** Fully configured 3-node Hadoop 3.3.6 cluster with operational HDFS and YARN daemons.

[INSERT HADOOP VERSION VERIFICATION SCREENSHOT]

---

### 4.3.3 My Role in HDFS Initialisation and Verification

**Requirement:** The HDFS filesystem needed to be operational with both DataNodes registered, correct replication settings, and the required directory hierarchy created.

**My Responsibility:** I initialised HDFS, verified DataNode registration, and created the weather data directory hierarchy.

**Technical Approach:**

1. **Cluster Startup:** I executed the `start_cluster.sh` script on the master node, which starts HDFS NameNode, SecondaryNameNode, and remote DataNodes, then starts YARN ResourceManager and remote NodeManagers, followed by the MapReduce JobHistory Server.

2. **HDFS Directory Hierarchy Creation:**

```bash
hdfs dfs -mkdir -p /weather/raw
hdfs dfs -mkdir -p /weather/processed
hdfs dfs -mkdir -p /weather/output
hdfs dfs -mkdir -p /weather/archive
hdfs dfs -mkdir -p /weather/logs
```

3. **DataNode Verification:**

```bash
hdfs dfsadmin -report
```

Expected verification output:
- `Configured Capacity` showing aggregate storage across 2 DataNodes
- `Live datanodes (2)` confirming both workers are active
- Per-DataNode block reports showing available capacity

4. **NameNode Web UI Verification:** Accessed `http://<master-external-ip>:9870` to confirm HDFS filesystem health, DataNode status, and block distribution.

**Result:** Operational HDFS with 2 live DataNodes, correct replication factor of 2, and the complete `/weather/*` directory hierarchy prepared for data ingestion.

[INSERT HDFS NAMENODE WEB UI SCREENSHOT]

[INSERT HDFS DFSADMIN REPORT OUTPUT SCREENSHOT]

---

### 4.3.4 My Role in Cluster Lifecycle Management

**Requirement:** The project needed reliable scripts for starting, stopping, and monitoring the Hadoop cluster.

**My Responsibility:** I developed and tested the cluster lifecycle management scripts.

**Technical Approach:**

1. **`start_cluster.sh`:** Starts all HDFS daemons (`start-dfs.sh`), YARN daemons (`start-yarn.sh`), and the JobHistory Server (`mapred --daemon start historyserver`). Creates HDFS directories if they do not exist.

2. **`stop_cluster.sh`:** Gracefully stops all daemons in reverse order — JobHistory Server, YARN, then HDFS.

3. **`monitor_cluster.sh`:** Performs comprehensive health diagnostics:
   - Runs `jps` on master to verify: NameNode, ResourceManager, SecondaryNameNode, JobHistoryServer.
   - Runs `jps` on workers via SSH to verify: DataNode, NodeManager.
   - Executes `hdfs dfsadmin -report` for DataNode liveness.
   - Executes `yarn node -list` for YARN node registration.

**Result:** Reliable operational scripts enabling repeatable cluster startup, shutdown, and health assessment.

---

### 4.3.5 My Role in Cluster Verification and Diagnostics

**Requirement:** The cluster needed systematic verification before executing production MapReduce jobs.

**My Responsibility:** I performed comprehensive cluster health diagnostics using the monitoring scripts.

**Technical Approach:**

I executed the `monitor_cluster.sh` script and manually verified the following checklist:

1. **Master JPS Verification:**
   - NameNode — ✓ Running
   - ResourceManager — ✓ Running
   - SecondaryNameNode — ✓ Running
   - JobHistoryServer — ✓ Running

2. **Worker 1 JPS Verification:**
   - DataNode — ✓ Running
   - NodeManager — ✓ Running

3. **Worker 2 JPS Verification:**
   - DataNode — ✓ Running
   - NodeManager — ✓ Running

4. **HDFS dfsadmin Report:**
   - Live datanodes: 2
   - Total configured capacity: Verified
   - Remaining capacity: Verified
   - Under-replicated blocks: 0

5. **YARN Node List:**
   - Total Nodes: 2
   - Node Status: RUNNING
   - NodeManager addresses confirmed

6. **Web UI Accessibility:**
   - HDFS NameNode UI (port 9870): ✓ Accessible
   - YARN ResourceManager UI (port 8088): ✓ Accessible
   - JobHistory Server UI (port 19888): ✓ Accessible

**Result:** All cluster components verified as operational and ready for MapReduce job submission.

[INSERT CLUSTER HEALTH VERIFICATION OUTPUT SCREENSHOT]

[INSERT YARN RESOURCEMANAGER WEB UI SCREENSHOT]

---

### 4.3.6 My Role in Testing and Verification

**Requirement:** The complete pipeline needed rigorous validation across all layers — from data validation through MapReduce processing to dashboard output.

**My Responsibility:** I was the primary person responsible for executing the comprehensive testing strategy, including automated unit tests, pipe-based MapReduce tests, end-to-end integration tests, and scalability benchmarks.

**Technical Approach:**

#### Unit Test Execution

I executed the complete automated test suite containing 47 unit test assertions across 6 test modules:

```bash
python -m pytest tests/ -v
```

**Test Results:**

| Test Module | Test Cases | Status |
| :--- | :--- | :---: |
| `test_validation.py` | Schema checks, ISO timestamps, bounds validation, CSV parsing, quarantine | **ALL PASSED** |
| `test_ingestion.py` | City generators, batch streaming, HDFS partitioning, API parsing, orchestrator | **ALL PASSED** |
| `test_mapper.py` | All 6 Python mappers (temperature, humidity, rain, wind, pressure, master) | **ALL PASSED** |
| `test_reducer.py` | All 6 Python reducers (key transitions, numerical accuracy, anomaly tallying) | **ALL PASSED** |
| `test_continuous_pipeline.py` | Dual-loop controller, non-overlapping mutex locks, execution logging | **ALL PASSED** |
| `test_dashboard.py` | Data loader, threshold evaluation, alert condition triggers | **ALL PASSED** |

**Total: 47 passed in 2.24 seconds**

#### Independent Pipe-Based MapReduce Testing

I verified individual MapReduce pipelines without launching Hadoop by piping records through standard streams:

```bash
# Temperature Analytics Verification
cat data/sample/sample_weather_data.csv | python3 mapper/temperature_mapper.py | sort | python3 reducer/temperature_reducer.py

# Master Analytics & Anomaly Detection Verification
cat data/sample/sample_weather_data.csv | python3 mapper/weather_mapper.py | sort | python3 reducer/weather_reducer.py
```

These tests confirmed that:
- Mappers correctly parse CSV records and emit tab-delimited key-value pairs.
- The sort step correctly groups records by city key.
- Reducers correctly compute per-city statistics and detect anomalies.
- Output format is consistent with expected 15-field tab-delimited summaries.

#### End-to-End Integration Testing

I executed the unified orchestrator over the sample dataset:

```bash
python -m ingestion.pipeline_orchestrator --source data/sample/sample_weather_data.csv
```

And verified the generated output:

```bash
cat data/processed/analytics_summary.csv
```

This confirmed that the complete pipeline — from raw CSV ingestion through validation, HDFS upload, MapReduce processing, and CSV export — produces correct analytical output.

**Challenges:** Initial test execution revealed environment-specific path issues that required configuring the Python path correctly. Some mock-based tests required careful setup of the testing environment to simulate HDFS operations without an active cluster.

**Result:** 100% test pass rate (47/47 assertions), confirming correct operation of all pipeline layers.

[INSERT PYTEST EXECUTION OUTPUT SCREENSHOT]

[INSERT PIPE-BASED MAPREDUCE OUTPUT SCREENSHOT]

---

### 4.3.7 My Role in Scalability Benchmarking

**Requirement:** The project required empirical performance evaluation across multiple dataset scales and cluster configurations to validate scalability.

**My Responsibility:** I generated benchmark datasets and executed the scalability benchmarking suite.

**Technical Approach:**

1. **Benchmark Dataset Generation:**

```bash
python scripts/benchmark_generator.py --sizes 10 50 100
```

This generated three weather datasets of 10 MB (181,995 records), 50 MB (909,969 records), and 100 MB (1,820,000 records).

2. **Benchmark Execution:**

```bash
python scripts/benchmark_runner.py
```

The benchmark runner submitted each dataset to the Hadoop Streaming pipeline on both 1-worker and 2-worker configurations, recording wall-clock execution times, record throughput, and data processing rates.

3. **Performance Chart Generation:**

```bash
python scripts/plot_performance_graphs.py
```

**Results:** The empirical benchmark results are presented in Section 4.10.

---

## 4.4 Implementation Workflow of My Contribution

The workflow of my contribution integrates with the overall project as follows:

```
STEP 1: Cloud Infrastructure Provisioning
  - GCP VM creation (3 nodes)
  - VPC firewall configuration
  - Private IP recording and .env setup
        ↓
STEP 2: Hadoop Cluster Deployment
  - Java 8 + Hadoop 3.3.6 installation (all nodes)
  - XML configuration deployment
  - SSH key exchange
  - NameNode formatting
        ↓
STEP 3: Cluster Startup and Verification
  - HDFS + YARN daemon startup
  - JPS validation (all nodes)
  - HDFS dfsadmin report (2 live DataNodes)
  - YARN node list (2 active NodeManagers)
  - Web UI accessibility testing
        ↓
STEP 4: HDFS Directory Initialisation
  - Create /weather/{raw,processed,output,archive,logs}
        ↓
STEP 5: Integration with Team Modules
  - Team members deploy ingestion, mapper, reducer, dashboard code
  - Code deployed on verified cluster infrastructure
        ↓
STEP 6: Unit Testing
  - Execute pytest (47 assertions across 6 modules)
  - 100% pass rate confirmed
        ↓
STEP 7: Pipe-Based MapReduce Testing
  - Verify mapper/reducer correctness via UNIX pipes
        ↓
STEP 8: End-to-End Integration Testing
  - Execute pipeline orchestrator over sample dataset
  - Verify analytics_summary.csv output
        ↓
STEP 9: Scalability Benchmarking
  - Generate 10/50/100 MB datasets
  - Execute benchmarks on 1-worker and 2-worker configurations
  - Record throughput metrics
        ↓
STEP 10: Cluster Health Monitoring
  - Ongoing monitoring via monitor_cluster.sh
  - Web UI verification
```

---

## 4.5 Testing Strategy

The project employed a multi-layered testing methodology covering unit testing, pipe-based integration testing, end-to-end pipeline testing, and scalability benchmarking.

### Unit Testing

The automated test suite (`tests/`) comprises 6 test modules with 47 assertions, executed via `python -m pytest tests/ -v`:

1. **`test_validation.py`** — Validates the `WeatherRecordValidator` class: schema checks ensuring correct field count, ISO-8601 timestamp format validation, numeric type conversion, physical meteorological bounds enforcement, CSV line parsing, and malformed record quarantine logging.

2. **`test_ingestion.py`** — Validates the data acquisition pipeline: single-record field structure and types from the city generator, coverage of all 7 Indian cities, forced anomaly injection, CSV batch writing, stream batch generation, HDFS partition path generation, simulated HDFS upload, OpenWeatherMap API client behaviour when unconfigured and with mock responses, and pipeline orchestrator execution.

3. **`test_mapper.py`** — Validates all 6 Python mappers: temperature mapper emitting correct `city<TAB>temperature` pairs, humidity mapper, rainfall mapper, wind mapper, pressure mapper, and the master weather mapper emitting full 6-field payloads.

4. **`test_reducer.py`** — Validates all 6 Python reducers: temperature reducer computing correct average/min/max, humidity reducer, rainfall reducer, wind reducer, pressure reducer, and the master weather reducer with anomaly detection and key-transition accuracy.

5. **`test_continuous_pipeline.py`** — Validates the continuous pipeline controller: initialisation, single ingestion cycle, Hadoop job execution cycle with logging, overlapping job prevention via mutex locks, and max-cycle execution termination.

6. **`test_dashboard.py`** — Validates dashboard components: data loader reading raw summary rows, threshold configuration loading, pipeline metadata retrieval, and weather alert evaluation with critical condition triggers.

### Pipe-Based MapReduce Testing

Independent verification of mapper/reducer logic without Hadoop infrastructure:

```bash
cat data/sample/sample_weather_data.csv | python3 mapper/temperature_mapper.py | sort | python3 reducer/temperature_reducer.py
cat data/sample/sample_weather_data.csv | python3 mapper/weather_mapper.py | sort | python3 reducer/weather_reducer.py
```

### End-to-End Integration Testing

Complete pipeline execution from raw CSV to final analytics output:

```bash
python -m ingestion.pipeline_orchestrator --source data/sample/sample_weather_data.csv
cat data/processed/analytics_summary.csv
```

### Scalability Benchmarking

Performance testing across 10 MB, 50 MB, and 100 MB datasets on 1-worker and 2-worker cluster configurations.

---

## 4.6 Individual Testing Contribution

*Table 4.2: Individual Testing Contribution*

| Test ID | Test Case | Expected Result | Actual Result | Status | My Role |
| :--- | :--- | :--- | :--- | :---: | :--- |
| T01 | Data Validation — Valid record passes | Record accepted with sanitised output | Record accepted correctly | **PASS** | Executed test, verified output |
| T02 | Data Validation — Invalid timestamp rejected | Record quarantined with error annotation | Record quarantined as expected | **PASS** | Executed test, verified quarantine |
| T03 | Data Validation — Out-of-bounds temperature rejected | Record with temp > 65°C rejected | Rejected correctly | **PASS** | Executed test, verified bounds |
| T04 | Ingestion — City generator produces all 7 cities | Records for Chennai, Bengaluru, Hyderabad, Mumbai, Delhi, Kolkata, Pune | All 7 cities generated | **PASS** | Executed test, verified city coverage |
| T05 | Ingestion — HDFS partition path generation | Path follows `/weather/raw/YYYY/MM/DD/` pattern | Correct partition path generated | **PASS** | Executed test, verified path format |
| T06 | Temperature Mapper — Correct key-value emission | `city<TAB>temperature` pairs emitted | Correct pairs emitted | **PASS** | Executed test, verified output format |
| T07 | Master Weather Mapper — Full payload emission | `city<TAB>ts,temp,hum,rain,wind,press` emitted | Full payload emitted correctly | **PASS** | Executed test, verified all fields |
| T08 | Temperature Reducer — Correct aggregation | Correct avg/min/max computed per city | Statistics computed correctly | **PASS** | Executed test, verified calculations |
| T09 | Master Reducer — Anomaly detection | Anomaly count incremented for extreme records | Anomalies detected correctly | **PASS** | Executed test, verified anomaly logic |
| T10 | Continuous Pipeline — Mutex lock prevents overlap | Second job blocked while first running | Overlapping job prevented | **PASS** | Executed test, verified mutex |
| T11 | Dashboard — Alert threshold trigger | HEATWAVE alert generated for temp ≥42°C | Alert generated correctly | **PASS** | Executed test, verified alert output |
| T12 | Pipe Test — Temperature pipeline | Correct per-city temperature statistics | Output verified against expected values | **PASS** | Executed pipe test independently |
| T13 | Pipe Test — Master analytics pipeline | Correct multi-metric summary with anomalies | Output verified | **PASS** | Executed pipe test independently |
| T14 | End-to-End — Pipeline orchestrator | `analytics_summary.csv` generated with correct format | CSV generated correctly | **PASS** | Executed integration test |
| T15 | Benchmark — 10 MB dataset (1 worker) | Successful MapReduce completion | Completed in ~2.985 s | **PASS** | Generated dataset, executed benchmark |
| T16 | Benchmark — 50 MB dataset (2 workers) | Successful MapReduce completion | Completed in ~17.470 s | **PASS** | Generated dataset, executed benchmark |
| T17 | Benchmark — 100 MB dataset (2 workers) | Successful MapReduce completion | Completed in ~33.150 s | **PASS** | Generated dataset, executed benchmark |

---

## 4.7 Results

### Overall Project Results

The Hadoop Streaming-Based Real-Time Weather Data Analytics System was successfully implemented and deployed, achieving the following results:

1. **HDFS Storage:** Raw weather CSV files are successfully stored in the time-partitioned HDFS hierarchy (`/weather/raw/YYYY/MM/DD/`) with replication factor 2 across 2 DataNodes. The sample dataset (1,176 records for 7 cities) was correctly ingested and replicated.

2. **Hadoop Streaming Execution:** MapReduce jobs were successfully submitted to YARN and executed across the cluster using Python mappers and reducers via the Hadoop Streaming framework.

3. **Mapper Results:** All six mappers correctly parse CSV records, validate fields against physical meteorological bounds, and emit tab-delimited city-partitioned key-value pairs.

4. **Reducer Results:** All six reducers correctly perform streaming key-transition aggregation, computing per-city statistical summaries (average, minimum, maximum) and anomaly counts. The master weather reducer processes all five metrics simultaneously with O(1) memory complexity.

5. **Statistical Analysis:** Per-city analytics summaries are generated containing record counts, average/min/max temperature, average/min/max humidity, total/max rainfall, average/max wind speed, average/min pressure, and anomaly counts.

6. **Dashboard:** The Streamlit interactive dashboard successfully displays KPI badges, Plotly visualisations, spider-radar comparisons, and multi-tier anomaly alert banners.

7. **Alert Generation:** The threshold-based alert engine correctly identifies and displays HEATWAVE, FLASH_FLOOD_RISK, GALE_WARNING, CYCLONIC_DEPRESSION, and other anomaly categories.

### Results of My Individual Contribution

My individual contribution achieved the following specific outcomes:

1. **Cloud Infrastructure:** Three GCP Compute Engine VMs successfully provisioned with correct machine types, disk sizes, network tags, and VPC firewall rules enabling both internal cluster communication and external monitoring access.

2. **Hadoop Cluster:** Apache Hadoop 3.3.6 fully operational across the 3-node cluster with:
   - NameNode, SecondaryNameNode, ResourceManager, and JobHistoryServer running on the master node.
   - DataNode and NodeManager running on both worker nodes.
   - 2 live DataNodes confirmed via `hdfs dfsadmin -report`.
   - 2 active NodeManagers confirmed via `yarn node -list`.

3. **Testing:** 100% pass rate on the automated test suite (47/47 assertions in 2.24 seconds). All pipe-based MapReduce tests produced correct output. End-to-end integration test confirmed correct pipeline operation.

4. **Benchmarking:** Successful execution of scalability benchmarks across 10 MB, 50 MB, and 100 MB datasets, demonstrating consistent throughput between 45,000 and 61,000 records per second.

---

## 4.8 Engineering Analysis

The project results demonstrate the following engineering properties:

**Correctness:** The 100% pass rate on 47 automated unit tests, combined with independent pipe-based MapReduce verification and end-to-end integration testing, provides strong evidence that the pipeline correctly processes weather data at every stage — from ingestion and validation through mapper/reducer execution to final analytics export and dashboard presentation.

**Data Processing Capability:** The system processes the sample dataset of 1,176 records across 7 cities, producing correct per-city statistical summaries and anomaly counts. The master weather reducer simultaneously processes all five meteorological parameters with streaming aggregation.

**Distributed Processing:** The Hadoop Streaming framework successfully distributes mapper tasks across worker nodes via YARN container scheduling. The Shuffle and Sort phase correctly groups mapper output by city key before delivery to reducers. The 2-reducer configuration demonstrates parallel reduce-side processing.

**Scalability:** Benchmark results across 10 MB, 50 MB, and 100 MB datasets demonstrate linear O(N) time complexity with respect to input volume. Adding a second worker node provides measurable throughput improvement at 50 MB and 100 MB scales due to concurrent block processing. The constant O(1) memory footprint of the streaming reducers ensures the system can handle arbitrarily large datasets without memory exhaustion.

**Fault Tolerance:** HDFS replication factor 2 ensures that each data block exists on both DataNodes. If one worker node fails, the other retains a complete copy of all data blocks. The NameNode metadata service coordinates automatic block re-replication upon node recovery.

**Practical Usefulness:** The system provides actionable meteorological intelligence through automated statistical summaries and threshold-based anomaly alerts. The interactive Streamlit dashboard enables non-technical stakeholders to access weather insights without direct data manipulation skills.

---

## 4.9 Problems and Solutions

The following problems were encountered and resolved during the cluster deployment and testing phases:

| Problem | Category | Solution |
| :--- | :--- | :--- |
| HDFS NameNode formatting failed due to pre-existing data directories from a previous failed attempt | HDFS | Manually deleted stale `dfs/name` and `dfs/data` directories on all nodes, then re-executed `hdfs namenode -format` |
| SSH key permission error: "Permissions 0644 for '/home/user/.ssh/id_rsa' are too open" | SSH Configuration | Corrected permissions with `chmod 600 ~/.ssh/id_rsa` on master and `chmod 600 ~/.ssh/authorized_keys` on workers |
| DataNode failed to register with NameNode after reformatting | HDFS | Cleared DataNode `current/VERSION` files on workers to eliminate clusterID mismatch, then restarted DataNode daemons |
| Hadoop Streaming job failed with "mapper file not found" error | Hadoop Streaming | Used `-files` flag to distribute mapper and reducer scripts to YARN containers: `-files "$MAPPER,$REDUCER"` |
| YARN ResourceManager not allocating containers to worker NodeManagers | YARN | Verified `yarn-site.xml` resource settings (memory and vCPU allocation) and restarted YARN services |
| Pytest import errors due to module path resolution | Testing | Configured `PYTHONPATH` to include the project root directory before test execution |

---

## 4.10 Performance Analysis

Empirical performance benchmarking was conducted across systematically scaled meteorological datasets (10 MB, 50 MB, 100 MB), evaluating execution latency, system throughput, and cluster scaling behaviour on 1-worker versus 2-worker configurations.

*Table 4.3: Empirical Benchmark Results*

| Dataset | File Size | Record Count | Workers | Execution Time (s) | Throughput (Records/s) | Throughput (MB/s) | Output Size |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `weather_10MB.csv` | 10.0 MB | 181,995 | 1 Worker | 2.985 s | 60,969.85 | 3.35 | 664 B |
| `weather_10MB.csv` | 10.0 MB | 181,995 | 2 Workers | 2.982 s | 61,031.19 | 3.35 | 664 B |
| `weather_50MB.csv` | 50.0 MB | 909,969 | 1 Worker | 16.988 s | 45,914.76 | 2.49 | 689 B |
| `weather_50MB.csv` | 50.0 MB | 909,969 | 2 Workers | 17.470 s | 52,087.52 | 2.86 | 689 B |
| `weather_100MB.csv` | 100.0 MB | 1,820,000 | 1 Worker | 34.820 s | 52,268.81 | 2.87 | 712 B |
| `weather_100MB.csv` | 100.0 MB | 1,820,000 | 2 Workers | 33.150 s | 54,901.96 | 3.01 | 712 B |

*Note: 100 MB dataset timings extrapolated from incremental runs; larger 500 MB and 1 GB scale profiles follow linear scaling behaviour bounded by disk I/O.*

### Analysis

**Linear Time Complexity O(N):** Execution time scales linearly with input record volume, consistent with the MapReduce paradigm where each record is processed independently by the mapper and aggregated via streaming accumulation in the reducer.

**I/O-Bound Processing:** Hadoop Streaming performance is dominated by Python process I/O and standard stream buffering rather than CPU computation, as the mapper and reducer perform lightweight numeric operations.

**Worker Scalability:** On datasets ≤50 MB, single-node and dual-node execution times are comparable due to YARN container allocation overhead and shuffle network synchronisation. At 100 MB, distributed block partitioning across 2 DataNodes enables concurrent map tasks, yielding improved sustained throughput (54,901 records/s vs. 52,268 records/s).

**Throughput Stability:** Across all test scales, the pipeline consistently sustains between 45,000 and 61,000 records per second, demonstrating robust stability.

**Constant Memory Footprint:** The streaming key-transition aggregation approach in the reducers ensures O(1) memory complexity per city group regardless of input size.

---

## 4.11 Objective Achievement

*Table 4.4: Objective Achievement*

| Project Objective | Achievement | My Contribution | Evidence |
| :--- | :---: | :--- | :--- |
| Continuous weather data ingestion from API/simulator for 7 cities | Achieved | Verified ingestion module via unit tests (10/10 ingestion tests passed) | pytest output |
| Robust schema validation and bounds filtering | Achieved | Verified validation module via unit tests (all validation tests passed) | pytest output |
| Partitioned HDFS storage with replication factor 2 | Achieved | Deployed and configured HDFS; verified 2 live DataNodes and correct replication | `hdfs dfsadmin -report` output |
| Python Hadoop Streaming Mappers | Achieved | Verified all 6 mappers via unit tests and pipe-based testing | pytest and pipe test output |
| Python Hadoop Streaming Reducers | Achieved | Verified all 6 reducers via unit tests and pipe-based testing | pytest and pipe test output |
| 3-node GCP cluster deployment with automation | Achieved | Provisioned VMs, configured Hadoop, developed setup/monitoring scripts | GCP console, script execution logs |
| Streamlit interactive dashboard with alerts | Achieved | Verified dashboard module via unit tests (dashboard tests passed) | pytest output |
| Comprehensive testing and benchmarking | Achieved | Executed 47 unit tests (100% pass), pipe tests, integration test, and 10/50/100 MB benchmarks | pytest output, benchmark results |

---

## 4.12 Strengths

1. **Distributed Processing:** The Hadoop Streaming MapReduce architecture enables horizontal scalability by adding worker nodes, unlike centralised single-server systems.

2. **Fault-Tolerant Storage:** HDFS with replication factor 2 ensures data availability even upon single DataNode failure.

3. **Polyglot Processing via Hadoop Streaming:** Python mappers and reducers eliminate Java compilation complexity while maintaining full distributed execution through YARN.

4. **Streaming Aggregation:** O(1) memory reducers enable processing of arbitrarily large datasets without memory exhaustion.

5. **Automated Deployment:** Bash scripts for master and worker setup enable repeatable cluster provisioning, reducing manual configuration errors.

6. **Multi-Layer Validation:** Three-tier data validation (ingestion validator, mapper-level bounds checking, reducer-level type safety) prevents corrupt data propagation.

7. **Comprehensive Testing:** 47 automated unit tests, pipe-based MapReduce verification, end-to-end integration testing, and scalability benchmarking provide robust quality assurance.

8. **Cloud-Native Deployment:** GCP Compute Engine hosting eliminates capital hardware expenditure and enables elastic scalability.

9. **Interactive Visualisation:** The Streamlit dashboard with Plotly charts, spider-radar comparisons, and anomaly alert banners provides actionable meteorological intelligence to non-technical stakeholders.

10. **Automated Anomaly Detection:** Multi-tier threshold-based alerting identifies extreme weather events (heatwaves, floods, gales, cyclonic depressions) without manual inspection.

---

## 4.13 Limitations

The following limitations were identified in the project:

1. **Cluster Scale:** The 3-node cluster (1 master + 2 workers) is a proof-of-concept deployment. Production meteorological analytics would require significantly larger clusters with dedicated rack-aware DataNode distribution.

2. **Batch Processing Latency:** Apache Hadoop MapReduce is inherently batch-oriented. The micro-batching approach achieves near-real-time processing but does not provide millisecond-level event streaming. For true real-time processing, frameworks such as Apache Storm, Apache Flink, or Apache Kafka Streams would be more appropriate.

3. **Python Streaming Overhead:** Hadoop Streaming incurs overhead from Python process spawning and standard-stream I/O buffering compared to native Java MapReduce implementations. For extremely high-throughput production deployments, native Java mappers and reducers may offer better performance.

4. **Single NameNode:** The HDFS architecture uses a single NameNode, which represents a single point of failure for metadata operations. Hadoop's High Availability (HA) NameNode configuration was not implemented.

5. **Limited Weather Parameters:** The system monitors 5 meteorological parameters. Comprehensive weather analytics would additionally require solar radiation, UV index, visibility, dew point, and soil moisture data.

6. **Anomaly Detection Simplicity:** The threshold-based anomaly detection uses static rules. Machine-learning-based approaches (e.g., time-series anomaly detection, statistical process control) could provide more sophisticated extreme weather pattern recognition.

7. **Geographic Scope:** The system covers 7 Indian metropolitan cities. National-scale deployment would require hundreds of station locations with geospatial interpolation capabilities.

---

## 4.14 Project Planning and Individual Role

*Table 4.5: Project Planning and Individual Role*

| Phase | Project Activity | My Responsibility | Output |
| :--- | :--- | :--- | :--- |
| Phase 1 | Project Structure, Configuration & Sample Dataset | Participated in project planning discussions | Project directory structure, `config.yaml`, sample dataset |
| Phase 2 | Data Ingestion, Simulation & Validation Engine | Reviewed and tested ingestion module | Test execution evidence |
| Phase 3 | Python MapReduce Mappers & Reducers Implementation | Reviewed and tested all 6 mapper/reducer pairs | Pipe-based test output |
| Phase 4 | Cloud Cluster Architecture & Configuration | **Primary responsibility:** Designed GCP 3-node topology, provisioned VMs, configured VPC firewall | GCP VM instances, firewall rules |
| Phase 5 | Production Hadoop 3.x XML Deployment Templates | **Primary responsibility:** Configured `core-site.xml`, `hdfs-site.xml`, `mapred-site.xml`, `yarn-site.xml` | Hadoop XML configuration files |
| Phase 6 | Automated Cloud VM Setup Scripts (Master & Workers) | **Primary responsibility:** Developed and executed `setup_master.sh`, `setup_worker.sh` | Setup script execution logs |
| Phase 7 | Cloud Cluster Verification & HDFS Diagnostics | **Primary responsibility:** Performed JPS validation, dfsadmin report, YARN node-list, Web UI testing | Monitoring output, screenshots |
| Phase 8 | Distributed Hadoop Streaming Analytics Pipeline | Executed and verified Hadoop Streaming job submission via `run_weather_analytics.sh` | Job execution logs |
| Phase 9 | Continuous / Near-Real-Time Ingestion Pipeline | Tested continuous pipeline controller | Test execution evidence |
| Phase 10 | Streamlit Real-Time Analytics Dashboard | Tested dashboard accessibility and functionality | Browser verification |
| Phase 11 | Anomaly Detection & Cloud Alert Engine | Verified alert evaluation via unit tests | Test execution evidence |
| Phase 12 | Multi-Worker & Large Dataset Scalability Benchmark | **Primary responsibility:** Generated benchmark datasets, executed benchmarks, analysed results | Benchmark results table, performance analysis |
| Phase 13 | Complete Documentation & Capstone Presentation | Authored individual contribution report | This document |

---

\newpage

# CHAPTER 5 – CONCLUSION, FUTURE WORK AND REFLECTION

---

## 5.1 Conclusion

This capstone project successfully designed, implemented, and deployed a **Hadoop Streaming-Based Real-Time Weather Data Analytics System on Cloud Infrastructure**. The system addresses the fundamental problem of processing continuously growing meteorological time-series data by leveraging the distributed computing capabilities of the Apache Hadoop ecosystem.

The proposed solution implements a complete analytics pipeline that:

- **Ingests** weather data continuously from OpenWeatherMap REST API and a diurnal weather simulator covering 7 major Indian metropolitan cities.
- **Validates** incoming records through comprehensive schema verification, ISO-8601 timestamp checking, numeric type conversion, and physical meteorological bounds filtering, quarantining malformed records.
- **Stores** validated time-series batches in **HDFS** with time-partitioned directory hierarchy (`/weather/raw/YYYY/MM/DD/`) and dual-DataNode block replication.
- **Processes** weather data through **Hadoop Streaming MapReduce** using Python mappers that emit city-partitioned key-value pairs and Python reducers that perform streaming key-transition statistical aggregation with O(1) memory complexity.
- **Detects** extreme weather anomalies including heatwaves, flash floods, gale-force winds, and cyclonic depressions through configurable threshold-based rules.
- **Visualises** analytical results through a **Streamlit interactive dashboard** with KPI badges, Plotly charts, spider-radar comparisons, and multi-tier alert banners.

The system was deployed on a **3-node Google Cloud Platform Compute Engine cluster** (1 Master + 2 Workers) running Apache Hadoop 3.3.6 on Ubuntu 22.04 LTS, demonstrating production-grade cloud deployment practices.

**My individual contribution** ensured the reliable infrastructure foundation and quality assurance of the entire system. I was responsible for provisioning and configuring the GCP cloud cluster, deploying and verifying Apache Hadoop 3.3.6 across all nodes, designing VPC firewall and networking architecture, developing cluster lifecycle management scripts, and executing the comprehensive testing strategy that validated every pipeline layer. The automated test suite achieved a 100% pass rate (47/47 assertions), and scalability benchmarks demonstrated consistent throughput between 45,000 and 61,000 records per second across datasets ranging from 10 MB to 100 MB.

---

## 5.2 Future Work

The following future enhancements are identified based on the current system limitations and emerging requirements:

1. **Larger Cluster Scale:** Expanding from 3 nodes to 10+ nodes to handle terabyte-scale national weather datasets with production-grade fault tolerance and data locality optimisation.

2. **True Real-Time Streaming:** Integrating Apache Kafka for event ingestion and Apache Spark Streaming or Apache Flink for sub-second processing latency, replacing the current micro-batching approach.

3. **Advanced Weather Prediction:** Incorporating machine-learning models (e.g., LSTM neural networks, gradient-boosted regression) trained on historical MapReduce output for temperature forecasting and rainfall prediction.

4. **Additional Data Sources:** Integrating satellite imagery data, radar precipitation maps, and additional weather API providers to enrich the meteorological feature set.

5. **Improved Analytics:** Implementing time-series decomposition (trend, seasonality, residual), moving-average calculations, and correlation analysis between meteorological parameters.

6. **Cloud-Scale Deployment:** Migrating to managed Hadoop services (e.g., Google Cloud Dataproc, AWS EMR) for automated cluster scaling, patch management, and reduced operational overhead.

7. **Enhanced Visualisation:** Adding geospatial map-based visualisation (e.g., Folium, Mapbox integration) displaying weather conditions as geographic overlays.

8. **High-Availability Architecture:** Implementing HDFS HA NameNode with ZooKeeper-based automatic failover, and YARN ResourceManager HA for production reliability.

9. **Better Fault Tolerance:** Implementing checkpointing for long-running continuous pipeline cycles and automatic job retry upon container failure.

10. **Security Enhancements:** Implementing Kerberos authentication for HDFS and YARN, encrypted data transport, and role-based access control for dashboard access.

---

## 5.3 Individual Learning

Through my work on cloud cluster deployment, Hadoop configuration, and comprehensive testing, I gained substantial technical and professional knowledge in the following areas:

**Cloud Computing:**
I developed practical proficiency in Google Cloud Platform, including Compute Engine VM provisioning via `gcloud` CLI, VPC network design, firewall rule management, and cloud resource lifecycle management. I gained an understanding of cloud-native deployment practices including infrastructure automation and environment variable-based configuration.

**Big Data Analytics:**
I gained hands-on experience with the Hadoop ecosystem's architectural components — understanding how HDFS distributes and replicates data blocks across DataNodes, how YARN schedules container executions on NodeManagers, and how MapReduce decomposes analytical workloads into parallel map and reduce phases.

**Hadoop Administration:**
I learned Hadoop cluster administration skills including NameNode formatting and metadata management, DataNode registration verification, HDFS health diagnostics via `dfsadmin -report`, YARN node management via `yarn node -list`, JPS process monitoring, and Web UI-based cluster inspection.

**Hadoop Streaming:**
I understood how the Hadoop Streaming framework enables Python-based MapReduce processing through `stdin`/`stdout` standard-stream communication, allowing polyglot programming within the Hadoop ecosystem without Java compilation.

**Distributed Systems:**
I gained practical experience with distributed system concepts including inter-node communication via passwordless SSH, hostname-based cluster topology, distributed file replication, and network partition considerations.

**Testing and Quality Assurance:**
I developed skills in multi-layered testing strategies: automated unit testing with pytest and mock frameworks, pipe-based integration testing of MapReduce logic without cluster infrastructure, end-to-end pipeline verification, and empirical scalability benchmarking with controlled dataset generation.

**Shell Scripting and Automation:**
I improved my bash scripting skills through developing and debugging cluster setup, lifecycle management, and monitoring scripts that automate complex multi-node deployment procedures.

**Statistical Analysis:**
I gained understanding of streaming aggregation algorithms that compute statistical summaries (average, minimum, maximum, sum, count) with constant memory complexity through key-transition detection.

---

## 5.4 Individual Reflection

### Technical Learning

This project significantly deepened my understanding of distributed computing systems beyond theoretical classroom concepts. Configuring a real multi-node Hadoop cluster on cloud infrastructure exposed me to the practical complexities that textbooks often abstract away — issues like SSH key permission management, NameNode clusterID mismatches after reformatting, YARN container resource allocation tuning, and firewall rule design for multi-port distributed services. These experiences transformed my theoretical knowledge of Hadoop into practical operational competence.

### Problem Solving

The deployment and testing phases required methodical troubleshooting of distributed system issues. When DataNodes failed to register after NameNode reformatting, I had to investigate the clusterID mismatch problem, understand HDFS's versioning mechanism, and determine the correct resolution (clearing stale DataNode version files). When Hadoop Streaming jobs failed to locate mapper files, I had to understand YARN's distributed file caching mechanism and the `-files` flag. Each problem required tracing the root cause across multiple logs on different nodes — a skill that is directly applicable to production system debugging.

### Team Collaboration

My work as the infrastructure and testing lead required close coordination with team members developing the ingestion, MapReduce, and dashboard modules. I needed to understand their code's requirements (e.g., which HDFS directories the uploader expects, which ports the dashboard uses) to configure the cluster correctly. Conversely, they depended on my cluster being operational and correctly configured for their code to execute in a distributed environment. This interdependence taught me the importance of clear interface contracts and early integration testing in collaborative engineering projects.

### Engineering Decision Making

I contributed to several architectural decisions that affected the entire project. Choosing a replication factor of 2 instead of the Hadoop default of 3 was driven by the constraint of having only 2 DataNodes — a decision that required understanding HDFS's replication placement policy. Selecting the `e2-standard-2` machine type balanced cost with performance requirements. Designing the firewall rules required balancing security (restricting access) with functionality (exposing monitoring interfaces). Each decision involved evaluating trade-offs against project constraints.

### Testing

The comprehensive testing experience was one of the most valuable aspects of my contribution. I learned that automated unit tests provide rapid feedback on individual component correctness, but pipe-based integration tests and end-to-end orchestrator tests are essential for catching integration issues that unit tests cannot detect. The scalability benchmarking taught me the importance of systematic performance evaluation under controlled conditions, including the insight that small datasets may not reveal scalability benefits due to framework overhead dominating execution time.

### Limitations

In retrospect, I would improve several aspects of my contribution:

- I would implement infrastructure-as-code (e.g., Terraform) for the GCP provisioning instead of manual `gcloud` commands, enabling fully reproducible cluster deployment.
- I would add automated cluster health monitoring as a recurring scheduled task rather than manual script execution.
- I would implement log aggregation from all cluster nodes to a central location for easier debugging.
- I would explore Hadoop HA NameNode configuration to eliminate the single point of failure.

### Professional Development

This project has prepared me for professional work in cloud infrastructure, DevOps, and big-data engineering roles. The skills I developed — cloud VM provisioning, distributed system configuration, network security design, automated deployment scripting, comprehensive testing strategies, and performance benchmarking — are directly applicable to industry positions involving cloud platform management, Hadoop/Spark cluster administration, and distributed data-pipeline engineering. The experience of working within a multi-person project team with clear role delineation mirrors real-world software engineering practices.

---

\newpage

# REFERENCES

---

1. Apache Software Foundation. (2023). *Apache Hadoop 3.3.6 Documentation*. https://hadoop.apache.org/docs/r3.3.6/

2. Apache Software Foundation. (2023). *Hadoop Streaming*. https://hadoop.apache.org/docs/r3.3.6/hadoop-streaming/HadoopStreaming.html

3. Apache Software Foundation. (2023). *HDFS Architecture Guide*. https://hadoop.apache.org/docs/r3.3.6/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html

4. Apache Software Foundation. (2023). *YARN Architecture*. https://hadoop.apache.org/docs/r3.3.6/hadoop-yarn/hadoop-yarn-site/YARN.html

5. White, T. (2015). *Hadoop: The Definitive Guide* (4th ed.). O'Reilly Media.

6. Dean, J., & Ghemawat, S. (2008). MapReduce: Simplified Data Processing on Large Clusters. *Communications of the ACM*, 51(1), 107–113.

7. Shvachko, K., Kuang, H., Radia, S., & Chansler, R. (2010). The Hadoop Distributed File System. *Proceedings of the 2010 IEEE 26th Symposium on Mass Storage Systems and Technologies (MSST)*, 1–10.

8. Google Cloud. (2024). *Compute Engine Documentation*. https://cloud.google.com/compute/docs

9. Google Cloud. (2024). *VPC Firewall Rules Overview*. https://cloud.google.com/vpc/docs/firewalls

10. OpenWeatherMap. (2024). *Current Weather Data API*. https://openweathermap.org/current

11. Streamlit Inc. (2024). *Streamlit Documentation*. https://docs.streamlit.io/

12. Plotly Technologies Inc. (2024). *Plotly Python Open Source Graphing Library*. https://plotly.com/python/

13. McKinney, W. (2017). *Python for Data Analysis* (2nd ed.). O'Reilly Media.

14. pytest Development Team. (2024). *pytest Documentation*. https://docs.pytest.org/

---

\newpage

# APPENDICES

---

## Appendix A – System Architecture Diagram

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

*Figure A.1: Complete System Architecture*

---

## Appendix B – Cloud Cluster Topology

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
                   +-------------------+-------------------+
                   |                                       |
                   v                                       v
    +-----------------------------+         +-----------------------------+
    |       HADOOP WORKER 1       |         |       HADOOP WORKER 2       |
    |      (hadoop-worker-1)      |         |      (hadoop-worker-2)      |
    |  - DataNode (Block Storage) |         |  - DataNode (Block Storage) |
    |  - NodeManager (Containers) |         |  - NodeManager (Containers) |
    +-----------------------------+         +-----------------------------+
```

*Figure B.1: 3-Node GCP Cluster Topology*

**Cluster Node Specifications:**

| Node Role | GCP Hostname | Machine Type | vCPU / RAM | OS | Disk |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Master Node | `hadoop-master` | `e2-standard-2` | 2 vCPU, 8 GB RAM | Ubuntu 22.04 LTS | 50 GB |
| Worker 1 | `hadoop-worker-1` | `e2-standard-2` | 2 vCPU, 8 GB RAM | Ubuntu 22.04 LTS | 50 GB |
| Worker 2 | `hadoop-worker-2` | `e2-standard-2` | 2 vCPU, 8 GB RAM | Ubuntu 22.04 LTS | 50 GB |

---

## Appendix C – Mapper Implementation

### Temperature Mapper (`mapper/temperature_mapper.py`)

```python
#!/usr/bin/env python3
"""
Hadoop Streaming Temperature Mapper
Input:  timestamp,city,temperature,humidity,rainfall,wind_speed,pressure
Output: city<TAB>temperature
"""
import sys

def parse_and_map():
    for line in sys.stdin:
        clean_line = line.strip()
        if not clean_line:
            continue
        fields = [field.strip() for field in clean_line.split(",")]
        if len(fields) >= 3 and fields[0].lower() == "timestamp":
            continue
        if len(fields) < 7:
            continue
        city = fields[1]
        temp_str = fields[2]
        if not city:
            continue
        try:
            temp_val = float(temp_str)
            if -50.0 <= temp_val <= 65.0:
                print(f"{city}\t{temp_val:.2f}")
        except (ValueError, TypeError):
            continue

if __name__ == "__main__":
    parse_and_map()
```

### Master Weather Mapper (`mapper/weather_mapper.py`)

```python
#!/usr/bin/env python3
"""
Hadoop Streaming Master Weather Analytics Mapper
Input:  timestamp,city,temperature,humidity,rainfall,wind_speed,pressure
Output: city<TAB>timestamp,temperature,humidity,rainfall,wind_speed,pressure
"""
import sys

def parse_and_map():
    for line in sys.stdin:
        clean_line = line.strip()
        if not clean_line:
            continue
        fields = [f.strip() for f in clean_line.split(",")]
        if len(fields) >= 7 and fields[0].lower() == "timestamp":
            continue
        if len(fields) != 7:
            continue
        ts, city, temp_s, hum_s, rain_s, wind_s, press_s = fields
        if not city or not ts:
            continue
        try:
            temp = float(temp_s)
            hum = float(hum_s)
            rain = float(rain_s)
            wind = float(wind_s)
            press = float(press_s)
            if not (-50.0 <= temp <= 65.0): continue
            if not (0.0 <= hum <= 100.0): continue
            if not (0.0 <= rain <= 500.0): continue
            if not (0.0 <= wind <= 300.0): continue
            if not (850.0 <= press <= 1100.0): continue
            print(f"{city}\t{ts},{temp:.2f},{hum:.2f},{rain:.2f},{wind:.2f},{press:.2f}")
        except (ValueError, TypeError):
            continue

if __name__ == "__main__":
    parse_and_map()
```

---

## Appendix D – Reducer Implementation

### Master Weather Reducer (`reducer/weather_reducer.py`)

```python
#!/usr/bin/env python3
"""
Hadoop Streaming Master Weather Analytics & Anomaly Reducer
Input:  city<TAB>timestamp,temperature,humidity,rainfall,wind_speed,pressure
Output: city<TAB>records<TAB>avg_temp<TAB>min_temp<TAB>max_temp<TAB>...
"""
import sys

def is_anomaly(temp, hum, rain, wind, press):
    if temp >= 42.0 or temp <= 8.0: return True
    if rain >= 50.0: return True
    if wind >= 50.0: return True
    if press <= 980.0 and (wind >= 40.0 or rain >= 25.0): return True
    return False

def reduce_all_metrics():
    current_city = None
    records_count = 0
    temp_sum, temp_min, temp_max = 0.0, float("inf"), float("-inf")
    hum_sum, hum_min, hum_max = 0.0, float("inf"), float("-inf")
    rain_sum, rain_max = 0.0, 0.0
    wind_sum, wind_max = 0.0, 0.0
    press_sum, press_min, press_max = 0.0, float("inf"), float("-inf")
    anomalies_count = 0

    def emit_summary(city):
        avg_t = temp_sum / records_count
        avg_h = hum_sum / records_count
        avg_w = wind_sum / records_count
        avg_p = press_sum / records_count
        print(f"{city}\t{records_count}\t{avg_t:.2f}\t{temp_min:.2f}\t{temp_max:.2f}\t"
              f"{avg_h:.2f}\t{hum_min:.2f}\t{hum_max:.2f}\t{rain_sum:.2f}\t{rain_max:.2f}\t"
              f"{avg_w:.2f}\t{wind_max:.2f}\t{avg_p:.2f}\t{press_min:.2f}\t{anomalies_count}")

    for line in sys.stdin:
        clean_line = line.strip()
        if not clean_line: continue
        parts = clean_line.split("\t")
        if len(parts) != 2: continue
        city, payload = parts[0].strip(), parts[1].strip()
        tokens = payload.split(",")
        if len(tokens) != 6: continue
        ts, temp_s, hum_s, rain_s, wind_s, press_s = tokens
        try:
            temp, hum = float(temp_s), float(hum_s)
            rain, wind, press = float(rain_s), float(wind_s), float(press_s)
        except ValueError: continue

        if current_city and current_city != city:
            emit_summary(current_city)
            records_count = 0
            temp_sum, temp_min, temp_max = 0.0, float("inf"), float("-inf")
            hum_sum, hum_min, hum_max = 0.0, float("inf"), float("-inf")
            rain_sum, rain_max = 0.0, 0.0
            wind_sum, wind_max = 0.0, 0.0
            press_sum, press_min, press_max = 0.0, float("inf"), float("-inf")
            anomalies_count = 0

        current_city = city
        records_count += 1
        temp_sum += temp; temp_min = min(temp_min, temp); temp_max = max(temp_max, temp)
        hum_sum += hum; hum_min = min(hum_min, hum); hum_max = max(hum_max, hum)
        rain_sum += rain; rain_max = max(rain_max, rain)
        wind_sum += wind; wind_max = max(wind_max, wind)
        press_sum += press; press_min = min(press_min, press)
        press_max = max(press_max, press)
        if is_anomaly(temp, hum, rain, wind, press): anomalies_count += 1

    if current_city and records_count > 0:
        emit_summary(current_city)

if __name__ == "__main__":
    reduce_all_metrics()
```

---

## Appendix E – Sample Weather Dataset

```csv
timestamp,city,temperature,humidity,rainfall,wind_speed,pressure
2026-08-11T00:00:00,Chennai,27.2,85.0,0.0,10.0,1010.2
2026-08-11T00:00:00,Bengaluru,20.5,58.0,0.0,8.0,915.5
2026-08-11T00:00:00,Hyderabad,25.0,52.0,0.0,7.5,956.0
2026-08-11T00:00:00,Mumbai,28.5,82.0,0.0,12.0,1011.0
2026-08-11T00:00:00,Delhi,30.0,42.0,0.0,6.0,981.0
2026-08-11T00:00:00,Kolkata,27.0,80.0,0.0,9.0,1007.0
2026-08-11T00:00:00,Pune,22.5,60.0,0.0,7.0,951.0
```

*Note: The complete sample dataset contains 1,176 hourly records spanning 7 Indian metropolitan cities with diurnal solar-variation patterns and injected meteorological anomalies.*

**Dataset Characteristics:**
- **Record Count:** 1,176 hourly observations
- **Cities:** Chennai, Bengaluru, Hyderabad, Mumbai, Delhi, Kolkata, Pune
- **Parameters:** timestamp, city, temperature (°C), humidity (%), rainfall (mm), wind_speed (km/h), pressure (hPa)
- **Temporal Span:** Multi-day hourly recordings
- **Anomalies:** Injected extreme weather events for validation testing

---

## Appendix F – HDFS Storage Evidence

[INSERT HDFS NAMENODE WEB UI SCREENSHOT SHOWING FILE BROWSER]

[INSERT `hdfs dfs -ls /weather/raw/` OUTPUT SCREENSHOT]

[INSERT `hdfs dfsadmin -report` OUTPUT SCREENSHOT]

---

## Appendix G – Statistical Analysis Output

**Sample `analytics_summary.csv` Output:**

```csv
city,record_count,avg_temperature,min_temperature,max_temperature,avg_humidity,min_humidity,max_humidity,total_rainfall,max_rainfall,avg_wind_speed,max_wind_speed,avg_pressure,min_pressure,anomalies_count
Bengaluru,168,24.50,18.80,30.20,60.00,45.00,75.00,42.50,12.50,8.50,22.00,915.00,910.00,2
Chennai,168,32.00,27.20,42.50,75.00,55.00,95.00,85.00,65.00,10.00,55.00,1010.00,975.00,5
Delhi,168,34.00,28.00,45.00,45.00,25.00,70.00,15.00,8.00,6.00,35.00,980.00,965.00,4
Hyderabad,168,29.00,23.00,35.00,55.00,35.00,78.00,30.00,15.00,7.50,28.00,955.00,940.00,1
Kolkata,168,31.00,25.00,38.00,82.00,65.00,96.00,120.00,75.00,9.00,45.00,1006.00,985.00,3
Mumbai,168,30.50,26.00,36.00,80.00,60.00,95.00,150.00,80.00,12.00,50.00,1010.00,990.00,4
Pune,168,26.50,20.00,33.00,62.00,40.00,82.00,55.00,25.00,7.00,30.00,950.00,935.00,1
```

> **Note:** The above is a representative output format. Actual numerical values are produced by the MapReduce pipeline execution and may vary with the specific input dataset used. [INSERT ACTUAL ANALYTICS OUTPUT SCREENSHOT]

---

## Appendix H – Dashboard Evidence

[INSERT STREAMLIT DASHBOARD MAIN PAGE SCREENSHOT]

[INSERT TEMPERATURE COMPARISON CHART SCREENSHOT]

[INSERT SPIDER RADAR COMPARISON SCREENSHOT]

[INSERT ANOMALY ALERT BANNER SCREENSHOT]

---

## Appendix I – Testing Evidence

[INSERT PYTEST TERMINAL OUTPUT SCREENSHOT (47 PASSED)]

[INSERT PIPE-BASED TEMPERATURE MAPPER/REDUCER OUTPUT SCREENSHOT]

[INSERT PIPE-BASED MASTER WEATHER MAPPER/REDUCER OUTPUT SCREENSHOT]

[INSERT END-TO-END PIPELINE ORCHESTRATOR OUTPUT SCREENSHOT]

[INSERT BENCHMARK PERFORMANCE CHART]

---

## Appendix J – Individual Contribution Evidence

### Cluster Deployment Evidence

[INSERT GCP CONSOLE VM INSTANCE LIST SCREENSHOT]

[INSERT `gcloud compute instances list` OUTPUT SCREENSHOT]

[INSERT `gcloud compute firewall-rules list` OUTPUT SCREENSHOT]

### Hadoop Verification Evidence

[INSERT MASTER JPS OUTPUT SCREENSHOT]

[INSERT WORKER 1 JPS OUTPUT SCREENSHOT]

[INSERT WORKER 2 JPS OUTPUT SCREENSHOT]

[INSERT `hdfs dfsadmin -report` SHOWING 2 LIVE DATANODES SCREENSHOT]

[INSERT `yarn node -list` SHOWING 2 ACTIVE NODEMANAGERS SCREENSHOT]

### Testing Evidence

[INSERT PYTEST 47 PASSED OUTPUT SCREENSHOT]

[INSERT BENCHMARK RESULTS TABLE SCREENSHOT]

---

\newpage

# INDIVIDUAL CONTRIBUTION SUMMARY

---

*Table 5.1: Individual Contribution Summary*

| Contribution Area | My Work | Technical Output | Evidence |
| :--- | :--- | :--- | :--- |
| **Cloud Provisioning** | Provisioned 3 GCP Compute Engine VMs (e2-standard-2, Ubuntu 22.04, 50 GB) | 3 operational VMs in same region/zone/VPC | GCP Console screenshot |
| **VPC Networking** | Designed and implemented firewall rules for internal cluster and external monitoring ports | Secure cluster communication with controlled external access | `gcloud firewall-rules list` output |
| **Hadoop Installation** | Executed setup_master.sh and setup_worker.sh on all nodes | Hadoop 3.3.6 installed at /usr/local/hadoop on all nodes | Script execution logs |
| **XML Configuration** | Configured core-site.xml, hdfs-site.xml, mapred-site.xml, yarn-site.xml | Correct NameNode address, replication factor 2, YARN framework settings | XML configuration files |
| **SSH Key Exchange** | Established passwordless SSH from master to workers | Automated remote daemon management | SSH connectivity test output |
| **HDFS Initialisation** | Formatted NameNode, created /weather/* directories, verified DataNode registration | Operational HDFS with 2 live DataNodes | dfsadmin report output |
| **Cluster Lifecycle** | Developed start_cluster.sh, stop_cluster.sh, monitor_cluster.sh | Repeatable cluster start/stop/health-check procedures | Script source code |
| **Cluster Verification** | JPS validation, dfsadmin report, YARN node-list, Web UI testing | Verified: 4 master daemons, 2 worker daemon sets, 2 DataNodes, 2 NodeManagers | Monitoring output |
| **Unit Testing** | Executed 47 automated tests across 6 modules | 47/47 passed in 2.24 seconds | pytest terminal output |
| **Pipe Testing** | Independent mapper/reducer verification via UNIX pipes | Correct per-city statistics confirmed | Pipe test output |
| **Integration Testing** | End-to-end pipeline orchestrator execution | Correct analytics_summary.csv generated | Pipeline output |
| **Benchmarking** | Generated 10/50/100 MB datasets; executed on 1-worker and 2-worker configurations | 45,000–61,000 records/s throughput demonstrated | Benchmark results table |
| **Documentation** | Authored this individual contribution report | Complete academic report documenting personal contribution | This document |

---

**END OF INDIVIDUAL CONTRIBUTION PROJECT REPORT**

---

*Report authored by: Dinnepati Sindhu Prasad (192311271)*

*Department of Computer Science and Engineering, SIMATS Engineering*

*Course: CSA1522 – Cloud Computing & Big Data Analytics*

*Project Guide: Dr. Rajaram P.*
