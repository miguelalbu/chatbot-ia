import chromadb
from app.config.settings import settings
import os
from pypdf import PdfReader 

class RAGService:
    def __init__(self):
        # Configura o ChromaDB no modo persistente
        # O Chroma usa automaticamente o modelo 'all-MiniLM-L6-v2' (Local e Grátis)
        self.client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
        self.collection = self.client.get_or_create_collection(name="base_conhecimento")
        self._seed_data()

    def _seed_data(self):
        """Lê PDF e popula o ChromaDB se estiver vazio."""
        if self.collection.count() == 0:
            print("\n--- [RAG] Indexando documentos (Modo Local)... ---")
            
            documents = []
            ids = []
            pdf_path = "data/manual_perfumes.pdf"

            # 1. TENTA LER O PDF
            if os.path.exists(pdf_path):
                print(f"--- [RAG] Lendo arquivo PDF: {pdf_path} ---")
                try:
                    reader = PdfReader(pdf_path)
                    for i, page in enumerate(reader.pages):
                        texto = page.extract_text()
                        if texto and len(texto.strip()) > 10:
                            # Limpeza básica
                            clean_text = texto.replace('\n', ' ').strip()
                            documents.append(clean_text)
                            ids.append(f"doc_pdf_pag_{i+1}")
                    print(f"--- [RAG] Sucesso! {len(documents)} páginas processadas. ---")
                except Exception as e:
                    print(f"--- [RAG] Erro ao ler PDF: {e} ---")
            
            # 2. FALLBACK (Dados de segurança)
            if not documents:
                print("--- [RAG] PDF não encontrado. Usando dados padrão. ---")
                documents = [
                    "Política de Troca: Perfumes abertos não podem ser devolvidos.",
                    "Dica: Aplique em áreas quentes (pescoço, pulsos).",
                    "Royal Scents: Especialistas em importados desde 2015."
                ]
                ids = [f"doc_fallback_{i}" for i in range(len(documents))]

            # 3. SALVA NO CHROMADB (Embeddings locais acontecem aqui automaticamente)
            if documents:
                self.collection.add(documents=documents, ids=ids)
                print("--- [RAG] Base vetorial atualizada! ---\n")

    def search(self, query: str, n_results: int = 2) -> str:
        """Busca os trechos mais relevantes."""
        try:
            results = self.collection.query(query_texts=[query], n_results=n_results)
            if results['documents'] and results['documents'][0]:
                return "\n\n".join(results['documents'][0])
        except Exception as e:
            print(f"Erro na busca RAG: {e}")
        
        return "Nenhuma informação específica encontrada na base de conhecimento."