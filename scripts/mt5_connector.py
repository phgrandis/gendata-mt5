import MetaTrader5 as mt5

def conectar_mt5():
    if not mt5.initialize():
        print("❌ Falha ao inicializar MT5")
        print("Erro:", mt5.last_error())
        raise ConnectionError(f"Erro ao conectar: {mt5.last_error()}")
    else:
        print("✅ Conectado ao MT5 com sucesso")

def desconectar_mt5():
    if mt5.shutdown():
        print("✅ MT5 desconectado com sucesso")
    else:
        print("⚠️ Falha ao desconectar MT5")
