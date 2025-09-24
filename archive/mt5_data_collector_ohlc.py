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
timeframe = mt5.TIMEFRAME_M1
#start = datetime(2025, 9, 11, 9)
#end = datetime(2025, 9, 11, 12)

rates = mt5.copy_rates_range(symbol, timeframe, start_utc, end_utc)
mt5.shutdown()

df = pd.DataFrame(rates)
df['time'] = pd.to_datetime(df['time'], unit='s')
df.rename(columns={'time': 'timestamp', 'tick_volume': 'volume'}, inplace=True)
df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
df.to_csv(f"ohlc_1min_{symbol.replace('$','')}_0900_1200.csv", index=False)
