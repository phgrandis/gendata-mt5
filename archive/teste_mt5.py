import MetaTrader5 as mt5

# Inicializa o terminal MT5
if not mt5.initialize():
    print("Erro ao iniciar MT5:", mt5.last_error())
else:
    print("MT5 conectado com sucesso!")
    mt5.shutdown()
