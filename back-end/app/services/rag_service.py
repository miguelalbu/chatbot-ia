import chromadb
from app.config.settings import settings
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class RAGService:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
        self.collection = self.client.get_or_create_collection(name="base_conhecimento")
        # Tenta verificar se já tem dados. Se estiver vazio, popula.
        if self.collection.count() == 0:
            self._seed_data()

    def _seed_data(self):
        print("\n--- [RAG] Iniciando indexação de DIRETÓRIO... ---")
        
        all_docs = []
        data_folder = "data" # Pasta onde ficam os PDFs
        
        # 1. Varre a pasta procurando PDFs
        if os.path.exists(data_folder):
            files = [f for f in os.listdir(data_folder) if f.endswith('.pdf')]
            
            if not files:
                print("--- [RAG] Nenhum PDF encontrado na pasta data/ ---")
            
            for filename in files:
                file_path = os.path.join(data_folder, filename)
                print(f"--- [RAG] Lendo arquivo: {filename} ---")
                
                try:
                    loader = PyPDFLoader(file_path)
                    raw_docs = loader.load()
                    all_docs.extend(raw_docs)
                except Exception as e:
                    print(f"❌ Erro ao ler {filename}: {e}")
        
        # 2. Processamento e Split (LangChain)
        final_docs = []
        ids = []
        
        if all_docs:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            final_docs = text_splitter.split_documents(all_docs)
            
            # Cria IDs únicos para cada pedaço
            for i, doc in enumerate(final_docs):
                # Limpeza extra de quebras de linha
                doc.page_content = doc.page_content.replace('\n', ' ').strip()
                ids.append(f"doc_{i}")
        
        # 3. Fallback (Se não tiver nenhum PDF válido)
        if not final_docs:
            print("--- [RAG] Usando dados de Fallback (Segurança) ---")
            texts = [
                "Luar Cosméticos: Somos especialistas em fragrâncias nacionais e importadas.",
                "Política: Trocas apenas com lacre intacto em 30 dias."
            ]
            final_docs = [Document(page_content=t) for t in texts]
            ids = [f"fallback_{i}" for i in range(len(texts))]

        # 4. Salva no ChromaDB
        # Extrai apenas o texto para salvar no Chroma nativo
        texts_to_save = [d.page_content for d in final_docs]
        metadatas = [{"source": "pdf_rag"} for _ in texts_to_save]
        
        if texts_to_save:
            self.collection.add(
                documents=texts_to_save,
                metadatas=metadatas,
                ids=ids
            )
            print(f"--- [RAG] Sucesso! {len(texts_to_save)} fragmentos de conhecimento adicionados. ---\n")

    def search(self, query: str, n_results: int = 3) -> str:
        """Busca os trechos mais relevantes."""
        try:
            results = self.collection.query(query_texts=[query], n_results=n_results)
            if results['documents'] and results['documents'][0]:
                return "\n\n".join(results['documents'][0])
        except Exception as e:
            print(f"Erro na busca RAG: {e}")
        
        return "Nenhuma informação específica encontrada na base de conhecimento."