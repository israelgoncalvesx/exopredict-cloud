from pathlib import Path

import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score
from sklearn.pipeline import Pipeline

from baseline_model import carregar_split
from transform import construir_preprocessador

PROJECT_ROOT = Path(__file__).resolve().parents[1]

ALVO = "koi_disposition"
IDENTIFICADORES = ["kepoi_name", "kepid", "rowid"]

# koi_quarters (string, 170 valores únicos) foi substituída por koi_num_quarters
# (contagem de '1's), engenheirada em src/cleaning.py — ver reports/model_comparison.md.
COLUNAS_NAO_NUMERICAS_A_EXCLUIR = ["koi_quarters"]


def separar_x_y(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    colunas_excluidas = IDENTIFICADORES + [ALVO] + COLUNAS_NAO_NUMERICAS_A_EXCLUIR
    colunas_x = [c for c in df.columns if c not in colunas_excluidas]
    return df[colunas_x], df[ALVO]


def construir_candidatos(colunas_numericas: list[str]) -> dict[str, Pipeline]:
    preprocessador = construir_preprocessador(colunas_numericas)

    return {
        "Regressão logística (baseline)": Pipeline(
            steps=[
                ("preprocessamento", preprocessador),
                (
                    "classificador",
                    LogisticRegression(
                        class_weight="balanced", max_iter=1000, random_state=42
                    ),
                ),
            ]
        ),
        "Random Forest": Pipeline(
            steps=[
                ("preprocessamento", preprocessador),
                (
                    "classificador",
                    RandomForestClassifier(
                        n_estimators=300,
                        class_weight="balanced",
                        random_state=42,
                        n_jobs=-1,
                    ),
                ),
            ]
        ),
        "Gradient Boosting (histograma)": Pipeline(
            steps=[
                ("preprocessamento", preprocessador),
                (
                    "classificador",
                    HistGradientBoostingClassifier(
                        class_weight="balanced", random_state=42
                    ),
                ),
            ]
        ),
    }


def main() -> None:
    treino = carregar_split("train")
    validacao = carregar_split("val")

    X_treino, y_treino = separar_x_y(treino)
    X_val, y_val = separar_x_y(validacao)

    candidatos = construir_candidatos(X_treino.columns.tolist())

    resultados = []
    for nome, modelo in candidatos.items():
        modelo.fit(X_treino, y_treino)
        y_pred = modelo.predict(X_val)
        f1_macro = f1_score(y_val, y_pred, average="macro")
        resultados.append((nome, f1_macro))

        print(f"\n{'=' * 60}\n{nome} — F1-macro: {f1_macro:.3f}\n{'=' * 60}")
        print(classification_report(y_val, y_pred, digits=3, zero_division=0))

    print("\nResumo comparativo (F1-macro na validação):")
    for nome, f1_macro in sorted(resultados, key=lambda item: -item[1]):
        print(f"  {nome:<35} {f1_macro:.3f}")


if __name__ == "__main__":
    main()
