# app/services/ai_service.py
import google.generativeai as genai
from app.config.settings import settings
from app.services.sql_service import SQLService
from app.services.rag_service import RAGService

class AIService:
    def __init__(self):
        if not settings.GOOGLE_API_KEY:
            raise ValueError("API Key do Google não configurada!")
        
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Injeção das dependências (Serviços)
        self.sql_service = SQLService()
        self.rag_service = RAGService()

    def generate_response(self, user_query: str) -> str:
        # 1. Busca Contexto SQL
        sql_context = self.sql_service.get_catalog_context()
        
        # 2. Busca Contexto RAG
        rag_context = self.rag_service.search(user_query)

        # 3. Monta o Prompt (Engenharia de Prompt)
        prompt = f"""
        Você é um consultor especialista da Loja de Perfumes.
        
        PERGUNTA DO CLIENTE: "{user_query}"
        
        CONTEXTO DE ESTOQUE E PREÇOS (SQL):
        {sql_context}
        
        CONTEXTO DE POLÍTICAS E DETALHES (RAG):
        {rag_context}
        
        INSTRUÇÕES:
        - Use os dados acima para responder.
        - Se perguntarem preço, seja exato.
        - Se perguntarem sobre cheiro/uso, seja criativo mas baseie-se no RAG.
        - Seja polido e vendedor.
        """

        # 4. Chama a LLM
        response = self.model.generate_content(prompt)
        return response.text