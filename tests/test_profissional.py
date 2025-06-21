from http import HTTPStatus

from vidaplus.schemas.profissional_schema import ProfissionalUserPublic


def test_create_profissionais(client, token_admin):
    response = client.post(
        '/profissionais/',
        json={
            'nome': 'Maria Oliveira',
            'email': 'maria@email.com',
            'telefone': '456789123',
            'senha': 'secret',
            'especialidade': 'Clinica Geral',
            'horario_atendimento': 'Plantão (12h)',
            'crmCoren': '054157701',
            'biografia': 'Médica com 10 anos de experiência',
            'tipo': 'PROFISSIONAL',
            'is_active': True,
            'is_superuser': False,
        },
        headers={'Authorization': f'Bearer {token_admin}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 2,
        'nome': 'Maria Oliveira',
        'email': 'maria@email.com',
        'telefone': '456789123',
        'especialidade': 'Clinica Geral',
        'horario_atendimento': 'Plantão (12h)',
        'crmCoren': '054157701',
        'biografia': 'Médica com 10 anos de experiência',
        'tipo': 'PROFISSIONAL',
        'is_active': True,
        'is_superuser': False,
    }


def test_read_profissionais(client, token_admin):
    response = client.get('/profissionais/', headers={'Authorization': f'Bearer {token_admin}'})
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'profissionais': []}


def test_read_profissionais_with_profissionais(client, profissional_user, token_admin):
    user_schema = ProfissionalUserPublic.model_validate(
        profissional_user
    ).model_dump(mode='json')

    response = client.get('/profissionais/', headers={'Authorization': f'Bearer {token_admin}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'profissionais': [user_schema]}


def test_get_profissional_not_found(client, token_profissional):
    response = client.get('/profissionais/999', headers={'Authorization': f'Bearer {token_profissional}'})
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_integrity_error(client, profissional_user, token_profissional, token_admin):
    client.post(
        '/profissionais/',
        json={
            'nome': 'Fausto Example',
            'email': 'fausto@email.com',
            'senha': 'secret',
            'telefone': '123456789',
            'crmCoren': '123456789',
            'especialidade': 'Clinica Geral',
            'horario_atendimento': 'Plantão (12h)',
            'biografia': 'Médico com 10 anos de experiência',
            'tipo': 'PROFISSIONAL',
            'is_active': True,
            'is_superuser': False,
        },
        headers={'Authorization': f'Bearer {token_admin}'},
    )

    response_update = client.put(
        f'/profissionais/{profissional_user.id}',
        headers={'Authorization': f'Bearer {token_profissional}'},
        json={
            'nome': 'Fausto Example',
            'email': 'fausto@email.com',
            'senha': 'secret',
            'telefone': '123456789',
            'crmCoren': '123456744',
            'especialidade': 'Clinica Geral',
            'horario_atendimento': 'Plantão (12h)',
            'biografia': 'Médico com 10 anos de experiência',
            'tipo': 'PROFISSIONAL',
            'is_active': True,
            'is_superuser': False,
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'CRM/Coren or Email already exists'
    }


# esse teste precisa ser corrigido
def test_update_user_not_found(client, token_profissional):
    response = client.put(
        '/profissionais/999',
        headers={'Authorization': f'Bearer {token_profissional}'},
        json={
            'nome': 'Fausto Example',
            'email': 'fausto@email.com',
            'senha': 'secret',
            'telefone': '123456789',
            'crmCoren': '123456789',
            'especialidade': 'Clinica Geral',
            'horario_atendimento': 'Plantão (12h)',
            'biografia': 'Médico com 10 anos de experiência',
            'tipo': 'PROFISSIONAL',
            'is_active': True,
            'is_superuser': False,
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': 'Você não tem permissão para atualizar este usuário'
    }


def test_delete_user(client, profissional_user, token_profissional):
    response = client.delete(
        f'/profissionais/{profissional_user.id}',
        headers={'Authorization': f'Bearer {token_profissional}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


# esse teste precisa ser corrigido
def test_delete_user_not_found(client, token_profissional):
    response = client.delete(
        '/profissionais/999',
        headers={'Authorization': f'Bearer {token_profissional}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': 'Você não tem permissão para deletar este usuário'
    }
