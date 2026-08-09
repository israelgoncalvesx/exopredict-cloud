# BIBLIOTECAS
from pathlib import Path

import pandas as pd

# CAMINHOS
PROJECT_ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = PROJECT_ROOT / "data" / "raw" / "kepler_koi.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "DICTIONARY.md"

# Colunas que a NASA não descreve no cabeçalho do CSV porque são
# artefatos da exportação, não medidas científicas.
MANUAL_OVERRIDES = {
    "rowid": (
        "Identificador sequencial gerado pela exportação do NASA "
        "Exoplanet Archive (1..N). Não é uma medida astrofísica — "
        "não deve ser usada como feature de modelo."
    ),
}


def parse_column_descriptions(csv_path: Path) -> dict[str, str]:
    """Lê as linhas '# COLUMN nome: descrição' do cabeçalho do CSV da NASA."""
    descriptions = {}

    with open(csv_path, encoding="utf-8") as arquivo:
        for linha in arquivo:
            if not linha.startswith("#"):
                break
            if linha.startswith("# COLUMN"):
                _, resto = linha.split("COLUMN", 1)
                nome, descricao = resto.split(":", 1)
                descriptions[nome.strip()] = descricao.strip()

    return descriptions


def main() -> None:
    descriptions = parse_column_descriptions(CSV_PATH)

    df = pd.read_csv(CSV_PATH, comment="#", dtype={"koi_quarters": "string"})

    linhas = [
        "# Dicionário de dados — tabela `koi_raw`",
        "",
        "Gerado automaticamente por `src/generate_data_dictionary.py` "
        "a partir dos comentários de cabeçalho de "
        "`data/raw/kepler_koi.csv`. Não editar manualmente — "
        "reexecute o script se o CSV de origem mudar.",
        "",
        f"Total de colunas: {len(df.columns)}",
        "",
        "| Coluna | Tipo (pandas) | Descrição (NASA Exoplanet Archive) |",
        "|---|---|---|",
    ]

    for coluna in df.columns:
        tipo = df[coluna].dtype
        descricao = descriptions.get(
            coluna,
            MANUAL_OVERRIDES.get(coluna, "_(sem descrição no cabeçalho do CSV)_"),
        )
        linhas.append(f"| `{coluna}` | `{tipo}` | {descricao} |")

    OUTPUT_PATH.write_text("\n".join(linhas) + "\n", encoding="utf-8")

    documentadas = sum(
        1 for coluna in df.columns if coluna in descriptions or coluna in MANUAL_OVERRIDES
    )

    print(f"Dicionário gerado em: {OUTPUT_PATH}")
    print(f"Colunas documentadas: {documentadas} de {len(df.columns)}")


if __name__ == "__main__":
    main()
