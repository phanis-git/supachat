
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv() 
app = FastAPI()

Instrumentator().instrument(app).expose(app)
# =========================
# CORS CONFIG
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# REQUEST MODEL
# =========================
class Query(BaseModel):
    query: str


# =========================
# SAFE DB CONNECTION
# =========================




def get_connection():
    conn = psycopg2.connect(
         host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=int(os.getenv("DB_PORT", 5432)),
        sslmode="require",
    )

    print("✅ Connected successfully!")
    return conn

# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
def health():
    return {"status": "ok"}


# =========================
# MAIN QUERY ENDPOINT
# =========================
@app.post("/api/query")
def run_query(q: Query):

    try:
        user_query = q.query.lower()

        # =========================
        # SIMPLE NLP → SQL MAPPING
        # =========================
        if "trending" in user_query:
            sql = """
                SELECT topic, SUM(views) as total_views
                FROM articles
                GROUP BY topic
                ORDER BY total_views DESC
                LIMIT 5;
            """
        elif "ai" in user_query:
            sql = "SELECT * FROM articles WHERE topic='AI';"
        elif "devops" in user_query:
            sql = "SELECT * FROM articles WHERE topic='DevOps';"
        else:
            sql = "SELECT * FROM articles LIMIT 5;"

        # =========================
        # DB EXECUTION (SAFE)
        # =========================
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(sql)

        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()

        cur.close()
        conn.close()

        return {
            "query": sql,
            "data": [dict(zip(columns, row)) for row in rows]
        }

    except Exception as e:
        # 🔴 IMPORTANT: prevents Docker crash + shows real error
        print("❌ Backend Error:", str(e))

        return {
            "error": str(e),
            "message": "Backend query failed. Check DB/table/schema."
        }