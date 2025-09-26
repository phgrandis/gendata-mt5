import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta

def coletar_ohlc_por_posicao(symbol, start_pos=0, n=100, timeframe=mt5.TIMEFRAME_M1):
    """
    Coleta os últimos n candles do ativo a partir de uma posição.
    Útil para coletas recentes.
    """
    dados = mt5.copy_rates_from_pos(symbol, timeframe, start_pos, n)
    df = pd.DataFrame(dados)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.rename(columns={'time': 'timestamp', 'tick_volume': 'volume'}, inplace=True)
    df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    return df


def coletar_ohlc_por_intervalo(symbol, start_brt, end_brt, timeframe=mt5.TIMEFRAME_M1):
    """
    Coleta candles entre dois horários específicos (em horário de Brasília).
    Converte para UTC antes de enviar ao MT5.
    """
    # Corrige conversão: Brasília (UTC−3) → UTC
    start_utc = start_brt - timedelta(hours=3)
    end_utc = end_brt - timedelta(hours=3)

    rates = mt5.copy_rates_range(symbol, timeframe, start_utc, end_utc)

    if rates is None or len(rates) == 0:
        print(f"❌ Nenhum dado encontrado para {symbol} entre {start_brt} e {end_brt}")
        return pd.DataFrame()

    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.rename(columns={'time': 'timestamp', 'tick_volume': 'volume'}, inplace=True)
    df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    return df


