from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import anthropic
import os
from dotenv import load_dotenv

import threading
import time

load_dotenv()

app = FastAPI(title="SupaChat DevOps Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# =========================
# HELPER FUNCTIONS
# =========================

def run_command(cmd: str) -> str:
    """Run shell command and return output"""
    try:
        result = subprocess.run(
            cmd, shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout + result.stderr
    except Exception as e:
        return f"Error running command: {str(e)}"

def ask_ai(system: str, prompt: str) -> str:
    """Ask Claude AI a question"""
    try:
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"System context: {system}\n\nQuestion: {prompt}"
                }
            ]
        )
        return response.content[0].text
    except Exception as e:
        return f"AI Error: {str(e)}"

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

# =========================
# HEALTH CHECK
# =========================

@app.get("/health")
def health():
    return {"status": "ok", "service": "devops-agent"}

# =========================
# 1. GET ALL CONTAINER STATUS
# =========================

@app.get("/agent/status")
def get_status():
    """Get status of all Docker containers"""
    output = run_command("docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'")
    
    # Ask AI to summarize
    summary = ask_ai(
        "You are a DevOps assistant. Analyze Docker container status.",
        f"Here is the docker ps output:\n{output}\n\nGive a brief health summary. List any containers that are down or unhealthy."
    )
    
    return {
        "raw_output": output,
        "ai_summary": summary
    }

# =========================
# 2. GET CONTAINER LOGS
# =========================

@app.get("/agent/logs/{container_name}")
def get_logs(container_name: str, lines: int = 50):
    """Get and analyze logs from a container"""
    output = run_command(f"docker logs {container_name} --tail {lines} 2>&1")
    
    # Ask AI to summarize logs
    summary = ask_ai(
        "You are a DevOps assistant. Analyze Docker container logs.",
        f"Here are the last {lines} lines of logs from {container_name}:\n{output}\n\nSummarize what is happening. Highlight any errors or warnings."
    )
    
    return {
        "container": container_name,
        "raw_logs": output,
        "ai_summary": summary
    }

# =========================
# 3. RESTART CONTAINER
# =========================

@app.post("/agent/restart/{container_name}")
def restart_container(container_name: str):
    """Restart a specific container"""
    output = run_command(f"docker restart {container_name}")
    
    # Check if restart was successful
    status = run_command(f"docker ps --filter name={container_name} --format '{{{{.Status}}}}'")
    
    summary = ask_ai(
        "You are a DevOps assistant.",
        f"Container {container_name} was restarted. Result: {output}. Current status: {status}. Was the restart successful?"
    )
    
    return {
        "container": container_name,
        "restart_output": output,
        "current_status": status,
        "ai_summary": summary
    }

# =========================
# 4. DIAGNOSE AN ISSUE
# =========================

@app.post("/agent/diagnose")
def diagnose(req: DiagnoseRequest):
    """AI diagnoses a DevOps issue"""
    
    # Gather system context
    containers = run_command("docker ps -a --format '{{.Names}}: {{.Status}}'")
    disk = run_command("df -h /")
    memory = run_command("free -h")
    
    # Ask AI to diagnose
    diagnosis = ask_ai(
        f"""You are an expert DevOps engineer. 
        Current system state:
        Containers: {containers}
        Disk: {disk}
        Memory: {memory}
        """,
        f"The user is experiencing this issue: {req.issue}\n\nProvide a diagnosis and step-by-step solution."
    )
    
    return {
        "issue": req.issue,
        "system_context": {
            "containers": containers,
            "disk": disk,
            "memory": memory
        },
        "ai_diagnosis": diagnosis
    }

# =========================
# 5. SUMMARIZE FAILED LOGS
# =========================

@app.get("/agent/errors/{container_name}")
def get_errors(container_name: str):
    """Get only error logs and summarize them"""
    
    # Get logs with errors only
    output = run_command(f"docker logs {container_name} 2>&1 | grep -i 'error\\|exception\\|failed\\|critical' | tail -20")
    
    if not output.strip():
        return {
            "container": container_name,
            "errors_found": False,
            "message": "No errors found in logs! ✅"
        }
    
    # Ask AI to explain errors
    explanation = ask_ai(
        "You are a DevOps expert. Explain errors in simple terms.",
        f"These errors were found in {container_name} logs:\n{output}\n\nExplain each error and provide fixes."
    )
    
    return {
        "container": container_name,
        "errors_found": True,
        "raw_errors": output,
        "ai_explanation": explanation
    }

# =========================
# 6. DEPLOY APPLICATION
# =========================

@app.post("/agent/deploy")
def deploy():
    """Pull latest code and redeploy"""
    
    results = {}
    
    # Step 1: Git pull
    results["git_pull"] = run_command("cd ~/supachat && git fetch origin && git reset --hard origin/main")
    
    # Step 2: Docker compose down
    results["compose_down"] = run_command("cd ~/supachat && docker compose down")
    
    # Step 3: Docker compose up
    results["compose_up"] = run_command("cd ~/supachat && docker compose up -d --build 2>&1")
    
    # Step 4: Check status
    results["final_status"] = run_command("docker ps --format 'table {{.Names}}\t{{.Status}}'")
    
    # Ask AI to summarize deployment
    summary = ask_ai(
        "You are a DevOps assistant analyzing a deployment.",
        f"Deployment results:\n{results}\n\nWas the deployment successful? Any issues?"
    )
    
    return {
        "deployment_steps": results,
        "ai_summary": summary
    }

# =========================
# 7. FULL HEALTH DIAGNOSTIC
# =========================

@app.get("/agent/diagnostic")
def full_diagnostic():
    """Run complete system health check"""
    
    diagnostic = {}
    
    # Gather all system info
    diagnostic["containers"] = run_command("docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'")
    diagnostic["disk_usage"] = run_command("df -h /")
    diagnostic["memory_usage"] = run_command("free -h")
    diagnostic["cpu_usage"] = run_command("top -bn1 | grep 'Cpu(s)'")
    diagnostic["backend_health"] = run_command("curl -s http://localhost:8000/health")
    diagnostic["nginx_status"] = run_command("docker logs supachat-nginx-1 --tail 5 2>&1")
    diagnostic["backend_errors"] = run_command("docker logs supachat-backend-1 2>&1 | grep -i error | tail -5")
    
    # Ask AI for complete analysis
    analysis = ask_ai(
        "You are a senior DevOps engineer doing a system health check.",
        f"Complete system diagnostic:\n{diagnostic}\n\nProvide a full health report. Rate overall health 1-10. List any issues and recommended actions."
    )
    
    return {
        "diagnostic_data": diagnostic,
        "ai_health_report": analysis
    }

# =========================
# 8. CHAT WITH AGENT
# =========================

class ChatRequest(BaseModel):
    message: str

@app.post("/agent/chat")
def chat_with_agent(req: ChatRequest):
    """Chat with DevOps agent in natural language"""
    
    # Get current system state for context
    containers = run_command("docker ps -a --format '{{.Names}}: {{.Status}}'")
    
    response = ask_ai(
        f"""You are a helpful DevOps agent for SupaChat application.
        Current container status: {containers}
        
        You can help with:
        - Explaining what's wrong
        - Suggesting fixes
        - Explaining logs
        - DevOps best practices
        
        Be concise and practical.
        """,
        req.message
    )
    
    return {
        "user_message": req.message,
        "agent_response": response
    }


# =========================
# WATCHDOG — Auto Healer
# =========================

CRITICAL_CONTAINERS = [
    "supachat-frontend-1",
    "supachat-backend-1",
    "supachat-nginx-1"
]

def watchdog():
    """Monitors containers and auto-restarts if down"""
    print("🐕 Watchdog started — monitoring containers...")
    
    while True:
        try:
            for container in CRITICAL_CONTAINERS:
                # Check if container is running
                result = run_command(
                    f"docker inspect -f '{{{{.State.Running}}}}' {container} 2>&1"
                )
                
                if "true" not in result:
                    print(f"🚨 {container} is DOWN! Restarting...")
                    
                    # Try to restart
                    restart = run_command(f"docker compose -f /home/ubuntu/supachat/docker-compose.yml up -d {container.replace('supachat-', '').replace('-1', '')}")
                    
                    print(f"✅ Restart attempted for {container}: {restart}")
                else:
                    print(f"✅ {container} is healthy")
                    
        except Exception as e:
            print(f"❌ Watchdog error: {e}")
        
        # Check every 30 seconds
        time.sleep(30)

# Start watchdog in background when app starts
@app.on_event("startup")
async def start_watchdog():
    thread = threading.Thread(target=watchdog, daemon=True)
    thread.start()
    print("🐕 Watchdog thread started!")

# =========================
# WATCHDOG STATUS ENDPOINT
# =========================

@app.get("/agent/watchdog")
def watchdog_status():
    """Check what watchdog is monitoring"""
    statuses = {}
    
    for container in CRITICAL_CONTAINERS:
        result = run_command(
            f"docker inspect -f '{{{{.State.Running}}}}' {container} 2>&1"
        )
        statuses[container] = "✅ Running" if "true" in result else "❌ Down"
    
    return {
        "monitored_containers": statuses,
        "check_interval": "30 seconds",
        "auto_restart": "enabled"
    }