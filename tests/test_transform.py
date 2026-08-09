import numpy as np
import pandas as pd

from transform import COLUNAS_LOG, construir_preprocessador


def _colunas_numericas(df: pd.DataFrame) -> list[str]:
    numericas = df.select_dtypes("number").columns.tolist()
    return [c for c in numericas if c not in ("kepid", "rowid", "koi_prad_implausivel")]


def test_preprocessador_nao_deixa_nan_residual(df_limpo):
    colunas = _colunas_numericas(df_limpo)
    preprocessador = construir_preprocessador(colunas)

    X_transformado = preprocessador.fit_transform(df_limpo[colunas])

    assert not np.isnan(X_transformado).any()


def test_preprocessador_produz_mesmo_numero_de_colunas(df_limpo):
    colunas = _colunas_numericas(df_limpo)
    preprocessador = construir_preprocessador(colunas)

    X_transformado = preprocessador.fit_transform(df_limpo[colunas])

    assert X_transformado.shape[1] == len(colunas)


def test_colunas_log_estao_entre_as_colunas_numericas_conhecidas(df_limpo):
    colunas = _colunas_numericas(df_limpo)
    for coluna in COLUNAS_LOG:
        assert coluna in colunas
