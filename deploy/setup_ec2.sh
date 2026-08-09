#!/usr/bin/env bash
# Roda uma vez dentro de uma instância EC2 (Ubuntu) recém-criada, para subir
# só a API (a interface fica no Streamlit Community Cloud, separada).
#
# Uso: ssh na instância, depois:
#   curl -fsSL https://raw.githubusercontent.com/<seu-usuario>/exopredict-cloud/main/deploy/setup_ec2.sh | bash
# ou, com o repo já clonado:
#   bash deploy/setup_ec2.sh
set -euo pipefail

REPO_URL="https://github.com/israelgoncalvesx/exopredict-cloud.git"
REPO_DIR="$HOME/exopredict-cloud"

echo "== Instalando Docker =="
if ! command -v docker &> /dev/null; then
    sudo apt-get update -y
    sudo apt-get install -y ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc
    echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
        $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
        sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update -y
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    sudo usermod -aG docker "$USER"
    echo "Docker instalado. Pode ser necessário reconectar via SSH para o grupo 'docker' valer."
fi

echo "== Clonando/atualizando o repositório =="
if [ -d "$REPO_DIR" ]; then
    git -C "$REPO_DIR" pull
else
    git clone "$REPO_URL" "$REPO_DIR"
fi

echo "== Subindo a API =="
cd "$REPO_DIR"
sudo docker compose up --build -d api

echo "== Pronto =="
echo "Verifique com: curl http://localhost:8000/health"
echo "Acesse de fora com: http://<IP-publico-da-instancia>:8000/health"
