# app/models.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

# Importa a Base que definimos em database.py
from .database import Base

# Define o modelo (tabela) para os usuários
class User(Base):
    # Nome da tabela no banco de dados
    __tablename__ = "users"

    # Colunas da tabela
    id = Column(Integer, primary_key=True, index=True) # Chave primária, auto-incremento
    email = Column(String, unique=True, index=True)  # E-mail do usuário, deve ser único
    hashed_password = Column(String) # Senha com hash (nunca armazene a senha em texto puro!)

    # Relacionamento com a tabela de tarefas.
    # Isso permite acessar as tarefas de um usuário facilmente (ex: user.tasks).
    tasks = relationship("Task", back_populates="owner")

# Define o modelo (tabela) para as tarefas
class Task(Base):
    # Nome da tabela no banco de dados
    __tablename__ = "tasks"

    # Colunas da tabela
    id = Column(Integer, primary_key=True, index=True) # Chave primária
    title = Column(String, index=True) # Título da tarefa
    description = Column(String, index=True, nullable=True) # Descrição da tarefa (opcional)
    completed = Column(Boolean, default=False) # Status da tarefa, padrão é False
    
    # Chave estrangeira que conecta a tarefa ao seu usuário (dono).
    # O `users.id` se refere à tabela `users` e à coluna `id`.
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Relacionamento com a tabela de usuários.
    # Isso permite acessar o usuário de uma tarefa facilmente (ex: task.owner).
    owner = relationship("User", back_populates="tasks")