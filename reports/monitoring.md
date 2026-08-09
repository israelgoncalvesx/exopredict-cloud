# Monitoramento básico — ExoPredict Cloud

Documenta as duas camadas de monitoramento adicionadas em `app/main.py`: logging estruturado (aplicação) e métricas Prometheus (previsões).

## Logging estruturado

Cada chamada a `/predict` gera uma linha de log em JSON (`log_evento`, em `app/main.py`): timestamp, classe prevista, latência em ms, e quantas das features foram de fato preenchidas (proxy simples de qualidade da entrada — um cliente que manda só 3 das 104 features é visivelmente diferente de um que manda todas).

Formato de uma linha:

```json
{"timestamp": "2026-08-09T17:46:47.796807+00:00", "evento": "predict", "classe_prevista": "FALSE POSITIVE", "latencia_ms": 207.01, "n_features_preenchidas": 3}
```

JSON linha-a-linha (não texto livre) por ser fácil de grepar manualmente e, mais adiante, de ingerir numa ferramenta de log agregado (CloudWatch Logs, por exemplo) sem parsing customizado.

**Ver na EC2:**

```bash
docker compose logs api
```

## Métricas Prometheus (`/metrics`)

Endpoint novo, formato de texto padrão do Prometheus (`prometheus-client`), com dois indicadores:

- `exopredict_predicoes_total{classe_prevista=...}` — contador de previsões, por classe. Serve tanto para volume de uso quanto para **monitorar deriva de distribuição**: se ao longo do tempo a proporção de classes previstas em produção se afastar muito da distribuição do treino (`reports/eda.md`, bloco 2 — 50,6% FALSE POSITIVE / 28,7% CONFIRMED / 20,7% CANDIDATE), é sinal de que os dados de entrada mudaram (data drift) e o modelo pode precisar de retreino.
- `exopredict_predict_latencia_segundos` — histograma de latência do endpoint, para acompanhar degradação de performance.

## Por que não um Prometheus/Grafana completo agora

Seria over-engineering para o porte do projeto — rodar um Prometheus de verdade exigiria outro serviço na infraestrutura, outro container, outra coisa para manter no ar. O endpoint `/metrics` já deixa a porta aberta: qualquer ferramenta de observabilidade (Grafana Cloud tem free tier, ou o próprio CloudWatch da AWS) consegue fazer scrape dele sem precisar tocar no código de novo. "Básico" aqui significa: instrumentado e exposto, não necessariamente com um painel visual rodando.

## Limitação conhecida

As métricas do `/metrics` ficam **em memória** — zeram se o container reiniciar (`docker compose up` de novo, ou a instância EC2 reiniciar). Para métricas persistentes de verdade ao longo do tempo, o próximo passo seria exportar para CloudWatch Metrics ou um Grafana Cloud com scrape periódico e armazenamento próprio.

## Testado

- `test_metrics_reflete_previsoes_feitas` (`tests/test_api.py`): faz uma previsão e confirma que os contadores aparecem em `/metrics`.
- Validado manualmente: `/predict` gera log JSON correto, `/metrics` reflete o contador incrementado e o histograma de latência populado.
- Validado com `requirements-api.txt` isolado (venv limpo, sem o resto das dependências do projeto) — `prometheus-client` já estava listado ali.
