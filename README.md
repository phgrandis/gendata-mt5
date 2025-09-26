# 📈 gendata-mt5

Sistema de coleta e agendamento de dados de mercado via MetaTrader 5.

## Descrição do projeto

✅ Coletor local via MT5 (main.py)
    * Conecta ao terminal MT5
    * Identifica contratos ativos
    * Coleta:
        - OHLC de 1 minuto
        - Ticks completos
        - Snapshot do DOM
    * Salva diretamente em .parquet com estrutura compatível com o agendador

✅ Agendador containerizado
    * Roda via Docker
    * Agenda coleta por minuto
    * Lê arquivos .parquet já salvos
    * Compatível com arquitetura distribuída

✅ Separação de responsabilidades
    * Coleta MT5: local, Windows, com terminal aberto
    * Agendamento e ingestão: containerizado, multiplataforma
    * Stub de coleta para ambientes sem MT5

🧠 Padrões adotados
    * Salvamento direto em .parquet (sem duplicação)
    * Estrutura de pastas por ativo e data
    * Modularização por tipo de coleta
    * Logs claros e rastreáveis


## 🔧 Funcionalidades

- Coleta de OHLC, Ticks e DOM via MT5
- Salvamento direto em `.parquet`
- Agendador containerizado via Docker
- Separação entre coleta local e ingestão distribuída

## 🚀 Como rodar localmente

```Bash
# Ativar ambiente virtual
.\.env\Scripts\Activate.ps1

# Instalar dependências
# coletor MT5
pip install -r requirements.base.txt -r requirements.windows.txt

#pipeline/processamento
pip install -r requirements.base.txt -r requirements.linux.txt

# Rodar coleta
python main.py
```
## 🐳 Como usar o Docker

```Bash
docker-compose build
docker-compose up
```
## 🗂 Estrutura

```Estrutura
gendata-mt5/
├── main.py                          # Script principal de coleta
├── requirements.mt5.txt            # Dependências para coleta via MT5
├── docker-compose.yml              # Orquestração do agendador containerizado
├── Dockerfile.agendador            # Imagem do agendador
├── data/                           # Diretório de saída dos dados
│   └── raw/
│       ├── ohlc/{symbol}/{data}/   # OHLC em .parquet
│       ├── ticks/{symbol}/{data}/  # Ticks em .parquet
│       └── dom/{symbol}/{data}/    # Snapshot do DOM em .parquet
├── scripts/
│   ├── mt5_connector.py            # Conexão e desconexão com MT5
│   ├── contract_identifier.py      # Identificação de contratos ativos
│   ├── data_collector.py           # Funções auxiliares de salvamento
│   ├── collectors/
│   │   ├── ohlc_collector_mt5.py   # Coleta OHLC via MT5 (local)
│   │   ├── ohlc_collector_stub.py  # Stub para agendador (container)
│   │   ├── tickdom_collector.py    # Coleta de ticks e DOM
│   └── scheduler/
│       └── ohlc_scheduler.py       # Agendador containerizado
```

## Status atual e próximos passos

