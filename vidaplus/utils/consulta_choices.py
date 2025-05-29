from enum import Enum


class Status(Enum):
    AGENDADA = 'Agendada'
    REALIZADA = 'Realizada'
    CANCELADA = 'Cancelada'
    NAO_COMPARECEU = 'Não Compareceu'
    REAGENDADA = 'Reagendada'
    PENDENTE = 'Pendente'


class TipoConsulta(Enum):
    TELECONSULTA = 'Teleconsulta'
    PRESENCIAL = 'Presencial'


class TipoItem(Enum):
    MEDICAMENTO = 'Medicamento'
    INSUMO = 'Insumo'
    EQUIPAMENTO = 'Equipamento'

