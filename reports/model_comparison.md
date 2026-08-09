# Comparação de modelos candidatos — ExoPredict Cloud

Documenta `src/compare_models.py`, treinado em `train.csv` e avaliado em `val.csv` (teste ainda intocado).

## Mudança na base antes de comparar

O baseline (`reports/baseline_model.md`) excluiu `koi_quarters` (única feature de texto) por falta de tempo de escopo. Antes de comparar modelos, resolvido: `koi_quarters` é uma string binária (1 quarter observado / 0 não observado) com **170 valores únicos no treino** — cardinalidade alta demais para one-hot. Em vez disso, `src/cleaning.py` ganhou `engenheirar_koi_num_quarters`, que conta os `'1'`s da string — uma grandeza física legítima (quantos quarters do Kepler observaram aquele alvo) e numérica. A coluna original é mantida no dataset, mas os scripts de modelagem usam `koi_num_quarters` no lugar dela.

Com essa mudança, o dataset limpo passou de 108 para 109 colunas, e o baseline foi re-executado para efeito de comparação justa (F1-macro passou de 0,882 para 0,881 — variação desprezível, dentro do ruído).

## Candidatos

| modelo | por que entrou na comparação |
|---|---|
| Regressão logística | referência já estabelecida (`reports/baseline_model.md`) |
| Random Forest (`n_estimators=300`, `class_weight="balanced"`) | ensemble de árvores, captura não-linearidade e interação entre variáveis sem engenharia manual |
| Gradient Boosting (`HistGradientBoostingClassifier`, `class_weight="balanced"`) | boosting costuma superar random forest em dados tabulares; implementação em histograma é rápida mesmo com ~9,5k linhas |

Todos os 3 usam o mesmo `ColumnTransformer` (imputação + log + padronização) de `src/transform.py`, para manter a comparação nas mesmas features — mesmo sabendo que árvores não precisam de padronização e o `HistGradientBoostingClassifier` aceita `NaN` nativamente. Escolha deliberada: isolar o efeito do algoritmo, não do pré-processamento. Vale revisitar mais adiante se compensa um pipeline de pré-processamento mais leve para os modelos de árvore.

## Resultado (F1-macro na validação)

| modelo | F1-macro | acurácia |
|---|---|---|
| Regressão logística | 0,881 | 0,905 |
| Random Forest | 0,910 | 0,932 |
| **Gradient Boosting** | **0,925** | **0,944** |

Por classe (Gradient Boosting, o melhor):

| classe | precisão | recall | F1 |
|---|---|---|---|
| CANDIDATE | 0,874 | 0,862 | 0,868 |
| CONFIRMED | 0,907 | 0,927 | 0,917 |
| FALSE POSITIVE | 0,994 | 0,988 | 0,991 |

## Leitura

- Os dois modelos de árvore superam a regressão logística — esperado, já que capturam relações não-lineares e interações entre variáveis (ex.: combinações de `koi_prad` × `koi_impact` que a EDA mostrou correlacionadas, bloco 8) sem precisar que a gente as construa manualmente.
- O ganho maior está exatamente onde o baseline errava mais: `CANDIDATE` ↔ `CONFIRMED` (F1 de `CANDIDATE` sobe de 0,811 para 0,868; `CONFIRMED` de 0,862 para 0,917). `FALSE POSITIVE` já estava quase saturado no baseline (F1 0,973) e segue quase saturado (0,991) — pouco espaço para melhorar ali.
- Gradient Boosting > Random Forest por margem pequena (0,925 vs. 0,910) — ambos são candidatos razoáveis; Gradient Boosting vai para a etapa seguinte (desbalanceamento e ajuste fino) como modelo principal.

## Regenerar

```bash
python src/compare_models.py
```
