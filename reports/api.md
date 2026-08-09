# API de previsão — ExoPredict Cloud

Documenta `app/main.py`. Serve o modelo final (`models/gradient_boosting_v1.joblib`, `reports/final_model.md`) via FastAPI.

## Por que o schema é gerado dinamicamente

O modelo espera 104 features numéricas (`models/gradient_boosting_v1.json`, campo `features`). Escrever um schema Pydantic manual com 104 campos seria repetitivo e, pior, ficaria dessincronizado do modelo a cada retreino (uma feature nova exigiria lembrar de editar a API à mão). Em vez disso, `create_model` do Pydantic monta a classe `KOIFeatures` em tempo de execução, lendo a lista de features direto do JSON de metadados salvo por `src/train_final_model.py`. API e modelo compartilham uma única fonte de verdade.

Cada campo é `Optional[float] = None` — `None` vira `NaN` no DataFrame de entrada, e a imputação já embutida no `Pipeline` (`src/transform.py`) cuida do resto. Um cliente pode mandar só as features que tem; o modelo não quebra, só fica menos confiante (testado abaixo).

## Endpoints

| método | rota | o que faz |
|---|---|---|
| GET | `/health` | checagem simples de disponibilidade |
| GET | `/model-info` | versão do modelo, algoritmo, commit git, métrica de teste |
| POST | `/predict` | recebe as features de um KOI, devolve classe prevista + probabilidades por classe |

Documentação interativa automática (Swagger) disponível em `/docs` quando o servidor está rodando.

## Testes manuais realizados

- `/health` e `/model-info` respondendo corretamente.
- `/predict` com um `CONFIRMED` real do conjunto de teste → previu `CONFIRMED` (0,79 de probabilidade), batendo com o rótulo real.
- `/predict` com só 3 das 104 features preenchidas → não quebrou; caiu para uma previsão de menor confiança (esperado — o modelo tem muito menos informação).
- Schema OpenAPI gerado com os 104 campos confirmados via `/openapi.json`.

## Rodar localmente

```bash
uvicorn app.main:app --reload
```

Depois, `http://127.0.0.1:8000/docs` para a documentação interativa.
