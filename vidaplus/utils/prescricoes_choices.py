from enum import Enum


class TipoPrescricao(Enum):
    MEDICACAO_CONTINUA = 'Medicação Contínua'
    MEDICACAO_TEMPORARIA = 'Medicação Temporária'
    ANTIBIOTICO = 'Antibiótico'
    ANALGESICO = 'Analgesico'
    RECEITA_ESPECIAL = 'Receita Especial'