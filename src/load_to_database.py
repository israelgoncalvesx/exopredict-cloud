# BIBLIOTECAS
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

# CAMINHOS
PROJECT_ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = PROJECT_ROOT / "data" / "raw" / "kepler_koi.csv"
DATABASE_PATH = PROJECT_ROOT / "database" / "exopredict.db"

df = pd.read_csv(CSV_PATH, comment="#", dtype={"koi_quarters": "string"})

# CARÁCTERÍSTICAS DO CSV

print(f"Quantidade de linhas: {df.shape[0]}")
print(f"Quantidade de colunas: {df.shape[1]}")

print("\nClassificações encontradas:")
print(df["koi_disposition"].value_counts())

# CONEXÃO PYTHON - SQLite

engine = create_engine(f"sqlite:///{DATABASE_PATH}")

print(f"\nConexão preparada para: {DATABASE_PATH}")

# SALVAR DATAFRAME DENTRO DO BANCO SQLite
df.to_sql(name="koi_raw", con=engine, if_exists="replace", index=False)

print("\nDados enviados para a tabela koi_raw.")

query_count = text(
    """
    SELECT COUNT(*) AS total_registros
    FROM koi_raw;
    """
)

with engine.connect() as connection:
    total_registros = connection.execute(query_count).scalar_one()

print(f"Total de registros no banco: {total_registros}")

# EXECUTANDO CONSULTA

query_disposition = text(
    """
    SELECT
        koi_disposition,
        COUNT(*) AS quantidade
    FROM koi_raw
    GROUP BY koi_disposition
    ORDER BY quantidade DESC;
    """
)

with engine.connect() as connection:
    resultados = connection.execute(query_disposition).fetchall()

print("\nDistribuição das classes no banco:")

for classe, quantidade in resultados:
    print(f"{classe}: {quantidade}")
