from enum import Enum


class UserRole(str, Enum):
    ADMIN = 'ADMIN'
    PACIENTE = 'PACIENTE'
    PROFISSIONAL = 'PROFISSIONAL'


class Especialidade(Enum):
    CLINICA_GERAL = 'Clinica Geral'
    DERMATOLOGIA = 'Dermatologia'
    GINECOLOGIA = 'Ginecologia'
    ORTOPEDIA = 'Ortopedia'
    PEDIATRIA = 'Pediatria'
    PSIQUIATRIA = 'Psiquiatria'
    PSICOLOGIA = 'Psicologia'
    NUTRICAO = 'Nutrição'
    FISIOTERAPIA = 'Fisioterapia'
    ODONTOLOGIA = 'Odontologia'


class HorarioAtendimento(Enum):
    MANHA = 'Manhã (08:00 - 12:00)'
    TARDE = 'Tarde (13:00 - 18:00)'
    NOITE = 'Noite (18:00 - 22:00)'
    INTEGRAL = 'Integral (08:00 - 22:00)'
    PLANTAO_12H = 'Plantão (12h)'
    PLANTAO_24H = 'Plantão (24h)'
