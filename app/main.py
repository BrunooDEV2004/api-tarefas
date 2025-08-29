# app/main.py

from fastapi import FastAPI
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
from .routers import auth, tasks

# Cria todas as tabelas no banco de dados, se elas ainda não existirem.
models.Base.metadata.create_all(bind=engine)

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="API de Tarefas (To-Do List)",
    description="Uma API simples para gerenciar tarefas, com autenticação JWT.",
    version="1.0.0",
)

# Inclui os routers (rotas) na aplicação.
app.include_router(auth.router)
app.include_router(tasks.router)

# Rota de teste para verificar se a API está funcionando.
@app.get("/")
def read_root():
    return {"message": "Bem-vindo à sua API de Tarefas! Acesse /docs para ver a documentação."}