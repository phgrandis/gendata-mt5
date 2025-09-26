from scripts.ingest.duckdb_session import connect_duckdb

def clean_ohlc(parquet_path, table_name):
    con = connect_duckdb()
    symbol = table_name.replace("ohlc_", "").upper()
    
    con.execute(f"""
        CREATE OR REPLACE TABLE {table_name} AS
        SELECT 
            '{symbol}' AS symbol,
            timestamp,
            open, high, low, close, volume
        FROM read_parquet('{parquet_path}')
        WHERE volume > 0
    """)
    con.close()
