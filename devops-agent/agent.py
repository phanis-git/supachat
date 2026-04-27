
# # 1

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from contextlib import asynccontextmanager
# from pydantic import BaseModel
# import subprocess

# from groq import Groq
# import os
# import threading
# import time
# from dotenv import load_dotenv

# load_dotenv()

# # =========================
# # HELPER FUNCTIONS
# # =========================

# def run_command(cmd: str) -> str:
#     try:
#         result = subprocess.run(
#             cmd, shell=True,
#             capture_output=True,
#             text=True,
#             timeout=60
#         )
#         return result.stdout + result.stderr
#     except Exception as e:
#         return f"Error running command: {str(e)}"
    
# # Here we use anthropic ai which is cost .. so we can try free ai tool 

# # def ask_ai(system: str, prompt: str) -> str:
# #     try:
# #         client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
# #         response = client.messages.create(
# #             model="claude-opus-4-5",
# #             max_tokens=1024,
# #             messages=[{"role": "user", "content": f"System context: {system}\n\nQuestion: {prompt}"}]
# #         )
# #         return response.content[0].text
# #     except Exception as e:
# #         return f"AI Error: {str(e)}"



# # Here i use grokai for free

# def ask_ai(system: str, prompt: str) -> str:
#     """Ask Groq AI a question — FREE!"""
#     try:
#         client = Groq(api_key=os.getenv("GROQ_API_KEY"))
#         response = client.chat.completions.create(
#             # model="llama3-8b-8192",   # free model
#             model="llama-3.3-70b-versatile",
#             messages=[
#                 {"role": "system", "content": system},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=1024
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         return f"AI Error: {str(e)}"

# # =========================
# # WATCHDOG
# # =========================

# CRITICAL_CONTAINERS = {
#    "frontend": "frontend",
#     "backend": "backend",
#     "nginx": "nginx"
# }

# COMPOSE_PATH = "/home/ubuntu/supachat"

# def check_container(container_name: str) -> bool:
#     result = run_command(
#         f"docker inspect -f '{{{{.State.Running}}}}' {container_name} 2>&1"
#     )
#     return "true" in result

# def watchdog():
#     print("🐕 Watchdog started — monitoring containers...")
#     while True:
#         for container_name, service_name in CRITICAL_CONTAINERS.items():
#             try:
#                 is_running = check_container(container_name)
#                 if not is_running:
#                     print(f"🚨 {container_name} is DOWN! Recreating...")
#                     result = run_command(
#                         f"cd {COMPOSE_PATH} && docker compose up -d --no-deps {service_name}"
#                     )
#                     print(f"✅ Recreate result: {result}")
#                 else:
#                     print(f"✅ {container_name} is healthy")
#             except Exception as e:
#                 print(f"❌ Watchdog error: {e}")
#         time.sleep(15)

# # =========================
# # LIFESPAN — starts watchdog
# # =========================

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print("🚀 Starting DevOps Agent...")
#     thread = threading.Thread(target=watchdog, daemon=True)
#     thread.start()
#     print("🐕 Watchdog thread started!")
#     yield
#     print("🛑 Shutting down...")

# # =========================
# # APP
# # =========================

# app = FastAPI(title="SupaChat DevOps Agent", lifespan=lifespan)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # =========================
# # REQUEST MODELS
# # =========================

# class CommandRequest(BaseModel):
#     command: str

# class LogRequest(BaseModel):
#     container: str
#     lines: int = 50

# class DiagnoseRequest(BaseModel):
#     issue: str

# class ChatRequest(BaseModel):
#     message: str

# # =========================
# # HEALTH CHECK
# # =========================

# @app.get("/health")
# def health():
#     return {"status": "ok", "service": "devops-agent"}

# # =========================
# # 1. CONTAINER STATUS
# # =========================

# # Clean & understandable output

# @app.get("/agent/status")
# def get_status():
#     output = run_command("docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'")
    
#     summary = ask_ai(
#         "You are a DevOps assistant. Be concise and use emojis.",
#         f"""Docker container status:
# {output}

# Reply in this exact format:
# Total Containers: X
# ✅ Running: list them
# ❌ Down: list them or 'None'
# ⚠️  Action needed: yes/no and what
# Overall Health: Healthy/Unhealthy"""
#     )
    
#     return {
#         "status": output,
#         "summary": summary
#     }

# # =========================
# # 2. CONTAINER LOGS
# # =========================

# # Cleaner logs endpoint
# @app.get("/agent/logs/{container_name}")
# def get_logs(container_name: str, lines: int = 50):
#     output = run_command(f"docker logs {container_name} --tail {lines} 2>&1")
    
#     summary = ask_ai(
#         "You are a DevOps assistant. Be very concise.",
#         f"""Logs from {container_name}:
# {output}

# Reply in this format:
# Status: Normal/Warning/Critical
# Key Events: (2-3 bullet points)
# Errors Found: Yes/No
# Action Required: Yes/No — what action"""
#     )
    
#     return {
#         "container": container_name,
#         "logs": output,
#         "summary": summary
#     }

# # =========================
# # 3. RESTART CONTAINER
# # =========================

# @app.post("/agent/restart/{container_name}")
# def restart_container(container_name: str):
#     output = run_command(f"docker restart {container_name}")
#     status = run_command(f"docker ps --filter name={container_name} --format '{{{{.Status}}}}'")
#     summary = ask_ai(
#         "You are a DevOps assistant.",
#         f"Container {container_name} restarted. Result: {output}. Status: {status}. Was it successful?"
#     )
#     return {"container": container_name, "restart_output": output, "current_status": status, "ai_summary": summary}

# # =========================
# # 4. DIAGNOSE ISSUE
# # =========================

# @app.post("/agent/diagnose")
# def diagnose(req: DiagnoseRequest):
#     containers = run_command("docker ps -a --format '{{.Names}}: {{.Status}}'")
#     disk = run_command("df -h /")
#     memory = run_command("free -h")
#     diagnosis = ask_ai(
#         f"You are a DevOps engineer. Containers: {containers} Disk: {disk} Memory: {memory}",
#         f"Issue: {req.issue}\n\nProvide diagnosis and step-by-step solution."
#     )
#     return {
#         "issue": req.issue,
#         "system_context": {"containers": containers, "disk": disk, "memory": memory},
#         "ai_diagnosis": diagnosis
#     }


# # =========================
# # 5. ERROR LOGS
# # =========================

# @app.get("/agent/errors/{container_name}")
# def get_errors(container_name: str):
#     output = run_command(f"docker logs {container_name} 2>&1 | grep -i 'error\\|exception\\|failed\\|critical' | tail -20")
#     if not output.strip():
#         return {"container": container_name, "errors_found": False, "message": "No errors found! ✅"}
#     explanation = ask_ai(
#         "You are a DevOps expert.",
#         f"Errors in {container_name}:\n{output}\n\nExplain each error and provide fixes."
#     )
#     return {"container": container_name, "errors_found": True, "raw_errors": output, "ai_explanation": explanation}

# # =========================
# # 6. DEPLOY
# # =========================

# @app.post("/agent/deploy")
# def deploy():
#     results = {}
#     results["git_pull"] = run_command(f"cd {COMPOSE_PATH} && git fetch origin && git reset --hard origin/main")
#     results["compose_down"] = run_command(f"cd {COMPOSE_PATH} && docker compose down")
#     results["compose_up"] = run_command(f"cd {COMPOSE_PATH} && docker compose up -d --build 2>&1")
#     # results["final_status"] = run_command("docker ps --format 'table {{.Names}}\t{{.Status}}'")
#     results["final_status"] = run_command("docker ps --format '{{.Names}}'")

#     summary = ask_ai(
#         "You are a DevOps assistant.",
#         f"Deployment results:\n{results}\n\nWas deployment successful? Any issues?"
#     )
#     return {"deployment_steps": results, "ai_summary": summary}

# # =========================
# # 7. FULL DIAGNOSTIC
# # =========================

# # Cleaner diagnostic endpoint
# @app.get("/agent/diagnostic")
# def full_diagnostic():
#     containers = run_command("docker ps -a --format 'table {{.Names}}\t{{.Status}}'")
#     disk = run_command("df -h / | tail -1")
#     memory = run_command("free -h | grep Mem")
#     cpu = run_command("top -bn1 | grep 'Cpu(s)'")
#     backend_health = run_command("curl -s http://localhost:8000/health")
    
#     summary = ask_ai(
#         "You are a DevOps engineer. Be concise.",
#         f"""System diagnostic:
# Containers: {containers}
# Disk: {disk}
# Memory: {memory}
# CPU: {cpu}
# Backend: {backend_health}

# Reply in this format:
# Health Score: X/10
# ✅ Good: (list)
# ⚠️  Warnings: (list or None)
# ❌ Issues: (list or None)
# Recommended Actions: (list or None)"""
#     )
    
#     return {
#         "containers": containers,
#         "disk": disk,
#         "memory": memory,
#         "cpu": cpu,
#         "backend": backend_health,
#         "health_report": summary
#     }


# # =========================
# # 8. CHAT
# # =========================

# # Cleaner chat endpoint
# @app.post("/agent/chat")
# def chat_with_agent(req: ChatRequest):
#     containers = run_command("docker ps -a --format '{{.Names}}: {{.Status}}'")
    
#     response = ask_ai(
#         f"""You are SupaChat DevOps Agent.
# Current containers: {containers}
# Be concise, practical, use bullet points.""",
#         req.message
#     )
    
#     return {
#         "question": req.message,
#         "answer": response
#     }

# # =========================
# # 9. WATCHDOG STATUS
# # =========================

# @app.get("/agent/watchdog")
# def watchdog_status():
#     statuses = {}
#     for container_name, service_name in CRITICAL_CONTAINERS.items():
#         is_running = check_container(container_name)
#         statuses[container_name] = {
#             "status": "✅ Running" if is_running else "❌ Down",
#             "service": service_name,
#             "auto_heal": "enabled"
#         }
#     return {
#         "watchdog": "active",
#         "check_interval": "15 seconds",
#         "monitored": statuses
#     }

# 2

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
import subprocess
from groq import Groq
import os
import threading
import time
from dotenv import load_dotenv

load_dotenv()

# =========================
# CONFIG
# =========================

CRITICAL_CONTAINERS = {
    "frontend": "frontend",
    "backend": "backend",
    "nginx": "nginx"
}

COMPOSE_PATH = "/home/ubuntu/supachat"
CHECK_INTERVAL = 15

# =========================
# HELPER FUNCTIONS
# =========================

def run_command(cmd: str) -> tuple:
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return 1, "", str(e)

def ask_ai(system: str, prompt: str) -> str:
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
            max_tokens=512
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Error: {str(e)}"

# =========================
# CONTAINER STATE DETECTION
# =========================

def get_container_state(container_name: str) -> str:
    code, out, err = run_command(
        f"docker inspect -f '{{{{.State.Status}}}}' {container_name}"
    )

    output = out + err

    if "No such object" in output:
        return "missing"
    elif "running" in output:
        return "running"
    elif "exited" in output or "created" in output:
        return "stopped"
    else:
        return "unknown"

# =========================
# AUTO-HEAL ENGINE
# =========================

def auto_heal(container_name: str, service_name: str):
    state = get_container_state(container_name)

    if state == "running":
        print(f"✅ {container_name} healthy")

    elif state == "stopped":
        print(f"⚠️ {container_name} stopped — restarting...")
        code, out, err = run_command(f"docker start {container_name}")
        if code == 0:
            print(f"🔁 Restarted {container_name}")
        else:
            print(f"❌ Restart failed: {err}")

    # elif state == "missing":
    #     print(f"🚨 {container_name} missing — recreating...")
    #     code, out, err = run_command(
    #         # f"cd {COMPOSE_PATH} && docker compose up -d {service_name}"
    #         f"cd {COMPOSE_PATH} && docker-compose up -d --build {service_name}"
    #     )
    #     if code == 0:
    #         print(f"🛠️ Recreated {container_name}")
    #     else:
    #         print(f"❌ Recreate failed: {err}")

    # else:
    #     print(f"❓ Unknown state for {container_name}")

    elif state == "missing":
        print(f"🚨 {container_name} missing — recreating...")

        code, out, err = run_command(
            f"cd {COMPOSE_PATH} && docker-compose up -d --build {service_name}"
        )

        print("STDOUT:", out)
        print("STDERR:", err)

        if code == 0:
            print(f"🛠️ Recreated {container_name}")
        else:
            print(f"❌ Recreate failed")

# =========================
# WATCHDOG THREAD
# =========================

def watchdog():
    print("🐕 Watchdog started...")
    while True:
        for container, service in CRITICAL_CONTAINERS.items():
            try:
                auto_heal(container, service)
            except Exception as e:
                print(f"❌ Watchdog error: {e}")
        time.sleep(CHECK_INTERVAL)

# =========================
# FASTAPI LIFESPAN
# =========================

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting DevOps Agent...")
    thread = threading.Thread(target=watchdog, daemon=True)
    thread.start()
    yield
    print("🛑 Stopping Agent...")

# =========================
# APP INIT
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
# MODELS
# =========================

class ChatRequest(BaseModel):
    message: str

# =========================
# ENDPOINTS
# =========================

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/agent/status")
def status():
    code, out, err = run_command("docker ps -a --format '{{.Names}}: {{.Status}}'")
    summary = ask_ai(
        "You are a DevOps assistant",
        f"Containers:\n{out}\nSummarize health."
    )
    return {"containers": out, "summary": summary}

@app.get("/agent/watchdog")
def watchdog_status():
    result = {}
    for c, s in CRITICAL_CONTAINERS.items():
        state = get_container_state(c)
        result[c] = {
            "state": state,
            "auto_heal": True
        }
    return {
        "watchdog": "active",
        "interval": CHECK_INTERVAL,
        "containers": result
    }

@app.post("/agent/restart/{container}")
def restart(container: str):
    code, out, err = run_command(f"docker restart {container}")
    return {"output": out, "error": err, "success": code == 0}

@app.post("/agent/chat")
def chat(req: ChatRequest):
    code, containers, _ = run_command("docker ps -a --format '{{.Names}}: {{.Status}}'")
    response = ask_ai(
        f"Containers: {containers}",
        req.message
    )
    return {"response": response}

@app.get("/agent/diagnostic")
def diagnostic():
    _, containers, _ = run_command("docker ps -a --format '{{.Names}} {{.Status}}'")
    _, disk, _ = run_command("df -h / | tail -1")
    _, memory, _ = run_command("free -h | grep Mem")
    _, cpu, _ = run_command("top -bn1 | grep 'Cpu(s)'")

    summary = ask_ai(
        "You are a DevOps engineer",
        f"""
Containers: {containers}
Disk: {disk}
Memory: {memory}
CPU: {cpu}

Give health report.
"""
    )

    return {
        "containers": containers,
        "disk": disk,
        "memory": memory,
        "cpu": cpu,
        "summary": summary
    }