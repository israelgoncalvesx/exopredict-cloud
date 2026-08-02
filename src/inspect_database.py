from pathlib import Path

from sqlalchemy import create_engine, text


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATABASE_PATH = PROJECT_ROOT / "database" / "exopredict.db"

engine = create_engine(
    f"sqlite:///{DATABASE_PATH}"
)

print(f"Banco que será analisado: {DATABASE_PATH}")
print(f"O banco existe? {DATABASE_PATH.exists()}")

#CONSULTA

query_tables = text(
    """
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name;
    """
)

with engine.connect() as connection:
    tabelas = connection.execute(query_tables).fetchall()

print("\nTabelas encontradas:")

for tabela in tabelas:
    print(tabela[0])

#DESCREVER A ESTRUTURA DA TABELA

query_columns = text(
    """
    PRAGMA table_info(koi_raw);
    """
)

with engine.connect() as connection:
    colunas = connection.execute(query_columns).fetchall()

print(f"\nQuantidade de colunas na tabela: {len(colunas)}")

print("\nPrimeiras 10 colunas:")

for coluna in colunas[:10]:
    print(coluna)

query_sample = text(
    """
    SELECT
        kepoi_name,
        koi_disposition,
        koi_pdisposition,
        koi_score,
        koi_fpflag_nt
    FROM koi_raw
    LIMIT 5;
    """
)

with engine.connect() as connection:
    amostra = connection.execute(query_sample).fetchall()

print("\nAmostra de colunas relacionadas à classificação:")

for registro in amostra:
    print(registro)

#COMPARAR DUAS CLASSIFICAÇÕES

query_disposition_comparison = text(
    """
    SELECT
        koi_disposition,
        koi_pdisposition,
        COUNT(*) AS quantidade
    FROM koi_raw
    GROUP BY
        koi_disposition,
        koi_pdisposition
    ORDER BY
        koi_disposition,
        quantidade DESC;
    """
)

with engine.connect() as connection:
    comparacoes = connection.execute(
        query_disposition_comparison
    ).fetchall()

print("\nComparação entre as classificações:")

for disposicao_final, disposicao_pipeline, quantidade in comparacoes:
    print(
        f"{disposicao_final} | "
        f"{disposicao_pipeline} | "
        f"{quantidade}"
    )

#MEDIA KOI SCORE POR CLASSE

query_score = text(
    """
    SELECT
        koi_disposition,
        ROUND(AVG(koi_score), 3) AS media_score
    FROM koi_raw
    GROUP BY koi_disposition
    ORDER BY media_score DESC;
    """
)

with engine.connect() as connection:
    scores = connection.execute(query_score).fetchall()

print("\nMédia do koi_score por classificação:")

for classe, media_score in scores:
    print(f"{classe}: {media_score}")