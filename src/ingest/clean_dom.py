from scripts.ingest.duckdb_session import connect_duckdb

def clean_dom(csv_path, table_name):
    con = connect_duckdb()
    df = con.execute(f"SELECT * FROM read_csv_auto('{csv_path}') LIMIT 1").fetchdf()
    if 'bid_volume' in df.columns and 'ask_volume' in df.columns:
        con.execute(f"""
            CREATE OR REPLACE TABLE {table_name} AS
            SELECT *
            FROM read_csv_auto('{csv_path}')
            WHERE bid_volume > 0 AND ask_volume > 0
        """)
    else:
        con.execute(f"""
            CREATE OR REPLACE TABLE {table_name} AS
            SELECT *
            FROM read_csv_auto('{csv_path}')
        """)
    con.close()
