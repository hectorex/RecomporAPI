from fastapi import APIRouter, HTTPException
from API.schemas.compostagem_schema import DadosCompostagem
from API.database.fake_db import bd_compostagens, bd_composteiras
from uuid import uuid4

router =  APIRouter()

@router.post("/minhas_composteiras/{composteira_id}/criar_compostagem") # criar compostagem
async def criar_compostagem(composteira_id: str, compostagem: DadosCompostagem):
    composteira = next(((composteira) for composteira in bd_composteiras if composteira["id"] == composteira_id), None)
    # Procuramos a primeira composteira cujo ID bate com o fornecido; se não houver, retornamos None
    if not composteira:
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
    }

@router.get("/minhas_composteiras/{composteira_id}/minhas_compostagens")
async def listar_compostagens():
    return [(compostagem) for compostagem in bd_compostagens]