# app/routers/auth.py

from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import schemas, models, crud
from ..database import get_db
from ..auth_utils import authenticate_user, create_access_token

# Cria um novo router para as rotas de autenticação
router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

# Rota para o registro de um novo usuário
@router.post("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Busca um usuário no banco de dados com o email fornecido
    db_user = crud.get_user_by_email(db, email=user.email)
    
    # Se o usuário já existir, retorna um erro 400
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já registrado."
        )
    
    # Se não existir, cria o novo usuário no banco
    return crud.create_user(db=db, user=user)

# Rota para o login
@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    # Autentica o usuário com base nos dados do formulário (email e senha)
    user = authenticate_user(db, form_data.username, form_data.password)
    
    # Se a autenticação falhar, retorna um erro 401
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Se a autenticação for bem-sucedida, cria o token de acesso
    access_token_expires = timedelta(minutes=30) # O token expira em 30 minutos
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    # Retorna o token para o cliente
    return {"access_token": access_token, "token_type": "bearer"}