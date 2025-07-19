from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

def hello_world():
    print('Hello World from Airflow!')

with DAG(
    'example_dag',
    start_date=datetime(2024, 10, 21),
    schedule_interval='@daily',
    catchup=False,
) as dag:
    task = PythonOperator(
        task_id='hello_task',
        python_callable=hello_world,
    )