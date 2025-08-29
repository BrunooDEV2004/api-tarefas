# app/schemas.py

from typing import Optional
from pydantic import BaseModel, EmailStr

# Schema base para as tarefas
# Usa o BaseModel do Pydantic para criar uma classe de validação
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

# Schema para a criação de uma nova tarefa
# Herda do TaskBase e adiciona um campo para o dono
class TaskCreate(TaskBase):
    pass

# Schema para a tarefa que será retornada pela API
# Herda do TaskBase e adiciona campos de metadados, como o ID
class TaskOut(TaskBase):
    id: int
    owner_id: int
    
    # A classe Config permite configurar o Pydantic
    class Config:
        # Permite que o Pydantic leia dados de objetos ORM
        # Isso significa que ele pode ler dados diretamente dos modelos do SQLAlchemy
        from_attributes = True

# Schemas para o usuário
class UserBase(BaseModel):
    email: EmailStr # Usa EmailStr para garantir que o email é válido

# Schema para a criação de um novo usuário
class UserCreate(UserBase):
    password: str

# Schema para o login do usuário
class UserLogin(UserBase):
    password: str

# Schema para o usuário que será retornado pela API
# Inclui o id e o campo de relacionamento `tasks`
class UserOut(UserBase):
    id: int
    # tasks: list[TaskOut] = [] # Se você quiser incluir as tarefas do usuário na resposta

    class Config:
        from_attributes = True

# Schema para o Token de autenticação JWT
class Token(BaseModel):
    access_token: str
    token_type: str

# Schema para os dados do token (payload)
class TokenData(BaseModel):
    email: Optional[str] = None