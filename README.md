# 🚀 SupaChat — Conversational Analytics Platform

SupaChat is a full-stack conversational analytics application built on top of **Supabase PostgreSQL + MCP server**, enabling users to query data using natural language and visualize insights through tables and charts.

This project demonstrates a complete **DevOps lifecycle**:
**Build → Dockerize → Deploy → Reverse Proxy → CI/CD → Monitoring**

---

# 📌 Live Demo

🌐 Public URL: `http://98.90.200.120:3000`

---

# 🏗️ Architecture

```
User → Nginx → Frontend (React) → Backend (FastAPI)
                               ↓
                         MCP Server
                               ↓
                     Supabase PostgreSQL

Monitoring Stack:
Prometheus → Grafana
```

---

# ⚙️ Tech Stack

## Frontend

* React / Vite
* Recharts (data visualization)
* Axios
* Chat UI

## Backend

* FastAPI
* MCP Query Translator
* Supabase PostgreSQL (via psycopg2)

## Infrastructure

* Docker & Docker Compose
* AWS EC2
* Nginx (Reverse Proxy)

## CI/CD

* GitHub Actions

## Monitoring

* Prometheus
* Grafana

---

# ✨ Features

✅ Natural language → SQL query conversion
✅ Chatbot-style UI
✅ Query history
✅ Tabular results
✅ Graph visualization (Recharts)
✅ Loading & error handling
✅ Health check endpoint (`/health`)

---

# 🧠 Example Queries

* “Show top trending topics in last 30 days”
* “Compare article engagement by topic”
* “Plot daily views trend for AI articles”

---

# 🖥️ Local Setup

## 1. Clone Repo

```bash
git clone https://github.com/phanis-git/supachat.git
cd supachat
```

## 2. Environment Variables

Create `.env` file:

```env
DB_HOST=your-supabase-host
DB_NAME=postgres
DB_USER=your-user
DB_PASSWORD=your-password
DB_PORT=6543
```

---

## 3. Run with Docker

```bash
docker-compose up --build
```

Access:

* Frontend → http://localhost:3000
* Backend → http://localhost:8000

---

# 🐳 Docker Setup

## Services

* frontend
* backend
* prometheus
* grafana

### Features

* Environment variables
* Health checks
* CPU/memory limits

---

# ☁️ Deployment (AWS EC2)

## Steps

1. Launch EC2 (Ubuntu)
2. Install Docker & Docker Compose
3. Clone repository
4. Run:

```bash
docker-compose up -d --build
```

5. Open ports:

* 80 (HTTP)
* 3000 / 5173 (optional)
* 9090 (Prometheus)
* 3001 (Grafana)

---

# 🌐 Nginx Reverse Proxy

## Routing

* `/` → Frontend
* `/query` → Backend

## Sample Config

```nginx
server {
    listen 80;

    location / {
        proxy_pass http://frontend:5173;
    }

    location /api {
        proxy_pass http://backend:8000;
    }
}
```

## Enabled Features

* Gzip compression
* Basic caching
* Reverse proxy routing

---

# 🔁 CI/CD Pipeline (GitHub Actions)

## Workflow

1. Code push to GitHub
2. Build Docker images
3. SSH into EC2
4. Pull latest code
5. Restart containers

## Sample Steps

```yaml
- name: Build Docker Images
  run: docker-compose build

- name: Deploy to EC2
  run: ssh ubuntu@<ec2-ip> "cd supachat && docker-compose up -d --build"
```

---

# 📊 Monitoring

## Prometheus

* Collects metrics:

  * CPU usage
  * Memory usage
  * Container health
  * Request latency

## Grafana

* Dashboards:

  * System metrics
  * App performance
  * API response time

Access:

* Prometheus → `http://98.90.200.120:9090`
* Grafana → `http://98.90.200.120:3001`

---

# ❤️ Health Check

```bash
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

---

# 🤖 AI Tools Used

* ChatGPT (architecture, debugging)
* Cursor / Claude (optionally used)
* AI used for:

  * SQL generation
  * Log debugging
  * DevOps automation guidance

---

# ⚠️ Known Limitations

* Loki (logging) not implemented
* DevOps agent not implemented (bonus)
* MCP logic simplified

---

# 🚀 Future Improvements

* Add Loki for centralized logging
* Build DevOps AI Agent
* Improve NLP → SQL accuracy
* Add authentication (Supabase Auth)

---

# 👨‍💻 Author

**Siva Phani Kumar**
DevOps & Fullstack Developer

---

# ⭐ Conclusion

This project demonstrates:

* Full-stack development
* Cloud deployment
* CI/CD automation
* Production-ready DevOps practices

---
