from fastapi import APIRouter, HTTPException, Depends
from API.schemas.compostagem_schema import DadosCompostagem
#from API.database.fake_db import bd_compostagens, bd_composteiras
from uuid import uuid4
from sqlalchemy import select
from API.models.compostagem import Compostagem
from http import HTTPStatus
from API.models.composteira import Composteira
from API.database import get_session
from dataclasses import asdict
from sqlalchemy.orm import Session
from datetime import datetime


router =  APIRouter()

@router.post("/minhas_composteiras/{composteira_id}/criar_compostagem") # criar compostagem
async def criar_compostagem(composteira_id: str, compostagem: DadosCompostagem, session = Depends(get_session)): #criação da session

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
            detail="Nome já existente"
            )
    
    db_composteira = session.scalar(
    select(Composteira).where(Composteira.id == composteira_id)
)
    if not db_composteira:
        raise HTTPException(
            status_code=404, 
            detail="Composteira não encontrada."
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

@router.get('/minhas_composteiras/{composteira_id}/minhas_compostagens')
def get_compostagens(limit: int = 10, offset: int = 0, session: Session = Depends(get_session)):
    compostagens = list(session.scalars(select(Compostagem).limit(limit).offset(offset)))
    return {"compostagens_table": [asdict(c) for c in compostagens]}

'''
    composteira = next(((composteira) for composteira in bd_composteiras if composteira["id"] == composteira_id), None)
    # Procuramos a primeira composteira cujo ID bate com o fornecido; se não houver, retornamos None
    if composteira:
        raise HTTPException(status_code=404, detail="A composteira em questão não foi encontrada.")
    
    dados = compostagem.model_dump()

    frequencia_valida = {"diária", "semanal", "mensal"}
    if dados["frequencia"].lower() not in frequencia_valida:
        raise HTTPException(status_code=400, detail="Frequência inválida - escreva: 'diária', 'semanal' ou 'mensal'.")

    dados["id"] = str(uuid4())
    dados["composteira_id"] = composteira_id
    bd_compostagens.append(dados)

    return{
        "mensagem": f"Compostagem adicionada à composteira '{composteira['nome']}'.",
        "detalhes": dados
    } '''

'''@router.get("/minhas_composteiras/{composteira_id}/minhas_compostagens")
async def listar_compostagens():
    return [(compostagem) for compostagem in bd_compostagens]'''