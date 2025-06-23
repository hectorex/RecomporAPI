from fastapi import APIRouter, HTTPException
from API.schemas.user_schema import DadosUser, DadosSenha
from API.database.fake_db import bd_users
from uuid import uuid4
from API.segurança import get_password_hash, password_check
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from API.settings import Settings
from API.models.user_model import User
from http import HTTPStatus

router = APIRouter()

@router.post("/criar_usuario")
def criar_user(user: DadosUser):
    engine = create_engine(Settings().DATABASE_URL)
    session = Session(engine)

    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        ) 
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already exists',
            )

    db_user = User(
        username=user.username, password=user.password, email=user.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

    '''dados = user.model_dump()
    dados["id"] = str(uuid4())
    if password_check(dados["password"]) == False:
        return {"mensagem": "Senha inválida.",
                "requisitos":"Deve conter de 6 a 20 digítos; "
                             "Deve possuir pelo menos um número;"
                             "Deve possuir pelo menos uma letra minúscula e uma maiúscula;"
                             "Deve possuir um caracter especial."
        } 
    dados["password"] = get_password_hash(user.password)
    bd_users.append(dados)
    return {
        "mensagem": f"Bem-vindo, {dados["username"]}, {dados["id"]}, {dados['password']}."
    }'''
@router.put("/users/{user_id}")
def edit_user(user_id: str, nova_senha: DadosSenha):
    user = next(((user) for user in bd_users if user_id == user["id"]), None)
    if not user:
        return HTTPException(status_code= 404, detail="O usuário em questão não foi encontrado.")
    elif nova_senha == user["password"]:
        return HTTPException(status_code= 400, detail="Senha em uso.")
    
    user["password"] = nova_senha #corrigir o hash dps

    return {
        "status": f"senha atualizada com sucesso! senha: {user["password"]}"
    }

@router.delete("/users/{user_id}")
def delete_user(user_id: str, senha: str):
    pass