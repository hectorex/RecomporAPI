from dataclasses import asdict
from sqlalchemy import select
from sqlalchemy.orm.session import Session
from API.models.user import User
from API.models.compostagem import Compostagem
from API.models.composteira import Composteira
from datetime import datetime

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
    
    assert user.id == 1
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
    breakpoint()
    assert composteira.id == 1
    assert composteira.tipo == "Terra"
    assert composteira.minhocas == True
    assert composteira.data_constru == "30/10/2007"
    assert composteira.regiao == "Sul"
    assert composteira.tamanho == 30.0
    assert composteira.user_id == new_user.id

