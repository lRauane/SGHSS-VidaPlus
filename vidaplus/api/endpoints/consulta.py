from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Query, Request
<<<<<<< Updated upstream
from sqlalchemy.orm import Session
=======
from sqlalchemy.ext.asyncio import AsyncSession
>>>>>>> Stashed changes
from sqlalchemy import select
from typing import Annotated
from vidaplus.database import get_session
from vidaplus.logger import get_logger
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
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[BaseUser, Depends(get_current_user)]

logger = get_logger("consultas")

@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=ConsultaSchemaPublic
)
<<<<<<< Updated upstream
def create_consulta(
=======
async def create_consulta(
>>>>>>> Stashed changes
    consulta: ConsultaSchema, session: Session, current_user: CurrentUser,
    request=Request
):
    paciente_id = await session.scalar(
        select(PacienteUser).where(PacienteUser.id == consulta.paciente_id)
    )
    profissional_id = await session.scalar(
        select(ProfissionalUser).where(
            ProfissionalUser.id == consulta.profissional_id,
        )
    )
    prontuario_id = await session.scalar(
        select(Prontuario).where(Prontuario.id == consulta.prontuario_id)
    )

    if not profissional_id:
        logger.resource_not_found(
            resource_type="profissional",
            resource_id=str(consulta.profissional_id),
            user_id=str(current_user.id),
            operation="create_consulta"
        )
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Profissional não encontrado.',
        )

    if not paciente_id:
        logger.resource_not_found(
            resource_type="paciente", 
            resource_id=str(consulta.paciente_id),
            user_id=str(current_user.id),
            operation="create_consulta"
        )
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Paciente não encontrado.',
        )
    
    if not prontuario_id:
        logger.resource_not_found(
            resource_type="prontuario",
            resource_id=str(consulta.prontuario_id),
            user_id=str(current_user.id),
            operation="create_consulta"
        )
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Prontuário não encontrado.',
        )


<<<<<<< Updated upstream
    db_consulta = session.scalar(
=======
    db_consulta = await session.scalar(
>>>>>>> Stashed changes
        select(Consulta).where(
            (Consulta.data == consulta.data)
            & (Consulta.hora == consulta.hora)
            & (Consulta.paciente_id == consulta.paciente_id)
            & (Consulta.profissional_id == consulta.profissional_id)
        )
    )

    if db_consulta:
        detail = 'Já existe uma consulta agendada para este paciente e profissional na mesma data e hora.'
        
        logger.business_conflict(
            conflict_type="agendamento_duplicado",
            details=detail,
            user_id=str(current_user.id),
            consulta_existente_id=str(db_consulta.id),
            paciente_id=str(consulta.paciente_id),
            profissional_id=str(consulta.profissional_id),
            data_consulta=consulta.data.isoformat(),
            hora_consulta=consulta.hora.isoformat()
        )
        
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=detail,
        )

    if (
        not current_user.is_superuser
        and current_user.id != consulta.profissional_id
    ):
        logger.permission_denied(
            operation="create_consulta",
            resource_id=f"profissional:{consulta.profissional_id}",
            user_id=str(current_user.id),
            reason="usuário_nao_eh_profissional_da_consulta"
        )
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
<<<<<<< Updated upstream
    session.commit()
    session.refresh(db_consulta)
=======
    await session.commit()
    await session.refresh(db_consulta)
>>>>>>> Stashed changes
    
    logger.operation_success(
        operation="create_consulta",
        resource_id=str(db_consulta.id),
        user_id=str(current_user.id),
        paciente_id=str(consulta.paciente_id),
        profissional_id=str(consulta.profissional_id)
    )

    return db_consulta


@router.get('/', response_model=ConsultaList)
async def get_consultas(
    session: Session,
    filter_consultas: Annotated[FilterPage, Query()],
    current_user: CurrentUser,
):
    db_consultas = await session.scalars(
        select(Consulta)
        .order_by(Consulta.data.desc())
        .offset(filter_consultas.offset)
        .limit(filter_consultas.limit)
    )
    db_consultas = db_consultas.all()

    if not current_user.is_superuser:
        db_consultas = [
            consulta
            for consulta in db_consultas
            if current_user.id
            in (consulta.paciente_id, consulta.profissional_id)
        ]

    return {'consultas': db_consultas}


@router.get('/{consulta_id}', response_model=ConsultaSchemaPublic)
async def get_consulta(
    consulta_id: int, session: Session, current_user: CurrentUser
):
    db_consulta = await session.get(Consulta, consulta_id)
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
async def update_consulta(
    consulta_id: int,
    consulta: ConsultaSchema,
    session: Session,
    current_user: CurrentUser,
):
    paciente_id = await session.scalar(
        select(PacienteUser).where(PacienteUser.id == consulta.paciente_id)
    )
    profissional_id = await session.scalar(
        select(ProfissionalUser).where(
            ProfissionalUser.id == consulta.profissional_id,
        )
    )
    prontuario_id = await session.scalar(
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

    db_consulta = await session.get(Consulta, consulta_id)
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

    await session.commit()
    await session.refresh(db_consulta)

    return db_consulta


@router.delete('/{consulta_id}')
async def delete_consulta(
    consulta_id: int, session: Session, current_user: CurrentUser
):
    db_consulta = await session.get(Consulta, consulta_id)
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

    await session.delete(db_consulta)
    await session.commit()

    return {'message': 'Consulta excluída com sucesso.'}
