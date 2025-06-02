from pydantic import BaseModel, Field, ConfigDict
from vidaplus.utils.consulta_choices import TipoItem
from datetime import date

class EstoqueSchema(BaseModel):
    tipo_item: TipoItem = Field(example=TipoItem.MEDICAMENTO)
    nome: str = Field(example='Paracetamol')
    quantidade: int = Field(example=100)
    unidade: str = Field(example='mg')
    data_validade: date = Field(example='2025-12-31')


class EstoqueSchemaPublic(BaseModel):
    id: int
    tipo_item: TipoItem = Field(example=TipoItem.MEDICAMENTO)
    nome: str = Field(example='Paracetamol')
    quantidade: int = Field(example=100)
    unidade: str = Field(example='mg')
    data_validade: date = Field(example='2025-12-31')

    model_config = ConfigDict(from_attributes=True)


class EstoqueList(BaseModel):
    estoques: list[EstoqueSchemaPublic]