import duckdb

def validate_table(table_name):
    con = duckdb.connect("data/clean/mt5_clean.duckdb")
    print(f"📊 Validando tabela: {table_name}")
    print(con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone())
    print(con.execute(f"SELECT * FROM {table_name} LIMIT 5").fetchdf())
    con.close()
