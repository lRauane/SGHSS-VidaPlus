from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Annotated
from vidaplus.database import get_session
from vidaplus.schemas.prescricao_schema import (
    PrescricaoSchema,
    PrescricaoSchemaPublic,
    PrescricaoList,
)
from vidaplus.security import (
    get_current_user,
)
from vidaplus.schemas.schemas import FilterPage
from vidaplus.models.models import (
    Prescricao,
    PacienteUser,
    ProfissionalUser,
    Prontuario,
    BaseUser,
)

router = APIRouter()
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[BaseUser, Depends(get_current_user)]


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=PrescricaoSchemaPublic
)
def create_prescricao(
    prescricao: PrescricaoSchema, session: Session, current_user: CurrentUser
):
    paciente_id = session.scalar(
        select(PacienteUser).where(PacienteUser.id == prescricao.paciente_id)
    )
    profissional_id = session.scalar(
        select(ProfissionalUser).where(
            ProfissionalUser.id == prescricao.profissional_id,
        )
    )
    prontuario_id = session.scalar(
        select(Prontuario).where(Prontuario.id == prescricao.prontuario_id)
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

    if (
        not current_user.is_superuser
        and current_user.id != prescricao.profissional_id
    ):
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Você não tem permissão para criar esta prescrição',
        )

    db_prescricao = Prescricao(
        data=prescricao.data,
        paciente_id=prescricao.paciente_id,
        profissional_id=prescricao.profissional_id,
        prontuario_id=prescricao.prontuario_id,
        tipo_prescricao=prescricao.tipo_prescricao,
        medicamentos=prescricao.medicamentos,
        observacao=prescricao.observacao,
    )

    session.add(db_prescricao)
    session.commit()
    session.refresh(db_prescricao)
    return db_prescricao


@router.get('/', response_model=PrescricaoList)
def get_prescricoes(
    session: Session,
    filter_prescricoes: Annotated[FilterPage, Query()],
    current_user: CurrentUser,
):
    db_prescricoes = session.scalars(
        select(Prescricao)
        .order_by(Prescricao.data.desc())
        .offset(filter_prescricoes.offset)
        .limit(filter_prescricoes.limit)
    ).all()

    if not current_user.is_superuser:
        db_prescricoes = [
            prescricao
            for prescricao in db_prescricoes
            if current_user.id
            in (prescricao.paciente_id, prescricao.profissional_id)
        ]

    return {'prescricoes': db_prescricoes}


@router.get('/{prescricao_id}', response_model=PrescricaoSchemaPublic)
def get_prescricao(
    prescricao_id: int, session: Session, current_user: CurrentUser
):
    db_prescricao = session.get(Prescricao, prescricao_id)
    if not db_prescricao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Prescrição não encontrada.',
        )
    if (
        not current_user.is_superuser
        and current_user.id != db_prescricao.profissional_id
        and current_user.id != db_prescricao.paciente_id
    ):
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Você não tem permissão para acessar esta prescrição',
        )

    return db_prescricao


# outros profissionais estão editando prescrições de outros profissionais, ajustar
@router.put('/{prescricao_id}', response_model=PrescricaoSchemaPublic)
def update_prescricao(
    prescricao_id: int,
    prescricao: PrescricaoSchema,
    session: Session,
    current_user: CurrentUser,
):
    db_prescricao = session.get(Prescricao, prescricao_id)
    if not db_prescricao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Prescrição não encontrada.',
        )

    paciente_id = session.scalar(
        select(PacienteUser).where(PacienteUser.id == prescricao.paciente_id)
    )
    profissional_id = session.scalar(
        select(ProfissionalUser).where(
            ProfissionalUser.id == prescricao.profissional_id,
        )
    )
    prontuario_id = session.scalar(
        select(Prontuario).where(Prontuario.id == prescricao.prontuario_id)
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

    if (
        not current_user.is_superuser
        and current_user.id != db_prescricao.profissional_id
    ):
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Você não tem permissão para atualizar esta prescrição',
        )

    db_prescricao.data = prescricao.data
    db_prescricao.paciente_id = prescricao.paciente_id
    db_prescricao.profissional_id = prescricao.profissional_id
    db_prescricao.prontuario_id = prescricao.prontuario_id
    db_prescricao.tipo_prescricao = prescricao.tipo_prescricao
    db_prescricao.medicamentos = prescricao.medicamentos
    db_prescricao.observacao = prescricao.observacao

    session.commit()
    session.refresh(db_prescricao)

    return db_prescricao


@router.delete('/{prescricao_id}')
def delete_prescricao(
    prescricao_id: int, session: Session, current_user: CurrentUser
):
    db_prescricao = session.get(Prescricao, prescricao_id)
    if not db_prescricao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Prescrição não encontrada.',
        )

    if (
        not current_user.is_superuser
        and current_user.id != db_prescricao.profissional_id
    ):
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Você não tem permissão para deletar esta prescrição',
        )

    session.delete(db_prescricao)
    session.commit()
    return {'message': 'Prescrição excluída com sucesso.'}
