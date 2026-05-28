from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)

# ── Mock do banco para não precisar de Postgres nos testes ────────────────────
def mock_conn():
    conn = MagicMock()
    cur = MagicMock()
    conn.cursor.return_value = cur
    return conn, cur

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

@patch("app.main.get_connection")
def test_list_tasks_empty(mock_get_conn):
    conn, cur = mock_conn()
    mock_get_conn.return_value = conn
    cur.fetchall.return_value = []
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []

@patch("app.main.get_connection")
def test_create_task(mock_get_conn):
    conn, cur = mock_conn()
    mock_get_conn.return_value = conn
    cur.fetchone.return_value = (1, "Test Task", "Desc", False, "2024-01-01 00:00:00")
    response = client.post("/tasks", json={"title": "Test Task", "description": "Desc"})
    assert response.status_code == 201
    assert response.json()["title"] == "Test Task"

@patch("app.main.get_connection")
def test_delete_task_not_found(mock_get_conn):
    conn, cur = mock_conn()
    mock_get_conn.return_value = conn
    cur.fetchone.return_value = None
    response = client.delete("/tasks/999")
    assert response.status_code == 404
