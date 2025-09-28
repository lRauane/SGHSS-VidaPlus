from fastapi import FastAPI
from vidaplus.logging_config import setup_logging
import logging

from vidaplus.api.endpoints import (
    auth,
    pacientes,
    profissionais,
    consulta,
    prescricoes,
    exame,
    prontuario,
    leitos,
    estoque,
)

logger = logging.getLogger(__name__)
# setup_logging()

app = FastAPI(
    title='VidaPlus API',
    description='A VidaPlus API é uma solução desenvolvida para gerenciar hospitais e serviços de saúde, permitindo o controle de usuários, pacientes, profissionais de saúde e autenticação. A API é construída utilizando o framework FastAPI, oferecendo endpoints organizados e documentados para facilitar a integração com sistemas externos.',
    version='0.1.0',
    openapi_url='/api/v1/openapi.json',
)

# midleware de loggins
# @app.middleware('http')
# async def log_requests(request, call_next):
#     start_time = time.time()

#     logger.info(f'Início da requisição: {request.method} {request.url}')
#     logger.debug(f'Headers: {request.headers}')

#     response = await call_next(request)

#     process_time = time.time() - start_time

#     logger.info(
#         f'Final da requisição: {request.method} {request.url} - Status code: {response.status_code} - Tempo de processamento: {process_time:.4f} segundos'
#     )

#     response.headers['X-Process-Time'] = str(process_time)

#     return response



app.include_router(pacientes.router, prefix='/pacientes', tags=['Pacientes'])
app.include_router(
    profissionais.router, prefix='/profissionais', tags=['Profissionais']
)
app.include_router(consulta.router, prefix='/consultas', tags=['Consultas'])
app.include_router(
    prescricoes.router, prefix='/prescricoes', tags=['Prescrições']
)
app.include_router(exame.router, prefix='/exames', tags=['Exames'])
app.include_router(
    prontuario.router, prefix='/prontuario', tags=['Prontuários']
)
app.include_router(leitos.router, prefix='/leitos', tags=['Leitos'])
app.include_router(estoque.router, prefix='/estoque', tags=['Estoque'])
app.include_router(auth.router, prefix='/auth/token', tags=['Tokens'])
