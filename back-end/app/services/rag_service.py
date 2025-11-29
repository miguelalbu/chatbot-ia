# app/services/rag_service.py
import chromadb
from app.config.settings import settings
import os

class RAGService:
    def __init__(self):
        # Persistente para não recriar a cada restart
        self.client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
        self.collection = self.client.get_or_create_collection(name="base_conhecimento")
        self._seed_data()

    def _seed_data(self):
        """Popula o ChromaDB se estiver vazio."""
        if self.collection.count() == 0:
            docs = [
                "Política de Troca: Perfumes abertos não podem ser devolvidos. Trocas apenas lacrados em 30 dias.",
                "Dica: Para maior fixação, aplique em áreas quentes (pescoço, pulsos).",
                "Essência Real: Amadeirado, notas de sândalo. Ideal para a noite.",
                "Aqua Blue: Cítrico e marinho. Ideal para dias quentes e escritório.",
                "Frete: Grátis acima de R$ 400,00 para todo o Brasil."
            ]
            ids = [f"id_{i}" for i in range(len(docs))]
            self.collection.add(documents=docs, ids=ids)

    def search(self, query: str, n_results: int = 2) -> str:
        results = self.collection.query(query_texts=[query], n_results=n_results)
        if results['documents']:
            return "\n".join(results['documents'][0])
        return "Nenhuma informação específica encontrada na base de conhecimento."