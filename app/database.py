# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Define o nome do arquivo do banco de dados SQLite.
# Isso cria um arquivo no seu projeto chamado 'todos.db'
SQLITE_DATABASE_URL = "sqlite:///./todos.db"

# Cria a engine (mecanismo) para se conectar ao banco de dados.
# connect_args={"check_same_thread": False} é necessário para o SQLite.
# Isso permite que múltiplas threads (requisições) acessem o banco de dados.
engine = create_engine(
    SQLITE_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Cria uma "fábrica de sessões". Cada sessão é uma conexão com o banco de dados.
# autocommit=False: As transações precisam ser comitadas explicitamente.
# autoflush=False: Não salva automaticamente as mudanças no banco.
# bind=engine: Vincula a sessão à engine que criamos.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# `declarative_base()` é uma classe base para os modelos (tabelas) do banco.
# Nossos modelos herdarão dessa classe.
Base = declarative_base()


# Função para obter uma sessão de banco de dados.
# Isso é um "gerador" que será usado como uma dependência no FastAPI.
def get_db():
    db = SessionLocal()
    try:
        # Retorna a sessão, permitindo que as rotas usem o banco.
        yield db
    finally:
        # Garante que a sessão é fechada, liberando a conexão.
        db.close()