# NOAA Data Engineering Pipeline Dashboard

A comprehensive Data Engineering pipeline designed to automate the extraction, transformation, and loading (ETL) of NOAA data for analysis of environmental patterns, specifically algae growth influenced by weather patterns and sea surface temperatures.

## Project Overview

This project establishes a robust, automated pipeline integrating data extraction from NOAA APIs, data transformation with Apache Spark, and storage into PostgreSQL databases. It sets the foundation for advanced analysis using Physics-Informed Neural Networks (PINNs) to model and evaluate algae growth patterns.

### Hypothesis

Specific weather patterns and sea surface temperatures can predict algae growth rates, allowing us to leverage machine learning, specifically Physics-Informed Neural Networks, to improve ecological forecasting.

---

## Current Progress

### 1. Data Extraction

* **NOAA API**: Automated extraction of weather and sea surface temperature data from NOAA's publicly available APIs.
* **Python & Bash Scripts**: Utilized for scheduled API calls, data retrieval, and initial data storage.

### 2. Data Transformation

* **Apache Spark**: Used for scalable transformation of raw data, including cleansing, aggregation, and enrichment to prepare datasets for analysis.
* **Hadoop (HDFS)**: Integrated to store large datasets efficiently and to facilitate distributed data processing.

### 3. Data Loading

* **PostgreSQL**: Chosen for structured data storage, leveraging SQL for data management and querying capabilities.
* **dbt**: Implemented for consistent, scalable transformations within PostgreSQL, enabling efficient data modeling and validation.

### 4. Workflow Automation

* **Apache Airflow**: Orchestrates the ETL pipeline, managing scheduling, dependencies, and error handling to ensure reliability and efficiency.
* **Docker**: Containerizes services for consistent development and deployment environments.

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
│   ├── 📄 noaa_etl_dag.py
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
│   │   └── 📄 climate_resolver.py
│   │
│   ├── 📂 spark_utils/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 spark_session.py
│   │   └── 📄 hdfs_helpers.py
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
│   └── 📄 transform_climate.py
│
├── 📂 data/
│   ├── 📂 raw/
│   ├── 📂 transformed/
│   ├── 📂 postgres_data/
│   └── 📂 hadoop_data/
│
├── 📄 docker-compose.yaml
├── 📄 .dockerignore
├── 📄 .env
├── 📄 requirements.txt
├── 📄 .gitignore
└── 📄 README.md

```

---

## Future Plans

### Physics-Informed Neural Networks (PINNs)

* Implement PINNs to incorporate physical laws governing algae growth alongside environmental data.
* Use TensorFlow or PyTorch for model development and training.

### Integration and Visualization

* Develop interactive dashboards using Streamlit and Plotly to visualize predictions and analyses.
* Deploy dashboards via Azure for seamless integration within existing infrastructure.

---

## Tools and Technologies

* **Programming & Scripting:** Python, Bash
* **Data Management:** SQL, PostgreSQL, dbt
* **Data Processing:** Apache Spark, Hadoop (HDFS)
* **Workflow Orchestration:** Apache Airflow
* **Containerization:** Docker
* **Machine Learning:** TensorFlow/PyTorch (planned for PINNs)
* **Visualization:** Streamlit, Plotly (planned)
* **Cloud Deployment:** Azure (planned)

---

## Contribution and Collaboration

This project is under active development. Contributions, suggestions, and collaboration requests are welcome. Please open an issue or pull request to engage with the project.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
