from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from contextlib import asynccontextmanager
import psycopg2
import os
from datetime import datetime

# ── Conexão com banco ──────────────────────────────────────────────────────────
def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "postgres"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "taskflow"),
        user=os.getenv("DB_USER", "taskuser"),
        password=os.getenv("DB_PASSWORD", "taskpass"),
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            done BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    conn.commit()
    cur.close()
    conn.close()
    yield

app = FastAPI(title="TaskFlow API", version="1.0.0", lifespan=lifespan)

# ── Modelos ────────────────────────────────────────────────────────────────────
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    done: Optional[bool] = None

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str]
    done: bool
    created_at: str

# ── Endpoints ──────────────────────────────────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@app.get("/tasks", response_model=List[Task])
def list_tasks():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, description, done, created_at FROM tasks ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        Task(id=r[0], title=r[1], description=r[2], done=r[3], created_at=str(r[4]))
        for r in rows
    ]

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tasks (title, description) VALUES (%s, %s) RETURNING id, title, description, done, created_at",
        (task.title, task.description),
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return Task(id=row[0], title=row[1], description=row[2], done=row[3], created_at=str(row[4]))

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskUpdate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM tasks WHERE id = %s", (task_id,))
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail="Task not found")

    fields, values = [], []
    if task.title is not None:
        fields.append("title = %s"); values.append(task.title)
    if task.description is not None:
        fields.append("description = %s"); values.append(task.description)
    if task.done is not None:
        fields.append("done = %s"); values.append(task.done)

    if fields:
        values.append(task_id)
        cur.execute(
            f"UPDATE tasks SET {', '.join(fields)} WHERE id = %s RETURNING id, title, description, done, created_at",
            values,
        )
        row = cur.fetchone()
        conn.commit()
    cur.close()
    conn.close()
    return Task(id=row[0], title=row[1], description=row[2], done=row[3], created_at=str(row[4]))

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s RETURNING id", (task_id,))
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail="Task not found")
    conn.commit()
    cur.close()
    conn.close()
