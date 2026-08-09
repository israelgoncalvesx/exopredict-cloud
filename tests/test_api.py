import json
from pathlib import Path

import pandas as pd
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

FEATURES_MODELO = json.loads(
    (Path(__file__).resolve().parents[1] / "models" / "gradient_boosting_v1.json").read_text()
)["features"]


def test_health():
    resposta = client.get("/health")
    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok"}


def test_model_info():
    resposta = client.get("/model-info")
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["algoritmo"] == "HistGradientBoostingClassifier"
    assert corpo["n_features"] > 0


def test_predict_com_exemplo_real_do_teste(splits):
    _, _, teste = splits
    linha_confirmada = teste[teste["koi_disposition"] == "CONFIRMED"].iloc[0]

    payload = {
        f: (None if pd.isna(linha_confirmada[f]) else float(linha_confirmada[f]))
        for f in FEATURES_MODELO
    }

    resposta = client.post("/predict", json=payload)
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["classe_prevista"] in {"CONFIRMED", "CANDIDATE", "FALSE POSITIVE"}
    assert abs(sum(corpo["probabilidades"].values()) - 1.0) < 1e-3


def test_predict_com_dados_parciais_nao_quebra():
    resposta = client.post("/predict", json={"koi_period": 10.5, "koi_prad": 2.1, "koi_depth": 450})
    assert resposta.status_code == 200
    assert resposta.json()["classe_prevista"] in {"CONFIRMED", "CANDIDATE", "FALSE POSITIVE"}


def test_predict_sem_nenhum_dado_nao_quebra():
    resposta = client.post("/predict", json={})
    assert resposta.status_code == 200


def test_metrics_reflete_previsoes_feitas():
    client.post("/predict", json={"koi_period": 10.5, "koi_prad": 2.1, "koi_depth": 450})

    resposta = client.get("/metrics")
    assert resposta.status_code == 200
    assert "exopredict_predicoes_total" in resposta.text
    assert "exopredict_predict_latencia_segundos" in resposta.text
