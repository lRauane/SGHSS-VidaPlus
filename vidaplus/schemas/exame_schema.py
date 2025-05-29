from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from vidaplus.utils.exames_choices import StatusExame, TipoExame


class ExameSchema(BaseModel):
    paciente_id: int = Field(example=1)
    prontuario_id: int | None = Field(example=1)
    data: date = Field(example='2025-04-28')
    tipo: TipoExame = Field(example=TipoExame.ELETROCARDIOGRAMA)
    status: StatusExame = Field(example=StatusExame.AGUARDANDO)
    resultado: str | None = Field(example='Resultado do exame')
    observacao: str | None = Field(example='Observação do exame')
    model_config = ConfigDict(from_attributes=True)


class ExameSchemaPublic(BaseModel):
    id: int = Field(example=1)
    paciente_id: int = Field(example=1)
    data: date = Field(example='2025-04-28')
    tipo: TipoExame = Field(example=TipoExame.ELETROCARDIOGRAMA)
    status: StatusExame = Field(example=StatusExame.AGUARDANDO)
    resultado: str | None = Field(example='Resultado do exame')
    observacao: str | None = Field(example='Observação do exame')
    model_config = ConfigDict(from_attributes=True)


class ExameList(BaseModel):
    exames: list[ExameSchemaPublic]
