# Interface de consulta e visualização — ExoPredict Cloud

Documenta `app/interface.py` (Streamlit), que consome `app/main.py` (API) via HTTP.

## Decisões

- **Streamlit**, não HTML/JS: padrão para demos de ML em Python puro, rápido de construir e manter para um portfólio de ciência de dados.
- **Consome a API via HTTP, não recarrega o modelo**: interface e API como serviços desacoplados, preparando o terreno para a publicação em nuvem (`app/main.py`, `reports/api.md`), onde cada um terá sua própria URL. A URL da API é configurável via variável de ambiente (`EXOPREDICT_API_URL`), com `http://127.0.0.1:8000` como padrão local.
- **Formulário curado, não as 104 features**: usa o subconjunto de maior peso real identificado em `reports/explainability.md` (as 4 flags automáticas, `koi_max_mult_ev`, `koi_count`, `koi_model_snr`) mais as variáveis físicas mais intuitivas para quem não é astrônomo (período, raio, profundidade, duração, temperatura estelar). As ~90 features restantes ficam `None`/imputadas pela API — já testado que isso não quebra a previsão (`reports/api.md`).
- **`app/sample_koi.csv`** (18 KOIs reais do conjunto de teste, 6 de cada classe) para o botão "carregar exemplo aleatório" — permite testar a interface sem o usuário ter dados KOI à mão. Diferente de `data/processed/*.csv` (regenerável, gitignorado), este é um fixture pequeno específico da demo, versionado no repo.

## Bug encontrado e corrigido durante o teste

Testar de verdade (não só ler o código) importa: os campos numéricos do formulário tinham `max_value` fixo (ex.: `koi_duration` até 20h). Ao carregar um exemplo real do conjunto de teste com duração de 36,8h — valor real, coerente com a cauda longa que a EDA já havia identificado em `reports/eda.md` (bloco 6) — a interface quebrava com `StreamlitValueAboveMaxError`. Corrigido removendo os tetos artificiais (mantido só `min_value=0`, fisicamente sensato); o modelo já lida com qualquer valor via o pipeline de transformação.

## Como foi testado (sem browser disponível neste ambiente)

- `streamlit.testing.v1.AppTest`: simula cliques reais nos botões da interface (não só leitura de código), com a API rodando de verdade por trás.
- 15 rodadas de "carregar exemplo aleatório" → "classificar", cobrindo as 3 classes, sem nenhuma exceção após a correção do bug de `max_value`.
- Confirmado que o app FastAPI continua funcionando após instalar Streamlit, apesar do `starlette` ter sido rebaixado de versão pela resolução de dependências.

## Rodar localmente

Em dois terminais:

```bash
uvicorn app.main:app --reload
```

```bash
streamlit run app/interface.py
```

## Regenerar `app/sample_koi.csv`

```python
import pandas as pd
df = pd.read_csv("data/processed/test.csv")
partes = [g.sample(6, random_state=42) for _, g in df.groupby("koi_disposition")]
pd.concat(partes).sample(frac=1, random_state=42).to_csv("app/sample_koi.csv", index=False)
```
