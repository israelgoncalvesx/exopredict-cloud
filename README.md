# ExoPredict Cloud

O **ExoPredict Cloud** será uma aplicação de ciência de dados e machine learning para analisar objetos de interesse do telescópio Kepler e estimar se um registro representa um exoplaneta confirmado, um candidato ou um falso positivo.

O projeto pretende percorrer o fluxo completo de um produto de dados: ingestão e validação dos dados, análise exploratória, preparação das variáveis, treinamento e avaliação de modelos, disponibilização das previsões por API e publicação de uma interface em nuvem.

## Estado atual

A base inicial do projeto usa o catálogo Kepler Objects of Interest (KOI). O CSV já foi carregado em um banco SQLite local e pode ser inspecionado pelos scripts disponíveis em `src/`.

- 9.564 registros carregados;
- 141 colunas na tabela `koi_raw`;
- classes encontradas: `CONFIRMED`, `CANDIDATE` e `FALSE POSITIVE`;
- consultas iniciais para conferir estrutura, amostras, distribuição das classes e média do `koi_score`.

A análise exploratória completa está em [`notebooks/01_eda.ipynb`](notebooks/01_eda.ipynb); os achados, conclusões e o resumo executivo estão documentados em [`reports/eda.md`](reports/eda.md). A classificação das 141 colunas e a lista de features sem vazamento de alvo estão em [`reports/feature_selection.md`](reports/feature_selection.md). As decisões de limpeza e transformação (e por que imputação é adiada para depois do split) estão em [`reports/cleaning.md`](reports/cleaning.md). O split treino/validação/teste está documentado em [`reports/split.md`](reports/split.md). O modelo baseline (regressão logística, F1-macro 0,881 na validação) está documentado em [`reports/baseline_model.md`](reports/baseline_model.md). A comparação de modelos candidatos (Gradient Boosting venceu, F1-macro 0,925) está em [`reports/model_comparison.md`](reports/model_comparison.md). A comparação de estratégias de desbalanceamento (confirma `class_weight="balanced"` como suficiente) está em [`reports/imbalance.md`](reports/imbalance.md). A avaliação por classe e matriz de confusão (os erros mais graves são quase inexistentes) está em [`reports/evaluation.md`](reports/evaluation.md). O modelo final (F1-macro 0,915 no teste) está versionado em `models/` e documentado em [`reports/final_model.md`](reports/final_model.md). A análise de explicabilidade (importância global e SHAP por classe) está em [`reports/explainability.md`](reports/explainability.md). A API de previsão (FastAPI, schema gerado dinamicamente a partir do modelo) está documentada em [`reports/api.md`](reports/api.md). A interface Streamlit (com o bug de validação que apareceu ao testar de verdade, e a correção) está documentada em [`reports/interface.md`](reports/interface.md). A suíte de testes automatizados (29 testes) está documentada em [`reports/tests.md`](reports/tests.md). Lint, formatação e CI (GitHub Actions) estão documentados em [`reports/ci.md`](reports/ci.md).

## Estrutura planejada

```text
exopredict-cloud/
├── app/          # aplicação e interface
├── data/         # dados brutos e processados
├── database/     # banco SQLite local
├── models/       # modelos treinados e artefatos
├── notebooks/    # exploração e experimentos reproduzíveis
├── reports/      # gráficos e resultados
├── sql/          # consultas e transformações SQL
└── src/          # scripts do pipeline de dados e ML
```

## Como executar o estágio atual

Requer Python 3. Depois de clonar o repositório:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Para recriar a tabela `koi_raw` a partir do CSV:

```bash
python src/load_to_database.py
```

Para inspecionar o banco e executar as consultas exploratórias:

```bash
python src/inspect_database.py
```

Para gerar/atualizar o dicionário de dados (`data/DICTIONARY.md`):

```bash
python src/generate_data_dictionary.py
```

Para validar a qualidade dos dados brutos:

```bash
python src/validate_data_quality.py
```

Para classificar as colunas e gerar a lista de variáveis utilizáveis sem vazamento de alvo (`reports/feature_selection.md`):

```bash
python src/define_feature_columns.py
```

Para limpar os dados e gerar `data/processed/koi_clean.csv`:

```bash
python src/cleaning.py
```

Para gerar os splits de treino, validação e teste:

```bash
python src/split.py
```

Para treinar e avaliar o modelo baseline:

```bash
python src/baseline_model.py
```

Para treinar e comparar os modelos candidatos:

```bash
python src/compare_models.py
```

Para comparar estratégias de tratamento do desbalanceamento:

```bash
python src/handle_imbalance.py
```

Para a avaliação consolidada por classe e matriz de confusão:

```bash
python src/evaluate_model.py
```

Para treinar e salvar o modelo final (única vez que o teste é usado):

```bash
python src/train_final_model.py
```

Para gerar a análise de explicabilidade (importância global + SHAP):

```bash
python src/explainability.py
```

Para rodar a API de previsão localmente:

```bash
uvicorn app.main:app --reload
```

Depois, acesse `http://127.0.0.1:8000/docs` para a documentação interativa.

Para rodar a interface (com a API acima já no ar):

```bash
streamlit run app/interface.py
```

Para rodar a suíte de testes automatizados:

```bash
pytest
```

Para lint e formatação:

```bash
ruff check .
ruff format .
```

## Tasks

### Fundação e dados

- [x] Criar a estrutura inicial de diretórios
- [x] Adicionar o catálogo KOI bruto
- [x] Criar o script de ingestão do CSV
- [x] Carregar os dados na tabela `koi_raw` do SQLite
- [x] Conferir esquema, amostras e distribuição inicial das classes
- [x] Documentar a origem, a licença e o dicionário dos dados
- [x] Criar validações automáticas de qualidade dos dados

### Análise e preparação

- [x] Realizar análise exploratória completa
- [x] Investigar valores ausentes, duplicados e outliers
- [x] Definir as variáveis que poderão ser usadas sem vazamento de alvo
- [x] Construir o pipeline de limpeza e transformação
- [x] Separar dados de treino, validação e teste

### Machine learning

- [x] Criar um modelo baseline
- [x] Treinar e comparar modelos candidatos
- [x] Tratar o desbalanceamento entre as classes
- [x] Avaliar métricas por classe e matriz de confusão
- [x] Selecionar, versionar e salvar o melhor modelo
- [x] Adicionar explicabilidade das previsões

### Produto e nuvem

- [x] Criar uma API de previsão
- [x] Criar uma interface para consulta e visualização
- [x] Adicionar testes automatizados
- [x] Configurar lint, formatação e integração contínua
- [ ] Criar imagens Docker
- [ ] Publicar aplicação, API e modelo em nuvem
- [ ] Adicionar monitoramento básico da aplicação e das previsões

## Objetivo final

Entregar uma aplicação reproduzível e acessível pela web que demonstre, de ponta a ponta, como dados astronômicos podem ser preparados e utilizados em um sistema de classificação com machine learning.

## Uso de inteligência artificial

Este é um projeto pessoal construído com o auxílio de ferramentas de inteligência artificial, utilizadas como apoio no planejamento, na pesquisa, na documentação, na revisão e no desenvolvimento de código. Esse suporte é combinado com minhas próprias decisões técnicas, análises e avaliações. A definição dos objetivos, a validação das soluções e a responsabilidade pelos resultados permanecem sob minha autoria.
