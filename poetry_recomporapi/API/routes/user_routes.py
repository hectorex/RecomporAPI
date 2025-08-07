from uuid import uuid4
from http import HTTPStatus
from dataclasses import asdict

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from API.database import get_session
from API.models.user_model import User
from API.schemas.user_schema import DadosUser, DadosSenha
from API.schemas.token_schema import Token
from API.security import get_password_hash, password_check, verify_password, create_access_token

router = APIRouter()

@router.post("/criar_usuario")
def criar_user(user: DadosUser, session = Depends(get_session)): #criação da session

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
#eu amo o celso
@router.get('/usuarios/') #listar os usuarios
def read_users(limit: int = 10, offset: int = 0, session: Session = Depends(get_session)):
    users = list(session.scalars(select(User).limit(limit).offset(offset)))
    return {"users_table": [asdict(user) for user in users]}


@router.put("/users/{user_id}") #editar um usuario ja existente
def update_user(user_id: str, user: DadosUser, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not password_check(user.password): #verificando segurança da senha
        raise HTTPException(
            status_code=400,
            detail="A senha deve: ter mais que 6 caracteres; " \
                "pelo menos um número; " \
                "pelo menos uma letra maiúscula e uma minúscula; " \
                "pelo menos um caracter especial.",
            )

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

@router.delete("/users/delete/{user_id}") #deletar do espaço-tempo um user
def delete_user(user_id: str, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado.")
    
    session.delete(db_user)
    session.commit()

    return{'message': 'Usuário deletado.'}

@router.post("/token/", response_model=Token) #autenticação e autorização de usuários / pode ser usado '/login' tb
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
    
    access_token = create_access_token(
        {"": db_user.username}
    )
    return {"access_token": access_token, "token_type": "Bearer"}