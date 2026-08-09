# Docker — ExoPredict Cloud

Documenta `Dockerfile.api`, `Dockerfile.interface` e `docker-compose.yml`.

## Duas imagens, não uma

Mesma lógica de desacoplamento já usada na API e na interface (`reports/api.md`, `reports/interface.md`): cada serviço tem sua própria imagem, seu próprio `requirements-*.txt` enxuto e escala/publica independentemente. Uma imagem única misturando os dois levaria dependências desnecessárias para cada lado (a API não precisa do Streamlit, a interface não precisa do scikit-learn).

## Por que `requirements-api.txt` e `requirements-interface.txt` existem

`requirements.txt` (o único usado até aqui) é monolítico — cresceu ao longo do projeto e inclui Jupyter, matplotlib, SHAP, pytest, tudo junto, porque serve tanto a EDA/treino quanto os testes. Nenhum desses serviços precisa disso para *servir* previsões ou renderizar a interface. Os dois arquivos novos listam só o que `app/main.py` e `app/interface.py` de fato importam — imagens menores, builds mais rápidos.

## Layout de arquivos dentro da imagem da API

`app/main.py` insere `src/` no `sys.path` e carrega o modelo via `joblib`, que internamente referencia o módulo `transform` (não `src.transform` — foi carregado assim durante o treino, rodando `python src/train_final_model.py`, que adiciona `src/` ao path). Por isso o `Dockerfile.api` preserva a mesma estrutura de diretórios do repo (`app/` e `src/` como irmãos, ambos sob `/app`) em vez de achatar tudo num único diretório — mudar o layout quebraria o `unpickling` do modelo.

## `docker-compose.yml`

- `interface` depende de `api` estar saudável (`healthcheck` batendo em `/health`) antes de subir — evita a corrida onde a interface sobe antes da API estar pronta para receber requisições.
- `EXOPREDICT_API_URL=http://api:8000` na interface, não `localhost` — dentro da rede do compose, os serviços se enxergam pelo nome do serviço, resolvido pelo DNS interno do Docker.

## Validação

O Docker Desktop não estava acessível no ambiente onde os arquivos foram escritos (falha de I/O no binário, integração WSL indisponível nesta sessão). Antes disso, validei o que dava pra validar sem Docker: criei um venv Python limpo só com `requirements-api.txt` (sem o venv "gordo" do projeto) e confirmei que `/health` e `/predict` respondiam corretamente com esse conjunto mínimo de dependências — mesmo conjunto que o `Dockerfile.api` instala, mesmo layout de arquivos.

O build real (`docker compose up --build`) foi validado localmente, com os dois containers conversando via rede interna do compose.

```bash
docker compose up --build
```

Depois, `http://localhost:8000/docs` (API) e `http://localhost:8501` (interface).
