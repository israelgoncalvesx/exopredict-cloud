from pathlib import Path

import numpy as np
import pandas as pd

from define_feature_columns import ALVO, IDENTIFICADORES, classificar_colunas, colunas_utilizaveis

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = PROJECT_ROOT / "data" / "raw" / "kepler_koi.csv"
PROCESSED_PATH = PROJECT_ROOT / "data" / "processed" / "koi_clean.csv"

LIMITE_KOI_PRAD_PLAUSIVEL = 30.0  # raios terrestres — ver reports/feature_selection.md


def carregar_dados_brutos() -> pd.DataFrame:
    return pd.read_csv(CSV_PATH, comment="#", dtype={"koi_quarters": "string"})


def selecionar_colunas_utilizaveis(df: pd.DataFrame) -> pd.DataFrame:
    """Mantém apenas identificador + alvo + features sem vazamento.

    Ver reports/feature_selection.md para o raciocínio completo.
    """
    grupos = classificar_colunas(df)
    colunas = IDENTIFICADORES + ALVO + colunas_utilizaveis(grupos)
    return df[colunas].copy()


def corrigir_koi_depth_zero(df: pd.DataFrame) -> pd.DataFrame:
    """koi_depth == 0 é placeholder de dado ausente, não medida real (reports/eda.md, bloco 6)."""
    df = df.copy()
    df.loc[df["koi_depth"] == 0, "koi_depth"] = np.nan
    return df


def corrigir_koi_prad_implausivel(
    df: pd.DataFrame, limite: float = LIMITE_KOI_PRAD_PLAUSIVEL
) -> pd.DataFrame:
    """Raio acima do limite físico plausível (mesmo para gigantes gasosos inflados) vira NaN.

    Preserva o sinal via flag booleana em vez de só descartar o valor: no
    bloco 5/7 da EDA, esses extremos concentram em FALSE POSITIVE não
    vetted — a própria implausibilidade é informativa.
    """
    df = df.copy()
    implausivel = df["koi_prad"] > limite
    df["koi_prad_implausivel"] = implausivel.astype(int)
    df.loc[implausivel, "koi_prad"] = np.nan
    return df


def engenheirar_koi_num_quarters(df: pd.DataFrame) -> pd.DataFrame:
    """koi_quarters é uma string binária (1 quarter observado / 0 não observado).

    Alta cardinalidade (170 valores únicos no treino) inviabiliza one-hot;
    a contagem de '1's (quantos quarters do Kepler observaram o alvo) é uma
    grandeza física legítima e numérica. Mantém a coluna original também —
    quem for usá-la escolhe explicitamente qual das duas quer.
    """
    df = df.copy()
    df["koi_num_quarters"] = df["koi_quarters"].str.count("1")
    return df


def limpar_dados(df: pd.DataFrame) -> pd.DataFrame:
    df = selecionar_colunas_utilizaveis(df)
    df = corrigir_koi_depth_zero(df)
    df = corrigir_koi_prad_implausivel(df)
    df = engenheirar_koi_num_quarters(df)
    return df


def main() -> None:
    df_bruto = carregar_dados_brutos()
    df_limpo = limpar_dados(df_bruto)

    print(f"Colunas brutas: {df_bruto.shape[1]}")
    print(f"Colunas após seleção (id + alvo + features): {df_limpo.shape[1]}")
    print(f"Linhas: {df_limpo.shape[0]}")
    print(f"koi_prad_implausivel == 1: {int(df_limpo['koi_prad_implausivel'].sum())}")

    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_limpo.to_csv(PROCESSED_PATH, index=False)
    print(f"\nDados limpos salvos em {PROCESSED_PATH.relative_to(PROJECT_ROOT)}")
    print(
        "Atenção: nulos remanescentes NÃO foram imputados aqui de propósito "
        "(ver src/transform.py) — imputar antes do split treino/teste "
        "vazaria informação do teste para o treino."
    )


if __name__ == "__main__":
    main()
