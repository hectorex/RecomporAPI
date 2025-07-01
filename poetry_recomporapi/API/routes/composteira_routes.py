from fastapi import APIRouter, HTTPException
from API.schemas.composteira_schema import DadosComposteira
from API.database.fake_db import bd_composteiras
from uuid import uuid4
from sqlalchemy.orm import Session
from API.settings import Settings
from sqlalchemy import create_engine, select
from API.models.composteira import Composteira
from http import HTTPStatus
from API.models.user_model import User

router =  APIRouter()

@router.post("/criar_composteira")
def criar_composteira(user_id: str,composteira: DadosComposteira):
    engine = create_engine(Settings().DATABASE_URL)
    session = Session(engine)

    db_composteira = session.scalar(
        select(Composteira).where(
            (Composteira.nome == composteira.nome)
        )
    )

    if not db_composteira:
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
    
@router.get("/minhas_composteiras")
async def listar_composteiras():
    if len(bd_composteiras) >= 1:
        ret = ((composteira) for composteira in bd_composteiras)
    else:
        ret = {"resposta": "você não tem composteiras criadas."}

    return ret