from dataclasses import asdict
from sqlalchemy import select
from sqlalchemy.orm.session import Session
from API.models.User import User

def test_create_user(session: Session):
    new_user = User(
        username="teste",
        email="teste@teste",
        password="secret"
    )

    session.add(new_user)
    session.commit()

    breakpoint()
    user = session.scalar(
        select(User).where(User.username == "teste") #estudar melhor dps
    )

    assert asdict(user) == {
        "id": 1,
        "username": "test",
        "email": "test@test",
        "password": "secret",
        "created_at": ...
    }