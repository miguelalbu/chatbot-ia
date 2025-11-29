from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_chat_integration():
    """Teste de integração: SQL + RAG + LLM"""
    # Pergunta que exige SQL (preço) e perfumes vinculados a marca específica no SQLite
    payload = {"message": "Quais são os preços dos perfumes da oBoticário ?"}
    response = client.post("/api/chat", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert len(data["response"]) > 0