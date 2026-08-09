"""Testa app/interface.py de ponta a ponta com AppTest, simulando cliques reais.

Cobre principalmente a regressão do bug encontrado ao testar manualmente
(reports/interface.md): max_value fixo nos campos numéricos quebrava com
exemplos reais de cauda longa (ex.: koi_duration de 36,8h). Roda várias
vezes porque o exemplo carregado é aleatório — um único run poderia não
pegar um valor extremo.
"""

import subprocess
import time
from pathlib import Path

import httpx
import pytest
from streamlit.testing.v1 import AppTest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INTERFACE_PATH = PROJECT_ROOT / "app" / "interface.py"


@pytest.fixture(scope="module", autouse=True)
def api_no_ar():
    """Sobe a API real como subprocesso — a interface chama via HTTP de verdade, não mock."""
    processo = subprocess.Popen(
        ["uvicorn", "app.main:app", "--port", "8000"],
        cwd=PROJECT_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        for _ in range(30):
            try:
                if httpx.get("http://127.0.0.1:8000/health", timeout=1).status_code == 200:
                    break
            except httpx.ConnectError:
                pass
            time.sleep(0.5)
        else:
            processo.terminate()
            pytest.skip("API não subiu a tempo para os testes de interface")

        yield
    finally:
        processo.terminate()
        processo.wait(timeout=5)


@pytest.mark.parametrize("execucao", range(10))
def test_carregar_exemplo_e_classificar_nao_quebra(execucao):
    at = AppTest.from_file(str(INTERFACE_PATH), default_timeout=30)
    at.run()
    assert not at.exception

    at.button[0].click().run()  # "Carregar exemplo aleatório"
    assert not at.exception

    botao_classificar = next(b for b in at.button if b.label == "Classificar")
    botao_classificar.click().run()

    assert not at.exception
    assert len(at.success) == 1
    classes = ("CONFIRMED", "CANDIDATE", "FALSE POSITIVE")
    assert any(classe in at.success[0].value for classe in classes)
