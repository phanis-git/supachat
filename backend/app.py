# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# # ✅ ADD THIS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # or ["http://localhost:5173"]
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# from fastapi import FastAPI
# from pydantic import BaseModel
# import psycopg2
# import os

# # app = FastAPI()

# class Query(BaseModel):
#     query: str

# # DB CONNECTION (replace with your Supabase details)


# # conn = psycopg2.connect(
# #     "postgresql://postgres.wxlpskafzqqxqazjtada:phani123supabase@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"
# # )

# conn = psycopg2.connect(
#     host="db.wxlpskafzqqxqazjtada.supabase.co",
#     database="postgres",
#     user="postgres",
#     password="phani123supabase",
#     # port=5432
# )

# @app.get("/health")
# def health():
#     return {"status": "ok"}

# @app.post("/query")
# def run_query(q: Query):
#     user_query = q.query.lower()

#     # SIMPLE NLP → SQL MAPPING
#     if "trending" in user_query:
#         sql = """
#         SELECT topic, SUM(views) as total_views
#         FROM articles
#         GROUP BY topic
#         ORDER BY total_views DESC
#         LIMIT 5;
#         """
#     elif "ai" in user_query:
#         sql = "SELECT * FROM articles WHERE topic='AI';"
#     elif "devops" in user_query:
#         sql = "SELECT * FROM articles WHERE topic='DevOps';"
#     else:
#         sql = "SELECT * FROM articles LIMIT 5;"

#     cur = conn.cursor()
#     cur.execute(sql)

#     columns = [desc[0] for desc in cur.description]
#     rows = cur.fetchall()

#     data = [dict(zip(columns, row)) for row in rows]

#     return {
#         "query": sql,
#         "data": data
#     }




from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2

app = FastAPI()

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
# def get_connection():
#     return psycopg2.connect(
#         # host="db.wxlpskafzqqxqazjtada.supabase.co",
#         # database="postgres",
#         # user="postgres",
#         # password="phani123supabase",
#         # port=5432,
#         # sslmode="require",
#         # connect_timeout=10

#         host="aws-0-ap-south-1.pooler.supabase.com",
#         database="postgres",
#         user="postgres.wxlpskafzqqxqazjtada",
#         password="phani123supabase",
#         port=6543,
#         sslmode="require"
#     )

def get_connection():
    return psycopg2.connect(
        # host="db.wxlpskafzqqxqazjtada.supabase.co",
        database="postgres",
        user="postgres",
        password="phani123supabase",
        # port=5432,
        sslmode="require",
        host="aws-0-ap-south-1.pooler.supabase.com",
        port=6543
    )


# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
def health():
    return {"status": "ok"}


# =========================
# MAIN QUERY ENDPOINT
# =========================
@app.post("/query")
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