import MetaTrader5 as mt5
import os
import pandas as pd
from datetime import datetime, timedelta

def get_ultimo_timestamp_csv(caminho_csv):
    if not os.path.exists(caminho_csv):
        return None
    df = pd.read_csv(caminho_csv)
    if df.empty:
        return None
    return pd.to_datetime(df['timestamp'].max())


def coletar_ticks(symbol, start_brt, end_brt):
    """
    Coleta ticks entre dois horários em horário de Brasília.
    """
    start_utc = start_brt - timedelta(hours=3)
    end_utc = end_brt - timedelta(hours=3)

    ticks = mt5.copy_ticks_range(symbol, start_utc, end_utc, mt5.COPY_TICKS_ALL)
    df_ticks = pd.DataFrame(ticks)
    df_ticks['time'] = pd.to_datetime(df_ticks['time'], unit='s')
    df_ticks.rename(columns={'time': 'timestamp'}, inplace=True)
    return df_ticks


def coletar_ticks_incremental(symbol, caminho_csv, end_brt):
    ultimo_ts = get_ultimo_timestamp_csv(caminho_csv)

    if ultimo_ts is None:
        start_brt = end_brt - timedelta(minutes=1)  # ou outro valor inicial
    else:
        start_brt = ultimo_ts + timedelta(seconds=1)

    start_utc = start_brt - timedelta(hours=3)
    end_utc = end_brt - timedelta(hours=3)

    ticks = mt5.copy_ticks_range(symbol, start_utc, end_utc, mt5.COPY_TICKS_ALL)
    df = pd.DataFrame(ticks)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.rename(columns={'time': 'timestamp'}, inplace=True)

    if not df.empty:
        df.to_csv(caminho_csv, mode='a', header=not os.path.exists(caminho_csv), index=False)

    return df


def coletar_dom(symbol):
    """
    Coleta a profundidade de mercado (DOM) atual do ativo.
    """
    mt5.market_book_add(symbol)
    book = mt5.market_book_get(symbol)
    mt5.market_book_release(symbol)

    if book is None:
        return pd.DataFrame()

    df_dom = pd.DataFrame(book)
    df_dom['symbol'] = symbol
    df_dom['timestamp'] = pd.Timestamp.now()
    return df_dom
