from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.pipeline import Pipeline

from baseline_model import carregar_split
from compare_models import separar_x_y
from transform import construir_preprocessador

PROJECT_ROOT = Path(__file__).resolve().parents[1]
IMAGEM_PATH = PROJECT_ROOT / "reports" / "images" / "confusion_matrix.png"

# Ordem escolhida por gravidade científica do erro, não alfabética: da
# classe mais "assentada" (CONFIRMED) até a mais distante (FALSE POSITIVE) —
# ver reports/evaluation.md para a discussão de por que a ordem importa aqui.
ORDEM_CLASSES = ["CONFIRMED", "CANDIDATE", "FALSE POSITIVE"]


def construir_modelo_final(colunas_numericas: list[str]) -> Pipeline:
    return Pipeline(
        steps=[
            ("preprocessamento", construir_preprocessador(colunas_numericas)),
            (
                "classificador",
                HistGradientBoostingClassifier(class_weight="balanced", random_state=42),
            ),
        ]
    )


def plotar_matrizes_confusao(cm, cm_normalizada) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=ORDEM_CLASSES,
        yticklabels=ORDEM_CLASSES,
        ax=axes[0],
    )
    axes[0].set_title("Matriz de confusão (contagem)")
    axes[0].set_xlabel("Previsto")
    axes[0].set_ylabel("Real")

    sns.heatmap(
        cm_normalizada,
        annot=True,
        fmt=".2f",
        cmap="Blues",
        xticklabels=ORDEM_CLASSES,
        yticklabels=ORDEM_CLASSES,
        ax=axes[1],
    )
    axes[1].set_title("Matriz de confusão (normalizada por classe real = recall)")
    axes[1].set_xlabel("Previsto")
    axes[1].set_ylabel("Real")

    plt.tight_layout()
    IMAGEM_PATH.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(IMAGEM_PATH, dpi=120)


def main() -> None:
    treino = carregar_split("train")
    validacao = carregar_split("val")

    X_treino, y_treino = separar_x_y(treino)
    X_val, y_val = separar_x_y(validacao)

    modelo = construir_modelo_final(X_treino.columns.tolist())
    modelo.fit(X_treino, y_treino)
    y_pred = modelo.predict(X_val)

    print(classification_report(y_val, y_pred, labels=ORDEM_CLASSES, digits=3))

    cm = confusion_matrix(y_val, y_pred, labels=ORDEM_CLASSES)
    cm_normalizada = confusion_matrix(y_val, y_pred, labels=ORDEM_CLASSES, normalize="true")

    print("Matriz de confusão (contagem):")
    print(pd.DataFrame(cm, index=ORDEM_CLASSES, columns=ORDEM_CLASSES))
    print("\nMatriz de confusão (normalizada por classe real):")
    print(pd.DataFrame(cm_normalizada, index=ORDEM_CLASSES, columns=ORDEM_CLASSES).round(3))

    idx_fp, idx_confirmed = ORDEM_CLASSES.index("FALSE POSITIVE"), ORDEM_CLASSES.index("CONFIRMED")
    falso_positivo_para_confirmed = cm[idx_fp, idx_confirmed]
    confirmed_para_falso_positivo = cm[idx_confirmed, idx_fp]
    print(
        f"\nErros graves — FALSE POSITIVE previsto como CONFIRMED: "
        f"{falso_positivo_para_confirmed}; CONFIRMED previsto como FALSE POSITIVE: "
        f"{confirmed_para_falso_positivo}"
    )

    plotar_matrizes_confusao(cm, cm_normalizada)
    print(f"\nImagem salva em {IMAGEM_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
