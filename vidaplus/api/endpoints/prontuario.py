from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from vidaplus.models.models import Prontuario, BaseUser, PacienteUser
from vidaplus.schemas.prontuario_schema import (
    ProntuarioSchema,
    ProntuarioSchemaPublic,
    ProntuarioList,
)
from sqlalchemy import select
from typing import Annotated
from vidaplus.security import (
    get_current_user,
)
from vidaplus.database import get_session
from vidaplus.schemas.schemas import FilterPage


router = APIRouter()
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[BaseUser, Depends(get_current_user)]


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=ProntuarioSchemaPublic,
)
async def create_prontuario(
    prontuario: ProntuarioSchema,
    session: Session,
    current_user: CurrentUser,
):
    paciente_id = await session.scalar(
        select(PacienteUser).where(PacienteUser.id == prontuario.paciente_id)
    )
    if not paciente_id:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Paciente não encontrado.',
        )

    db_prontuario = await session.scalar(
        select(Prontuario).where(
            Prontuario.paciente_id == prontuario.paciente_id
        )
    )

    if db_prontuario:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Prontuário já existe para este paciente.',
        )

    if not current_user.is_superuser:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Apenas usuários com permissão de administrador podem criar prontuários.',
        )
    
    db_prontuario = Prontuario(
        paciente_id=prontuario.paciente_id,
    )

    session.add(db_prontuario)
    await session.commit()
    await session.refresh(db_prontuario)

    return db_prontuario


@router.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=ProntuarioList,
)
async def get_prontuarios(
    session: Session,
    filter_prontuario: Annotated[FilterPage, Query()],
    current_user: CurrentUser,
):
    result = await session.execute(
        select(Prontuario)
        .options(
            joinedload(Prontuario.lista_consultas),
            joinedload(Prontuario.lista_prescricoes),
            joinedload(Prontuario.lista_exames),
        )
        .offset(filter_prontuario.offset)
        .limit(filter_prontuario.limit)
    )
    db_prontuarios = result.unique().scalars().all()

    if not db_prontuarios:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Nenhum prontuário encontrado.',
        )

    if not current_user.is_superuser:
        db_prontuarios = [
            prontuario
            for prontuario in db_prontuarios
            if current_user.id == prontuario.paciente_id
        ]

    return {
        'prontuarios': db_prontuarios,
    }

@router.get(
    '/{prontuario_id}',
    response_model=ProntuarioSchemaPublic,
)
async def get_prontuario(
    prontuario_id: int,
    session: Session,
    current_user: CurrentUser,
):
    db_prontuario = await session.get(Prontuario, prontuario_id)

    if not db_prontuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Prontuário não encontrado.',
        )

    if not current_user.is_superuser:
        if current_user.id != db_prontuario.paciente_id:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail='Você não tem permissão para acessar este prontuário.',
            )
        
    return db_prontuario