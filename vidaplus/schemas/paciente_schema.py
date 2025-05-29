from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from vidaplus.utils.general import UserRole


class Message(BaseModel):
    message: str


class FilterPage(BaseModel):
    offset: int = 0
    limit: int = 100


class PacienteUserSchema(BaseModel):
    nome: str = Field(example='João Silva')
    email: EmailStr = Field(example='joao.silva@example.com')
    telefone: str = Field(example='11999999999')
    senha: str = Field(example='senha_secreta')
    cpf: str = Field(example='12345678901')
    data_nascimento: date = Field(example='1990-01-01')
    endereco: str = Field(example='Rua das Flores')
    complemento: str | None = Field(example='Apto 101')
    numero: int = Field(example=123)
    cep: str = Field(example='01001000')
    cidade: str = Field(example='São Paulo')
    bairro: str = Field(example='Centro')
    estado: str = Field(example='SP')
    tipo: UserRole = Field(example=UserRole.PACIENTE.value)
    is_active: bool = Field(example=True)
    is_superuser: bool = Field(example=False)


class PacienteUserPublic(BaseModel):
    id: int = Field(example=1)
    nome: str = Field(example='João Silva')
    email: EmailStr = Field(example='joao.silva@example.com')
    telefone: str = Field(example='11999999999')
    cpf: str = Field(example='12345678901')
    data_nascimento: date = Field(example='1990-01-01')
    endereco: str = Field(example='Rua das Flores')
    complemento: str | None = Field(example='Apto 101')
    numero: int = Field(example=123)
    cep: str = Field(example='01001000')
    cidade: str = Field(example='São Paulo')
    bairro: str = Field(example='Centro')
    estado: str = Field(example='SP')
    tipo: UserRole = Field(example=UserRole.PACIENTE.value)
    is_active: bool = Field(example=True)
    is_superuser: bool = Field(example=False)

    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    pacientes: list[PacienteUserPublic]
