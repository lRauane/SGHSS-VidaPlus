import logging
from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Annotated
from vidaplus.database import get_session
from vidaplus.schemas.consulta_schema import (
    ConsultaSchema,
    ConsultaSchemaPublic,
    ConsultaList,
)
from vidaplus.schemas.schemas import FilterPage
from vidaplus.security import (
    get_current_user,
)
from vidaplus.models.models import (
    Consulta,
    PacienteUser,
    ProfissionalUser,
    Prontuario,
    BaseUser,
)

router = APIRouter()
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[BaseUser, Depends(get_current_user)]

logger = logging.getLogger("vidaplus")


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=ConsultaSchemaPublic
)
def create_consulta(
    consulta: ConsultaSchema, session: Session, current_user: CurrentUser
):
    paciente_id = session.scalar(
        select(PacienteUser).where(PacienteUser.id == consulta.paciente_id)
    )
    profissional_id = session.scalar(
        select(ProfissionalUser).where(
            ProfissionalUser.id == consulta.profissional_id,
        )
    )
    prontuario_id = session.scalar(
        select(Prontuario).where(Prontuario.id == consulta.prontuario_id)
    )

    if not profissional_id:
        logger.error("Profissional não encontrado: %s", consulta.profissional_id)
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Profissional não encontrado.',
        )

    if not paciente_id:
        logger.error("Paciente não encontrado: %s", consulta.paciente_id)
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Paciente não encontrado.',
        )
    
    if not prontuario_id:
        logger.error(
            "Prontuário não encontrado: %s", consulta.prontuario_id
        )
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Prontuário não encontrado.',
        )

    db_consulta = session.scalar(
        select(Consulta).where(
            (Consulta.data == consulta.data)
            & (Consulta.hora == consulta.hora)
            & (Consulta.paciente_id == consulta.paciente_id)
            & (Consulta.profissional_id == consulta.profissional_id)
        )
    )

    if db_consulta:
        detail='Já existe uma consulta agendada para este paciente e profissional na mesma data e hora.'
        
        logger.error(
            f"{detail}: %s", db_consulta.id
        )
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=detail,
        )

    if (
        not current_user.is_superuser
        and current_user.id != consulta.profissional_id
    ):
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Você não tem permissão para criar esta consulta',
        )

    db_consulta = Consulta(
        data=consulta.data,
        hora=consulta.hora,
        paciente_id=consulta.paciente_id,
        profissional_id=consulta.profissional_id,
        prontuario_id=consulta.prontuario_id,
        status=consulta.status,
        tipoConsulta=consulta.tipoConsulta,
        link=consulta.link,
        observacao=consulta.observacao,
    )

    session.add(db_consulta)
    session.commit()
    session.refresh(db_consulta)
    logger.info("Consulta criada com sucesso: %s", db_consulta.id)
    return db_consulta


@router.get('/', response_model=ConsultaList)
def get_consultas(
    session: Session,
    filter_consultas: Annotated[FilterPage, Query()],
    current_user: CurrentUser,
):
    db_consultas = session.scalars(
        select(Consulta)
        .order_by(Consulta.data.desc())
        .offset(filter_consultas.offset)
        .limit(filter_consultas.limit)
    ).all()

    if not current_user.is_superuser:
        db_consultas = [
            consulta
            for consulta in db_consultas
            if current_user.id
            in (consulta.paciente_id, consulta.profissional_id)
        ]

    return {'consultas': db_consultas}


@router.get('/{consulta_id}', response_model=ConsultaSchemaPublic)
def get_consulta(
    consulta_id: int, session: Session, current_user: CurrentUser
):
    db_consulta = session.get(Consulta, consulta_id)
    if not db_consulta:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Consulta não encontrada.',
        )
    if (
        not current_user.is_superuser
        and current_user.id != db_consulta.profissional_id
        and current_user.id != db_consulta.paciente_id
    ):
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Você não tem permissão para acessar esta consulta',
        )

    return db_consulta


# outros profissionais estão editando consultas de outros profissionais, ajustar
@router.put('/{consulta_id}', response_model=ConsultaSchemaPublic)
def update_consulta(
    consulta_id: int,
    consulta: ConsultaSchema,
    session: Session,
    current_user: CurrentUser,
):
    paciente_id = session.scalar(
        select(PacienteUser).where(PacienteUser.id == consulta.paciente_id)
    )
    profissional_id = session.scalar(
        select(ProfissionalUser).where(
            ProfissionalUser.id == consulta.profissional_id,
        )
    )
    prontuario_id = session.scalar(
        select(Prontuario).where(Prontuario.id == consulta.prontuario_id)
    )

    if not profissional_id:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Profissional não encontrado.',
        )

    if not paciente_id:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Paciente não encontrado.',
        )
    
    if not prontuario_id:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Prontuário não encontrado.',
        )

    db_consulta = session.get(Consulta, consulta_id)
    if not db_consulta:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Consulta não encontrada.',
        )

    if (
        not current_user.is_superuser
        and current_user.id != db_consulta.profissional_id
        and current_user.id != db_consulta.paciente_id
    ):
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Você não tem permissão para atualizar esta consulta',
        )

    db_consulta.data = consulta.data
    db_consulta.hora = consulta.hora
    db_consulta.paciente_id = consulta.paciente_id
    db_consulta.profissional_id = consulta.profissional_id
    db_consulta.prontuario_id = consulta.prontuario_id
    db_consulta.status = consulta.status
    db_consulta.tipoConsulta = consulta.tipoConsulta
    db_consulta.link = consulta.link
    db_consulta.observacao = consulta.observacao

    session.commit()
    session.refresh(db_consulta)

    return db_consulta


@router.delete('/{consulta_id}')
def delete_consulta(
    consulta_id: int, session: Session, current_user: CurrentUser
):
    db_consulta = session.get(Consulta, consulta_id)
    if not db_consulta:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Consulta não encontrada.',
        )

    if (
        not current_user.is_superuser
        and current_user.id != db_consulta.profissional_id
    ):
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Você não tem permissão para deletar esta consulta',
        )

    session.delete(db_consulta)
    session.commit()

    return {'message': 'Consulta excluída com sucesso.'}
