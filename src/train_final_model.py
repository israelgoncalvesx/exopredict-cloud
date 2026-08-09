import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import classification_report, f1_score
from sklearn.pipeline import Pipeline

from baseline_model import carregar_split
from compare_models import separar_x_y
from evaluate_model import ORDEM_CLASSES
from transform import construir_preprocessador

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = PROJECT_ROOT / "models"

VERSAO = "v1"


def construir_modelo_final(colunas_numericas: list[str]) -> Pipeline:
    return Pipeline(
        steps=[
            ("preprocessamento", construir_preprocessador(colunas_numericas)),
            (
                "classificador",
                HistGradientBoostingClassifier(
                    class_weight="balanced", random_state=42
                ),
            ),
        ]
    )


def git_commit_atual() -> str:
    try:
        return (
            subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=PROJECT_ROOT)
            .decode()
            .strip()
        )
    except Exception:
        return "desconhecido"


def main() -> None:
    treino = carregar_split("train")
    validacao = carregar_split("val")
    teste = carregar_split("test")

    # re-treina com treino + validação: a escolha de algoritmo/técnica já
    # está feita (reports/model_comparison.md, reports/imbalance.md), então
    # usamos mais dado para o modelo final. O teste é avaliado uma única vez.
    treino_completo = pd.concat([treino, validacao], ignore_index=True)

    X_treino, y_treino = separar_x_y(treino_completo)
    X_teste, y_teste = separar_x_y(teste)

    modelo = construir_modelo_final(X_treino.columns.tolist())
    modelo.fit(X_treino, y_treino)

    y_pred = modelo.predict(X_teste)
    f1_macro_teste = f1_score(y_teste, y_pred, average="macro")

    print(f"F1-macro no teste (avaliação final, única): {f1_macro_teste:.3f}\n")
    print(classification_report(y_teste, y_pred, labels=ORDEM_CLASSES, digits=3))

    MODELS_DIR.mkdir(exist_ok=True)
    caminho_modelo = MODELS_DIR / f"gradient_boosting_{VERSAO}.joblib"
    joblib.dump(modelo, caminho_modelo)

    metadados = {
        "versao": VERSAO,
        "algoritmo": "HistGradientBoostingClassifier",
        "hiperparametros": {"class_weight": "balanced", "random_state": 42},
        "treinado_em": datetime.now(timezone.utc).isoformat(),
        "commit_git": git_commit_atual(),
        "linhas_treino": len(treino_completo),
        "linhas_teste": len(teste),
        "features": X_treino.columns.tolist(),
        "metricas_teste": {
            "f1_macro": round(f1_macro_teste, 4),
            "classification_report": classification_report(
                y_teste, y_pred, labels=ORDEM_CLASSES, output_dict=True
            ),
        },
    }
    caminho_metadados = MODELS_DIR / f"gradient_boosting_{VERSAO}.json"
    caminho_metadados.write_text(
        json.dumps(metadados, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(f"\nModelo salvo em {caminho_modelo.relative_to(PROJECT_ROOT)}")
    print(f"Metadados salvos em {caminho_metadados.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
