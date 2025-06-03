from poetry_recomporapi.models.User import User

def test_create_user(session):
    user = User(
        username="teste",
        email="teste@teste",
        password="secret"
    )

    session.add(user)
    session.commit()

    assert user.username == "teste"