from fastapi import APIRouter, HTTPException
from schemas.user_schema import DadosUser
from database.fake_db import bd_users
from uuid import uuid4

router = APIRouter()

@router.post("/criar_usuario")
def criar_user(user: DadosUser):
    dados = user.model_dump()
    dados["id"] = str(uuid4())
    bd_users.append(dados)
    return {
        "mensagem": f"Bem-vindo, {dados["username"]}."
    }
@router.put("/users/{user_id}")
def edit_user(user_id: str, nova_senha: str):
    user = next(((user) for user in bd_users if user_id == user["id"]), None)
    if not user:
        return HTTPException(status_code= 404, detail="O usuário em questão não foi encontrado.")
    elif nova_senha == user["password"]:
        return HTTPException(status_code= 400, detail="Senha em uso.")
    
    user["password"] = nova_senha

@router.delete("/users/{user_id}")
def delete_user(user_id: str, senha: str):
    pass
