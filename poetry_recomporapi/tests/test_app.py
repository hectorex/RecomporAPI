from http import HTTPStatus

from API.schemas.user_schema import DadosUser

def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.username, 'password': user.password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token