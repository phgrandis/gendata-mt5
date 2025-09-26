from validate.validate_parquet import validate_parquet_folder, validate_parquet
from datetime import date


# Ativo e data que você quer validar
symbol = "WINV25"
#date = "2025-09-25"
#folder = f"data/raw/ohlc/{symbol}/{date}"
today = date.today().isoformat()  # '2025-09-25'
folder = f"data/raw/ohlc/WINV25/{today}"

print(f"🔍 Validando coleta de {symbol} em {today}")
validate_parquet_folder(folder)
