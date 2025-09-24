import schedule
import time
from datetime import datetime, timedelta
import os

#from scripts.mt5_connector import conectar_mt5, desconectar_mt5
from scripts.collectors.ohlc_collector_stub import coletar_ohlc_por_intervalo

from scripts.contract_identifier import get_indice_contract
from scripts.storage.parquet_writer import salvar_parquet

try:
    from scripts.mt5_connector import conectar_mt5, desconectar_mt5
except ImportError:
    conectar_mt5 = lambda: None
    desconectar_mt5 = lambda: None


def tarefa_ohlc():
    conectar_mt5()

    symbol = get_indice_contract()
    now = datetime.now()

    # Define intervalo do candle anterior
    start_brt = now.replace(second=0, microsecond=0) - timedelta(minutes=1)
    end_brt = now.replace(second=0, microsecond=0)

    df = coletar_ohlc_por_intervalo(symbol, start_brt, end_brt)

    if not df.empty:
        # Cria diretório por ativo e data
        pasta = f"data/raw/{symbol}/{start_brt.strftime('%Y-%m-%d')}"
        os.makedirs(pasta, exist_ok=True)

        # Salva com timestamp do candle
        nome_arquivo = f"{symbol}_ohlc_{start_brt.strftime('%H%M')}.parquet"
        caminho = os.path.join(pasta, nome_arquivo)

        salvar_parquet(df, caminho)
        print(f"✅ OHLC salvo: {caminho}")
    else:
        print(f"⚠️ Nenhum dado OHLC disponível para {symbol} às {start_brt.strftime('%H:%M')}")

    desconectar_mt5()

# Agendar a cada minuto
schedule.every(60).seconds.do(tarefa_ohlc)

print("🕒 Agendador OHLC iniciado. Coletando a cada minuto...")

while True:
    schedule.run_pending()
    time.sleep(1)
