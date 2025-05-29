from enum import Enum


class StatusExame(Enum):
    AGUARDANDO = 'Aguardando'
    REALIZADO = 'Realizado'
    CONCLUIDO = 'Concluído'
    CANCELADO = 'Cancelado'


class TipoExame(Enum):
    HEMOGRAMA = 'Hemograma'
    RAIO_X = 'Raio-X'
    ULTRASSOM = 'Ultrassom'
    TOMOGRAFIA = 'Tomografia'
    RESSONANCIA = 'Ressonância'
    ELETROCARDIOGRAMA = 'Eletrocardiograma'
    GLICEMIA = 'Glicemia'
    COLESTEROL = 'Colesterol'