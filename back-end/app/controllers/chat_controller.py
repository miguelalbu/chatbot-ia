from fastapi import APIRouter, HTTPException
from app.models.schemas import UserMessage, BotResponse
from app.services.ai_service import AIService

router = APIRouter()

# Instanciamos o serviço de IA (que contém o SQL, RAG e Memory services dentro dele)
ai_service = AIService()

# --- ROTA DE ENVIO DE MENSAGEM (POST) ---
@router.post("/chat", response_model=BotResponse)
async def chat_endpoint(user_msg: UserMessage):
    """
    Recebe a mensagem do usuário, processa via LangChain (SQL+RAG+Redis)
    e retorna a resposta do Bot.
    """
    # Se o front não mandar session_id, usamos um padrão para testes
    session_id = user_msg.session_id or "usuario_padrao"
    
    try:
        # Chama o serviço principal
        response_text = ai_service.generate_response(user_msg.message, session_id)
        
        return BotResponse(response=response_text)
    
    except Exception as e:
        print(f"❌ [CONTROLLER] Erro no endpoint /chat: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao processar mensagem.")


# --- ROTA DE LIMPEZA DE HISTÓRICO (DELETE) ---
@router.delete("/chat/history/{session_id}")
async def clear_history_endpoint(session_id: str):
    """
    Limpa o histórico de conversa de uma sessão específica (Redis ou RAM).
    Usado quando o usuário clica em 'Nova Conversa'.
    """
    try:
        ai_service.memory_service.clear_history(session_id)
        
        print(f"🧹 [CONTROLLER] Histórico da sessão '{session_id}' apagado.")
        return {"message": "Histórico limpo com sucesso", "session_id": session_id}
        
    except Exception as e:
        print(f"❌ [CONTROLLER] Erro ao limpar histórico: {e}")
        raise HTTPException(status_code=500, detail="Erro ao limpar histórico.")