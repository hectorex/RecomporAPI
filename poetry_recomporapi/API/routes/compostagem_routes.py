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
from API.schemas.compostagem_schema import DadosCompostagem, calculo_previsao, DadosCompostagemRetorno


router =  APIRouter()

@router.post("/minhas_composteiras/{composteira_id}/criar_compostagem", response_model= DadosCompostagemRetorno) # criar compostagem -- definindo qual será a "classe" retornada (já com previsao)
async def criar_compostagem(fkUsuario: str, fkComposteira: str, compostagem: DadosCompostagem, session = Depends(get_session)): #criação da session

    db_composteira = session.scalar(
    select(Composteira).where(Composteira.id == fkComposteira)
)
    if not db_composteira:
        raise HTTPException(
            status_code=404, 
            detail="Composteira não encontrada."
            )
    
    if not compostagem.peso > 0:
        raise HTTPException( #verificando se a quantReduo possui valor válido
            status_code=400,
            detail="O peso inserido é inválido. Insira: um valor maior que 0."
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
    previsao_calculada = calculo_previsao(compostagem.quantReduo)
    db_compostagem = Compostagem( # Instanciando objeto da classe compostagem
        data_inicio= compostagem.data_inicio,
        peso= compostagem.peso,
        frequencia= compostagem.frequencia,
        #data_pronto= previsao_calculada,
        fkComposteira = fkComposteira,
        fkUsuario = fkUsuario,
    )
    session.add(db_compostagem)
    session.commit()
    session.refresh(db_compostagem)

    return db_compostagem

@router.get('/minhas_composteiras/{composteira_id}/minhas_compostagens/{id_compostagem}')
def exibir_Compostagem(id_compostagem: str, session: Session = Depends(get_session)):
    db_compostagem = session.scalar(select(Compostagem).where(Compostagem.id == id_compostagem))

    if not db_compostagem:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Compostagem não encontrada.")
    
    compostagem = session.scalar(
    select(Compostagem).where(
        (Compostagem.id == id_compostagem)
        )
    )
    
    return compostagem


@router.get('/minhas_composteiras/{composteira_id}/minhas_compostagens') #listando compostagens
def exibir_compostagens(limit: int = 10, offset: int = 0, session: Session = Depends(get_session)):
    compostagens = list(session.scalars(select(Compostagem).limit(limit).offset(offset)))
    if len(compostagens) == 0: #verificando se a tabela de compostagens está vazia
        return {"message": "Nenhuma compostagem encontrada."}
    else:
        return {"compostagens_table": [asdict(c) for c in compostagens]}

@router.delete("/minhas_composteiras/{composteira_id}/minhas_compostagens/{id}") #deletar do espaço-tempo uma compostagem
def deletar_compostagem(id_compostagem: str, session: Session = Depends(get_session)):
    db_compostagem = session.scalar(select(Compostagem).where(Compostagem.id == id))

    if not db_compostagem:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Compostagem não encontrada.")
    
    session.delete(db_compostagem)
    session.commit()

    return{'message': 'Compostagem deletada.'}


@router.put("/minhas_composteiras/{composteira_id}/minhas_compostagens/{id}") #editar uma compostagem ja existente
def atualizar_compostagem(id_compostagem: str, compostagem: DadosCompostagem, session: Session = Depends(get_session)):
    db_compostagem = session.scalar(select(Compostagem).where(Compostagem.id == id))
    
    
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

        

    if not db_compostagem:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Compostagem não encontrada.")

    try:
        db_compostagem.data_inicio = compostagem.data_inicio
        db_compostagem.peso = compostagem.peso
        db_compostagem.frequencia = compostagem.frequencia
        db_compostagem.data_pronto = compostagem.data_pronto



        session.add(db_compostagem)
        session.commit()
        session.refresh(db_compostagem)
        
        return db_compostagem
    
    except IntegrityError:
        raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Compostagem já existente.',
            )