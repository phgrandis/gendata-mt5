import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta

# Inicializa conexão com MT5
if not mt5.initialize():
    print("❌ Falha ao conectar ao MetaTrader 5")
    quit()

# Define ativo e intervalo
symbol = "PETR4"  # Exemplo: mini índice futuro
timeframe = mt5.TIMEFRAME_M1  # 1 minutos
days_back = 3

# Define intervalo de tempo
utc_from = datetime.now() - timedelta(days=days_back)
utc_to = datetime.now()

# Solicita dados históricos
rates = mt5.copy_rates_range(symbol, timeframe, utc_from, utc_to)

# Finaliza conexão
mt5.shutdown()

# Converte para DataFrame
df = pd.DataFrame(rates)
df['time'] = pd.to_datetime(df['time'], unit='s')

# Renomeia colunas para compatibilidade com pipeline
df.rename(columns={
    'time': 'timestamp',
    'open': 'open',
    'high': 'high',
    'low': 'low',
    'close': 'close',
    'tick_volume': 'volume'
}, inplace=True)

# Filtra colunas
df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]

# Salva como CSV
df.to_csv(f"ohlc_{symbol.replace('$','')}.csv", index=False)
print(f"✅ Dados salvos em ohlc_{symbol.replace('$','')}.csv")
