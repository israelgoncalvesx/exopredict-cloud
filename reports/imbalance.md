# Tratamento do desbalanceamento — ExoPredict Cloud

Documenta `src/handle_imbalance.py`. A EDA (`reports/eda.md`, bloco 2) já havia apostado que o desbalanceamento (~2,4x entre a maior e a menor classe) era moderado demais para justificar técnicas agressivas como SMOTE, e que `class_weight="balanced"` deveria bastar. Esta task testa essa hipótese empiricamente em vez de aceitá-la sem verificação, usando o Gradient Boosting (vencedor de `reports/model_comparison.md`) como base de comparação.

## Cenários comparados

| cenário | o que faz |
|---|---|
| Sem tratamento | `HistGradientBoostingClassifier` padrão, sem `class_weight` nem resampling — controle |
| `class_weight="balanced"` | reponderação do erro por classe (o que já vínhamos usando nos candidatos) |
| SMOTE | oversampling sintético da(s) classe(s) minoritária(s), aplicado só no fold de treino via `imblearn.pipeline.Pipeline` (nunca na validação/teste — senão a avaliação seria contaminada por exemplos sintéticos derivados de dados que deveriam ser invisíveis ao modelo) |

## Resultado (F1-macro na validação)

| cenário | F1-macro |
|---|---|
| **`class_weight="balanced"`** | **0,925** |
| Sem tratamento | 0,922 |
| SMOTE | 0,918 |

## Leitura

- **Diferença pequena entre os 3 cenários** (0,918–0,925) — confirma a hipótese da EDA: o desbalanceamento aqui é moderado o suficiente para não precisar de intervenção agressiva. Mesmo sem nenhum tratamento, o modelo já ia bem.
- `class_weight="balanced"` é a melhor opção das três, ainda que por margem pequena — decisão mantida como já estava em `reports/model_comparison.md`, agora com evidência em vez de suposição.
- **SMOTE piorou levemente.** Hipótese: os exemplos sintéticos interpolados da classe minoritária (`CANDIDATE`) introduzem ruído na fronteira de decisão sem adicionar sinal físico real — SMOTE cria pontos "entre" exemplos reais no espaço de features, o que pode não corresponder a um KOI fisicamente plausível. Combinado com a árvore já lidando razoavelmente bem com o desbalanceamento moderado, o custo (ruído) superou o benefício.
- Conclusão prática: manter `class_weight="balanced"`, não adotar oversampling.

## Regenerar

```bash
python src/handle_imbalance.py
```
