from fastapi import APIRouter
from schemas.composteira_schema import DadosComposteira
from database.fake_db import bd_composteiras
from uuid import uuid4

router =  APIRouter()

@router.post("/criar_composteira")
def criar_composteira(composteira: DadosComposteira):
    dados = composteira.model_dump()
    dados["id"] = str(uuid4())
    dados["minhocas"] = "Tem minhocas" if composteira.minhocas else "Não tem minhocas"
    bd_composteiras.append(dados)
    return {
        "mensagem": f"Composteira '{dados["nome"]}' criada com sucesso!",
        "detalhes": dados
    }
@router.get("/minhas_composteiras")
async def listar_composteiras():
    if len(bd_composteiras) >= 1:
        ret = ((composteira) for composteira in bd_composteiras)
    else:
        ret = {"resposta": "você não tem composteiras criadas."}

    return ret