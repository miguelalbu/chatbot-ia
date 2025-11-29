# main.py
import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers import chat_controller

app = FastAPI(title="Perfumaria AI - RAG & SQL")

# Configuração CORS (Permitir Front React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir Rotas
app.include_router(chat_controller.router, prefix="/api")

@app.get("/")
def health_check():
    return {"status": "online", "message": "Backend da Perfumaria rodando!"}

if __name__ == "__main__":
    # Cria pasta data se não existir ao rodar direto
    os.makedirs("data", exist_ok=True)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)