from fastapi import APIRouter, HTTPException, Depends
from API.schemas.user_schema import DadosUser, DadosSenha
#from API.database.fake_db import bd_users
from uuid import uuid4
from API.segurança import get_password_hash, password_check
from sqlalchemy import select
from API.models.user_model import User
from http import HTTPStatus
from API.database import get_session

router = APIRouter()

@router.post("/criar_usuario")
def criar_user(user: DadosUser, session = Depends(get_session)): #criação da session

    db_user = session.scalar( #buscando os dados
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        ) 
    )

    if db_user:
        if db_user.username == user.username: #verificação
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username já exite',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already exists',
            )

    db_user = User( #definindo
        username=user.username, password=user.password, email=user.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

'''@router.put("/users/{user_id}")
def edit_user(user_id: str, nova_senha: DadosSenha):
    user = next(((user) for user in bd_users if user_id == user["id"]), None)
    if not user:
        return HTTPException(status_code= 404, detail="O usuário em questão não foi encontrado.")
    elif nova_senha == user["password"]:
        return HTTPException(status_code= 400, detail="Senha em uso.")
    
    user["password"] = nova_senha #corrigir o hash dps

    return {
        "status": f"senha atualizada com sucesso! senha: {user["password"]}"
    }'''

@router.delete("/users/{user_id}")
def delete_user(user_id: str, senha: str):
    pass