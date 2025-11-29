import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    # Defina caminhos absolutos ou relativos para o banco para evitar erros
    SQL_DB_PATH = "data/perfumaria.db"
    CHROMA_DB_PATH = "data/chroma_store"

settings = Settings()