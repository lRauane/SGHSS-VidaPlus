from pydantic import BaseModel, ConfigDict, EmailStr, Field

from vidaplus.utils.general import Especialidade, HorarioAtendimento, UserRole


class Message(BaseModel):
    message: str


class FilterPage(BaseModel):
    offset: int = 0
    limit: int = 100


class ProfissionalUserSchema(BaseModel):
    nome: str = Field(example='Maria Oliveira')
    email: EmailStr = Field(example='maria@email.com')
    senha: str = Field(example='maria123')
    telefone: str = Field(example='456789123')
    crmCoren: str = Field(example='CRM-PR 67890')
    especialidade: Especialidade = Field(
        example=Especialidade.CLINICA_GERAL.value
    )
    horario_atendimento: HorarioAtendimento = Field(
        example=HorarioAtendimento.PLANTAO_12H.value
    )
    biografia: str = Field(example='Médica com 10 anos de experiência')
    tipo: UserRole = Field(example=UserRole.PROFISSIONAL.value)
    is_active: bool = Field(example=True)
    is_superuser: bool = Field(example=False)


class ProfissionalUserPublic(BaseModel):
    id: int = Field(example=1)
    nome: str = Field(example='Maria Oliveira')
    email: EmailStr = Field(example='maria@email.com')
    telefone: str = Field(example='456789123')
    especialidade: Especialidade = Field(
        example=Especialidade.CLINICA_GERAL.value
    )
    horario_atendimento: HorarioAtendimento = Field(
        example=HorarioAtendimento.PLANTAO_12H.value
    )
    crmCoren: str = Field(example='CRM-PR 67890')
    biografia: str = Field(example='Médica com 10 anos de experiência')
    tipo: UserRole = Field(example=UserRole.PROFISSIONAL.value)
    is_active: bool = Field(example=True)
    is_superuser: bool = Field(example=False)

    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    profissionais: list[ProfissionalUserPublic]
