from __future__ import annotations
from datetime import date, datetime, time

from sqlalchemy import Date, Enum, ForeignKey, Integer, String, Time, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

from vidaplus.utils.general import Especialidade, HorarioAtendimento, UserRole
from vidaplus.utils.consulta_choices import (
    Status,
    TipoConsulta,
    TipoItem,
)
from vidaplus.utils.leitos_choices import (
    StatusLeito,
    TipoLeito,
)
from vidaplus.utils.prescricoes_choices import (
    TipoPrescricao,
)
from vidaplus.utils.exames_choices import (
    StatusExame,
    TipoExame,
)

table_registry = registry()


@table_registry.mapped_as_dataclass
class BaseUser:
    __tablename__ = 'users'
    __mapper_args__ = {
        'polymorphic_on': 'tipo',
        'polymorphic_identity': 'BASE',
    }

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    nome: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False
    )
    senha: Mapped[str] = mapped_column(String(255), nullable=False)
    telefone: Mapped[str] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), init=False
    )
    tipo: Mapped[UserRole] = mapped_column(Enum(UserRole))
    is_active: Mapped[bool] = mapped_column()
    is_superuser: Mapped[bool] = mapped_column()


@table_registry.mapped_as_dataclass
class AdminUser(BaseUser):
    __tablename__ = 'admin_users'
    __mapper_args__ = {
        'polymorphic_identity': UserRole.ADMIN.value,
    }

    id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), primary_key=True, init=False
    )


@table_registry.mapped_as_dataclass
class PacienteUser(BaseUser):
    __tablename__ = 'paciente_users'
    __mapper_args__ = {
        'polymorphic_identity': UserRole.PACIENTE.value,
    }

    id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), primary_key=True, init=False
    )
    cpf: Mapped[str] = mapped_column(
        String(14), unique=True, nullable=False, index=True
    )
    data_nascimento: Mapped[date] = mapped_column(Date)
    endereco: Mapped[str] = mapped_column(String(255))
    complemento: Mapped[str] = mapped_column(String(100), nullable=True)
    numero: Mapped[int] = mapped_column(Integer)
    bairro: Mapped[str] = mapped_column(String(100))
    cidade: Mapped[str] = mapped_column(String(100))
    estado: Mapped[str] = mapped_column(String(2))
    cep: Mapped[str] = mapped_column(String(10))


@table_registry.mapped_as_dataclass
class ProfissionalUser(BaseUser):
    __tablename__ = 'profissional_users'
    __mapper_args__ = {
        'polymorphic_identity': UserRole.PROFISSIONAL.value,
    }

    id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), primary_key=True, init=False
    )
    crmCoren: Mapped[str] = mapped_column(
        String(10), unique=True, nullable=False, index=True
    )
    especialidade: Mapped[Especialidade] = mapped_column(Enum(Especialidade))
    biografia: Mapped[str] = mapped_column(String(255), nullable=True)
    horario_atendimento: Mapped[HorarioAtendimento] = mapped_column(
        Enum(HorarioAtendimento)
    )


@table_registry.mapped_as_dataclass
class Consulta:
    __tablename__ = 'consultas'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    data: Mapped[date] = mapped_column(Date)
    hora: Mapped[time] = mapped_column(Time)
    paciente_id: Mapped[int] = mapped_column(
        ForeignKey('paciente_users.id'), nullable=False
    )
    profissional_id: Mapped[int] = mapped_column(
        ForeignKey('profissional_users.id'), nullable=False
    )
    prontuario_id: Mapped[int] = mapped_column(ForeignKey('prontuarios.id'))
    status: Mapped[Status] = mapped_column(Enum(Status), nullable=False)
    tipoConsulta: Mapped[TipoConsulta] = mapped_column(
        Enum(TipoConsulta), nullable=False
    )
    link: Mapped[str] = mapped_column(String(255), nullable=True)
    observacao: Mapped[str] = mapped_column(String(255), nullable=True)


@table_registry.mapped_as_dataclass
class Prescricao:
    __tablename__ = 'prescricoes'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    data: Mapped[date] = mapped_column(Date)
    paciente_id: Mapped[PacienteUser] = mapped_column(
        ForeignKey('paciente_users.id'), nullable=False
    )
    profissional_id: Mapped[ProfissionalUser] = mapped_column(
        ForeignKey('profissional_users.id'), nullable=False
    )
    prontuario_id: Mapped[int] = mapped_column(ForeignKey('prontuarios.id'))
    tipo_prescricao: Mapped[TipoPrescricao] = mapped_column(
        Enum(TipoPrescricao), nullable=False
    )
    medicamentos: Mapped[str] = mapped_column(String(255), nullable=False)
    observacao: Mapped[str] = mapped_column(String(255), nullable=True)


@table_registry.mapped_as_dataclass
class Exame:
    __tablename__ = 'exames'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    paciente_id: Mapped[int] = mapped_column(
        ForeignKey('paciente_users.id'), nullable=False
    )
    prontuario_id: Mapped[int] = mapped_column(ForeignKey('prontuarios.id'))
    data: Mapped[datetime] = mapped_column(Date)
    tipo: Mapped[TipoExame] = mapped_column(Enum(TipoExame), nullable=False)
    resultado: Mapped[str] = mapped_column(String(255), nullable=True)
    observacao: Mapped[str] = mapped_column(String(255), nullable=True)
    status: Mapped[StatusExame] = mapped_column(
        Enum(StatusExame), nullable=False
    )


@table_registry.mapped_as_dataclass
class Prontuario:
    __tablename__ = 'prontuarios'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    paciente_id: Mapped[int] = mapped_column(
        ForeignKey('paciente_users.id'), nullable=False
    )
    lista_consultas: Mapped[list['Consulta']] = relationship(
        init=False, 
        cascade='all, delete-orphan',
        lazy='selectin',
    )
    lista_prescricoes: Mapped[list['Prescricao']] = relationship(
        init=False,
        cascade='all, delete-orphan',
        lazy='selectin',
    ) 
    lista_exames: Mapped[list['Exame']] = relationship(
        init=False,
        cascade='all, delete-orphan',
        lazy='selectin',
    )


@table_registry.mapped_as_dataclass
class Leito:
    __tablename__ = 'leitos'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    numero_leito: Mapped[str] = mapped_column(String(10), nullable=False)
    paciente_id: Mapped[int] = mapped_column(
        ForeignKey('paciente_users.id'), nullable=True
    )
    tipo: Mapped[TipoLeito] = mapped_column(Enum(TipoLeito), nullable=False)
    status: Mapped[StatusLeito] = mapped_column(
        Enum(StatusLeito), nullable=False
    )


@table_registry.mapped_as_dataclass
class Estoque:
    __tablename__ = 'estoques'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    tipo_item: Mapped[TipoItem] = mapped_column(Enum(TipoItem), nullable=False)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    unidade: Mapped[str] = mapped_column(String(50), nullable=False)
    data_validade: Mapped[date] = mapped_column(Date, nullable=True)
