from fastapi.testclient import TestClient
from main import app # Importa sua aplicação principal
import pytest

# Cliente de teste do FastAPI (simula requisições HTTP sem precisar subir o servidor)
client = TestClient(app)

# --- 1. TESTE BÁSICO (Smoke Test) ---
def test_read_root():
    """Verifica se a API está online e respondendo."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "online", "message": "Backend da Perfumaria rodando!"}

# --- 2. TESTE DE INTEGRAÇÃO SQL (Produtos) ---
def test_chat_sql_product_price():
    """
    Testa se o bot consegue recuperar um preço exato do SQLite.
    Pergunta: Quanto custa o Essencial Oud?
    Esperado: R$ 180,00 ou 180 na resposta.
    """
    payload = {
        "message": "Qual o preço do perfume Essencial Oud?",
        "session_id": "test_sql_user"
    }
    response = client.post("/api/chat", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    
    # A resposta da IA varia, mas DEVE conter o número 180 (preço do banco)
    resposta_ia = data["response"].lower()
    print(f"\n[SQL Test] Resposta da IA: {resposta_ia}")
    
    # Verifica palavras-chave
    assert "180" in resposta_ia or "180,00" in resposta_ia
    assert "essencial" in resposta_ia

# --- 3. TESTE DE INTEGRAÇÃO RAG (Políticas) ---
def test_chat_rag_policy():
    """
    Testa se o bot consegue ler as regras do PDF/RAG.
    Pergunta: Posso trocar perfume aberto?
    Esperado: Negativo (Não).
    """
    payload = {
        "message": "Comprei um perfume, abri o lacre e não gostei. Posso devolver?",
        "session_id": "test_rag_user"
    }
    response = client.post("/api/chat", json=payload)
    
    assert response.status_code == 200
    resposta_ia = response.json()["response"].lower()
    print(f"\n[RAG Test] Resposta da IA: {resposta_ia}")
    
    # O RAG diz que troca apenas lacrado, então a resposta deve ser negativa
    condicoes_negativas = ["não", "apenas lacrado", "lacre intacto", "impossível"]
    
    # Verifica se pelo menos uma condição negativa aparece na resposta
    assert any(x in resposta_ia for x in condicoes_negativas)

# --- 4. TESTE DE LIMPEZA DE MEMÓRIA (Redis/System) ---
def test_clear_history():
    """
    Testa se o endpoint de deletar histórico funciona.
    """
    session_id = "user_to_delete"
    
    # 1. Envia uma mensagem para criar histórico
    client.post("/api/chat", json={"message": "Oi", "session_id": session_id})
    
    # 2. Chama a rota de DELETE
    response = client.delete(f"/api/chat/history/{session_id}")
    
    assert response.status_code == 200
    assert response.json() == {
        "message": "Histórico limpo com sucesso", 
        "session_id": session_id
    }

# --- 5. TESTE DE ERRO (Input Vazio) ---
def test_empty_message_validation():
    """
    Testa se o sistema lida bem com input vazio (Pydantic deve barrar ou IA tratar).
    Nota: O comportamento depende de como o Pydantic está configurado, 
    mas esperamos que não quebre (500) sem tratamento.
    """
    # Enviando string vazia
    response = client.post("/api/chat", json={"message": "", "session_id": "bug_tester"})
    
    # Se o Pydantic validar min_length, pode ser 422. Se passar, deve ser 200 com resposta genérica.
    # Vamos assumir que queremos que a API não crash (500).
    assert response.status_code != 500