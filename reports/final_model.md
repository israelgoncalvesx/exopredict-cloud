# Modelo final — ExoPredict Cloud

Documenta `src/train_final_model.py`. Primeira e única vez em que o conjunto de teste é usado — todas as etapas anteriores (comparação de modelos, tratamento de desbalanceamento, avaliação por classe) usaram treino/validação, mantendo o teste intocado para uma estimativa final sem viés de seleção.

## Decisões

- **Algoritmo**: Gradient Boosting (`HistGradientBoostingClassifier`, `class_weight="balanced"`) — vencedor de `reports/model_comparison.md`, confirmado em `reports/imbalance.md`.
- **Re-treino em treino + validação**: como a escolha de algoritmo e técnica de desbalanceamento já estava definida antes desta etapa, o modelo final é treinado com `train.csv` + `val.csv` combinados (mais dado disponível), e avaliado **uma única vez** em `test.csv`. Depois deste número, o teste não pode mais informar nenhuma decisão — senão vira validação disfarçada e a estimativa deixa de ser honesta.
- **Versionamento**: `joblib.dump` do `Pipeline` inteiro (pré-processamento + classificador como uma unidade só, elimina o risco de usar o modelo com uma transformação diferente da que ele foi treinado) + um JSON de metadados irmão, com hiperparâmetros, hash do commit git, timestamp, lista de features e métricas — rastreabilidade sem depender de uma ferramenta externa de model registry, adequado ao porte do projeto.

## Resultado no teste (avaliação final)

| classe | precisão | recall | F1 | suporte |
|---|---|---|---|---|
| CONFIRMED | 0,906 | 0,891 | 0,898 | 412 |
| CANDIDATE | 0,847 | 0,859 | 0,853 | 297 |
| FALSE POSITIVE | 0,993 | 0,997 | 0,995 | 726 |

**F1-macro no teste: 0,915** (vs. 0,925 na validação, `reports/model_comparison.md`) — queda pequena e esperada, consistente com um modelo que generaliza bem, sem sinal de overfitting nas escolhas feitas ao longo do projeto.

## Artefatos gerados

- `models/gradient_boosting_v1.joblib` (1,2 MB) — pipeline completo, pronto para `predict()` em dados novos com o mesmo schema de `reports/feature_selection.md`.
- `models/gradient_boosting_v1.json` — metadados: hiperparâmetros, commit git, timestamp, features usadas, métricas completas do teste.

## Regenerar

```bash
python src/train_final_model.py
```
