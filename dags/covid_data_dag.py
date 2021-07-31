import os
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from covid_tasks import extract_data, load_to_database

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2021, 7, 30),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'covid_data_dag',
    default_args=default_args,
    description="A DAG that extracts COVID data from the public MKN repository, computes a case to death ratio and stores it in a MySQL database",
    schedule_interval=timedelta(days=1),
    catchup=False,
)

t1 = PythonOperator(
    task_id="extract_data",
    python_callable=extract_data,
    dag=dag)

t2 = PythonOperator(
    task_id="load_to_database",
    python_callable=load_to_database,
    dag=dag)

t1 >> t2
