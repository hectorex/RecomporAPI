from dataclasses import asdict
from sqlalchemy import select
from sqlalchemy.orm.session import Session
from API.models.user import User
from API.models.compostagem import Compostagem
from API.models.composteira import Composteira
from datetime import datetime

def test_create_user(session): #Esse user aqui não será acessado pois ele "sumirá" --
    # -- quando a função debaixo (da composteira) rodar
    #ou seja, é melhor testar tudo em uma função só!
    #já podemos apagar aqui e testar tudo apenas na função debaixo
    #lá conseguimos verificar o user e a composteira!

    #apagar aqui e deixar só a função debaixo (com um nome generico, como testes objetos) dps
    new_user = User(           
        username="teste",
        email="teste@teste",
        password="secret"
    )

    session.add(new_user)
    session.commit()

    
    user = session.scalar(
        select(User).where(User.username == "teste") #estudar melhor dps
    )

    assert user.id == 1
    assert user.username == "teste"
    assert user.email == "teste@teste"
    assert user.password == "secret"
    assert isinstance(user.created_at, datetime) #consertar o horario dps, tem que usar o horario do db

'''    assert asdict(user) == { #isso aqui vai servir para configurar a hora do db, configurar apos o celso terminar
        "id": 1,
        "username": "teste",
        "email": "teste@teste", 
        "password": "secret",
        "created_at": time #esse time vai consertar isso, mas preciso arrumar o conftest
    }'''

def test_create_composteira(session: Session):
    new_user2 = User( #criando user só para conseguir testar a composteira
        username="teste1",
        email="teste@teste",
        password="secret"
    )

    session.add(new_user2)
    session.commit()

    
    user2 = session.scalar(
        select(User).where(User.username == "teste1") #estudar melhor dps
    )

    assert user2.id == 1
    assert user2.username == "teste1"
    assert user2.email == "teste@teste"
    assert user2.password == "secret"
    assert isinstance(user2.created_at, datetime)
    new_composteira = Composteira(
        nome="Compostilson",
        tipo="Terra",
        minhocas=True,
        data_constru= "30/10/2007",
        regiao="Sul",
        tamanho= 30.0,
        user_id= new_user2.id,
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
    assert composteira.user_id == new_user2.id

