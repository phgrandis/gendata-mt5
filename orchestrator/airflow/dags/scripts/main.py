from datetime import datetime
import os
import pandas as pd
from scripts.mt5_connector import conectar_mt5, desconectar_mt5
from scripts.data_collector import salvar_csv
from scripts.collectors.ohlc_collector import coletar_ohlc_por_intervalo
from scripts.collectors.tickdom_collector import coletar_ticks, coletar_dom
from scripts.contract_identifier import get_dolar_contract, get_indice_contract
import time



def main():
    conectar_mt5()

    # Lista de ativos
    symbols = [
        get_indice_contract(),
    #   get_dolar_contract(),
        "PETR4","VALE3","ITUB4"]
    
    now = datetime.now()   

    #start_brt = datetime(2025, 9, 24, 9)
    #end_brt = datetime(2025, 9, 24, 13)
    start_brt = now.replace(hour=9, minute=0, second=0, microsecond=0)
    end_brt = now.replace(hour=13, minute=0, second=0, microsecond=0)

    for symbol in symbols:
        print(f"📊 Coletando dados para {symbol}...")

        # OHLC
        t0 = time.time()
        
        df_ohlc = coletar_ohlc_por_intervalo(symbol, start_brt, end_brt)
        '''
        salvar_csv(df_ohlc, f"ohlc_1min_{symbol}_0900_1300.csv")
        print(f"✅ OHLC coletado em {time.time() - t0:.2f} segundos")
        '''
        if not df_ohlc.empty:
            pasta = f"data/raw/ohlc/{symbol}/{start_brt.strftime('%Y-%m-%d')}"
            os.makedirs(pasta, exist_ok=True)

            nome_arquivo = f"{symbol}_ohlc_{start_brt.strftime('%H%M')}_{end_brt.strftime('%H%M')}.parquet"
            caminho_parquet = os.path.join(pasta, nome_arquivo)

            df_ohlc.to_parquet(caminho_parquet, index=False)
            print(f"✅ OHLC salvo em: {caminho_parquet}")
        else:
            print("⚠️ Nenhum dado coletado.")

        # Ticks
        t1 = time.time()
        df_ticks = coletar_ticks(symbol, start_brt, end_brt)
        '''
        salvar_csv(df_ticks, f"ticks_{symbol}_0900_1300.csv")
        print(f"✅ Ticks coletados em {time.time() - t1:.2f} segundos")
        '''

        if not df_ticks.empty:
            pasta = f"data/raw/ticks/{symbol}/{start_brt.strftime('%Y-%m-%d')}"
            os.makedirs(pasta, exist_ok=True)

            nome_arquivo = f"{symbol}_ticks_{start_brt.strftime('%H%M')}_{end_brt.strftime('%H%M')}.parquet"
            caminho_parquet = os.path.join(pasta, nome_arquivo)

            df_ticks.to_parquet(caminho_parquet, index=False)
            print(f"✅ TICKS salvo em: {caminho_parquet}")
        else:
            print("⚠️ Nenhum dado coletado.")

        # DOM
        t2 = time.time()
        df_dom = coletar_dom(symbol)
        salvar_csv(df_dom, f"dom_{symbol}_snapshot.csv")
        print(f"✅ DOM coletado em {time.time() - t2:.2f} segundos")

    desconectar_mt5()

if __name__ == "__main__":
    main()
