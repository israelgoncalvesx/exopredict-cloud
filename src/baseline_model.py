from pathlib import Path

import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, f1_score
from sklearn.pipeline import Pipeline

from transform import construir_preprocessador

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

ALVO = "koi_disposition"
IDENTIFICADORES = ["kepoi_name", "kepid", "rowid"]

# koi_quarters é a única feature de texto entre as 103 selecionadas em
# reports/feature_selection.md; precisa de codificação categórica própria.
# Fora do escopo do baseline — ver reports/baseline_model.md.
COLUNAS_NAO_NUMERICAS_A_EXCLUIR = ["koi_quarters"]


def carregar_split(nome: str) -> pd.DataFrame:
    return pd.read_csv(PROCESSED_DIR / f"{nome}.csv")


def separar_x_y(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    colunas_excluidas = IDENTIFICADORES + [ALVO] + COLUNAS_NAO_NUMERICAS_A_EXCLUIR
    colunas_x = [c for c in df.columns if c not in colunas_excluidas]
    return df[colunas_x], df[ALVO]


def construir_modelo_baseline(colunas_numericas: list[str]) -> Pipeline:
    preprocessador = construir_preprocessador(colunas_numericas)
    return Pipeline(
        steps=[
            ("preprocessamento", preprocessador),
            (
                "classificador",
                LogisticRegression(
                    class_weight="balanced",
                    max_iter=1000,
                    random_state=42,
                ),
            ),
        ]
    )


def avaliar(nome: str, modelo, X_val: pd.DataFrame, y_val: pd.Series) -> None:
    y_pred = modelo.predict(X_val)
    f1_macro = f1_score(y_val, y_pred, average="macro")

    print(f"\n{'=' * 60}")
    print(f"{nome} — F1-macro: {f1_macro:.3f}")
    print("=" * 60)
    print(classification_report(y_val, y_pred, digits=3, zero_division=0))
    print("Matriz de confusão (linhas=real, colunas=previsto):")
    ordem = sorted(y_val.unique())
    matriz = confusion_matrix(y_val, y_pred, labels=ordem)
    print(pd.DataFrame(matriz, index=ordem, columns=ordem))


def main() -> None:
    treino = carregar_split("train")
    validacao = carregar_split("val")

    X_treino, y_treino = separar_x_y(treino)
    X_val, y_val = separar_x_y(validacao)

    dummy = DummyClassifier(strategy="most_frequent")
    dummy.fit(X_treino, y_treino)
    avaliar("Dummy (sempre a classe majoritária)", dummy, X_val, y_val)

    modelo = construir_modelo_baseline(X_treino.columns.tolist())
    modelo.fit(X_treino, y_treino)
    avaliar("Baseline (regressão logística)", modelo, X_val, y_val)


if __name__ == "__main__":
    main()
