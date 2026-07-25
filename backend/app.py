from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="Awake - Enterprise Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "awake.db"
HR_MASTER_PASSWORD = "admin123"

def get_db_connection():

    return sqlite3.connect(DB_FILE, timeout=15)

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            current_posture TEXT DEFAULT 'UNKNOWN',
            is_healthy TEXT DEFAULT 'NO',
            bonus_earnings_rs REAL DEFAULT 0.0,
            healthy_time_sec INTEGER DEFAULT 0,
            sleep_time_sec INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

@app.on_event("startup")
def startup_event():
    init_db()

# HR ADMIN AUTHENTICATION 

class AdminLogin(BaseModel):
    password: str

@app.post("/api/admin/login")
def admin_login(data: AdminLogin):
    if data.password == HR_MASTER_PASSWORD:
        return {"status": "success"}
    return {"error": "Invalid HR Credentials"}

# CONCURRENT POSTURE TRACKING 

class PostureData(BaseModel):
    name: str
    state: str

def update_database(name: str, state: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM employees WHERE name = ?", (name,))
    user = cursor.fetchone()
    if not user:
        cursor.execute("INSERT INTO employees (name) VALUES (?)", (name,))
        conn.commit()
        user_id = cursor.lastrowid
    else:
        user_id = user[0]

    is_healthy_flag = "YES" if state == "HEALTHY" else "NO"
    cursor.execute('UPDATE employees SET current_posture = ?, is_healthy = ? WHERE id = ?', (state, is_healthy_flag, user_id))
    
    if state == "HEALTHY":
        cursor.execute('''
            UPDATE employees 
            SET healthy_time_sec = healthy_time_sec + 1,
                bonus_earnings_rs = ROUND(bonus_earnings_rs + (100.0 / 3600.0), 2)
            WHERE id = ?
        ''', (user_id,))
    elif state == "SLEEPING":
        cursor.execute('UPDATE employees SET sleep_time_sec = sleep_time_sec + 1 WHERE id = ?', (user_id,))
        cursor.execute('SELECT sleep_time_sec, bonus_earnings_rs FROM employees WHERE id = ?', (user_id,))
        sleep_sec, current_money = cursor.fetchone()
        
        if sleep_sec >= 3600:
            new_money = max(0.0, round(current_money - 100.0, 2))
            cursor.execute('UPDATE employees SET bonus_earnings_rs = ?, sleep_time_sec = 0 WHERE id = ?', (new_money, user_id))
            
    conn.commit()
    conn.close()

@app.post("/update_posture")
def update_posture(data: PostureData, background_tasks: BackgroundTasks):
    background_tasks.add_task(update_database, data.name.strip(), data.state)
    return {"status": "success"}

# HR DATASET ENDPOINT 

@app.get("/api/dataset")
def get_dataset():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, current_posture, is_healthy, bonus_earnings_rs, healthy_time_sec, sleep_time_sec FROM employees')
    rows = cursor.fetchall()
    conn.close()
    
    dataset = []
    for row in rows:
        dataset.append({
            "id": row[0], "name": row[1], "current_posture": row[2],
            "is_healthy": row[3], "bonus_earnings": row[4],
            "healthy_time": row[5], "sleep_time": row[6]
        })
    return dataset