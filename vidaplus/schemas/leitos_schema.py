from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from vidaplus.utils.leitos_choices import StatusLeito, TipoLeito


class LeitosSchema(BaseModel):
    numero_leito: str = Field(example='101-A')
    paciente_id: Optional[int] = Field(example=1, default=None)
    tipo: TipoLeito = Field(example=TipoLeito.ENFERMARIA)
    status: StatusLeito = Field(example=StatusLeito.LIVRE)


class LeitosSchemaPublic(BaseModel):
    id: int
    numero_leito: str
    paciente_id: Optional[int] = Field(default=None)
    tipo: TipoLeito = Field(example=TipoLeito.ENFERMARIA)
    status: StatusLeito = Field(example=StatusLeito.LIVRE)

    model_config = ConfigDict(from_attributes=True)


class LeitosList(BaseModel):
    leitos: list[LeitosSchemaPublic]