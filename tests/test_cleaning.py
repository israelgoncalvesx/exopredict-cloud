import numpy as np
import pandas as pd

from cleaning import (
    LIMITE_KOI_PRAD_PLAUSIVEL,
    corrigir_koi_depth_zero,
    corrigir_koi_prad_implausivel,
    engenheirar_koi_num_quarters,
)


def test_koi_depth_zero_vira_nan():
    df = pd.DataFrame({"koi_depth": [0.0, 100.0, 0.0, np.nan]})
    resultado = corrigir_koi_depth_zero(df)

    assert resultado["koi_depth"].isna().sum() == 3  # os dois zeros + o nan original
    assert resultado.loc[1, "koi_depth"] == 100.0


def test_koi_prad_implausivel_vira_nan_com_flag():
    df = pd.DataFrame({"koi_prad": [1.0, LIMITE_KOI_PRAD_PLAUSIVEL + 1, 2.0, np.nan]})
    resultado = corrigir_koi_prad_implausivel(df)

    assert resultado["koi_prad_implausivel"].tolist() == [0, 1, 0, 0]
    assert pd.isna(resultado.loc[1, "koi_prad"])
    assert resultado.loc[0, "koi_prad"] == 1.0


def test_koi_num_quarters_conta_uns_da_string():
    df = pd.DataFrame({"koi_quarters": ["111000", "1111111111", None]})
    resultado = engenheirar_koi_num_quarters(df)

    assert resultado["koi_num_quarters"].tolist()[:2] == [3, 10]
    assert pd.isna(resultado["koi_num_quarters"].iloc[2])


def test_dados_limpos_nao_tem_vazamento_nem_colunas_vazias(df_limpo):
    assert "koi_score" not in df_limpo.columns
    assert "koi_pdisposition" not in df_limpo.columns
    assert "kepler_name" not in df_limpo.columns  # vazamento estrutural, reports/eda.md bloco 3

    assert df_limpo["koi_depth"].eq(0).sum() == 0
    assert (df_limpo["koi_prad"] > LIMITE_KOI_PRAD_PLAUSIVEL).sum() == 0
