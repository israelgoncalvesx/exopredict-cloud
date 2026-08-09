# ExoPredict Cloud

O **ExoPredict Cloud** será uma aplicação de ciência de dados e machine learning para analisar objetos de interesse do telescópio Kepler e estimar se um registro representa um exoplaneta confirmado, um candidato ou um falso positivo.

O projeto pretende percorrer o fluxo completo de um produto de dados: ingestão e validação dos dados, análise exploratória, preparação das variáveis, treinamento e avaliação de modelos, disponibilização das previsões por API e publicação de uma interface em nuvem.

## Estado atual

A base inicial do projeto usa o catálogo Kepler Objects of Interest (KOI). O CSV já foi carregado em um banco SQLite local e pode ser inspecionado pelos scripts disponíveis em `src/`.

- 9.564 registros carregados;
- 141 colunas na tabela `koi_raw`;
- classes encontradas: `CONFIRMED`, `CANDIDATE` e `FALSE POSITIVE`;
- consultas iniciais para conferir estrutura, amostras, distribuição das classes e média do `koi_score`.

A análise exploratória completa está em [`notebooks/01_eda.ipynb`](notebooks/01_eda.ipynb); os achados, conclusões e o resumo executivo estão documentados em [`reports/eda.md`](reports/eda.md). A classificação das 141 colunas e a lista de features sem vazamento de alvo estão em [`reports/feature_selection.md`](reports/feature_selection.md). As decisões de limpeza e transformação (e por que imputação é adiada para depois do split) estão em [`reports/cleaning.md`](reports/cleaning.md). O split treino/validação/teste está documentado em [`reports/split.md`](reports/split.md).

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

- [ ] Criar um modelo baseline
- [ ] Treinar e comparar modelos candidatos
- [ ] Tratar o desbalanceamento entre as classes
- [ ] Avaliar métricas por classe e matriz de confusão
- [ ] Selecionar, versionar e salvar o melhor modelo
- [ ] Adicionar explicabilidade das previsões

### Produto e nuvem

- [ ] Criar uma API de previsão
- [ ] Criar uma interface para consulta e visualização
- [ ] Adicionar testes automatizados
- [ ] Configurar lint, formatação e integração contínua
- [ ] Criar imagens Docker
- [ ] Publicar aplicação, API e modelo em nuvem
- [ ] Adicionar monitoramento básico da aplicação e das previsões

## Objetivo final

Entregar uma aplicação reproduzível e acessível pela web que demonstre, de ponta a ponta, como dados astronômicos podem ser preparados e utilizados em um sistema de classificação com machine learning.

## Uso de inteligência artificial

Este é um projeto pessoal construído com o auxílio de ferramentas de inteligência artificial, utilizadas como apoio no planejamento, na pesquisa, na documentação, na revisão e no desenvolvimento de código. Esse suporte é combinado com minhas próprias decisões técnicas, análises e avaliações. A definição dos objetivos, a validação das soluções e a responsabilidade pelos resultados permanecem sob minha autoria.
