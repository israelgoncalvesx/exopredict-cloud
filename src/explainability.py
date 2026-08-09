from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
from sklearn.inspection import permutation_importance

from baseline_model import carregar_split
from compare_models import separar_x_y

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODELO_PATH = PROJECT_ROOT / "models" / "gradient_boosting_v1.joblib"
IMAGES_DIR = PROJECT_ROOT / "reports" / "images"

N_TOP_FEATURES = 15


def importancia_global(modelo, X_teste: pd.DataFrame, y_teste: pd.Series) -> pd.Series:
    """Permutation importance: embaralha cada coluna e mede quanto o F1-macro piora.

    Model-agnostic — funciona sobre o Pipeline inteiro (pré-processamento
    incluso), não só sobre o classificador.
    """
    resultado = permutation_importance(
        modelo, X_teste, y_teste,
        scoring="f1_macro", n_repeats=10, random_state=42, n_jobs=-1,
    )
    return pd.Series(resultado.importances_mean, index=X_teste.columns).sort_values(ascending=False)


def plotar_importancia_global(importancias: pd.Series) -> None:
    top = importancias.head(N_TOP_FEATURES).sort_values()
    fig, ax = plt.subplots(figsize=(8, 6))
    top.plot.barh(ax=ax)
    ax.set_title(f"Top {N_TOP_FEATURES} features — permutation importance (F1-macro)")
    ax.set_xlabel("Queda média no F1-macro ao embaralhar a coluna")
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "feature_importance_global.png", dpi=120)
    plt.close(fig)


def preparar_shap(modelo, X: pd.DataFrame) -> tuple[shap.TreeExplainer, np.ndarray, list[str]]:
    """SHAP precisa do classificador isolado + dados já transformados (pós pré-processamento)."""
    preprocessador = modelo.named_steps["preprocessamento"]
    classificador = modelo.named_steps["classificador"]

    X_transformado = preprocessador.transform(X)
    nomes_features = preprocessador.get_feature_names_out()

    explainer = shap.TreeExplainer(classificador)
    return explainer, X_transformado, list(nomes_features)


def plotar_shap_summary(explainer, X_transformado, nomes_features, classes) -> None:
    shap_values = explainer.shap_values(X_transformado)

    for i, classe in enumerate(classes):
        fig = plt.figure(figsize=(8, 6))
        shap.summary_plot(
            shap_values[:, :, i], X_transformado, feature_names=nomes_features,
            show=False, max_display=15,
        )
        plt.title(f"SHAP — impacto das features na previsão de {classe}")
        plt.tight_layout()
        nome_arquivo = f"shap_summary_{classe.lower().replace(' ', '_')}.png"
        plt.savefig(IMAGES_DIR / nome_arquivo, dpi=120)
        plt.close(fig)


def explicar_caso(explainer, X_transformado, nomes_features, classes, indice: int, classe_alvo: str) -> None:
    idx_classe = classes.index(classe_alvo)
    shap_values = explainer.shap_values(X_transformado[indice : indice + 1])

    explicacao = shap.Explanation(
        values=shap_values[0, :, idx_classe],
        base_values=explainer.expected_value[idx_classe],
        data=X_transformado[indice],
        feature_names=nomes_features,
    )
    fig = plt.figure(figsize=(8, 6))
    shap.plots.waterfall(explicacao, max_display=12, show=False)
    plt.title(f"Por que o modelo pesou '{classe_alvo}' neste caso")
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "shap_waterfall_caso_erro.png", dpi=120)
    plt.close(fig)


def main() -> None:
    modelo = joblib.load(MODELO_PATH)
    teste = carregar_split("test")
    X_teste, y_teste = separar_x_y(teste)

    print("Calculando importância global (permutation importance)...")
    importancias = importancia_global(modelo, X_teste, y_teste)
    print(importancias.head(N_TOP_FEATURES))
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    plotar_importancia_global(importancias)

    print("\nCalculando explicações SHAP...")
    explainer, X_transformado, nomes_features = preparar_shap(modelo, X_teste)
    classes = list(modelo.named_steps["classificador"].classes_)
    plotar_shap_summary(explainer, X_transformado, nomes_features, classes)

    y_pred = modelo.predict(X_teste)
    erros = teste.reset_index(drop=True)[
        (y_teste.reset_index(drop=True) == "CONFIRMED") & (pd.Series(y_pred) == "CANDIDATE")
    ]
    if len(erros) > 0:
        indice_erro = erros.index[0]
        print(f"\nExplicando caso de erro (CONFIRMED previsto como CANDIDATE), índice {indice_erro}...")
        explicar_caso(explainer, X_transformado, nomes_features, classes, indice_erro, "CANDIDATE")

    print(f"\nImagens salvas em {IMAGES_DIR.relative_to(PROJECT_ROOT)}/")


if __name__ == "__main__":
    main()
