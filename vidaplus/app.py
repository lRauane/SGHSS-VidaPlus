from fastapi import FastAPI
from vidaplus.logging_config import setup_logging

from vidaplus.api.endpoints import (
    auth,
    pacientes,
    profissionais,
    consulta,
    prescricoes,
    exame,
    prontuario,
    leitos,
)

setup_logging()

app = FastAPI(
    title='VidaPlus API',
    description='A VidaPlus API é uma solução desenvolvida para gerenciar hospitais e serviços de saúde, permitindo o controle de usuários, pacientes, profissionais de saúde e autenticação. A API é construída utilizando o framework FastAPI, oferecendo endpoints organizados e documentados para facilitar a integração com sistemas externos.',
    version='0.1.0',
    openapi_url='/api/v1/openapi.json',
)

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
app.include_router(auth.router, prefix='/auth/token', tags=['Tokens'])
