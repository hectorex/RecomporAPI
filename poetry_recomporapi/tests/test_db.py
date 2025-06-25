from dataclasses import asdict
from sqlalchemy import select
from sqlalchemy.orm.session import Session
from API.models.user_model import User
from API.models.compostagem import Compostagem
from API.models.composteira import Composteira
from datetime import datetime
from API.schemas.compostagem_schema import calculo_previsao
from API.segurança import gerando_uuid4
from uuid import UUID

def test_create(session: Session):
    #create_user
    new_user = User( 
        username="Luiz Felipe",
        email="luizfelipemam2007@gmail.com",
        password="C&L123"
    )

    session.add(new_user)
    session.commit()
    
    user = session.scalar(
        select(User).where(User.username == "Luiz Felipe") #estudar melhor dps
    )
    
    UUID(user.id)
    assert user.username == "Luiz Felipe"
    assert user.email == "luizfelipemam2007@gmail.com"
    assert user.password == "C&L123"
    assert isinstance(user.created_at, datetime)
    
    #create_composteira
    new_composteira = Composteira( 
        nome="Compostilson",
        tipo="Terra",
        minhocas=True,
        data_constru= "30/10/2007",
        regiao="Sul",
        tamanho= 30.0,
        user_id= new_user.id,
    )

    session.add(new_composteira)
    session.commit()

    composteira = session.scalar(
        select(Composteira).where(Composteira.nome == "Compostilson")
    )

    UUID(composteira.id)
    assert composteira.tipo == "Terra"
    assert composteira.minhocas == True
    assert composteira.data_constru == "30/10/2007"
    assert composteira.regiao == "Sul"
    assert composteira.tamanho == 30.0
    assert composteira.user_id == new_user.id

    #create_compostagem
    new_compostagem = Compostagem(
        nome="Compostagem Top",
        data_compostagem="16/06/2025",
        quantReduo=10.0,
        frequencia="Diária",
        previsao= calculo_previsao(10.0),
        composteira_id= new_composteira.id
    )

    session.add(new_compostagem)
    session.commit()

    compostagem =  session.scalar(
        select(Compostagem).where(Compostagem.nome == "Compostagem Top")
    )

    
    breakpoint()

    UUID(compostagem.id)
    assert compostagem.nome == "Compostagem Top"
    assert compostagem.data_compostagem == "16/06/2025"
    assert compostagem.quantReduo == 10.0
    assert compostagem.previsao == (calculo_previsao(new_compostagem.quantReduo))
    assert compostagem.composteira_id == new_composteira.id