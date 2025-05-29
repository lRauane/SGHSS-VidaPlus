from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from vidaplus.utils.prescricoes_choices import TipoPrescricao


class PrescricaoSchema(BaseModel):
    data: date = Field(example='2025-04-28')
    paciente_id: int = Field(example=1)
    profissional_id: int = Field(example=2)
    prontuario_id: int | None = Field(example=1)
    tipo_prescricao: TipoPrescricao = Field(example=TipoPrescricao.ANTIBIOTICO)
    medicamentos: str = Field(example='Medicamento A, Medicamento B')
    observacao: str | None = Field(example='Observação da prescrição')


class PrescricaoSchemaPublic(BaseModel):
    id: int = Field(example=1)
    data: date = Field(example='2025-04-28')
    paciente_id: int = Field(example=1)
    profissional_id: int = Field(example=2)
    tipo_prescricao: TipoPrescricao = Field(example=TipoPrescricao.ANTIBIOTICO)
    medicamentos: str = Field(example='Medicamento A, Medicamento B')
    observacao: str | None = Field(example='Observação da prescrição')
    model_config = ConfigDict(from_attributes=True)


class PrescricaoList(BaseModel):
    prescricoes: list[PrescricaoSchemaPublic]
