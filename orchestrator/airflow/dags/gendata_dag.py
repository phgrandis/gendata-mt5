from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
#from scripts.mt5_connector import coletar_dados
from scripts.validate.validate_parquet import validate_parquet_folder
from scripts.ingest.ingest_postgres import ingest_ohlc_postgres

with DAG("gendata_dag", start_date=datetime(2025, 9, 25), schedule_interval="*/1 * * * *", catchup=False) as dag:
    coleta = PythonOperator(task_id="coletar_dados", python_callable=coletar_dados)
    validar = PythonOperator(task_id="validar_parquet", python_callable=lambda: validate_parquet_folder("data/raw/ohlc/WINV25/2025-09-25"))
    ingestao = PythonOperator(task_id="ingest_postgres", python_callable=ingest_ohlc_postgres)

    coleta >> validar >> ingestao
