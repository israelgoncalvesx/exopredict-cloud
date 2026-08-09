"""API de previsão do ExoPredict Cloud.

O schema de entrada de /predict é gerado dinamicamente a partir de
models/<versao>.json — a mesma lista de features usada para treinar o
modelo. Isso evita que a API e o modelo se dessincronizem: se o modelo for
retreinado com uma feature a mais, a API acompanha sem edição manual.
"""

import json
import sys
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, create_model

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = PROJECT_ROOT / "models"
VERSAO_MODELO = "v1"

# o Pipeline salvo referencia a função de log definida em src/transform.py
sys.path.insert(0, str(PROJECT_ROOT / "src"))

_modelo = joblib.load(MODELS_DIR / f"gradient_boosting_{VERSAO_MODELO}.joblib")
_metadados = json.loads((MODELS_DIR / f"gradient_boosting_{VERSAO_MODELO}.json").read_text())
_features = _metadados["features"]

# cada feature vira um campo opcional float — None é interpretado como NaN e
# tratado pela imputação já embutida no Pipeline (src/transform.py)
KOIFeatures: type[BaseModel] = create_model(
    "KOIFeatures",
    __config__=ConfigDict(extra="ignore"),
    **{nome: (float | None, None) for nome in _features},
)

app = FastAPI(
    title="ExoPredict Cloud API",
    description=(
        "Classifica um KOI (Kepler Object of Interest) como CONFIRMED, CANDIDATE ou FALSE POSITIVE."
    ),
    version=VERSAO_MODELO,
)


class Previsao(BaseModel):
    classe_prevista: str
    probabilidades: dict[str, float]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/model-info")
def model_info() -> dict:
    return {
        "versao": _metadados["versao"],
        "algoritmo": _metadados["algoritmo"],
        "treinado_em": _metadados["treinado_em"],
        "commit_git": _metadados["commit_git"],
        "n_features": len(_features),
        "f1_macro_teste": _metadados["metricas_teste"]["f1_macro"],
    }


@app.post("/predict", response_model=Previsao)
def predict(entrada: KOIFeatures) -> Previsao:
    linha = pd.DataFrame([entrada.model_dump()])[_features]

    classe_prevista = _modelo.predict(linha)[0]
    probabilidades = _modelo.predict_proba(linha)[0]
    classes = _modelo.named_steps["classificador"].classes_

    return Previsao(
        classe_prevista=classe_prevista,
        probabilidades={
            c: round(float(p), 4) for c, p in zip(classes, probabilidades, strict=True)
        },
    )
