from fastapi import APIRouter, HTTPException, Depends
from API.schemas.composteira_schema import DadosComposteira
#from API.database.fake_db import bd_composteiras
from uuid import uuid4
from sqlalchemy import select
from API.models.composteira import Composteira
from http import HTTPStatus
from API.models.user_model import User
from API.database import get_session
from dataclasses import asdict
from sqlalchemy.orm import Session

router =  APIRouter()

@router.post("/criar_composteira")
def criar_composteira(user_id: str,composteira: DadosComposteira, session = Depends(get_session)): #criação da session

    db_composteira = session.scalar(
        select(Composteira).where(
            (Composteira.nome == composteira.nome)
        )
    )

    if db_composteira:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Composteira já existe com esse nome.',
            )
        
    
    db_user = session.scalar(
        select(User).where(
            (User.id == user_id)
        )
    )
    if not db_user:
         raise HTTPException(
            status_code=404,
            detail="User não encontrado."
         )

    db_composteira = Composteira( # Instanciando um objeto da classe Composteira
        nome=composteira.nome,
        tipo= composteira.tipo,
        minhocas= composteira.minhocas,
        data_constru= composteira.data_constru,
        regiao= composteira.regiao,
        tamanho= composteira.tamanho,
        user_id= user_id          
    )
    session.add(db_composteira)
    session.commit()
    session.refresh(db_composteira) # Atualizando o objeto com os dados do banco

    return db_composteira
    
@router.get('/minhas_composteiras/')
def get_composteiras(limit: int = 10, offset: int = 0, session: Session = Depends(get_session)):
    composteiras = list(session.scalars(select(Composteira).limit(limit).offset(offset)))
    return {"composteiras_table": [asdict(c) for c in composteiras]}