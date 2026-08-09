# Publicação em nuvem — ExoPredict Cloud

Documenta a publicação da API (AWS EC2) e da interface (Streamlit Community Cloud).

## Por que dois provedores diferentes

Mesmo desacoplamento de sempre entre API e interface (`reports/api.md`, `reports/interface.md`, `reports/docker.md`): cada serviço publicado onde faz mais sentido para ele. Streamlit Community Cloud é hospedagem nativa e gratuita para apps Streamlit, com deploy direto do GitHub. AWS EC2 foi escolhido para a API por já ser o provedor de nuvem em uso.

## API na AWS EC2

**O que só pode ser feito pelo Console/CLI da AWS (fora do meu alcance nesta sessão — sem AWS CLI configurado, sem acesso a browser):**

1. Console AWS → EC2 → *Launch instance*.
2. AMI: **Ubuntu Server 22.04 LTS** (ou mais recente).
3. Tipo de instância: `t3.micro` ou `t2.micro` (elegível ao free tier — a API sozinha, com `requirements-api.txt` enxuto, é leve).
4. Par de chaves: crie ou reaproveite um `.pem` para SSH.
5. **Security group**: liberar a porta **22** (SSH, seu IP) e a porta **8000** (API, `0.0.0.0/0` ou restrito, conforme preferir).
6. Lançar a instância e anotar o **IP público**.

**Depois de lançada, via SSH** (isso eu posso te ajudar a rodar, se você me der acesso à instância, ou você mesmo roda):

```bash
ssh -i sua-chave.pem ubuntu@<IP-publico-da-instancia>
curl -fsSL https://raw.githubusercontent.com/israelgoncalvesx/exopredict-cloud/main/deploy/setup_ec2.sh | bash
```

O script (`deploy/setup_ec2.sh`) instala Docker, clona o repositório e sobe só o serviço `api` do `docker-compose.yml` (a interface não roda no EC2 — vai para o Streamlit Cloud) com `restart: unless-stopped`, sobrevivendo a reinícios da instância.

**Verificação:**

```bash
curl http://<IP-publico-da-instancia>:8000/health
```

## Limitação conhecida: sem domínio nem HTTPS

A API fica exposta pelo IP público na porta 8000, sem TLS. Aceitável para portfólio/demo, mas não seria adequado para produção real com dados sensíveis. Evolução natural: Nginx como proxy reverso + Let's Encrypt (Certbot) na frente da porta 8000, com um domínio próprio apontando para o IP da instância (ou um Elastic IP, para o IP não mudar a cada restart).

## Interface no Streamlit Community Cloud

1. [share.streamlit.io](https://share.streamlit.io) → *New app*.
2. Repositório: `israelgoncalvesx/exopredict-cloud`, branch `main`, arquivo principal: `app/interface.py`.
3. **Dependências**: por padrão o Streamlit Cloud instala `requirements.txt` da raiz — como esse é o monolítico do projeto (inclui Jupyter, SHAP etc.), nas *Advanced settings* apontar para `requirements-interface.txt` em vez disso, para um deploy mais leve e rápido.
4. **Secret** `EXOPREDICT_API_URL`, apontando para a API publicada: `http://54.233.91.240:8000`.
5. Deploy — o Streamlit Cloud cuida do resto (build, HTTPS próprio, URL pública `*.streamlit.app`).

## Endereços publicados

- **API**: [http://54.233.91.240:8000](http://54.233.91.240:8000) (Elastic IP, fixo — não muda com reinício da instância). `/health`, `/model-info` e `/predict` testados e funcionando.
- **Interface**: [https://israel-exopredict.streamlit.app](https://israel-exopredict.streamlit.app) — pública, testada de ponta a ponta (carregar exemplo → classificar → resultado exibido corretamente).

## Detalhes que apareceram na prática (não previstos no plano original)

- **Streamlit Community Cloud não tem mais um campo "requirements file" separado** nas Advanced settings (só Python version e Secrets) — a versão atual da plataforma usa uma convenção própria: procura `requirements.txt` na mesma pasta do arquivo principal (`app/interface.py`) antes de olhar a raiz do repo. Resolvido criando `app/requirements.txt` com o mesmo conteúdo de `requirements-interface.txt`.
- **`curl` a partir de um agente/bot recebe redirecionamento para login mesmo em app configurado como público** — a plataforma parece tratar tráfego sem navegador de forma diferente. Testado direto num navegador (inclusive em janela anônima, sem sessão) e funciona normalmente sem pedir login. Não é um problema real, só uma limitação de como validar via linha de comando.
- **Security group da EC2 não libera nenhuma porta customizada por padrão** — precisou adicionar regra de inbound manualmente para a porta 8000 (só a 22/SSH vem liberada por padrão ao criar a instância).
- **IP público de instância EC2 muda a cada parada/reinício** — resolvido associando um Elastic IP antes de configurar o secret da interface, para não quebrar a integração se a instância for reiniciada no futuro.

## Elastic IP (recomendado)

Por padrão, o IP público de uma instância EC2 muda se ela for parada e reiniciada — o que quebraria o secret `EXOPREDICT_API_URL` configurado no Streamlit Cloud. Associar um **Elastic IP** (gratuito enquanto associado a uma instância em execução) evita esse problema.
