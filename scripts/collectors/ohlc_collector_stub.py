import pandas as pd

def coletar_ohlc_por_intervalo(symbol, start_brt, end_brt):
    # Simula ou carrega dados já coletados
    caminho = f"data/raw/{symbol}/{start_brt.strftime('%Y-%m-%d')}/{symbol}_ohlc_{start_brt.strftime('%H%M')}.parquet"
    try:
        return pd.read_parquet(caminho)
    except FileNotFoundError:
        return pd.DataFrame()
