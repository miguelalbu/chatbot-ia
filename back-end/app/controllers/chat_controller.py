# app/controllers/chat_controller.py
from fastapi import APIRouter, HTTPException
from app.models.schemas import UserMessage, BotResponse
from app.services.ai_service import AIService

router = APIRouter()
ai_service = AIService() # Instancia o serviço

@router.post("/chat", response_model=BotResponse)
async def chat_endpoint(user_msg: UserMessage):
    try:
        response_text = ai_service.generate_response(user_msg.message)
        return BotResponse(response=response_text)
    except Exception as e:
        # Logar o erro real no console para debug
        print(f"Erro: {e}") 
        raise HTTPException(status_code=500, detail="Erro interno no processamento da IA.")