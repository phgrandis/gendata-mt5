from scripts.ingest.duckdb_session import connect_duckdb

def clean_ticks(parquet_path, table_name):
    con = connect_duckdb()
    con.execute(f"""
        CREATE OR REPLACE TABLE {table_name} AS
        SELECT 
            symbol,
            CAST(time AS TIMESTAMP) AS timestamp,
            price, volume
        FROM read_parquet('{parquet_path}')
        WHERE volume > 0
    """)
    con.close()
