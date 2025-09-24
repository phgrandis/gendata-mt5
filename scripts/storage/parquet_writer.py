import pandas as pd

def salvar_parquet(df, caminho):
    df.to_parquet(caminho, index=False)
