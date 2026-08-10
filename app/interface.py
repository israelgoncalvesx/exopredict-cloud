"""Interface Streamlit do ExoPredict Cloud — consome a API (app/main.py) via HTTP.

Não recarrega o modelo diretamente: interface e API são serviços separados,
o que já prepara o terreno para a etapa de publicação em nuvem (cada um com
sua própria URL).
"""

import os
from pathlib import Path

import pandas as pd
import requests
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_PATH = PROJECT_ROOT / "app" / "sample_koi.csv"
API_URL = os.environ.get("EXOPREDICT_API_URL", "http://127.0.0.1:8000")

# Subconjunto curado a partir de reports/explainability.md: as flags
# automáticas e as features com maior peso real na decisão (koi_max_mult_ev,
# koi_count, koi_model_snr), mais as variáveis físicas mais intuitivas.
# As demais ~90 features ficam None/imputadas — a API já foi testada com
# isso (reports/api.md).
CAMPOS_FORMULARIO = {
    # (rótulo, mínimo, padrão) — sem máximo: variáveis físicas como período e
    # duração têm cauda longa (reports/eda.md, bloco 6); um teto artificial
    # quebraria a interface ao carregar exemplos reais fora do "comum".
    "koi_period": ("Período orbital (dias)", 0.0, 10.0),
    "koi_prad": ("Raio do planeta (raios terrestres)", 0.0, 2.0),
    "koi_depth": ("Profundidade do trânsito (ppm)", 0.0, 500.0),
    "koi_duration": ("Duração do trânsito (horas)", 0.0, 4.0),
    "koi_impact": ("Parâmetro de impacto", 0.0, 0.5),
    "koi_model_snr": ("Relação sinal-ruído do trânsito", 0.0, 20.0),
    "koi_max_mult_ev": ("Estatística de evento múltiplo", 0.0, 30.0),
    "koi_count": ("Nº de planetas conhecidos no sistema", 0, 1),
    "koi_steff": ("Temperatura efetiva da estrela (K)", 0.0, 5700.0),
    "koi_srad": ("Raio da estrela (raios solares)", 0.0, 1.0),
}

CAMPOS_FLAG = {
    "koi_fpflag_nt": "Flag: não parece trânsito",
    "koi_fpflag_ss": "Flag: eclipse estelar",
    "koi_fpflag_co": "Flag: centroide deslocado",
    "koi_fpflag_ec": "Flag: contaminação por efeméride",
}

# Medianas por classe, de reports/eda.md (bloco 7) — referência para a
# explicação em linguagem simples abaixo. Não é um SHAP ao vivo (pesaria
# demais na API enxuta, ver reports/api.md); é uma leitura heurística
# fundamentada nos mesmos achados documentados em reports/explainability.md.
MEDIANA_KOI_PRAD_FALSE_POSITIVE = 8.97
MEDIANA_KOI_PRAD_CONFIRMED_CANDIDATE = 2.0


def gerar_explicacao(entrada: dict, classe_prevista: str) -> list[str]:
    """Poucas frases contextualizando a previsão, com base nas features de
    maior peso real identificadas em reports/explainability.md.

    Cuidado deliberado: a fronteira CONFIRMED/CANDIDATE é a mais difícil do
    modelo (~85% dos erros, reports/evaluation.md) porque as duas classes têm
    perfil físico parecido. Por isso, para essas duas classes o texto descreve
    os valores observados sem soar mais confiante do que o modelo realmente
    é — evita frases que pareçam contradizer a própria previsão quando o
    modelo erra exatamente nessa fronteira.
    """
    pontos = []

    flags_ativas = [rotulo for nome, rotulo in CAMPOS_FLAG.items() if entrada.get(nome) == 1]
    if flags_ativas:
        pontos.append(
            f"🚩 {len(flags_ativas)} flag(s) automática(s) ativada(s) ({', '.join(flags_ativas)}) "
            "— é o sinal mais forte que o modelo usa para identificar FALSE POSITIVE "
            "(reports/explainability.md)."
        )

    raio = entrada.get("koi_prad")
    if raio is not None and raio > MEDIANA_KOI_PRAD_FALSE_POSITIVE * 0.7:
        pontos.append(
            f"🪐 Raio do planeta estimado em {raio:.2f} raios terrestres — próximo da mediana "
            f"típica de FALSE POSITIVE (~{MEDIANA_KOI_PRAD_FALSE_POSITIVE:.1f} R⊕), bem acima da "
            f"mediana de CONFIRMED/CANDIDATE (~{MEDIANA_KOI_PRAD_CONFIRMED_CANDIDATE:.1f} R⊕) "
            "— reports/eda.md, bloco 7."
        )

    if classe_prevista == "FALSE POSITIVE" and not pontos:
        pontos.append(
            "Nenhuma flag automática ativada e raio dentro do esperado — outras variáveis "
            "físicas do trânsito pesaram para FALSE POSITIVE."
        )

    snr = entrada.get("koi_model_snr")
    evento_multiplo = entrada.get("koi_max_mult_ev")
    fronteira_dificil = classe_prevista in ("CONFIRMED", "CANDIDATE")
    if fronteira_dificil and snr is not None and evento_multiplo is not None:
        pontos.append(
            f"📶 Sinal-ruído ({snr:.1f}) e estatística de evento múltiplo ({evento_multiplo:.1f}) "
            "são as variáveis que mais pesam nessa fronteira específica "
            "(reports/explainability.md), mas CONFIRMED e CANDIDATE têm perfil físico "
            "parecido — é onde o modelo mais erra (reports/evaluation.md)."
        )

    n_planetas = entrada.get("koi_count")
    if fronteira_dificil and n_planetas is not None and n_planetas > 1:
        pontos.append(
            f"🌌 O sistema já tem {int(n_planetas)} planeta(s) conhecido(s) — sistemas "
            "multi-planetários costumam ter seus candidatos confirmados com mais frequência, "
            "um dos fatores que o modelo considera nessa fronteira."
        )

    if not pontos:
        pontos.append(
            "Não há um fator isolado dominante nos campos preenchidos — a previsão combina "
            "várias variáveis com peso menor cada uma."
        )

    return pontos


@st.cache_data
def carregar_amostras() -> pd.DataFrame:
    return pd.read_csv(SAMPLE_PATH)


def montar_formulario(valores_iniciais: dict) -> dict:
    entrada = {}
    col1, col2 = st.columns(2)
    campos = list(CAMPOS_FORMULARIO.items())
    metade = len(campos) // 2

    for coluna, itens in zip((col1, col2), (campos[:metade], campos[metade:]), strict=True):
        with coluna:
            for nome_coluna, (rotulo, minimo, padrao) in itens:
                valor_inicial = valores_iniciais.get(nome_coluna, padrao)
                if isinstance(padrao, int):
                    entrada[nome_coluna] = st.number_input(
                        rotulo,
                        min_value=int(minimo),
                        value=int(valor_inicial) if pd.notna(valor_inicial) else padrao,
                    )
                else:
                    entrada[nome_coluna] = st.number_input(
                        rotulo,
                        min_value=float(minimo),
                        value=float(valor_inicial) if pd.notna(valor_inicial) else padrao,
                    )

    st.markdown("**Flags automáticas de falso positivo** (0 = não, 1 = sim)")
    cols_flags = st.columns(4)
    for coluna, (nome_coluna, rotulo) in zip(cols_flags, CAMPOS_FLAG.items(), strict=True):
        with coluna:
            valor_inicial = valores_iniciais.get(nome_coluna, 0)
            entrada[nome_coluna] = st.selectbox(
                rotulo,
                options=[0, 1],
                index=int(valor_inicial) if pd.notna(valor_inicial) else 0,
            )

    return entrada


def main() -> None:
    st.set_page_config(page_title="ExoPredict Cloud", page_icon="🪐")
    st.title("🪐 ExoPredict Cloud")
    st.caption(
        "Classifica um KOI (Kepler Object of Interest) como CONFIRMED, "
        "CANDIDATE ou FALSE POSITIVE, a partir das características do trânsito."
    )

    amostras = carregar_amostras()
    st.subheader("1. Preencha os dados ou carregue um exemplo real")

    if "valores_iniciais" not in st.session_state:
        st.session_state.valores_iniciais = {}

    if st.button("🎲 Carregar exemplo aleatório do conjunto de teste"):
        exemplo = amostras.sample(1).iloc[0]
        st.session_state.valores_iniciais = exemplo.to_dict()
        st.session_state.classe_real = exemplo["koi_disposition"]
        st.session_state.nome_exemplo = exemplo["kepoi_name"]

    if "nome_exemplo" in st.session_state:
        st.info(f"Exemplo carregado: **{st.session_state.nome_exemplo}**")

    entrada = montar_formulario(st.session_state.valores_iniciais)

    st.subheader("2. Previsão")
    if st.button("Classificar", type="primary"):
        try:
            resposta = requests.post(f"{API_URL}/predict", json=entrada, timeout=10)
            resposta.raise_for_status()
        except requests.exceptions.RequestException as erro:
            st.error(
                f"Não foi possível falar com a API em {API_URL}. "
                f"Ela está rodando? (`uvicorn app.main:app --reload`)\n\nDetalhe: {erro}"
            )
            return

        resultado = resposta.json()
        st.success(f"Classe prevista: **{resultado['classe_prevista']}**")

        if "classe_real" in st.session_state:
            classe_real = st.session_state.classe_real
            if classe_real == resultado["classe_prevista"]:
                st.caption(f"✅ Classe real do exemplo: **{classe_real}** — o modelo acertou.")
            else:
                st.caption(f"❌ Classe real do exemplo: **{classe_real}** — o modelo errou.")

        probs = pd.Series(resultado["probabilidades"], name="probabilidade").sort_values()
        st.bar_chart(probs)

        st.markdown("**Por que essa previsão?**")
        for ponto in gerar_explicacao(entrada, resultado["classe_prevista"]):
            st.markdown(f"- {ponto}")
        st.caption(
            "Leitura simplificada, baseada nos achados de reports/explainability.md "
            "e reports/eda.md do repositório — não é uma explicação SHAP em tempo real."
        )


if __name__ == "__main__":
    main()
