from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ ADD THIS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import os

# app = FastAPI()

class Query(BaseModel):
    query: str

# DB CONNECTION (replace with your Supabase details)
# conn = psycopg2.connect(
#     # # host="YOUR_HOST",
#     # # database="postgres",
#     # # user="postgres",
#     # # password="YOUR_PASSWORD"
#     "postgresql://postgres:phani123supabase@db.wxlpskafzqqxqazjtada.supabase.co:5432/postgres"
#     # # host="https://wxlpskafzqqxqazjtada.supabase.co",
#     # # database="postgres",
#     # # user="postgres",
#     # # password="Phani@123supachat"
  
# )
# conn = psycopg2.connect(
#     "postgresql://postgres.wxlpskafzqqxqazjtada:phani123supabase@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"
# )
# conn = psycopg2.connect(
#     "postgresql://postgres.wxlpskafzqqxqazjtada:phani123supabase@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"
# )
# conn = psycopg2.connect(
#     "postgresql://postgres.wxlpskafzqqxqazjtada:phani123supabase@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"
# )
# postgresql://postgres:[YOUR-PASSWORD]@db.wxlpskafzqqxqazjtada.supabase.co:5432/postgres
conn = psycopg2.connect(
    host="db.wxlpskafzqqxqazjtada.supabase.co",
    database="postgres",
    user="postgres",
    password="phani123supabase",
    # port=5432
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/query")
def run_query(q: Query):
    user_query = q.query.lower()

    # SIMPLE NLP → SQL MAPPING
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

    cur = conn.cursor()
    cur.execute(sql)

    columns = [desc[0] for desc in cur.description]
    rows = cur.fetchall()

    data = [dict(zip(columns, row)) for row in rows]

    return {
        "query": sql,
        "data": data
    }