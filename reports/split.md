# Split treino/validação/teste — ExoPredict Cloud

Documenta `src/split.py`, que consome `data/processed/koi_clean.csv` (saída de `src/cleaning.py`).

## Por que estratificado

A EDA (`reports/eda.md`, bloco 2) mostrou desbalanceamento moderado entre as classes (50,6% / 28,7% / 20,7%). Um split puramente aleatório poderia, por acaso, concentrar uma classe a mais no teste e a menos no treino — distorcendo tanto o aprendizado quanto a confiabilidade da avaliação. `train_test_split(..., stratify=df["koi_disposition"])` preserva a proporção original em cada partição.

## Por que duas chamadas de `train_test_split`

A função do scikit-learn só divide em duas partes. Para 3 partições, aplicamos em cascata: primeiro separamos o teste (15%) do restante, depois separamos a validação (15% do total original, recalculado como proporção do que sobrou) do treino. `random_state=42` fixo em ambas as chamadas garante que o split é reproduzível.

## Proporção

70% treino / 15% validação / 15% teste — padrão razoável para ~9.500 linhas, dá ~1.400 linhas por split de avaliação (suficiente para métricas estáveis nas 3 classes).

## Resultado

| split | linhas | % | FALSE POSITIVE | CONFIRMED | CANDIDATE |
|---|---|---|---|---|---|
| original | 9.564 | 100% | 50,6% | 28,7% | 20,7% |
| treino | 6.694 | 70,0% | 50,6% | 28,7% | 20,7% |
| validação | 1.435 | 15,0% | 50,6% | 28,7% | 20,7% |
| teste | 1.435 | 15,0% | 50,6% | 28,7% | 20,7% |

Estratificação preservou a proporção original em todos os splits.

## Por que a transformação (log + imputação) não roda aqui

`src/transform.py` define o `ColumnTransformer` mas não é chamado neste script. A transformação será embutida dentro do `Pipeline` do modelo na etapa de "criar modelo baseline" — pré-processamento e estimador como uma unidade só, encaixados (`fit`) exclusivamente com `train.csv`. Isso evita dois riscos: vazar estatística do teste/validação para o treino, e ter uma transformação "solta" que poderia divergir entre o treino do modelo e o momento de gerar previsões novas.

## Regenerar

```bash
python src/split.py
```

Gera `data/processed/{train,val,test}.csv` (não versionados — regeneráveis a partir de `data/raw/`, mesmo princípio de `koi_clean.csv`).
