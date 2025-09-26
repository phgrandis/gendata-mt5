import MetaTrader5 as mt5
import pandas as pd
import os

def coletar_dados(ativo="PETR4", timeframe=mt5.TIMEFRAME_M1, n=100):
    dados = mt5.copy_rates_from_pos(ativo, timeframe, 0, n)
    df = pd.DataFrame(dados)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

def salvar_csv(df, nome_arquivo):
    caminho = os.path.join("data", nome_arquivo)
    df.to_csv(caminho, index=False)
    print(f"Dados salvos em: {caminho}")
