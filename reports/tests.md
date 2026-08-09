# Testes automatizados — ExoPredict Cloud

Documenta a suíte em `tests/`, formalizando com `pytest` boa parte do que vinha sendo validado manualmente ao longo do projeto.

## Estrutura

`tests/conftest.py` define fixtures de sessão (`df_bruto`, `df_limpo`, `splits`) que rodam a limpeza e o split reais uma única vez por execução da suíte — os testes usam o mesmo `data/raw/kepler_koi.csv` versionado no repo, sem fixtures sintéticas artificiais.

| arquivo | cobre |
|---|---|
| `test_define_feature_columns.py` | a classificação das 141 colunas não tem sobreposição nem esquece nenhuma; vazamento e colunas vazias nunca entram como feature |
| `test_cleaning.py` | `koi_depth == 0` → `NaN`; `koi_prad` implausível → `NaN` + flag; `koi_quarters` → contagem correta; dados limpos sem vazamento residual |
| `test_split.py` | treino/validação/teste não se sobrepõem, somam o total, e a estratificação preserva a proporção de classes (tolerância de 2 pontos percentuais) |
| `test_transform.py` | o `ColumnTransformer` não deixa `NaN` residual e preserva o número de colunas |
| `test_api.py` | `/health`, `/model-info`, `/predict` com dados completos, parciais e vazios — via `TestClient` do FastAPI, sem precisar de servidor rodando |
| `test_interface.py` | fluxo completo "carregar exemplo → classificar" via `AppTest`, 10 repetições (o exemplo é aleatório) — regressão do bug de `max_value` encontrado em `reports/interface.md` |

## Por que `test_interface.py` precisa de um servidor de verdade

Diferente de `test_api.py` (que usa `TestClient`, chamando a aplicação em memória, sem rede), a interface faz uma chamada HTTP real (`requests.post`) para a API. Mockar essa chamada esconderia justamente o tipo de bug que apareceu no teste manual (incompatibilidade entre o dado real devolvido pela API e os limites do formulário). Por isso, um fixture (`api_no_ar`, `scope="module"`) sobe `uvicorn` como subprocesso antes dos testes de interface e derruba depois — mais lento, mas testa o caminho real.

## Rodar

```bash
pytest
```

29 testes, ~20s (a maior parte do tempo é o fixture de API subindo o servidor para os testes de interface).
