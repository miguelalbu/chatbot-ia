from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config.settings import settings
from app.services.sql_service import SQLService
from app.services.rag_service import RAGService
from app.services.memory_service import MemoryService

class AIService:
    def __init__(self):
        if not settings.GOOGLE_API_KEY:
            raise ValueError("API Key do Google não configurada!")
        
        # 1. Configuração do LLM via LangChain
        # Usamos temperature=0.7 para ele ser criativo mas não alucinar dados
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.7 
        )
        
        # 2. Injeção de Dependências (Seus serviços robustos)
        self.sql_service = SQLService()
        self.rag_service = RAGService()
        self.memory_service = MemoryService()

        # 3. Definição do Prompt Template (Padrão LangChain)
        self.prompt_template = PromptTemplate.from_template("""
        Você é um consultor especialista e vendedor da Loja de Perfumes 'Royal Scents'.
        
        >>> CONTEXTO DE DADOS (Fatos Reais) <<<
        ESTOQUE E PREÇOS (SQL):
        {sql_context}
        
        MANUAL E POLÍTICAS (RAG):
        {rag_context}
        
        >>> HISTÓRICO DA CONVERSA <<<
        {history}
        
        >>> NOVA MENSAGEM DO CLIENTE <<<
        {query}
        
        >>> DIRETRIZES DE RESPOSTA <<<
        1. Responda de forma fluida, amigável e persuasiva.
        2. Use ESTRITAMENTE os dados do SQL para preços e estoque.
        3. Use os dados do RAG para descrições, dicas e regras.
        4. Se não souber, diga que vai verificar com o gerente, não invente.
        5. Tente fechar a venda sugerindo produtos disponíveis.
        """)

        # 4. Criação da Chain (Cadeia de Processamento)
        # Prompt -> LLM -> Texto Puro
        self.chain = self.prompt_template | self.llm | StrOutputParser()

    def generate_response(self, user_query: str, session_id: str = "usuario_padrao") -> str:
        print(f"\n--- [LANGCHAIN] Processando Sessão '{session_id}': {user_query} ---")

        # A. Recuperação de Contexto (Seus serviços manuais)
        try:
            sql_context = self.sql_service.get_catalog_context()
        except Exception:
            sql_context = "Erro no catálogo."

        try:
            rag_context = self.rag_service.search(user_query)
        except Exception:
            rag_context = "Sem dados de base de conhecimento."

        # B. Recuperação de Memória
        history_tuples = self.memory_service.get_history(session_id)
        history_text = ""
        if history_tuples:
            for role, text in history_tuples[-6:]:
                role_name = "Cliente" if role == "user" else "Vendedor"
                history_text += f"{role_name}: {text}\n"
        else:
            history_text = "Início da interação."

        # C. Execução da Chain (A mágica do LangChain)
        print("🔗 [LANGCHAIN] Invocando a Chain...")
        try:
            bot_response = self.chain.invoke({
                "sql_context": sql_context,
                "rag_context": rag_context,
                "history": history_text,
                "query": user_query
            })
            
            # D. Salva na Memória
            self.memory_service.add_message(session_id, "user", user_query)
            self.memory_service.add_message(session_id, "model", bot_response)
            
            print("🚀 [LANGCHAIN] Resposta gerada com sucesso!\n")
            return bot_response

        except Exception as e:
            print(f"❌ [ERRO] Falha na Chain: {e}")
            return "Desculpe, tivemos um erro de comunicação com nosso sistema central."