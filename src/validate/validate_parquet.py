import pandas as pd
import os

def validate_parquet(path):
    df = pd.read_parquet(path)
    print(f"✅ {os.path.basename(path)}")
    print(f"→ Linhas: {len(df)}")
    print(f"→ Colunas: {df.columns.tolist()}")
    print(f"→ Nulos:\n{df.isnull().sum()}")
    print("-" * 40)

def validate_parquet_folder(folder_path):
    if not os.path.exists(folder_path):
        print(f"⚠️ Pasta não encontrada: {folder_path}")
        return

    files = [f for f in os.listdir(folder_path) if f.endswith(".parquet")]
    if not files:
        print(f"⚠️ Nenhum .parquet encontrado em: {folder_path}")
        return

    for file in sorted(files):
        full_path = os.path.join(folder_path, file)
        try:
            df = pd.read_parquet(full_path)
            n_rows = len(df)
            ts_col = "timestamp" if "timestamp" in df.columns else df.columns[0]
            min_ts = df[ts_col].min()
            max_ts = df[ts_col].max()
            print(f"✅ {file} → {n_rows} linhas | {ts_col}: {min_ts} → {max_ts}")
        except Exception as e:
            print(f"❌ Erro ao ler {file}: {e}")
