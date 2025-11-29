import sqlite3
from app.config.settings import settings
import os

class SQLService:
    def __init__(self):
        self.db_path = settings.SQL_DB_PATH
        self._init_db()

    def _init_db(self):
        """Inicializa a tabela e dados seed se não existirem."""
        os.makedirs("data", exist_ok=True) # Garante que a pasta existe
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS perfumes (
                id INTEGER PRIMARY KEY,
                nome TEXT,
                marca TEXT,
                preco REAL,
                estoque INTEGER
            )
        ''')
        # Seed básico para evitar banco vazio
        cursor.execute("SELECT count(*) FROM perfumes")
        if cursor.fetchone()[0] == 0:
            dados = [
                (1, 'Essência Real', 'Royal Scents', 250.00, 15),
                (2, 'Aqua Blue', 'Oceanic', 180.00, 8),
                (3, 'Nightfall Intense', 'Dark Wood', 320.00, 5),
                (4, 'Citrus Breeze', 'Summer Vibes', 120.00, 20)
            ]
            cursor.executemany("INSERT INTO perfumes VALUES (?, ?, ?, ?, ?)", dados)
            conn.commit()
        conn.close()

    def get_catalog_context(self) -> str:
        """Retorna os dados do banco formatados para o LLM."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT nome, marca, preco, estoque FROM perfumes")
        produtos = cursor.fetchall()
        conn.close()
        
        # Formata bonito para a IA entender
        lista_fmt = [f"- {p[0]} ({p[1]}): R$ {p[2]} | Estoque: {p[3]}" for p in produtos]
        return "\n".join(lista_fmt)