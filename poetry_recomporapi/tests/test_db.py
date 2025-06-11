from dataclasses import asdict
from sqlalchemy import select
from sqlalchemy.orm.session import Session
from API.models.user import User
from API.models.compostagem import Compostagem
from API.models.composteira import Composteira
from datetime import datetime

def test_create_user(session: Session):
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
    breakpoint()

    assert user.id == 1
    assert user.username == "teste"
    assert user.email == "teste@teste"
    assert user.password == "secret"
    assert isinstance(user.created_at, datetime)
    # assert asdict(user) == {
    #     "id": 1,
    #     "username": "teste",
    #     "email": "test@test",
    #     "password": "secret",
    #     "created_at": ...
    # }

# def test_create_composteira(session):
#     new_composteira