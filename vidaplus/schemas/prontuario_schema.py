from pydantic import BaseModel, Field, ConfigDict
from vidaplus.schemas.consulta_schema import ConsultaSchemaPublic
from vidaplus.schemas.prescricao_schema import PrescricaoSchemaPublic
from vidaplus.schemas.exame_schema import ExameSchemaPublic
from typing import List


class ProntuarioSchema(BaseModel):
    paciente_id: int = Field(example=1)


class ProntuarioSchemaPublic(BaseModel):
    id: int = Field(example=1)
    paciente_id: int = Field(example=1)
    lista_consultas: List[ConsultaSchemaPublic] = Field(default_factory=list)
    lista_prescricoes: List[PrescricaoSchemaPublic] = Field(
        default_factory=list
    )
    lista_exames: List[ExameSchemaPublic] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class ProntuarioList(BaseModel):
    prontuarios: list[ProntuarioSchemaPublic]
