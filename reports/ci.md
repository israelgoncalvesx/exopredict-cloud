# Lint, formatação e CI — ExoPredict Cloud

Documenta `pyproject.toml` (config do `ruff`) e `.github/workflows/ci.yml`.

## Por que ruff

`.ruff_cache/` já estava no `.gitignore` desde o início do projeto — a ferramenta já era a intenção. `ruff` substitui a combinação flake8 + black + isort + pyupgrade num único binário (escrito em Rust, ordens de magnitude mais rápido), com um único arquivo de configuração.

## Regras habilitadas

`E`/`F` (pycodestyle/pyflakes — erros e estilo básico), `I` (organização de imports), `UP` (sintaxe moderna — ex.: `float | None` em vez de `Optional[float]`, `datetime.UTC` em vez de `timezone.utc`), `B` (flake8-bugbear — erros sutis, ex.: `zip()` sem `strict=`, que mascara listas de tamanhos diferentes).

## O que apareceu ao rodar pela primeira vez

26 problemas no código já escrito ao longo do projeto — nada grave, mas reais:

- 6 blocos de import desorganizados, 2 imports não usados (`ruff --fix` corrigiu sozinho)
- 5 usos de `zip()` sem `strict=True` (em `app/interface.py`, `app/main.py` e no notebook de EDA) — sem isso, se duas listas tiverem tamanhos diferentes por engano, `zip` trunca silenciosamente em vez de avisar
- 1 uso de `typing.Optional` em vez da sintaxe moderna `X | None` (`app/main.py`)
- 11 linhas acima de 100 caracteres, principalmente docstrings e f-strings

Todos corrigidos manualmente (os não cobertos por `--fix`) antes de configurar o CI — não faz sentido ligar uma verificação automática que já nasce falhando.

## CI (GitHub Actions)

`.github/workflows/ci.yml` roda em todo push/PR para `main`: instala `requirements.txt`, roda `ruff check`, `ruff format --check` e `pytest`. Usa o `requirements.txt` único do projeto (não um arquivo de CI separado) — mantém uma única fonte de verdade de dependências, ao custo de um install um pouco mais lento (inclui Jupyter, SHAP etc., que a CI não usa diretamente, mas que os testes exercitam indiretamente via `data/raw/kepler_koi.csv` e `models/gradient_boosting_v1.joblib`, ambos versionados no repo).

## Rodar localmente (o mesmo que o CI roda)

```bash
ruff check .
ruff format --check .
pytest
```
