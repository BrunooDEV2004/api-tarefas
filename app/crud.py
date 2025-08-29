# app/crud.py

from sqlalchemy.orm import Session
from . import models, schemas
from .auth_utils import get_password_hash

# --- Funções para Usuários ---

# Busca um usuário pelo ID
def get_user(db: Session, user_id: int):
    # .first() retorna o primeiro resultado ou None
    return db.query(models.User).filter(models.User.id == user_id).first()

# Busca um usuário pelo email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Cria um novo usuário
def create_user(db: Session, user: schemas.UserCreate):
    # Cria o hash da senha antes de salvar no banco
    hashed_password = get_password_hash(user.password)
    # Cria uma instância do modelo User
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    
    # Adiciona e salva no banco
    db.add(db_user)
    db.commit()
    db.refresh(db_user) # Atualiza a instância com os dados do banco (como o ID)
    return db_user

# --- Funções para Tarefas ---

# Cria uma nova tarefa para um usuário específico
def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
    # Cria uma instância do modelo Task, já associada ao dono
    db_task = models.Task(**task.model_dump(), owner_id=user_id)
    
    # Adiciona e salva a tarefa no banco
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# Busca todas as tarefas de um usuário
def get_tasks(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    # Filtra as tarefas pelo owner_id e retorna os resultados
    return db.query(models.Task).filter(models.Task.owner_id == user_id).offset(skip).limit(limit).all()

# Busca uma tarefa específica de um usuário
def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

# Deleta uma tarefa específica
def delete_task(db: Session, task: models.Task):
    db.delete(task)
    db.commit()

# Atualiza uma tarefa
def update_task(db: Session, task: models.Task, updated_data: schemas.TaskBase):
    # Atualiza os campos do objeto com os novos dados
    for key, value in updated_data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    
    db.add(task)
    db.commit()
    db.refresh(task)
    return task