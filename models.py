from sqlalchemy import Column, Integer, String, DateTime, Date #importa tipos de dados e colunas do SQLAlchemy para definir a estrutura da tabela no banco de dados
from sqlalchemy.orm import declarative_base #importa a função que cria a base para os modelos ORM (que mapeiam classes Python para tabelas SQL)
from datetime import date #importa a data atual do sistema, usada para registrar a data do pedido
from pydantic import BaseModel, EmailStr #importa a classe BaseModel do Pydantic, usada para validação de dados da API / EmailStr garante que o email recebido tem formato válido

Base = declarative_base() #cria a classe base usada para definir modelos SQLAlchemy. Todas as tabelas herdarão dela.

class Order(Base): #cria a classe Order, que representa uma tabela chamada orders
    __tablename__ = "orders" #define o nome da tabela no banco de dados
    id = Column(Integer, primary_key=True, index=True) #id: chave primária, valor único e automático para cada pedido / index=True: cria um índice no banco, deixando buscas mais rápidas
    client_name = Column(String, nullable=False) #nome do cliente / nullable=False significa que é obrigatório
    client_email = Column(String, nullable=False) #email do cliente também é obrigatório
    order_number = Column(String, unique=True, nullable=False) #número do pedido / unique=True: o banco não permite dois pedidos com o mesmo número
    status = Column(String, nullable=False, nullable=False) #status do pedido
    order_date = Column(Date, nullable=False) #data do pedido / Nao esta em formato "DateTime" para conseguir comparar com a data atual no watsonx assistant

class OrderCreate(BaseModel): #esse modelo é usado pelo FastAPI para validar dados quando o cliente envia um novo pedido
    client_name: str
    client_email: EmailStr
    order_number: str
    status: str
    order_date: date

class OrderResponse(OrderCreate):
    id: int

    class Config:
        orm_mode = True
