from http import HTTPStatus
# from vidaplus.schemas.consulta_schema import ConsultaSchemaPublic


def test_create_consulta(client, token_profissional, profissional_user, paciente_user, prontuario_user):
    response = client.post(
        '/consultas/',
        json={
            'data': "2025-04-28",
            'hora': "14:00",
            'paciente_id': paciente_user.id,
            'profissional_id': profissional_user.id,
            'prontuario_id': prontuario_user.id,
            'status': "Agendada",
            'tipoConsulta': "Teleconsulta",
            'link': "https://example.com/consulta",
            'observacao': "Consulta de rotina",
        },
        headers={'Authorization': f'Bearer {token_profissional}'}
    )
    
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'data': "2025-04-28",
        'hora': "14:00:00",
        'paciente_id': paciente_user.id,
        'profissional_id': profissional_user.id,
        'status': "Agendada",
        'tipoConsulta': "Teleconsulta",
        'observacao': "Consulta de rotina",
    }

def test_create_consulta_with_invalid_profissional(client, nova_consulta, token_profissional, prontuario_user, paciente_user):
    headers = {'Authorization': f'Bearer {token_profissional}'}
    nova_consulta.profissional_id = 99999

    response = client.post(
        '/consultas/',
        json={
            "data": "2025-04-28",
            "hora": "14:00",
            "paciente_id": paciente_user.id,
            "profissional_id": nova_consulta.profissional_id,
            "prontuario_id": prontuario_user.id,
            "status": "Agendada",
            "tipoConsulta": "Teleconsulta",
            "link": "https://example.com/consulta",
            "observacao": "Consulta inicial",
        },
        headers=headers
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Profissional não encontrado.'}


def test_create_consulta_with_invalid_paciente(client, nova_consulta, token_profissional, profissional_user, prontuario_user, paciente_user):
    headers = {'Authorization': f'Bearer {token_profissional}'}
    nova_consulta.paciente_id = 99999

    response = client.post(
        '/consultas/',
        json={
            "data": "2025-04-28",
            "hora": "14:00",
            "paciente_id": nova_consulta.paciente_id,  # ID de paciente inexistente
            "profissional_id": profissional_user.id,
            "prontuario_id": prontuario_user.id,
            "status": "Agendada",
            "tipoConsulta": "Teleconsulta",
            "link": "https://example.com/consulta",
            "observacao": "Consulta inicial",
        },
        headers=headers
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Paciente não encontrado.'}

def test_get_consultas(client, token_profissional):
    headers = {'Authorization': f'Bearer {token_profissional}'}
    response = client.get('/consultas/', headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'consultas': []}


def test_create_duplicate_consulta(client, token_profissional, profissional_user, paciente_user, prontuario_user):
    response_1 = client.post(
        "/consultas/",
        json={
            "data": "2025-04-28",
            "hora": "14:00",
            "paciente_id": paciente_user.id,
            "profissional_id": profissional_user.id,
            "prontuario_id": prontuario_user.id,
            "status": "Agendada",
            "tipoConsulta": "Teleconsulta",
            "link": "https://example.com/consulta",
            "observacao": "Consulta inicial",
        },
        headers={'Authorization': f'Bearer {token_profissional}'}
    )
    assert response_1.status_code == HTTPStatus.CREATED

    response_2 = client.post(
        "/consultas/",
        json={
            "data": "2025-04-28",
            "hora": "14:00",       # Mesma hora
            "paciente_id": paciente_user.id,  # Mesmo paciente
            "profissional_id": profissional_user.id,  # Mesmo profissional
            "prontuario_id": prontuario_user.id,
            "status": "Agendada",
            "tipoConsulta": "Teleconsulta",
            "link": "https://example.com/consulta",
            "observacao": "Consulta duplicada",
        },
        headers={'Authorization': f'Bearer {token_profissional}'}
    )

    assert response_2.status_code == HTTPStatus.CONFLICT
    assert response_2.json() == {
        "detail": "Já existe uma consulta agendada para este paciente e profissional na mesma data e hora."
    }
