# FROM python:3.11-slim
# WORKDIR /app
# RUN apt-get update && apt-get install -y \
#     curl \
#     docker.io \
#     && rm -rf /var/lib/apt/lists/*
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# COPY . .
# EXPOSE 8001
# CMD ["uvicorn", "agent:app", "--host", "0.0.0.0", "--port", "8001"]



FROM python:3.11-slim

WORKDIR /app

# Install Docker CLI + Compose v2 plugin
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    gnupg \
    lsb-release \
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
    && echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
    bookworm stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null \
    && apt-get update \
    && apt-get install -y docker-ce-cli docker-compose-plugin \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["uvicorn", "agent:app", "--host", "0.0.0.0", "--port", "8001"]