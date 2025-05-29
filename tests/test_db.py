from dataclasses import asdict

from sqlalchemy import select

from vidaplus.models.models import AdminUser, PacienteUser, ProfissionalUser
from vidaplus.utils.general import Especialidade, HorarioAtendimento, UserRole


def test_admin_user(session, mock_db_time):
    with mock_db_time(model=AdminUser) as time:
        new_user = AdminUser(
            nome='Admin',
            email='adm@email.com',
            telefone='123456789',
            senha='admin123',
            tipo=UserRole.ADMIN,
            is_active=True,
            is_superuser=True,
        )

        session.add(new_user)
        session.commit()

    user = session.scalar(select(AdminUser).where(AdminUser.nome == 'Admin'))

    assert asdict(user) == {
        'id': 1,
        'nome': 'Admin',
        'email': 'adm@email.com',
        'telefone': '123456789',
        'senha': 'admin123',
        'tipo': UserRole.ADMIN,
        'is_active': True,
        'is_superuser': True,
        'created_at': time,
    }


def test_paciente_user(session, mock_db_time, mock_db_date):
    with mock_db_time(model=PacienteUser) as time:
        with mock_db_date(model=PacienteUser) as date:
            new_user = PacienteUser(
                nome='João',
                email='joao@email.com',
                senha='joao123',
                telefone='987654321',
                tipo=UserRole.PACIENTE,
                is_active=True,
                is_superuser=False,
                cpf='12345678901',
                data_nascimento=date,
                endereco='Rua A',
                complemento='Apto 1',
                numero=123,
                bairro='Centro',
                cidade='São Paulo',
                estado='SP',
                cep='12345678',
            )
            session.add(new_user)
            session.commit()

    user = session.scalar(
        select(PacienteUser).where(PacienteUser.nome == 'João')
    )

    assert asdict(user) == {
        'id': 1,
        'nome': 'João',
        'email': 'joao@email.com',
        'senha': 'joao123',
        'telefone': '987654321',
        'tipo': UserRole.PACIENTE,
        'is_active': True,
        'is_superuser': False,
        'created_at': time,
        'cpf': '12345678901',
        'data_nascimento': date,
        'endereco': 'Rua A',
        'complemento': 'Apto 1',
        'numero': 123,
        'bairro': 'Centro',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'cep': '12345678',
    }


def test_profissional_user(session, mock_db_time):
    with mock_db_time(model=ProfissionalUser) as time:
        new_user = ProfissionalUser(
            nome='Maria',
            email='maria@email.com',
            senha='maria123',
            telefone='456789123',
            tipo=UserRole.PROFISSIONAL,
            is_active=True,
            is_superuser=False,
            crmCoren='054157701',
            especialidade=Especialidade.CLINICA_GERAL,
            horario_atendimento=HorarioAtendimento.PLANTAO_12H,
            biografia='Médica com 10 anos de experiência',
        )
        session.add(new_user)
        session.commit()

    user = session.scalar(
        select(ProfissionalUser).where(ProfissionalUser.nome == 'Maria')
    )

    assert asdict(user) == {
        'id': 1,
        'nome': 'Maria',
        'email': 'maria@email.com',
        'senha': 'maria123',
        'telefone': '456789123',
        'tipo': UserRole.PROFISSIONAL,
        'is_active': True,
        'is_superuser': False,
        'created_at': time,
        'crmCoren': '054157701',
        'especialidade': Especialidade.CLINICA_GERAL,
        'horario_atendimento': HorarioAtendimento.PLANTAO_12H,
        'biografia': 'Médica com 10 anos de experiência',
    }
