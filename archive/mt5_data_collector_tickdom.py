import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta

mt5.initialize()

#Horário de Brasília (UTC-3)
start_brt = datetime(2025, 9, 11, 9)
end_brt = datetime(2025, 9, 11, 13)

#Converte para UTC
start_utc = start_brt - timedelta(hours=3)
end_utc = end_brt - timedelta(hours=3)

symbol = "PETR4"
start = datetime(2025, 9, 11, 9)
end = datetime(2025, 9, 11, 12)

# Ticks
ticks = mt5.copy_ticks_range(symbol, start_utc, end_utc, mt5.COPY_TICKS_ALL)
df_ticks = pd.DataFrame(ticks)
df_ticks['time'] = pd.to_datetime(df_ticks['time'], unit='s')
df_ticks.rename(columns={'time': 'timestamp'}, inplace=True)
df_ticks.to_csv(f"ticks_{symbol.replace('$','')}_0900_1200.csv", index=False)

# DOM snapshot (exemplo: uma captura única)
mt5.market_book_add(symbol)
book = mt5.market_book_get(symbol)
mt5.market_book_release(symbol)
mt5.shutdown()

if book:
    df_dom = pd.DataFrame(book)
    df_dom.to_csv(f"dom_snapshot_{symbol.replace('$','')}_0900.csv", index=False)
