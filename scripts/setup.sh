#!/bin/bash

set -e

echo "=============================="
echo "🚀 Updating system packages"
echo "=============================="
sudo apt update && sudo apt upgrade -y

echo "=============================="
echo "📦 Installing required dependencies"
echo "=============================="
sudo apt install -y ca-certificates curl gnupg lsb-release

echo "=============================="
echo "🔑 Adding Docker GPG key"
echo "=============================="
sudo install -m 0755 -d /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo "=============================="
echo "📡 Adding Docker repository"
echo "=============================="
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

echo "=============================="
echo "🐳 Installing Docker Engine + Compose plugin"
echo "=============================="
sudo apt update

sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo "=============================="
echo "🔧 Starting Docker service"
echo "=============================="
sudo systemctl start docker
sudo systemctl enable docker

echo "=============================="
echo "👤 Adding current user to docker group"
echo "=============================="
sudo usermod -aG docker $USER

# Fix socket permissions
sudo chmod 666 /var/run/docker.sock

# Apply group change immediately
newgrp docker

echo "=============================="
echo "✅ Docker Version:"
echo "=============================="
docker --version || true

echo "=============================="
echo "✅ Docker Compose Version:"
echo "=============================="
docker compose version || true




echo "=============================="
echo "🎉 Setup completed!"
echo "👉 IMPORTANT: logout & login again OR run: newgrp docker"
echo "=============================="