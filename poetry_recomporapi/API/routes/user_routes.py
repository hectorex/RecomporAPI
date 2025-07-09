from fastapi import APIRouter, HTTPException, Depends
from API.schemas.user_schema import DadosUser, DadosSenha
from uuid import uuid4
from API.security import get_password_hash, password_check
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from API.models.user_model import User
from http import HTTPStatus
from API.database import get_session
from sqlalchemy.orm import Session
from dataclasses import asdict

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
                detail='Email já existe',
            )

    db_user = User( #definindo
        username=user.username, password=get_password_hash(user.password), email=user.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

@router.get('/usuarios/') #listar os usuarios
def read_users(limit: int = 10, offset: int = 0, session: Session = Depends(get_session)):
    users = list(session.scalars(select(User).limit(limit).offset(offset)))
    return {"users_table": [asdict(user) for user in users]}


@router.put("/users/{user_id}") #editar um usuario ja existente
def update_user(user_id: str, user: DadosUser, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado.")

    try:
        db_user.email = user.email
        db_user.username = user.username
        db_user.password = get_password_hash(user.password)

        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        
        return db_user
    
    except IntegrityError:
        raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username ou Email já existem.',
            )

@router.delete("/users/{user_id}") #deletar do espaço-tempo um user
def update_user(user_id: str, user: DadosUser, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado.")
    
    session.delete(db_user)
    session.commit()

    return{'message': 'Usuário deletado.'}