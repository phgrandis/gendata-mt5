# run_pipeline.py

from scripts.ingest.clean_ohlc import clean_ohlc
from scripts.ingest.clean_dom import clean_dom
from scripts.ingest.clean_ticks import clean_ticks
from scripts.ingest.utils import list_parquet_files, list_csv_files

# Caminhos base
ohlc_raw_path = "data/raw/ohlc"
dom_raw_path = "data/"
ticks_raw_path = "data/raw/ticks"

# OHLC
print("🚀 Iniciando limpeza OHLC...")
for symbol in ["WINV25", "PETR4", "VALE3", "ITUB4"]:
    folder = f"{ohlc_raw_path}/{symbol}/2025-09-24"
    for file in list_parquet_files(folder):
        table_name = f"ohlc_{symbol.lower()}"
        clean_ohlc(file, table_name)

# DOM
print("🚀 Iniciando limpeza DOM...")
for symbol in ["WINV25", "PETR4", "VALE3", "ITUB4"]:
    file = f"{dom_raw_path}/dom_{symbol}_snapshot.csv"
    table_name = f"dom_{symbol.lower()}"
    clean_dom(file, table_name)

# Ticks (se houver)
print("🚀 Iniciando limpeza Ticks...")
for symbol in ["WINV25", "PETR4", "VALE3", "ITUB4"]:
    folder = f"{ticks_raw_path}/{symbol}/2025-09-24"
    for file in list_parquet_files(folder):
        table_name = f"ticks_{symbol.lower()}"
        clean_ticks(file, table_name)

print("✅ Pipeline finalizado com sucesso!")
