# Limpeza e transformação — ExoPredict Cloud

Documenta as decisões de `src/cleaning.py` e `src/transform.py`, que seguem diretamente dos achados de `reports/eda.md` e da seleção de variáveis em `reports/feature_selection.md`.

## Por que limpeza e transformação são dois módulos separados

**Limpeza** (`src/cleaning.py`) contém apenas correções que não dependem de estatística calculada sobre o dataset — são regras fixas, seguras de aplicar antes de qualquer split de treino/teste:

1. Seleciona identificador + alvo + as 103 features sem vazamento (`reports/feature_selection.md`).
2. `koi_depth == 0` → `NaN` (placeholder de dado ausente, não medida real — `reports/eda.md`, bloco 6).
3. `koi_prad > 30` raios terrestres → `NaN` + flag `koi_prad_implausivel` (acima do limite físico plausível mesmo para gigantes gasosos inflados — `reports/eda.md`, blocos 5 e 7).

**Transformação** (`src/transform.py`) contém passos que aprendem algo *dos dados* — imputação por mediana, por exemplo — e por isso não são executados sobre o dataset inteiro aqui. Se a mediana fosse calculada antes do split, o conjunto de teste influenciaria um valor usado para preencher o conjunto de treino: vazamento de informação que infla a métrica de validação de forma irreal. Em vez de gerar um CSV já imputado, `src/transform.py` define um `sklearn.Pipeline`/`ColumnTransformer` reutilizável, que a etapa de split (próxima task do checklist) deve encaixar (`fit`) só com os dados de treino.

## `koi_prad_implausivel`: por que virou flag, não só descarte

Testado diretamente nos dados limpos: a implausibilidade de `koi_prad` não é ruído aleatório, é sinal de classe.

| classe | `koi_prad_implausivel` = 1 | total | % |
|---|---|---|---|
| FALSE POSITIVE | 1.583 | 4.839 | 32,7% |
| CANDIDATE | 56 | 1.978 | 2,8% |
| CONFIRMED | 5 | 2.747 | 0,2% |

Descartar a linha ou zerar o valor sem sinalizar perderia essa informação. Guardar como `NaN` + flag preserva os dois: o valor bruto (fisicamente sem sentido) não entra na escala do modelo, mas o *fato* de ter sido sinalizado como implausível sim.

## Transformação log

Aplicada via `log1p` (tolera zero, preserva `NaN` para a imputação rodar depois) só nas colunas onde a EDA confirmou cauda longa (`reports/eda.md`, bloco 6): `koi_period`, `koi_prad`, `koi_depth`. Não generalizamos para outras colunas fisicamente parecidas sem checar a distribuição de cada uma individualmente.

## Resultado

`data/processed/koi_clean.csv`: 108 colunas (3 identificadores + alvo + 103 features + `koi_prad_implausivel`), 9.564 linhas, nulos remanescentes intencionalmente não imputados. Regenerar com:

```bash
python src/cleaning.py
```

O `ColumnTransformer` de `src/transform.py` foi validado (imputação + log rodando sem erro, sem `NaN` residual) mas ainda não foi encaixado (`fit`) em produção — isso acontece na próxima etapa, ao separar treino/validação/teste.
