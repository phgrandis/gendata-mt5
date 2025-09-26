import os

def list_parquet_files(base_path):
    if not os.path.exists(base_path):
        print(f"⚠️ Diretório não encontrado: {base_path}")
        return []
    return [os.path.join(base_path, f) for f in os.listdir(base_path) if f.endswith('.parquet')]

def list_csv_files(base_path):
    if not os.path.exists(base_path):
        print(f"⚠️ Diretório não encontrado: {base_path}")
        return []
    return [os.path.join(base_path, f) for f in os.listdir(base_path) if f.endswith('.csv')]
