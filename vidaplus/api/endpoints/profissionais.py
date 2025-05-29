from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from vidaplus.security import (
    get_current_user,
    get_password_hash,
)

from vidaplus.database import get_session
from vidaplus.models.models import ProfissionalUser
from vidaplus.schemas.profissional_schema import (
    FilterPage,
    Message,
    ProfissionalUserPublic,
    ProfissionalUserSchema,
    UserList,
)
from vidaplus.utils.general import UserRole

router = APIRouter()
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[ProfissionalUser, Depends(get_current_user)]


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=ProfissionalUserPublic
)
def create_user(user: ProfissionalUserSchema, session: Session):
    db_user = session.scalar(
        select(ProfissionalUser).where(
            (ProfissionalUser.email == user.email)
            | (ProfissionalUser.crmCoren == user.crmCoren)
        )
    )

    if db_user:
        if db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already exists',
            )
        elif db_user.crmCoren == user.crmCoren:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='CRM/Coren already exists',
            )

    hashed_password = get_password_hash(user.senha)

    db_user = ProfissionalUser(
        nome=user.nome,
        email=user.email,
        senha=hashed_password,
        telefone=user.telefone,
        crmCoren=user.crmCoren,
        especialidade=user.especialidade,
        horario_atendimento=user.horario_atendimento,
        biografia=user.biografia,
        tipo=user.tipo,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/', response_model=UserList)
def get_users(session: Session, filter_users: Annotated[FilterPage, Query()]):
    profissionais = session.scalars(
        select(ProfissionalUser)
        .where(ProfissionalUser.tipo == UserRole.PROFISSIONAL)
        .offset(filter_users.offset)
        .limit(filter_users.limit)
    ).all()
    return {'profissionais': profissionais}


@router.get('/{user_id}', response_model=ProfissionalUserPublic)
def get_user(user_id: int, session: Session):
    user = session.get(ProfissionalUser, user_id)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return user


@router.put('/{user_id}', response_model=ProfissionalUserPublic)
def update_user(
    user_id: int,
    user: ProfissionalUserSchema,
    session: Session,
    current_user: CurrentUser,
):
    if not current_user.is_superuser and current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Você não tem permissão para atualizar este usuário',
        )

    user_to_update = session.get(ProfissionalUser, user_id)
    if not user_to_update:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    try:
        user_to_update.nome = user.nome
        user_to_update.email = user.email
        user_to_update.senha = get_password_hash(user.senha)
        user_to_update.telefone = user.telefone
        user_to_update.crmCoren = user.crmCoren
        user_to_update.especialidade = user.especialidade
        user_to_update.horario_atendimento = user.horario_atendimento
        user_to_update.biografia = user.biografia
        user_to_update.tipo = user.tipo
        user_to_update.is_active = user.is_active
        user_to_update.is_superuser = user.is_superuser

        session.commit()
        session.refresh(user_to_update)

        return user_to_update
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='CRM/Coren or Email already exists',
        )


@router.delete('/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session, current_user: CurrentUser):
    if not current_user.is_superuser and current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Você não tem permissão para deletar este usuário',
        )

    user_to_delete = session.get(ProfissionalUser, user_id)
    if not user_to_delete:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado',
        )

    session.delete(user_to_delete)
    session.commit()

    return {'message': 'User deleted'}
