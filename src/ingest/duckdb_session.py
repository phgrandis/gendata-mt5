import duckdb

def connect_duckdb(db_path='data/clean/mt5_clean.duckdb'):
    return duckdb.connect(database=db_path)
