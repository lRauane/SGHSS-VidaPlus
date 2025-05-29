from enum import Enum


class TipoLeito(Enum):
    UTI = 'UTI'
    ENFERMARIA = 'Enfermaria'
    EMERGENCIA = 'Emergência'
    ISOLAMENTO = 'Isolamento'
    SEMI_INTENSIVO = 'Semi-Intensivo'
    PEDIATRICO = 'Pediátrico'
    NEONATAL = 'Neonatal'
    PSIQUIATRICO = 'Psiquiátrico'


class StatusLeito(Enum):
    OCUPADO = 'Ocupado'
    LIVRE = 'Livre'
    RESERVADO = 'Reservado'
    EM_MANUTENCAO = 'Em Manutenção'