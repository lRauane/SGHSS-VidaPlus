from contextlib import contextmanager
from datetime import date, datetime, time

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy import event

from vidaplus.app import app
from vidaplus.database import get_session
from vidaplus.models.models import (
    PacienteUser,
    ProfissionalUser,
    AdminUser,
    Consulta,
    Prontuario,
    table_registry,
)
from vidaplus.security import get_password_hash


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@pytest_asyncio.fixture
async def client(session):
    async def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()


@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):
    def fake_time_handler(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_handler)

    yield time

    event.remove(model, 'before_insert', fake_time_handler)


@contextmanager
def _mock_db_date(*, model, time=date(1998, 2, 13)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'data_nascimento'):
            target.data_nascimento = time

    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def mock_db_date():
    return _mock_db_date


@pytest_asyncio.fixture
async def paciente_user(session, mock_db_date):
    with mock_db_date(model=PacienteUser) as date:
        senha = 'maria123'
        user = PacienteUser(
            nome='Maria',
            email='maria@email.com',
            senha=get_password_hash(senha),
            telefone='987654322',
            tipo='PACIENTE',
            is_active=True,
            is_superuser=False,
            cpf='98765432100',
            data_nascimento=date,
            endereco='Rua B',
            complemento='Casa',
            numero=456,
            bairro='Jardim',
            cidade='Rio de Janeiro',
            estado='RJ',
            cep='87654321',
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

        user.clean_password = senha

        return user


@pytest_asyncio.fixture
async def profissional_user(session):
    senha = 'carlos123'
    user = ProfissionalUser(
        nome='Carlos',
        email='carlos@email.com',
        senha=get_password_hash(senha),
        telefone='987654323',
        crmCoren='123456',
        especialidade='GINECOLOGIA',
        biografia='Cardiologista experiente',
        horario_atendimento='TARDE',
        tipo='PROFISSIONAL',
        is_active=True,
        is_superuser=False,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = senha

    return user


@pytest_asyncio.fixture
async def admin_user(session):
    senha = 'admin123'
    user = AdminUser(
        nome='Admin',
        email='admin@vidaplus.com',
        senha=get_password_hash(senha),
        telefone='123456789',
        tipo='ADMIN',
        is_active=True,
        is_superuser=True,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = senha
    return user


@pytest_asyncio.fixture
async def token_pacient(client, paciente_user):
    response = await client.post(
        '/auth/token',
        data={
            'username': paciente_user.email,
            'password': paciente_user.clean_password,
        },
    )
    return response.json()['access_token']


@pytest_asyncio.fixture
async def token_profissional(client, profissional_user):
    response = await client.post(
        '/auth/token',
        data={
            'username': profissional_user.email,
            'password': profissional_user.clean_password,
        },
    )
    return response.json()['access_token']


@pytest_asyncio.fixture
async def token_admin(client, admin_user):
    response = await client.post(
        '/auth/token',
        data={
            'username': admin_user.email,
            'password': admin_user.clean_password,
        },
    )
    return response.json()['access_token']


@pytest_asyncio.fixture
async def prontuario_user(paciente_user, session):
    prontuario = Prontuario(
        paciente_id=paciente_user.id,
    )

    session.add(prontuario)
    await session.commit()
    await session.refresh(prontuario)
    return prontuario
    

@pytest_asyncio.fixture
async def nova_consulta(paciente_user, profissional_user, prontuario_user, session):
    consulta = Consulta(
        data=date(2025, 4, 28),
        hora=time(14, 0),
        paciente_id=paciente_user.id,
        profissional_id=profissional_user.id,
        prontuario_id=prontuario_user.id,
        status="AGENDADA",
        tipoConsulta="PRESENCIAL",
        link="https://example.com/consulta",
        observacao="Observação da consulta"
    )

    session.add(consulta)
    await session.commit()
    await session.refresh(consulta)

    return consulta
