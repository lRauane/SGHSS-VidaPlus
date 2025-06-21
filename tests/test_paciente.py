from http import HTTPStatus

from vidaplus.schemas.paciente_schema import PacienteUserPublic


def test_create_paciente(client, token_admin):
    response = client.post(
        '/pacientes/',
        json={
            'nome': 'Alice Silva',
            'email': 'alice@example.com',
            'senha': 'secret',
            'telefone': '123456789',
            'cpf': '123.456.789-00',
            'data_nascimento': '2002-01-01',
            'endereco': 'Rua Exemplo, 123',
            'complemento': 'Apto 101',
            'numero': 123,
            'bairro': 'Centro',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'cep': '12345-678',
            'tipo': 'PACIENTE',
            'is_active': True,
            'is_superuser': False,
        },
        headers={'Authorization': f'Bearer {token_admin}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 2,
        'nome': 'Alice Silva',
        'email': 'alice@example.com',
        'telefone': '123456789',
        'cpf': '123.456.789-00',
        'data_nascimento': '2002-01-01',
        'endereco': 'Rua Exemplo, 123',
        'complemento': 'Apto 101',
        'numero': 123,
        'bairro': 'Centro',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'cep': '12345-678',
        'tipo': 'PACIENTE',
        'is_active': True,
        'is_superuser': False,
    }


def test_read_paciente(client, token_admin):
    response = client.get('/pacientes/', headers={'Authorization': f'Bearer {token_admin}'})
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'pacientes': []}


def test_read_pacientes_with_pacientes(client, paciente_user, token_admin):
    user_schema = PacienteUserPublic.model_validate(paciente_user).model_dump(
        mode='json'
    )

    response = client.get('/pacientes/', headers={'Authorization': f'Bearer {token_admin}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'pacientes': [user_schema]}


def test_get_paciente_not_found(client, token_pacient):
    response = client.get('/pacientes/999', headers={'Authorization': f'Bearer {token_pacient}'})
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_integrity_error(client, paciente_user, token_pacient, token_admin):
    client.post(
        '/pacientes',
        json={
            'nome': 'Fausto',
            'email': 'fausto@email.com',
            'senha': 'secret',
            'telefone': '123456789',
            'cpf': '987.654.321-00',
            'data_nascimento': '2002-01-01',
            'endereco': 'Rua Exemplo, 123',
            'complemento': 'Apto 101',
            'numero': 123,
            'bairro': 'Centro',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'cep': '12345-678',
            'tipo': 'PACIENTE',
            'is_active': True,
            'is_superuser': False,
        },
        headers={'Authorization': f'Bearer {token_admin}'},
    )

    response_update = client.put(
        f'/pacientes/{paciente_user.id}',
        headers={'Authorization': f'Bearer {token_pacient}'},
        json={
            'nome': 'Fausto Example',
            'email': 'fausto@email.com',
            'senha': 'secret',
            'telefone': '123456789',
            'cpf': '123.223.789-00',
            'data_nascimento': '2002-01-01',
            'endereco': 'Rua Exemplo, 123',
            'complemento': 'Apto 101',
            'numero': 123,
            'bairro': 'Centro',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'cep': '12345-678',
            'tipo': 'PACIENTE',
            'is_active': True,
            'is_superuser': False,
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {'detail': 'CPF or Email already exists'}


# esse teste precisa ser corrigido
def test_update_user_not_found(client, token_pacient):
    response = client.put(
        '/pacientes/999',
        headers={'Authorization': f'Bearer {token_pacient}'},
        json={
            'nome': 'Fausto Example',
            'email': 'fausto@email.com',
            'senha': 'secret',
            'telefone': '123456789',
            'cpf': '123.223.789-00',
            'data_nascimento': '2002-01-01',
            'endereco': 'Rua Exemplo, 123',
            'complemento': 'Apto 101',
            'numero': 123,
            'bairro': 'Centro',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'cep': '12345-678',
            'tipo': 'PACIENTE',
            'is_active': True,
            'is_superuser': False,
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': 'Você não tem permissão para atualizar este usuário'
    }


def test_delete_user(client, paciente_user, token_pacient):
    response = client.delete(
        f'/pacientes/{paciente_user.id}',
        headers={'Authorization': f'Bearer {token_pacient}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


# esse teste precisa ser corrigido
def test_delete_user_wrong_user(client, token_pacient):
    response = client.delete(
        '/pacientes/99',
        headers={'Authorization': f'Bearer {token_pacient}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': 'Você não tem permissão para deletar este usuário'
    }
