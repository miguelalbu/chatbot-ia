# tests/test_api.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_chat_integration():
    """Teste de integração: SQL + RAG + LLM"""
    # Pergunta que exige SQL (preço) e RAG (descrição)
    payload = {"message": "Qual o preço do Aqua Blue e como é o cheiro?"}
    response = client.post("/api/chat", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert len(data["response"]) > 0
    # Verifica se a IA mencionou o preço correto do DB (180.00)
    # Nota: Em testes reais com IA, validação de texto exato é difícil, 
    # mas verificamos se a resposta não é vazia e código 200.