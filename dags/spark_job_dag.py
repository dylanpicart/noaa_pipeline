from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'dylanpicart',  
    'start_date': datetime(2023, 7, 1),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG('spark_job_dag', default_args=default_args, schedule_interval='@weekly') as dag:

    pmn_job = SparkSubmitOperator(
        task_id='pmn_etl',
        application='/opt/airflow/spark_jobs/transform_pmn.py',
        conn_id='spark_default'
    )

    chlorophyll_job = SparkSubmitOperator(
        task_id='chlorophyll_etl',
        application='/opt/airflow/spark_jobs/transform_chlorophyll.py',
        conn_id='spark_default'
    )

    climate_job = SparkSubmitOperator(
        task_id='climate_etl',
        application='/opt/airflow/spark_jobs/transform_climate.py',
        conn_id='spark_default'
    )

    buoy_job = SparkSubmitOperator(
        task_id='buoy_etl',
        application='/opt/airflow/spark_jobs/transform_buoy.py',
        conn_id='spark_default'
    )

    pmn_job >> chlorophyll_job >> climate_job >> buoy_job
