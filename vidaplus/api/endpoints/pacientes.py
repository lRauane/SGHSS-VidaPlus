from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from vidaplus.database import get_session
from vidaplus.models.models import PacienteUser
from vidaplus.schemas.paciente_schema import (
    FilterPage,
    Message,
    PacienteUserPublic,
    PacienteUserSchema,
    UserList,
)
from vidaplus.security import (
    get_current_user,
    get_password_hash,
)
from vidaplus.utils.general import UserRole

router = APIRouter()
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[PacienteUser, Depends(get_current_user)]


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=PacienteUserPublic
)
def create_user(user: PacienteUserSchema, session: Session, current_user: CurrentUser):
    
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Apenas usuários com permissão de administrador podem criar pacientes.',
        )
    
    db_user = session.scalar(
        select(PacienteUser).where(
            (PacienteUser.email == user.email) | (PacienteUser.cpf == user.cpf)
        )
    )

    if db_user:
        if db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already exists',
            )
        elif db_user.cpf == user.cpf:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='CPF already exists',
            )

    hashed_password = get_password_hash(user.senha)

    db_user = PacienteUser(
        nome=user.nome,
        email=user.email,
        senha=hashed_password,
        telefone=user.telefone,
        cpf=user.cpf,
        data_nascimento=user.data_nascimento,
        endereco=user.endereco,
        complemento=user.complemento,
        numero=user.numero,
        bairro=user.bairro,
        cidade=user.cidade,
        estado=user.estado,
        cep=user.cep,
        tipo=user.tipo,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/', response_model=UserList)
def get_users(session: Session, filter_users: Annotated[FilterPage, Query()], current_user: CurrentUser):
    pacientes = session.scalars(
        select(PacienteUser)
        .where(PacienteUser.tipo == UserRole.PACIENTE)
        .offset(filter_users.offset)
        .limit(filter_users.limit)
    ).all()

    if not current_user.is_superuser:
        pacientes = [
            paciente for paciente in pacientes if paciente.id == current_user.id
        ]
    
    return {'pacientes': pacientes}


@router.get('/{user_id}', response_model=PacienteUserPublic)
def get_user(user_id: int, session: Session, current_user: CurrentUser):
    user = session.get(PacienteUser, user_id)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    
    if not current_user.is_superuser and current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Você não tem permissão para acessar este usuário',
        )

    return user


@router.put('/{user_id}', response_model=PacienteUserPublic)
def update_user(
    user_id: int,
    user: PacienteUserSchema,
    session: Session,
    current_user: CurrentUser,
):
    if not current_user.is_superuser and current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Você não tem permissão para atualizar este usuário',
        )

    user_to_update = session.get(PacienteUser, user_id)
    if not user_to_update:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    try:
        user_to_update.nome = user.nome
        user_to_update.email = user.email
        user_to_update.senha = get_password_hash(user.senha)
        user_to_update.telefone = user.telefone
        user_to_update.cpf = user.cpf
        user_to_update.data_nascimento = user.data_nascimento
        user_to_update.endereco = user.endereco
        user_to_update.complemento = user.complemento
        user_to_update.numero = user.numero
        user_to_update.bairro = user.bairro
        user_to_update.cidade = user.cidade
        user_to_update.estado = user.estado
        user_to_update.cep = user.cep
        user_to_update.tipo = user.tipo
        user_to_update.is_active = user.is_active
        user_to_update.is_superuser = user.is_superuser

        session.commit()
        session.refresh(user_to_update)

        return user_to_update
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='CPF or Email already exists',
        )


@router.delete('/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session, current_user: CurrentUser):
    if not current_user.is_superuser and current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Você não tem permissão para deletar este usuário',
        )

    user_to_delete = session.get(PacienteUser, user_id)
    if not user_to_delete:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado',
        )

    session.delete(user_to_delete)
    session.commit()

    return {'message': 'User deleted'}
