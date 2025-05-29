from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from vidaplus.models.models import Leito, BaseUser
from vidaplus.schemas.leitos_schema import (
    LeitosSchema,
    LeitosSchemaPublic,
    LeitosList,
)
from sqlalchemy import select
from typing import Annotated
from vidaplus.security import (
    get_current_user,
)
from vidaplus.database import get_session
from vidaplus.schemas.schemas import FilterPage

router = APIRouter()
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[BaseUser, Depends(get_current_user)]

@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=LeitosSchemaPublic,
)
def create_leito(
    leito: LeitosSchema,
    session: Session,
    current_user: CurrentUser,
):
    db_leito = session.scalar(
        select(Leito).where(Leito.numero_leito == leito.numero_leito)
    )

    if db_leito:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Leito já existe.',
        )

    if not current_user.is_superuser:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Apenas usuários com permissão de administrador podem criar leitos.',
        )

    if leito.status == 'Livre' and leito.paciente_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Leito livre não pode ter paciente associado.',
        )

    db_leito = Leito(
        numero_leito=leito.numero_leito,
        paciente_id=leito.paciente_id,
        tipo=leito.tipo,
        status=leito.status,
    )
    session.add(db_leito)
    session.commit()
    session.refresh(db_leito)

    return db_leito


@router.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=LeitosList,
)
def get_leitos(
    session: Session,
    filter_leitos: Annotated[FilterPage, Query()],
    current_user: CurrentUser,
):
    db_leitos = session.scalars(
        select(Leito)
        .offset(filter_leitos.offset)
        .limit(filter_leitos.limit)
    ).all()

    if not current_user.is_superuser:
        db_leitos = [
            leito
            for leito in db_leitos
            if current_user.id == leito.paciente_id
        ]

    return {'leitos': db_leitos}


@router.get(
    '/{leito_id}',
    response_model=LeitosSchemaPublic,
)
def get_leito(
    leito_id: int,
    session: Session,
    current_user: CurrentUser,
):
    db_leito = session.get(Leito, leito_id)

    if not db_leito:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Leito não encontrado.',
        )

    if not current_user.is_superuser:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Você não tem permissão para acessar este leito.',
        )

    return db_leito


@router.put(
    '/{leito_id}',
    response_model=LeitosSchemaPublic,
)
def update_leito(
    leito_id: int,
    leito: LeitosSchema,
    session: Session,
    current_user: CurrentUser,
):
    db_leito = session.get(Leito, leito_id)

    if not db_leito:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Leito não encontrado.',
        )

    if not current_user.is_superuser:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Você não tem permissão para acessar este leito.',
        )

    if leito.status == 'Livre' and leito.paciente_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Leito livre não pode ter paciente associado.',
        )

    db_leito.numero_leito = leito.numero_leito
    db_leito.paciente_id = leito.paciente_id
    db_leito.tipo = leito.tipo
    db_leito.status = leito.status

    session.commit()
    session.refresh(db_leito)

    return db_leito


@router.delete(
    '/{leito_id}',
)
def delete_leito(
    leito_id: int,
    session: Session,
    current_user: CurrentUser,
):
    db_leito = session.get(Leito, leito_id)

    if not db_leito:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Leito não encontrado.',
        )

    if not current_user.is_superuser:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Você não tem permissão para acessar este leito.',
        )

    session.delete(db_leito)
    session.commit()

    return {'message': 'Leito deletado com sucesso.'}