import redis
import json
from typing import List, Tuple

class MemoryService:
    def __init__(self):
        self.use_redis = False
        try:
            # Tenta conectar no Redis local (Porta padrão 6379)
            self.client = redis.Redis(host='localhost', port=6379, decode_responses=True, socket_connect_timeout=1)
            self.client.ping() # Testa conexão
            self.use_redis = True
            print("✅ [MEMORY] Conectado ao Redis com sucesso!")
        except Exception:
            print("⚠️ [MEMORY] Redis não detectado. Usando memória RAM (Fallback).")
            self.local_memory = {} # Fallback: Dicionário simples

    def add_message(self, session_id: str, role: str, content: str):
        """Salva uma mensagem no histórico."""
        msg_obj = json.dumps({"role": role, "content": content})
        
        if self.use_redis:
            key = f"chat:{session_id}"
            self.client.rpush(key, msg_obj)
            # Define expiração para 1 hora (3600 segundos) para não lotar o banco
            self.client.expire(key, 3600)
        else:
            if session_id not in self.local_memory:
                self.local_memory[session_id] = []
            self.local_memory[session_id].append(msg_obj)

    def get_history(self, session_id: str) -> List[Tuple[str, str]]:
        """Recupera o histórico formatado."""
        messages = []
        
        if self.use_redis:
            key = f"chat:{session_id}"
            # Pega todas as mensagens da lista
            raw_msgs = self.client.lrange(key, 0, -1)
        else:
            raw_msgs = self.local_memory.get(session_id, [])

        # Processa de JSON para Tupla
        for m in raw_msgs:
            data = json.loads(m)
            messages.append((data['role'], data['content']))
            
        return messages

    def clear_history(self, session_id: str):
        if self.use_redis:
            self.client.delete(f"chat:{session_id}")
        else:
            if session_id in self.local_memory:
                del self.local_memory[session_id]