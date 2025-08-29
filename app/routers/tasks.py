# app/routers/tasks.py

from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas, crud, models
from ..database import get_db
from ..auth_utils import get_current_user

# Cria um novo router para as rotas de tarefas
router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    # Todas as rotas neste router exigem autenticação
    dependencies=[Depends(get_current_user)] 
)

# Rota para criar uma nova tarefa
@router.post("/", response_model=schemas.TaskOut)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Chama a função de CRUD para criar a tarefa no banco de dados
    return crud.create_task(db=db, task=task, user_id=current_user.id)

# Rota para listar todas as tarefas do usuário autenticado
@router.get("/", response_model=List[schemas.TaskOut])
def read_tasks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Chama a função de CRUD para buscar as tarefas
    return crud.get_tasks(db, user_id=current_user.id)

# Rota para buscar uma tarefa específica por ID
@router.get("/{task_id}", response_model=schemas.TaskOut)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Busca a tarefa
    db_task = crud.get_task(db, task_id=task_id)
    
    # Se a tarefa não existir ou não pertencer ao usuário, retorna erro
    if db_task is None or db_task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada."
        )
    return db_task

# Rota para atualizar uma tarefa
@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(
    task_id: int,
    updated_data: schemas.TaskBase,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Busca a tarefa a ser atualizada
    db_task = crud.get_task(db, task_id=task_id)
    
    # Se a tarefa não existir ou não pertencer ao usuário, retorna erro
    if db_task is None or db_task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada."
        )
    
    # Chama a função de CRUD para atualizar os dados
    return crud.update_task(db=db, task=db_task, updated_data=updated_data)

# Rota para deletar uma tarefa
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Busca a tarefa a ser deletada
    db_task = crud.get_task(db, task_id=task_id)
    
    # Se a tarefa não existir ou não pertencer ao usuário, retorna erro
    if db_task is None or db_task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada."
        )
    
    # Chama a função de CRUD para deletar
    crud.delete_task(db, task=db_task)
    return