from sqlalchemy import create_engine #função que cria a conexão com o banco de dados
from sqlalchemy.orm import sessionmaker #função que cria sessões do banco de dados, que permitem inserir, consultar, atualizar e deletar dados (CRUD)


SQLALCHEMY_DATABASE_URL = "sqlite:///./orders.db" #define a URL do banco de dados
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}) #cria o motor de conexão com o banco
# connect_args={"check_same_thread": False}: é um ajuste necessário no SQLite para que múltiplas conexões funcionem bem dentro do FastAPI
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False) #cria uma fábrica de sessões do banco