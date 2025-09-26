import pandas as pd
from sqlalchemy import create_engine

def ingest_ohlc_postgres():
    df = pd.read_parquet("/opt/airflow/dags/data/raw/ohlc/WINV25/2025-09-25/WINV25_ohlc_0900_1300.parquet")
    engine = create_engine("postgresql://airflow:airflow@postgres:5432/airflow")
    df.to_sql("ohlc_winv25", engine, if_exists="append", index=False)
