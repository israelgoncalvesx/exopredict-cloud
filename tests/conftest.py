import pandas as pd
import pytest

from cleaning import carregar_dados_brutos, limpar_dados
from split import separar_treino_validacao_teste


@pytest.fixture(scope="session")
def df_bruto() -> pd.DataFrame:
    return carregar_dados_brutos()


@pytest.fixture(scope="session")
def df_limpo(df_bruto: pd.DataFrame) -> pd.DataFrame:
    return limpar_dados(df_bruto)


@pytest.fixture(scope="session")
def splits(df_limpo: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    return separar_treino_validacao_teste(df_limpo)
