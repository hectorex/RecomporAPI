from fastapi import APIRouter, HTTPException, Depends
from API.schemas.composteira_schema import DadosComposteira
#from API.database.fake_db import bd_composteiras
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from API.models.composteira import Composteira
from http import HTTPStatus
from API.models.user_model import User
from API.database import get_session
from dataclasses import asdict
from sqlalchemy.orm import Session

router =  APIRouter()

@router.post("/criar_composteira")
def criar_composteira(user_id: str,composteira: DadosComposteira, session = Depends(get_session)): #criação da session

    # Verificação Minhocas e retorno de String
    # Vai dar erro, porque mesmo que verifiquemos se é True ou False e 
    # dai atribuimos a devida string, 
    # o banco estará esperando um Boolean.
    # if composteira.minhocas == True:
    #     composteira.minhocas = "Sim"
    # elif composteira.minhocas == False:
    #     composteira.minhocas = "Não"

    # else:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="A inserção é inválida, insira True para sim e False para não"
    #     )
    
    if len(composteira.nome) < 3 and composteira.nome != "   ":
        raise HTTPException(
            status_code=400,
            detail="Valor inválido. Insira: um valor com pelo menos 3 caracteres. Não insira: 3 espaços em branco."
        )
    if composteira.tamanho <= 0: #verificando se o tamanho é válido
        raise HTTPException(
            status_code=400,
            detail="O tamanho inserido é inválido, insira um número maior que 0."
        )

    db_composteira = session.scalar( #consultando se tem uma composteira com mesmo nome no banco
        select(Composteira).where(
            (Composteira.nome == composteira.nome)
        )
    )

    if db_composteira:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Composteira já existe com esse nome.',
            )

        
    db_user = session.scalar( #verificando se o id informado existe no banco
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

@router.delete("/minhas_composteiras/delete/{id}") #deletar do espaço-tempo uma composteira
def delete_composteira(id: str, session: Session = Depends(get_session)):
    db_composteira = session.scalar(select(Composteira).where(Composteira.id == id))

    if not db_composteira:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Composteira não encontrada.")
    
    session.delete(db_composteira)
    session.commit()

    return{'message': 'Composteira deletada.'}


@router.put("/minhas_composteiras/{id}") #editar uma composteira ja existente
def update_composteira(id: str, composteira: DadosComposteira, session: Session = Depends(get_session)):
    db_composteira = session.scalar(select(Composteira).where(Composteira.id == id))

    if not db_composteira:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Composteira não encontrada.")

    try:
        db_composteira.nome = composteira.nome
        db_composteira.tipo = composteira.tipo
        db_composteira.minhocas = composteira.minhocas
        db_composteira.data_constru = composteira.data_constru
        db_composteira.regiao = composteira.regiao
        db_composteira.tamanho = composteira.tamanho


        session.add(db_composteira)
        session.commit()
        session.refresh(db_composteira)
        
        return db_composteira
    
    except IntegrityError:
        raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Composteira já existente.',
            )