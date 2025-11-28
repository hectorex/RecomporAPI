from uuid import uuid4
from http import HTTPStatus
from dataclasses import asdict

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from API.database.database import get_session
from API.models.user_model import User
from API.schemas.user_schema import DadosUser, DadosSenha
from API.schemas.token_schema import Token
from API.security import get_password_hash, password_check, verify_password, username_check

router = APIRouter()

@router.post("/users") #criar user
def criar_user(user: DadosUser, session = Depends(get_session)): #criação da session

    if not username_check(user.username): #verificando o usarname
        raise HTTPException(
            status_code=400,
            detail="O username deve ter pelo menos cinco caracteres; Deve começar com uma letra e deve conter somente letras e números (sem espaços e caracteres especiais)."
        )
    if not password_check(user.password): #verificando segurança da senha
        raise HTTPException(
            status_code=400,
            detail="A senha deve: ter mais que 6 caracteres; " \
                "pelo menos um número; " \
                "pelo menos uma letra maiúscula e uma minúscula; " \
                "pelo menos um caracter especial.",
            )
    db_user = session.scalar( #buscando os dados
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        ) 
    )

    if db_user:  #se tiver user com mesmo nome ou email:
        if db_user.username == user.username: #verificação se já existe o usarname
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Username já exite",
            )
        if db_user.email == user.email: #verificação se já existe o email
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Email já existe",
            )


    db_user = User( #definindo
        username=user.username, password=get_password_hash(user.password), email=user.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

@router.get("/users/{user_id}") #consultar um user
def exibir_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado.")

    user = session.scalar(
    select(User).where(
        (User.id == user_id)
        )
    )

    return user


@router.get("/users") #listar os usuarios
def exibir_users(limit: int = 10, offset: int = 0, session: Session = Depends(get_session)):
    users = list(session.scalars(select(User).limit(limit).offset(offset)))
    if len(users) == 0: #verificando se a tabela de users está vazia
        return {"message": "Nenhum usuário encontrado."}
    else:
        return {"users_table": [asdict(user) for user in users]}


@router.put("/users/{user_id}") #editar um usuario ja existente
def atualizar_user(user_id: int, user: DadosUser, session: Session = Depends(get_session)):
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
def deletar_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado.")
    
    session.delete(db_user)
    session.commit()

    return{'message': 'Usuário deletado.'}

@router.post("/token/", response_model=Token) #em desenvolvimento by luiz felipe
#autenticação e autorização de usuários / pode ser usado '/login' tb
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), #dunossauro disse: 'é estranho mesmo!'
    session: Session = Depends(get_session)
):
    db_user = session.scalar(
        select(User).where(User.username == form_data.username)
    )

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Email ou senha incorretos."
        )

    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Email ou senha incorretos."
        )