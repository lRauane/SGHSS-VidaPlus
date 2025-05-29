from http import HTTPStatus


def test_get_token_paciente(client, paciente_user):
    response = client.post(
        '/auth/token',
        data={
            'username': paciente_user.email,
            'password': paciente_user.clean_password,
        },
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_get_token_profissional(client, profissional_user):
    response = client.post(
        '/auth/token',
        data={
            'username': profissional_user.email,
            'password': profissional_user.clean_password,
        },
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token
