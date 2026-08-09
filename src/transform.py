"""Pipeline de transformação (imputação + log) para as features do ExoPredict.

Define a receita, mas não a executa (`fit`) sobre o dataset inteiro: fazer
isso antes do split treino/teste vazaria a distribuição do teste (ex.: a
mediana usada na imputação) para dentro do treino. Quem consome este módulo
deve chamar `fit` só com os dados de treino (ver `reports/eda.md` e
`reports/feature_selection.md` para o raciocínio por trás das escolhas).
"""

from pathlib import Path

import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Cauda longa observada e confirmada com log10 em reports/eda.md, bloco 6.
# Só as colunas efetivamente examinadas ali — não generalizamos a outras
# colunas fisicamente parecidas sem checar a distribuição de cada uma.
COLUNAS_LOG = ["koi_period", "koi_prad", "koi_depth"]


def _log1p_seguro(X: np.ndarray) -> np.ndarray:
    """log1p tolera 0 (vira 0) e preserva NaN (SimpleImputer roda depois)."""
    return np.log1p(X)


def construir_pipeline_log() -> Pipeline:
    """Imputa pela mediana e aplica log1p nas colunas de cauda longa."""
    return Pipeline(
        steps=[
            ("imputar_mediana", SimpleImputer(strategy="median")),
            ("log1p", FunctionTransformer(_log1p_seguro, feature_names_out="one-to-one")),
        ]
    )


def construir_pipeline_padrao() -> Pipeline:
    """Imputa pela mediana, sem transformação de escala."""
    return Pipeline(steps=[("imputar_mediana", SimpleImputer(strategy="median"))])


def construir_preprocessador(colunas_numericas: list[str]) -> ColumnTransformer:
    """ColumnTransformer completo: log nas colunas de cauda longa, mediana nas demais.

    `colunas_numericas` deve vir da lista de features numéricas em
    `reports/feature_selection.md` (após `src/cleaning.py`). Colunas de
    texto (ex.: `koi_quarters`) e a flag `koi_prad_implausivel` não entram
    aqui — a primeira precisa de codificação própria, a segunda já é 0/1.
    """
    colunas_log = [c for c in COLUNAS_LOG if c in colunas_numericas]
    colunas_padrao = [c for c in colunas_numericas if c not in colunas_log]

    return ColumnTransformer(
        transformers=[
            ("log", construir_pipeline_log(), colunas_log),
            ("padrao", construir_pipeline_padrao(), colunas_padrao),
        ]
    )
