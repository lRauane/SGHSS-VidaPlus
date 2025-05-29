from pydantic import BaseModel, Field, ConfigDict
from datetime import date, time
from vidaplus.utils.consulta_choices import Status, TipoConsulta


class ConsultaSchema(BaseModel):
    data: date = Field(example='2025-04-28')
    hora: time = Field(example='14:00')
    paciente_id: int = Field(example=1)
    profissional_id: int = Field(example=2)
    prontuario_id: int | None = Field(example=1)
    status: Status = Field(example=Status.AGENDADA)
    tipoConsulta: TipoConsulta = Field(example=TipoConsulta.TELECONSULTA)
    link: str | None = Field(example='https://example.com/consulta')
    observacao: str | None = Field(example='Observação da consulta')


class ConsultaSchemaPublic(BaseModel):
    id: int = Field(example=1)
    data: date = Field(example='2025-04-28')
    hora: time = Field(example='14:00')
    paciente_id: int = Field(example=1)
    profissional_id: int = Field(example=2)
    status: Status = Field(example=Status.AGENDADA)
    tipoConsulta: TipoConsulta = Field(example=TipoConsulta.TELECONSULTA)
    observacao: str | None = Field(example='Observação da consulta')
    model_config = ConfigDict(from_attributes=True)


class ConsultaList(BaseModel):
    consultas: list[ConsultaSchemaPublic]
