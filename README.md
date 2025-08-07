# NOAA Data Pipeline to PINN Analysis Dashboard

A comprehensive Data Engineering pipeline designed to automate the extraction, loading, and transformation (ELT) of NOAA data for analysis of environmental patterns, specifically phytoplankton (PMN) growth influenced by weather patterns, sea surface temperatures, and chlorophyll-a concentration.

## Project Overview

This project establishes a robust, automated pipeline integrating data extraction from NOAA APIs, data transformation with Apache Spark, and storage into PostgreSQL databases. It sets the foundation for advanced analysis using Physics-Informed Neural Networks (PINNs) to model and evaluate phytoplankton growth patterns.

### Hypothesis

Specific weather patterns, sea surface temperatures, and chlorophyll-a concentrations can predict phytoplankton growth rates, allowing us to leverage machine learning, specifically Physics-Informed Neural Networks, to improve ecological forecasting.

---

## Current Progress

### 1. Data Extraction

* **NOAA APIs**: Automated extraction of environmental data including buoy, climate anomalies, phytoplankton counts, and chlorophyll-a from NOAA's publicly available APIs.
* **Python & Bash Scripts**: Used for scheduled API calls, robust error handling, and initial data storage.

### 2. Data Transformation

* **Apache Spark**: Used for scalable transformation of raw data, including cleaning, aggregation (weekly), and alignment to prepare datasets for analysis.
* **Hadoop (HDFS & YARN)**: Integrated for efficient storage and distributed processing of large datasets.

### 3. Data Loading

* **PostgreSQL**: Structured data storage utilizing SQL for data management and querying.
* **dbt**: Planned for scalable transformations within PostgreSQL, enabling efficient data modeling and validation.

### 4. Workflow Automation

* **Apache Airflow**: Orchestrates the ELT pipeline, managing scheduling, dependencies, and error handling to ensure reliability and efficiency.
* **Docker & Docker Compose**: Containerizes services ensuring consistent development and deployment environments.

---

## Project Structure

```
📁 noaa_pipeline/
│
├── 📂 .docker/
│   ├── 📄 Dockerfile.airflow
│   ├── 📄 Dockerfile.graphql
│   └── 📄 Dockerfile.spark
│
├── 📂 dags/
│   ├── 📄 noaa_ELT_dag.py
│   ├── 📄 __init__.py
│   └── 📂 scripts/
│       ├── 📄 extract_noaa_data.py
│       ├── 📄 transform_data.py
│       └── 📄 upload_to_gcp.py
│
├── 📂 graphql/                       
│   ├── 📂 resolvers/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 pmn_resolver.py
│   │   ├── 📄 buoy_resolver.py
│   │   ├── 📄 climate_resolver.py
│   │   └── 📄 chlorophyll_resolver.py
│   │
│   ├── 📂 spark_utils/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 session.py
│   │   └── 📄 hdfs.py
│   │
│   ├── 📂 utils/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 api_requests.py
│   │   └── 📄 logging_setup.py
│   │
│   ├── 📄 schema.py
│   ├── 📄 app.py
│   └── 📄 requirements.txt
│
├── 📂 spark_jobs/
│   ├── 📄 transform_pmn.py
│   ├── 📄 transform_buoy.py
│   ├── 📄 transform_climate.py
│   └── 📄 transform_chlorophyll.py
│
├── 📂 data/
│   ├── 📂 raw/
│   ├── 📂 transformed/
│   ├── 📂 postgres_data/
│   └── 📂 hadoop_data/
│
├── 📂 postgres/
│   ├── 📄 schema.sql
│   ├── 📄 queries.sql
│   └── 📂 migrations/
│       └── 📄 V1_initial_startup.sql
│
├── 📄 docker-compose.yaml
├── 📄 .dockerignore
├── 📄 .env
├── 📄 requirements.txt
├── 📄 .gitignore
└── 📄 README.md
```
---

## **Stack Overview: End-to-End Data Engineering Environment**

With the successful setup and orchestration of **PostgreSQL**, **Hadoop (HDFS/YARN)**, **Apache Spark**, and **Apache Airflow**, you now have a complete, production-grade local data engineering pipeline. Here’s what this enables:

### **What’s Running**

* **PostgreSQL:**
  Relational database for structured storage, fast queries, and the Airflow metadata backend.
* **Hadoop HDFS:**
  Distributed file storage, designed for big data scale and fault tolerance.
* **YARN:**
  Resource manager that schedules and coordinates distributed jobs (including Spark).
* **Apache Spark:**
  High-performance in-memory compute framework for scalable ELT, analytics, and ML.
* **Apache Airflow:**
  Orchestrator for all ELT, analytics, and ML workflows—manages dependencies, scheduling, and pipeline reliability.

### **What This Enables**

* **Production-like development environment:**
  Simulate a real-world, scalable data platform—ideal for robust development, testing, and onboarding.
* **Automated, reliable ELT:**
  Airflow triggers Spark jobs, data moves in/out of HDFS, results land in PostgreSQL, and everything is containerized for repeatability.
* **Data science and analytics ready:**
  Quickly prototype, test, and deploy Spark analytics or ML jobs, even against large or distributed data.
* **Extensible and collaborative:**
  Add new nodes (DataNodes, Spark Workers) or services with minimal config changes. Perfect for scaling or team collaboration.
* **Cloud-ready:**
  The local stack mimics cloud platforms—easy to migrate or deploy to Azure or another cloud.

### **Typical Workflow Example**

1. **Airflow triggers extraction scripts** (Python/Bash) to pull fresh NOAA data.
2. **Raw data lands in HDFS**, tracked in Airflow.
3. **Spark jobs transform and aggregate** the raw data in HDFS (cleaning, weekly aggregation, feature engineering).
4. **Transformed data is loaded to PostgreSQL** for downstream analysis and dashboarding.
5. **All orchestration, scheduling, and monitoring handled by Airflow** with full auditability and retry logic.

---

## **Why This Matters**

* **You can test, debug, and iterate on real data engineering and ML pipelines before deploying to production.**
* **You are ready for advanced orchestration, distributed analytics, and future ML integration** (like PINNs), with minimal local-to-cloud friction.
* **You can collaborate, extend, and automate your workflows with confidence.**

---

## Future Plans

### Physics-Informed Neural Networks (PINNs)

* Implement PINNs to incorporate physical laws governing phytoplankton growth alongside environmental data.
* Use TensorFlow or PyTorch for model development and training.

### Integration and Visualization

* Develop interactive dashboards using Streamlit and Plotly to visualize predictions and analyses.
* Deploy dashboards via Azure for seamless integration within existing infrastructure.

---

## Tools and Technologies

* **Programming & Scripting:** Python, Bash
* **Data Management:** SQL, PostgreSQL, dbt
* **Data Processing:** Apache Spark, Hadoop (HDFS, YARN)
* **Workflow Orchestration:** Apache Airflow
* **Containerization:** Docker, Docker Compose
* **Machine Learning:** TensorFlow/PyTorch (planned for PINNs)
* **Visualization:** Streamlit, Plotly (planned)
* **Cloud Deployment:** Azure (planned)

---

## Contribution and Collaboration

This project is under active development. Contributions, suggestions, and collaboration requests are welcome. Please open an issue or pull request to engage with the project.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Under development by **Dylan Picart**.
