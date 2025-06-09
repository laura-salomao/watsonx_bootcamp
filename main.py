from fastapi import FastAPI, Depends, HTTPException #importa o FastAPI para criar a aplicação e o Depends para gerenciar injeção de dependências (como o banco de dados)
from sqlalchemy.orm import Session #importa a classe Session, usada para trabalhar com o banco de dados (inserir, consultar, etc.)
from database import engine, SessionLocal #importa objetos do arquivo database.py
from models import Base, Order, OrderCreate, OrderResponse #importa os modelos definidos no models.py
from typing import List
from datetime import date #importa a data atual do sistema, usada para registrar a data do pedido

app = FastAPI() #cria a instância principal da API

# Cria as tabelas no banco, se ainda não existirem
Base.metadata.create_all(bind=engine)

# Dependência para obter uma sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint POST para criar pedidos
@app.post("/orders", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):

# Garante que o valor seja do tipo date, mesmo se vier como string
order.order_date = (
    order.order_date
    if isinstance(order.order_date, date)
    else date.fromisoformat(order.order_date)
)

    db_order = Order(**order.dict()) #converte os dados do OrderCreate para um objeto Order compatível com o banco
    db.add(db_order) #adiciona o novo pedido no banco
    db.commit() #salva o novo pedido no banco
    db.refresh(db_order) #atualiza o objeto com os dados finais (por exemplo, o ID gerado automaticamente)
    return db_order #retorna o pedido criado como resposta JSON

# Endpoint GET para listar pedidos
@app.get("/orders", response_model=List[OrderResponse])
def list_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


# Endpoint GET para pesquisar pedidos
@app.get("/orders/search", response_model=List[OrderResponse])
def search_orders(number: str = None, db: Session = Depends(get_db)):
    query = db.query(Order)

    if number:
        query = query.filter(Order.order_number.ilike(number))

    results = query.all()

    if not results:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    return results


# Endpoint DELETE para excluir pedidos
@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    db.delete(db_order)
    db.commit()
    return {"detail": f"Pedido {order_id} removido com sucesso"}

# Endpoint PUT para atualizar pedidos
@app.put("/orders/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, updated_order: OrderCreate, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    for field, value in updated_order.dict().items():
        setattr(db_order, field, value)

    db.commit()
    db.refresh(db_order)
    return db_order