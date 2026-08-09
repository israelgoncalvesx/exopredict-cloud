from pathlib import Path

import pandas as pd
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as PipelineImb
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import classification_report, f1_score
from sklearn.pipeline import Pipeline

from baseline_model import carregar_split
from compare_models import separar_x_y
from transform import construir_preprocessador

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def construir_cenarios(colunas_numericas: list[str]) -> dict[str, Pipeline]:
    preprocessador = lambda: construir_preprocessador(colunas_numericas)  # noqa: E731

    return {
        "Sem tratamento": Pipeline(
            steps=[
                ("preprocessamento", preprocessador()),
                ("classificador", HistGradientBoostingClassifier(random_state=42)),
            ]
        ),
        "class_weight=balanced": Pipeline(
            steps=[
                ("preprocessamento", preprocessador()),
                (
                    "classificador",
                    HistGradientBoostingClassifier(
                        class_weight="balanced", random_state=42
                    ),
                ),
            ]
        ),
        "SMOTE (oversampling)": PipelineImb(
            steps=[
                ("preprocessamento", preprocessador()),
                ("smote", SMOTE(random_state=42)),
                ("classificador", HistGradientBoostingClassifier(random_state=42)),
            ]
        ),
    }


def main() -> None:
    treino = carregar_split("train")
    validacao = carregar_split("val")

    X_treino, y_treino = separar_x_y(treino)
    X_val, y_val = separar_x_y(validacao)

    cenarios = construir_cenarios(X_treino.columns.tolist())

    resultados = []
    for nome, modelo in cenarios.items():
        modelo.fit(X_treino, y_treino)
        y_pred = modelo.predict(X_val)
        f1_macro = f1_score(y_val, y_pred, average="macro")
        resultados.append((nome, f1_macro))

        print(f"\n{'=' * 60}\n{nome} — F1-macro: {f1_macro:.3f}\n{'=' * 60}")
        print(classification_report(y_val, y_pred, digits=3, zero_division=0))

    print("\nResumo comparativo (F1-macro na validação):")
    for nome, f1_macro in sorted(resultados, key=lambda item: -item[1]):
        print(f"  {nome:<25} {f1_macro:.3f}")


if __name__ == "__main__":
    main()
