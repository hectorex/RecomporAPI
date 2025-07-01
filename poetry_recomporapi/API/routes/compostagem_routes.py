from fastapi import APIRouter, HTTPException
from API.schemas.compostagem_schema import DadosCompostagem
from API.database.fake_db import bd_compostagens, bd_composteiras
from uuid import uuid4
from sqlalchemy.orm import Session
from API.settings import Settings
from sqlalchemy import create_engine, select
from API.models.compostagem import Compostagem
from http import HTTPStatus
from API.models.composteira import Composteira


router =  APIRouter()

@router.post("/minhas_composteiras/{composteira_id}/criar_compostagem") # criar compostagem
async def criar_compostagem(composteira_id: str, compostagem: DadosCompostagem):
    engine = create_engine(Settings().DATABASE_URL)
    session = Session(engine)

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

@router.get("/minhas_composteiras/{composteira_id}/minhas_compostagens")
async def listar_compostagens():
    return [(compostagem) for compostagem in bd_compostagens]