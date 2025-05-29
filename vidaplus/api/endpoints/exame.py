from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Annotated
from vidaplus.schemas.schemas import FilterPage
from vidaplus.models.models import Exame, PacienteUser, BaseUser, Prontuario
from vidaplus.security import (
    get_current_user,
)
from vidaplus.database import get_session
from vidaplus.schemas.exame_schema import (
    ExameSchema,
    ExameSchemaPublic,
    ExameList,
)

router = APIRouter()
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[BaseUser, Depends(get_current_user)]


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=ExameSchemaPublic
)
def create_exame(
    exame: ExameSchema, session: Session, current_user: CurrentUser
):
    paciente_id = session.scalar(
        select(PacienteUser).where(PacienteUser.id == exame.paciente_id)
    )
    prontuario_id = session.scalar(
        select(Prontuario).where(Prontuario.id == exame.prontuario_id)
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

    db_exame = session.scalar(
        select(Exame).where(
            (Exame.data == exame.data)
            & (Exame.paciente_id == exame.paciente_id)
        )
    )

    if db_exame:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Já existe um exame agendado para este paciente na mesma data.',
        )

    if not current_user.is_superuser:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Apenas profissionais podem criar exames.',
        )

    db_exame = Exame(
        paciente_id=exame.paciente_id,
        prontuario_id=exame.prontuario_id,
        data=exame.data,
        tipo=exame.tipo,
        status=exame.status,
        resultado=exame.resultado,
        observacao=exame.observacao,
    )
    session.add(db_exame)
    session.commit()
    session.refresh(db_exame)

    return db_exame


@router.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=ExameList,
)
def get_exames(
    session: Session,
    filter_exames: Annotated[FilterPage, Query()],
    current_user: CurrentUser,
):
    db_exames = session.scalars(
        select(Exame)
        .order_by(Exame.data.desc())
        .offset(filter_exames.offset)
        .limit(filter_exames.limit)
    ).all()

    if not current_user.is_superuser:
        db_exames = [
            exame
            for exame in db_exames
            if current_user.id == exame.paciente_id
        ]

    return {'exames': db_exames}


@router.get(
    '/{exame_id}',
    response_model=ExameSchemaPublic,
)
def get_exame(exame_id: int, session: Session, current_user: CurrentUser):
    db_exame = session.get(Exame, exame_id)

    if not db_exame:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Exame não encontrado.',
        )

    if (
        not current_user.is_superuser
        and current_user.id != db_exame.paciente_id
    ):
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Você não tem permissão para acessar este exame',
        )

    return db_exame


@router.put('/{exame_id}', response_model=ExameSchemaPublic)
def update_exame(
    exame_id: int,
    exame: ExameSchema,
    session: Session,
    current_user: CurrentUser,
):
    pacient_id = session.scalar(
        select(PacienteUser).where(PacienteUser.id == exame.paciente_id)
    )
    prontuario_id = session.scalar(
        select(Prontuario).where(Prontuario.id == exame.prontuario_id)
    )

    if not pacient_id:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Paciente não encontrado.',
        )

    if not prontuario_id:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Prontuário não encontrado.',
        )

    db_exame = session.get(Exame, exame_id)

    if not db_exame:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Exame não encontrado.',
        )

    if not current_user.is_superuser:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Você não tem permissão para atualizar este exame',
        )

    db_exame.paciente_id = exame.paciente_id
    db_exame.prontuario_id = exame.prontuario_id
    db_exame.data = exame.data
    db_exame.tipo = exame.tipo
    db_exame.resultado = exame.resultado
    db_exame.observacao = exame.observacao
    db_exame.status = exame.status

    session.commit()
    session.refresh(db_exame)
    return db_exame


@router.delete('/{exame_id}')
def delete_exame(exame_id: int, session: Session, current_user: CurrentUser):
    db_exame = session.get(Exame, exame_id)

    if not db_exame:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Exame não encontrado.',
        )

    if (
        not current_user.is_superuser
        and current_user.id != db_exame.paciente_id
    ):
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Você não tem permissão para deletar este exame',
        )

    session.delete(db_exame)
    session.commit()

    return {'message': 'Exame deletado com sucesso.'}
