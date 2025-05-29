# from http import HTTPStatus
# from vidaplus.schemas.consulta_schema import ConsultaSchemaPublic


# def test_create_consulta(client, nova_consulta, token_profissional):
#     headers = {'Authorization': f'Bearer {token_profissional}'}
#     response = client.post('/consultas/', json=nova_consulta, headers=headers)
#     print(response.json())
#     assert response.status_code == HTTPStatus.CREATED


# def test_create_consulta_with_invalid_profissional(
#     client, nova_consulta, token_profissional
# ):
#     headers = {'Authorization': f'Bearer {token_profissional}'}
#     nova_consulta['profissional_id'] = 99999
#     response = client.post('/consultas/', json=nova_consulta, headers=headers)
#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'Profissional não encontrado.'}


# def test_create_consulta_with_invalid_paciente(
#     client, nova_consulta, token_profissional
# ):
#     headers = {'Authorization': f'Bearer {token_profissional}'}
#     nova_consulta['paciente_id'] = 99999
#     response = client.post('/consultas/', json=nova_consulta, headers=headers)
#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'Paciente não encontrado.'}


# def test_get_consultas(client, token_profissional):
#     headers = {'Authorization': f'Bearer {token_profissional}'}
#     response = client.get('/consultas/', headers=headers)
#     assert response.status_code == HTTPStatus.OK
#     assert response.json() == {'consultas': []}


# def test_get_consulta(client, nova_consulta, token_profissional):
#     headers = {'Authorization': f'Bearer {token_profissional}'}
#     response_create = client.post(
#         '/consultas/', json=nova_consulta, headers=headers
#     )
#     assert response_create.status_code == HTTPStatus.CREATED
#     consulta_criada = response_create.json()

#     consulta_schema = ConsultaSchemaPublic.model_validate(
#         consulta_criada
#     ).model_dump(mode='json')

#     response_get = client.get(
#         f'/consultas/{consulta_criada["id"]}', headers=headers
#     )
#     print(response_get.json())
#     assert response_get.status_code == HTTPStatus.OK
#     assert response_get.json() == consulta_schema


# def test_update_consulta(client, nova_consulta):
#     client.post("/consultas/", json=nova_consulta)

#     response_update = client.put(
#         f"/consultas/{nova_consulta.id}",
#         json={
#             "data": "2023-10-01",
#             "hora": "10:00",
#             "paciente_id": 1,
#             "profissional_id": 1,
#             "status": "AGENDADA",
#             "tipoConsulta": "TELEMEDICINA",
#             "link": "https://example.com/consulta",
#             "observacao": "Observação atualizada",
#         },
#     )
#     assert response_update.status_code == HTTPStatus.OK
