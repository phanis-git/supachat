
# 2

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
import subprocess
import anthropic
from groq import Groq
import os
import threading
import time
from dotenv import load_dotenv

load_dotenv()

# =========================
# HELPER FUNCTIONS
# =========================

def run_command(cmd: str) -> str:
    try:
        result = subprocess.run(
            cmd, shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.stdout + result.stderr
    except Exception as e:
        return f"Error running command: {str(e)}"
    
# Here we use anthropic ai which is cost .. so we can try free ai tool 

# def ask_ai(system: str, prompt: str) -> str:
#     try:
#         client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
#         response = client.messages.create(
#             model="claude-opus-4-5",
#             max_tokens=1024,
#             messages=[{"role": "user", "content": f"System context: {system}\n\nQuestion: {prompt}"}]
#         )
#         return response.content[0].text
#     except Exception as e:
#         return f"AI Error: {str(e)}"



# Here i use grokai for free

def ask_ai(system: str, prompt: str) -> str:
    """Ask Groq AI a question — FREE!"""
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        response = client.chat.completions.create(
            # model="llama3-8b-8192",   # free model
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Error: {str(e)}"

# =========================
# WATCHDOG
# =========================

CRITICAL_CONTAINERS = {
    "supachat-frontend-1": "frontend",
    "supachat-backend-1": "backend",
    "supachat-nginx-1": "nginx"
}

COMPOSE_PATH = "/home/ubuntu/supachat"

def check_container(container_name: str) -> bool:
    result = run_command(
        f"docker inspect -f '{{{{.State.Running}}}}' {container_name} 2>&1"
    )
    return "true" in result

def watchdog():
    print("🐕 Watchdog started — monitoring containers...")
    while True:
        for container_name, service_name in CRITICAL_CONTAINERS.items():
            try:
                is_running = check_container(container_name)
                if not is_running:
                    print(f"🚨 {container_name} is DOWN! Recreating...")
                    result = run_command(
                        f"cd {COMPOSE_PATH} && docker compose up -d --no-deps {service_name}"
                    )
                    print(f"✅ Recreate result: {result}")
                else:
                    print(f"✅ {container_name} is healthy")
            except Exception as e:
                print(f"❌ Watchdog error: {e}")
        time.sleep(15)

# =========================
# LIFESPAN — starts watchdog
# =========================

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting DevOps Agent...")
    thread = threading.Thread(target=watchdog, daemon=True)
    thread.start()
    print("🐕 Watchdog thread started!")
    yield
    print("🛑 Shutting down...")

# =========================
# APP
# =========================

app = FastAPI(title="SupaChat DevOps Agent", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# REQUEST MODELS
# =========================

class CommandRequest(BaseModel):
    command: str

class LogRequest(BaseModel):
    container: str
    lines: int = 50

class DiagnoseRequest(BaseModel):
    issue: str

class ChatRequest(BaseModel):
    message: str

# =========================
# HEALTH CHECK
# =========================

@app.get("/health")
def health():
    return {"status": "ok", "service": "devops-agent"}

# =========================
# 1. CONTAINER STATUS
# =========================

# @app.get("/agent/status")
# def get_status():
#     output = run_command("docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'")
#     summary = ask_ai(
#         "You are a DevOps assistant. Analyze Docker container status.",
#         f"Docker ps output:\n{output}\n\nGive a brief health summary. List any containers that are down."
#     )
#     return {"raw_output": output, "ai_summary": summary}

# Clean & understandable output

@app.get("/agent/status")
def get_status():
    output = run_command("docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'")
    
    summary = ask_ai(
        "You are a DevOps assistant. Be concise and use emojis.",
        f"""Docker container status:
{output}

Reply in this exact format:
Total Containers: X
✅ Running: list them
❌ Down: list them or 'None'
⚠️  Action needed: yes/no and what
Overall Health: Healthy/Unhealthy"""
    )
    
    return {
        "status": output,
        "summary": summary
    }

# =========================
# 2. CONTAINER LOGS
# =========================

@app.get("/agent/logs/{container_name}")
def get_logs(container_name: str, lines: int = 50):
    output = run_command(f"docker logs {container_name} --tail {lines} 2>&1")
    summary = ask_ai(
        "You are a DevOps assistant. Analyze Docker logs.",
        f"Logs from {container_name}:\n{output}\n\nSummarize. Highlight errors."
    )
    return {"container": container_name, "raw_logs": output, "ai_summary": summary}

# =========================
# 3. RESTART CONTAINER
# =========================

@app.post("/agent/restart/{container_name}")
def restart_container(container_name: str):
    output = run_command(f"docker restart {container_name}")
    status = run_command(f"docker ps --filter name={container_name} --format '{{{{.Status}}}}'")
    summary = ask_ai(
        "You are a DevOps assistant.",
        f"Container {container_name} restarted. Result: {output}. Status: {status}. Was it successful?"
    )
    return {"container": container_name, "restart_output": output, "current_status": status, "ai_summary": summary}

# =========================
# 4. DIAGNOSE ISSUE
# =========================

@app.post("/agent/diagnose")
def diagnose(req: DiagnoseRequest):
    containers = run_command("docker ps -a --format '{{.Names}}: {{.Status}}'")
    disk = run_command("df -h /")
    memory = run_command("free -h")
    diagnosis = ask_ai(
        f"You are a DevOps engineer. Containers: {containers} Disk: {disk} Memory: {memory}",
        f"Issue: {req.issue}\n\nProvide diagnosis and step-by-step solution."
    )
    return {
        "issue": req.issue,
        "system_context": {"containers": containers, "disk": disk, "memory": memory},
        "ai_diagnosis": diagnosis
    }

# =========================
# 5. ERROR LOGS
# =========================

@app.get("/agent/errors/{container_name}")
def get_errors(container_name: str):
    output = run_command(f"docker logs {container_name} 2>&1 | grep -i 'error\\|exception\\|failed\\|critical' | tail -20")
    if not output.strip():
        return {"container": container_name, "errors_found": False, "message": "No errors found! ✅"}
    explanation = ask_ai(
        "You are a DevOps expert.",
        f"Errors in {container_name}:\n{output}\n\nExplain each error and provide fixes."
    )
    return {"container": container_name, "errors_found": True, "raw_errors": output, "ai_explanation": explanation}

# =========================
# 6. DEPLOY
# =========================

@app.post("/agent/deploy")
def deploy():
    results = {}
    results["git_pull"] = run_command(f"cd {COMPOSE_PATH} && git fetch origin && git reset --hard origin/main")
    results["compose_down"] = run_command(f"cd {COMPOSE_PATH} && docker compose down")
    results["compose_up"] = run_command(f"cd {COMPOSE_PATH} && docker compose up -d --build 2>&1")
    results["final_status"] = run_command("docker ps --format 'table {{.Names}}\t{{.Status}}'")
    summary = ask_ai(
        "You are a DevOps assistant.",
        f"Deployment results:\n{results}\n\nWas deployment successful? Any issues?"
    )
    return {"deployment_steps": results, "ai_summary": summary}

# =========================
# 7. FULL DIAGNOSTIC
# =========================

@app.get("/agent/diagnostic")
def full_diagnostic():
    diagnostic = {}
    diagnostic["containers"] = run_command("docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'")
    diagnostic["disk_usage"] = run_command("df -h /")
    diagnostic["memory_usage"] = run_command("free -h")
    diagnostic["cpu_usage"] = run_command("top -bn1 | grep 'Cpu(s)'")
    diagnostic["backend_health"] = run_command("curl -s http://localhost:8000/health")
    diagnostic["nginx_status"] = run_command("docker logs supachat-nginx-1 --tail 5 2>&1")
    diagnostic["backend_errors"] = run_command("docker logs supachat-backend-1 2>&1 | grep -i error | tail -5")
    analysis = ask_ai(
        "You are a senior DevOps engineer.",
        f"System diagnostic:\n{diagnostic}\n\nFull health report. Rate 1-10. List issues and actions."
    )
    return {"diagnostic_data": diagnostic, "ai_health_report": analysis}

# =========================
# 8. CHAT
# =========================

@app.post("/agent/chat")
def chat_with_agent(req: ChatRequest):
    containers = run_command("docker ps -a --format '{{.Names}}: {{.Status}}'")
    response = ask_ai(
        f"You are a DevOps agent for SupaChat. Containers: {containers}. Help with issues, fixes, logs, best practices.",
        req.message
    )
    return {"user_message": req.message, "agent_response": response}

# =========================
# 9. WATCHDOG STATUS
# =========================

@app.get("/agent/watchdog")
def watchdog_status():
    statuses = {}
    for container_name, service_name in CRITICAL_CONTAINERS.items():
        is_running = check_container(container_name)
        statuses[container_name] = {
            "status": "✅ Running" if is_running else "❌ Down",
            "service": service_name,
            "auto_heal": "enabled"
        }
    return {
        "watchdog": "active",
        "check_interval": "15 seconds",
        "monitored": statuses
    }