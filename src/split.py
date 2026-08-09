from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from cleaning import PROCESSED_PATH, limpar_dados, carregar_dados_brutos

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

ALVO = "koi_disposition"
SEED = 42
PROPORCAO_TESTE = 0.15
PROPORCAO_VALIDACAO = 0.15  # do total original, não do restante após separar teste


def separar_treino_validacao_teste(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Split estratificado por koi_disposition, em duas etapas (train_test_split só divide em 2)."""
    treino_val, teste = train_test_split(
        df,
        test_size=PROPORCAO_TESTE,
        stratify=df[ALVO],
        random_state=SEED,
    )

    # proporção de validação relativa ao que sobrou após tirar o teste
    proporcao_val_relativa = PROPORCAO_VALIDACAO / (1 - PROPORCAO_TESTE)
    treino, validacao = train_test_split(
        treino_val,
        test_size=proporcao_val_relativa,
        stratify=treino_val[ALVO],
        random_state=SEED,
    )

    return treino, validacao, teste


def resumo_classes(df: pd.DataFrame, nome: str) -> pd.DataFrame:
    resumo = df[ALVO].value_counts(normalize=True).mul(100).round(1)
    resumo.name = nome
    return resumo


def main() -> None:
    if not PROCESSED_PATH.exists():
        df_bruto = carregar_dados_brutos()
        df = limpar_dados(df_bruto)
    else:
        df = pd.read_csv(PROCESSED_PATH)

    treino, validacao, teste = separar_treino_validacao_teste(df)

    print(f"Treino:    {len(treino):>5} linhas ({len(treino) / len(df):.1%})")
    print(f"Validação: {len(validacao):>5} linhas ({len(validacao) / len(df):.1%})")
    print(f"Teste:     {len(teste):>5} linhas ({len(teste) / len(df):.1%})")

    comparacao = pd.concat(
        [
            resumo_classes(df, "original"),
            resumo_classes(treino, "treino"),
            resumo_classes(validacao, "validação"),
            resumo_classes(teste, "teste"),
        ],
        axis=1,
    )
    print("\nDistribuição de classes por split (%):")
    print(comparacao)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    treino.to_csv(PROCESSED_DIR / "train.csv", index=False)
    validacao.to_csv(PROCESSED_DIR / "val.csv", index=False)
    teste.to_csv(PROCESSED_DIR / "test.csv", index=False)
    print(f"\nSplits salvos em {PROCESSED_DIR.relative_to(PROJECT_ROOT)}/")


if __name__ == "__main__":
    main()
