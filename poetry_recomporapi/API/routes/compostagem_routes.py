from uuid import uuid4
from http import HTTPStatus
from datetime import datetime
from dataclasses import asdict

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from API.database import get_session
from API.models.compostagem import Compostagem
from API.models.composteira import Composteira
from API.schemas.compostagem_schema import DadosCompostagem


router =  APIRouter()

@router.post("/minhas_composteiras/{composteira_id}/criar_compostagem") # criar compostagem
async def criar_compostagem(composteira_id: str, compostagem: DadosCompostagem, session = Depends(get_session)): #criação da session

    db_composteira = session.scalar(
    select(Composteira).where(Composteira.id == composteira_id)
)
    if not db_composteira:
        raise HTTPException(
            status_code=404, 
            detail="Composteira não encontrada."
            )
    
    if len(compostagem.nome) < 3 and compostagem.nome != "   ":
        raise HTTPException(
            status_code=400,
            detail="Valor inválido. Insira: um valor com pelo menos 3 caracteres."
        )
    
    if not compostagem.quantReduo > 0:
        raise HTTPException( #verificando se a quantReduo possui valor válido
            status_code=400,
            detail="Valor inválido. Insira: um valor maior que 0."
        )
    if compostagem.frequencia.capitalize() not in ["Diaria","Semanal","Mensal"]:
        raise HTTPException( #verificando se frequencia é válida
            status_code=400, 
            detail="Valor inválido. Insira: Diaria, Semanal ou Mensal (sem acento)."
            )

        
    db_compostagem = session.scalar(
        select(Compostagem).where(
            (Compostagem.nome == compostagem.nome )
        )
    )
    if db_compostagem:
        raise HTTPException( #verificando se o nome existe no db
            status_code=HTTPStatus.CONFLICT, 
            detail="Valor inválido. Nome já existente"
            )
    
    db_compostagem = Compostagem( # Instanciando objeto da classe compostagem
        nome= compostagem.nome,
        data_compostagem= compostagem.data_compostagem,
        quantReduo= compostagem.quantReduo,
        frequencia= compostagem.frequencia,
        previsao= compostagem.previsao,
        composteira_id = composteira_id
    )
    session.add(db_compostagem)
    session.commit()
    session.refresh(db_compostagem)

    return db_compostagem

@router.get('/minhas_composteiras/{composteira_id}/minhas_compostagens') #listando compostagens
def get_compostagens(limit: int = 10, offset: int = 0, session: Session = Depends(get_session)):
    compostagens = list(session.scalars(select(Compostagem).limit(limit).offset(offset)))
    if len(compostagens) == 0: #verificando se a tabela de compostagens está vazia
        return {"message": "Nenhuma composteira encontrada."}
    else:
        return {"compostagens_table": [asdict(c) for c in compostagens]}

@router.delete("/minhas_composteiras/{composteira_id}/minhas_compostagens/{id}") #deletar do espaço-tempo uma compostagem
def delete_compostagem(id: str, session: Session = Depends(get_session)):
    db_compostagem = session.scalar(select(Compostagem).where(Compostagem.id == id))

    if not db_compostagem:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Compostagem não encontrada.")
    
    session.delete(db_compostagem)
    session.commit()

    return{'message': 'Compostagem deletada.'}


@router.put("/minhas_composteiras/{composteira_id}/minhas_compostagens/{id}") #editar uma composteira ja existente
def update_compostagem(id: str, compostagem: DadosCompostagem, session: Session = Depends(get_session)):
    db_compostagem = session.scalar(select(Compostagem).where(Compostagem.id == id))
    
    if len(compostagem.nome) < 3 and compostagem.nome != "   ":
        raise HTTPException(
            status_code=400,
            detail="Valor inválido. Insira: um valor com pelo menos 3 caracteres."
        )
    
    if not compostagem.quantReduo > 0:
        raise HTTPException( #verificando se a quantReduo possui valor válido
            status_code=400,
            detail="Valor inválido. Insira: um valor maior que 0."
        )
    if compostagem.frequencia.capitalize() not in ["Diaria","Semanal","Mensal"]:
        raise HTTPException( #verificando se frequencia é válida
            status_code=400, 
            detail="Valor inválido. Insira: Diaria, Semanal ou Mensal (sem acento)."
            )

        
    db_compostagem = session.scalar(
        select(Compostagem).where(
            (Compostagem.nome == compostagem.nome )
        )
    )
    if db_compostagem:
        raise HTTPException( #verificando se o nome existe no db
            status_code=HTTPStatus.CONFLICT, 
            detail="Valor inválido. Nome já existente"
            )  

    if not db_compostagem:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Compostagem não encontrada.")

    try:
        db_compostagem.nome = compostagem.nome
        db_compostagem.data_compostagem = compostagem.data_compostagem
        db_compostagem.quantReduo = compostagem.quantReduo
        db_compostagem.frequencia = compostagem.frequencia
        db_compostagem.previsao = compostagem.previsao



        session.add(db_compostagem)
        session.commit()
        session.refresh(db_compostagem)
        
        return db_compostagem
    
    except IntegrityError:
        raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Compostagem já existente.',
            )