from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


# 1. Definir o Modelo de Dados (Schema)
class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


# 2. Simular os dados básicos
items_db = {
    1: {"name": "Maçã", "price": 1.0, "is_offer": True},
    2: {"name": "Banana", "price": 0.5, "is_offer": False},
}
next_id = 3

app = FastAPI()


# ==========================================================
# OPERAÇÃO: CREATE (POST)
# ==========================================================
@app.post("/items/")
def create_item(item: Item):
    """Cria um novo item (Recurso: /items)"""
    global next_id
    items_db[next_id] = item.model_dump()  # Converte o Pydantic Model para dicionário
    item_id = next_id
    next_id += 1
    return {"id": item_id, "data": item}


# ==========================================================
# OPERAÇÃO: READ (GET) - Lista de itens
# ==========================================================
@app.get("/items/")
def read_items():
    """Retorna a lista de todos os itens (Recurso: /items)"""
    # Em um cenário real, você faria SELECT * FROM items
    return items_db


# ==========================================================
# OPERAÇÃO: READ (GET) - Item específico (já existia)
# ==========================================================
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    """Retorna um item específico pelo ID (Recurso: /items/{id})"""
    if item_id not in items_db:
        # Padrão REST: retornar código 404 para recurso não encontrado
        raise HTTPException(status_code=404, detail="Item not found")

    item_data = items_db[item_id]
    return {"item_id": item_id, "q": q, "data": item_data}


# ==========================================================
# OPERAÇÃO: UPDATE (PUT)
# ==========================================================
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    """Atualiza completamente um item existente (Recurso: /items/{id})"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    items_db[item_id] = item.model_dump()
    return {"message": "Item updated successfully", "id": item_id, "data": item}


# ==========================================================
# OPERAÇÃO: DELETE (DELETE)
# ==========================================================
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """Deleta um item específico (Recurso: /items/{id})"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    del items_db[item_id]
    # Padrão REST: retornar código 204 No Content para deleção bem-sucedida
    return {"message": "Item deleted successfully", "id": item_id}


# ==========================================================
# Rota Raiz (apenas demonstração)
# ==========================================================
@app.get("/")
def read_root():

    return {"message": "Welcome to the RESTful API do Mackenzie!"}
