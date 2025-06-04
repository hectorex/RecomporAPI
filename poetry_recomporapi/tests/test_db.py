from sqlalchemy import select
from API.models.User import User

def test_create_user(session):
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

    assert user.username == {
        "username": "test",
        "email": "test@test",
        "password": "secret"
    }