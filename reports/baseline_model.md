# Modelo baseline — ExoPredict Cloud

Documenta `src/baseline_model.py`, treinado em `train.csv` e avaliado em `val.csv` (o teste fica intocado até a escolha final do modelo).

## Decisões

- **Algoritmo**: regressão logística multiclasse (`class_weight="balanced"`, dado o desbalanceamento moderado já quantificado em `reports/eda.md`, bloco 2). Baseline padrão da área — rápido, interpretável, referência justa para comparar contra modelos mais complexos na próxima etapa.
- **Métrica de referência**: comparado contra um `DummyClassifier` (sempre prevê a classe majoritária). Necessário porque, com 50,6% de `FALSE POSITIVE`, um modelo "burro" já acerta ~50% de acurácia só chutando sempre a mesma classe — acurácia isolada engana em problema desbalanceado. Por isso o resumo usa **F1-macro** (peso igual às 3 classes) e o relatório por classe, não só acurácia.
- **`koi_quarters` excluída**: única feature de texto entre as 103 selecionadas em `reports/feature_selection.md`; precisa de codificação categórica específica, fora do escopo do baseline (fica para "treinar e comparar modelos candidatos").
- **Padronização adicionada ao pipeline** (`src/transform.py`): a primeira rodada sem `StandardScaler` não convergiu (features em escalas muito diferentes — dias, Kelvin, magnitudes, raios terrestres). Adicionado `StandardScaler` após a imputação/log em ambos os ramos do `ColumnTransformer` — não é um ajuste cosmético, é o que resolveu a não-convergência.

## Resultado

| modelo | F1-macro | acurácia |
|---|---|---|
| Dummy (classe majoritária) | 0,224 | 0,506 |
| Baseline (regressão logística) | **0,882** | 0,905 |

Por classe (baseline):

| classe | precisão | recall | F1 |
|---|---|---|---|
| CANDIDATE | 0,757 | 0,872 | 0,811 |
| CONFIRMED | 0,875 | 0,850 | 0,862 |
| FALSE POSITIVE | 0,996 | 0,950 | 0,973 |

Matriz de confusão:

|  | previsto CANDIDATE | previsto CONFIRMED | previsto FALSE POSITIVE |
|---|---|---|---|
| real CANDIDATE | 259 | 36 | 2 |
| real CONFIRMED | 61 | 350 | 1 |
| real FALSE POSITIVE | 22 | 14 | 690 |

## Leitura

- **`FALSE POSITIVE` já sai quase perfeito** (99,6% precisão, 95% recall) — coerente com `reports/eda.md` (blocos 5–7): `koi_prad`, `koi_depth` e as flags automáticas de falso positivo separam bem essa classe.
- **A confusão principal é `CANDIDATE` ↔ `CONFIRMED`** (61 + 36 dos 97 erros totais). Faz sentido fisicamente: um "candidato" é um possível planeta ainda não confirmado — as duas classes tendem a ter perfil físico parecido, a diferença muitas vezes está em confirmação observacional adicional que não está nas variáveis físicas do trânsito.
- Já supera o dummy por uma margem grande (0,882 vs. 0,224 de F1-macro) — confirma que as features selecionadas carregam sinal real, não é preciso um modelo muito mais sofisticado só para "funcionar".

## Regenerar

```bash
python src/baseline_model.py
```
