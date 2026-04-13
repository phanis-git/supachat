# 🚀 SupaChat — Conversational Analytics Platform

SupaChat is a full-stack conversational analytics application built on top of **Supabase PostgreSQL + MCP server**, enabling users to query data using natural language and visualize insights through tables and charts.

This project demonstrates a complete **DevOps lifecycle**:
**Build → Dockerize → Deploy → Reverse Proxy → CI/CD → Monitoring → DevOps Agent**

---

# 📌 Live Demo

🌐 Public URL: `http://34.230.85.14`
📊 Prometheus: `http://34.230.85.14:9090`
📈 Grafana: `http://34.230.85.14:3002`
🤖 DevOps Agent: `http://34.230.85.14:8001/docs`

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

### DevOps Agent
- FastAPI
- Anthropic Claude API (AI-powered)
- Docker SDK (container management)
- Watchdog (auto-healing)

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
✅ Tabular results display
✅ Bar chart visualization (Recharts)
✅ Loading & error handling
✅ Health check endpoint (`/health`)
✅ Prometheus metrics (`/metrics`)
✅ Auto-healing watchdog (DevOps Agent)
✅ AI-powered log analysis
✅ CI/CD auto-deployment via GitHub Actions

---

# 🧠 Example Queries

- `trending` → Show top topics by total views
- `ai` → Show all AI articles
- `devops` → Show all DevOps articles

---

## 🗄️ Database Schema

Supabase PostgreSQL with `articles` table:

| Column | Type | Description |
|--------|------|-------------|
| id | int4 | Primary key |
| title | text | Article title |
| topic | text | Category (AI, DevOps, etc.) |
| views | int4 | View count |
| likes | int4 | Like count |
| created_at | timestamp | Creation date |

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
ANTHROPIC_API_KEY=ANTHROPIC_API_KEY
```

---

## 3. Run with Docker

```bash
docker-compose up --build
```

Access:

| Service | URL |
|---------|-----|
| App | http://localhost |
| Backend API | http://localhost/api/query |
| DevOps Agent | http://localhost:8001/docs |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3002 |

---

# 🐳 Docker Setup

## Services

* frontend
* backend
* prometheus
* grafana

| Service | Image | Port |
|---------|-------|------|
| frontend | custom build | 80 (internal) |
| backend | custom build | 8000 (internal) |
| nginx | nginx:alpine | 80 (public) |
| devops-agent | custom build | 8001 (public) |
| prometheus | prom/prometheus | 9090 (public) |
| grafana | grafana/grafana | 3002 (public) |

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

    location /api/ {
        proxy_pass http://backend:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        proxy_pass http://frontend:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    location /agent/ {
    proxy_pass http://devops-agent:8001/agent/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
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

---

# 🤖 DevOps Agent (Bonus Implemented)

A lightweight AI-powered DevOps assistant built as a microservice.

## Capabilities

✅ Restart containers  
✅ Summarize failed logs  
✅ Explain CI/CD failures  
✅ Health diagnostics  
✅ Deployment debugging  

---

# ⚠️ Known Limitations

* Loki (logging) not implemented
* MCP logic simplified

---

# 🚀 Future Improvements

* Add Loki for centralized logging

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
