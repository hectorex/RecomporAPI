from uuid import uuid4
from http import HTTPStatus
from dataclasses import asdict

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from API.database import get_session
from API.models.composteira import Composteira
from API.models.user_model import User
from API.schemas.composteira_schema import DadosComposteira
# from API.database.fake_db import bd_composteiras


router =  APIRouter()

@router.post("/criar_composteira")
def criar_composteira(fkUsuario: str,composteira: DadosComposteira, session = Depends(get_session)): #criação da session

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
    
    if composteira.regiao not in ["Norte","Nordeste","Sudeste","Centro-Oeste","Sul"]:
        raise HTTPException(
            status_code=400,
            detail="A regiao inserida é inválido. Insira: Norte, Nordeste, Sul, Sudeste ou Centro-Oeste."
        )

    if composteira.tipo != "Terra" and composteira.tipo != "Caixa":
        raise HTTPException(
            status_code=400,
            detail="O tipo inserido é inválido. Insira: Terra ou Caixa."
        )
    if len(composteira.nome) < 3 and composteira.nome != "   ":
        raise HTTPException(
            status_code=400,
            detail="O nome inserido é inválido. Insira: um valor com pelo menos 3 caracteres. Não insira: 3 espaços em branco."
        )
    if composteira.tamanho != "Pequena" and composteira.tamanho != "Média" and composteira.tamanho != "Grande": #verificando se o tamanho é válido
        raise HTTPException(
            status_code=400,
            detail="O tamanho inserido é inválido, insira: Pequena; Média ou Grande."
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
            (User.id == fkUsuario)
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
        data_construcao= composteira.data_construcao,
        regiao= composteira.regiao,
        tamanho= composteira.tamanho,
        fkUsuario= fkUsuario          
    )
    session.add(db_composteira)
    session.commit()
    session.refresh(db_composteira) # Atualizando o objeto com os dados do banco

    return db_composteira
    
@router.get('/minhas_composteiras/')
def exibir_composteiras(limit: int = 10, offset: int = 0, session: Session = Depends(get_session)):
    composteiras = list(session.scalars(select(Composteira).limit(limit).offset(offset)))
    if len(composteiras) == 0:
        return {"message": "Nenhuma composteira encontrada."}
    else:
        return {"composteiras_table": [asdict(c) for c in composteiras]}
    
@router.get("/minhas_composteiras/{composteira_id}")
def exibir_composteira(composteira_id: str, session: Session = Depends(get_session)):
    db_composteira = session.scalar(select(Composteira).where(Composteira.id_composteira == composteira_id))

    if not db_composteira:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Composteira não encontrada.")

    # composteira = session.scalar(
    # select(Composteira).where(
    #     (Composteira.id_composteira == composteira_id)
    #     )
    # )
    
    return db_composteira

@router.delete("/minhas_composteiras/delete/{id}") #deletar do espaço-tempo uma composteira
def deletar_composteira(id: str, session: Session = Depends(get_session)):
    db_composteira = session.scalar(select(Composteira).where(Composteira.id_composteira == id))

    if not db_composteira:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Composteira não encontrada.")
    
    session.delete(db_composteira)
    session.commit()

    return{'message': 'Composteira deletada.'}


@router.put("/minhas_composteiras/{id}") #editar uma composteira ja existente
def atualizar_composteira(id: str, composteira: DadosComposteira, session: Session = Depends(get_session)):
    db_composteira = session.scalar(select(Composteira).where(Composteira.id_composteira == id))

    if composteira.regiao not in ["Norte","Nordeste","Sudeste","Centro-Oeste","Sul"]:
        raise HTTPException(
            status_code=400,
            detail="A regiao inserida é inválido. Insira: Norte, Nordeste, Sul, Sudeste ou Centro-Oeste."
        )

    elif composteira.tipo not in ["Terra", "Caixa"]:
        raise HTTPException(
            status_code=400,
            detail="O tipo inserido é inválido. Insira: Terra ou Caixa."
        )
    elif len(composteira.nome.strip()) < 3: #strip retira caracteres vazios " "
        raise HTTPException(
            status_code=400,
            detail="O nome inserido é inválido. Insira ao menos 3 caracteres diferentes de espaço."
        )
    elif composteira.tamanho not in ["Pequena","Média","Grande"]: #verificando se o tamanho é válido
        raise HTTPException(
            status_code=400,
            detail="O tamanho inserido é inválido, insira: Pequena, Média ou Grande."
        )

    nome_existente = session.scalar( #consultando se tem uma composteira com mesmo nome no banco
        select(Composteira).where(
            (Composteira.nome == composteira.nome),
            (Composteira.id_composteira != id)
        )
    )

    if nome_existente:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Composteira já existe com esse nome.',
            )

    try:
        db_composteira.nome = composteira.nome
        db_composteira.tipo = composteira.tipo
        db_composteira.minhocas = composteira.minhocas
        db_composteira.data_construcao = composteira.data_construcao
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