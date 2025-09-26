from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os

def coletar_dados():
    os.system("python /opt/airflow/dags/scripts/main.py")

def validar_dados():
    os.system("python /opt/airflow/dags/scripts/run_validate.py")

def inserir_postgres():
    os.system("python /opt/airflow/dags/scripts/ingest_postgres.py")

with DAG(
    dag_id="gendata_dag",
    start_date=datetime(2025, 9, 25),
    schedule_interval="*/1 * * * *",
    catchup=False,
    tags=["mt5", "coleta", "postgres"]
) as dag:

    coleta = PythonOperator(task_id="coletar_dados", python_callable=coletar_dados)
    validar = PythonOperator(task_id="validar_dados", python_callable=validar_dados)
    inserir = PythonOperator(task_id="inserir_postgres", python_callable=inserir_postgres)

    coleta >> validar >> inserir
